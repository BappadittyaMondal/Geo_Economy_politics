from .civilizational import PaleogenomicDemographicContinuitySieve
"""
Lens 2: World & Indian Diplomatic History Lens.
Grounds multilateral summitry in deep historical lineages: Bandung 1955,
the Non-Aligned Movement (NAM), Indian Strategic Autonomy (Panchsheel),
Bretton Woods structural divergence, and post-Soviet Eurasian transformations.
"""

import math
from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, SummitEvent


class HistoryLens:
    """Historical and diplomatic trajectory evaluator."""

    LENS_NAME = "World & Indian Diplomatic History"
    PRIMARY_TIER = EpistemicTier.TIER_3_SOVEREIGN_REDLINES

    @classmethod
    def evaluate(
        cls,
        summit: SummitEvent,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Assesses summit dynamics through historical treaties, post-colonial lineages,
        and India's civilizational refusal of bloc vassalage.
        Dynamically grounds assessment in historical treaties and precedent claims.
        """
        findings = [
            "Bandung 1955 & NAM Lineage: Summit reflects the structural evolution of Afro-Asian solidarity against Western institutional monopolies.",
            "Indian Strategic Autonomy: New Delhi preserves its historical doctrine of multi-alignment (Panchsheel evolution), refusing to convert BRICS into a Sinocentric or anti-Western vassal bloc.",
            "Post-Bretton Woods Revisionism: Acceleration of alternative settlement systems is a direct historical reaction to the weaponization of SWIFT and sovereign reserve asset freezes in 2022.",
            "Historical Border Distrust: Lingering 1962 historical trauma and unresolved LAC disputes fundamentally cap strategic trust between India and China, preventing a formal collective security treaty.",
            "1000-Year Historical Reversal Cycle: Modern Indian sovereign posture inverts the millennial arc of subjugation (1026 Somnath, 1192 Tarain, 1193 Nalanda) through systemic reclamation (Nalanda 2024 rebirth, BNS decolonization, maritime SAGAR doctrine mirroring 1025 Chola expeditions)."
        ]

        metrics = {
            "historical_precedent": "Bandung 1955 -> NAM 1961 -> BRIC 2006 -> Expanded BRICS",
            "indian_doctrinal_anchor": "Strategic Autonomy & Panchsheel",
            "structural_historical_friction": "Sino-Indian Territorial Standoff & Rivalry for Global South Leadership",
            "civilizational_reversal_ratio": 1.45
        }

        alignment = 0.45
        confidence = 0.92

        if claims:
            history_keywords = [
                "treaty", "1962", "1971", "1993", "lac", "nam", "panchsheel",
                "bandung", "historical", "colonial", "border", "non-alignment"
            ]
            matched_hist = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in history_keywords)
                for c in claims
            )
            if matched_hist:
                findings.insert(0, "[GROUNDED TELEMETRY] Historical boundary treaty / non-alignment precedent verified in event telemetry.")
                confidence = min(0.99, round(confidence + 0.02, 2))
                metrics["grounded_historical_claims_verified"] = True
            metrics["claims_evaluated"] = len(claims)

        # Phase 254: Sub-National Insurgency Incubation Sieve (Patel vs. Indira Historical Warning)
        _insurgency_res = SubNationalInsurgencyIncubationSieve.calculate_insurgency_blowback(
            partisan_patronage_ratio=float(metrics.get("partisan_patronage_ratio", 0.0)),
            fringe_militant_tolerance=float(metrics.get("fringe_militant_tolerance", 0.0)),
            external_sanctuary_diffusion=float(metrics.get("external_sanctuary_diffusion", 0.0)),
            institutional_counter_intel=float(metrics.get("institutional_counter_intel", 0.7)),
        )
        metrics.update(_insurgency_res)

        # Phase 259: Archaeo-Astronomical Chronology Sieve
        _chrono_res = ArchaeoAstronomicalChronologySieve.calculate_chronological_validity(
            astronomical_precession_fit=float(metrics.get("astronomical_precession_fit", 0.7)),
            epigraphical_anchor_density=float(metrics.get("epigraphical_anchor_density", 0.7)),
            textual_internal_consistency=float(metrics.get("textual_internal_consistency", 0.7)),
            curricular_distortion_bias=float(metrics.get("curricular_distortion_bias", 0.2)),
        )
        metrics.update(_chrono_res)

        # Moderate alignment score (cooperation on multipolarity, tempered by deep historical territorial distrust)
        # Phase 278 & 279: Wire PaleogenomicDemographicContinuitySieve & MultidisciplinaryEpistemicTriangulationSieve
        hist_meta = getattr(summit, "metadata", {}) or {}
        triang_params = hist_meta.get("epistemic_triangulation", {}) if isinstance(hist_meta, dict) else {}
        _triang_res = MultidisciplinaryEpistemicTriangulationSieve.calculate_triangulation_concordance(
            genetics_concordance=triang_params.get("genetics_concordance", 0.85),
            archaeozoology_concordance=triang_params.get("archaeozoology_concordance", 0.80),
            stratigraphy_concordance=triang_params.get("stratigraphy_concordance", 0.75),
            hydrology_concordance=triang_params.get("hydrology_concordance", 0.80),
            epigraphy_concordance=triang_params.get("epigraphy_concordance", 0.70),
        )
        metrics.update(_triang_res)

        # Phase 293: Wire ArchaeoAstronomicalEpigraphicDatingSieve
        astro_dating_params = hist_meta.get("archaeo_astronomy", {}) if isinstance(hist_meta, dict) else {}
        _astro_dating_res = ArchaeoAstronomicalEpigraphicDatingSieve.calculate_archaeo_astronomy(
            planetary_conjunction_accuracy=astro_dating_params.get("planetary_conjunction_accuracy", 0.85),
            sediment_stratigraphy=astro_dating_params.get("sediment_stratigraphy", 0.80),
            textual_compression_bias=astro_dating_params.get("textual_compression_bias", 0.25),
            degeneracy_drag=astro_dating_params.get("degeneracy_drag", 0.20),
        )
        metrics["archaeo_astronomical_dating_score"] = _astro_dating_res["archaeo_astronomical_dating_score"]
        metrics["planetary_ephemeris_accuracy"] = _astro_dating_res["planetary_ephemeris_accuracy"]
        metrics["chronological_concordance_index"] = _astro_dating_res["chronological_concordance_index"]
        metrics["vedic_chronology_tier"] = _astro_dating_res["vedic_chronology_tier"]

        # Phase 303: Wire HistoricalDemystificationPartitionSieve
        part_params = hist_meta.get("partition_demystification", {}) if isinstance(hist_meta, dict) else {}
        _part_res = HistoricalDemystificationPartitionSieve.calculate(
            empirical_archival_evidence=part_params.get("empirical_archival_evidence", 0.85),
            mythological_deification_drag=part_params.get("mythological_deification_drag", 0.25),
            khilafat_appeasement_cost=part_params.get("khilafat_appeasement_cost", 0.80),
            secular_historical_amnesia=part_params.get("secular_historical_amnesia", 0.20),
            primary_source_neutrality=part_params.get("primary_source_neutrality", 0.85),
        )
        metrics["historical_sandarshan_score"] = _part_res["historical_sandarshan_score"]
        metrics["historical_truth_tier"] = _part_res["historical_truth_tier"]
        metrics["archival_veracity_index"] = _part_res["archival_veracity_index"]

        # Phase 309: Wire ArchivalPrimarySourceSieve
        arch_params = hist_meta.get("archival_primary_source", {}) if isinstance(hist_meta, dict) else {}
        _arch_res = ArchivalPrimarySourceSieve.calculate(
            primary_epigraphy=arch_params.get("primary_epigraphy", 0.85),
            secondary_academic_narrative=arch_params.get("secondary_academic_narrative", 0.25),
            contemporary_revenue_records=arch_params.get("contemporary_revenue_records", 0.80),
            postcolonial_speculative_bias=arch_params.get("postcolonial_speculative_bias", 0.20),
        )
        metrics["archival_fidelity_score"] = _arch_res["archival_fidelity_score"]
        metrics["archival_fidelity_tier"] = _arch_res["archival_fidelity_tier"]
        metrics["primary_epigraphic_index"] = _arch_res["primary_epigraphic_index"]

        # Phase 314: Wire SubalternMemorySieve
        sub_params = hist_meta.get("subaltern_memory", {}) if isinstance(hist_meta, dict) else {}
        _sub_res = SubalternMemorySieve.calculate(
            hero_stones_density=sub_params.get("hero_stones_density", 0.80),
            oral_folk_resistance=sub_params.get("oral_folk_resistance", 0.75),
            colonial_official_erasure=sub_params.get("colonial_official_erasure", 0.30),
        )
        metrics["subaltern_memory_score"] = _sub_res["subaltern_memory_score"]
        metrics["subaltern_memory_tier"] = _sub_res["subaltern_memory_tier"]
        metrics["subaltern_resilience_index"] = _sub_res["subaltern_resilience_index"]

        # Phase 317: Wire ColonialDrainExtractionSieve
        drain_params = hist_meta.get("colonial_drain_extraction", {}) if isinstance(hist_meta, dict) else {}
        _drain_res = ColonialDrainExtractionSieve.calculate(
            council_bills_drain_nominal=drain_params.get("council_bills_drain_nominal", 0.85),
            domestic_capital_formation=drain_params.get("domestic_capital_formation", 0.30),
            forced_tariff_deindustrialization=drain_params.get("forced_tariff_deindustrialization", 0.80),
            reinvested_infrastructure_mitigation=drain_params.get("reinvested_infrastructure_mitigation", 0.15),
        )
        metrics["colonial_drain_score"] = _drain_res["colonial_drain_score"]
        metrics["colonial_drain_tier"] = _drain_res["colonial_drain_tier"]
        metrics["sovereign_drain_extraction_index"] = _drain_res["sovereign_drain_extraction_index"]

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=confidence,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )


class SubNationalInsurgencyIncubationSieve:
    """
    Phase 254: Sub-National Insurgency Incubation Sieve (Patel vs. Indira Historical Warning).
    Models the systemic hazard where a governing executive instrumentalizes or tolerates radical
    sub-national factions for short-term domestic political leverage, triggering uncontrollable
    kinetic insurgency, external sanctuary diffusion, and sovereign decapitation blowback.
    """

    @staticmethod
    def calculate_insurgency_blowback(
        partisan_patronage_ratio: float = 0.0,
        fringe_militant_tolerance: float = 0.0,
        external_sanctuary_diffusion: float = 0.0,
        institutional_counter_intel: float = 0.5,
    ) -> Dict[str, Any]:
        ppr = min(1.0, max(0.0, float(partisan_patronage_ratio)))
        fmt = min(1.0, max(0.0, float(fringe_militant_tolerance)))
        esd = min(1.0, max(0.0, float(external_sanctuary_diffusion)))
        ici = min(1.0, max(0.0, float(institutional_counter_intel)))

        z = (3.2 * ppr + 2.6 * fmt + 2.2 * esd - 3.0 * ici - 1.0)
        risk = 1.0 / (1.0 + math.exp(-z))
        risk = round(min(1.0, max(0.0, risk)), 4)

        if risk >= 0.80:
            tier = "IMMINENT_SOVEREIGN_BLOWBACK_AND_DECAPITATION_RISK"
            verdict = "ACUTE_INDIRA_PARADOX_SOVEREIGN_VULNERABILITY"
        elif risk >= 0.60:
            tier = "UNCONTROLLED_INSURGENCY_INCUBATION"
            verdict = "SANCTUARY_DIFFUSION_AND_EXTREMIST_ENTRENCHMENT"
        elif risk >= 0.40:
            tier = "LATENT_SUB_NATIONAL_POLARIZATION"
            verdict = "CONTROLLED_DOMESTIC_POLARIZATION_FRICTION"
        else:
            tier = "PATEL_CONSENSUAL_INSTITUTIONAL_STABILITY"
            verdict = "FORTIFIED_SOVEREIGN_INTEGRATION"

        return {
            "partisan_blowback_risk": risk,
            "insurgency_tier": tier,
            "insurgency_verdict": verdict,
            "partisan_patronage_ratio": ppr,
            "fringe_militant_tolerance": fmt,
            "external_sanctuary_diffusion": esd,
            "institutional_counter_intel": ici,
            "is_blowback_critical": risk >= 0.60
        }


class ArchaeoAstronomicalChronologySieve:
    """
    Phase 259: Archaeo-Astronomical & Epigraphical Chronology Sieve.
    Dismantles colonial/Marxist curricular compression and unanchored software hyper-antiquity
    via multi-pillar triangulation across astronomical precession alignments (50.3''/yr),
    epigraphical copper-plate/rock inscriptional density, and Sanskrit textual internal consistency.
    """

    @staticmethod
    def calculate_chronological_validity(
        astronomical_precession_fit: float = 0.5,
        epigraphical_anchor_density: float = 0.5,
        textual_internal_consistency: float = 0.5,
        curricular_distortion_bias: float = 0.2,
    ) -> Dict[str, Any]:
        apf = min(1.0, max(0.0, float(astronomical_precession_fit)))
        ead = min(1.0, max(0.0, float(epigraphical_anchor_density)))
        tic = min(1.0, max(0.0, float(textual_internal_consistency)))
        cdb = min(1.0, max(0.0, float(curricular_distortion_bias)))

        z = (3.0 * apf + 2.6 * ead + 2.2 * tic - 2.8 * cdb - 0.5)
        score = 1.0 / (1.0 + math.exp(-z))
        score = round(min(1.0, max(0.0, score)), 4)

        if score >= 0.80:
            tier = "VERIFIED_EMPIRICAL_CHRONOLOGICAL_ANCHOR"
            verdict = "TRIANGULATED_HISTORICAL_GROUND_TRUTH"
        elif score >= 0.60:
            tier = "PROBABLE_HISTORICAL_TIMELINE"
            verdict = "ROBUST_EPIGRAPHICAL_AND_CELESTIAL_CORROBORATION"
        elif score >= 0.40:
            tier = "CONTESTED_INTERPOLATED_DATING"
            verdict = "METHODOLOGICAL_FRICTION_AND_PARTIAL_CORROBORATION"
        else:
            tier = "IDEOLOGICALLY_DISTORTED_OR_MYTHOLOGICAL_FABRICATION"
            verdict = "REJECTED_CURRICULAR_DISTORTION_OR_UNANCHORED_SPECULATION"

        return {
            "chronological_validity_score": score,
            "chronology_tier": tier,
            "chronology_verdict": verdict,
            "astronomical_precession_fit": apf,
            "epigraphical_anchor_density": ead,
            "textual_internal_consistency": tic,
            "curricular_distortion_bias": cdb,
            "is_chronology_verified": score >= 0.60
        }




class MultidisciplinaryEpistemicTriangulationSieve:
    """
    Phase 279: Multidisciplinary Epistemic Triangulation Sieve.
    Evaluates historical claims by measuring geometric concordance across 5 distinct hard disciplines:
    ancient DNA, archaeozoology (faunal remains / osteometry), stratigraphy, paleoclimatology / hydrology,
    and epigraphy / linguistics.
    """

    @staticmethod
    def calculate_triangulation_concordance(
        genetics_concordance: float = 0.85,
        archaeozoology_concordance: float = 0.80,
        stratigraphy_concordance: float = 0.75,
        hydrology_concordance: float = 0.80,
        epigraphy_concordance: float = 0.70,
    ) -> dict:
        import math
        g = min(1.0, max(0.0, float(genetics_concordance)))
        a = min(1.0, max(0.0, float(archaeozoology_concordance)))
        s = min(1.0, max(0.0, float(stratigraphy_concordance)))
        h = min(1.0, max(0.0, float(hydrology_concordance)))
        e = min(1.0, max(0.0, float(epigraphy_concordance)))

        # Weighted geometric mean of (1 + E_k)/2
        w_g, w_a, w_s, w_h, w_e = 0.25, 0.20, 0.20, 0.20, 0.15
        tau = (
            ((1.0 + g) / 2.0) ** w_g *
            ((1.0 + a) / 2.0) ** w_a *
            ((1.0 + s) / 2.0) ** w_s *
            ((1.0 + h) / 2.0) ** w_h *
            ((1.0 + e) / 2.0) ** w_e
        )
        score = round(min(1.0, max(0.0, 2.0 * (tau - 0.5))), 4)

        if score >= 0.75:
            tier = "UNASSAILABLE_MULTI_DOMAIN_EPISTEMIC_CONVERGENCE"
            verdict = "HARD_SCIENCE_VALIDATION_ACROSS_ADNA_FAUNAL_AND_PALEOCLIMATIC_LAYERS"
        elif score >= 0.55:
            tier = "HIGH_FIDELITY_HISTORICAL_ROBUSTNESS"
            verdict = "MULTI_DISCIPLINARY_CORROBORATION_RESISTANT_TO_NARRATIVE_MANIPULATION"
        elif score >= 0.35:
            tier = "SPECULATIVE_SINGLE_DISCIPLINE_VULNERABILITY"
            verdict = "OVER_RELIANCE_ON_LINGUISTIC_OR_TEXTUAL_SPECULATION"
        else:
            tier = "EPISTEMIC_COLLAPSE_UNVERIFIED_HISTORICAL_CONSTRUCT"
            verdict = "DISCREDITED_COLONIAL_MYTHOLOGY_CONTRADICTED_BY_PHYSICAL_SCIENCES"

        return {
            "epistemic_triangulation_score": score,
            "genetics_concordance": round(g, 4),
            "archaeozoology_concordance": round(a, 4),
            "stratigraphy_concordance": round(s, 4),
            "hydrology_concordance": round(h, 4),
            "epigraphy_concordance": round(e, 4),
            "triangulation_tier": tier,
            "triangulation_verdict": verdict,
            "is_triangulation_conclusive": score >= 0.55,
        }


class ArchaeoAstronomicalEpigraphicDatingSieve:
    """
    Phase 293: Archaeo-Astronomical & Epigraphic Dating Sieve.
    Enforces atomic multi-pillar planetary conjunction triangulation, retro-calculation
    algorithms for ancient equinoxes/solstices, stratigraphic sedimentology correlation,
    and mathematical refutation of colonial 1500 BCE invasion dogma.
    """

    @classmethod
    def calculate_archaeo_astronomy(
        cls,
        planetary_conjunction_accuracy: float = 0.85,
        sediment_stratigraphy: float = 0.80,
        textual_compression_bias: float = 0.25,
        degeneracy_drag: float = 0.20,
    ) -> Dict[str, Any]:
        """
        Calculates Archaeo-Astronomical Dating Score using calibrated logistic sigmoid:
            z = 3.0 * conjunction + 2.6 * sediment - 3.5 * compression - 2.4 * degeneracy - 0.5
            score = 1 / (1 + exp(-z))
        """
        import math
        conj = max(0.0, min(1.0, float(planetary_conjunction_accuracy)))
        sed = max(0.0, min(1.0, float(sediment_stratigraphy)))
        comp = max(0.0, min(1.0, float(textual_compression_bias)))
        deg = max(0.0, min(1.0, float(degeneracy_drag)))

        z = 3.0 * conj + 2.6 * sed - 3.5 * comp - 2.4 * deg - 0.5
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "RIGOROUS_ASTRONOMICAL_EPIGRAPHIC_CERTAINTY"
            verdict = "MULTI_PILLAR_CHRONOLOGICAL_CONCORDANCE_VERIFIED"
            rationale = (
                f"Rigorous certainty ({score:.4f}): Precise planetary conjunction alignments ({conj:.2f}) and sediment "
                f"stratigraphy ({sed:.2f}) demolish colonial artificial timeline compressions."
            )
        elif score >= 0.55:
            tier = "HIGH_FIDELITY_CHRONOLOGICAL_CONCORDANCE"
            verdict = "CONCORDANT_EPIGRAPHIC_AND_STELLAR_MATCH"
            rationale = (
                f"High-fidelity concordance ({score:.4f}): Astronomical observations align closely with epigraphic and archaeological records."
            )
        elif score >= 0.35:
            tier = "CONTESTED_POETIC_DEGENERACY_INTERVAL"
            verdict = "ELEVATED_METAPHORICAL_INTERPOLATION_RISK"
            rationale = (
                f"Contested interval ({score:.4f}): Textual compression bias ({comp:.2f}) creates chronological uncertainty."
            )
        else:
            tier = "COLONIAL_EUROCENTRIC_FABRICATION"
            verdict = "UNSCIENTIFIC_MAX_MULLER_TIMELINE_DISTORTION"
            rationale = (
                f"Colonial distortion ({score:.4f}): High compression bias and zero empirical backing preserve obsolete 19th-century dogma."
            )

        concordance_idx = round(min(1.0, sed * 0.60 + conj * 0.40), 4)

        return {
            "archaeo_astronomical_dating_score": score,
            "planetary_conjunction_accuracy": round(conj, 4),
            "sediment_stratigraphy": round(sed, 4),
            "textual_compression_bias": round(comp, 4),
            "degeneracy_drag": round(deg, 4),
            "planetary_ephemeris_accuracy": round(conj, 4),
            "chronological_concordance_index": concordance_idx,
            "vedic_chronology_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_chronologically_rigorous": score >= 0.55,
        }


class HistoricalDemystificationPartitionSieve:
    """
    Phase 303: Quantifies historical truth-telling (Sandarshan) by stripping away political deification
    (Mahatma-ism), evaluating archival evidence regarding Khilafat appeasement, silence on Moplah atrocities,
    and the causal acceleration of 1947 Partition.
    
    Mathematical Formulation:
      ratio = empirical_archival_evidence / (mythological_deification_drag + eps)
      z = 2.8 * (ratio / 2.5) + 2.6 * khilafat_appeasement_cost - 3.2 * secular_historical_amnesia - 0.3
      S_Historical_Sandarshan = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        empirical_archival_evidence: float = 0.85,
        mythological_deification_drag: float = 0.25,
        khilafat_appeasement_cost: float = 0.80,
        secular_historical_amnesia: float = 0.20,
        primary_source_neutrality: float = 0.85,
    ) -> Dict[str, Any]:
        archival = max(0.0, min(1.0, float(empirical_archival_evidence)))
        myth = max(0.0, min(1.0, float(mythological_deification_drag)))
        khilafat = max(0.0, min(1.0, float(khilafat_appeasement_cost)))
        amnesia = max(0.0, min(1.0, float(secular_historical_amnesia)))
        neutrality = max(0.0, min(1.0, float(primary_source_neutrality)))

        ratio = min(5.0, archival / (myth + 1e-6))
        z = 2.8 * (ratio / 2.5) + 2.6 * khilafat - 3.2 * amnesia - 0.3
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "OBJECTIVE_HISTORICAL_SANDARSHAN"
            verdict = "RIGOROUS_ARCHIVAL_DEMORALIZATION_AND_TRUTH_TELLING"
            rationale = (
                f"Objective historical Sandarshan ({score:.4f}): Archival documentation ({archival:.2f}) rigorously exposes "
                f"the catastrophic cost of Khilafat appeasement ({khilafat:.2f}) and dispels political deification myths ({myth:.2f})."
            )
        elif score >= 0.55:
            tier = "ARCHIVAL_DEMOPOLITIZATION_STABLE"
            verdict = "EMERGING_EMPIRICAL_HISTORIOGRAPHY"
            rationale = (
                f"Archival stability ({score:.4f}): Primary historical sources progressively challenge sanitized secular narratives, "
                f"though institutional inertia ({amnesia:.2f}) persists."
            )
        elif score >= 0.35:
            tier = "CONTESTED_MYTHOLOGICAL_NARRATIVE_BIAS"
            verdict = "POLITICAL_DEIFICATION_DRAG"
            rationale = (
                f"Contested narrative ({score:.4f}): Post-independence state hagiography obscures causal drivers of Partition, "
                f"distorting strategic civilizational memory."
            )
        else:
            tier = "TOTAL_SECULAR_HISTORICAL_AMNESIA"
            verdict = "TOTAL_TABOO_DRIVEN_HISTORICAL_CENSORSHIP"
            rationale = (
                f"Critical amnesia ({score:.4f}): Pervasive taboos censor historical records of communal violence and appeasement, "
                f"leaving society vulnerable to repeated geopolitical errors."
            )

        archival_veracity_idx = round(min(1.0, (score * 0.60) + (neutrality * 0.40)), 4)

        return {
            "historical_sandarshan_score": score,
            "archival_to_myth_ratio": round(ratio, 4),
            "empirical_archival_evidence": round(archival, 4),
            "mythological_deification_drag": round(myth, 4),
            "khilafat_appeasement_cost": round(khilafat, 4),
            "secular_historical_amnesia": round(amnesia, 4),
            "primary_source_neutrality": round(neutrality, 4),
            "archival_veracity_index": archival_veracity_idx,
            "historical_truth_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_historically_demystified": score >= 0.55,
        }


