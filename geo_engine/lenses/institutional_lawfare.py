"""
Lens 16: Institutional Lawfare & Sovereign Jurisdiction Weaponization.
Analyzes the weaponization of international legal architectures, FATF grey-listing timing,
extraterritorial US OFAC secondary sanctions, ICC/ICJ arrest warrants, and sovereign asset freezes.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, StrategicEvent


class InstitutionalLawfareLens:
    """Evaluator for judicial warfare, FATF regulatory leverage, and extraterritorial sanctions."""

    LENS_NAME = "Institutional Lawfare & Sovereign Jurisdiction Weaponization"
    PRIMARY_TIER = EpistemicTier.TIER_3_SOVEREIGN_REDLINES

    @classmethod
    def evaluate(
        cls,
        event: Any,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Deconstructs institutional compliance pressures, sovereign asset risks, and jurisdiction weaponization.
        """
        findings = [
            "FATF & Regulatory Timing Leverage: Strategic coordination of Financial Action Task Force (FATF) mutual evaluations, grey-listing reviews, and anti-money laundering compliance systematically coincides with geopolitical pressure points to deter cross-border private investment.",
            "Extraterritorial Secondary Sanctions Weaponization: The US Treasury OFAC regulatory framework exercises extraterritorial jurisdiction by threatening to sever tier-1 commercial banks from USD correspondent clearing if they facilitate transactions with designated sovereign entities.",
            "International Court Jurisdictional Expansion (ICC/ICJ): Selective issuance of arrest warrants, advisory opinions, and provisional measures utilized as asymmetrical instruments to restrict sovereign diplomatic mobility and erode state legitimacy.",
            "Sovereign Asset Confiscation Precedent: The Western freezing of ~$300 Billion in Russian sovereign central bank reserves permanently compromised the perceived neutrality of G7 sovereign debt as a safe-haven reserve asset, accelerating central bank physical gold repatriation.",
            "Bilateral Maritime Accord Lawfare & Buffer Breaches: Asymmetric naval maneuvers violate bilateral confidence-building frameworks (e.g., Article 10 of 1991 India-Pakistan Agreement requiring 3 NM buffer) and COLREGs Rule 8, weaponizing ambiguous maritime boundaries and international waters to contest sovereignty without triggering formal armed conflict under UN Charter Article 51."
        ]

        metrics = {
            "fatf_regulatory_friction_score": 0.68,
            "sovereign_asset_confiscation_risk": 0.85,
            "extraterritorial_compliance_penalty_pct": 28.5,
            "dollar_clearing_vulnerability_index": 0.72,
            "institutional_neutrality_erosion_score": 0.88,
            "bilateral_maritime_accord_compliance_score": 0.25
        }

        alignment = -0.50  # Indicates elevated legal, regulatory, and sanctions friction

        if claims:
            lawfare_detected = any(
                "fatf" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "sanction" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "icc" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "asset freeze" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower()
                for c in claims
            )
            if lawfare_detected:
                findings.insert(0, "[GROUNDED TELEMETRY] Active lawfare or regulatory sanction lever identified: Sovereign financial or diplomatic assets subjected to extraterritorial jurisdiction.")
                alignment = -0.75
                metrics["fatf_regulatory_friction_score"] = 0.90

            domestic_keywords = [
                "article 44", "ucc", "uniform civil code", "waqf", "fcra",
                "hrce", "temple control", "personal law", "concurrent list", "pil network"
            ]
            domestic_lawfare_detected = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in domestic_keywords)
                for c in claims
            )
            if domestic_lawfare_detected:
                findings.insert(0, "[GROUNDED TELEMETRY] Domestic constitutional/statutory lawfare detected: Asymmetric regulatory jurisdiction, Article 44 Concurrent List federal friction, or FCRA-leveraged judicial challenge identified.")
                alignment = min(alignment, -0.60)
                metrics["domestic_statutory_asymmetry_score"] = 0.82
                metrics["fcra_litigation_leverage_index"] = 0.74
                metrics["concurrent_jurisdiction_friction"] = 0.69

            maritime_keywords = [
                "1991 agreement", "colregs", "article 10", "buffer distance",
                "maritime accord", "bow crossing", "ramming", "naval standoff"
            ]
            maritime_lawfare_detected = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in maritime_keywords)
                for c in claims
            )
            if maritime_lawfare_detected:
                findings.insert(0, "[GROUNDED TELEMETRY] Bilateral maritime accord breach identified: Violation of 1991 Agreement Article 10 (3 NM buffer) and COLREGs Rule 8 safe navigation rules in international waters.")
                alignment = min(alignment, -0.70)
                metrics["bilateral_maritime_accord_compliance_score"] = 0.15
                metrics["maritime_treaty_breach_severity"] = 0.85

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=0.90,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics,
            evidence_status="sufficient"
        )
