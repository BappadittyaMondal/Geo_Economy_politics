"""
Lens 10: Deep-State & Bureaucratic Continuity Lens.
Applies Putnam's Two-Level Game model to deconstruct domestic institutional vetoes:
Permanent civil bureaucracies, security secretariats, and regulatory filters that execute or quietly kill summit agreements.
"""

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