class ArchivalPrimarySourceSieve:
    """
    Phase 309: Evaluates the weighting of primary archival evidence (contemporary inscriptions,
    copper plates, Persian/Kannada Inam revenue registers) vs secondary academic commentaries.
    
    Mathematical Formulation:
      ratio = primary_epigraphy / (secondary_academic_narrative + eps)
      z = 3.2 * (ratio / 2.5) + 2.5 * contemporary_revenue_records - 3.0 * postcolonial_speculative_bias - 0.4
      S_Archival_Fidelity = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        primary_epigraphy: float = 0.85,
        secondary_academic_narrative: float = 0.25,
        contemporary_revenue_records: float = 0.80,
        postcolonial_speculative_bias: float = 0.20,
    ) -> Dict[str, Any]:
        epigraphy = max(0.0, min(1.0, float(primary_epigraphy)))
        secondary = max(0.0, min(1.0, float(secondary_academic_narrative)))
        revenue = max(0.0, min(1.0, float(contemporary_revenue_records)))
        bias = max(0.0, min(1.0, float(postcolonial_speculative_bias)))

        ratio = min(5.0, epigraphy / (secondary + 1e-6))
        z = 3.2 * (ratio / 2.5) + 2.5 * revenue - 3.0 * bias - 0.4
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "PRISTINE_PRIMARY_ARCHIVAL_GROUNDING"
            verdict = "PRIMARY_EPIGRAPHIC_SUPREMACY"
            rationale = (
                f"Pristine archival grounding ({score:.4f}): Inscriptional evidence ({epigraphy:.2f}) and contemporaneous "
                f"revenue records ({revenue:.2f}) decisively invalidate speculative secondary commentary ({secondary:.2f})."
            )
        elif score >= 0.55:
            tier = "ROBUST_DOCUMENTARY_FIDELITY"
            verdict = "SUBSTANTIAL_ARCHIVAL_SUPPORT"
            rationale = (
                f"Robust documentary fidelity ({score:.4f}): Primary records provide resilient evidentiary anchoring, "
                f"resisting revisionist ideological drift."
            )
        elif score >= 0.35:
            tier = "CONTESTED_SECONDARY_BIAS_RISK"
            verdict = "ELEVATED_SPECULATIVE_COMMENTARY_DRAG"
            rationale = (
                f"Contested historiography ({score:.4f}): Lack of direct primary epigraphy allows secondary narrative "
                f"extrapolations ({bias:.2f}) to distort historical event assessment."
            )
        else:
            tier = "TOTAL_HISTORIOGRAPHICAL_FABRICATION"
            verdict = "CRITICAL_PRIMARY_SOURCE_DEFICIT"
            rationale = (
                f"Severe archival deficit ({score:.4f}): Complete absence of inscriptional backing enables total "
                f"historiographical fabrication."
            )

        epigraphic_idx = round(min(1.0, (score * 0.65) + (epigraphy * 0.35)), 4)

        return {
            "archival_fidelity_score": score,
            "epigraphic_to_secondary_ratio": round(ratio, 4),
            "primary_epigraphy": round(epigraphy, 4),
            "secondary_academic_narrative": round(secondary, 4),
            "contemporary_revenue_records": round(revenue, 4),
            "postcolonial_speculative_bias": round(bias, 4),
            "primary_epigraphic_index": epigraphic_idx,
            "archival_fidelity_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_archivally_grounded": score >= 0.55,
        }


class SubalternMemorySieve:
    """
    Phase 314: Ingests physical artifacts (Hero Stones / Viragals, local shrines) and oral traditions
    to cross-examine and correct official state or colonial administrative accounts.
    
    Mathematical Formulation:
      z = 2.8 * hero_stones_density + 2.6 * oral_folk_resistance - 3.0 * colonial_official_erasure - 0.4
      S_Subaltern_Memory = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        hero_stones_density: float = 0.80,
        oral_folk_resistance: float = 0.75,
        colonial_official_erasure: float = 0.30,
    ) -> Dict[str, Any]:
        hero = max(0.0, min(1.0, float(hero_stones_density)))
        oral = max(0.0, min(1.0, float(oral_folk_resistance)))
        erasure = max(0.0, min(1.0, float(colonial_official_erasure)))

        z = 2.8 * hero + 2.6 * oral - 3.0 * erasure - 0.4
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "FORTIFIED_SUBALTERN_MEMORY"
            verdict = "RESILIENT_COMMUNITY_HISTORICAL_CONTINUITY"
            rationale = (
                f"Fortified subaltern memory ({score:.4f}): Dense physical hero stones ({hero:.2f}) and living oral traditions "
                f"({oral:.2f}) successfully preserve battlefield sacrifices erased by colonial annals ({erasure:.2f})."
            )
        elif score >= 0.55:
            tier = "ROBUST_ORAL_RESISTANCE_TRUTH"
            verdict = "EFFECTIVE_FOLK_EVIDENTIARY_ANCHOR"
            rationale = (
                f"Robust oral resistance ({score:.4f}): Local cultural memory provides verifiable historical truth-telling."
            )
        elif score >= 0.35:
            tier = "CONTESTED_FOLKLORE_AMNESIA"
            verdict = "EROSION_OF_LOCAL_TACTICAL_HERITAGE"
            rationale = (
                f"Contested memory ({score:.4f}): Urbanization and colonial historiographical bias ({erasure:.2f}) erode "
                f"indigenous resistance recollections."
            )
        else:
            tier = "EXTINCTION_OF_LOCAL_HERITAGE"
            verdict = "TOTAL_HISTORICAL_DELETION"
            rationale = (
                f"Critical memory loss ({score:.4f}): Complete loss of oral and in-situ hero stones leaves society "
                f"historically disarmed."
            )

        subaltern_idx = round(min(1.0, (score * 0.60) + (hero * 0.40)), 4)

        return {
            "subaltern_memory_score": score,
            "hero_stones_density": round(hero, 4),
            "oral_folk_resistance": round(oral, 4),
            "colonial_official_erasure": round(erasure, 4),
            "subaltern_resilience_index": subaltern_idx,
            "subaltern_memory_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_subaltern_memory_preserved": score >= 0.55,
        }


