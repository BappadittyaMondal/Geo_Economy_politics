"""
geo_engine.verification.engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Master Evidence Intelligence & Fact Verification Engine.

Orchestrates atomic claim extraction, evidentiary triangulation, domain sieves,
and Richards Heuer's Analysis of Competing Hypotheses (ACH) to emit transparent,
evidence-grounded verdicts across all 7 standardized states:
1. VERIFIED
2. MOSTLY_ACCURATE
3. MISLEADING_OR_MISSING_CONTEXT
4. DISPUTED
5. UNSUPPORTED
6. FALSE
7. UNVERIFIABLE
"""

import hashlib
import time
from typing import List, Optional, Dict, Any
from geo_engine.verification.models import (
    VerificationVerdict, EvidenceDomain, AtomicClaim, EvidenceItem,
    ClaimVerificationResult, FactVerificationReport, ConfidenceMetadata
)
from geo_engine.verification.claim_extractor import AtomicClaimExtractor
from geo_engine.verification.triangulator import EvidentiaryTriangulator
from geo_engine.storage.event_store import EventStore
from geo_engine.core.temporal_guardrail import TemporalGuardrail


class FactVerificationEngine:
    """Master orchestrator for multi-domain evidence intelligence and claim auditing."""

    def __init__(self, event_store: Optional[EventStore] = None):
        self.store = event_store or EventStore()
        self.triangulator = EvidentiaryTriangulator(self.store)

    def verify_text(self, text: str) -> FactVerificationReport:
        """Audits unstructured text, extracting atomic claims and verifying each one."""
        claims = AtomicClaimExtractor.extract_claims(text)
        if not claims:
            # Fallback for short single proposition
            claims = [AtomicClaim(
                claim_id="CLAIM-SINGLE-01",
                raw_statement=text,
                extracted_proposition=text.strip(),
                domain=AtomicClaimExtractor.classify_domain(text)
            )]

        claim_results: List[ClaimVerificationResult] = []
        for claim in claims:
            res = self.verify_single_claim(claim)
            claim_results.append(res)

        # Synthesize consolidated master report
        total_claims = len(claim_results)
        verified_count = sum(1 for r in claim_results if r.verdict == VerificationVerdict.VERIFIED)
        mostly_count = sum(1 for r in claim_results if r.verdict == VerificationVerdict.MOSTLY_ACCURATE)
        false_count = sum(1 for r in claim_results if r.verdict == VerificationVerdict.FALSE)
        misleading_count = sum(1 for r in claim_results if r.verdict == VerificationVerdict.MISLEADING_OR_MISSING_CONTEXT)
        unverifiable_count = sum(1 for r in claim_results if r.verdict in (VerificationVerdict.UNVERIFIABLE, VerificationVerdict.UNSUPPORTED))

        # Overall verdict determination
        if false_count > 0:
            overall_verdict = VerificationVerdict.FALSE if false_count >= total_claims / 2 else VerificationVerdict.MISLEADING_OR_MISSING_CONTEXT
        elif misleading_count > 0:
            overall_verdict = VerificationVerdict.MISLEADING_OR_MISSING_CONTEXT
        elif verified_count == total_claims:
            overall_verdict = VerificationVerdict.VERIFIED
        elif verified_count + mostly_count >= total_claims / 2:
            overall_verdict = VerificationVerdict.MOSTLY_ACCURATE
        elif unverifiable_count == total_claims:
            overall_verdict = VerificationVerdict.UNVERIFIABLE
        else:
            overall_verdict = VerificationVerdict.DISPUTED

        avg_confidence = sum(r.confidence_score for r in claim_results) / max(1, total_claims)
        report_id = f"FVR-{hashlib.sha256(text.encode('utf-8')).hexdigest()[:10].upper()}"

        summary = (
            f"Analyzed {total_claims} claim(s). Verdict: {overall_verdict.value} "
            f"({verified_count} Verified, {mostly_count} Mostly Accurate, {misleading_count} Misleading, "
            f"{false_count} False, {unverifiable_count} Unsupported/Unverifiable). "
            f"Average Evidence Confidence: {avg_confidence:.2f} (Uncalibrated heuristic)."
        )

        overall_conf_label = "high" if avg_confidence >= 0.85 else "moderate" if avg_confidence >= 0.50 else "low"
        report_conf_meta = ConfidenceMetadata(
            value=round(avg_confidence, 3),
            label=overall_conf_label,
            calibration_status="not_calibrated",
            explanation="Uncalibrated composite heuristic derived from evidentiary tiers and source independence."
        )

        return FactVerificationReport(
            report_id=report_id,
            input_text=text,
            overall_verdict=overall_verdict,
            composite_confidence=round(avg_confidence, 3),
            confidence_metadata=report_conf_meta,
            total_claims_analyzed=total_claims,
            verified_claims_count=verified_count,
            false_claims_count=false_count,
            misleading_claims_count=misleading_count,
            unverifiable_claims_count=unverifiable_count,
            claim_results=claim_results,
            executive_summary=summary,
            reproducibility_hash=hashlib.sha256(f"{report_id}:{avg_confidence}".encode('utf-8')).hexdigest()[:16]
        )

    def verify_single_claim(self, claim: AtomicClaim) -> ClaimVerificationResult:
        """Verifies a single atomic claim using multi-pillar arbitration."""
        biases: List[str] = []

        # 1. Check for chronological feasibility / tenure anachronisms
        if claim.temporal_boundary:
            # Check for CEC tenure or constitutional appointments
            for official, title in [("gyanesh_kumar", "Chief Election Commissioner")]:
                if "gyanesh" in claim.raw_statement.lower() or "cec" in claim.raw_statement.lower():
                    tenure_check = TemporalGuardrail.verify_chronological_feasibility(
                        official, title, f"{claim.temporal_boundary}-01-01"
                    )
                    if not tenure_check.get("is_chronologically_feasible", True):
                        biases.append(f"ANACHRONISTIC_FABRICATION: {tenure_check.get('message', '')}")
                        return ClaimVerificationResult(
                            claim=claim,
                            verdict=VerificationVerdict.FALSE,
                            confidence_score=0.98,
                            verdict_rationale=f"Chronologically impossible. {tenure_check.get('message', '')}",
                            corroboration_score=0.0,
                            source_independence_index=1.0,
                            epistemic_tier_used="TIER_1_PRIMARY_ARCHIVE",
                            identified_biases_or_fallacies=biases
                        )

        # 2. Check for poisoned tail (premise true, conclusion conspiracy leap)
        if claim.has_poisoned_tail:
            biases.append("POISONED_TAIL: Factual premise coupled with unevidenced speculative conclusion.")
            return ClaimVerificationResult(
                claim=claim,
                verdict=VerificationVerdict.MISLEADING_OR_MISSING_CONTEXT,
                confidence_score=0.88,
                verdict_rationale="Statement connects an administrative premise to an unsubstantiated conspiratorial leap.",
                corroboration_score=0.40,
                source_independence_index=0.75,
                epistemic_tier_used="TIER_3_SOVEREIGN_REDLINES",
                identified_biases_or_fallacies=biases
            )

        # 3. Check for suppressed denominator
        if claim.has_suppressed_denominator:
            biases.append("SUPPRESSED_DENOMINATOR: Absolute count cited without disclosing total electorate or base.")
            return ClaimVerificationResult(
                claim=claim,
                verdict=VerificationVerdict.MISLEADING_OR_MISSING_CONTEXT,
                confidence_score=0.85,
                verdict_rationale="Statistical distortion: Raw counts are emphasized without total population or electorate baseline.",
                corroboration_score=0.50,
                source_independence_index=0.80,
                epistemic_tier_used="TIER_2_FINANCIAL",
                identified_biases_or_fallacies=biases
            )

        # 4. Triangulate with ground truth
        supporting, contradictory, independence = self.triangulator.triangulate_claim(claim)

        # 5. Evaluate evidence balance
        if contradictory:
            # Check if direct primary debunk exists
            if any(c.is_primary_source for c in contradictory):
                return ClaimVerificationResult(
                    claim=claim,
                    verdict=VerificationVerdict.FALSE,
                    confidence_score=0.95,
                    primary_evidence=supporting,
                    contradictory_evidence=contradictory,
                    verdict_rationale="Directly contradicted by verifiable primary record or documented debunk registry.",
                    corroboration_score=0.0,
                    source_independence_index=independence,
                    epistemic_tier_used="TIER_1_PRIMARY_ARCHIVE",
                    identified_biases_or_fallacies=biases
                )
            else:
                return ClaimVerificationResult(
                    claim=claim,
                    verdict=VerificationVerdict.DISPUTED,
                    confidence_score=0.75,
                    primary_evidence=supporting,
                    contradictory_evidence=contradictory,
                    verdict_rationale="Conflicting evidence exists across independent sources without settled consensus.",
                    corroboration_score=0.50,
                    source_independence_index=independence,
                    epistemic_tier_used="TIER_5_INDEPENDENT_MEDIA",
                    identified_biases_or_fallacies=biases
                )

        if supporting:
            # If supported by primary source with high independence
            has_primary = any(s.is_primary_source for s in supporting)
            verdict = VerificationVerdict.VERIFIED if (has_primary and independence >= 0.80) else VerificationVerdict.MOSTLY_ACCURATE
            conf = 0.95 if verdict == VerificationVerdict.VERIFIED else 0.85
            return ClaimVerificationResult(
                claim=claim,
                verdict=verdict,
                confidence_score=conf,
                primary_evidence=supporting,
                verdict_rationale="Corroborated by independent primary records and established empirical baselines.",
                corroboration_score=0.90,
                source_independence_index=independence,
                epistemic_tier_used="TIER_1_PRIMARY_ARCHIVE" if has_primary else "TIER_3_OFFICIAL_STATEMENT",
                identified_biases_or_fallacies=biases
            )

        # 6. Insufficient evidence / Unverifiable
        if claim.is_opinion_or_forecast:
            return ClaimVerificationResult(
                claim=claim,
                verdict=VerificationVerdict.UNVERIFIABLE,
                confidence_score=0.30,
                verdict_rationale="Forward-looking forecast or normative opinion cannot be empirically verified.",
                corroboration_score=0.0,
                source_independence_index=0.50,
                epistemic_tier_used="TIER_0_INSUFFICIENT_EVIDENCE",
                identified_biases_or_fallacies=["NORMATIVE_OPINION_OR_SPECULATIVE_FORECAST"]
            )

        return ClaimVerificationResult(
            claim=claim,
            verdict=VerificationVerdict.UNSUPPORTED,
            confidence_score=0.20,
            verdict_rationale="No traceable primary evidence, statutory record, or audited dataset found to corroborate claim.",
            corroboration_score=0.0,
            source_independence_index=0.50,
            epistemic_tier_used="TIER_0_INSUFFICIENT_EVIDENCE",
            identified_biases_or_fallacies=["ABSENCE_OF_PRIMARY_TRACEABILITY"]
        )
