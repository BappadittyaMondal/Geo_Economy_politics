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
        metadata_fallback: Optional[Dict[str, Any]] = None
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
            transcript = cls.fetch_stream_transcript(url_or_id, metadata_fallback=metadata_fallback)
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
            "avionics_sovereignty_audit": avionics_audit,
            "chokepoint_audit": chokepoint_audit,
            "endowment_audit": endowment_audit,
            "rollback_audit": rollback_audit,
            "sartorial_audit": sartorial_audit,
            "chronology_audit": chronology_audit,
            "tenure_audit": tenure_audit,
            "decomposed_claim": decomposed_claim.model_dump() if decomposed_claim else None,
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