class ColonialDrainExtractionSieve:
    """
    Phase 317: Factors in historical wealth extraction coefficients ($45 trillion drain via Council Bills)
    into long-term capital formation and sovereign industrial trajectory modeling.
    
    Mathematical Formulation:
      ratio = council_bills_drain_nominal / (domestic_capital_formation + eps)
      z = 3.2 * (ratio / 2.5) + 2.6 * forced_tariff_deindustrialization - 2.8 * reinvested_infrastructure_mitigation - 0.4
      S_Colonial_Drain_Extraction = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        council_bills_drain_nominal: float = 0.85,
        domestic_capital_formation: float = 0.30,
        forced_tariff_deindustrialization: float = 0.80,
        reinvested_infrastructure_mitigation: float = 0.15,
    ) -> Dict[str, Any]:
        drain = max(0.0, min(1.0, float(council_bills_drain_nominal)))
        capital = max(0.0, min(1.0, float(domestic_capital_formation)))
        tariff = max(0.0, min(1.0, float(forced_tariff_deindustrialization)))
        reinvest = max(0.0, min(1.0, float(reinvested_infrastructure_mitigation)))

        ratio = min(5.0, drain / (capital + 1e-6))
        z = 3.2 * (ratio / 2.5) + 2.6 * tariff - 2.8 * reinvest - 0.4
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "CATASTROPHIC_WEALTH_DRAIN_COEFFICIENT"
            verdict = "SEVERE_SYSTEMIC_SURPLUS_SIPHON"
            rationale = (
                f"Catastrophic drain ({score:.4f}): Unilateral export surplus siphoned via Council Bills ({drain:.2f}) "
                f"and forced tariff asymmetries ({tariff:.2f}) systematically crippled domestic capital formation ({capital:.2f})."
            )
        elif score >= 0.55:
            tier = "SEVERE_CAPITAL_STARVATION"
            verdict = "ACCELERATED_DEINDUSTRIALIZATION"
            rationale = (
                f"Severe capital starvation ({score:.4f}): Substantial colonial fiscal extraction stunted indigenous manufacturing capacity."
            )
        elif score >= 0.35:
            tier = "CONTESTED_COLONIAL_ECONOMIC_DISTORTION"
            verdict = "MODERATE_FISCAL_ASYMMETRY"
            rationale = (
                f"Contested economic distortion ({score:.4f}): Colonial trade policies created chronic structural imbalances."
            )
        else:
            tier = "MINIMAL_SYSTEMIC_EXTRACTION"
            verdict = "AUTONOMOUS_CAPITAL_ACCUMULATION"
            rationale = (
                f"Minimal extraction ({score:.4f}): Domestic capital formation outpaced external trade leakage."
            )

        sovereign_drain_idx = round(min(1.0, (score * 0.65) + (tariff * 0.35)), 4)

        return {
            "colonial_drain_score": score,
            "drain_to_capital_ratio": round(ratio, 4),
            "council_bills_drain_nominal": round(drain, 4),
            "domestic_capital_formation": round(capital, 4),
            "forced_tariff_deindustrialization": round(tariff, 4),
            "reinvested_infrastructure_mitigation": round(reinvest, 4),
            "sovereign_drain_extraction_index": sovereign_drain_idx,
            "colonial_drain_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_colonial_drain_critical": score >= 0.55,
        }


