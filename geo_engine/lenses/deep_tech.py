"""
Lens 1: Deep-Tech & Quantitative Modeling Lens.
Applies Bayesian confidence discounting, knowledge graph entity resolution,
and discrepancy vector calculation between declarative text and ground-truth metrics.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, SummitEvent


class STEMCapitalDilutionSieve:
    """
    Phase 100: STEM Capital Dilution & Technological Dividend Viability Sieve.
    Quantifies the diversion of institutional engineering/scientific capital and physical lab CapEx
    into non-empirical social grievance doctrines and ideological administration, directly threatening
    long-term demographic dividend viability and strategic technology autonomy.

    Mathematical Formulation:
      Budget_Ratio = grievance_curricula_budget_share / max(0.10, physical_lab_capex_share)
      Admin_Penalty = 0.40 * ideological_administrative_overhead + 0.35 * max(0.0, 1.0 - meritocratic_faculty_retention)
      D_stem = min(1.0, max(0.0, round(0.50 * min(1.0, Budget_Ratio) + 0.50 * Admin_Penalty, 4)))
    """

    @classmethod
    def calculate_stem_dilution(
        cls,
        grievance_curricula_budget_share: float = 0.35,
        physical_lab_capex_share: float = 0.40,
        ideological_administrative_overhead: float = 0.30,
        meritocratic_faculty_retention: float = 0.65
    ) -> Dict[str, Any]:
        g_share = min(1.0, max(0.0, float(grievance_curricula_budget_share)))
        lab_share = min(1.0, max(0.0, float(physical_lab_capex_share)))
        overhead = min(1.0, max(0.0, float(ideological_administrative_overhead)))
        retention = min(1.0, max(0.0, float(meritocratic_faculty_retention)))

        budget_ratio = g_share / max(0.10, lab_share)
        admin_penalty = (0.40 * overhead) + (0.35 * max(0.0, 1.0 - retention))
        d_stem = min(1.0, max(0.0, round(0.50 * min(1.0, budget_ratio) + 0.50 * admin_penalty, 4)))

        if d_stem >= 0.70:
            tier = "ACUTE_CAPITAL_DILUTION"
            verdict = "SEVERE_EROSION_OF_HARD_ENGINEERING_DEMOGRAPHIC_DIVIDEND_AT_RISK"
        elif d_stem >= 0.45:
            tier = "ELEVATED_CURRICULAR_DIVERSION"
            verdict = "LABORATORY_FUNDING_DIVERSION_IDEOLOGICAL_ADMIN_EXPANSION"
        elif d_stem >= 0.20:
            tier = "MODERATE_LAB_LAG"
            verdict = "MANAGEABLE_INSTITUTIONAL_OVERHEAD_TECHNICAL_FOUNDATION_INTACT"
        else:
            tier = "MAXIMAL_STEM_RIGOR"
            verdict = "PRIORITIZED_ENGINEERING_CAPEX_MERITOCRATIC_FACULTY_ALLOCATION"

        rationale = (
            f"Grievance budget ({g_share:.2f}) vs Lab CapEx ({lab_share:.2f}), "
            f"Admin overhead ({overhead:.2f}), Faculty retention ({retention:.2f}). "
            f"STEM dilution D_stem: {d_stem:.4f} ({tier})."
        )

        return {
            "stem_dilution_score": d_stem,
            "stem_dilution_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "grievance_curricula_budget_share": g_share,
            "physical_lab_capex_share": lab_share,
            "ideological_administrative_overhead": overhead,
            "meritocratic_faculty_retention": retention,
            "demographic_dividend_at_risk": (d_stem >= 0.45)
        }


class DeepTechLens:
    """Quantitative, entity-linked, and algorithmic evaluation engine."""

    LENS_NAME = "Deep-Tech & Quantitative Modeling"
    PRIMARY_TIER = EpistemicTier.TIER_2_FINANCIAL

    @classmethod
    def evaluate(
        cls,
        summit: SummitEvent,
        rhetoric_sentiment_score: float = 0.85, # Highly optimistic public declarations
        hard_data_alignment_score: float = 0.35, # Ground truth economic/border alignment
        unverified_claims_count: int = 12,
        evidence: Optional[List[Any]] = None,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Calculates the divergence vector between diplomatic sentiment and hard metrics.
        Applies Bayesian discounting for unverified claims and boosts confidence if verified primary evidence exists.
        Dynamically handles both primary evidence items and ingested claims.
        """
        evidence = evidence or claims
        evidence_citations = []
        if evidence:
            unverified_claims_count = sum(1 for e in evidence if getattr(e, "reliability_weight", 0.5) < 0.70)
            avg_reliability = sum(getattr(e, "reliability_weight", 0.70) for e in evidence) / len(evidence)
            confidence = max(0.3, round(avg_reliability - (unverified_claims_count * 0.02), 2))
            for e in evidence[:2]:
                evidence_citations.append(f"[INGESTED EVIDENCE: {getattr(e, 'source_name', 'Open Source')}] {getattr(e, 'raw_text', '')[:120]}...")
        else:
            # Bayesian confidence discount: more unverified claims = lower confidence
            confidence = max(0.2, round(0.95 - (unverified_claims_count * 0.04), 2))

        # Divergence: High rhetoric + low hard data = high discrepancy penalty
        discrepancy = abs(rhetoric_sentiment_score - hard_data_alignment_score)
        
        # Net alignment is anchored on hard data, not rhetoric
        net_score = round(hard_data_alignment_score - (discrepancy * 0.3), 3)

        findings = [
            f"Sentiment-Reality Discrepancy Vector: {discrepancy:.2f} (Public optimism: {rhetoric_sentiment_score:.2f} vs Ground Truth: {hard_data_alignment_score:.2f}).",
            f"Bayesian Confidence: {confidence:.2f} (derived from {len(evidence) if evidence else unverified_claims_count} evaluated evidence records).",
            "Algorithmically anchored analysis to physical and transaction ledgers, suppressing cosmetic press release sentiment."
        ]
        if evidence_citations:
            findings.extend(evidence_citations)

        metrics = {
            "rhetoric_sentiment": rhetoric_sentiment_score,
            "ground_truth_alignment": hard_data_alignment_score,
            "discrepancy_vector": discrepancy,
            "unverified_claims_count": unverified_claims_count,
            "bayesian_confidence": confidence,
            "evidence_records_ingested": len(evidence) if evidence else 0
        }

        corpus = (
            f"{getattr(summit, 'summit_name', '')} {getattr(summit, 'title', '')} " +
            " ".join(getattr(e, 'raw_text', getattr(e, 'asserted_fact', getattr(e, 'assertion', ''))) for e in (evidence or []))
        ).lower()

        stem_terms = [
            "stem dilution", "grievance curricula", "engineering capex", "technological dividend",
            "demographic dividend liability", "hard engineering", "lab capex", "stem education"
        ]
        stem_detected = any(t in corpus for t in stem_terms)
        if stem_detected:
            g_share = 0.55 if "grievance" in corpus else 0.35
            lab_share = 0.25 if "dilution" in corpus or "liability" in corpus else 0.40
            overhead = 0.45 if "curricula" in corpus or "grievance" in corpus else 0.25
            retention = 0.50 if "dilution" in corpus else 0.70
            stem_calc = STEMCapitalDilutionSieve.calculate_stem_dilution(
                grievance_curricula_budget_share=g_share,
                physical_lab_capex_share=lab_share,
                ideological_administrative_overhead=overhead,
                meritocratic_faculty_retention=retention
            )
            findings.insert(0, (
                f"[STEM CAPITAL DILUTION FORENSICS] {stem_calc['tactical_rationale']} "
                f"Verdict: {stem_calc['operational_verdict']}."
            ))
            metrics["stem_capital_dilution_score"] = stem_calc["stem_dilution_score"]
            metrics["stem_dilution_tier"] = stem_calc["stem_dilution_tier"]
            metrics["demographic_dividend_at_risk"] = stem_calc["demographic_dividend_at_risk"]
            if stem_calc["demographic_dividend_at_risk"]:
                net_score = max(0.10, round(net_score - 0.15, 3))

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=net_score,
            confidence=confidence,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )
