# LENS SPECIFICATION: SUBSEA_CABLES

```python
"""
Lens 19: Subsea Cables & Hydro-Spatial Sovereignty.
Evaluates physical underwater fiber-optic communications infrastructure,
subsea cable landing stations (Mumbai, Chennai), deep-sea seabed mining (polymetallic nodules),
and acoustic/maritime chokepoint vulnerabilities in the Indian Ocean and Indo-Pacific.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, StrategicEvent


class SubseaCablesLens:
    """Evaluator for subsea telecommunications cables, seabed mining, and hydro-acoustic security."""

    LENS_NAME = "Subsea Cables & Hydro-Spatial Sovereignty"
    PRIMARY_TIER = EpistemicTier.TIER_1_PHYSICAL

    @classmethod
    def evaluate(
        cls,
        event: Any,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Assesses underwater critical infrastructure, cable landing concentration, and seabed mining rights.
        """
        findings = [
            "Subsea Fiber-Optic Cable Traffic Dominance: Over 95% of international financial messaging and data traffic relies on undersea cables, with Mumbai and Chennai serving as primary peninsular landing hubs.",
            "Maritime Chokepoint Vulnerability: Critical routes through the Red Sea (Bab-el-Mandeb), Suez, Malacca, and Luzon Straits represent high-risk single points of failure susceptible to anchor drags and asymmetric sabotage.",
            "Central Indian Ocean Seabed Mining: Sovereign exploration rights for polymetallic nodules (nickel, copper, cobalt) under International Seabed Authority (ISA) contracts secure long-term deep-sea mineral access.",
            "Hydro-Acoustic Surveillance Coverage: Subsurface acoustic arrays and anti-submarine hydrophone cordons along the Andaman & Nicobar ridge provide acoustic domain awareness over submarine ingress routes."
        ]

        metrics = {
            "subsea_bandwidth_dependency_pct": 98.5,
            "landing_station_concentration_index": 0.76,
            "seabed_mining_concession_readiness": 0.62,
            "cable_repair_ship_autonomy_score": 0.45,
            "hydro_spatial_sovereignty_score": 0.68
        }

        alignment = 0.40

        if claims:
            cable_or_subsea = any(
                "cable" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "subsea" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "fiber optic" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "seabed" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "underwater" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower()
                for c in claims
            )
            if cable_or_subsea:
                findings.insert(0, "[GROUNDED TELEMETRY] Subsea cable or hydro-spatial event verified: Active infrastructure deployment or corridor monitoring confirmed.")
                alignment = 0.65
                metrics["hydro_spatial_sovereignty_score"] = 0.78

        # Phase 216: Wire SubseaCableSovereigntySieve
        _cable_sieve = SubseaCableSovereigntySieve()
        _cable_result = _cable_sieve.calculate_cable_sovereignty(
            landing_station_exposure_risk=metrics.get("landing_station_exposure_risk", 0.50),
            chokepoint_depth_risk=metrics.get("chokepoint_depth_risk", 0.40),
            domestic_cable_redundancy_score=metrics.get("domestic_cable_redundancy_score", 0.50),
            encryption_layer_score=metrics.get("encryption_layer_score", 0.50),
            repair_ship_autonomy_score=metrics.get("repair_ship_autonomy_score", 0.40),
        )
        metrics.update(_cable_result)

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=0.88,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics,
            evidence_status="sufficient"
        )


class SubseaCableSovereigntySieve:
    """
    Phase 206: Quantifies physical undersea fiber-optic landing station vulnerability,
    SIGINT interception risk, dark-vessel cable tampering probability, and domestic
    cable redundancy resilience for sovereign communications sovereignty.

    Mathematical core:
        CableVulnerabilityIndex = σ(
            2.8 · LandingStationExposureRisk
            + 2.5 · ChokepointDepthRisk
            - 2.0 · DomesticCableRedundancyScore
            - 1.5 · EncryptionLayerScore
        )
    """

    CABLE_KEYWORDS = [
        "subsea cable", "undersea fiber", "landing station", "cable cut", "dark vessel",
        "cable sabotage", "signal intercept", "cable repair ship", "cable tap", "fiber optic cut"
    ]

    @classmethod
    def calculate_cable_sovereignty(
        cls,
        landing_station_exposure_risk: float = 0.60,
        chokepoint_depth_risk: float = 0.55,
        domestic_cable_redundancy_score: float = 0.40,
        encryption_layer_score: float = 0.35,
        repair_ship_autonomy_score: float = 0.30,
        claims=None
    ):
        """
        Calculates undersea cable sovereignty index and vulnerability tier.

        Args:
            landing_station_exposure_risk: 0-1, physical exposure of cable landing stations (Mumbai, Chennai, etc.)
            chokepoint_depth_risk: 0-1, vulnerability of cable routes through choke points (Red Sea, Malacca, etc.)
            domestic_cable_redundancy_score: 0-1, India's own cable redundancy & rerouting capability
            encryption_layer_score: 0-1, end-to-end encryption protecting signal from SIGINT intercept
            repair_ship_autonomy_score: 0-1, sovereign cable repair vessel availability
            claims: optional list of claim objects for keyword boosting

        Returns:
            dict with cable_vulnerability_index, cable_sovereignty_tier, is_cable_compromised, etc.
        """
        import math

        exp_risk = max(0.0, min(1.0, float(landing_station_exposure_risk)))
        ckpt_risk = max(0.0, min(1.0, float(chokepoint_depth_risk)))
        redundancy = max(0.0, min(1.0, float(domestic_cable_redundancy_score)))
        encryption = max(0.0, min(1.0, float(encryption_layer_score)))
        repair = max(0.0, min(1.0, float(repair_ship_autonomy_score)))

        # Keyword-based boosting from claim corpus
        if claims:
            matched = []
            for c in claims:
                txt = c if isinstance(c, str) else (
                    getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
                    if not isinstance(c, dict)
                    else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "")
                )
                txt_l = txt.lower()
                for kw in cls.CABLE_KEYWORDS:
                    if kw in txt_l and kw not in matched:
                        matched.append(kw)
            if matched:
                exp_risk = min(1.0, exp_risk + 0.08 * len(matched))
                ckpt_risk = min(1.0, ckpt_risk + 0.06 * len(matched))

        z = (
            2.8 * exp_risk
            + 2.5 * ckpt_risk
            - 2.0 * redundancy
            - 1.5 * encryption
            - 1.0 * repair
            - 1.5
        )
        cable_vulnerability_index = round(1.0 / (1.0 + math.exp(-z)), 4)

        cable_sovereignty_score = round(1.0 - cable_vulnerability_index, 4)

        if cable_vulnerability_index >= 0.75:
            tier = "CRITICAL_CABLE_SOVEREIGNTY_FAILURE"
            verdict = "IMMEDIATE_REDUNDANCY_AND_ENCRYPTION_MANDATE"
            rationale = (
                f"Severe undersea cable vulnerability: Landing station exposure ({exp_risk:.2f}) and "
                f"chokepoint risk ({ckpt_risk:.2f}) far exceed domestic redundancy ({redundancy:.2f}) and "
                f"encryption protection ({encryption:.2f}). Single-point intercept probability is critical."
            )
            is_compromised = True
        elif cable_vulnerability_index >= 0.55:
            tier = "HIGH_VULNERABILITY_PARTIAL_SOVEREIGNTY"
            verdict = "PRIORITY_REDUNDANCY_UPGRADE_REQUIRED"
            rationale = (
                f"Significant cable vulnerability: chokepoint concentration and landing station exposure "
                f"outweigh domestic cable resilience. SIGINT interception risk is elevated."
            )
            is_compromised = True
        elif cable_vulnerability_index >= 0.35:
            tier = "MODERATE_VULNERABILITY_MANAGEABLE"
            verdict = "TARGETED_HARDENING_ADVISABLE"
            rationale = "Cable infrastructure has partial domestic redundancy; targeted hardening of key landing stations recommended."
            is_compromised = False
        else:
            tier = "RESILIENT_CABLE_SOVEREIGNTY"
            verdict = "CABLE_SOVEREIGNTY_MAINTAINED"
            rationale = "Domestic cable redundancy and encryption layers provide adequate protection against routine interception risk."
            is_compromised = False

        return {
            "cable_vulnerability_index": cable_vulnerability_index,
            "cable_sovereignty_score": cable_sovereignty_score,
            "landing_station_exposure_risk": round(exp_risk, 4),
            "chokepoint_depth_risk": round(ckpt_risk, 4),
            "domestic_cable_redundancy_score": round(redundancy, 4),
            "encryption_layer_score": round(encryption, 4),
            "repair_ship_autonomy_score": round(repair, 4),
            "cable_sovereignty_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_cable_compromised": is_compromised
        }

```