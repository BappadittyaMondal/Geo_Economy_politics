"""
Headless Audio Stream & Media Transcript Connector.
Bypasses dynamic client-side JavaScript lockouts on YouTube, podcasts, and video URLs,
providing headless transcript extraction, timestamped parsing, and automated ClaimItem normalization.
"""

import hashlib
import re
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

from .transcript_engine import TranscriptResult, TranscriptSegment, VideoTranscriptEngine
from .url_parser import YouTubeURLParser
from ..ingestion.models import ClaimItem, ClaimType
from ..core.query_parser import QueryParser
from ..ingestion.telemetry_adapter import MacroTelemetryAdapter
from ..core.models import EpistemicTier
from ..storage.event_store import EventStore


class AudioStreamMetadata(BaseModel):
    """Metadata for an external audio/video media stream."""
    media_id: str
    source_url: str
    source_type: str = "youtube"  # 'youtube', 'podcast', 'stream', 'audio_file'
    title: Optional[str] = None
    duration_seconds: Optional[float] = None
    language: str = "en"


class AudioTranscript(BaseModel):
    """Structured transcript output from an audio or video stream."""
    media_id: str
    source_url: Optional[str] = None
    language: str = "en"
    full_text: str = ""
    segments: List[TranscriptSegment] = Field(default_factory=list)
    is_degraded: bool = False
    is_simulated: bool = False
    extraction_method: str = "caption_stream"


class DiscourseVectorDecomposition(BaseModel):
    """Quantitative 4-vector decomposition of a strategic speech or media transcript."""
    factuality_ratio: float
    ideology_intensity: float
    agenda_potency: float
    omission_penalty: float
    dominant_ideology: str
    primary_agenda_type: str
    identified_factual_anchors: List[str] = Field(default_factory=list)
    identified_ideological_tokens: List[str] = Field(default_factory=list)
    identified_actionable_demands: List[str] = Field(default_factory=list)
    critical_omitted_counterweights: List[str] = Field(default_factory=list)
    discourse_classification: str = "MIXED_CRITICAL_DISCOURSE"


class DiscourseDecompositionEngine:
    """Decomposes strategic monologues and media transcripts into 4 distinct epistemic vectors."""

    FACTUAL_KEYWORDS: List[str] = [
        "act", "section", "court", "statute", "amendment", "brier", "crore", "rupee", "dollar",
        "percent", "%", "1947", "1950", "1953", "1963", "1974", "1987", "1991", "1992", "1998",
        "2015", "2018", "2021", "2023", "2024", "kashinath", "sarbananda", "bigha", "exam", "marks",
        "engineer", "vacancy", "gdp", "taxpayer", "subsidy", "budget", "gazette", "notification"
    ]

    IDEOLOGICAL_KEYWORDS: List[str] = [
        "merit", "jizya", "appeasement", "caste", "decolonial", "hindutva", "secular", "left",
        "right", "marxist", "trad", "dharma", "social justice", "savarna", "bahujan", "victimhood",
        "leech", "bribe", "traitor", "demonic", "blunder", "colonized", "freebies", "free", "welfarism",
        "general category", "caste reservation", "safeguard"
    ]

    AGENDA_KEYWORDS: List[str] = [
        "vote", "boycott", "punish", "elect", "protest", "mobilize", "abuse", "strike",
        "don't vote", "we will not vote", "strategic vote", "overthrow", "remove from power",
        "defeat", "hold accountable", "double down"
    ]

    @classmethod
    def decompose_discourse(cls, text: str) -> DiscourseVectorDecomposition:
        if not text:
            return DiscourseVectorDecomposition(
                factuality_ratio=0.10,
                ideology_intensity=0.10,
                agenda_potency=0.0,
                omission_penalty=0.0,
                dominant_ideology="NEUTRAL",
                primary_agenda_type="INFORMATIONAL",
                discourse_classification="NEUTRAL_OR_EMPTY"
            )
        text_lower = text.lower()

        found_facts = [kw for kw in cls.FACTUAL_KEYWORDS if kw in text_lower]
        found_ideology = [kw for kw in cls.IDEOLOGICAL_KEYWORDS if kw in text_lower]
        found_agenda = [kw for kw in cls.AGENDA_KEYWORDS if kw in text_lower]

        fact_ratio = round(min(1.0, max(0.10, len(found_facts) * 0.14)), 2)
        ideology_int = round(min(1.0, max(0.10, len(found_ideology) * 0.16)), 2)
        agenda_pot = round(min(1.0, max(0.0, len(found_agenda) * 0.18)), 2)


        # Check negative space omissions
        omitted = []
        if ("jizya" in text_lower or "subsidy" in text_lower or "80 crore" in text_lower or "free" in text_lower) and not any(w in text_lower for w in ["food security", "famine", "inflation floor", "starvation", "covid relief", "stability floor"]):
            omitted.append("MACROECONOMIC_FOOD_SECURITY_STABILITY_FLOOR")
        if ("rollback" in text_lower or "coward" in text_lower or "retracted" in text_lower) and not any(w in text_lower for w in ["two front", "china", "galwan", "foreign ngo", "color revolution"]):
            omitted.append("EXTERNAL_TWO_FRONT_AND_HYBRID_WARFARE_REALPOLITIK")
        if ("caste" in text_lower or "sc st" in text_lower or "reservation" in text_lower) and not any(w in text_lower for w in ["historical discrimination", "untouchability", "social integration", "dignity"]):
            omitted.append("SUBALTERN_HISTORICAL_EXCLUSION_AND_INTEGRATION")
        if ("infrastructure" in text_lower or "broken" in text_lower) and not any(w in text_lower for w in ["highways", "freight corridor", "nhai", "electrification", "dpi", "capex"]):
            omitted.append("SYSTEMIC_SUPPLY_SIDE_CAPEX_EXPANSION")

        omission_pen = round(min(1.0, len(omitted) * 0.25), 2)

        # Dominant ideology
        if any(w in text_lower for w in ["merit", "taxpayer", "savarna", "blunder"]):
            dom_ideol = "TRADITIONALIST_MERITOCRACY"
        elif any(w in text_lower for w in ["decolonial", "temple", "places of worship"]):
            dom_ideol = "INDIC_DECOLONIAL_JURISPRUDENCE"
        elif any(w in text_lower for w in ["stem", "semi-conductor", "avionics"]):
            dom_ideol = "DEEP_TECH_NATIONALISM"
        elif any(w in text_lower for w in ["ambedkar", "annihilation of caste"]):
            dom_ideol = "SUBALTERN_CONSTITUTIONALISM"
        else:
            dom_ideol = "GENERAL_POLITICAL_POLEMIC"

        # Primary agenda type
        if any(w in text_lower for w in ["boycott", "not vote", "we will not vote"]):
            agenda_type = "ELECTORAL_BOYCOTT_AND_DISCIPLINARY_PRESSURE"
        elif any(w in text_lower for w in ["protest", "mobilize", "strike"]):
            agenda_type = "STREET_MOBILIZATION"
        elif any(w in text_lower for w in ["statute", "amendment", "bail"]):
            agenda_type = "STATUTORY_DUE_PROCESS_REFORM"
        else:
            agenda_type = "AWARENESS_AND_DISCOURSE_SHIFT"

        # Classification
        if fact_ratio >= 0.55 and ideology_int >= 0.45:
            classification = "EVIDENTIARY_POLEMIC"
        elif fact_ratio >= 0.65 and ideology_int < 0.40:
            classification = "FORENSIC_OBJECTIVE_AUDIT"
        elif fact_ratio < 0.35 and agenda_pot >= 0.50:
            classification = "TACTICAL_POLITICAL_MOBILIZATION"
        else:
            classification = "MIXED_CRITICAL_DISCOURSE"

        return DiscourseVectorDecomposition(
            factuality_ratio=fact_ratio,
            ideology_intensity=ideology_int,
            agenda_potency=agenda_pot,
            omission_penalty=omission_pen,
            dominant_ideology=dom_ideol,
            primary_agenda_type=agenda_type,
            identified_factual_anchors=found_facts,
            identified_ideological_tokens=found_ideology,
            identified_actionable_demands=found_agenda,
            critical_omitted_counterweights=omitted,
            discourse_classification=classification
        )


