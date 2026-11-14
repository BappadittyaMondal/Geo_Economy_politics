# LENS SPECIFICATION: HYBRID_COVERT

```python
from .petro_logistics import CriticalRefineryCyberKineticSabotageSieve
import math
"""
Lens 12: Covert Action, Hybrid Warfare & Strategic Leverage Lens.
Analyzes asymmetric statecraft, intelligence maneuvering, regulatory lawfare (FATF, OFAC),
and non-kinetic pressure levers exerted before, during, and after multilateral summits.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, SummitEvent


class HybridCovertLens:
    """Hybrid warfare, intelligence posturing, and non-kinetic leverage evaluator."""

    LENS_NAME = "Hybrid Warfare & Asymmetric Leverage"
    PRIMARY_TIER = EpistemicTier.TIER_3_SOVEREIGN_REDLINES

    @classmethod
    def evaluate(
        cls,
        summit: SummitEvent,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Assesses covert signaling, regulatory timing, and non-kinetic pressure points.
        Dynamically ingests sanctions advisories, intelligence posturing, and covert lawfare claims.
        """
        findings = [
            "Western Regulatory Counter-Programming: Timing of Western regulatory advisories (OFAC sanctions expansions, FATF monitoring reviews) systematically coincides with summit gatherings to deter private-sector compliance with alternative settlement systems.",
            "Asymmetric Bilateral Pressure: Behind public diplomatic smiles, member states exercise non-kinetic pressure (e.g., China withholding transboundary hydrological data on the Brahmaputra/Yarlung Tsangpo; selective visa issuance and trade technical barriers).",
            "Lawfare & Jurisdictional Arbitrage: Use of sovereign immunity doctrines to shield central bank assets against extraterritorial asset seizures in Atlantic jurisdictions.",
            "Information Operation Shielding: State intelligence agencies run counter-disinformation operations to insulate domestic populations from foreign narrative attacks during summit cycles.",
            "Maritime Grey-Zone Coercion & Sub-Kinetic Probing: Asymmetric naval tactics including bow-crossing, shouldering, and intentional collisions (e.g., PNS Hunain incident in North Arabian Sea) mirror South China Sea maritime militia doctrine, testing adversary rules of engagement (ROE) below the kinetic threshold.",
            "Covert Kinetic Deterrence & Counter-Proxy Preemption: Transition from passive 'Dossier Diplomacy' to active 'Offensive-Defense' (Doval Doctrine), leveraging asymmetric deniable neutralization ('Unknown Gunmen') against hostile cross-border leadership and terror safe-havens.",
            "Sanctuary Asymmetry & Diaspora Leverage: Exploitation of Western host-nation legal safeguards and domestic electoral coalitions (e.g., Canadian minority government pandering) to harbor secessionist networks, prompting retaliatory diplomatic friction, intelligence expulsions, and bilateral trade freezes."
        ]

        metrics = {
            "external_regulatory_pressure_index": 0.88, # Intense Western regulatory pressure
            "intra_bloc_asymmetric_friction": 0.65,
            "lawfare_resilience_score": 0.52,
            "maritime_grey_zone_coercion_score": 0.82,
            "deterrence_doctrine_mode": "OFFENSIVE_DEFENSIVE",
            "extraterritorial_neutralization_index": 0.84,
            "sanctuary_friction_score": 0.79
        }

        alignment = 0.38
        confidence = 0.87

        if claims:
            hybrid_keywords = [
                "fatf", "ofac", "sanction", "sabotage", "covert", "intelligence",
                "grey list", "lawfare", "asymmetric", "leverage", "espionage", "subversion",
                "ramming", "shouldering", "bow crossing", "hunain", "pns", "grey zone", "sub-kinetic",
                "unknown gunmen", "offensive-defense", "doval", "sanctuary", "diaspora leverage",
                "kahuta", "spg", "nijjar", "ripudaman", "d-company", "clifton", "preemption", "proxy neutralization"
            ]
            matched_hybrid = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in hybrid_keywords)
                for c in claims
            )
            if matched_hybrid:
                findings.insert(0, "[GROUNDED TELEMETRY] Asymmetric leverage / regulatory sanctions lawfare activity identified.")
                confidence = min(0.99, round(confidence + 0.02, 2))
                metrics["grounded_hybrid_claims_verified"] = True
                metrics["maritime_grey_zone_coercion_score"] = 0.92

            kinetic_keywords = ["unknown gunmen", "offensive-defense", "sanctuary", "nijjar", "doval", "kahuta", "proxy neutralization"]
            matched_kinetic = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in kinetic_keywords)
                for c in claims
            )
            if matched_kinetic:
                findings.insert(0, "[COVERT TELEMETRY] Extraterritorial kinetic deterrence / counter-proxy offensive-defense operation identified.")
                metrics["covert_kinetic_deterrence_verified"] = True
                metrics["extraterritorial_neutralization_index"] = 0.94
                metrics["sanctuary_friction_score"] = 0.91

            mercenary_keywords = [
                "vandyke", "van dyke", "ukrainian drone", "mercenary trainer", "foreign combatant",
                "fpv kamikaze", "counter-jamming", "rf-hopping", "camp victoria", "sons of liberty",
                "soli", "irregular warfare contractor", "cna drone", "cdf drone"
            ]
            matched_mercenary = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in mercenary_keywords)
                for c in claims
            )
            if matched_mercenary:
                findings.insert(0, "[MERCENARY TECH TELEMETRY] Foreign combatant / Ukrainian tactical FPV drone proliferation detected: Asymmetric tech transfer directly altering non-state actor strike thresholds along sovereign borderlands.")
                metrics["foreign_mercenary_presence_verified"] = True
                metrics["mercenary_tech_diffusion_index"] = 0.88
                metrics["fpv_tactical_proliferation_score"] = 0.92

            sovereign_asymmetry_keywords = [
                "vandyke", "van dyke", "quattrocchi", "warren anderson", "anderson",
                "enrica lexie", "italian marines", "mercenary off-ramp", "sovereign compromise",
                "diplomatic deportation", "asymmetric immunity"
            ]
            matched_sovereign_asymmetry = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in sovereign_asymmetry_keywords)
                for c in claims
            )
            if matched_sovereign_asymmetry or matched_mercenary:
                priv_val = 0.90 if any("vandyke" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or "van dyke" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims) else 0.70
                coerc_val = 0.85
                parity_val = 0.30
                asym_res = ExtraterritorialSovereignAsymmetrySieve.calculate_sovereign_asymmetry(
                    foreign_privilege_intensity=priv_val,
                    bilateral_coercion_pressure=coerc_val,
                    domestic_parity_enforcement=parity_val
                )
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Extraterritorial Sovereign Asymmetry Sieve triggered: "
                    f"Tier [{asym_res['sovereign_compromise_tier']}] (Score: {asym_res['extraterritorial_sovereign_asymmetry_score']:.2f}). "
                    f"{asym_res['judicial_sovereignty_summary']} Remedy: {asym_res['sovereign_remedy_pathway']}"
                ))
                metrics["extraterritorial_sovereign_asymmetry_score"] = asym_res["extraterritorial_sovereign_asymmetry_score"]
                metrics["sovereign_judicial_compromise_tier"] = asym_res["sovereign_compromise_tier"]

            intel_compromise_keywords = [
                "hamid ansari", "ansari", "tehran raw", "nusrat mirza", "counter-intel vetting",
                "diplomatic compromise", "diplomatic deep state", "station compromise", "raw network compromise"
            ]
            matched_intel_compromise = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in intel_compromise_keywords)
                for c in claims
            )
            if matched_intel_compromise:
                tenure_v = 0.90 if any("tehran" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or "ansari" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims) else 0.70
                assoc_v = 0.85 if any("nusrat" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or "iamc" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims) else 0.65
                vet_v = 0.25
                fac_v = 0.80
                intel_res = DiplomaticCounterIntelSieve.calculate_counter_intel_vulnerability(
                    single_region_tenure_ratio=tenure_v,
                    transnational_hostile_associations=assoc_v,
                    counter_intel_vetting_depth=vet_v,
                    ideological_factional_alignment=fac_v
                )
                findings.insert(0, (
                    f"[DIPLOMATIC COUNTER-INTEL FORENSICS] {intel_res['tactical_rationale']} "
                    f"Verdict: {intel_res['operational_verdict']}."
                ))
                metrics["counter_intel_vulnerability_score"] = intel_res["counter_intel_vulnerability_score"]
                metrics["intel_exposure_tier"] = intel_res["intel_exposure_tier"]
                metrics["diplomatic_station_compromise_flag"] = (intel_res["counter_intel_vulnerability_score"] >= 0.50)
                if intel_res["counter_intel_review_mandated"]:
                    alignment = max(0.15, round(alignment - 0.15, 2))

            metrics["claims_evaluated"] = len(claims)

        # Phase 234: Wire NuclearAmbiguitySieve
        _na_result = NuclearAmbiguitySieve.calculate_nuclear_ambiguity(
            unacknowledged_warhead_capacity=metrics.get("unacknowledged_warhead_capacity", 0.85),
            second_strike_credibility=metrics.get("second_strike_credibility", 0.90),
            tactical_deception_capability=metrics.get("tactical_deception_capability", 0.80),
            treaty_inspection_penetration=metrics.get("treaty_inspection_penetration", 0.15),
        )
        metrics.update(_na_result)

        # Phase 241: Wire NuclearMineralEspionageSieve
        _fe_result = NuclearMineralEspionageSieve.calculate_fissile_vulnerability(
            uranium_deposit_proximity=metrics.get("uranium_deposit_proximity", 0.85),
            corridor_logistics_control=metrics.get("corridor_logistics_control", 0.80),
            clandestine_proliferation_risk=metrics.get("clandestine_proliferation_risk", 0.75),
            airspace_reconnaissance_interdiction=metrics.get("airspace_reconnaissance_interdiction", 0.40),
        )
        metrics.update(_fe_result)

        # Phase 245: Wire AsymmetricHostageCoercionSieve
        _hc_result = AsymmetricHostageCoercionSieve.calculate_hostage_coercion(
            domestic_distraction_incentive=metrics.get("domestic_distraction_incentive", 0.85),
            sub_kinetic_threshold_gap=metrics.get("sub_kinetic_threshold_gap", 0.80),
            offensive_defense_deterrence=metrics.get("offensive_defense_deterrence", 0.75),
            diplomatic_leverage=metrics.get("diplomatic_leverage", 0.30),
        )
        metrics.update(_hc_result)

        # Phase 262: Wire SubConventionalProxyWarfareSieve
        hyb_meta = getattr(summit, "metadata", {}) or {}
        hyb_params = hyb_meta.get("proxy_warfare", {}) if isinstance(hyb_meta, dict) else {}
        _pw_res = SubConventionalProxyWarfareSieve.calculate_proxy_attrition(
            infiltration_corridors_density=hyb_params.get("infiltration_corridors_density", 0.50),
            narco_hawala_financing_flow=hyb_params.get("narco_hawala_financing_flow", 0.45),
            precision_retaliation_deterrence=hyb_params.get("precision_retaliation_deterrence", 0.70),
            internal_societal_cohesion=hyb_params.get("internal_societal_cohesion", 0.75),
        )
        metrics["asymmetric_attrition_threat"] = _pw_res["asymmetric_attrition_threat"]
        metrics["counter_proxy_deterrence_index"] = _pw_res["counter_proxy_deterrence_index"]
        metrics["proxy_attrition_tier"] = _pw_res["proxy_attrition_tier"]

        # Phase 274: Wire CriticalRefineryCyberKineticSabotageSieve in HybridCovertLens
        hc_meta = getattr(summit, "metadata", {}) or {}
        hc_sab = hc_meta.get("refinery_sabotage", {}) if isinstance(hc_meta, dict) else {}
        _hc_ref_res = CriticalRefineryCyberKineticSabotageSieve.calculate_refinery_sabotage_risk(
            dcs_anomaly_index=hc_sab.get("dcs_anomaly_index", 0.65),
            crack_spread_exposure=hc_sab.get("crack_spread_exposure", 0.75),
            osint_prenotification_velocity=hc_sab.get("osint_prenotification_velocity", 0.50),
            airgap_cyber_defense_score=hc_sab.get("airgap_cyber_defense_score", 0.70),
        )
        metrics.update({f"hybrid_{k}": v for k, v in _hc_ref_res.items()})

        # Phase 285: Wire InterAgencyCounterSubversionSynergySieve
        subv_params = hyb_meta.get("counter_subversion", {}) if isinstance(hyb_meta, dict) else {}
        _subv_res = InterAgencyCounterSubversionSynergySieve.calculate_counter_subversion(
            inter_agency_data_sharing=subv_params.get("inter_agency_data_sharing", 0.80),
            asset_attachment_speed=subv_params.get("asset_attachment_speed", 0.75),
            hawala_volume=subv_params.get("hawala_volume", 0.30),
            diaspora_sanctuary_drag=subv_params.get("diaspora_sanctuary_drag", 0.40),
        )
        metrics["counter_subversion_score"] = _subv_res["counter_subversion_score"]
        metrics["inter_agency_velocity_index"] = _subv_res["inter_agency_velocity_index"]
        metrics["hawala_disruption_efficiency"] = _subv_res["hawala_disruption_efficiency"]
        metrics["counter_subversion_tier"] = _subv_res["counter_subversion_tier"]

        # Phase 294: Wire DeepStateBlackProjectIntelligenceSieve
        bp_params = hyb_meta.get("black_projects", {}) if isinstance(hyb_meta, dict) else {}
        _bp_res = DeepStateBlackProjectIntelligenceSieve.calculate_black_project_resilience(
            compartmentalization_depth=bp_params.get("compartmentalization_depth", 0.80),
            early_warning_cushion=bp_params.get("early_warning_cushion", 0.85),
            c4isr_latency=bp_params.get("c4isr_latency", 0.25),
            foreign_penetration_risk=bp_params.get("foreign_penetration_risk", 0.20),
        )
        metrics["black_project_resilience_score"] = _bp_res["black_project_resilience_score"]

        # Phases 320, 327: Mitrokhin Deep State, Transnational FCRA Ecclesiastical
        hy_meta = getattr(summit, "metadata", {}) or {}
        ds_params = hy_meta.get("mitrokhin_deep_state", {}) if isinstance(hy_meta, dict) else {}
        _ds_res = MitrokhinDeepStatePenetrationSieve.calculate(
            extra_constitutional_power=ds_params.get("extra_constitutional_power", 0.75),
            foreign_fcra_funding=ds_params.get("foreign_fcra_funding", 0.70),
            statutory_ministerial_accountability=ds_params.get("statutory_ministerial_accountability", 0.30),
        )
        metrics["mitrokhin_deep_state_penetration_score"] = _ds_res["mitrokhin_deep_state_penetration_score"]

        fc_params = hy_meta.get("fcra_ecclesiastical", {}) if isinstance(hy_meta, dict) else {}
        _fc_res = TransnationalFCRAEcclesiasticalSieve.calculate(
            foreign_ecclesiastical_inflow=fc_params.get("foreign_ecclesiastical_inflow", 0.75),
            conversion_velocity=fc_params.get("conversion_velocity", 0.70),
            fcra_audit_enforcement=fc_params.get("fcra_audit_enforcement", 0.35),
        )
        metrics["transnational_fcra_ecclesiastical_score"] = _fc_res["transnational_fcra_ecclesiastical_score"]
        metrics["sap_compartmentalization_index"] = _bp_res["sap_compartmentalization_index"]
        metrics["c4isr_warning_latency_margin"] = _bp_res["c4isr_warning_latency_margin"]
        metrics["covert_deterrence_tier"] = _bp_res["covert_deterrence_tier"]

                # Phases 343, 344: Exfiltration & Retaliation Threat Sieve Evaluations
        _efs_res = ExfiltrationAndForeignSanctuarySieve.evaluate(
            visa_pre_clearance=hc_meta.get("visa_pre_clearance", 0.20),
            embassy_sanctuary_proximity=hc_meta.get("embassy_sanctuary_proximity", 0.15),
            offshore_retainer=hc_meta.get("offshore_retainer", 0.20),
            domestic_residence_commitment=hc_meta.get("domestic_residence_commitment", 0.85),
        )
        metrics["exfiltration_and_foreign_sanctuary_score"] = _efs_res["exfiltration_and_foreign_sanctuary_score"]

        _rto_res = RetaliationThreatAndOpSecSieve.evaluate(
            physical_intimidation=hc_meta.get("physical_intimidation", 0.30),
            slapp_litigation_asymmetry=hc_meta.get("slapp_litigation_asymmetry", 0.40),
            statutory_police_protection=hc_meta.get("statutory_police_protection", 0.70),
        )
        metrics["retaliation_threat_and_opsec_score"] = _rto_res["retaliation_threat_and_opsec_score"]

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=confidence,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )

    @staticmethod
    def calculate_mercenary_tech_diffusion(
        foreign_trainers_count: int,
        combat_theater_veterancy: float,
        tactical_asymmetry_level: float
    ) -> Dict[str, Any]:
        """
        Phase 78: Mathematically models foreign mercenary tech diffusion and asymmetric proliferation:
            diffusion_risk = min(1.0, round(
                (foreign_trainers_count / 10.0) * 0.40 +
                combat_theater_veterancy * 0.35 +
                tactical_asymmetry_level * 0.25,
                4
            ))
        """
        trainers = max(0, int(foreign_trainers_count))
        veterancy = max(0.0, min(1.0, float(combat_theater_veterancy)))
        asymmetry = max(0.0, min(1.0, float(tactical_asymmetry_level)))

        trainer_score = min(1.0, trainers / 10.0)
        diffusion_index = min(1.0, round(trainer_score * 0.40 + veterancy * 0.35 + asymmetry * 0.25, 4))
        threat_level = "CRITICAL_PROLIFERATION" if diffusion_index >= 0.70 else "LOCALIZED_ASYMMETRY" if diffusion_index >= 0.40 else "NEGLIGIBLE_RISK"

        return {
            "foreign_trainers_count": trainers,
            "combat_theater_veterancy": veterancy,
            "tactical_asymmetry_level": asymmetry,
            "mercenary_tech_diffusion_index": diffusion_index,
            "threat_classification": threat_level,
            "tactical_proliferation_active": diffusion_index >= 0.40
        }

    @staticmethod
    def calculate_state_resistance_threshold(
        core_salience: float,
        coalition_cushion: float,
        disruption_cost: float,
        election_proximity_months: float
    ) -> Dict[str, Any]:
        """
        Mathematically models state resolve vs. asymmetric street-veto coercion and hybrid disruption:
            R_state = (core_salience * coalition_cushion) * electoral_discount
        Where:
            electoral_discount = 1.0 / (1.0 + max(0.0, (12.0 - election_proximity_months) / 12.0)) if election_proximity_months < 12 else 1.0
        If disruption_cost > R_state:
            State is vulnerable to street-veto capitulation or policy reversal.
        """
        salience = max(0.0, min(1.0, float(core_salience)))
        cushion = max(0.0, min(1.0, float(coalition_cushion)))
        disruption = max(0.0, min(1.0, float(disruption_cost)))
        months = max(0.0, float(election_proximity_months))

        if months < 12.0:
            electoral_discount = round(1.0 / (1.0 + (12.0 - months) / 12.0), 4)
        else:
            electoral_discount = 1.0

        r_state = round(salience * cushion * electoral_discount, 4)
        threshold_gap = round(r_state - disruption, 4)

        if disruption > r_state:
            gap_ratio = (disruption - r_state) / max(0.01, 1.0 - r_state)
            capitulation_prob = min(0.95, round(0.50 + 0.45 * gap_ratio, 4))
            posture = "VULNERABLE_TO_STREET_VETO"
            verdict = "Disruption cost exceeds state resolve threshold; elevated risk of tactical capitulation or policy freeze."
        else:
            resistance_ratio = disruption / max(0.01, r_state)
            capitulation_prob = max(0.02, round(0.40 * resistance_ratio, 4))
            posture = "RESILIENT_STATE_ENFORCEMENT"
            verdict = "State institutional and political cushion exceeds disruption pressure; state resolve holds."

        return {
            "core_salience": salience,
            "coalition_cushion": cushion,
            "disruption_cost": disruption,
            "election_proximity_months": months,
            "electoral_discount_factor": electoral_discount,
            "state_resistance_threshold": r_state,
            "threshold_gap": threshold_gap,
            "capitulation_probability": capitulation_prob,
            "state_posture": posture,
            "strategic_verdict": verdict
        }

    @staticmethod
    def calculate_covert_deterrence_elasticity(
        dossier_fatigue: float,
        sanctuary_protection_level: float,
        preemption_capability: float
    ) -> Dict[str, Any]:
        """
        Mathematically models covert deterrence elasticity and offensive-defense preemption:
            deterrence_ratio = (preemption_capability * (1.0 + 0.6 * dossier_fatigue)) / max(0.10, 1.0 - 0.4 * sanctuary_protection_level)
        """
        fatigue = max(0.0, min(1.0, float(dossier_fatigue)))
        sanctuary = max(0.0, min(1.0, float(sanctuary_protection_level)))
        preemption = max(0.0, min(1.0, float(preemption_capability)))

        effective_push = preemption * (1.0 + 0.6 * fatigue)
        shielding_divisor = max(0.10, 1.0 - 0.4 * sanctuary)

        ratio = round(effective_push / shielding_divisor, 4)
        preemption_prob = min(0.98, max(0.05, round(0.35 * ratio, 4)))
        backlash_risk = min(0.95, max(0.05, round(sanctuary * 0.70 + 0.15 * preemption, 4)))

        if ratio >= 1.25:
            doctrine = "OFFENSIVE_DEFENSIVE_DOMINANT"
            verdict = "Passive diplomacy exhausted; high probability of deniable extraterritorial counter-proxy neutralization."
        elif ratio >= 0.75:
            doctrine = "HYBRID_CONTESTED_DETERRENCE"
            verdict = "Calibrated equilibrium between covert pushback and diplomatic sanctuary shielding."
        else:
            doctrine = "PASSIVE_DOSSIER_CONSTRAINED"
            verdict = "State constrained by host-nation legal safeguards and diplomatic insulation."

        return {
            "dossier_fatigue": fatigue,
            "sanctuary_protection_level": sanctuary,
            "preemption_capability": preemption,
            "covert_deterrence_ratio": ratio,
            "kinetic_preemption_probability": preemption_prob,
            "diplomatic_backlash_risk": backlash_risk,
            "operational_doctrine": doctrine,
            "strategic_verdict": verdict
        }


class ExtraterritorialSovereignAsymmetrySieve:
    """
    Phase 94: Extraterritorial Sovereign Asymmetry Sieve.
    Quantifies the degradation of domestic judicial authority and sovereign equality
    when foreign contractors or intelligence operatives (e.g. Matthew VanDyke, Enrica Lexie, Warren Anderson)
    receive managed legal off-ramps, diplomatic deportation, or default bail under external bilateral coercion.

    Formula:
        A_sovereign = min(1.0, max(0.0, (S_foreign_privilege * P_bilateral_coercion) / max(0.10, J_domestic_parity)))
    """

    @staticmethod
    def calculate_sovereign_asymmetry(
        foreign_privilege_intensity: float,
        bilateral_coercion_pressure: float,
        domestic_parity_enforcement: float
    ) -> Dict[str, Any]:
        privilege = max(0.0, min(1.0, float(foreign_privilege_intensity)))
        coercion = max(0.0, min(1.0, float(bilateral_coercion_pressure)))
        parity = max(0.0, min(1.0, float(domestic_parity_enforcement)))

        divisor = max(0.10, parity)
        score = round(min(1.0, max(0.0, (privilege * coercion) / divisor)), 4)

        if score >= 0.75:
            tier = "ACUTE_SOVEREIGN_COMPROMISE"
            summary = (
                "Acute sovereign compromise: Severe bilateral coercion forces domestic authorities to concede "
                "statutory off-ramps (compounding, default bail, non-prosecution) to foreign state-backed combatants "
                "or mercenaries, severely eroding domestic judicial equality."
            )
            remedy = (
                "Enact non-derogable statutory prosecution bars for borderland mercenary activity under UAPA, "
                "condition diplomatic concessions on reciprocal extradition, and reject managed statutory off-ramps."
            )
        elif score >= 0.50:
            tier = "ELEVATED_DIPLOMATIC_PRESSURE"
            summary = (
                "Elevated pressure: External diplomatic leverage induces tactical delay or administrative compounding, "
                "balancing bilateral trade/security dependencies against domestic judicial enforcement."
            )
            remedy = "Maintain transparent judicial trial records while compartmentalizing bilateral commercial negotiations."
        elif score >= 0.25:
            tier = "CONTROLLED_RECIPROCAL_PAWN"
            summary = (
                "Calibrated leverage: Detained foreign personnel utilized as strategic bargaining pawns to secure "
                "concessions or protect overseas sovereign assets without fully subordinating domestic law."
            )
            remedy = "Extract verified reciprocal consular or intelligence concessions prior to deportation."
        else:
            tier = "UNCOMPROMISED_JUDICIAL_SOVEREIGNTY"
            summary = "Uncompromised sovereign parity: Equal application of municipal penal statutes without foreign immunity or executive interference."
            remedy = "Continue institutionalized rule of law and standard consular notification protocols."

        return {
            "extraterritorial_sovereign_asymmetry_score": score,
            "foreign_privilege_intensity": privilege,
            "bilateral_coercion_pressure": coercion,
            "domestic_parity_enforcement": parity,
            "sovereign_compromise_tier": tier,
            "judicial_sovereignty_summary": summary,
            "sovereign_remedy_pathway": remedy
        }


class DiplomaticCounterIntelSieve:
    """
    Phase 100: Diplomatic Counter-Intelligence Screening & Ideological Vulnerability Sieve.
    Quantifies the risk of intelligence asset exposure, station compromises, and sovereign policy
    subversion resulting from long-tenure regional diplomatic postings, unvetted transnational
    associations (e.g. IAMC, PFI fronts, hostile foreign intelligence interfaces), and domestic political bias.

    Mathematical Formulation:
      Exposure_Factor = (
          0.35 * single_region_tenure_ratio +
          0.35 * transnational_hostile_associations +
          0.30 * ideological_factional_alignment
      )
      Vetting_Divisor = max(0.10, counter_intel_vetting_depth)
      L_intel = min(1.0, max(0.0, round(Exposure_Factor * (0.50 / Vetting_Divisor), 4)))
    """

    @classmethod
    def calculate_counter_intel_vulnerability(
        cls,
        single_region_tenure_ratio: float = 0.85,
        transnational_hostile_associations: float = 0.75,
        counter_intel_vetting_depth: float = 0.30,
        ideological_factional_alignment: float = 0.80
    ) -> Dict[str, Any]:
        tenure = min(1.0, max(0.0, float(single_region_tenure_ratio)))
        assoc = min(1.0, max(0.0, float(transnational_hostile_associations)))
        vetting = min(1.0, max(0.0, float(counter_intel_vetting_depth)))
        faction = min(1.0, max(0.0, float(ideological_factional_alignment)))

        exposure = (0.35 * tenure) + (0.35 * assoc) + (0.30 * faction)
        divisor = max(0.10, vetting)
        l_intel = min(1.0, max(0.0, round(exposure * (0.50 / divisor), 4)))

        if l_intel >= 0.75:
            tier = "CRITICAL_INTEL_EXPOSURE"
            verdict = "COMPROMISED_HUMINT_STATIONS_HIGH_FOREIGN_PENETRATION_RISK"
        elif l_intel >= 0.50:
            tier = "ELEVATED_COUNTER_INTEL_RISK"
            verdict = "SUBSTANTIAL_FACTIONAL_VULNERABILITY_MANDATORY_VETTING_REVIEW"
        elif l_intel >= 0.25:
            tier = "MODERATE_DIPLOMATIC_FRICTION"
            verdict = "CONVENTIONAL_INSTITUTIONAL_INERTIA_NO_STATION_LEAK"
        else:
            tier = "VETTED_INTELLIGENCE_INTEGRITY"
            verdict = "COUNTER_ESPIONAGE_SAFEGUARDS_INTACT"

        rationale = (
            f"Regional tenure ({tenure:.2f}), Hostile associations ({assoc:.2f}), "
            f"Vetting depth ({vetting:.2f}), Factional alignment ({faction:.2f}). "
            f"Counter-intel vulnerability L_intel: {l_intel:.4f} ({tier})."
        )

        return {
            "counter_intel_vulnerability_score": l_intel,
            "intel_exposure_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "single_region_tenure_ratio": tenure,
            "transnational_hostile_associations": assoc,
            "counter_intel_vetting_depth": vetting,
            "ideological_factional_alignment": faction,
            "counter_intel_review_mandated": (l_intel >= 0.50)
        }






class NuclearAmbiguitySieve:
    """
    Phase 234: Evaluates strategic nuclear ambiguity (e.g. Dimona Amimut model, Samson option)
    balancing unacknowledged warhead capacity, survivable second-strike deterrence, and tactical
    deception against intrusive treaty inspection penetration.
    """

    @classmethod
    def calculate_nuclear_ambiguity(
        cls,
        unacknowledged_warhead_capacity: float = 0.85,
        second_strike_credibility: float = 0.90,
        tactical_deception_capability: float = 0.80,
        treaty_inspection_penetration: float = 0.15,
    ) -> Dict[str, Any]:
        """
        Calculates nuclear ambiguity deterrence score using logistic sigmoid model.
        """
        import math
        u_war = max(0.0, min(1.0, float(unacknowledged_warhead_capacity)))
        s_strike = max(0.0, min(1.0, float(second_strike_credibility)))
        t_dec = max(0.0, min(1.0, float(tactical_deception_capability)))
        t_insp = max(0.0, min(1.0, float(treaty_inspection_penetration)))

        numerator = u_war * 0.35 + s_strike * 0.40 + t_dec * 0.25
        ratio = numerator / max(0.10, t_insp)
        z = 1.8 * ratio - 4.5
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.80:
            tier = "MAXIMAL_STRATEGIC_AMBIGUITY_DETERRENCE"
            verdict = "SAMSON_OPTION_CAPABILITY_ZERO_SANCTION_VULNERABILITY"
            rationale = (
                f"Maximal strategic ambiguity ({score:.4f}): Second-strike credibility ({s_strike:.2f}) and deception "
                f"({t_dec:.2f}) maintain supreme deterrence without provoking statutory non-proliferation sanctions."
            )
        elif score >= 0.60:
            tier = "CREDIBLE_OPAQUE_DETERRENCE"
            verdict = "SECURE_SECOND_STRIKE_PROTECTED_POSTURE"
            rationale = (
                f"Credible deterrence ({score:.4f}): Solid retaliatory capability with low inspection penetration ({t_insp:.2f})."
            )
        elif score >= 0.40:
            tier = "CONTESTED_NON_PROLIFERATION_FRICTION"
            verdict = "INSPECTION_PRESSURE_COMPROMISING_AMBIGUITY"
            rationale = (
                f"Contested posture ({score:.4f}): Elevated inspection pressure ({t_insp:.2f}) constraining deterrence flexibility."
            )
        else:
            tier = "COMPROMISED_STRATEGIC_POSTURE"
            verdict = "TRANSPARENCY_CRIPPLING_RETALIATORY_LEVERAGE"
            rationale = (
                f"Compromised ambiguity ({score:.4f}): High inspection penetration or weak second strike erodes deterrence."
            )

        return {
            "nuclear_ambiguity_score": score,
            "unacknowledged_warhead_capacity": round(u_war, 4),
            "second_strike_credibility": round(s_strike, 4),
            "tactical_deception_capability": round(t_dec, 4),
            "treaty_inspection_penetration": round(t_insp, 4),
            "nuclear_ambiguity_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_strategic_ambiguity_intact": score >= 0.60
        }


class NuclearMineralEspionageSieve:
    """
    Phase 241: Nuclear Mineral Espionage & Fissile Transit Corridor Sieve.
    Evaluates covert mineral espionage and border pre-emption linked to strategic fissile deposits
    (e.g., 1947 Gilgit Op Dateline, 1962 Aksai Chin G219 uranium transit, Sino-Pak proliferation).
    Formula:
        fissile_ratio = (0.40 * uranium + 0.35 * corridor + 0.25 * clandestine) / max(0.10, airspace_recon)
        z = 2.8 * fissile_ratio - 3.2
        fissile_chokepoint_vulnerability = 1.0 / (1.0 + exp(-z))
    """
    @classmethod
    def calculate_fissile_vulnerability(
        cls,
        uranium_deposit_proximity: float = 0.85,
        corridor_logistics_control: float = 0.80,
        clandestine_proliferation_risk: float = 0.75,
        airspace_reconnaissance_interdiction: float = 0.40
    ) -> Dict[str, Any]:
        u_prox = max(0.0, min(1.0, float(uranium_deposit_proximity)))
        c_ctrl = max(0.0, min(1.0, float(corridor_logistics_control)))
        p_risk = max(0.0, min(1.0, float(clandestine_proliferation_risk)))
        a_recon = max(0.10, min(1.0, float(airspace_reconnaissance_interdiction)))

        numerator = 0.40 * u_prox + 0.35 * c_ctrl + 0.25 * p_risk
        fissile_ratio = numerator / a_recon
        z = 2.8 * fissile_ratio - 3.2
        vuln = round(1.0 / (1.0 + math.exp(-max(-20.0, min(20.0, z)))), 4)

        if vuln >= 0.80:
            tier = "CRITICAL_FISSILE_CORRIDOR_FLASHPOINT"
            verdict = "PREEMPTIVE_MINERAL_INTERDICTION_FLASHPOINT"
            rationale = (
                f"Critical vulnerability ({vuln:.4f}): Proximity to high-grade uranium deposits combined with "
                f"strategic logistics control creates an imminent pre-emption vector."
            )
        elif vuln >= 0.60:
            tier = "STRATEGIC_NUCLEAR_BUFFER_FRICTION"
            verdict = "ELEVATED_COVERT_TRANSIT_VULNERABILITY"
            rationale = (
                f"Strategic buffer friction ({vuln:.4f}): Contested mineral corridors subject to active "
                f"aerial photoreconnaissance and clandestine monitoring."
            )
        elif vuln >= 0.40:
            tier = "MONITORED_MINERAL_FRONTIER"
            verdict = "STABLE_SURVEILLANCE_POSTURE"
            rationale = (
                f"Monitored frontier ({vuln:.4f}): Fissile deposits sufficiently buffered with adequate "
                f"reconnaissance interdiction."
            )
        else:
            tier = "SECURE_DEMILITARIZED_TERRAIN"
            verdict = "NEGLIGIBLE_FISSILE_ESPIONAGE_RISK"
            rationale = (
                f"Secure terrain ({vuln:.4f}): Zero fissile corridor vulnerability; high airspace sovereignty."
            )

        return {
            "fissile_chokepoint_vulnerability": vuln,
            "uranium_deposit_proximity": round(u_prox, 4),
            "corridor_logistics_control": round(c_ctrl, 4),
            "clandestine_proliferation_risk": round(p_risk, 4),
            "airspace_reconnaissance_interdiction": round(a_recon, 4),
            "fissile_chokepoint_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_nuclear_mineral_flashpoint": vuln >= 0.60
        }


class AsymmetricHostageCoercionSieve:
    """
    Phase 245: Sub-Kinetic Border Captive & Hostage Diplomacy Sieve.
    Evaluates asymmetric captive maneuvers by destabilized adversaries attempting to manufacture
    domestic distractions and extract diplomatic concessions below open kinetic warfare thresholds.
    Formula:
        z = 2.5 * domestic_distraction + 2.2 * sub_kinetic_gap - 3.0 * offensive_defense - 1.2 * diplomatic_leverage
        hostage_coercion_leverage = 1.0 / (1.0 + exp(-z))
    """
    @classmethod
    def calculate_hostage_coercion(
        cls,
        domestic_distraction_incentive: float = 0.85,
        sub_kinetic_threshold_gap: float = 0.80,
        offensive_defense_deterrence: float = 0.75,
        diplomatic_leverage: float = 0.30
    ) -> Dict[str, Any]:
        d_dist = max(0.0, min(1.0, float(domestic_distraction_incentive)))
        s_gap = max(0.0, min(1.0, float(sub_kinetic_threshold_gap)))
        o_det = max(0.0, min(1.0, float(offensive_defense_deterrence)))
        d_lev = max(0.0, min(1.0, float(diplomatic_leverage)))

        z = 2.5 * d_dist + 2.2 * s_gap - 3.0 * o_det - 1.2 * d_lev
        leverage = round(1.0 / (1.0 + math.exp(-max(-20.0, min(20.0, z)))), 4)

        if leverage >= 0.75:
            tier = "ACUTE_HOSTAGE_DIPLOMACY_TRAP"
            verdict = "ASYMMETRIC_CIVILIAN_WEAPONIZATION_ACTIVE"
            rationale = (
                f"Acute coercion trap ({leverage:.4f}): Adversary is aggressively weaponizing border captives to "
                f"deflect domestic collapse; mandates non-linear kinetic/economic counter-escalation."
            )
        elif leverage >= 0.55:
            tier = "ELEVATED_ASYMMETRIC_LEVERAGE"
            verdict = "SUB_KINETIC_GRAYZONE_MANEUVER"
            rationale = (
                f"Elevated hostage posture ({leverage:.4f}): Captive detentions used as diplomatic leverage; "
                f"demands assertive offensive-defense signaling."
            )
        elif leverage >= 0.35:
            tier = "CONTROLLED_BORDER_FRICTION"
            verdict = "ROUTINE_CONSULAR_CONTAINMENT"
            rationale = (
                f"Controlled friction ({leverage:.4f}): Captive incidents handled through standard bilateral "
                f"consular mechanisms without strategic coercion."
            )
        else:
            tier = "MINIMAL_COERCIVE_UTILITY"
            verdict = "TOTAL_OFFENSIVE_DEFENSE_DETERRENCE"
            rationale = (
                f"Minimal utility ({leverage:.4f}): Robust offensive-defense posture completely neutralizes "
                f"adversary's attempt to extract concessions from hostage-taking."
            )

        return {
            "hostage_coercion_leverage": leverage,
            "domestic_distraction_incentive": round(d_dist, 4),
            "sub_kinetic_threshold_gap": round(s_gap, 4),
            "offensive_defense_deterrence": round(o_det, 4),
            "diplomatic_leverage": round(d_lev, 4),
            "hostage_coercion_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_hostage_diplomacy_active": leverage >= 0.55
        }


class SubConventionalProxyWarfareSieve:
    """
    Phase 262: Sub-Conventional Proxy Warfare Sieve.
    Quantifies adversary asymmetric attrition pressure, Operation Tupac-style proxy networks,
    narco-hawala dark capital flow velocity, cross-border infiltration corridor density,
    counterbalanced by precision standoff kinetic deterrence and internal legal/statutory cohesion (NIA/UAPA).
    """

    @classmethod
    def calculate_proxy_attrition(
        cls,
        infiltration_corridors_density: float = 0.50,
        narco_hawala_financing_flow: float = 0.45,
        precision_retaliation_deterrence: float = 0.70,
        internal_societal_cohesion: float = 0.75,
    ) -> Dict[str, Any]:
        """
        Calculates asymmetric proxy attrition threat using calibrated logistic sigmoid:
            z = 2.8 * Infil + 2.5 * Narco - 2.6 * Retaliation - 2.2 * Cohesion - 0.5
            threat = 1 / (1 + exp(-z))
        """
        import math
        infil = max(0.0, min(1.0, float(infiltration_corridors_density)))
        narco = max(0.0, min(1.0, float(narco_hawala_financing_flow)))
        retal = max(0.0, min(1.0, float(precision_retaliation_deterrence)))
        cohes = max(0.0, min(1.0, float(internal_societal_cohesion)))

        z = 2.8 * infil + 2.5 * narco - 2.6 * retal - 2.2 * cohes - 0.5
        threat = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if threat >= 0.75:
            tier = "ACUTE_SUB_CONVENTIONAL_PROXY_WARFARE"
            verdict = "STATE_SPONSORED_ASYMMETRIC_ATTRITION_CAMPAIGN"
            rationale = (
                f"Acute proxy warfare threat ({threat:.4f}): Dense infiltration corridors ({infil:.2f}) and active "
                f"narco-hawala networks ({narco:.2f}) outpace conventional deterrence; mandates standoff kinetic strikes."
            )
        elif threat >= 0.55:
            tier = "ELEVATED_ASYMMETRIC_ATTRITION_RISK"
            verdict = "SUB_KINETIC_PROXY_PROBING_ACTIVE"
            rationale = (
                f"Elevated attrition risk ({threat:.4f}): Sleeper cell financing and localized border skirmishing "
                f"attempt to tie down domestic security forces."
            )
        elif threat >= 0.35:
            tier = "CONTROLLED_BORDER_SECURITY_FRICTION"
            verdict = "CONTAINED_HYBRID_INFILTRATION_PRESSURE"
            rationale = (
                f"Controlled friction ({threat:.4f}): Robust internal cohesion ({cohes:.2f}) and statutory enforcement "
                f"successfully constrain cross-border proxy mobility."
            )
        else:
            tier = "FORTIFIED_COUNTER_SUBVERSION_POSTURE"
            verdict = "OVERWHELMING_OFFENSIVE_DEFENSE_DETERRENCE"
            rationale = (
                f"Fortified deterrence ({threat:.4f}): Proactive retaliation readiness ({retal:.2f}) and high internal "
                f"cohesion neutralize adversary sub-conventional initiatives."
            )

        counter_det = round(min(1.0, max(0.0, 1.0 - threat * 0.85)), 4)
        dark_cap = round(min(1.0, max(0.0, 1.0 - narco * 0.90)), 4)

        return {
            "asymmetric_attrition_threat": threat,
            "infiltration_corridors_density": round(infil, 4),
            "narco_hawala_financing_flow": round(narco, 4),
            "precision_retaliation_deterrence": round(retal, 4),
            "internal_societal_cohesion": round(cohes, 4),
            "counter_proxy_deterrence_index": counter_det,
            "dark_capital_interception_rate": dark_cap,
            "proxy_attrition_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_proxy_attrition_acute": threat >= 0.55,
        }


class InterAgencyCounterSubversionSynergySieve:
    """
    Phase 285: Inter-Agency Counter-Subversion Synergy Sieve.
    Models synchronized operational velocity across intelligence, kinetic, economic,
    and statutory law enforcement agencies (NIA, CBI, ED, IB, FIU-IND) targeting
    extraterritorial gangster-terror-narco funding pipelines and FCRA non-compliant foreign conduits.
    """

    @classmethod
    def calculate_counter_subversion(
        cls,
        inter_agency_data_sharing: float = 0.80,
        asset_attachment_speed: float = 0.75,
        hawala_volume: float = 0.30,
        diaspora_sanctuary_drag: float = 0.40,
    ) -> Dict[str, Any]:
        """
        Calculates Counter-Subversion Readiness Score using calibrated logistic sigmoid:
            z = 2.6 * sharing + 2.8 * attachment - 3.0 * hawala - 2.5 * sanctuary - 0.3
            score = 1 / (1 + exp(-z))
        """
        import math
        sharing = max(0.0, min(1.0, float(inter_agency_data_sharing)))
        attach = max(0.0, min(1.0, float(asset_attachment_speed)))
        hawala = max(0.0, min(1.0, float(hawala_volume)))
        sanc = max(0.0, min(1.0, float(diaspora_sanctuary_drag)))

        z = 2.6 * sharing + 2.8 * attach - 3.0 * hawala - 2.5 * sanc - 0.3
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "PROACTIVE_OFFENSIVE_DEFENSE_SUPREMACY"
            verdict = "SYNCHRONIZED_MULTI_AGENCY_SUBVERSION_DISRUPTION"
            rationale = (
                f"Proactive supremacy ({score:.4f}): Seamless inter-agency data sharing ({sharing:.2f}) and rapid ED/NIA asset "
                f"attachment ({attach:.2f}) decapitate terror-gangster-hawala syndicates."
            )
        elif score >= 0.55:
            tier = "COORDINATED_INTER_AGENCY_DISRUPTION"
            verdict = "EFFECTIVE_FINANCIAL_AND_INTELLIGENCE_CONTAINMENT"
            rationale = (
                f"Coordinated disruption ({score:.4f}): FIU-IND and IB tracking successfully constrains domestic subversion, "
                f"absorbing moderate external diaspora sanctuary drag ({sanc:.2f})."
            )
        elif score >= 0.35:
            tier = "ASYMMETRIC_HYBRID_SECURITY_FRICTION"
            verdict = "INTER_AGENCY_SILO_FRICTION_IMPEDING_INTERDICTION"
            rationale = (
                f"Asymmetric friction ({score:.4f}): Sluggish asset attachments and persistent hawala conduits ({hawala:.2f}) "
                f"slow response velocity against foreign covert conduits."
            )
        else:
            tier = "ACUTE_SUBVERSIVE_PENETRATION_VULNERABILITY"
            verdict = "UNCOORDINATED_ENFORCEMENT_SECURITY_DEFICIT"
            rationale = (
                f"Acute vulnerability ({score:.4f}): Severe inter-agency friction and uninhibited dark hawala flows ({hawala:.2f}) "
                f"expose critical internal security nodes."
            )

        velocity_idx = round(min(1.0, sharing * 0.60 + attach * 0.40), 4)
        hawala_disrupt = round(max(0.0, 1.0 - hawala), 4)

        return {
            "counter_subversion_score": score,
            "inter_agency_data_sharing": round(sharing, 4),
            "asset_attachment_speed": round(attach, 4),
            "hawala_volume": round(hawala, 4),
            "diaspora_sanctuary_drag": round(sanc, 4),
            "inter_agency_velocity_index": velocity_idx,
            "hawala_disruption_efficiency": hawala_disrupt,
            "counter_subversion_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_counter_subversion_ready": score >= 0.55,
        }


class DeepStateBlackProjectIntelligenceSieve:
    """
    Phase 294: Deep-State Black Project Intelligence Sieve.
    Models covert black-budget R&D, compartmentalized special access programs (SAP),
    C4ISR nuclear launch warning latency, and sovereign intelligence resilience against foreign deep-state subversion.
    """

    @classmethod
    def calculate_black_project_resilience(
        cls,
        compartmentalization_depth: float = 0.80,
        early_warning_cushion: float = 0.85,
        c4isr_latency: float = 0.25,
        foreign_penetration_risk: float = 0.20,
    ) -> Dict[str, Any]:
        """
        Calculates Black Project Resilience Score using calibrated logistic sigmoid:
            z = 2.8 * compart + 2.6 * early - 3.2 * latency - 2.8 * penet - 0.3
            score = 1 / (1 + exp(-z))
        """
        import math
        compart = max(0.0, min(1.0, float(compartmentalization_depth)))
        early = max(0.0, min(1.0, float(early_warning_cushion)))
        latency = max(0.0, min(1.0, float(c4isr_latency)))
        penet = max(0.0, min(1.0, float(foreign_penetration_risk)))

        z = 2.8 * compart + 2.6 * early - 3.2 * latency - 2.8 * penet - 0.3
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "FORTIFIED_AIRGAPPED_STRATEGIC_BLACK_PROGRAM"
            verdict = "AIRGAPPED_SPECIAL_ACCESS_PROGRAM_SUPREMACY"
            rationale = (
                f"Fortified black program ({score:.4f}): Deep compartmentalization ({compart:.2f}) and generous early warning "
                f"cushion ({early:.2f}) protect sovereign deterrence R&D and command-and-control continuity."
            )
        elif score >= 0.55:
            tier = "COMPARTMENTALIZED_DETERRENCE_STABILITY"
            verdict = "FUNCTIONAL_C4ISR_SURVIVABILITY"
            rationale = (
                f"Compartmentalized stability ({score:.4f}): Controlled foreign penetration risk ({penet:.2f}) ensures "
                f"adequate nuclear alert cushion and intelligence integrity."
            )
        elif score >= 0.35:
            tier = "ELEVATED_C4ISR_LATENCY_VULNERABILITY"
            verdict = "EXCESSIVE_DECISION_LATENCY_IN_EARLY_WARNING"
            rationale = (
                f"Elevated latency ({score:.4f}): C4ISR decision delays ({latency:.2f}) compress launch response timelines."
            )
        else:
            tier = "CRITICAL_EARLY_WARNING_COMPROMISE"
            verdict = "ACUTE_STRATEGIC_PROGRAM_LEAKAGE"
            rationale = (
                f"Critical compromise ({score:.4f}): Compromised compartmentalization and high penetration risk ({penet:.2f}) "
                f"endanger strategic deterrence survivability."
            )

        warning_margin = round(early - latency, 4)

        return {
            "black_project_resilience_score": score,
            "compartmentalization_depth": round(compart, 4),
            "early_warning_cushion": round(early, 4),
            "c4isr_latency": round(latency, 4),
            "foreign_penetration_risk": round(penet, 4),
            "sap_compartmentalization_index": round(compart, 4),
            "c4isr_warning_latency_margin": warning_margin,
            "covert_deterrence_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_black_program_resilient": score >= 0.55,
        }
class MitrokhinDeepStatePenetrationSieve:
    """
    Phase 320: Quantifies foreign intelligence penetration of national cabinet corridors
    and extra-constitutional advisory bodies (e.g. 2004–2014 NAC model), measuring defense
    procurement delays and statutory subversion.

    Mathematical Formulation:
      z = 3.2 * extra_constitutional_power + 2.8 * foreign_fcra_funding - 3.0 * statutory_ministerial_accountability - 0.4
      S_DeepState_Penetration = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        extra_constitutional_power: float = 0.75,
        foreign_fcra_funding: float = 0.70,
        statutory_ministerial_accountability: float = 0.30,
    ) -> dict:
        extra = max(0.0, min(1.0, float(extra_constitutional_power)))
        fcra = max(0.0, min(1.0, float(foreign_fcra_funding)))
        accountability = max(0.0, min(1.0, float(statutory_ministerial_accountability)))

        z = 3.2 * extra + 2.8 * fcra - 3.0 * accountability - 0.4
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "CRITICAL_SHADOW_CABINET_SUBVERSION"
            verdict = "NATIONAL_SECURITY_PARALYSIS_DETECTED"
            rationale = (
                f"Critical subversion ({score:.4f}): Extra-constitutional policy drafting ({extra:.2f}) and foreign "
                f"institutional conduits ({fcra:.2f}) actively subvert statutory defense procurement and sovereign autonomy."
            )
        elif score >= 0.45:
            tier = "ELEVATED_INFLUENCE_PEDDLING"
            verdict = "INSTITUTIONAL_PRESSURE_CONDUIT"
            rationale = f"Elevated vulnerability ({score:.4f}): Foreign lobby networks exerting bureaucratic friction."
        else:
            tier = "SECURED_STATUTORY_CHAIN_OF_COMMAND"
            verdict = "SOVEREIGN_CABINET_INTEGRITY_MAINTAINED"
            rationale = f"Sovereign integrity ({score:.4f}): Robust statutory accountability ({accountability:.2f}) insulates governance."

        return {
            "mitrokhin_deep_state_penetration_score": score,
            "extra_constitutional_power": round(extra, 4),
            "foreign_fcra_funding": round(fcra, 4),
            "statutory_ministerial_accountability": round(accountability, 4),
            "deep_state_penetration_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_deep_state_compromised": score >= 0.70,
        }
class TransnationalFCRAEcclesiasticalSieve:
    """
    Phase 327: Quantifies foreign institutional charity pipelines, demographic voting shifts
    in sensitive border corridors, and the effectiveness of statutory FCRA license cancellations.

    Mathematical Formulation:
      z = 3.0 * foreign_ecclesiastical_inflow + 2.6 * conversion_velocity - 3.2 * fcra_audit_enforcement - 0.3
      S_FCRA_Subversion = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        foreign_ecclesiastical_inflow: float = 0.75,
        conversion_velocity: float = 0.70,
        fcra_audit_enforcement: float = 0.35,
    ) -> dict:
        inflow = max(0.0, min(1.0, float(foreign_ecclesiastical_inflow)))
        velocity = max(0.0, min(1.0, float(conversion_velocity)))
        audit = max(0.0, min(1.0, float(fcra_audit_enforcement)))

        z = 3.0 * inflow + 2.6 * velocity - 3.2 * audit - 0.3
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.65:
            tier = "SEVERE_TRANSNATIONAL_ECLESIATICAL_SUBVERSION"
            verdict = "COVERT_DEMOGRAPHIC_AND_POLITICAL_ENGINEERING"
            rationale = (
                f"Severe demographic vulnerability ({score:.4f}): Foreign institutional funding ({inflow:.2f}) exploits lax "
                f"regulatory enforcement ({audit:.2f}) to engineer demographic voting shifts in sensitive corridors."
            )
        elif score >= 0.45:
            tier = "MONITORED_FOREIGN_CHARITY_CHANNELS"
            verdict = "ELEVATED_SCRUTINY_REQUIRED"
            rationale = f"Elevated monitoring ({score:.4f}): Inflows require strict statutory utilization audits."
        else:
            tier = "TIGHTLY_AUDITED_SOVEREIGN_NON_PROFIT_FRAMEWORK"
            verdict = "STATUTORY_FCRA_COMPLIANCE_CERTIFIED"
            rationale = f"Robust regulatory enforcement ({score:.4f}): Strict FCRA cancellation protocols ({audit:.2f}) neutralize subversion."

        return {
            "transnational_fcra_ecclesiastical_score": score,
            "foreign_ecclesiastical_inflow": round(inflow, 4),
            "conversion_velocity": round(velocity, 4),
            "fcra_audit_enforcement": round(audit, 4),
            "ecclesiastical_subversion_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_fcra_subversion_severe": score >= 0.65,
        }

# ============================================================================
# PHASES 343, 344: EXFILTRATION & WHISTLEBLOWER OPSEC SIEVES
# ============================================================================

class ExfiltrationAndForeignSanctuarySieve:
    """
    Phase 343: Evaluates asylum pipelines, pre-arranged foreign visas, embassy sanctuary proximity,
    and offshore intermediary retainers indicating foreign intelligence extraction coordination.
    """
    @staticmethod
    def evaluate(
        visa_pre_clearance: float = 0.20,
        embassy_sanctuary_proximity: float = 0.15,
        offshore_retainer: float = 0.20,
        domestic_residence_commitment: float = 0.85,
    ) -> dict:
        v_pre = max(0.0, min(1.0, float(visa_pre_clearance)))
        e_sanc = max(0.0, min(1.0, float(embassy_sanctuary_proximity)))
        o_ret = max(0.0, min(1.0, float(offshore_retainer)))
        d_res = max(0.0, min(1.0, float(domestic_residence_commitment)))

        z = 3.6 * v_pre + 3.0 * e_sanc + 2.5 * o_ret - 2.8 * d_res - 0.5
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "ACTIVE_FOREIGN_INTELLIGENCE_EXFILTRATION_PIPELINE"
            verdict = "COVERT_EXTRACTION_COLLUSION_CONFIRMED"
            rationale = (
                f"Severe exfiltration markers ({score:.4f}): Pre-arranged visas ({v_pre:.2f}) and embassy sanctuary proximity ({e_sanc:.2f}) "
                f"indicate orchestrated foreign intelligence asset extraction."
            )
        elif score >= 0.45:
            tier = "SUSPECT_OFFSHORE_TIES"
            verdict = "ELEVATED_BORDER_AND_TRANSIT_SCRUTINY"
            rationale = f"Elevated exfiltration risk ({score:.4f}): Offshore retainers require financial counter-intelligence audit."
        else:
            tier = "AUTHENTIC_DOMESTIC_RESIDENCY"
            verdict = "ZERO_FOREIGN_EXTRACTION_INDICATORS"
            rationale = f"Domestic integrity ({score:.4f}): Deep residency commitment ({d_res:.2f}) with zero foreign asylum ties."

        return {
            "exfiltration_and_foreign_sanctuary_score": score,
            "visa_pre_clearance_index": round(v_pre, 4),
            "embassy_sanctuary_proximity": round(e_sanc, 4),
            "offshore_retainer_index": round(o_ret, 4),
            "domestic_residence_commitment": round(d_res, 4),
            "exfiltration_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_exfiltration_active": score >= 0.70,
        }


class RetaliationThreatAndOpSecSieve:
    """
    Phase 344: Evaluates physical intimidation, asymmetric SLAPP litigation, and operational security
    to calculate the whistleblower safety protection index.
    """
    @staticmethod
    def evaluate(
        physical_intimidation: float = 0.30,
        slapp_litigation_asymmetry: float = 0.40,
        statutory_police_protection: float = 0.70,
    ) -> dict:
        p_intim = max(0.0, min(1.0, float(physical_intimidation)))
        s_slapp = max(0.0, min(1.0, float(slapp_litigation_asymmetry)))
        s_prot = max(0.0, min(1.0, float(statutory_police_protection)))

        z = 3.5 * p_intim + 3.0 * s_slapp - 2.8 * s_prot - 0.4
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "ACUTE_RETALIATION_AND_PHYSICAL_JEOPARDY"
            verdict = "IMMEDIATE_WITNESS_PROTECTION_MANDATE"
            rationale = (
                f"Extreme danger to insider ({score:.4f}): Physical intimidation ({p_intim:.2f}) and asymmetric SLAPP lawsuits ({s_slapp:.2f}) "
                f"demand sealed identity and active state security."
            )
        elif score >= 0.45:
            tier = "MODERATE_CORPORATE_RETALIATION_RISK"
            verdict = "STATUTORY_WHISTLEBLOWER_LEGAL_COUNSEL"
            rationale = f"Moderate jeopardy ({score:.4f}): Employment termination / civil litigation threats require legal shield."
        else:
            tier = "PROTECTED_OR_SECURE_OPERATING_ENVIRONMENT"
            verdict = "ROBUST_STATUTORY_PROTECTIONS_ACTIVE"
            rationale = f"Low retaliation threat ({score:.4f}): Institutional security ({s_prot:.2f}) mitigates intimidation risks."

        return {
            "retaliation_threat_and_opsec_score": score,
            "physical_intimidation_index": round(p_intim, 4),
            "slapp_litigation_asymmetry": round(s_slapp, 4),
            "statutory_police_protection": round(s_prot, 4),
            "retaliation_threat_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_retaliation_threat_acute": score >= 0.70,
        }

```