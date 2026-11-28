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
        self.db_path = db_path or getattr(self.store, "db_path", "data/events.db")
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

    _STOPWORDS = frozenset({
        "that", "this", "with", "from", "have", "will", "into", "over", "their",
        "about", "which", "were", "been", "also", "more", "than", "what", "when",
        "where", "there", "they", "would", "could", "should", "after", "before",
        "under", "between", "through", "during", "while", "some", "only", "very",
    })
    _DEBUNK_MARKERS = (
        "not true", "false", "debunked", "fabricated", "hoax", "morphed",
        "cropped", "fake", "refuted", "never occurred", "misleading", "out of context",
        "manipulated", "deepfake",
    )
    _NEGATION_TOKENS = frozenset({"not", "never", "no", "neither", "nor", "false", "fake", "hoax", "debunked", "refuted"})

    @classmethod
    def _extract_content_tokens(cls, text: str) -> set:
        import re
        raw_tokens = re.findall(r"[a-z0-9]{4,}", (text or "").lower())
        return {tok for tok in raw_tokens if tok not in cls._STOPWORDS}

    @classmethod
    def _has_contradiction_or_debunk(cls, proposition: str, candidate_text: str) -> bool:
        prop_low = (proposition or "").lower()
        cand_low = (candidate_text or "").lower()
        if any(marker in prop_low for marker in cls._DEBUNK_MARKERS):
            return True
        if any(marker in cand_low for marker in cls._DEBUNK_MARKERS):
            return True
        import re
        prop_neg = bool(cls._NEGATION_TOKENS.intersection(re.findall(r"[a-z]+", prop_low)))
        cand_neg = bool(cls._NEGATION_TOKENS.intersection(re.findall(r"[a-z]+", cand_low)))
        return prop_neg != cand_neg

    def auto_harmonize_quarantine(self, min_corroboration_count: int = 3) -> dict:
        """
        Phase 215 (Schema-Corrected & Contradiction-Safe): Autonomous Quarantine Harmonizer Daemon.
        Scans claim_quarantine table (column: status, proposition),
        cross-references against events (description), historical_treaty_clauses (clause_text),
        and historical_anniversaries (historical_summary) tables using stopword-filtered
        per-row token overlap and negation/debunk contradiction screening,
        promoting claims with >= min_corroboration_count verified anchors to 'promoted' status.
        """
        import sqlite3
        db_path = getattr(self, 'db_path', None) or getattr(self.store, 'db_path', 'data/events.db')
        promoted = []
        retained = []
        contradicted_retained = []
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "SELECT quarantine_id, proposition, confidence "
                "FROM claim_quarantine WHERE LOWER(status) = 'quarantined' "
                "ORDER BY confidence DESC"
            )
            quarantined_rows = cur.fetchall()

            corpus_rows: List[str] = []
            for sql_q in (
                "SELECT COALESCE(title, '') || ' ' || COALESCE(summary, '') FROM events WHERE summary IS NOT NULL OR title IS NOT NULL",
                "SELECT clause_text FROM historical_treaty_clauses WHERE clause_text IS NOT NULL",
                "SELECT historical_summary FROM historical_anniversaries WHERE historical_summary IS NOT NULL",
                "SELECT COALESCE(key_thesis, '') || ' ' || COALESCE(strategic_doctrine, '') FROM knowledge_discourses WHERE key_thesis IS NOT NULL OR strategic_doctrine IS NOT NULL",
            ):
                try:
                    cur.execute(sql_q)
                    corpus_rows.extend(r[0] for r in cur.fetchall() if r and r[0])
                except sqlite3.OperationalError:
                    pass

            tokenized_corpus = [
                (row_txt, self._extract_content_tokens(row_txt))
                for row_txt in corpus_rows
            ]

            for row_id, proposition, confidence in quarantined_rows:
                prop_tokens = self._extract_content_tokens(proposition or "")
                best_overlap = 0
                contradiction_hit = any(m in (proposition or "").lower() for m in self._DEBUNK_MARKERS)

                if len(prop_tokens) >= min_corroboration_count and not contradiction_hit:
                    for row_txt, row_tokens in tokenized_corpus:
                        overlap = len(prop_tokens.intersection(row_tokens))
                        if overlap >= min_corroboration_count:
                            if self._has_contradiction_or_debunk(proposition or "", row_txt):
                                contradiction_hit = True
                                break
                            if overlap > best_overlap:
                                best_overlap = overlap

                if best_overlap >= min_corroboration_count and not contradiction_hit:
                    cur.execute(
                        "UPDATE claim_quarantine SET status = 'promoted' "
                        "WHERE quarantine_id = ?",
                        (row_id,)
                    )
                    promoted.append({
                        "id": row_id,
                        "corroboration_count": best_overlap,
                        "confidence": confidence,
                    })
                else:
                    retained.append({
                        "id": row_id,
                        "corroboration_count": best_overlap,
                        "contradiction_blocked": contradiction_hit,
                    })
                    if contradiction_hit:
                        contradicted_retained.append(row_id)
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
            "contradiction_blocked_count": len(contradicted_retained),
            "promoted_ids": [r["id"] for r in promoted],
            "min_corroboration_threshold": min_corroboration_count,
            "operational_note": (
                "Claims promoted to 'promoted' status after multi-token entity/predicate corroboration and contradiction screening."
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

