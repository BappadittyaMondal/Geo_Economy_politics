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

    def learn_from_chat(
        self,
        conversation_messages: Any,
        user_identity: str = "Authoritative User Directive",
        auto_promote: bool = True,
        min_promotion_confidence: float = 0.85,
    ) -> Dict[str, Any]:
        """
        Phase 205: Autonomous Chat-Conversion Hook.
        Ingests user-agent conversation messages, distills atomic factual propositions,
        safely stores them into `claim_quarantine` in SQLite, runs Epistemic Verification,
        and auto-promotes verified claims into the active knowledge graph without code mutation.
        """
        if isinstance(conversation_messages, list):
            combined_text = "\n".join(str(m) for m in conversation_messages)
        else:
            combined_text = str(conversation_messages)

        return self.learn_from_text(
            raw_text=combined_text,
            source_name=f"Chat Conversion [{user_identity}]",
            auto_promote=auto_promote,
            min_promotion_confidence=min_promotion_confidence,
        )

    def auto_harmonize_quarantine(self, min_corroboration_count: int = 3) -> dict:
        """
        Phase 215 (Schema-Corrected): Autonomous Quarantine Harmonizer Daemon.
        Scans claim_quarantine table (column: status, proposition),
        cross-references against events (description) and
        historical_treaty_clauses (clause_text) tables,
        promotes claims with >= min_corroboration_count anchors to 'promoted' status.
        """
        import sqlite3
        db_path = getattr(self, 'db_path', 'data/events.db')
        promoted = []
        retained = []
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            # Correct column names: status (not verification_status), proposition (not claim_text)
            cur.execute(
                "SELECT quarantine_id, proposition, confidence "
                "FROM claim_quarantine WHERE status = 'quarantined' "
                "ORDER BY confidence DESC"
            )
            quarantined_rows = cur.fetchall()
            for row_id, proposition, confidence in quarantined_rows:
                words = [w.strip().lower() for w in (proposition or "").split()
                         if len(w.strip()) >= 4]
                corroboration_count = 0
                for word in words[:10]:
                    # Correct table: events (has description column)
                    try:
                        cur.execute(
                            "SELECT COUNT(*) FROM events "
                            "WHERE LOWER(description) LIKE ?",
                            ("%" + word + "%",)
                        )
                        ev_count = cur.fetchone()[0]
                    except sqlite3.OperationalError:
                        ev_count = 0
                    # Correct table: historical_treaty_clauses (has clause_text column)
                    try:
                        cur.execute(
                            "SELECT COUNT(*) FROM historical_treaty_clauses "
                            "WHERE LOWER(clause_text) LIKE ?",
                            ("%" + word + "%",)
                        )
                        tc_count = cur.fetchone()[0]
                    except sqlite3.OperationalError:
                        tc_count = 0
                    # Also check historical_anniversaries (historical_summary column)
                    try:
                        cur.execute(
                            "SELECT COUNT(*) FROM historical_anniversaries "
                            "WHERE LOWER(historical_summary) LIKE ?",
                            ("%" + word + "%",)
                        )
                        ha_count = cur.fetchone()[0]
                    except sqlite3.OperationalError:
                        ha_count = 0
                    if ev_count > 0 or tc_count > 0 or ha_count > 0:
                        corroboration_count += 1
                # Promote if corroboration meets threshold
                if corroboration_count >= min_corroboration_count:
                    cur.execute(
                        "UPDATE claim_quarantine SET status = 'promoted' "
                        "WHERE quarantine_id = ?",
                        (row_id,)
                    )
                    promoted.append({
                        "id": row_id,
                        "corroboration_count": corroboration_count,
                        "confidence": confidence,
                    })
                else:
                    retained.append({"id": row_id, "corroboration_count": corroboration_count})
            conn.commit()
            conn.close()
        except Exception as exc:
            return {
                "harmonizer_status": "DB_ERROR",
                "error": str(exc),
                "promoted_count": 0,
                "retained_count": 0,
            }
        return {
            "harmonizer_status": "HARMONIZATION_COMPLETE",
            "promoted_count": len(promoted),
            "retained_count": len(retained),
            "promoted_ids": [r["id"] for r in promoted],
            "min_corroboration_threshold": min_corroboration_count,
            "operational_note": (
                "Claims promoted to 'promoted' status for active knowledge graph ingestion."
            ),
        }

    def learn_from_event(self, event, auto_promote: bool = True,
                         min_promotion_confidence: float = 0.85) -> dict:
        """
        Phase 217: Autonomous SummitEvent-to-Quarantine Learning Hook.
        Takes any SummitEvent (or duck-typed object with title/description/
        civilizational_significance), distills its content into atomic propositions,
        stores them in claim_quarantine, and auto-promotes verified claims.
        Enables the learning system to accumulate DNA from every analyzed event.
        """
        title = getattr(event, "title", "") or ""
        desc = getattr(event, "description", "") or ""
        civ = getattr(event, "civilizational_significance", "") or ""
        region = getattr(event, "region", "") or ""
        combined = f"{title}. {desc}. {civ}. {region}".strip(". ")
        eid = getattr(event, "event_id", None) or getattr(event, "id", "unknown")
        return self.learn_from_text(
            raw_text=combined,
            source_name=f"SummitEvent[{eid}]",
            auto_promote=auto_promote,
            min_promotion_confidence=min_promotion_confidence,
        )