class AudioStreamConnector:

    """
    Connects to external media URLs, bypassing dynamic client-side JavaScript lockouts
    by extracting caption tracks, headless metadata, or streaming transcript segments,
    and transforming them into verified ClaimItem records for the multi-lens engine.
    """

    @classmethod
    def extract_acoustic_telemetry(
        cls,
        data_or_path: Union[bytes, str],
        sample_rate: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Processes raw audio buffer or WAV file path through native AcousticDSPWorker,
        extracting fundamental frequency, jitter, and pause latency features.
        """
        from .acoustic_dsp import AcousticDSPWorker
        return AcousticDSPWorker.analyze_audio(data_or_path, sample_rate=sample_rate)

    @classmethod
    def extract_media_id(cls, url_or_id: str) -> str:
        """
        Extracts a clean 11-character YouTube video ID or generates a deterministic
        media ID hash for arbitrary media/audio URLs.
        """
        raw = str(url_or_id).strip()
        # Direct 11-char YouTube ID match
        if re.match(r"^[a-zA-Z0-9_-]{11}$", raw):
            return raw

        try:
            parsed = YouTubeURLParser.parse(raw)
            return parsed["video_id"]
        except Exception:
            # Fallback for podcast, audio stream, or non-standard media URLs
            media_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:11]
            return f"MED-{media_hash}"

    @classmethod
    def fetch_stream_transcript(
        cls,
        url_or_id: str,
        preferred_languages: Optional[List[str]] = None,
        metadata_fallback: Optional[Dict[str, Any]] = None
    ) -> AudioTranscript:
        """
        Headless extraction of timestamped transcript from video/audio stream URL.
        Bypasses client-side minified JS lockouts using YouTube caption tracks and fallback heuristics.
        """
        media_id = cls.extract_media_id(url_or_id)
        langs = preferred_languages or ["en", "hi"]

        result: TranscriptResult = VideoTranscriptEngine.fetch_transcript(
            video_id=media_id,
            preferred_languages=langs,
            metadata_fallback=metadata_fallback
        )

        return AudioTranscript(
            media_id=media_id,
            source_url=url_or_id if url_or_id.startswith("http") else None,
            language=result.language,
            full_text=result.full_text,
            segments=result.segments,
            is_degraded=result.is_degraded,
            is_simulated=result.is_simulated,
            extraction_method=result.fallback_mode or "caption_stream"
        )

    @classmethod
    def transcript_to_claims(
        cls,
        transcript: AudioTranscript,
        target_lenses: Optional[List[str]] = None,
        default_reliability: float = 0.85
    ) -> List[ClaimItem]:
        """
        Transforms transcript segments into epistemically tiered ClaimItem records
        suitable for ingestion into the SQLite EventStore and multi-lens evaluators.

        If target_lenses is not specified, dynamically detects relevant lenses for each
        chunk using QueryParser.LENS_KEYWORDS, routing claims across all 20 analytical
        optics based on the actual transcript content.
        """
        raw_records = []
        # Group transcript segments into ~30-60 second chunks for coherent claim representation
        chunk_text = []
        chunk_start = 0.0
        chunk_idx = 0

        def _detect_lenses_from_text(text: str) -> List[str]:
            """Scans chunk text against QueryParser.LENS_KEYWORDS to detect relevant lenses."""
            text_lower = text.lower()
            detected = []
            for lens_name, keywords in QueryParser.LENS_KEYWORDS.items():
                if any(kw in text_lower for kw in keywords):
                    detected.append(lens_name)
            # Always include at minimum the two baseline lenses for political/economic video content
            if "institutional_lawfare" not in detected:
                detected.append("institutional_lawfare")
            if "geopolitical" not in detected:
                detected.append("geopolitical")
            return detected

        for seg in transcript.segments:
            chunk_text.append(seg.text)
            if (seg.start - chunk_start) >= 45.0 or seg == transcript.segments[-1]:
                combined = " ".join(chunk_text).strip()
                if combined:
                    # Use caller-provided lenses if given; otherwise detect dynamically
                    chunk_lenses = target_lenses if target_lenses else _detect_lenses_from_text(combined)
                    raw_records.append({
                        "id": f"AUD-{transcript.media_id}-{chunk_idx:02d}",
                        "text": combined,
                        "source_id": f"SRC-AUDIO-{transcript.media_id}",
                        "target_lenses": chunk_lenses,
                        "reliability_weight": default_reliability
                    })
                    chunk_idx += 1
                chunk_text = []
                chunk_start = seg.end

        if not raw_records and transcript.full_text:
            fallback_lenses = target_lenses if target_lenses else _detect_lenses_from_text(transcript.full_text[:500])
            raw_records.append({
                "id": f"AUD-{transcript.media_id}-00",
                "text": transcript.full_text[:500],
                "source_id": f"SRC-AUDIO-{transcript.media_id}",
                "target_lenses": fallback_lenses,
                "reliability_weight": default_reliability
            })

        return MacroTelemetryAdapter.normalize_telemetry(raw_records)


    @classmethod
    def ingest_media_url(
        cls,
        url_or_id: str,
        store: Optional[EventStore] = None,
        metadata_fallback: Optional[Dict[str, Any]] = None,
        target_lenses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        High-level pipeline: fetches transcript for media URL, normalizes into ClaimItems,
        and persists into the EventStore. Returns summary ingestion statistics.
        """
        target_store = store or EventStore()
        transcript = cls.fetch_stream_transcript(url_or_id, metadata_fallback=metadata_fallback)
        claims = cls.transcript_to_claims(transcript, target_lenses=target_lenses)

        ingested_count = MacroTelemetryAdapter.ingest_to_event_store(claims, store=target_store)

        return {
            "media_id": transcript.media_id,
            "language": transcript.language,
            "extraction_method": transcript.extraction_method,
            "is_degraded": transcript.is_degraded,
            "total_segments": len(transcript.segments),
            "claims_generated": len(claims),
            "claims_ingested": ingested_count
        }

    @classmethod
    def audit_media_claims(
        cls,
        url_or_id: Union[str, AudioTranscript],
        store: Optional[EventStore] = None,
        metadata_fallback: Optional[Dict[str, Any]] = None,
        preferred_languages: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Forensic Epistemic Audit Pipeline for audio/video media.
        Extracts transcript, maps claims against canonical cosmic anchors and hoax registries,
        computes the Evidence-Distortion Tensor (ALEDT), and synthesizes a 6-perspective
        Civilizational Council evaluation.
        """
        from ..lenses.propaganda import PropagandaLens
        from ..arbitration.persona_narrator import CivilizationalCouncil

        target_store = store or EventStore()
        if isinstance(url_or_id, AudioTranscript):
            transcript = url_or_id
        else:
            transcript = cls.fetch_stream_transcript(
                url_or_id,
                preferred_languages=preferred_languages,
                metadata_fallback=metadata_fallback
            )
        claims = cls.transcript_to_claims(transcript)

        full_text = (transcript.full_text or "").lower()
        if metadata_fallback:
            fb_title = metadata_fallback.get("title", "")
            fb_desc = metadata_fallback.get("description", "")
            full_text = f"{full_text} {fb_title} {fb_desc}".lower()

        # 1. Match against known hoax & debunk registries
        debunks = target_store.get_debunk_registry()
        detected_hoaxes = []
        for d in debunks:
            b_id = d.get("benchmark_id", "")
            notes = d.get("debunk_notes", "")
            if "nostradamus" in b_id.lower() or "nostradamus" in notes.lower():
                if any(w in full_text for w in ["nostradamus", "twin tower", "hister", "two brother", "iron bird"]):
                    detected_hoaxes.append({
                        "id": b_id,
                        "canonical_source": d.get("canonical_source"),
                        "debunk_notes": notes
                    })
            if "kashinath" in b_id.lower() or "malika" in notes.lower():
                if any(w in full_text for w in ["malika", "kashinath", "achyutananda", "panchasakha", "2032"]):
                    detected_hoaxes.append({
                        "id": b_id,
                        "canonical_source": d.get("canonical_source"),
                        "debunk_notes": notes
                    })

        # 2. Check for physical anchors mentioned
        physical_keywords = ["cyclone", "fani", "covid", "locust", "tree", "flag", "temple", "rock", "stone", "wheel", "storm"]
        matched_physical = [kw for kw in physical_keywords if kw in full_text]

        # 3. Detect Millenarian / Apocalyptic Distortion Vectors & Electoral Fraud Claims
        apocalyptic_terms = ["2032", "kali yuga", "apocalypse", "doomsday", "kalki", "ww3", "pralaya", "end of world"]
        has_apocalyptic = any(term in full_text for term in apocalyptic_terms)

        electoral_terms = [
            "vote chori", "vote theft", "electoral roll", "special intensive revision", "sir",
            "turn approver", "approver", "gyanesh kumar", "voter deletion", "election commission",
            "rigged", "stolen election"
        ]
        has_electoral_claim = any(term in full_text for term in electoral_terms)

        # Check for Archaeological / Ancient Chronology Claims
        from ..arbitration.historical_arbiter import MultiPillarChronologyArbiter
        chronological_terms = [
            "sinauli", "sanauli", "rakhigarhi", "harappan", "vedic age", "chariot",
            "copper hoard", "pgw", "ocp", "aryabhata", "aihole", "dating", "5561", "3067",
            "1000 bce", "bronze age", "antennae sword", "paleogenomics", "adna"
        ]
        has_chronological_claim = any(term in full_text for term in chronological_terms)
        chronology_audit = None
        if has_chronological_claim:
            event_title = f"Media Stream Chronology Audit ({transcript.media_id})"
            chronology_report = MultiPillarChronologyArbiter.arbitrate(event_name=event_title)
            chronology_audit = chronology_report.to_dict()

        # Check for Defense Avionics & 5th-Gen Procurement Claims
        from ..lenses.military_readiness import AvionicsSovereigntySieve
        defense_avionics_terms = [
            "f-35", "f35", "su-57", "su57", "mrfa", "stealth fighter",
            "digital leash", "kill switch", "kill-switch", "luneburg", "jodhpur",
            "tarang shakti", "lockheed", "avionics"
        ]
        has_defense_claim = any(term in full_text for term in defense_avionics_terms)
        avionics_audit = None
        if has_defense_claim:
            is_f35 = ("f-35" in full_text or "f35" in full_text or "lockheed" in full_text or "alis" in full_text or "odin" in full_text)
            source_transfer = False if is_f35 else ("su-57" in full_text or "mrfa" in full_text)
            on_prem = False if is_f35 else True
            cloud_tether = True if is_f35 else False
            kill_switch = 0.85 if is_f35 else 0.45
            avionics_audit = AvionicsSovereigntySieve.calculate_operational_autonomy(
                source_code_transfer=source_transfer,
                on_prem_mission_data=on_prem,
                foreign_cloud_tether=cloud_tether,
                proprietary_kill_switch_risk=kill_switch
            )

        # Check for Sub-National Chokepoint & Pincer Claims
        from ..lenses.geopolitical import ChokepointKineticSieve
        chokepoint_terms = [
            "siliguri", "chicken's neck", "chickens neck", "doklam", "chumbi",
            "suwalki", "wakhan", "teesta", "rangpur", "pincer"
        ]
        has_chokepoint_claim = any(term in full_text for term in chokepoint_terms)
        chokepoint_audit = None
        if has_chokepoint_claim:
            width = 22.0 if ("siliguri" in full_text or "chicken" in full_text) else 40.0
            prox = 30.0 if "chumbi" in full_text or "doklam" in full_text else 45.0
            flank = 0.85 if "bangladesh" in full_text or "rangpur" in full_text else 0.60
            hydro = 0.75 if "teesta" in full_text else 0.40
            chokepoint_audit = ChokepointKineticSieve.calculate_chokepoint_vulnerability(
                corridor_width_km=width,
                adversary_proximity_km=prox,
                hostile_flank_index=flank,
                upstream_hydro_leverage=hydro,
                logistics_redundancy_count=1
            )

        # Phase 88: Sub-National Sacred Geography & Religious Endowment Sieve
        from ..lenses.institutional_lawfare import SubNationalEndowmentSieve
        endowment_terms = ["sattra", "satras", "batadrava", "gorukhuti", "dhalpur", "char land", "waqf", "section 40", "hrce"]
        has_endowment_claim = any(term in full_text for term in endowment_terms)
        endowment_audit = None
        if has_endowment_claim:
            encroach = 0.85 if ("gorukhuti" in full_text or "char" in full_text or "batadrava" in full_text) else 0.60
            asym = 0.90 if ("waqf" in full_text or "section 40" in full_text or "sattra" in full_text or "batadrava" in full_text) else 0.50
            cadastre = 0.20 if ("char" in full_text or "batadrava" in full_text) else 0.50
            endowment_audit = SubNationalEndowmentSieve.calculate_endowment_vulnerability(
                encroachment_intensity=encroach,
                waqf_statutory_asymmetry=asym,
                cadastral_survey_clarity=cadastre
            )

        # Phase 89: Executive Policy Rollback Elasticity Model
        from ..lenses.bureaucratic_inertia import BureaucraticRollbackModel
        rollback_terms = ["rollback", "de-reservation", "draft guidelines", "ugc", "policy rollback", "executive retreat"]
        has_rollback_claim = any(term in full_text for term in rollback_terms)
        rollback_audit = None
        if has_rollback_claim:
            has_ugc = "ugc" in full_text or "de-reservation" in full_text
            electoral_sens = 0.90 if has_ugc else 0.70
            mob_vel = 0.85 if has_ugc else 0.65
            exec_comm = 0.25 if has_ugc else 0.50
            deficit = 0.80 if has_ugc else 0.40
            rollback_audit = BureaucraticRollbackModel.calculate_rollback_elasticity(
                electoral_sensitivity=electoral_sens,
                mobilization_velocity=mob_vel,
                executive_commitment=exec_comm,
                consultation_deficit=deficit
            )

        # Phase 90: Sartorial & Semiotic Micro-Signal Forensics
        from ..lenses.kinesics import SartorialSemioticSieve
        sartorial_terms = ["gamusa", "saffron", "corporate attire", "sartorial", "semiotic"]
        has_sartorial_claim = any(term in full_text for term in sartorial_terms)
        sartorial_audit = None
        if has_sartorial_claim:
            attire = "gamusa_indigenous" if "gamusa" in full_text else ("saffron_civilizational" if "saffron" in full_text else "corporate_western")
            dissonance = 0.55 if ("war" in full_text or "conflict" in full_text) else 0.20
            masking = 0.50 if ("peace" in full_text or "protocol" in full_text) else 0.20
            sartorial_audit = SartorialSemioticSieve.calculate_sartorial_congruence(
                attire_type=attire,
                diplomatic_posture_dissonance=dissonance,
                semiotic_masking_score=masking,
                prosodic_jitter=0.06
            )

        # Phase 93: Intra-Civilizational Faultline & Statutory Asymmetry Forensics
        from ..lenses.institutional_lawfare import IntraCivilizationalFaultlineSieve
        faultline_terms = ["sc st act", "section 18a", "kashinath mahajan", "anticipatory bail", "caste faultline", "general category", "ancestral sin"]
        has_faultline_claim = any(term in full_text for term in faultline_terms)
        faultline_audit = None
        if has_faultline_claim:
            has_18a = "section 18a" in full_text or "kashinath" in full_text or "anticipatory bail" in full_text
            has_sin = "ancestral sin" in full_text or "hisab chukta" in full_text
            faultline_audit = IntraCivilizationalFaultlineSieve.calculate_faultline_vulnerability(
                statutory_due_process_asymmetry=0.90 if has_18a else 0.60,
                historical_guilt_narrative_intensity=0.85 if has_sin else 0.40,
                meritocratic_preservation_index=0.35 if has_18a else 0.65
            )

        # Phase 94: Extraterritorial Sovereign Asymmetry Forensics
        from ..lenses.hybrid_covert import ExtraterritorialSovereignAsymmetrySieve
        sovereign_asym_terms = ["vandyke", "van dyke", "quattrocchi", "warren anderson", "enrica lexie", "italian marines", "mercenary trainer", "sons of liberty"]
        has_sovereign_asym_claim = any(term in full_text for term in sovereign_asym_terms)
        sovereign_asym_audit = None
        if has_sovereign_asym_claim:
            has_vd = "vandyke" in full_text or "van dyke" in full_text
            sovereign_asym_audit = ExtraterritorialSovereignAsymmetrySieve.calculate_sovereign_asymmetry(
                foreign_privilege_intensity=0.90 if has_vd else 0.70,
                bilateral_coercion_pressure=0.85,
                domestic_parity_enforcement=0.30
            )

        # Phase 95: Antithetical Rhetoric & Oratorical Priming Forensics
        from ..lenses.propaganda import AntitheticalRhetoricSieve
        antithetical_terms = ["hisab chukta", "hisaab chukta", "hisab karega", "settle scores", "karega ki nahi", "antithetical priming"]
        has_antithetical_claim = any(term in full_text for term in antithetical_terms)
        antithetical_audit = None
        if has_antithetical_claim:
            antithetical_audit = AntitheticalRhetoricSieve.calculate_antithetical_priming(
                premise_activation_intensity=0.85,
                crowd_validation_factor=0.90,
                restraint_claim_credibility=0.40
            )

        # Phase 98: Asymmetric Interceptor Cost-Exchange Forensics
        from ..lenses.military_readiness import AsymmetricInterceptionSieve
        burnout_terms = ["drone burnout", "cost-exchange", "interceptor exhaustion", "sm-2", "sm-6", "shahed", "houthi drone", "red sea", "drone swarm"]
        has_burnout_claim = any(term in full_text for term in burnout_terms)
        burnout_audit = None
        if has_burnout_claim:
            burnout_audit = AsymmetricInterceptionSieve.calculate_cost_exchange_ratio(
                interceptor_count=2,
                cost_per_interceptor_usd=2_500_000.0 if ("sm-2" in full_text or "sm-6" in full_text or "red sea" in full_text) else 1_200_000.0,
                threat_count=1,
                cost_per_threat_usd=20_000.0 if ("shahed" in full_text or "houthi" in full_text) else 35_000.0,
                magazine_depth_remaining_ratio=0.35 if ("exhaust" in full_text or "burnout" in full_text) else 0.55
            )

        # Phase 99: Diaspora Host-Nation Backlash Forensics
        from ..lenses.demographic_infiltration import DiasporaBacklashSieve
        diaspora_terms = ["diaspora under siege", "sb 403", "caste lawfare", "texas hanuman", "statue of union", "nativist backlash", "h-1b ban", "diaspora fragility"]
        has_diaspora_claim = any(term in full_text for term in diaspora_terms)
        diaspora_audit = None
        if has_diaspora_claim:
            diaspora_audit = DiasporaBacklashSieve.calculate_diaspora_vulnerability(
                nativist_hate_incidents=0.80 if ("temple" in full_text or "hanuman" in full_text) else 0.55,
                caste_lawfare_activity=0.85 if ("sb 403" in full_text or "caste" in full_text) else 0.45,
                grassroots_advocacy_strength=0.25,
                host_country_polarization=0.85
            )

        # Phase 100: Diplomatic Counter-Intelligence Forensics
        from ..lenses.hybrid_covert import DiplomaticCounterIntelSieve
        diplomatic_terms = ["hamid ansari", "ansari", "tehran raw", "nusrat mirza", "counter-intel vetting", "diplomatic compromise"]
        has_diplomatic_claim = any(term in full_text for term in diplomatic_terms)
        diplomatic_audit = None
        if has_diplomatic_claim:
            diplomatic_audit = DiplomaticCounterIntelSieve.calculate_counter_intel_vulnerability(
                single_region_tenure_ratio=0.90 if ("tehran" in full_text or "ansari" in full_text) else 0.70,
                transnational_hostile_associations=0.85 if ("nusrat" in full_text or "iamc" in full_text or "pfi" in full_text) else 0.60,
                counter_intel_vetting_depth=0.25,
                ideological_factional_alignment=0.80
            )

        # Phase 100: STEM Capital Dilution Forensics
        from ..lenses.deep_tech import STEMCapitalDilutionSieve
        stem_terms = ["stem dilution", "grievance curricula", "engineering capex", "technological dividend", "demographic dividend liability"]
        has_stem_claim = any(term in full_text for term in stem_terms)
        stem_audit = None
        if has_stem_claim:
            stem_audit = STEMCapitalDilutionSieve.calculate_stem_dilution(
                grievance_curricula_budget_share=0.55 if "grievance" in full_text else 0.35,
                physical_lab_capex_share=0.25 if "dilution" in full_text else 0.40,
                ideological_administrative_overhead=0.40,
                meritocratic_faculty_retention=0.55
            )

        # Level-0 Atomic Temporal Guardrail Check on Incumbency/Tenure
        from ..core.temporal_guardrail import TemporalGuardrail
        tenure_audit = None
        if "gyanesh kumar" in full_text or "gyanesh" in full_text:
            for yr in ["2021", "2022", "2023"]:
                if yr in full_text:
                    tenure_audit = TemporalGuardrail.verify_chronological_feasibility(
                        person_key="gyanesh_kumar",
                        office_keyword="Chief Election Commissioner",
                        event_date_str=f"{yr}-06-15"
                    )
                    break
            if not tenure_audit:
                tenure_audit = TemporalGuardrail.verify_chronological_feasibility(
                    person_key="gyanesh_kumar",
                    office_keyword="Chief Election Commissioner",
                    event_date_str="2026-09-24"
                )

        # Atomic Claim Decomposition & Poisoned Tail Detection
        from ..arbitration.competing_hypotheses import ClaimDecomposer
        decomposed_claim = ClaimDecomposer.decompose(transcript.full_text[:500] if transcript.full_text else "")

        # Forensic Courtroom Cross-Examination Archetype Takeaway
        from ..arbitration.persona_narrator import PersonaNarrator
        from ..core.models import SummitEvent, SummitAnalysisReport
        dummy_event = SummitEvent(summit_name=f"Media Stream Audit ({transcript.media_id})", year=2026)
        dummy_report = SummitAnalysisReport(event=dummy_event)
        rizwan_cross_exam = PersonaNarrator.apply_persona(dummy_report, "rizwan_ahmed")

        if has_apocalyptic:
            empirical_support = 0.20 if matched_physical else 0.10
            phi_theological = 0.65
            phi_pseudoscience = 0.85 if detected_hoaxes else 0.70
            phi_ideological = 0.15
        elif has_electoral_claim:
            empirical_support = 0.25 if not (tenure_audit and not tenure_audit.get("is_chronologically_feasible")) else 0.10
            phi_theological = 0.05
            phi_ideological = 0.85 if decomposed_claim.is_poisoned_tail_detected else 0.65
            phi_pseudoscience = 0.75 if any(t in full_text for t in ["turn approver", "deshdrohi", "vote chori"]) else 0.40
        elif has_chronological_claim:
            has_archaeological_material = any(w in full_text for w in ["c14", "radiocarbon", "coffin", "sword", "shield", "copper", "cart", "burial", "bsip", "excavation", "asi"])
            empirical_support = 0.75 if has_archaeological_material else 0.45
            phi_colonial = 0.25 if any(w in full_text for w in ["aryan invasion", "ait", "colonial", "max muller"]) else 0.10
            phi_theological = 0.15
            phi_ideological = 0.35 if any(w in full_text for w in ["conspiracy", "hidden", "stopped excavation", "secret"]) else 0.20
            phi_pseudoscience = 0.30 if any(w in full_text for w in ["alien", "vimana", "nuclear war"]) else 0.10
        elif has_defense_claim:
            empirical_support = 0.70
            phi_theological = 0.05
            phi_colonial = 0.20 if ("usaf" in full_text or "lockheed" in full_text or "america" in full_text) else 0.10
            phi_ideological = 0.45 if ("f-35" in full_text or "f35" in full_text) else 0.25
            phi_pseudoscience = 0.10
        elif has_chokepoint_claim:
            empirical_support = 0.80
            phi_theological = 0.05
            phi_colonial = 0.15
            phi_ideological = 0.35 if ("bangladesh" in full_text or "regime" in full_text) else 0.20
            phi_pseudoscience = 0.05
        elif has_endowment_claim or has_rollback_claim:
            empirical_support = 0.78 if (endowment_audit or rollback_audit) else 0.50
            phi_theological = 0.30 if has_endowment_claim else 0.05
            phi_colonial = 0.12
            phi_ideological = 0.35 if has_rollback_claim else 0.25
            phi_pseudoscience = 0.05
        elif has_faultline_claim or has_antithetical_claim or has_sovereign_asym_claim:
            empirical_support = 0.82 if (faultline_audit or antithetical_audit or sovereign_asym_audit) else 0.55
            phi_theological = 0.25 if has_faultline_claim else 0.10
            phi_colonial = 0.35 if (has_sovereign_asym_claim or "ancestral sin" in full_text) else 0.15
            phi_ideological = 0.40 if has_antithetical_claim else 0.25
            phi_pseudoscience = 0.05
        else:
            empirical_support = 0.60 if matched_physical else 0.40
            phi_theological = 0.20
            phi_pseudoscience = 0.30 if detected_hoaxes else 0.15
            phi_ideological = 0.15

        # 4. Compute closed-form Evidence-Distortion Tensor
        tensor = PropagandaLens.calculate_evidence_distortion_tensor(
            empirical_support=empirical_support,
            phi_colonial=0.10,
            phi_ideological=phi_ideological,
            phi_theological=phi_theological,
            phi_pseudoscience=phi_pseudoscience
        )

        # 5. Synthesize Civilizational Council Perspectives
        council_data = CivilizationalCouncil.evaluate(
            topic_or_claim=f"Media Stream Audit ({transcript.media_id})",
            tensor_data=tensor,
            context_notes=f"Extraction: {transcript.extraction_method}, Language: {transcript.language}, Segments: {len(transcript.segments)}"
        )

        formatted_report = CivilizationalCouncil.format_council_report(council_data)

        # Build visual score bar (40 blocks)
        r_blocks = int(round((tensor["reality_percentage"] / 100.0) * 40))
        p_blocks = 40 - r_blocks
        bar = "█" * r_blocks + "░" * p_blocks

        # 6. Deconstruct Discourse Vectors (Fact vs Ideology vs Agenda vs Omission)
        discourse_audit = DiscourseDecompositionEngine.decompose_discourse(full_text)

        return {
            "media_id": transcript.media_id,
            "language": transcript.language,
            "extraction_method": transcript.extraction_method,
            "is_degraded": transcript.is_degraded,
            "total_segments": len(transcript.segments),
            "claims_generated": len(claims),
            "detected_hoaxes": detected_hoaxes,
            "matched_physical_keywords": matched_physical,
            "has_electoral_claim": has_electoral_claim,
            "has_chronological_claim": has_chronological_claim,
            "has_defense_claim": has_defense_claim,
            "has_chokepoint_claim": has_chokepoint_claim,
            "has_endowment_claim": has_endowment_claim,
            "has_rollback_claim": has_rollback_claim,
            "has_sartorial_claim": has_sartorial_claim,
            "has_faultline_claim": has_faultline_claim,
            "has_sovereign_asymmetry_claim": has_sovereign_asym_claim,
            "has_antithetical_claim": has_antithetical_claim,
            "has_burnout_claim": has_burnout_claim,
            "has_diaspora_claim": has_diaspora_claim,
            "has_diplomatic_claim": has_diplomatic_claim,
            "has_stem_claim": has_stem_claim,
            "interceptor_burnout_audit": burnout_audit,
            "diaspora_backlash_audit": diaspora_audit,
            "diplomatic_counter_intel_audit": diplomatic_audit,
            "stem_dilution_audit": stem_audit,
            "avionics_sovereignty_audit": avionics_audit,
            "chokepoint_audit": chokepoint_audit,
            "endowment_audit": endowment_audit,
            "rollback_audit": rollback_audit,
            "sartorial_audit": sartorial_audit,
            "faultline_audit": faultline_audit,
            "sovereign_asymmetry_audit": sovereign_asym_audit,
            "antithetical_audit": antithetical_audit,
            "chronology_audit": chronology_audit,
            "tenure_audit": tenure_audit,
            "decomposed_claim": decomposed_claim.model_dump() if decomposed_claim else None,
            "discourse_decomposition": discourse_audit.model_dump(),
            "courtroom_cross_examination": rizwan_cross_exam,
            "tensor": tensor,
            "reality_percentage": tensor["reality_percentage"],
            "propaganda_percentage": tensor["propaganda_percentage"],
            "epistemic_classification": tensor["epistemic_classification"],
            "epistemic_classification_ascii": tensor["epistemic_classification_ascii"],
            "visual_gauge": bar,
            "council_evaluation": council_data,
            "formatted_report": formatted_report
        }



class MediaAuditWorkerQueue:
    """
    Asynchronous Worker Queue for Media Extraction and Claim Auditing.
    Decouples heavy multi-hour video/audio ingestion from the synchronous request thread,
    recording job execution states and progress inside SQLite events.db.
    """
    import concurrent.futures
    _executor: Optional[concurrent.futures.ThreadPoolExecutor] = None

    @classmethod
    def _get_executor(cls):
        import concurrent.futures
        if cls._executor is None:
            cls._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="MediaAuditWorker")
        return cls._executor

    @classmethod
    def submit_audit_job(
        cls,
        url_or_id: str,
        preferred_languages: Optional[List[str]] = None,
        metadata_fallback: Optional[Dict[str, Any]] = None,
        db_path: Optional[str] = None
    ) -> str:
        """
        Dispatches an asynchronous media audit task to the worker pool.
        Returns unique job_id immediately without blocking the caller.
        """
        import uuid
        job_id = f"JOB-{uuid.uuid4().hex[:12].upper()}"
        store = EventStore(db_path=db_path)
        store.create_media_job(job_id=job_id, source_url=str(url_or_id))

        executor = cls._get_executor()
        executor.submit(
            cls._execute_worker_task,
            job_id,
            url_or_id,
            preferred_languages,
            metadata_fallback,
            db_path
        )
        return job_id

    @classmethod
    def _execute_worker_task(
        cls,
        job_id: str,
        url_or_id: str,
        preferred_languages: Optional[List[str]],
        metadata_fallback: Optional[Dict[str, Any]],
        db_path: Optional[str]
    ) -> None:
        """Background thread worker execution body."""
        import json
        store = EventStore(db_path=db_path)
        try:
            store.update_media_job(job_id, status="PROCESSING", progress_pct=15.0)

            # Step 1: Run complete media audit
            audit_result = AudioStreamConnector.audit_media_claims(
                url_or_id=url_or_id,
                store=store,
                metadata_fallback=metadata_fallback,
                preferred_languages=preferred_languages
            )
            store.update_media_job(job_id, status="PROCESSING", progress_pct=85.0)

            # Step 2: Serialize result and mark COMPLETED
            result_str = json.dumps(audit_result, default=str)
            store.update_media_job(
                job_id,
                status="COMPLETED",
                progress_pct=100.0,
                result_json=result_str
            )
        except Exception as exc:
            store.update_media_job(
                job_id,
                status="FAILED",
                progress_pct=100.0,
                error_message=str(exc)
            )

    @classmethod
    def get_job_status(cls, job_id: str, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Queries the current status and results of a media audit background job."""
        import json
        store = EventStore(db_path=db_path)
        job = store.get_media_job(job_id)
        if not job:
            return None
        if job.get("result_json"):
            try:
                job["result"] = json.loads(job["result_json"])
            except Exception:
                job["result"] = None
        return job

    @classmethod
    def wait_for_job(
        cls,
        job_id: str,
        timeout_seconds: float = 30.0,
        poll_interval: float = 0.1,
        db_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Synchronously polls for background job completion up to timeout_seconds."""
        import time
        start_t = time.time()
        while time.time() - start_t < timeout_seconds:
            status = cls.get_job_status(job_id, db_path=db_path)
            if status and status.get("status") in ("COMPLETED", "FAILED"):
                return status
            time.sleep(poll_interval)
        return {
            "job_id": job_id,
            "status": "TIMEOUT",
            "error_message": f"Job {job_id} exceeded wait timeout of {timeout_seconds}s"
        }


class StreamingAudioChunk(BaseModel):
    """A real-time timestamped chunk of speech or transcript text."""
    chunk_id: str
    timestamp_start_s: float
    timestamp_end_s: float
    raw_text: str
    speaker_tag: Optional[str] = None
    signal_quality: float = 1.0


class StreamingDiscourseAlert(BaseModel):
    """Real-time forensic anomaly or threshold alert."""
    alert_id: str
    timestamp_s: float
    alert_type: str  # 'RAPID_AGENDA_ESCALATION', 'HIGH_OMISSION_PENALTY', 'GRAYZONE_FRACTURE_TRIGGER'
    severity: float  # 0.0 to 1.0
    trigger_statement: str
    recommended_countermeasure: str


class ChunkAuditTelemetry(BaseModel):
    """Telemetry produced per streaming chunk evaluation."""
    chunk_id: str
    timestamp_s: float
    window_factuality: float
    window_ideology: float
    window_agenda: float
    window_omission: float
    dominant_ideology: str
    active_alerts: List[StreamingDiscourseAlert] = Field(default_factory=list)
    distilled_claims_count: int = 0


class StreamingChunkAuditor:
    """
    Stateful rolling auditor for real-time live broadcast streams,
    podcasts, and conference audio feeds.
    """

    def __init__(self, window_size: int = 5, alert_threshold: float = 0.65):
        self.window_size = window_size
        self.alert_threshold = alert_threshold
        self.history: List[StreamingAudioChunk] = []
        self.alerts: List[StreamingDiscourseAlert] = []
        self._processed_chunks_count: int = 0

    def process_chunk(
        self,
        chunk: StreamingAudioChunk,
        store: Optional[EventStore] = None
    ) -> ChunkAuditTelemetry:
        """Processes an incoming real-time audio chunk and evaluates rolling discourse metrics."""
        self.history.append(chunk)
        self._processed_chunks_count += 1

        # Keep sliding window
        active_window = self.history[-self.window_size:]
        window_text = " ".join(c.raw_text for c in active_window)

        # Run rolling discourse decomposition
        decomp = DiscourseDecompositionEngine.decompose_discourse(window_text)

        new_alerts: List[StreamingDiscourseAlert] = []

        # 1. Rapid Agenda Escalation: High agenda, low factuality
        if decomp.agenda_potency >= self.alert_threshold and decomp.factuality_ratio <= 0.35:
            alert = StreamingDiscourseAlert(
                alert_id=f"ALT-AGENDA-{hashlib.sha256(chunk.raw_text.encode('utf-8')).hexdigest()[:8].upper()}",
                timestamp_s=chunk.timestamp_end_s,
                alert_type="RAPID_AGENDA_ESCALATION",
                severity=decomp.agenda_potency,
                trigger_statement=chunk.raw_text[:120],
                recommended_countermeasure="Enforce Tier 5 Communique PR haircut and request verifiable statutory or fiscal corroboration."
            )
            new_alerts.append(alert)
            self.alerts.append(alert)

        # 2. High Negative-Space Omission Penalty
        if decomp.omission_penalty >= 0.50:
            alert = StreamingDiscourseAlert(
                alert_id=f"ALT-OMISSION-{hashlib.sha256(chunk.raw_text.encode('utf-8')).hexdigest()[:8].upper()}",
                timestamp_s=chunk.timestamp_end_s,
                alert_type="HIGH_OMISSION_PENALTY",
                severity=decomp.omission_penalty,
                trigger_statement=chunk.raw_text[:120],
                recommended_countermeasure=f"Query negative space diff: missing counterweights {decomp.critical_omitted_counterweights}."
            )
            new_alerts.append(alert)
            self.alerts.append(alert)

        # 3. Grayzone Fracture Trigger (Direct tax fatigue / due-process dilution)
        lower_txt = chunk.raw_text.lower()
        if any(w in lower_txt for w in ["section 18a", "kashinath", "middle class tax", "jizya", "presumption of guilt"]):
            alert = StreamingDiscourseAlert(
                alert_id=f"ALT-GRAYZONE-{hashlib.sha256(chunk.raw_text.encode('utf-8')).hexdigest()[:8].upper()}",
                timestamp_s=chunk.timestamp_end_s,
                alert_type="GRAYZONE_FRACTURE_TRIGGER",
                severity=0.85,
                trigger_statement=chunk.raw_text[:120],
                recommended_countermeasure="Route to CulturalReligiousGrayzoneSieve and calculate intra-civilizational fracture index."
            )
            new_alerts.append(alert)
            self.alerts.append(alert)

        # Distill claims if store provided
        distilled_count = 0
        if store:
            from ..core.conversation_distiller import ChatConversationDistiller
            rep = ChatConversationDistiller.distill_text(chunk.raw_text, source_context=f"stream_chunk_{chunk.chunk_id}")
            if rep.claims:
                distilled_count = store.record_distillation_report(rep.to_dict())

        return ChunkAuditTelemetry(
            chunk_id=chunk.chunk_id,
            timestamp_s=chunk.timestamp_end_s,
            window_factuality=decomp.factuality_ratio,
            window_ideology=decomp.ideology_intensity,
            window_agenda=decomp.agenda_potency,
            window_omission=decomp.omission_penalty,
            dominant_ideology=decomp.dominant_ideology,
            active_alerts=new_alerts,
            distilled_claims_count=distilled_count
        )



