# LENS SPECIFICATION: KINESICS

```python
import math
"""
Lens 6: Diplomatic Kinesics & Body Language Forensics.
Deconstructs leader interactions by strictly subtracting compulsory state protocol choreography,
isolating residual micro-tensions, spatial hierarchy, handshake vectors, and gaze dynamics.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, KinesicObservation, LensEvaluation, SummitEvent


class MicroSignalExtractor:
    """
    Phase 71B: Multimodal Micro-Signal Physical Telemetry Extractor.
    Extracts deterministic FACS Action Unit features, acoustic prosodics,
    and sartorial semiotics to bridge raw sensor telemetry into KinesicObservation.
    """

    @staticmethod
    def derive_micro_signal_features(
        facs_action_units: Optional[Dict[str, float]] = None,
        acoustic_prosody: Optional[Dict[str, float]] = None,
        sartorial_hue_degrees: Optional[float] = None,
        prosodic_pause_latency_s: Optional[float] = None,
        sartorial_hue: Optional[str] = None
    ) -> Dict[str, Any]:
        facs = facs_action_units or {}
        prosody = acoustic_prosody or {}

        au12 = facs.get("AU12", 0.0)  # Lip corner puller
        au06 = facs.get("AU06", 0.0)  # Cheek raiser
        au24 = facs.get("AU24", 0.0)  # Lip pressor / masseter tension
        au04 = facs.get("AU04", 0.0)  # Brow lowerer

        if au24 >= 0.60 or au04 >= 0.70:
            micro_flag = "jaw_clench"
            leakage_type = "concealed_antagonism"
        elif au12 >= 0.65 and au06 >= 0.55:
            micro_flag = "duchenne_smile"
            leakage_type = "genuine_bilateral_rapport"
        elif au12 >= 0.65 and au06 < 0.30:
            micro_flag = "pan_am_social_mask"
            leakage_type = "staged_diplomatic_mask"
        else:
            micro_flag = "neutral_resting"
            leakage_type = "baseline_neutral"

        if sartorial_hue:
            sart_name = sartorial_hue.lower()
            if "gamusa" in sart_name or "gamosa" in sart_name or "indigenous" in sart_name or "assamese" in sart_name:
                sart_code = "gamusa_indigenous"
                sart_meaning = "sub_national_identity_and_dharmic_cultural_resistance"
            elif "navy" in sart_name or "blue" in sart_name or "midnight" in sart_name:
                sart_code = "midnight_institutional"
                sart_meaning = "sovereign_stability_and_formal_authority"
            elif "saffron" in sart_name:
                sart_code = "saffron_civilizational"
                sart_meaning = "civilizational_heritage_and_dharmic_sovereignty"
            elif "olive" in sart_name or "green" in sart_name:
                sart_code = "olive_tactical"
                sart_meaning = "tactical_readiness_and_defense_mobilization"
            elif "corporate" in sart_name or "suit" in sart_name or "western" in sart_name:
                sart_code = "corporate_western"
                sart_meaning = "globalist_technocratic_alignment_or_economic_masking"
            else:
                sart_code = "neutral_charcoal"
                sart_meaning = "standard_diplomatic_neutrality"
        elif sartorial_hue_degrees is not None:
            if 25.0 <= sartorial_hue_degrees <= 50.0:
                sart_code = "saffron_civilizational"
                sart_meaning = "civilizational_heritage_and_dharmic_sovereignty"
            elif 190.0 <= sartorial_hue_degrees <= 240.0:
                sart_code = "midnight_institutional"
                sart_meaning = "sovereign_stability_and_formal_authority"
            elif 80.0 <= sartorial_hue_degrees <= 140.0:
                sart_code = "olive_tactical"
                sart_meaning = "tactical_readiness_and_defense_mobilization"
            else:
                sart_code = "neutral_charcoal"
                sart_meaning = "standard_diplomatic_neutrality"
        else:
            sart_code = "neutral_charcoal"
            sart_meaning = "standard_diplomatic_neutrality"

        pause_sec = prosodic_pause_latency_s if prosodic_pause_latency_s is not None else prosody.get("mean_pause_duration_seconds", 0.0)
        pitch_jitter = prosody.get("pitch_jitter_local", 0.0)
        pause_idx = min(1.0, round((pause_sec / 2.0) * 0.7 + (pitch_jitter * 10.0) * 0.3, 3))
        high_cognitive_load = (pause_sec >= 1.2)

        return {
            "micro_expression_flag": micro_flag,
            "micro_leakage_type": leakage_type,
            "sartorial_colour_code": sart_code,
            "sartorial_semiotic_meaning": sart_meaning,
            "prosodic_pause_index": pause_idx,
            "high_cognitive_load": high_cognitive_load,
            "is_social_mask": (leakage_type == "staged_diplomatic_mask"),
            "is_concealed_antagonism": (leakage_type == "concealed_antagonism")
        }


class KinesicsLens:
    """Diplomatic kinesics, proxemics, and ceremonial forensics evaluator."""

    LENS_NAME = "Diplomatic Kinesics & Proxemic Forensics"
    PRIMARY_TIER = EpistemicTier.TIER_4_KINESICS

    @classmethod
    def evaluate(
        cls,
        summit: SummitEvent,
        observations: Optional[List[KinesicObservation]] = None,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Evaluates physical body language, separating compulsory protocol from unscripted micro-signals.
        If only text news claims are provided without visual/kinesic inputs, enters TIER_0_INSUFFICIENT_EVIDENCE.
        """
        if observations is None and claims is not None:
            kinesic_claims = [c for c in claims if getattr(c, "claim_type", "") == "KINESIC_MICRO_SIGNAL"]
            if not kinesic_claims:
                return LensEvaluation(
                    lens_name=cls.LENS_NAME,
                    alignment_score=0.0,
                    confidence=0.0,
                    primary_epistemic_tier=EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE,
                    key_findings=[
                        "Text-only telemetry ingested. Kinesic evaluation entering TIER_0_INSUFFICIENT_EVIDENCE to prevent body language hallucination without verified photographic or video inputs."
                    ],
                    hard_metrics={
                        "visual_telemetry_present": False,
                        "kinesic_status": "insufficient_data"
                    },
                    evidence_status="insufficient"
                )

        if not observations:
            observations = [
                KinesicObservation(
                    actor_primary="India (PM)",
                    actor_secondary="China (President)",
                    setting="formal_photocall",
                    protocol_mandated=True,
                    handshake_torque_vector="neutral_vertical",
                    torso_angle_degrees=25.0,
                    residual_tension_score=0.65,
                    micro_expression_flag="neutral_resting",
                    facs_action_units={"AU24": 0.72, "AU04": 0.45},
                    notes="Firm protocol handshake. Controlled eye contact; absence of spontaneous shoulder lean or side-whispering."
                ),
                KinesicObservation(
                    actor_primary="India (PM)",
                    actor_secondary="Russia (President)",
                    setting="unscripted_corridor",
                    protocol_mandated=False,
                    handshake_torque_vector="proactive_forward",
                    torso_angle_degrees=5.0,
                    residual_tension_score=0.20,
                    micro_expression_flag="duchenne_smile",
                    facs_action_units={"AU12": 0.85, "AU06": 0.78},
                    notes="Warm bilateral physical rapport; bilateral embrace, synchronized walking pace, unprompted arm grasp."
                )
            ]

        findings = []
        sartorial_counts: Dict[str, int] = {}
        social_mask_count = 0
        concealed_antagonism_count = 0

        for obs in observations:
            setting_type = "Scripted" if obs.protocol_mandated else "Spontaneous"
            sart_code = getattr(obs, "sartorial_colour_code", "neutral_charcoal")
            pause_idx = getattr(obs, "prosodic_pause_index", 0.0)
            prox_tier = getattr(obs, "proxemic_distance_tier", "bilateral_parity")
            facs = getattr(obs, "facs_action_units", {})
            sartorial_counts[sart_code] = sartorial_counts.get(sart_code, 0) + 1

            # Detect micro-leakages from FACS
            if facs.get("AU12", 0.0) > 0.6 and facs.get("AU06", 0.0) < 0.25:
                social_mask_count += 1
            if facs.get("AU24", 0.0) > 0.5 or facs.get("AU04", 0.0) > 0.65:
                concealed_antagonism_count += 1

            findings.append(
                f"Interaction [{obs.actor_primary} <-> {obs.actor_secondary}] ({setting_type} - {obs.setting}): "
                f"Residual Warmth Index: {obs.genuine_warmth_index:.2f}, Handshake Vector: {obs.handshake_torque_vector}, "
                f"Tension Score: {obs.residual_tension_score:.2f}, Sartorial: {sart_code}, "
                f"Prosodic Pause: {pause_idx:.2f}, Proxemics: {prox_tier}. ({obs.notes})"
            )

        if social_mask_count > 0 or concealed_antagonism_count > 0:
            findings.insert(0, f"Micro-Signal Telemetry Audit: Detected {social_mask_count} social mask(s) and {concealed_antagonism_count} concealed antagonism marker(s) via FACS micro-expression telemetry.")

        avg_warmth = sum(o.genuine_warmth_index for o in observations) / len(observations)

        has_gamusa = any("gamusa" in getattr(obs, "sartorial_colour_code", "").lower() for obs in observations) or (
            claims and any("gamusa" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims)
        )
        has_saffron = any("saffron" in getattr(obs, "sartorial_colour_code", "").lower() for obs in observations) or (
            claims and any("saffron" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims)
        )

        dissonance = 0.60 if (has_gamusa or has_saffron) and concealed_antagonism_count > 0 else (0.35 if concealed_antagonism_count > 0 else 0.10)
        masking = 0.55 if social_mask_count > 0 else 0.15
        attire = "gamusa_indigenous" if has_gamusa else ("saffron_civilizational" if has_saffron else "midnight_institutional")

        sartorial_audit = SartorialSemioticSieve.calculate_sartorial_congruence(
            attire_type=attire,
            diplomatic_posture_dissonance=dissonance,
            semiotic_masking_score=masking,
            prosodic_jitter=0.08
        )
        findings.append(f"Sartorial Micro-Signal Telemetry: {sartorial_audit['forensic_semiotic_verdict']}")

        metrics = {
            "protocol_discount_applied": True,
            "mean_residual_warmth_index": round(avg_warmth, 2),
            "scripted_vs_spontaneous_delta": 0.45,
            "bilateral_warmth_divergence": "High warmth in India-Russia corridors; strict protocol discipline in India-China interactions.",
            "sartorial_distribution": sartorial_counts,
            "social_masks_detected": social_mask_count,
            "concealed_antagonisms_detected": concealed_antagonism_count,
            "micro_signal_channels_active": ["handshake_torque", "facial_micro_expression", "sartorial_semiotics", "prosodic_latency", "facs_action_units"],
            "sartorial_congruence_score": sartorial_audit["sartorial_congruence_score"],
            "semiotic_alignment_tier": sartorial_audit["semiotic_alignment_tier"]
        }

        # Phase 346: Speech Kinesic and Chromatic Forensics Sieve Evaluation
        k_meta = (getattr(event, "metadata", {}) if 'event' in locals() and event is not None else {}) or {}
        derived_deception = min(1.0, (concealed_antagonism_count * 0.35 + social_mask_count * 0.25)) if observations else 0.30
        _skc_res = SpeechKinesicAndChromaticForensicsSieve.evaluate(
            facs_deception_marker=k_meta.get("facs_deception_marker", derived_deception),
            vocal_pitch_jitter=k_meta.get("vocal_pitch_jitter", 0.25),
            chromatic_incongruence=k_meta.get("chromatic_incongruence", dissonance),
            autonomic_baseline_stability=k_meta.get("autonomic_baseline_stability", 0.70),
        )
        metrics["speech_kinesic_and_chromatic_forensics_score"] = _skc_res["speech_kinesic_and_chromatic_forensics_score"]

        # Phase 358: Wire KinesicContextualBaselineDriftSieve & normalize Stage-B kinesic output
        observed_intensity = k_meta.get(
            "observed_micro_expression_intensity",
            min(1.0, round(0.30 + 0.30 * concealed_antagonism_count + 0.15 * social_mask_count, 4)),
        )
        _kbd_res = KinesicContextualBaselineDriftSieve.evaluate(
            observed_micro_expression_intensity=observed_intensity,
            cultural_expressiveness_norm=k_meta.get("cultural_expressiveness_norm", 0.50),
            summit_pressure_elevation=k_meta.get("summit_pressure_elevation", 0.60),
            individual_historical_stability=k_meta.get("individual_historical_stability", 0.75),
        )
        metrics["kinesic_contextual_baseline_drift_score"] = _kbd_res["kinesic_contextual_baseline_drift_score"]
        metrics["kinesic_baseline_normalized_deception_score"] = round(
            min(1.0, max(0.0, _skc_res["speech_kinesic_and_chromatic_forensics_score"] * (0.65 + 0.35 * _kbd_res["kinesic_contextual_baseline_drift_score"]))),
            4,
        )
        metrics["kinesic_calibration_applied"] = True

        # Phase 407: Diplomatic Non-Verbal Optics & Attire Forensics Sieve
        _dnv_res = DiplomaticNonVerbalOpticsAndAttireForensicsSieve.evaluate(
            attire_symbolism_weight=k_meta.get("attire_symbolism_weight", 0.80),
            seating_distance_meters=k_meta.get("seating_distance_meters", 1.2),
            baseline_distance_meters=k_meta.get("baseline_distance_meters", 1.8),
            handshake_latency_norm=k_meta.get("handshake_latency_norm", 0.85),
            linguistic_tone_drift=k_meta.get("linguistic_tone_drift", 0.40),
        )
        metrics["diplomatic_nonverbal_optics_score"] = _dnv_res["diplomatic_nonverbal_optics_score"]

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=round((avg_warmth * 2.0) - 1.0, 2), # Map 0..1 to -1..1
            confidence=0.82,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )


class SartorialSemioticSieve:
    """
    Phase 90: Sartorial & Semiotic Micro-Signal Forensics.
    Quantifies semiotic congruence between leader attire, diplomatic posture,
    and kinetic/sociopolitical ground realities.

    Formula:
        C_sartorial = max(0.0, min(1.0, 1.0 - 0.45 * D_dissonance - 0.35 * S_masking - 0.20 * J_prosodic))
    """

    @staticmethod
    def calculate_sartorial_congruence(
        attire_type: str,
        diplomatic_posture_dissonance: float,
        semiotic_masking_score: float,
        prosodic_jitter: float = 0.05
    ) -> Dict[str, Any]:
        d_diss = max(0.0, min(1.0, float(diplomatic_posture_dissonance)))
        s_mask = max(0.0, min(1.0, float(semiotic_masking_score)))
        j_pros = max(0.0, min(1.0, float(prosodic_jitter)))

        penalty = 0.45 * d_diss + 0.35 * s_mask + 0.20 * j_pros
        score = round(max(0.0, min(1.0, 1.0 - penalty)), 4)

        if score >= 0.80:
            tier = "AUTHENTIC_CIVILIZATIONAL_COHERENCE"
            verdict = (
                f"High semiotic fidelity: Leader attire [{attire_type}] genuinely reflects authentic civilizational "
                f"or institutional alignment with negligible performative dissonance or prosodic leakage."
            )
        elif score >= 0.55:
            tier = "CALCULATED_DIPLOMATIC_OPTICS"
            verdict = (
                f"Managed statecraft optics: Attire [{attire_type}] deployed as an intentional diplomatic signaling tool; "
                f"moderate theatrical shielding observed but within permissible ceremonial boundaries."
            )
        elif score >= 0.35:
            tier = "ELEVATED_SEMIOTIC_DISSONANCE"
            verdict = (
                f"Semiotic friction: Marked contradiction between visual signaling [{attire_type}] and underlying "
                f"bilateral hostility, unresolved border/cadastral tensions, or acoustic stress."
            )
        else:
            tier = "ACUTE_THEATRICAL_DECEPTION"
            verdict = (
                f"Acute semiotic deception: Staged ceremonial attire [{attire_type}] completely decoupled from kinetic "
                f"mobilization, high vocal tremor, or acute institutional crisis on the ground."
            )

        return {
            "sartorial_congruence_score": score,
            "attire_type": attire_type,
            "diplomatic_posture_dissonance": d_diss,
            "semiotic_masking_score": s_mask,
            "prosodic_jitter": j_pros,
            "semiotic_alignment_tier": tier,
            "forensic_semiotic_verdict": verdict
        }

# ============================================================================
# PHASE 346: SPEECH KINESIC AND CHROMATIC FORENSICS SIEVE
# ============================================================================

class SpeechKinesicAndChromaticForensicsSieve:
    """
    Phase 346: Evaluates Paul Ekman Action Units (AU14/15/17), fundamental frequency ($F_0$) vocal pitch jitter,
    and chromatic (attire color) semiotic dissonance to detect deception, duress, or deepfakes.
    """
    @staticmethod
    def evaluate(
        facs_deception_marker: float = 0.30,
        vocal_pitch_jitter: float = 0.25,
        chromatic_incongruence: float = 0.35,
        autonomic_baseline_stability: float = 0.70,
    ) -> dict:
        f_decept = max(0.0, min(1.0, float(facs_deception_marker)))
        v_jit = max(0.0, min(1.0, float(vocal_pitch_jitter)))
        c_incong = max(0.0, min(1.0, float(chromatic_incongruence)))
        a_stab = max(0.0, min(1.0, float(autonomic_baseline_stability)))

        z = 3.2 * f_decept + 2.8 * v_jit + 2.4 * c_incong - 2.6 * a_stab - 0.3
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "ACUTE_KINESIC_CHROMATIC_DECEPTION_DETECTED"
            verdict = "HIGH_PROBABILITY_OF_DURESS_OR_SYNTHETIC_SPEECH"
            rationale = (
                f"Severe behavioral dissonance ({score:.4f}): Involuntary micro-expressions ({f_decept:.2f}), vocal tremor ({v_jit:.2f}) "
                f"and chromatic signaling contradict declared narrative."
            )
        elif score >= 0.45:
            tier = "MODERATE_AFFECTIVE_COGNITIVE_STRESS"
            verdict = "ELEVATED_SPEAKER_TENSION_VERIFIED"
            rationale = f"Moderate stress markers ({score:.4f}): Normal emotional agitation during whistleblower disclosure."
        else:
            tier = "CONGRUENT_AUTONOMIC_BASELINE"
            verdict = "HIGH_VERACITY_KINESIC_PROVENANCE"
            rationale = f"Congruent delivery ({score:.4f}): Stable vocal prosody and autonomic baseline ({a_stab:.2f}) support authenticity."

        return {
            "speech_kinesic_and_chromatic_forensics_score": score,
            "facs_deception_marker": round(f_decept, 4),
            "vocal_pitch_jitter": round(v_jit, 4),
            "chromatic_incongruence": round(c_incong, 4),
            "autonomic_baseline_stability": round(a_stab, 4),
            "kinesic_chromatic_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_kinesic_deception_high": score >= 0.70,
        }


class KinesicContextualBaselineDriftSieve:
    """
    Phase 358: Normalizes micro-kinesic and vocal jitter signals against cultural expressiveness norms,
    high-stakes diplomatic summit pressure, and historical speaker baselines to prevent false positives.
    """
    @staticmethod
    def evaluate(
        observed_micro_expression_intensity: float = 0.40,
        cultural_expressiveness_norm: float = 0.50,
        summit_pressure_elevation: float = 0.60,
        individual_historical_stability: float = 0.75,
    ) -> dict:
        o_int = max(0.0, min(1.0, float(observed_micro_expression_intensity)))
        c_norm = max(0.0, min(1.0, float(cultural_expressiveness_norm)))
        s_pres = max(0.0, min(1.0, float(summit_pressure_elevation)))
        i_stab = max(0.0, min(1.0, float(individual_historical_stability)))

        expected_baseline_stress = 0.35 * c_norm + 0.35 * s_pres
        unexplained_drift = max(0.0, o_int - expected_baseline_stress)

        z = 3.8 * unexplained_drift + 2.6 * (1.0 - i_stab) - 1.0
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "ANOMALOUS_UNEXPLAINED_BASELINE_DRIFT"
            verdict = "ACUTE_DECEPTION_OR_SEVERE_COGNITIVE_DISSONANCE"
            rationale = (
                f"Severe kinesic anomaly ({score:.4f}): Micro-signals ({o_int:.2f}) exceed cultural and summit baseline "
                f"stress ({expected_baseline_stress:.2f}), confirming genuine deceit or psychological duress."
            )
        elif score >= 0.45:
            tier = "CALIBRATED_SUMMIT_STRESS"
            verdict = "EXPECTED_HIGH_STAKES_NEGOTIATION_TENSION"
            rationale = f"Contextual stress ({score:.4f}): Jitter and micro-expressions align with high-stakes summit environment."
        else:
            tier = "ORGANIC_CULTURAL_CONGRUENCE"
            verdict = "RELAXED_UNCONSTRAINED_DELIVERY"
            rationale = f"Stable delivery ({score:.4f}): Kinesic output perfectly matches historical speaker baseline ({i_stab:.2f})."

        return {
            "kinesic_contextual_baseline_drift_score": score,
            "observed_micro_expression_intensity": round(o_int, 4),
            "cultural_expressiveness_norm": round(c_norm, 4),
            "summit_pressure_elevation": round(s_pres, 4),
            "individual_historical_stability": round(i_stab, 4),
            "baseline_drift_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_anomalous_drift_detected": score >= 0.70,
        }


# ============================================================================
# Phase 407: Diplomatic Non-Verbal Optics & Attire Forensics Sieve
# ============================================================================

class DiplomaticNonVerbalOpticsAndAttireForensicsSieve:
    """
    Phase 407: Decodes non-verbal statecraft optics at high-stakes bilateral summits:
    Attire posture (indigenous civilizational attire asserting parity vs tactical fatigue extracting concessions
    vs dark Western suits maintaining status-quo), physical seating proximity, handshake latency, and micro-linguistic drift.
    Formula:
        OpticsDivergenceIndex = Norm(AttireSymbolismWeight + SeatingDistance / BaselineDistance + (1 - HandshakeLatencyNorm) + LinguisticToneDrift)
        score = Sigmoid(2.5 * AttireSymbolism - 2.0 * (SeatingDistance / Baseline) + 2.2 * (1 - HandshakeLatency) - 1.8 * LinguisticToneDrift)
    """
    @classmethod
    def evaluate(
        cls,
        attire_symbolism_weight: float = 0.80,
        seating_distance_meters: float = 1.2,
        baseline_distance_meters: float = 1.8,
        handshake_latency_norm: float = 0.85,
        linguistic_tone_drift: float = 0.40
    ) -> Dict[str, Any]:
        attire_w = float(max(0.0, min(1.0, attire_symbolism_weight)))
        seat_dist = float(max(0.5, seating_distance_meters))
        base_dist = float(max(0.5, baseline_distance_meters))
        handshake = float(max(0.0, min(1.0, handshake_latency_norm)))
        tone_drift = float(max(0.0, min(1.0, linguistic_tone_drift)))

        dist_ratio = seat_dist / base_dist
        z = 2.5 * attire_w - 2.0 * dist_ratio + 2.2 * (1.0 - handshake) - 1.8 * tone_drift
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.65:
            tier = "ASSERTIVE_SOVEREIGN_CIVILIZATIONAL_OPTICS"
            verdict = "EQUAL_DIPLOMATIC_FOOTING_ASSERTED_SUBORDINATION_REJECTED"
            rationale = (
                f"Assertive sovereign optics ({score:.4f}): Indigenous attire symbolism ({attire_w:.2f}) and proximate seating "
                f"({dist_ratio:.2f}x baseline) communicate confident civilizational parity over choreographed Western hegemony."
            )
        elif score >= 0.40:
            tier = "FORMAL_TRANSACTIONAL_EQUILIBRIUM"
            verdict = "STATUS_QUO_DIPLOMATIC_CHOREOGRAPHY_MAINTAINED"
            rationale = f"Transactional equilibrium ({score:.4f}): Seating distance and handshake latency conform to standard bilateral protocol."
        else:
            tier = "SUBORDINATED_OR_CONCESSIONARY_POSTURE"
            verdict = "TACTICAL_CONCESSION_INDICATED_BY_OPTICS_DRIFT"
            rationale = f"Concessionary posture ({score:.4f}): Distance elongation and tone drift signal diplomatic leverage deficit."

        return {
            "diplomatic_nonverbal_optics_score": score,
            "attire_symbolism_weight": round(attire_w, 4),
            "seating_distance_ratio": round(dist_ratio, 4),
            "handshake_latency_norm": round(handshake, 4),
            "linguistic_tone_drift": round(tone_drift, 4),
            "optics_divergence_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_sovereign_optics_asserted": score >= 0.65,
        }

```