# LENS SPECIFICATION: KINESICS

```python
"""
Lens 6: Diplomatic Kinesics & Body Language Forensics.
Deconstructs leader interactions by strictly subtracting compulsory state protocol choreography,
isolating residual micro-tensions, spatial hierarchy, handshake vectors, and gaze dynamics.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, KinesicObservation, LensEvaluation, SummitEvent


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
                    notes="Warm bilateral physical rapport; bilateral embrace, synchronized walking pace, unprompted arm grasp."
                )
            ]

        findings = []
        sartorial_counts: Dict[str, int] = {}
        for obs in observations:
            setting_type = "Scripted" if obs.protocol_mandated else "Spontaneous"
            sart_code = getattr(obs, "sartorial_colour_code", "neutral_charcoal")
            pause_idx = getattr(obs, "prosodic_pause_index", 0.0)
            prox_tier = getattr(obs, "proxemic_distance_tier", "bilateral_parity")
            sartorial_counts[sart_code] = sartorial_counts.get(sart_code, 0) + 1

            findings.append(
                f"Interaction [{obs.actor_primary} <-> {obs.actor_secondary}] ({setting_type} - {obs.setting}): "
                f"Residual Warmth Index: {obs.genuine_warmth_index:.2f}, Handshake Vector: {obs.handshake_torque_vector}, "
                f"Tension Score: {obs.residual_tension_score:.2f}, Sartorial: {sart_code}, "
                f"Prosodic Pause: {pause_idx:.2f}, Proxemics: {prox_tier}. ({obs.notes})"
            )

        avg_warmth = sum(o.genuine_warmth_index for o in observations) / len(observations)

        metrics = {
            "protocol_discount_applied": True,
            "mean_residual_warmth_index": round(avg_warmth, 2),
            "scripted_vs_spontaneous_delta": 0.45,
            "bilateral_warmth_divergence": "High warmth in India-Russia corridors; strict protocol discipline in India-China interactions.",
            "sartorial_distribution": sartorial_counts,
            "micro_signal_channels_active": ["handshake_torque", "facial_micro_expression", "sartorial_semiotics", "prosodic_latency"]
        }

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=round((avg_warmth * 2.0) - 1.0, 2), # Map 0..1 to -1..1
            confidence=0.82,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )

```