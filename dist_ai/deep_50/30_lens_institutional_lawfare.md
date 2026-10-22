# LENS SPECIFICATION: INSTITUTIONAL_LAWFARE

```python
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
            "bilateral_maritime_accord_compliance_score": 0.25,
            "statutory_remedy_bypass_index": 0.0,
            "legal_terminology_hijack_detected": False,
            "sub_national_endowment_vulnerability": 0.0,
            "grayzone_fracture_index": 0.0
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
                "maritime accord", "bow crossing", "ramming", "naval standoff",
                "unclos", "act 80", "eez", "maritime zone", "innocent passage",
                "transit passage", "fonop", "freedom of navigation", "anti-piracy act",
                "contiguous zone", "lakshadweep fonop"
            ]
            maritime_lawfare_detected = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in maritime_keywords)
                for c in claims
            )
            if maritime_lawfare_detected:
                has_fonop = any("fonop" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or "freedom of navigation" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims)
                has_anti_piracy = any("anti-piracy" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims)
                if has_fonop:
                    findings.insert(0, "[GROUNDED TELEMETRY] Maritime EEZ Sovereignty Challenge: Foreign warship executed Freedom of Navigation Operation (FONOP) inside Indian 200 NM EEZ without prior consent, contesting Indian Maritime Zones Act 1976 (Act 80) and UNCLOS Article 56 declaration.")
                    metrics["eez_sovereignty_challenge_severity"] = 0.88
                    metrics["maritime_jurisdiction_friction"] = 0.82
                elif has_anti_piracy:
                    findings.insert(0, "[GROUNDED TELEMETRY] High-Seas Universal Maritime Jurisdiction: Indian naval boarding and interdiction executed under Maritime Anti-Piracy Act 2022 and UNCLOS Articles 100-107.")
                    metrics["anti_piracy_statutory_authority_score"] = 0.95
                else:
                    findings.insert(0, "[GROUNDED TELEMETRY] Bilateral maritime accord breach identified: Violation of 1991 Agreement Article 10 (3 NM buffer) and COLREGs Rule 8 safe navigation rules in international waters.")
                alignment = min(alignment, -0.70)
                metrics["bilateral_maritime_accord_compliance_score"] = 0.15
                metrics["maritime_treaty_breach_severity"] = 0.85

            electoral_keywords = [
                "rpa", "representation of the people", "booth level agent", "bla",
                "special intensive revision", "sir", "electoral roll", "vote chori",
                "vote theft", "turn approver", "election commission", "form 7", "form 8",
                "form 17c", "voter deletion", "election petition"
            ]
            electoral_lawfare_detected = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in electoral_keywords)
                for c in claims
            )
            if electoral_lawfare_detected:
                has_courtroom_jargon = any(
                    any(j in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for j in ["turn approver", "approver", "conspiracy", "deshdrohi", "treason"])
                    for c in claims
                )
                has_formal_petition = any(
                    any(p in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for p in ["election petition", "section 80", "section 24", "affidavit under oath", "high court petition"])
                    for c in claims
                )
                remedy_bypass_score = 0.88 if not has_formal_petition else 0.15
                findings.insert(0, (
                    "[GROUNDED TELEMETRY] Domestic Electoral Statutory Audit: Allegations of electoral roll fraud evaluated against "
                    "Representation of the People Act 1950 (Sections 21, 22, 24), RPA 1951 (Section 80), and Registration of Electors Rules 1960. "
                    "Mandatory statutory remedies (Booth Level Agent scrutiny, Section 24 statutory appeals, High Court election petitions) "
                    "were bypassed in favor of extra-judicial political press narratives."
                ))
                alignment = min(alignment, -0.65)
                metrics["statutory_remedy_bypass_index"] = remedy_bypass_score
                metrics["electoral_jurisprudence_compliance_score"] = 0.30 if not has_formal_petition else 0.85
                metrics["legal_terminology_hijack_detected"] = bool(has_courtroom_jargon and not has_formal_petition)

            off_ramp_keywords = [
                "default bail", "section 167", "180 days", "section 188", "piecemeal chargesheet",
                "foreigners act compounding", "compounding fee", "frro compounding", "van dyke bail",
                "vandyke bail", "statutory off-ramp", "managed off-ramp"
            ]
            off_ramp_detected = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in off_ramp_keywords)
                for c in claims
            )
            if off_ramp_detected:
                findings.insert(0, (
                    "[STATUTORY OFF-RAMP TELEMETRY] Forensic Statutory Exit Identified: Investigation against foreign nationals "
                    "utilized Section 167(2) default bail and Foreigners Act compounding (Sections 21/23) as a managed diplomatic off-ramp, "
                    "navigating Section 188 CrPC extraterritorial evidentiary sanction barriers."
                ))
                metrics["statutory_off_ramp_detected"] = True
                metrics["extraterritorial_sanction_barrier_flag"] = True
                metrics["default_bail_diplomatic_compromise_score"] = 0.88

            endowment_keywords = [
                "sattra", "satras", "batadrava", "gorukhuti", "dhalpur",
                "char land", "waqf board", "section 40", "hrce", "temple land encroachment",
                "srimanta sankardev", "barpeta sattra", "lumding sattra"
            ]
            endowment_detected = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in endowment_keywords)
                for c in claims
            )
            if endowment_detected:
                has_waqf = any("waqf" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or "section 40" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims)
                has_char = any("char" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or "gorukhuti" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims)
                
                encroach_val = 0.85 if has_char else 0.65
                asym_val = 0.90 if has_waqf else 0.50
                cadastre_val = 0.20 if has_char else 0.50
                
                sieve_res = SubNationalEndowmentSieve.calculate_endowment_vulnerability(
                    encroachment_intensity=encroach_val,
                    waqf_statutory_asymmetry=asym_val,
                    cadastral_survey_clarity=cadastre_val
                )
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Sub-National Sacred Geography & Religious Endowment Sieve triggered: "
                    f"Vulnerability Tier [{sieve_res['vulnerability_tier']}] (Score: {sieve_res['endowment_vulnerability_score']:.2f}). "
                    f"{sieve_res['legal_risk_summary']} Statutory pathway: {sieve_res['statutory_remedy_pathway']}"
                ))
                alignment = min(alignment, -0.72)
                metrics["sub_national_endowment_vulnerability"] = sieve_res["endowment_vulnerability_score"]
                metrics["endowment_vulnerability_tier"] = sieve_res["vulnerability_tier"]
                metrics["waqf_section_40_asymmetry_flag"] = bool(has_waqf)
                metrics["char_land_cadastral_vagueness"] = sieve_res["cadastral_vagueness_index"]

            faultline_keywords = [
                "sc st act", "section 18a", "kashinath mahajan", "subhash kashinath",
                "anticipatory bail denial", "hisab chukta", "ancestral sin", "general category",
                "caste faultline", "caste polarization", "creamy layer exclusion", "due process erosion"
            ]
            faultline_detected = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in faultline_keywords)
                for c in claims
            )
            if faultline_detected:
                has_18a = any("section 18a" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or "kashinath" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or "anticipatory bail" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims)
                has_guilt = any("ancestral sin" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or "hisab chukta" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims)
                
                asym_input = 0.90 if has_18a else 0.65
                guilt_input = 0.85 if has_guilt else 0.45
                merit_input = 0.35 if has_18a else 0.60
                
                fault_res = IntraCivilizationalFaultlineSieve.calculate_faultline_vulnerability(
                    statutory_due_process_asymmetry=asym_input,
                    historical_guilt_narrative_intensity=guilt_input,
                    meritocratic_preservation_index=merit_input
                )
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Intra-Civilizational Faultline & Statutory Asymmetry Sieve triggered: "
                    f"Threat Tier [{fault_res['fracture_threat_tier']}] (Score: {fault_res['intra_civilizational_fracture_score']:.2f}). "
                    f"{fault_res['civilizational_risk_summary']} Statutory pathway: {fault_res['jurisprudential_remedy_pathway']}"
                ))
                alignment = min(alignment, -0.75)
                metrics["intra_civilizational_fracture_score"] = fault_res["intra_civilizational_fracture_score"]
                metrics["fracture_threat_tier"] = fault_res["fracture_threat_tier"]
                metrics["statutory_due_process_deficit_flag"] = bool(has_18a)
                metrics["meritocratic_erosion_risk"] = fault_res["meritocratic_erosion_index"]

            grayzone_keywords = [
                "jizya", "middle class tax", "taxpayer burden", "base rebellion", "grayzone",
                "blunder called modi", "taxpayer squeeze", "merit denial", "electoral welfarism"
            ]
            grayzone_detected = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in grayzone_keywords)
                for c in claims
            )
            if grayzone_detected:
                has_tax_fatigue = any(any(k in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for k in ["jizya", "middle class", "taxpayer", "tax"]) for c in claims)
                has_strict_law = any(any(k in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for k in ["section 18a", "sc st", "bail", "merit"]) for c in claims)

                gz_res = CulturalReligiousGrayzoneSieve.calculate_grayzone_fracture(
                    direct_tax_burden_ratio=0.85 if has_tax_fatigue else 0.50,
                    middle_class_benefit_ratio=0.08,
                    presumption_of_guilt=0.90 if has_strict_law else 0.40,
                    bail_exclusion_severity=0.85 if has_strict_law else 0.35,
                    ecosystem_shield_strength=0.20
                )
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Cultural & Religious Grayzone Sieve triggered: "
                    f"Fracture Tier [{gz_res['fracture_tier']}] (Index: {gz_res['grayzone_fracture_index']:.2f}). "
                    f"Electoral Risk: {gz_res['electoral_alienation_risk']}. {gz_res['structural_summary']}"
                ))
                alignment = min(alignment, -0.78)
                metrics["grayzone_fracture_index"] = gz_res["grayzone_fracture_index"]
                metrics["grayzone_fracture_tier"] = gz_res["fracture_tier"]
                metrics["electoral_alienation_risk"] = gz_res["electoral_alienation_risk"]

            # Phase 181: Judicial Subversion & Extra-Judicial Deterrence Sieve
            subv_res = JudicialSubversionSieve.evaluate_judicial_subversion(claims=claims)
            metrics["judicial_subversion_score"] = subv_res["judicial_subversion_score"]
            metrics["judicial_subversion_tier"] = subv_res["judicial_subversion_tier"]
            metrics["judicial_subversion_risk_flag"] = subv_res["is_subversion_detected"]
            metrics["judicial_operational_verdict"] = subv_res["operational_verdict"]
            if subv_res["is_subversion_detected"] or subv_res["matched_arson_keywords"]:
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Judicial Subversion & Extra-Judicial Deterrence Sieve triggered: "
                    f"Tier [{subv_res['judicial_subversion_tier']}] (Score: {subv_res['judicial_subversion_score']:.2f}). "
                    f"Verdict: {subv_res['operational_verdict']}. {subv_res['tactical_rationale']}"
                ))
                alignment = min(alignment, -0.82)

            # Phase 187: Asymmetric Coercion Premium & Democratic Subversion Sieve
            coercion_res = CoercionPremiumSieve.evaluate_coercion_premium(claims=claims)
            metrics["coercion_premium_score"] = coercion_res["coercion_premium_score"]
            metrics["coercion_premium_tier"] = coercion_res["coercion_premium_tier"]
            metrics["daily_economic_friction_inr_cr"] = coercion_res["daily_economic_friction_inr_cr"]
            metrics["is_coercion_premium_active"] = coercion_res["is_coercion_premium_active"]
            metrics["coercion_operational_verdict"] = coercion_res["operational_verdict"]
            if coercion_res["is_coercion_premium_active"] or coercion_res["matched_mob_keywords"]:
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Coercion Premium & Democratic Subversion Sieve triggered: "
                    f"Tier [{coercion_res['coercion_premium_tier']}] (Score: {coercion_res['coercion_premium_score']:.2f}, "
                    f"Friction: ₹{coercion_res['daily_economic_friction_inr_cr']:.1f} Cr/day). "
                    f"Verdict: {coercion_res['operational_verdict']}. {coercion_res['tactical_rationale']}"
                ))
                alignment = min(alignment, -0.80)

            # Phase 193: Granovetter Crowd Cascade Threshold Sieve
            cascade_res = CrowdCascadeThresholdSieve.evaluate_cascade_threshold(claims=claims)
            metrics["crowd_cascade_probability"] = cascade_res["cascade_probability"]
            metrics["crowd_cascade_tier"] = cascade_res["cascade_tier"]
            metrics["tipping_threshold_reached"] = cascade_res["is_tipping_reached"]
            metrics["cascade_operational_verdict"] = cascade_res["operational_verdict"]
            if cascade_res["is_tipping_reached"] or cascade_res["matched_keywords"]:
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Crowd Cascade Threshold Sieve triggered: "
                    f"Tier [{cascade_res['cascade_tier']}] (Probability: {cascade_res['cascade_probability']:.2f}). "
                    f"Verdict: {cascade_res['operational_verdict']}. {cascade_res['tactical_rationale']}"
                ))
                alignment = min(alignment, -0.78)

            # Phase 194: State Machiavellian Inaction & Safety Valve Sieve
            inaction_res = StateMachiavellianSieve.evaluate_state_inaction(
                daily_economic_friction_inr_cr=coercion_res["daily_economic_friction_inr_cr"],
                claims=claims
            )
            metrics["state_inaction_score"] = inaction_res["state_inaction_score"]
            metrics["state_inaction_tier"] = inaction_res["state_inaction_tier"]
            metrics["is_deliberate_toleration"] = inaction_res["is_deliberate_toleration"]
            metrics["state_inaction_verdict"] = inaction_res["operational_verdict"]
            if inaction_res["is_deliberate_toleration"] or inaction_res["matched_keywords"]:
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] State Machiavellian Inaction Sieve triggered: "
                    f"Tier [{inaction_res['state_inaction_tier']}] (Score: {inaction_res['state_inaction_score']:.2f}). "
                    f"Verdict: {inaction_res['operational_verdict']}. {inaction_res['tactical_rationale']}"
                ))
        else:
            metrics["judicial_subversion_score"] = 0.15
            metrics["judicial_subversion_tier"] = "STABLE_CONSTITUTIONAL_EQUILIBRIUM"
            metrics["judicial_subversion_risk_flag"] = False
            metrics["coercion_premium_score"] = 0.10
            metrics["coercion_premium_tier"] = "CONSTITUTIONAL_ORDER_MAINTAINED"
            metrics["daily_economic_friction_inr_cr"] = 0.0
            metrics["is_coercion_premium_active"] = False
            metrics["crowd_cascade_probability"] = 0.12
            metrics["crowd_cascade_tier"] = "DORMANT_CROWD_EQUILIBRIUM"
            metrics["tipping_threshold_reached"] = False
            metrics["state_inaction_score"] = 0.20
            metrics["state_inaction_tier"] = "IMMEDIATE_DECISIVE_ENFORCEMENT"
            metrics["is_deliberate_toleration"] = False

        if "judicial_subversion_score" not in metrics:
            metrics["judicial_subversion_score"] = 0.15
        if "coercion_premium_score" not in metrics:
            metrics["coercion_premium_score"] = 0.10
        if "crowd_cascade_probability" not in metrics:
            metrics["crowd_cascade_probability"] = 0.12
        if "state_inaction_score" not in metrics:
            metrics["state_inaction_score"] = 0.20

        return LensEvaluation(

            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=0.90,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics,
            evidence_status="sufficient"
        )

    @staticmethod
    def calculate_statutory_off_ramp(
        days_in_custody: int,
        uapa_chargesheet_filed: bool,
        crpc_188_sanction_present: bool,
        foreigners_act_compounded: bool
    ) -> Dict[str, Any]:
        """
        Phase 78: Mathematically models statutory legal off-ramps under Indian criminal jurisprudence:
            If days_in_custody >= 180 and not uapa_chargesheet_filed:
                Default bail is mandatory under Section 167(2) CrPC / Section 43D(2) UAPA.
            If not crpc_188_sanction_present:
                Extraterritorial offences face mandatory statutory bar on cognizance without Central Sanction.
            If foreigners_act_compounded:
                Administrative exit permitted via FRRO compounding fee settlement.
        """
        custody = max(0, int(days_in_custody))
        is_default_entitlement = custody >= 180 and not uapa_chargesheet_filed
        sanction_barrier = not crpc_188_sanction_present
        compounded = bool(foreigners_act_compounded)

        compromise_score = round(
            (0.45 if is_default_entitlement else 0.10) +
            (0.35 if sanction_barrier else 0.0) +
            (0.20 if compounded else 0.0),
            4
        )

        if is_default_entitlement and sanction_barrier:
            exit_type = "MANAGED_DIPLOMATIC_STATUTORY_EXIT"
            verdict = "State utilized statutory procedural expiration to permit foreign national departure without executive pardon fallout."
        elif is_default_entitlement:
            exit_type = "STATUTORY_DEFAULT_BAIL"
            verdict = "Procedural timeline lapse under CrPC Section 167(2) compelled judicial release."
        else:
            exit_type = "STANDARD_INVESTIGATION_CONTINUING"
            verdict = "Statutory custody window active; trial/investigation within regular jurisdictional limits."

        return {
            "days_in_custody": custody,
            "default_bail_statutory_entitlement": is_default_entitlement,
            "extraterritorial_sanction_barrier": sanction_barrier,
            "foreigners_act_compounded": compounded,
            "diplomatic_compromise_score": compromise_score,
            "statutory_exit_classification": exit_type,
            "legal_verdict": verdict
        }

    @staticmethod
    def calculate_pundit_credibility(
        diagnostic_accuracy: float,
        operational_feasibility: float
    ) -> Dict[str, Any]:
        """
        Quantifies the analytical credibility vs. rhetorical noise of commentators and pundits:
            Credibility Score = Diagnostic Accuracy * Operational Feasibility
        Separates valid constitutional/statutory critiques from normative wishful thinking
        lacking statecraft execution capability.
        """
        diag = max(0.0, min(1.0, float(diagnostic_accuracy)))
        feas = max(0.0, min(1.0, float(operational_feasibility)))

        score = round(diag * feas, 4)

        if diag >= 0.70 and feas >= 0.60:
            category = "Actionable Statecraft / Strategic Doctrine"
            operational_actionability = "HIGH"
            guidance = "Analytical critique aligns with constitutional mechanisms and operational enforcement pathways."
        elif diag >= 0.70 and feas < 0.40:
            category = "Rhetorical / Normative Critique (High Diagnostic, Low Operational Execution)"
            operational_actionability = "LOW"
            guidance = "Accurate diagnosis of statutory asymmetry, but operational proposals ignore legislative/coalition constraints."
        elif diag >= 0.70 and 0.40 <= feas < 0.60:
            category = "Strategic Diagnosis Constrained by Bureaucratic Friction"
            operational_actionability = "MODERATE"
            guidance = "Sound diagnosis with viable mechanisms that require coalition alignment or judicial overcoming."
        elif diag < 0.50 and feas >= 0.60:
            category = "Bureaucratic Inertia / Procedural Compliance"
            operational_actionability = "PROCEDURAL"
            guidance = "High procedural feasibility but misidentifies underlying civilizational or strategic drivers."
        elif diag < 0.50 and feas < 0.50:
            category = "Superficial Propaganda / Informational Noise"
            operational_actionability = "NEGLIGIBLE"
            guidance = "Neither strategically accurate nor operationally executable; discursive noise."
        else:
            category = "Mixed Intermediate Discourse"
            operational_actionability = "INTERMEDIATE"
            guidance = "Presents partial empirical evidence with moderate execution bottlenecks."

        return {
            "diagnostic_accuracy": diag,
            "operational_feasibility": feas,
            "credibility_score": score,
            "discourse_category": category,
            "operational_actionability": operational_actionability,
            "execution_guidance": guidance,
            "statutory_execution_barrier_identified": feas < 0.50
        }

    @staticmethod
    def calculate_maritime_jurisdiction_compliance(
        zone_nm: float,
        is_warship: bool = True,
        prior_consent_declared: bool = False,
        conducting_military_maneuver: bool = False,
        anti_piracy_interception: bool = False
    ) -> Dict[str, Any]:
        """
        Phase 84: Evaluates maritime domain sovereignty across:
        - Indian Maritime Zones Act 1976 (Act 80 of 1976):
          * Section 3: 12 NM Territorial Waters (Sovereign baseline, warships require prior notification)
          * Section 5: 24 NM Contiguous Zone (Customs, fiscal, immigration, sanitation)
          * Section 7: 200 NM Exclusive Economic Zone (EEZ sovereign rights for resource exploitation)
        - UNCLOS 1982:
          * Articles 17-26: Innocent Passage regime
          * Articles 56 & 58: EEZ jurisdiction vs foreign military activities (US FONOPs friction)
        - COLREGs 1972: Rules 8, 14, 15 liability for grayzone shouldering/ramming
        - Maritime Anti-Piracy Act, 2022: High-seas universal jurisdiction enforcement
        """
        zone_nm = max(0.0, float(zone_nm))
        if zone_nm <= 12.0:
            zone_type = "TERRITORIAL_WATERS"
            act_section = "Act 80/1976 Section 3"
            unclos_regime = "UNCLOS Articles 17-26 (Innocent Passage)"
            sovereignty_tier = "SOVEREIGN_TERRITORY"
            is_infringement = bool(is_warship and not prior_consent_declared)
        elif zone_nm <= 24.0:
            zone_type = "CONTIGUOUS_ZONE"
            act_section = "Act 80/1976 Section 5"
            unclos_regime = "UNCLOS Article 33"
            sovereignty_tier = "ENFORCEMENT_JURISDICTION"
            is_infringement = bool(is_warship and conducting_military_maneuver and not prior_consent_declared)
        elif zone_nm <= 200.0:
            zone_type = "EXCLUSIVE_ECONOMIC_ZONE"
            act_section = "Act 80/1976 Section 7"
            unclos_regime = "UNCLOS Articles 56 & 58 (Resource Sovereign Rights vs Navigation)"
            sovereignty_tier = "SOVEREIGN_ECONOMIC_RIGHTS"
            is_infringement = bool(conducting_military_maneuver and not prior_consent_declared)
        else:
            zone_type = "HIGH_SEAS"
            act_section = "Maritime Anti-Piracy Act 2022 / Universal Jurisdiction"
            unclos_regime = "UNCLOS Article 87 (Freedom of the High Seas)"
            sovereignty_tier = "GLOBAL_COMMONS"
            is_infringement = False

        if anti_piracy_interception:
            legality = "AUTHORIZED_UNIVERSAL_JURISDICTION"
            legal_basis = "Maritime Anti-Piracy Act 2022 / UNCLOS Art. 100-107"
            compliance_score = 0.95
        elif is_infringement:
            legality = "SOVEREIGN_EEZ_CHALLENGE_OR_FONOP"
            legal_basis = f"Violation of {act_section} and Indian declaration under UNCLOS Art. 56"
            compliance_score = 0.20
        else:
            legality = "COMPLIANT_PASSAGE"
            legal_basis = f"Authorized under {act_section} and {unclos_regime}"
            compliance_score = 0.85

        return {
            "zone_distance_nm": zone_nm,
            "maritime_zone_classification": zone_type,
            "statutory_act": act_section,
            "unclos_regime": unclos_regime,
            "sovereignty_tier": sovereignty_tier,
            "is_sovereignty_infringement": is_infringement,
            "legality_assessment": legality,
            "legal_basis": legal_basis,
            "maritime_jurisdiction_score": compliance_score
        }


class SubNationalEndowmentSieve:
    """
    Phase 88: Sub-National Sacred Geography & Religious Endowment Sieve.
    Evaluates asymmetric statutory protections, riverine cadastre ambiguity,
    and institutional encroachment vulnerabilities on sacred/indigenous endowments.
    
    Formula:
        S_endowment = min(1.0, max(0.0, 0.40 * E_encroach + 0.35 * W_asymmetry + 0.25 * (1.0 - C_cadastre)))
    """

    @staticmethod
    def calculate_endowment_vulnerability(
        encroachment_intensity: float,
        waqf_statutory_asymmetry: float,
        cadastral_survey_clarity: float
    ) -> Dict[str, Any]:
        encroach = max(0.0, min(1.0, float(encroachment_intensity)))
        asymmetry = max(0.0, min(1.0, float(waqf_statutory_asymmetry)))
        cadastre = max(0.0, min(1.0, float(cadastral_survey_clarity)))
        cadastral_vagueness = round(1.0 - cadastre, 4)

        score = round(min(1.0, max(0.0, 0.40 * encroach + 0.35 * asymmetry + 0.25 * cadastral_vagueness)), 4)

        if score >= 0.75:
            tier = "CRITICAL_ENCROACHMENT_RISK"
            summary = (
                "Severe vulnerability: Unchecked demographic/physical encroachment compounded by asymmetric statutory "
                "inquiry powers (e.g. Waqf Act Section 40) and absent or shifting riverine cadastral boundaries."
            )
            remedy = (
                "Deploy statutory delimitation under RPA Section 8A, execute eviction drives under Assam Land and "
                "Revenue Regulation 1886, and enact legislative parity removing unilateral endowment determination authority."
            )
        elif score >= 0.50:
            tier = "ELEVATED_STATUTORY_ASYMMETRY"
            summary = (
                "Elevated vulnerability: Substantial statutory imbalance between self-governing Waqf tribunals and state-controlled "
                "Hindu Religious and Charitable Endowments (HR&CE), exposing institutions to legal/territorial friction."
            )
            remedy = (
                "Establish reciprocal autonomous property adjudication boards and mandate judicial pre-clearance for property reclassification."
            )
        elif score >= 0.25:
            tier = "MODERATE_CADASTRAL_FRICTION"
            summary = (
                "Moderate friction: Riverine/char-land boundary ambiguity or local administrative delays without acute statutory capture."
            )
            remedy = "Execute GIS-delineated drone cadastre surveys and digitize ancestral revenue pattas."
        else:
            tier = "SECURE_ENDOWMENT"
            summary = "Endowment titles legally anchored, verified by registered cadastre surveys with symmetrical institutional protection."
            remedy = "Maintain periodic cadastral audits and satellite boundary telemetry."

        return {
            "endowment_vulnerability_score": score,
            "encroachment_intensity": encroach,
            "waqf_asymmetry_index": asymmetry,
            "cadastral_clarity_index": cadastre,
            "cadastral_vagueness_index": cadastral_vagueness,
            "vulnerability_tier": tier,
            "legal_risk_summary": summary,
            "statutory_remedy_pathway": remedy
        }


class IntraCivilizationalFaultlineSieve:
    """
    Phase 93: Intra-Civilizational Faultline & Statutory Asymmetry Sieve.
    Quantifies civilizational polarization, due process erosion, and meritocratic friction
    induced by competitive electoral clientelism, strict liability statutory amendments (e.g. Section 18A SC/ST Act),
    and state-internalized collective historical guilt narratives.

    Formula:
        F_fracture = min(1.0, max(0.0, 0.40 * S_asymmetry + 0.35 * G_grievance + 0.25 * (1.0 - M_merit)))
    """

    @staticmethod
    def calculate_faultline_vulnerability(
        statutory_due_process_asymmetry: float,
        historical_guilt_narrative_intensity: float,
        meritocratic_preservation_index: float
    ) -> Dict[str, Any]:
        asymmetry = max(0.0, min(1.0, float(statutory_due_process_asymmetry)))
        guilt = max(0.0, min(1.0, float(historical_guilt_narrative_intensity)))
        merit = max(0.0, min(1.0, float(meritocratic_preservation_index)))
        merit_deficit = round(1.0 - merit, 4)

        score = round(min(1.0, max(0.0, 0.40 * asymmetry + 0.35 * guilt + 0.25 * merit_deficit)), 4)

        if score >= 0.75:
            tier = "CRITICAL_CIVILIZATIONAL_FRACTURE"
            summary = (
                "Severe faultline risk: Complete removal of judicial due process safeguards (e.g. denial of anticipatory "
                "bail and preliminary inquiry), coupled with aggressive state-promoted collective historical guilt narratives "
                "and severe erosion of meritocratic administrative advancement."
            )
            remedy = (
                "Restore procedural due process safeguards (mandatory preliminary inquiry per Kashinath Mahajan), "
                "de-escalate competitive caste-based statutory weaponization, and anchor civilizational discourse in "
                "dharmic consensus and universal equal protection under Article 14."
            )
        elif score >= 0.50:
            tier = "ELEVATED_POLARIZATION"
            summary = (
                "Elevated polarization: Legislative override of judicial safeguards creates asymmetric legal exposure, "
                "fostering inter-community alienation and risk of capital/human talent flight among unreserved categories."
            )
            remedy = (
                "Mandate judicial scrutiny for vexatious complaints, introduce economic-creamy-layer filters across all "
                "affirmative action categories, and institutionalize objective arbitration boards."
            )
        elif score >= 0.25:
            tier = "MODERATE_COMMUNAL_FRICTION"
            summary = (
                "Moderate friction: Political campaign rhetoric invoking historical grievance or regional identity quotas "
                "without systemic legislative due process dismantlement."
            )
            remedy = "Enforce strict judicial limits on sub-quota fragmentation and maintain administrative merit baselines."
        else:
            tier = "COHESIVE_DHARMIC_EQUILIBRIUM"
            summary = (
                "Harmonious civilizational statecraft: Balanced social empowerment aligned with universal constitutional "
                "equality, merit preservation, and shared civilizational heritage."
            )
            remedy = "Maintain institutional parity, objective rule of law, and transparent merit-based public appointments."

        return {
            "intra_civilizational_fracture_score": score,
            "statutory_due_process_asymmetry": asymmetry,
            "historical_guilt_narrative_intensity": guilt,
            "meritocratic_preservation_index": merit,
            "meritocratic_erosion_index": merit_deficit,
            "fracture_threat_tier": tier,
            "civilizational_risk_summary": summary,
            "jurisprudential_remedy_pathway": remedy
        }


class CulturalReligiousGrayzoneSieve:
    """
    Phase 110: Cultural & Religious Grayzone Sieve (Intra-Civilizational Base Fracturing).
    Quantifies the subterranean fracture within a ruling coalition or civilizational core
    induced by asymmetric middle-class direct tax burden vs populist welfare distribution,
    strict statutory liability weaponization, and lack of independent intellectual ecosystem shields.

    Formula:
        Tax_Grievance = min(1.0, direct_tax_burden_ratio / max(0.10, middle_class_benefit_ratio * 10.0))
        Lawfare_Severity = 0.50 * presumption_of_guilt + 0.50 * bail_exclusion_severity
        Fracture_Index = min(1.0, max(0.0, 0.40 * Tax_Grievance + 0.35 * Lawfare_Severity + 0.25 * (1.0 - ecosystem_shield)))
    """

    @staticmethod
    def calculate_grayzone_fracture(
        direct_tax_burden_ratio: float,
        middle_class_benefit_ratio: float,
        presumption_of_guilt: float,
        bail_exclusion_severity: float,
        ecosystem_shield_strength: float
    ) -> Dict[str, Any]:
        tax_ratio = max(0.0, float(direct_tax_burden_ratio))
        benefit_ratio = max(0.01, float(middle_class_benefit_ratio))
        guilt = max(0.0, min(1.0, float(presumption_of_guilt)))
        bail = max(0.0, min(1.0, float(bail_exclusion_severity)))
        shield = max(0.0, min(1.0, float(ecosystem_shield_strength)))

        # Tax grievance normalized with division guard
        tax_grievance = round(min(1.0, tax_ratio / max(0.10, benefit_ratio * 10.0)), 4)
        lawfare_sev = round(0.50 * guilt + 0.50 * bail, 4)
        shield_deficit = round(1.0 - shield, 4)

        fracture_idx = round(min(1.0, max(0.0, 0.40 * tax_grievance + 0.35 * lawfare_sev + 0.25 * shield_deficit)), 4)

        if fracture_idx >= 0.75:
            tier = "CRITICAL_BASE_REBELLION"
            summary = (
                "Acute base alienation: Disproportionate direct tax extraction without social security nets, combined with "
                "statutory presumption of guilt and absence of ecosystem protection, triggering active voter apathy, third-party "
                "protest votes, and severe intra-coalition fracturing."
            )
            electoral_risk = "HIGH_APATHY_AND_PARLIAMENTARY_SEAT_LOSS"
        elif fracture_idx >= 0.50:
            tier = "ACUTE_INTRA_COALITION_FRICTION"
            summary = (
                "Elevated intra-bloc tension: Public intellectual rebellion and growing resentment among core taxpayers and "
                "unreserved communities over perceived one-sided welfarism and statutory double standards."
            )
            electoral_risk = "MODERATE_MARGINAL_SWING_VULNERABILITY"
        elif fracture_idx >= 0.25:
            tier = "MANAGEABLE_TACTICAL_TENSION"
            summary = (
                "Manageable friction: Localized middle-class complaints absorbed by national security or civilizational "
                "symbolic resonance."
            )
            electoral_risk = "LOW_IMPACT_ELECTORAL_NOISE"
        else:
            tier = "COHESIVE_CIVILIZATIONAL_EQUILIBRIUM"
            summary = (
                "Harmonious civilizational statecraft: Equitable fiscal burden, due process integrity, and strong institutional "
                "support across all demographic strata."
            )
            electoral_risk = "STABLE_HEGEMONIC_COALITION"

        return {
            "grayzone_fracture_index": fracture_idx,
            "tax_grievance_score": tax_grievance,
            "lawfare_severity_score": lawfare_sev,
            "ecosystem_shield_deficit": shield_deficit,
            "fracture_tier": tier,
            "electoral_alienation_risk": electoral_risk,
            "structural_summary": summary
        }


class JudicialSubversionSieve:
    """
    Phase 181: Judicial Subversion & Extra-Judicial Deterrence Sieve.
    Evaluates public incitement targeting judicial benches and constitutional architecture,
    measuring the breach of statutory immunity, foreign replication rhetoric (e.g. Albanian Supreme Court arson threats),
    and BNS Section 152 / 124A statutory deterrence thresholds.

    Formula:
        S_subversion = min(1.0, max(0.0, 0.40 * I_incitement + 0.35 * B_breach + 0.25 * (1.0 - D_deterrence)))
    """

    ARSON_INCITEMENT_KEYWORDS = [
        "burn down supreme court", "burn court", "burn supreme court", "albania supreme court",
        "albanian supreme court", "sc arson", "court arson", "subvert judiciary", "overthrow judiciary",
        "threaten judge", "arson threat", "storm supreme court", "attack high court",
        "lynch judge", "paralyze judiciary"
    ]

    STATUTORY_BREACH_KEYWORDS = [
        "bns 152", "bns section 152", "section 152", "sedition", "contempt of court", "constitutional contempt",
        "extra-judicial threat", "intimidate bench", "coercion of judges", "judicial blackmail"
    ]

    @classmethod
    def evaluate_judicial_subversion(
        cls,
        incitement_intensity: float = 0.0,
        statutory_breach_level: float = 0.0,
        deterrence_speed: float = 0.5,
        claims: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        incite = max(0.0, min(1.0, float(incitement_intensity)))
        breach = max(0.0, min(1.0, float(statutory_breach_level)))
        det = max(0.1, min(1.0, float(deterrence_speed)))

        matched_arson = []
        matched_breach = []

        if claims:
            for c in claims:
                txt = c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
                txt_l = txt.lower()
                for kw in cls.ARSON_INCITEMENT_KEYWORDS:
                    if kw in txt_l and kw not in matched_arson:
                        matched_arson.append(kw)
                for kw in cls.STATUTORY_BREACH_KEYWORDS:
                    if kw in txt_l and kw not in matched_breach:
                        matched_breach.append(kw)

            if matched_arson:
                incite = max(incite, min(1.0, 0.50 + 0.15 * len(matched_arson)))
                breach = max(breach, 0.70)
            if matched_breach:
                breach = max(breach, min(1.0, 0.40 + 0.15 * len(matched_breach)))

        score = round(min(1.0, max(0.0, 0.40 * incite + 0.35 * breach + 0.25 * (1.0 - det))), 4)

        if score >= 0.75:
            tier = "CRITICAL_JUDICIAL_INTIMIDATION"
            verdict = "HIGH_RISK_INSTITUTIONAL_CONTEMPT"
            rationale = (
                "Severe extra-judicial threat detected: Public incitement threatening physical violence, arson, or insurrection "
                "against constitutional benches (e.g. Albanian Supreme Court arson model). Mandates immediate BNS Section 152 deterrence."
            )
        elif score >= 0.50:
            tier = "ELEVATED_EXTRAJUDICIAL_INCITEMENT"
            verdict = "ELEVATED_CONTEMPT_RISK"
            rationale = (
                "Elevated institutional intimidation: Sustained political rhetoric seeking to delegitimize judicial independence "
                "via street mobilization and coercive narrative pressure."
            )
        elif score >= 0.25:
            tier = "MODERATE_RHETORICAL_FRICTION"
            verdict = "ROUTINE_LEGAL_CHALLENGE"
            rationale = "Constitutional dispute confined within standard appellate and procedural legal processes."
        else:
            tier = "STABLE_CONSTITUTIONAL_EQUILIBRIUM"
            verdict = "JUDICIAL_INTEGRITY_SECURE"
            rationale = "Judicial authority fully respected with active statutory enforcement and due process integrity."

        return {
            "judicial_subversion_score": score,
            "incitement_escalation_score": incite,
            "statutory_immunity_breach_score": breach,
            "deterrence_speed_score": det,
            "judicial_subversion_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "matched_arson_keywords": matched_arson,
            "matched_breach_keywords": matched_breach,
            "is_subversion_detected": score >= 0.50
        }


class CoercionPremiumSieve:
    """
    Phase 187: Asymmetric Coercion Premium & Democratic Subversion Sieve.
    Quantifies the institutional and economic leverage when organized minority street vetoes
    blockade critical national arterials (national highways, freight railway corridors, border crossings),
    imposing crushing deadweight friction on unorganized daily commuters and supply chains to extract
    executive policy concessions contrary to parliamentary legislative mandates.

    Formula:
        HoursLostNorm = min(1.0, daily_hours_lost / 8.0)
        CommutersNorm = min(1.0, impacted_commuters_millions / 5.0)
        EconomicFrictionCr = impacted_commuters_millions * 1e6 * daily_hours_lost * (hourly_wage_inr / 1e7)
        raw_cp = (0.45 * HoursLostNorm + 0.40 * CommutersNorm + 0.15 * foreign_amplification_factor) * (1.0 - 0.40 * statutory_enforcement_speed)
        CoercionPremiumScore = min(1.0, max(0.0, raw_cp))
    """

    MOB_COERCION_KEYWORDS = [
        "highway blockade", "rail roko", "chakka jam", "border blockade", "shaheen bagh",
        "singhu border", "tikri border", "arterial blockade", "street veto", "hostage city",
        "paralyze capital", "delhi blockade", "encircle capital", "tractor rally",
        "toll plaza capture", "freight disruption", "supply chain hostage"
    ]

    STATUTORY_SUBVERSION_KEYWORDS = [
        "bns 152", "bnss 163", "section 144", "subversion of parliament", "electoral mandate override",
        "minority veto", "mobocracy", "coercion premium", "asymmetric veto", "leveraged suffering"
    ]

    @classmethod
    def evaluate_coercion_premium(
        cls,
        impacted_commuters_millions: float = 0.5,
        daily_hours_lost: float = 2.0,
        hourly_wage_inr: float = 120.0,
        foreign_amplification_factor: float = 0.30,
        statutory_enforcement_speed: float = 0.50,
        claims: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        commuters = max(0.0, float(impacted_commuters_millions))
        hours = max(0.0, min(12.0, float(daily_hours_lost)))
        wage = max(20.0, float(hourly_wage_inr))
        foreign_amp = max(0.0, min(1.0, float(foreign_amplification_factor)))
        enforce_spd = max(0.0, min(1.0, float(statutory_enforcement_speed)))

        matched_mob = []
        matched_statutory = []

        if claims:
            for c in claims:
                txt = c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
                txt_l = txt.lower()
                for kw in cls.MOB_COERCION_KEYWORDS:
                    if kw in txt_l and kw not in matched_mob:
                        matched_mob.append(kw)
                for kw in cls.STATUTORY_SUBVERSION_KEYWORDS:
                    if kw in txt_l and kw not in matched_statutory:
                        matched_statutory.append(kw)

            if matched_mob:
                commuters = max(commuters, min(5.0, 1.0 + 0.5 * len(matched_mob)))
                hours = max(hours, min(8.0, 2.5 + 0.6 * len(matched_mob)))
            if matched_statutory:
                foreign_amp = min(1.0, foreign_amp + 0.15 * len(matched_statutory))
            if any(k in matched_mob for k in ["singhu border", "tikri border", "delhi blockade", "encircle capital"]):
                # Prolonged strategic siege posture
                commuters = max(commuters, 3.5)
                hours = max(hours, 4.5)
                foreign_amp = min(1.0, foreign_amp + 0.25)

        commuters_norm = min(1.0, commuters / 5.0)
        hours_norm = min(1.0, hours / 8.0)
        daily_friction_cr = round((commuters * 1_000_000.0 * hours * wage) / 10_000_000.0, 2)

        raw_cp = (0.45 * hours_norm + 0.40 * commuters_norm + 0.15 * foreign_amp) * (1.0 - 0.40 * enforce_spd)
        score = round(min(1.0, max(0.0, raw_cp)), 4)

        if score >= 0.75:
            tier = "CRITICAL_MOB_COERCION_PREMIUM"
            verdict = "DEMOCRATIC_MANDATE_PARALYZED"
            rationale = (
                f"Severe asymmetric coercion: Prolonged arterial highway/rail blockade impacting ~{commuters:.1f}M commuters "
                f"with ~{hours:.1f} hours lost daily (economic friction ₹{daily_friction_cr:.1f} Cr/day). Non-electoral street veto "
                f"threatens parliamentary supremacy. Mandates BNSS Section 163 / BNS 152 containment."
            )
        elif score >= 0.50:
            tier = "ELEVATED_STREET_VETO_PRESSURE"
            verdict = "LEVERAGED_CIVILIAN_SUFFERING"
            rationale = (
                f"Elevated coercion pressure: Strategic choke points occupied to manufacture commuter suffering "
                f"(₹{daily_friction_cr:.1f} Cr/day friction) and force executive policy concessions."
            )
        elif score >= 0.25:
            tier = "MODERATE_LOCALIZED_FRICTION"
            verdict = "CONTAINED_ARTERIAL_PROTEST"
            rationale = "Localized public demonstration with managed traffic diversions and baseline statutory law enforcement."
        else:
            tier = "CONSTITUTIONAL_ORDER_MAINTAINED"
            verdict = "UNHINDERED_PUBLIC_COMMUTE"
            rationale = "Transport corridors completely free; democratic dispute resolution channeled through legislative and judicial forums."

        return {
            "coercion_premium_score": score,
            "daily_economic_friction_inr_cr": daily_friction_cr,
            "impacted_commuters_millions": round(commuters, 2),
            "daily_hours_lost": round(hours, 2),
            "foreign_amplification_factor": round(foreign_amp, 2),
            "statutory_enforcement_speed": round(enforce_spd, 2),
            "coercion_premium_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "matched_mob_keywords": matched_mob,
            "matched_statutory_keywords": matched_statutory,
            "is_coercion_premium_active": score >= 0.50
        }


class CrowdCascadeThresholdSieve:
    """
    Phase 193: Granovetter Crowd Cascade & Critical Mass Threshold Sieve.
    Mathematically models non-linear crowd mobilization transitions using Mark Granovetter's
    Threshold Model of Collective Behavior (1978) combined with Erica Chenoweth's 3.5%
    empirical rule of non-violent regime coercion.

    Quantifies the tipping point where passive citizen populations transition into active
    street mobilization as individual participation thresholds are triggered by peer cascades
    and algorithmic digital virality.

    Formula:
        T_eff = max(0.005, T_mean * (1.0 - 0.50 * BackfireFactor))
        z = 3.5 * ((N_active / N_pop) / T_eff - 1.0) + 2.0 * DigitalVelocity
        P_cascade = 1 / (1 + exp(-z))
    """

    CASCADE_KEYWORDS = [
        "granovetter", "tipping point", "critical mass", "3.5 percent rule", "crowd cascade",
        "flash mob", "protest surge", "mass mobilization", "general strike", "million man march",
        "bandwagon effect", "spontaneous gathering", "street surge", "popular uprising"
    ]

    @classmethod
    def evaluate_cascade_threshold(
        cls,
        active_participants: float = 25_000.0,
        jurisdiction_population: float = 30_000_000.0,
        individual_threshold_mean: float = 0.05,
        digital_amplification_velocity: float = 0.30,
        repression_backfire_factor: float = 0.20,
        claims: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        import math
        active = max(0.0, float(active_participants))
        pop = max(100_000.0, float(jurisdiction_population))
        t_mean = max(0.001, min(1.0, float(individual_threshold_mean)))
        velocity = max(0.0, min(1.0, float(digital_amplification_velocity)))
        backfire = max(0.0, min(1.0, float(repression_backfire_factor)))

        matched_kws = []
        if claims:
            for c in claims:
                txt = c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
                txt_l = txt.lower()
                for kw in cls.CASCADE_KEYWORDS:
                    if kw in txt_l and kw not in matched_kws:
                        matched_kws.append(kw)

            if matched_kws:
                active = max(active, 100_000.0 + 50_000.0 * len(matched_kws))
                velocity = min(1.0, velocity + 0.15 * len(matched_kws))
            if any(k in matched_kws for k in ["critical mass", "3.5 percent rule", "million man march", "general strike"]):
                active = max(active, 1_050_000.0)
                velocity = min(1.0, velocity + 0.35)

        active_ratio = active / pop
        chenoweth_threshold = 0.035
        chenoweth_saturation = min(1.0, active_ratio / chenoweth_threshold)

        t_eff = max(0.005, t_mean * (1.0 - 0.50 * backfire))
        z = 3.5 * ((active_ratio / t_eff) - 1.0) + 2.0 * velocity
        cascade_prob = round(1.0 / (1.0 + math.exp(-z)), 4)
        headroom = round(max(0.0, 1.0 - cascade_prob), 4)

        if cascade_prob >= 0.75:
            tier = "IRREVERSIBLE_MASS_CASCADE"
            verdict = "CRITICAL_MASS_ACHIEVED"
            rationale = (
                f"Severe crowd contagion: Mobilization headcount (~{active:,.0f} / {active_ratio*100:.2f}%) has breached "
                f"the Granovetter tipping threshold and approached the Chenoweth 3.5% critical mass limit ({chenoweth_saturation*100:.1f}% saturation). "
                f"High risk of cascading institutional paralysis."
            )
        elif cascade_prob >= 0.50:
            tier = "ELEVATED_MOBILIZATION_SURGE"
            verdict = "THRESHOLD_CONTAGION_ACTIVE"
            rationale = (
                f"Elevated mobilization: Active participation (~{active:,.0f}) is triggering secondary peer thresholds "
                f"accelerated by social media virality (velocity index {velocity:.2f})."
            )
        elif cascade_prob >= 0.25:
            tier = "CONTAINED_PERIPHERAL_GATHERING"
            verdict = "SUB_CRITICAL_PROTEST"
            rationale = "Localized demonstration confined below the social tipping threshold; low probability of broad civic contagion."
        else:
            tier = "DORMANT_CROWD_EQUILIBRIUM"
            verdict = "STABLE_CIVIC_ORDER"
            rationale = "Civic equilibrium stable; individual mobilization thresholds remain unbreached."

        return {
            "cascade_probability": cascade_prob,
            "active_participants": round(active, 0),
            "jurisdiction_population": round(pop, 0),
            "active_population_ratio": round(active_ratio, 6),
            "effective_threshold": round(t_eff, 4),
            "digital_velocity": round(velocity, 2),
            "chenoweth_saturation_ratio": round(chenoweth_saturation, 4),
            "counter_mobilization_headroom": headroom,
            "cascade_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "matched_keywords": matched_kws,
            "is_tipping_reached": cascade_prob >= 0.50
        }


class StateMachiavellianSieve:
    """
    Phase 194: State Machiavellian Inaction & Safety Valve Sieve.
    Formalizes the state's strategic calculus of deliberate toleration and tactical hesitation.
    Synthesizes:
    1. Piven & Cloward (1977) Safety Valve: Permitting disruptive dissent to vent without structural policy concessions.
    2. Steven Wilkinson (2004, 'Votes and Violence'): Electoral incentives governing police intervention vs deliberate stand-down orders.
    3. IPS Vibhuti Narain Rai 24-hour rule: No communal riot or street siege persists past 24 hours without state hesitation or connivance.
    4. John Mueller (1970) Rally-Around-the-Flag: Disruption fatigue turning middle-class voters toward the incumbent executive.
    5. Brian Martin (2007) Dilution Tactics: Establishing inquiry committees ('churna') to dissolve protest momentum over time.

    Formula:
        FrictionDampener = min(1.0, DailyEconomicFrictionCr / 500.0)
        HesitationNorm = min(1.0, HesitationHours / 168.0)
        z = 0.35 * RallyGain + 0.30 * SafetyValve + 0.20 * HesitationNorm + CommFactor - 0.35 * FrictionDampener
        StateInactionScore = 1 / (1 + exp(-3.5 * (z - 0.25)))
    """

    STATE_INACTION_KEYWORDS = [
        "safety valve", "strategic inaction", "deliberate delay", "rally around the flag",
        "inquiry committee", "piven cloward", "wilkinson", "rai 24 hour rule", "churna",
        "stand down", "let them exhaust", "patience statecraft", "exhaustion strategy", "tactical hesitation"
    ]

    @classmethod
    def evaluate_state_inaction(
        cls,
        electoral_consolidation_gain: float = 0.40,
        safety_valve_utility: float = 0.35,
        daily_economic_friction_inr_cr: float = 50.0,
        administrative_hesitation_hours: float = 48.0,
        inquiry_commission_active: bool = False,
        claims: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        import math
        rally = max(0.0, min(1.0, float(electoral_consolidation_gain)))
        safety = max(0.0, min(1.0, float(safety_valve_utility)))
        friction = max(0.0, float(daily_economic_friction_inr_cr))
        hesitation = max(0.0, float(administrative_hesitation_hours))
        comm_active = bool(inquiry_commission_active)

        matched_kws = []
        if claims:
            for c in claims:
                txt = c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
                txt_l = txt.lower()
                for kw in cls.STATE_INACTION_KEYWORDS:
                    if kw in txt_l and kw not in matched_kws:
                        matched_kws.append(kw)

            if matched_kws:
                rally = min(1.0, rally + 0.15 * len(matched_kws))
                hesitation = max(hesitation, 72.0 + 24.0 * len(matched_kws))
            if any(k in matched_kws for k in ["inquiry committee", "churna"]):
                comm_active = True
            if any(k in matched_kws for k in ["let them exhaust", "patience statecraft", "rally around the flag"]):
                rally = max(rally, 0.75)
                safety = max(safety, 0.70)

        friction_dampener = min(1.0, friction / 500.0)
        hesitation_norm = min(1.0, hesitation / 168.0)
        comm_factor = 0.15 if comm_active else 0.0

        z = 0.35 * rally + 0.30 * safety + 0.20 * hesitation_norm + comm_factor - 0.35 * friction_dampener
        inaction_score = round(1.0 / (1.0 + math.exp(-3.5 * (z - 0.25))), 4)

        if inaction_score >= 0.75:
            tier = "CALCULATED_STRATEGIC_ATTRITION"
            verdict = "DELIBERATE_TOLERATION_FOR_RALLY"
            rationale = (
                f"Sovereign deliberate inaction confirmed: State withholds kinetic police dispersal (hesitation ~{hesitation:.0f} hrs, "
                f"Rai 24-hr threshold exceeded). Electoral calculus (Wilkinson model) projects voter backlash against disruption "
                f"yielding rally-around-the-flag consolidation (gain score {rally:.2f})."
            )
        elif inaction_score >= 0.50:
            tier = "MANAGED_SAFETY_VALVE_DISSIPATION"
            verdict = "PACIFICATION_VIA_PROCRASTINATION"
            rationale = (
                f"Managed venting: State utilizes Piven-Cloward safety-valve mechanism (utility {safety:.2f}) coupled with "
                f"inquiry committee procedures to dissipate agitational momentum without policy capitulation."
            )
        elif inaction_score >= 0.25:
            tier = "TACTICAL_POLICE_RESTRAINT"
            verdict = "DE_ESCALATION_POSTURE"
            rationale = "Temporary administrative restraint maintained to avoid civilian casualties while preparing statutory containment."
        else:
            tier = "IMMEDIATE_DECISIVE_ENFORCEMENT"
            verdict = "ZERO_TOLERANCE_STATUTORY_DISPERSAL"
            rationale = "High economic friction forces immediate administrative interdiction; zero political toleration for disruption."

        return {
            "state_inaction_score": inaction_score,
            "electoral_rally_gain": round(rally, 2),
            "safety_valve_utility": round(safety, 2),
            "administrative_hesitation_hours": round(hesitation, 1),
            "inquiry_commission_active": comm_active,
            "economic_friction_dampener": round(friction_dampener, 4),
            "state_inaction_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "matched_keywords": matched_kws,
            "is_deliberate_toleration": inaction_score >= 0.50
        }








```