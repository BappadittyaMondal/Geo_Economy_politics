# LENS SPECIFICATION: DEMOGRAPHIC_INFILTRATION

```python
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

        # Phase 232: Wire StatutoryBorderDemographySieve
        _bd_result = StatutoryBorderDemographySieve.calculate_border_demography(
            voter_roll_cleansing_rigor=metrics.get("voter_roll_cleansing_rigor", 0.75),
            biometric_deduplication_rate=metrics.get("biometric_deduplication_rate", 0.80),
            cross_border_infiltration_flow=metrics.get("cross_border_infiltration_flow", 0.30),
            lawfare_injunction_friction=metrics.get("lawfare_injunction_friction", 0.25),
        )
        metrics.update(_bd_result)

        # Phase 305: Wire TheologicalIncompatibilityApostasySieve
        demo_meta = getattr(event, "metadata", {}) or {}
        theol_params = demo_meta.get("theological_apostasy", {}) if isinstance(demo_meta, dict) else {}
        _theol_res = TheologicalIncompatibilityApostasySieve.calculate(
            ex_muslim_apostasy_velocity=theol_params.get("ex_muslim_apostasy_velocity", 0.70),
            scriptural_demystification_rate=theol_params.get("scriptural_demystification_rate", 0.75),
            dogmatic_indoctrination_pressure=theol_params.get("dogmatic_indoctrination_pressure", 0.30),
            syncretic_illusion_drag=theol_params.get("syncretic_illusion_drag", 0.25),
            grassroots_ex_muslim_reach=theol_params.get("grassroots_ex_muslim_reach", 0.65),
        )
        metrics["theological_realism_score"] = _theol_res["theological_realism_score"]
        metrics["theological_realism_tier"] = _theol_res["theological_realism_tier"]
        metrics["counter_radicalization_index"] = _theol_res["counter_radicalization_index"]

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=0.88,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics,
            evidence_status="sufficient"
        )



class StatutoryBorderDemographySieve:
    """
    Phase 232: Evaluates demographic sovereignty and border frontier security along sensitive border corridors
    (e.g., Eastern border, Siliguri corridor) by analyzing voter roll cleansing rigor, biometric deduplication,
    cross-border illegal infiltration flows, and judicial lawfare injunctions against deportation.
    """

    @classmethod
    def calculate_border_demography(
        cls,
        voter_roll_cleansing_rigor: float = 0.75,
        biometric_deduplication_rate: float = 0.80,
        cross_border_infiltration_flow: float = 0.30,
        lawfare_injunction_friction: float = 0.25,
    ) -> Dict[str, Any]:
        """
        Calculates demographic sovereignty score using logistic sigmoid model.
        """
        import math
        v_clean = max(0.0, min(1.0, float(voter_roll_cleansing_rigor)))
        b_dedup = max(0.0, min(1.0, float(biometric_deduplication_rate)))
        c_flow = max(0.0, min(1.0, float(cross_border_infiltration_flow)))
        l_inj = max(0.0, min(1.0, float(lawfare_injunction_friction)))

        z = 2.8 * v_clean + 2.4 * b_dedup - 3.2 * c_flow - 1.6 * l_inj - 0.2
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.80:
            tier = "FORTIFIED_DEMOGRAPHIC_SOVEREIGNTY"
            verdict = "BORDER_FRONTIER_STABILIZED_STATUTORY_CONTROL"
            rationale = (
                f"Fortified sovereignty ({score:.4f}): Rigorous voter roll cleansing ({v_clean:.2f}) and biometric deduplication "
                f"({b_dedup:.2f}) effectively neutralize infiltration risks."
            )
        elif score >= 0.60:
            tier = "CONTAINED_BORDER_INFILTRATION"
            verdict = "ACTIVE_BIOMETRIC_SCRUTINY_BORDER_FENCING"
            rationale = (
                f"Contained infiltration ({score:.4f}): Active biometric screening maintains acceptable demographic stability."
            )
        elif score >= 0.40:
            tier = "VULNERABLE_DEMOGRAPHIC_CHOKEPOINT"
            verdict = "CHICKENS_NECK_SILIGURI_CORRIDOR_PRESSURE"
            rationale = (
                f"Demographic chokepoint vulnerability ({score:.4f}): Infiltration flows ({c_flow:.2f}) or lawfare injunctions "
                f"({l_inj:.2f}) straining local administrative control."
            )
        else:
            tier = "ACUTE_DEMOGRAPHIC_SOVEREIGNTY_EROSION"
            verdict = "CRITICAL_ARTICLE_355_INTERVENTION_MANDATED"
            rationale = (
                f"Acute demographic erosion ({score:.4f}): Severe cross-border infiltration threatening constitutional order. "
                f"Immediate federal intervention under Article 355 required."
            )

        return {
            "demographic_sovereignty_score": score,
            "voter_roll_cleansing_rigor": round(v_clean, 4),
            "biometric_deduplication_rate": round(b_dedup, 4),
            "cross_border_infiltration_flow": round(c_flow, 4),
            "lawfare_injunction_friction": round(l_inj, 4),
            "demographic_sovereignty_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_demographic_sovereignty_secure": score >= 0.60
        }


class TheologicalIncompatibilityApostasySieve:
    """
    Phase 305: Models the theological exclusivity of literalist scripture vs syncretic political
    constructs, tracking the velocity of the grassroots ex-Muslim apostasy movement (Irtidad)
    as an organic internal counter-radicalization indicator.
    
    Mathematical Formulation:
      z = 2.8 * ex_muslim_apostasy_velocity + 2.6 * scriptural_demystification_rate
          - 3.2 * dogmatic_indoctrination_pressure - 1.8 * syncretic_illusion_drag - 0.3
      S_Theological_Realism = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        ex_muslim_apostasy_velocity: float = 0.70,
        scriptural_demystification_rate: float = 0.75,
        dogmatic_indoctrination_pressure: float = 0.30,
        syncretic_illusion_drag: float = 0.25,
        grassroots_ex_muslim_reach: float = 0.65,
    ) -> Dict[str, Any]:
        import math
        apostasy = max(0.0, min(1.0, float(ex_muslim_apostasy_velocity)))
        demyst = max(0.0, min(1.0, float(scriptural_demystification_rate)))
        indoctrination = max(0.0, min(1.0, float(dogmatic_indoctrination_pressure)))
        syncretic = max(0.0, min(1.0, float(syncretic_illusion_drag)))
        reach = max(0.0, min(1.0, float(grassroots_ex_muslim_reach)))

        z = 2.8 * apostasy + 2.6 * demyst - 3.2 * indoctrination - 1.8 * syncretic - 0.3
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "HIGH_THEOLOGICAL_CLARITY_AND_REFORM"
            verdict = "ORGANIC_INTERNAL_ENLIGHTENMENT_EXPANDING"
            rationale = (
                f"High theological clarity ({score:.4f}): Rapid growth in ex-Muslim apostasy velocity ({apostasy:.2f}) "
                f"and open scriptural demystification ({demyst:.2f}) decisively challenge literalist dogmatic hegemony ({indoctrination:.2f})."
            )
        elif score >= 0.55:
            tier = "ORGANIC_APOSTASY_COUNTER_RADICALIZATION"
            verdict = "ACTIVE_GRASSROOTS_SECULAR_DISSENT"
            rationale = (
                f"Organic counter-radicalization ({score:.4f}): Emerging digital platforms ({reach:.2f}) foster internal debate, "
                f"gradually eroding dogmatic enforcement despite political syncretic myths ({syncretic:.2f})."
            )
        elif score >= 0.35:
            tier = "CONTESTED_SYNCRETIC_ILLUSION_DRAG"
            verdict = "ELEVATED_DOGMATIC_RESISTANCE_TO_REFORM"
            rationale = (
                f"Contested theological reform ({score:.4f}): Dogmatic institutions actively suppress apostates while "
                f"superficial syncretic narratives delay critical structural understanding."
            )
        else:
            tier = "ACUTE_DOGMATIC_RADICALIZATION_TRAP"
            verdict = "TOTAL_THEOLOGICAL_EXCLUSION_AND_CENSORSHIP"
            rationale = (
                f"Acute dogmatic entrapment ({score:.4f}): Pervasive blasphemy fears and institutional intimidation completely "
                f"silence dissent, entrenching theological exclusivity and social tension."
            )

        counter_radicalization_idx = round(min(1.0, (score * 0.60) + (reach * 0.40)), 4)

        return {
            "theological_realism_score": score,
            "ex_muslim_apostasy_velocity": round(apostasy, 4),
            "scriptural_demystification_rate": round(demyst, 4),
            "dogmatic_indoctrination_pressure": round(indoctrination, 4),
            "syncretic_illusion_drag": round(syncretic, 4),
            "grassroots_ex_muslim_reach": round(reach, 4),
            "counter_radicalization_index": counter_radicalization_idx,
            "theological_realism_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_theological_reform_active": score >= 0.55,
        }


```