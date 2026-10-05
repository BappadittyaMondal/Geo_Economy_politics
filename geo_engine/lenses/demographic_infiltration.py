"""
Lens 14: Demographic Infiltration & Weaponized Migration Forensics.
Deconstructs asymmetric demographic flows, coercive engineered migration,
and transit corridor exploitation across Europe (Spain/Mediterranean/Canary routes),
South Asia (Eastern border, Siliguri neck), and Latin America/US borders.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, StrategicEvent


class DiasporaBacklashSieve:
    """
    Phase 99: Diaspora Host-Nation Backlash & Vulnerability Sieve.
    Quantifies the institutional, political, and societal squeeze on expatriate communities under
    dual-flank ideological pressure: far-right nativist xenophobia + progressive caste lawfare.

    Mathematical Formulation:
      Base_Vulnerability = (
          0.40 * nativist_hate_incidents +
          0.35 * caste_lawfare_activity +
          0.25 * max(0.0, 1.0 - grassroots_advocacy_strength)
      )
      Amplifier = 1.0 + 0.20 * max(0.0, min(1.0, host_country_polarization))
      V_diaspora = min(1.0, max(0.0, round(Base_Vulnerability * Amplifier, 4)))
    """

    @classmethod
    def calculate_diaspora_vulnerability(
        cls,
        nativist_hate_incidents: float = 0.65,
        caste_lawfare_activity: float = 0.70,
        grassroots_advocacy_strength: float = 0.25,
        host_country_polarization: float = 0.80
    ) -> Dict[str, Any]:
        hate = min(1.0, max(0.0, float(nativist_hate_incidents)))
        lawfare = min(1.0, max(0.0, float(caste_lawfare_activity)))
        advocacy = min(1.0, max(0.0, float(grassroots_advocacy_strength)))
        polar = min(1.0, max(0.0, float(host_country_polarization)))

        base = (0.40 * hate) + (0.35 * lawfare) + (0.25 * max(0.0, 1.0 - advocacy))
        amplifier = 1.0 + 0.20 * polar
        v_diaspora = min(1.0, max(0.0, round(base * amplifier, 4)))

        if v_diaspora >= 0.80:
            tier = "ACUTE_HOST_NATION_BACKLASH"
            verdict = "TARGETED_PHYSICAL_AND_LEGISLATIVE_ASSAULT_UNPROTECTED_DIASPORA"
        elif v_diaspora >= 0.55:
            tier = "ELEVATED_INSTITUTIONAL_SQUEEZE"
            verdict = "DUAL_FLANK_BIPARTISAN_PRESSURE_CIVIL_RIGHTS_VULNERABLE"
        elif v_diaspora >= 0.35:
            tier = "MODERATE_COMMUNITY_FRICTION"
            verdict = "MANAGEABLE_LOCAL_FRICTION_EMERGING_LAWFARE"
        else:
            tier = "SECURE_DIASPORA_EQUILIBRIUM"
            verdict = "EFFECTIVE_LEGAL_ADVOCACY_AND_CIVILIZATIONAL_SECURITY"

        rationale = (
            f"Nativist hate ({hate:.2f}), Caste lawfare ({lawfare:.2f}), Grassroots advocacy ({advocacy:.2f}), "
            f"Host polarization ({polar:.2f}). Diaspora vulnerability V_diaspora: {v_diaspora:.4f} ({tier})."
        )

        return {
            "diaspora_vulnerability_index": v_diaspora,
            "diaspora_threat_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "nativist_hate_incidents": hate,
            "caste_lawfare_activity": lawfare,
            "grassroots_advocacy_strength": advocacy,
            "host_country_polarization": polar,
            "institutional_squeeze_active": (v_diaspora >= 0.55)
        }


class DemographicInfiltrationLens:
    """Evaluator for weaponized migration, border corridor pressure, and asymmetric demographic statecraft."""

    LENS_NAME = "Demographic Infiltration & Weaponized Migration Forensics"
    PRIMARY_TIER = EpistemicTier.TIER_1_PHYSICAL

    @classmethod
    def evaluate(
        cls,
        event: Any,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Assesses border integrity, state-sponsored demographic pressure, and transit corridor stress.
        """
        findings = [
            "Coercive Engineered Migration: State and non-state actors periodically weaponize demographic flows as asymmetric grey-zone instruments to compel diplomatic concessions, extract subsidies, or overwhelm border security infrastructure.",
            "Transit Corridor & Chokepoint Vulnerability: Concentrated maritime routes (Western Mediterranean to Andalusia, Canary Islands, Aegean, Bay of Bengal) operate with organized human trafficking cartels and NGO logistics pipelines.",
            "Schengen & Border Treaty Friction: Unregulated mass influxes trigger emergency suspension of free-movement accords, forcing interior border checks (Pyrenees, Alps, Eastern borders) and fracturing governing coalitions.",
            "Civilizational & Internal Security Nexus: Rapid unassimilated demographic arrivals exacerbate domestic polarization, lawfare controversies, and critical infrastructure security strains."
        ]

        # Default baseline metrics
        metrics: Dict[str, Any] = {
            "border_stress_index": 0.72,
            "transit_corridor_vulnerability": 0.80,
            "grey_zone_state_leverage_score": 0.65,
            "maritime_interdiction_efficiency_pct": 42.0,
            "schengen_fragmentation_probability": 0.78
        }

        alignment = -0.45  # Negative score indicates severe systemic friction/crisis

        corpus = (
            f"{getattr(event, 'summit_name', '')} {getattr(event, 'title', '')} " +
            " ".join(getattr(c, 'raw_text', getattr(c, 'asserted_fact', getattr(c, 'assertion', ''))) for c in (claims or []))
        ).lower()

        diaspora_terms = [
            "diaspora", "diaspora under siege", "sb 403", "caste lawfare",
            "texas hanuman", "statue of union", "nativist backlash", "h-1b", "h1b ban",
            "hinduphobia", "temple attack", "sugar land", "caste ordinance"
        ]
        diaspora_detected = any(t in corpus for t in diaspora_terms)
        diaspora_calc = None

        if diaspora_detected:
            hate_val = 0.80 if ("temple" in corpus or "hanuman" in corpus or "nativist" in corpus) else 0.55
            lawfare_val = 0.85 if ("sb 403" in corpus or "caste" in corpus) else 0.45
            advocacy_val = 0.20 if "unprepared" in corpus or "fragility" in corpus else 0.35
            polar_val = 0.85
            diaspora_calc = DiasporaBacklashSieve.calculate_diaspora_vulnerability(
                nativist_hate_incidents=hate_val,
                caste_lawfare_activity=lawfare_val,
                grassroots_advocacy_strength=advocacy_val,
                host_country_polarization=polar_val
            )
            findings.insert(0, (
                f"[DIASPORA HOST-NATION FORENSICS] {diaspora_calc['tactical_rationale']} "
                f"Verdict: {diaspora_calc['operational_verdict']}."
            ))
            metrics["diaspora_backlash_vulnerability_index"] = diaspora_calc["diaspora_vulnerability_index"]
            metrics["diaspora_threat_tier"] = diaspora_calc["diaspora_threat_tier"]
            metrics["caste_lawfare_active"] = ("sb 403" in corpus or "caste" in corpus)
            metrics["nativist_hate_detected"] = ("nativist" in corpus or "hanuman" in corpus or "temple" in corpus or "h-1b" in corpus)
            if diaspora_calc["institutional_squeeze_active"]:
                alignment = min(-0.65, round(alignment - 0.20, 2))

        if claims:
            spain_or_morocco = any(
                "spain" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "infiltrat" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "ceuta" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "migrant" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower()
                for c in claims
            )
            if spain_or_morocco:
                findings.insert(0, "[GROUNDED TELEMETRY] Specific demographic surge detected: Acute border pressure on Southern European/Iberian littoral. Frontex mechanisms strained; heightened risk of interior transit blockage.")
                alignment = -0.70
                metrics["border_stress_index"] = 0.91

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=0.88,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics,
            evidence_status="sufficient"
        )
