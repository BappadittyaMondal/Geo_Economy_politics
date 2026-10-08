"""
Phase 148: Multimodal Micro-Signal Telemetry Bridge.
Integrates raw acoustic DSP waveforms (WAV/PCM/MP3), FACS Action Units, and sartorial semiotics
into verified KinesicObservation instances and executes KinesicsLens evaluations with empirical rigor.
"""

from typing import Any, Dict, List, Optional, Union
import math

from geo_engine.core.models import EpistemicTier, KinesicObservation, LensEvaluation, SummitEvent
from geo_engine.video.acoustic_dsp import AcousticDSPWorker
from geo_engine.lenses.kinesics import MicroSignalExtractor, KinesicsLens


class MultimodalMicroSignalBridge:
    """
    Automated bridge connecting physical acoustic DSP signals,
    facial action units, and sartorial parameters directly to the 20-Lens Matrix.
    """

    @classmethod
    def bridge_audio_and_vision_to_observation(
        cls,
        actor_primary: str,
        actor_secondary: str,
        audio_data_or_path: Optional[Union[bytes, str]] = None,
        facs_action_units: Optional[Dict[str, float]] = None,
        sartorial_hue: Optional[str] = None,
        sartorial_hue_degrees: Optional[float] = None,
        setting: str = "formal_photocall",
        protocol_mandated: bool = False,
        handshake_torque_vector: str = "neutral_vertical",
        torso_angle_degrees: float = 0.0,
        proxemic_distance_tier: str = "bilateral_parity",
        notes: str = ""
    ) -> KinesicObservation:
        """
        Synthesizes a KinesicObservation from raw multimodal physical telemetry.
        """
        acoustic_metrics: Dict[str, Any] = {}
        if audio_data_or_path is not None:
            try:
                acoustic_metrics = AcousticDSPWorker.analyze_audio(audio_data_or_path)
            except Exception:
                acoustic_metrics = {}

        # Extract unified micro-signal features
        features = MicroSignalExtractor.derive_micro_signal_features(
            facs_action_units=facs_action_units,
            acoustic_prosody=acoustic_metrics,
            sartorial_hue_degrees=sartorial_hue_degrees,
            prosodic_pause_latency_s=acoustic_metrics.get("mean_pause_duration_seconds"),
            sartorial_hue=sartorial_hue
        )

        # Derive residual tension score
        # Combines masseter tension, pause latency, and pitch jitter
        au24 = (facs_action_units or {}).get("AU24", 0.0)
        au04 = (facs_action_units or {}).get("AU04", 0.0)
        pause_idx = features.get("prosodic_pause_index", 0.0)
        pitch_jitter = acoustic_metrics.get("pitch_jitter_local", 0.0)

        tension = min(1.0, round(
            (au24 * 0.4) + (au04 * 0.3) + (pause_idx * 0.2) + (min(1.0, pitch_jitter * 10.0) * 0.1),
            3
        ))

        sart_meaning = features.get("sartorial_semiotic_meaning", "standard_diplomatic_neutrality")
        leakage = features.get("micro_leakage_type", "baseline_neutral")

        observation_notes = notes or f"Multimodal telemetry: sartorial={sart_meaning}, leakage={leakage}"

        return KinesicObservation(
            actor_primary=actor_primary,
            actor_secondary=actor_secondary,
            setting=setting,
            protocol_mandated=protocol_mandated,
            handshake_torque_vector=handshake_torque_vector,
            torso_angle_degrees=torso_angle_degrees,
            residual_tension_score=tension,
            micro_expression_flag=features.get("micro_expression_flag", "neutral_resting"),
            sartorial_colour_code=features.get("sartorial_colour_code", "neutral_charcoal"),
            prosodic_pause_index=pause_idx,
            proxemic_distance_tier=proxemic_distance_tier,
            facs_action_units=facs_action_units or {},
            notes=observation_notes
        )

    @classmethod
    def evaluate_multimodal_summit(
        cls,
        summit_title: str,
        observations: List[KinesicObservation],
        location: str = "Bilateral Summit Venue",
        date: str = "2026-10-08",
        formal_communique_text: str = "Formal bilateral summit discussion with joint declaration."
    ) -> LensEvaluation:
        """
        Wraps observations in a SummitEvent and evaluates directly via KinesicsLens.
        """
        actors = list({obs.actor_primary for obs in observations} | {obs.actor_secondary for obs in observations})
        summit = SummitEvent(
            event_id=f"summit_{summit_title.lower().replace(' ', '_')[:25]}",
            title=summit_title,
            date=date,
            location=location,
            actors=actors,
            formal_communique_text=formal_communique_text,
            joint_statement_issued=True,
            bilateral_deliverables=["Strategic Framework", "Security Dialogue"]
        )
        return KinesicsLens.evaluate(summit=summit, observations=observations)
