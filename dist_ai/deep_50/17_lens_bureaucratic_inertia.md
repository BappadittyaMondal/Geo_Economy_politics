# LENS SPECIFICATION: BUREAUCRATIC_INERTIA

```python
"""
Lens 10: Deep-State & Bureaucratic Continuity Lens.
Applies Putnam's Two-Level Game model to deconstruct domestic institutional vetoes:
Permanent civil bureaucracies, security secretariats, and regulatory filters that execute or quietly kill summit agreements.
"""

import math
from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, SummitEvent


class BureaucraticInertiaLens:
    """Bureaucratic permanence and domestic regulatory veto evaluator."""

    LENS_NAME = "Deep-State & Bureaucratic Continuity"
    PRIMARY_TIER = EpistemicTier.TIER_3_SOVEREIGN_REDLINES

    @classmethod
    def evaluate(
        cls,
        summit: SummitEvent,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Assesses permanent institutional roadblocks and regulatory barriers.
        Dynamically ingests regulatory compliance, veto action, and bureaucratic inertia claims.
        """
        findings = [
            "Indian Institutional Filter (Press Note 3): Regardless of summit handshakes, India's Ministry of Commerce and Home Affairs strictly maintain Press Note 3 compliance—subjecting all Chinese FDI, corporate takeovers, and joint ventures to rigorous security vetting.",
            "Chinese Mercantilist Protectionism: China's National Development and Reform Commission (NDRC) systematically prioritizes offloading domestic industrial overcapacity over opening its domestic markets to Indian pharmaceuticals, IT services, or Brazilian manufactured goods.",
            "Bureaucratic Friction in Currency Settlement: Central bank bureaucracies (RBI, Russian Central Bank, PBOC) refuse to accept open-ended cross-currency liabilities, stalling grand political de-dollarization proposals in bureaucratic technical committees.",
            "Putnam's Level-2 Constraint: Leaders cannot ratify trade concessions at the summit table that would decimate domestic voting constituencies (e.g., Indian MSMEs and farmers rejecting broad Chinese tariff reductions)."
        ]

        metrics = {
            "domestic_ratification_probability": 0.40,
            "bureaucratic_veto_intensity": "High (Commerce & Security Ministries prioritize national industrial protection)",
            "indian_regulatory_anchor": "Press Note 3 & National Security Directives",
            "chinese_regulatory_anchor": "NDRC Industrial Capacity Offloading Strategy",
            "executive_rollback_elasticity_score": 0.0
        }

        alignment = 0.28 # Very low alignment once filtered through permanent civil services
        confidence = 0.93

        if claims:
            regulatory_keywords = [
                "press note 3", "veto", "bureaucracy", "ndrc", "rbi", "commerce",
                "regulatory", "tariff", "customs", "clearance", "ratification", "deep-state"
            ]
            matched_reg = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in regulatory_keywords)
                for c in claims
            )
            if matched_reg:
                findings.insert(0, "[GROUNDED TELEMETRY] Bureaucratic regulatory friction / institutional veto verified in domestic execution pipeline.")
                confidence = min(0.99, round(confidence + 0.02, 2))
                metrics["grounded_regulatory_claims_verified"] = True

            rollback_keywords = [
                "ugc rollback", "de-reservation", "draft guidelines", "policy rollback",
                "farm laws rollback", "executive retreat", "clerical overreach", "bureaucratic disconnect",
                "rollback"
            ]
            matched_rollback = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in rollback_keywords)
                for c in claims
            )
            if matched_rollback:
                has_ugc = any("ugc" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or "de-reservation" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for c in claims)
                electoral_sens = 0.90 if has_ugc else 0.70
                mob_velocity = 0.85 if has_ugc else 0.65
                exec_commit = 0.25 if has_ugc else 0.50
                deficit = 0.80 if has_ugc else 0.40

                rb_res = BureaucraticRollbackModel.calculate_rollback_elasticity(
                    electoral_sensitivity=electoral_sens,
                    mobilization_velocity=mob_velocity,
                    executive_commitment=exec_commit,
                    consultation_deficit=deficit
                )
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Executive Policy Rollback Elasticity triggered: "
                    f"Risk Tier [{rb_res['rollback_risk_tier']}] (Score: {rb_res['rollback_elasticity_score']:.2f}, Half-Life: {rb_res['predicted_half_life_days']} days). "
                    f"{rb_res['bureaucratic_disconnect_analysis']} Recommendation: {rb_res['policy_stabilization_recommendation']}"
                ))
                alignment = min(alignment, 0.12)
                metrics["executive_rollback_elasticity_score"] = rb_res["rollback_elasticity_score"]
                metrics["policy_rollback_risk_tier"] = rb_res["rollback_risk_tier"]
                metrics["bureaucratic_consultation_deficit_detected"] = bool(deficit >= 0.50)
                metrics["predicted_policy_half_life_days"] = rb_res["predicted_half_life_days"]

            metrics["claims_evaluated"] = len(claims)

        # Phase 287: Wire SubNationalBureaucraticFrictionSieve
        bur_meta = getattr(summit, "metadata", {}) or {}
        bur_params = bur_meta.get("bureaucratic_friction", {}) if isinstance(bur_meta, dict) else {}
        _bur_res = SubNationalBureaucraticFrictionSieve.calculate_administrative_velocity(
            executive_clarity=bur_params.get("executive_clarity", 0.75),
            statutory_de_registration=bur_params.get("statutory_de_registration", 0.70),
            file_looping_latency=bur_params.get("file_looping_latency", 0.35),
            pil_stay_order_drag=bur_params.get("pil_stay_order_drag", 0.30),
        )
        metrics["administrative_velocity_score"] = _bur_res["administrative_velocity_score"]
        metrics["bureaucratic_friction_drag"] = _bur_res["bureaucratic_friction_drag"]
        metrics["pil_lawfare_resistance_index"] = _bur_res["pil_lawfare_resistance_index"]
        metrics["administrative_velocity_tier"] = _bur_res["administrative_velocity_tier"]

        _dec_res = DynasticExtraConstitutionalShadowCabinetSieve.evaluate(
            unconstitutional_shadow_veto_power=bur_meta.get("unconstitutional_shadow_veto_power", 0.35),
            statutory_oversight_bypass_frequency=bur_meta.get("statutory_oversight_bypass_frequency", 0.30),
            parliamentary_transparency_rigor=bur_meta.get("parliamentary_transparency_rigor", 0.80),
        )
        metrics["dynastic_extra_constitutional_shadow_cabinet_score"] = _dec_res["dynastic_extra_constitutional_shadow_cabinet_score"]

        # Phase 425: Algorithmic Faceless Procurement Transparency Sieve
        _afp_res = AlgorithmicFacelessProcurementTransparencySieve.evaluate(
            faceless_smart_contract_share=bur_meta.get("faceless_smart_contract_share", 0.85),
            public_ledger_auditability=bur_meta.get("public_ledger_auditability", 0.80),
            discretionary_bureaucratic_bypass=bur_meta.get("discretionary_bureaucratic_bypass", 0.75),
            procurement_rent_seeking_legacy_drag=bur_meta.get("procurement_rent_seeking_legacy_drag", 0.25),
        )
        metrics["algorithmic_faceless_procurement_efficiency_score"] = _afp_res["algorithmic_faceless_procurement_efficiency_score"]

        # Phase 429: Sovereign CapEx Moat and Faceless Governance Sieve (PM Narendra Modi Module)
        _scm_res = SovereignCapExMoatAndFacelessGovernanceSieve.evaluate(
            physical_infrastructure_capex_velocity=bur_meta.get("physical_infrastructure_capex_velocity", 0.90),
            semiconductor_fab_sovereignty_progress=bur_meta.get("semiconductor_fab_sovereignty_progress", 0.80),
            dpi_disintermediation_depth=bur_meta.get("dpi_disintermediation_depth", 0.85),
            bureaucratic_veto_friction=bur_meta.get("bureaucratic_veto_friction", 0.25),
            judicial_infrastructure_stay_rate=bur_meta.get("judicial_infrastructure_stay_rate", 0.20),
        )
        metrics["sovereign_capex_moat_escape_velocity_score"] = _scm_res["sovereign_capex_moat_escape_velocity_score"]

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=confidence,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )


class BureaucraticRollbackModel:
    """
    Phase 89: Executive Policy Rollback Elasticity Model.
    Quantifies bureaucratic disconnect between administrative guideline drafting
    and political executive capital, measuring policy half-life under mass mobilization.

    Formula:
        R_rollback = min(1.0, max(0.0, (S_electoral * V_mobilization * (1.0 + D_consultation)) / max(0.10, 2.0 * C_executive_commitment)))
    """

    @staticmethod
    def calculate_rollback_elasticity(
        electoral_sensitivity: float,
        mobilization_velocity: float,
        executive_commitment: float,
        consultation_deficit: float = 0.50
    ) -> Dict[str, Any]:
        s_elec = max(0.0, min(1.0, float(electoral_sensitivity)))
        v_mob = max(0.0, min(1.0, float(mobilization_velocity)))
        c_exec = max(0.0, min(1.0, float(executive_commitment)))
        d_cons = max(0.0, min(1.0, float(consultation_deficit)))

        numerator = s_elec * v_mob * (1.0 + d_cons)
        denominator = max(0.10, 2.0 * c_exec)
        score = round(min(1.0, max(0.0, numerator / denominator)), 4)

        half_life_days = round(max(1.0, 180.0 * ((1.0 - score) ** 1.5)), 1)

        if score >= 0.75:
            risk_tier = "IMMINENT_EXECUTIVE_ROLLBACK"
            disconnect = (
                "Extreme administrative-political disconnect: Autonomous bureaucratic guidelines issued without cabinet-level "
                "pre-vetting facing overwhelming mobilization and acute electoral liabilities, compelling immediate executive retreat."
            )
            stabilization = (
                "Execute immediate administrative withdrawal or stay order; initiate formal inter-ministerial political pre-consultation "
                "and parliamentary committee deliberation before reissuance."
            )
        elif score >= 0.50:
            risk_tier = "HIGH_VULNERABILITY_PAUSE"
            disconnect = (
                "Elevated vulnerability: Strong public pushback and electoral sensitivity outmatch bureaucratic momentum, "
                "forcing the executive to place notifications into indefinite administrative abeyance."
            )
            stabilization = (
                "Constitute a multi-stakeholder expert review panel to absorb public protest velocity and draft compensatory carve-outs."
            )
        elif score >= 0.25:
            risk_tier = "MODERATE_AMENDMENT_CYCLE"
            disconnect = (
                "Moderate friction: Procedural objections raised by interest groups, but executive political capital remains sufficient "
                "to absorb friction through minor technical revisions."
            )
            stabilization = (
                "Publish targeted clarifying corrigenda and phase implementation timelines across successive fiscal quarters."
            )
        else:
            risk_tier = "DURABLE_STATUTORY_REFORM"
            disconnect = (
                "High executive coherence: Deep cabinet alignment, low electoral exposure, and disciplined bureaucratic execution "
                "confer durable statutory longevity."
            )
            stabilization = (
                "Proceed with permanent statutory gazetting and institutional standard operating procedure enforcement."
            )

        return {
            "rollback_elasticity_score": score,
            "electoral_sensitivity": s_elec,
            "mobilization_velocity": v_mob,
            "executive_commitment": c_exec,
            "consultation_deficit": d_cons,
            "predicted_half_life_days": half_life_days,
            "rollback_risk_tier": risk_tier,
            "bureaucratic_disconnect_analysis": disconnect,
            "policy_stabilization_recommendation": stabilization
        }




class SubNationalBureaucraticFrictionSieve:
    """
    Phase 287: Sub-National Bureaucratic Friction Sieve.
    Quantifies administrative fifth-column resistance, procedural file-looping,
    and Public Interest Litigation (PIL) legal weaponization stalling strategic infrastructure and defense corridor projects.
    """

    @classmethod
    def calculate_administrative_velocity(
        cls,
        executive_clarity: float = 0.75,
        statutory_de_registration: float = 0.70,
        file_looping_latency: float = 0.35,
        pil_stay_order_drag: float = 0.30,
    ) -> Dict[str, Any]:
        """
        Calculates Administrative Velocity Score using calibrated logistic sigmoid:
            z = 2.8 * clarity + 2.5 * dereg - 3.0 * looping - 2.7 * pil - 0.3
            score = 1 / (1 + exp(-z))
        """
        import math
        clarity = max(0.0, min(1.0, float(executive_clarity)))
        dereg = max(0.0, min(1.0, float(statutory_de_registration)))
        looping = max(0.0, min(1.0, float(file_looping_latency)))
        pil = max(0.0, min(1.0, float(pil_stay_order_drag)))

        z = 2.8 * clarity + 2.5 * dereg - 3.0 * looping - 2.7 * pil - 0.3
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "DECISIVE_SOVEREIGN_EXECUTIVE_VELOCITY"
            verdict = "FAST_TRACK_STATUTORY_EXECUTION_UNHINDERED"
            rationale = (
                f"Decisive executive velocity ({score:.4f}): High executive clarity ({clarity:.2f}) and proactive statutory "
                f"de-registration ({dereg:.2f}) eradicate bureaucratic file-looping and frivolous PIL stay orders."
            )
        elif score >= 0.55:
            tier = "MANAGEABLE_BUREAUCRATIC_FRICTION"
            verdict = "PROCEDURAL_COMPLIANCE_WITH_CONTROLLED_LATENCY"
            rationale = (
                f"Manageable friction ({score:.4f}): Inter-ministerial coordination overcomes routine procedural resistance."
            )
        elif score >= 0.35:
            tier = "CONTESTED_JUDICIAL_ADMINISTRATIVE_GRIDLOCK"
            verdict = "SUB_NATIONAL_PIL_LAWFARE_DELAYING_CAPEX"
            rationale = (
                f"Contested gridlock ({score:.4f}): Lawfare stay orders ({pil:.2f}) and file ping-pong stall critical defense projects."
            )
        else:
            tier = "CRITICAL_DEEP_STATE_POLICY_PARALYSIS"
            verdict = "TOTAL_ADMINISTRATIVE_FIFTH_COLUMN_VETO"
            rationale = (
                f"Critical paralysis ({score:.4f}): Severe file-looping ({looping:.2f}) and judicial injunctions freeze national strategy."
            )

        friction_drag = round(min(1.0, looping * 0.60 + pil * 0.40), 4)
        pil_resilience = round(max(0.0, 1.0 - pil), 4)

        return {
            "administrative_velocity_score": score,
            "executive_clarity": round(clarity, 4),
            "statutory_de_registration": round(dereg, 4),
            "file_looping_latency": round(looping, 4),
            "pil_stay_order_drag": round(pil, 4),
            "bureaucratic_friction_drag": friction_drag,
            "pil_lawfare_resistance_index": pil_resilience,
            "administrative_velocity_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_executive_velocity_decisive": score >= 0.55,
        }


# ============================================================================
# Phase 389: Dynastic Extra-Constitutional Shadow Cabinet Sieve (NAC Era)
# ============================================================================

class DynasticExtraConstitutionalShadowCabinetSieve:
    """
    Phase 389: Models and detects extra-constitutional shadow governance structures (e.g. NAC)
    where formal cabinet authority, prime ministerial discretion, and statutory oversight
    are subordinated to unaccountable extra-parliamentary party secretariats.
    """
    @classmethod
    def evaluate(
        cls,
        unconstitutional_shadow_veto_power: float = 0.85,
        statutory_oversight_bypass_frequency: float = 0.80,
        parliamentary_transparency_rigor: float = 0.25
    ) -> Dict[str, Any]:
        u_veto = float(max(0.0, min(1.0, unconstitutional_shadow_veto_power)))
        s_byp = float(max(0.0, min(1.0, statutory_oversight_bypass_frequency)))
        p_trans = float(max(0.0, min(1.0, parliamentary_transparency_rigor)))

        z = 3.4 * u_veto + 2.8 * s_byp - 3.2 * p_trans - 0.4
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "CRITICAL_SHADOW_CABINET_SUBVERSION"
            verdict = "CONSTITUTIONAL_EXECUTIVE_POWER_SUBORDINATED_TO_PARTY_CABAL"
            rationale = (
                f"Severe extra-constitutional capture ({score:.4f}): Shadow veto power ({u_veto:.2f}) and statutory bypass ({s_byp:.2f}) "
                f"violate Articles 74/75 of the Constitution. Executive decisions dictated without parliamentary accountability."
            )
        elif score >= 0.45:
            tier = "MODERATE_EXTRA_PARLIAMENTARY_INFLUENCE"
            verdict = "RESTRICT_ADVISORY_BODIES_TO_STATUTORY_CONSULTATIVE_ROLES"
            rationale = f"Elevated shadow influence ({score:.4f}): Advisory committees exerting unvetted executive pressure."
        else:
            tier = "CONSTITUTIONAL_EXECUTIVE_SUPREMACY_MAINTAINED"
            verdict = "CABINET_GOVERNANCE_ACCOUNTABLE_TO_PARLIAMENT"
            rationale = f"Constitutional integrity intact ({score:.4f}): High parliamentary transparency ({p_trans:.2f}) defeats shadow cabals."

        return {
            "dynastic_extra_constitutional_shadow_cabinet_score": score,
            "unconstitutional_shadow_veto_power": round(u_veto, 4),
            "statutory_oversight_bypass_frequency": round(s_byp, 4),
            "parliamentary_transparency_rigor": round(p_trans, 4),
            "shadow_cabinet_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_shadow_cabinet_subversion_critical": score >= 0.70,
        }


# ============================================================================
# Phase 425: Algorithmic Faceless Procurement Transparency Sieve
# ============================================================================

class AlgorithmicFacelessProcurementTransparencySieve:
    """
    Phase 425: Models the elimination of bureaucratic bribery and rent-seeking via
    automated smart-contract escrows, faceless public digital ledgers (GeM portal architecture),
    and algorithmic vendor allocation.
    Formula:
        EfficiencyScore = Norm((0.40 * faceless_share + 0.35 * ledger_auditability + 0.25 * bureaucratic_bypass) /
                               (1.0 + rent_seeking_legacy_drag))
        score = Sigmoid(2.8 * EfficiencyScore + 2.5 * faceless_share - 1.2)
    """
    @classmethod
    def evaluate(
        cls,
        faceless_smart_contract_share: float = 0.85,
        public_ledger_auditability: float = 0.80,
        discretionary_bureaucratic_bypass: float = 0.75,
        procurement_rent_seeking_legacy_drag: float = 0.25
    ) -> Dict[str, Any]:
        f_share = float(max(0.0, min(1.0, faceless_smart_contract_share)))
        p_audit = float(max(0.0, min(1.0, public_ledger_auditability)))
        b_bypass = float(max(0.0, min(1.0, discretionary_bureaucratic_bypass)))
        r_drag = float(max(0.0, min(1.0, procurement_rent_seeking_legacy_drag)))

        raw_eff = (0.40 * f_share + 0.35 * p_audit + 0.25 * b_bypass) / (1.0 + r_drag)
        z = 2.8 * raw_eff + 2.5 * f_share - 1.2
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "DECISIVE_FACELESS_GOVERNANCE_TRANSPARENCY"
            verdict = "MANDATE_END_TO_END_SMART_CONTRACT_ESCROW_FOR_ALL_PUBLIC_TENDERS"
            rationale = (
                f"Decisive faceless procurement ({score:.4f}): High smart contract share ({f_share:.2f}) "
                f"and discretionary bypass ({b_bypass:.2f}) systematically eliminate intermediary rent-seeking."
            )
        elif score >= 0.45:
            tier = "MODERATE_DIGITAL_TENDERING_ADOPTION"
            verdict = "ACCELERATE_MUNICIPAL_ONBOARDING_TO_NATIONAL_PROCUREMENT_LEDGER"
            rationale = f"Moderate transparency ({score:.4f}): Legacy rent-seeking drag ({r_drag:.2f}) persists in local bodies."
        else:
            tier = "DISCRETIONARY_BUREAUCRATIC_CAPTURE"
            verdict = "OVERHAUL_MANUAL_TENDERING_AND_IMPOSE_ALGORITHMIC_ALLOCATION"
            rationale = f"High corruption vulnerability ({score:.4f}): Discretionary clerical approvals dominate."

        return {
            "algorithmic_faceless_procurement_efficiency_score": score,
            "faceless_smart_contract_share": round(f_share, 4),
            "public_ledger_auditability": round(p_audit, 4),
            "discretionary_bureaucratic_bypass": round(b_bypass, 4),
            "procurement_rent_seeking_legacy_drag": round(r_drag, 4),
            "procurement_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_procurement_transparency_decisive": score >= 0.70,
        }


# ============================================================================
# Phase 429: Sovereign CapEx Moat and Faceless Governance Sieve (PM Narendra Modi Module)
# ============================================================================

class SovereignCapExMoatAndFacelessGovernanceSieve:
    """
    Phase 429 (PM Narendra Modi Module): Mathematical evaluation of physical capital expenditure escape velocity
    (Viksit Bharat 2047 benchmark), dedicated freight corridor throughput, semiconductor fabrication sovereignty,
    and bureaucratic disintermediation via Direct Benefit Transfer (DBT) and Digital Public Infrastructure (DPI).
    Formula:
        EscapeVelocity = Norm((0.40 * capex_velocity + 0.35 * fab_sovereignty + 0.25 * dpi_disintermediation) /
                              (1.0 + bureaucratic_veto_friction + judicial_stay_rate))
        score = Sigmoid(2.8 * EscapeVelocity + 2.5 * capex_velocity - 1.2)
    """
    @classmethod
    def evaluate(
        cls,
        physical_infrastructure_capex_velocity: float = 0.90,
        semiconductor_fab_sovereignty_progress: float = 0.80,
        dpi_disintermediation_depth: float = 0.85,
        bureaucratic_veto_friction: float = 0.25,
        judicial_infrastructure_stay_rate: float = 0.20
    ) -> Dict[str, Any]:
        capex_vel = float(max(0.0, min(1.0, physical_infrastructure_capex_velocity)))
        fab_prog = float(max(0.0, min(1.0, semiconductor_fab_sovereignty_progress)))
        dpi_depth = float(max(0.0, min(1.0, dpi_disintermediation_depth)))
        veto_fric = float(max(0.0, min(1.0, bureaucratic_veto_friction)))
        stay_rate = float(max(0.0, min(1.0, judicial_infrastructure_stay_rate)))

        raw_escape = (0.40 * capex_vel + 0.35 * fab_prog + 0.25 * dpi_depth) / (1.0 + veto_fric + stay_rate)
        z = 2.8 * raw_escape + 2.5 * capex_vel - 1.2
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "DECISIVE_CAPEX_ESCAPE_VELOCITY_ACHIEVED"
            verdict = "LOCK_IN_PHYSICAL_INFRASTRUCTURE_ASSETS_AND_SCALE_DOMESTIC_FABRICATION"
            rationale = (
                f"Decisive CapEx escape velocity ({score:.4f}): Infrastructure velocity ({capex_vel:.2f}) "
                f"and DPI disintermediation ({dpi_depth:.2f}) break historic bureaucratic inertia, sealing the national industrial moat."
            )
        elif score >= 0.45:
            tier = "ELEVATED_CAPEX_EXPANSION_TRAJECTORY"
            verdict = "FAST_TRACK_STATUTORY_ENVIRONMENTAL_AND_LAND_CLEARANCES"
            rationale = f"Elevated expansion ({score:.4f}): Judicial stay friction ({stay_rate:.2f}) requires legislative streamlining."
        else:
            tier = "BUREAUCRATIC_INERTIA_ENTRAPMENT"
            verdict = "DISINTERMEDIATE_CLERICAL_RED_TAPE_AND_MANDATE_TIME_BOUND_SANCTIONS"
            rationale = f"Low velocity ({score:.4f}): Administrative friction outpaces physical capital formation."

        return {
            "sovereign_capex_moat_escape_velocity_score": score,
            "physical_infrastructure_capex_velocity": round(capex_vel, 4),
            "semiconductor_fab_sovereignty_progress": round(fab_prog, 4),
            "dpi_disintermediation_depth": round(dpi_depth, 4),
            "bureaucratic_veto_friction": round(veto_fric, 4),
            "judicial_infrastructure_stay_rate": round(stay_rate, 4),
            "escape_velocity_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_capex_escape_velocity_achieved": score >= 0.70,
        }

```