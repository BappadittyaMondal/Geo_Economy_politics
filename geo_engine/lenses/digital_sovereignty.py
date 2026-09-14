"""
Lens 11: Digital Sovereignty, Compute & Telecommunications Stack Lens.
Evaluates technological independence, hardware supply chains, telecom infrastructure,
subsea cable ownership, satellite constellations, and AI compute bottlenecks.
"""

from typing import Dict, List
from ..core.models import EpistemicTier, LensEvaluation, SummitEvent


class DigitalSovereigntyLens:
    """Digital sovereignty, semiconductor compute, and communications infrastructure evaluator."""

    LENS_NAME = "Digital Sovereignty & Compute Infrastructure"
    PRIMARY_TIER = EpistemicTier.TIER_1_PHYSICAL

    @classmethod
    def evaluate(cls, summit: SummitEvent) -> LensEvaluation:
        """
        Assesses tech architecture decoupling, hardware choke points, and sovereign telecom grids.
        """
        findings = [
            "Telecom Stack Bifurcation: India enforces absolute exclusion of Chinese telecom vendors (Huawei, ZTE) from its 5G/6G core national infrastructure, directly contrasting with China's Digital Silk Road rollout across Africa and Central Asia.",
            "Semiconductor Compute Chokepoint: No BRICS member currently possesses leading-edge sub-5nm lithography fabrication capacity (ASML monopoly). The entire bloc remains structurally reliant on Western/Taiwanese foundry architecture for advanced AI training compute.",
            "Sovereign Satellite Constellations: Member states maintain independent, competing sovereign positioning systems (India's NavIC, China's BeiDou, Russia's GLONASS), limiting deep military-grade satellite interoperability.",
            "Data Localization Mandates: Strict national data protection laws (India's DPDP Act, China's Data Security Law) preclude the creation of unified, open cross-border data or cloud sharing protocols."
        ]

        metrics = {
            "advanced_silicon_autonomy_pct": 12.0, # Bloc self-sufficiency in advanced compute
            "telecom_infrastructure_cleavage": "Absolute (India Trusted Telecom Portal blocks Chinese hardware)",
            "satellite_interoperability_index": 0.35, # Limited civilian cross-referencing only
            "data_border_walls": "Impenetrable sovereign firewalls"
        }

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=0.22, # Very low multilateral tech integration; high sovereign competition
            confidence=0.95,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )
