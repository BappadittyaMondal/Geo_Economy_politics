"""
geo_engine.verification.learner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Autonomous Safe Self-Learning & Governed Quarantine Ingestion Pipeline.
Phase 168: Ingests unstructured inputs, extracts atomic propositions,
quarantines candidate claims in SQLite, cross-verifies against EIFVE,
and safely promotes verified knowledge without codebase mutation.
"""

from typing import Any, Dict, List, Optional
import uuid

from geo_engine.verification.models import (
    AtomicClaim,
    VerificationVerdict,
    ClaimVerificationResult,
)
from geo_engine.verification.sanitizer import EvidenceSanitizer
from geo_engine.verification.claim_extractor import AtomicClaimExtractor
from geo_engine.verification.engine import FactVerificationEngine
from geo_engine.storage.event_store import EventStore


class AutonomousLearner:
    """
    Governed self-learning engine.
    Safely accumulates knowledge into the quarantine and promotion lifecycle:
    1. Input sanitization against prompt injection.
    2. Proposition extraction with qualifier and claim-type retention.
    3. Candidate claims inserted into `claim_quarantine` in SQLite.
    4. Epistemic verification via FactVerificationEngine.
    5. Promotion to verified knowledge only if confidence >= 0.85 and zero contradictions.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.store = EventStore(db_path=db_path) if db_path else EventStore()
        self.extractor = AtomicClaimExtractor()
        self.engine = FactVerificationEngine(event_store=self.store)
        self.sanitizer = EvidenceSanitizer()

    def learn_from_text(
        self,
        raw_text: str,
        source_name: str = "Conversational Ingestion",
        auto_promote: bool = True,
        min_promotion_confidence: float = 0.85,
    ) -> Dict[str, Any]:
        """
        Executes the safe learning cycle on unstructured text.
        """
        # 1. Sanitize text against prompt injection
        clean_text, injection_detected = EvidenceSanitizer.sanitize_untrusted_text(
            raw_text=raw_text, source_identifier=source_name
        )

        # 2. Extract atomic claims (strip wrapper delimiters so tags are not extracted as claims)
        import re
        unwrapped_text = re.sub(r"</?UNTRUSTED_EXTERNAL_EVIDENCE[^>]*>", "", clean_text).strip()
        claims: List[AtomicClaim] = self.extractor.extract_claims(unwrapped_text)

        quarantined_count = 0
        promoted_count = 0
        retained_count = 0
        results_summary = []

        for claim in claims:
            # 3. Quarantine candidate claim
            qid = f"Q-{uuid.uuid4().hex[:8].upper()}"
            domain_val = claim.domain.value if hasattr(claim.domain, "value") else str(claim.domain)
            try:
                self.store.quarantine_candidate_claim(
                    quarantine_id=qid,
                    claim_id=claim.claim_id,
                    raw_statement=claim.raw_statement,
                    proposition=claim.extracted_proposition,
                    domain=domain_val,
                    confidence=0.5,
                    review_required=True,
                )
                quarantined_count += 1
            except Exception:
                pass

            # 4. Epistemic verification
            result: ClaimVerificationResult = self.engine.verify_single_claim(claim)

            # 5. Check promotion threshold
            is_promotable = (
                auto_promote
                and result.verdict in (VerificationVerdict.VERIFIED, VerificationVerdict.MOSTLY_ACCURATE)
                and result.confidence_score >= min_promotion_confidence
                and result.source_independence_index >= 0.70
                and len(result.contradictory_evidence) == 0
            )

            if is_promotable:
                try:
                    self.store.promote_quarantined_claim(
                        quarantine_id=qid,
                        reviewer_notes="AutonomousLearner auto-promotion based on high confidence and source independence",
                    )
                    promoted_count += 1
                    status = "PROMOTED_TO_VERIFIED"
                except Exception:
                    retained_count += 1
                    status = "RETAINED_IN_QUARANTINE"
            else:
                retained_count += 1
                status = "RETAINED_IN_QUARANTINE"

            results_summary.append({
                "claim_id": claim.claim_id,
                "proposition": claim.extracted_proposition,
                "domain": domain_val,
                "verdict": result.verdict.value,
                "confidence": result.confidence_score,
                "learning_status": status,
                "verdict_rationale": result.verdict_rationale,
            })

        return {
            "learning_session_id": f"learn_{uuid.uuid4().hex[:10]}",
            "source_name": source_name,
            "prompt_injection_intercepted": injection_detected,
            "total_claims_extracted": len(claims),
            "quarantined_count": quarantined_count,
            "promoted_count": promoted_count,
            "retained_in_quarantine_count": retained_count,
            "claims_summary": results_summary,
            "operational_status": "LEARNING_CYCLE_COMPLETED_SAFELY",
        }
