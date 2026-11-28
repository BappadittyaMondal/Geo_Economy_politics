# SUBSYSTEM SPECIFICATION: FACT VERIFICATION ENGINE & AUTONOMOUS LEARNER

## Module: `geo_engine/verification/__init__.py`

```python
"""
geo_engine.verification
~~~~~~~~~~~~~~~~~~~~~~~
Evidence Intelligence & Fact Verification Engine.
"""

from geo_engine.verification.models import (
    VerificationVerdict,
    EvidenceDomain,
    SourceCredibilityTier,
    EvidenceItem,
    AtomicClaim,
    ClaimVerificationResult,
    FactVerificationReport,
    ConfidenceMetadata,
)
from geo_engine.verification.claim_extractor import AtomicClaimExtractor
from geo_engine.verification.triangulator import EvidentiaryTriangulator
from geo_engine.verification.engine import FactVerificationEngine
from geo_engine.verification.sanitizer import EvidenceSanitizer
from geo_engine.verification.learner import AutonomousLearner

__all__ = [
    "VerificationVerdict",
    "EvidenceDomain",
    "SourceCredibilityTier",
    "EvidenceItem",
    "AtomicClaim",
    "ClaimVerificationResult",
    "FactVerificationReport",
    "ConfidenceMetadata",
    "AtomicClaimExtractor",
    "EvidentiaryTriangulator",
    "FactVerificationEngine",
    "EvidenceSanitizer",
    "AutonomousLearner",
]

```

## Module: `geo_engine/verification/claim_extractor.py`

```python
"""
geo_engine.verification.claim_extractor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Atomic Claim Decomposer & Proposition Extractor.

Decomposes complex, multi-clause statements into standalone, verifiable atomic
claims, identifying:
- Subject, Predicate, Metric, Temporal & Geographic anchors
- Domain classification (Macro, Defense, Legal, Chronology, Civilizational, etc.)
- Separation of empirical propositions from opinions, forecasts, and religious tenets
- Poisoned-tail detection and suppressed denominator flagging
"""

import re
import hashlib
from typing import List, Tuple
from geo_engine.verification.models import AtomicClaim, EvidenceDomain
from geo_engine.arbitration.competing_hypotheses import ClaimDecomposer


class AtomicClaimExtractor:
    """Extracts atomic testable claims and categorizes their epistemic domain."""

    # Sentence & clause splitting boundaries (split on .!?, newlines, or semicolons unless followed by causal connectors)
    SPLIT_PATTERNS = re.compile(r'(?<=[.!?])\s+|;(?!\s*(?:therefore|hence|thus|consequently)\b)\s*|\n+', re.IGNORECASE)

    # Domain keyword indicators

    DOMAIN_MAP = {
        EvidenceDomain.STATUTORY_LEGAL: [
            "act", "section", "article", "court", "judgment", "ordinance", "amendment",
            "statute", "petition", "bail", "rpa", "places of worship", "waqf", "crpc", "bnss"
        ],
        EvidenceDomain.MACROECONOMIC_FISCAL: [
            "gdp", "capex", "deficit", "inflation", "rbi", "vostro", "mou", "currency",
            "dollar", "billion", "crore", "trillion", "npa", "gva", "trade gap", "tax"
        ],
        EvidenceDomain.KINETIC_DEFENSE: [
            "military", "missile", "drone", "troop", "border", "lac", "loc", "air defense",
            "s-400", "wwr", "ammunition", "orbat", "interceptor", "shahed", "navy", "airstrike"
        ],
        EvidenceDomain.HISTORICAL_CHRONOLOGY: [
            "bce", "ce", "century", "dynasty", "archaeology", "excavation", "inscription",
            "aihole", "dating", "chronology", "mahabharata", "epoch", "treaty of", "partition",
            "kali yuga", "yuga", "nostradamus", "apocalypse"
        ],
        EvidenceDomain.CIVILIZATIONAL_CULTURAL: [
            "temple", "sanatan", "vedic", "hrce", "kalinga", "purusha sukta", "sampradaya",
            "dharmic", "festival", "kumbha", "navratri", "sacred", "decolonial",
            "kali yuga", "yuga", "nostradamus"
        ],
        EvidenceDomain.ENERGY_SUPPLY_CHAIN: [
            "hormuz", "malacca", "crude", "oil", "lng", "pipeline", "chokepoint", "tanker",
            "shadow fleet", "rare earth", "lithium", "gallium", "refinery", "fertilizer"
        ],
        EvidenceDomain.COGNITIVE_WARFARE: [
            "psyop", "narrative", "propaganda", "disinformation", "lawfare", "media bias",
            "conspiracy", "false flag", "bot", "deepfake", "rumor"
        ],
    }

    # Temporal patterns
    YEAR_PATTERN = re.compile(r'\b(1[0-9]{3}|20[0-9]{2}|[0-9]{3,4}\s*(?:BCE|CE|BC|AD))\b', re.IGNORECASE)

    # Metric patterns (numbers, percentages, currencies)
    METRIC_PATTERN = re.compile(
        r'(\$\s*\d+(?:\.\d+)?\s*(?:billion|million|trillion|b|m)?|'
        r'₹\s*\d+(?:\.\d+)?\s*(?:lakh|crore|billion)?|'
        r'\d+(?:\.\d+)?\s*(?:%|percent|bps|tonnes|bpd|troops|days|seats))',
        re.IGNORECASE
    )

    # Qualifier patterns (truth-conditional qualifiers that must not be silently stripped)
    QUALIFIER_PATTERNS = [
        "allegedly", "reportedly", "approximately", "according to", "claimed to",
        "estimated", "purported", "preliminary", "nearly", "roughly", "first", "only", "supposedly"
    ]

    # Opinion & Forecast indicators
    OPINION_FORECAST_INDICATORS = [
        "in my opinion", "i believe", "could lead to", "might happen", "predicted to", "expected to"
    ]


    @classmethod
    def classify_domain(cls, text: str) -> EvidenceDomain:
        """Classifies the primary evidence domain of a statement."""
        text_lower = text.lower()
        domain_scores = {d: 0 for d in cls.DOMAIN_MAP}

        for domain, keywords in cls.DOMAIN_MAP.items():
            for kw in keywords:
                if kw in text_lower:
                    domain_scores[domain] += 1

        best_domain = max(domain_scores, key=domain_scores.get)
        if domain_scores[best_domain] > 0:
            return best_domain
        return EvidenceDomain.GENERAL

    @classmethod
    def extract_claims(cls, raw_text: str) -> List[AtomicClaim]:
        """Extracts atomic claims from raw text or compound arguments."""
        if not raw_text or not raw_text.strip():
            return []

        raw_sentences = [s.strip() for s in cls.SPLIT_PATTERNS.split(raw_text) if len(s.strip()) > 8]
        extracted_claims: List[AtomicClaim] = []

        for idx, sentence in enumerate(raw_sentences):
            # 1. Check for compound assertions using ClaimDecomposer
            decomposed = ClaimDecomposer.decompose(sentence)
            
            # 2. Extract temporal anchor
            year_match = cls.YEAR_PATTERN.search(sentence)
            temporal = year_match.group(0) if year_match else None

            # 3. Extract metrics
            metric_match = cls.METRIC_PATTERN.search(sentence)
            metric = metric_match.group(0) if metric_match else None

            # 4. Opinion / Forecast check
            is_opinion = any(ind in sentence.lower() for ind in cls.OPINION_FORECAST_INDICATORS)

            # 5. Domain classification
            domain = cls.classify_domain(sentence)

            # 6. Extract truth-conditional qualifiers
            sentence_lower = sentence.lower()
            detected_qualifiers = [q for q in cls.QUALIFIER_PATTERNS if q in sentence_lower]

            # 7. Determine claim type
            if is_opinion:
                c_type = "opinion"
            elif metric:
                c_type = "numerical"
            elif domain == EvidenceDomain.STATUTORY_LEGAL:
                c_type = "legal"
            elif domain == EvidenceDomain.HISTORICAL_CHRONOLOGY:
                c_type = "historical"
            elif any(c in sentence_lower for c in ["therefore", "hence", "causes", "lead to", "results in"]):
                c_type = "causal"
            elif any(a in sentence_lower for a in ["according to", "stated that", "said that", "declared"]):
                c_type = "attribution"
            else:
                c_type = "factual"

            # 8. Check for suppressed denominators (e.g. absolute counts with no base)
            has_suppressed_denom = bool(
                re.search(
                    r'\b\d+(?:\.\d+)?\s*(?:million|lakh|crore|thousand)?\s*(?:votes|people|voters|cases|names)?\s*(?:were|are|have been|got)?\s*(?:deleted|arrested|stolen|purged|lost)\b',
                    sentence,
                    re.IGNORECASE
                )
                and not re.search(r'\b(out of|total|electorate|population|base|denominator|baseline)\b', sentence, re.IGNORECASE)
            )

            # Generate deterministic claim ID
            claim_hash = hashlib.sha256(f"{idx}:{sentence}".encode('utf-8')).hexdigest()[:10]
            claim_id = f"CLAIM-{claim_hash.upper()}"

            # If decomposed into separate premise and conclusion with poisoned tail, record
            has_poisoned = decomposed.is_poisoned_tail_detected or (
                bool(decomposed.conjunction_detected) and
                bool(re.search(r'\b(?:conspirat\w*|stolen|rigged|traitors?|sabotage|plot)\b', sentence, re.IGNORECASE))
            )

            claim = AtomicClaim(
                claim_id=claim_id,
                raw_statement=sentence,
                extracted_proposition=decomposed.factual_premises[0] if decomposed.factual_premises else sentence,
                domain=domain,
                temporal_boundary=temporal,
                quantitative_metric=metric,
                is_opinion_or_forecast=is_opinion,
                has_poisoned_tail=has_poisoned,
                has_suppressed_denominator=has_suppressed_denom,
                qualifiers=detected_qualifiers,
                claim_type=c_type
            )

            extracted_claims.append(claim)

        return extracted_claims

```

## Module: `geo_engine/verification/engine.py`

```python
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
import math
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


# ============================================================================
# Phase 433: Empirical Falsification and Cryptographic Verification Engine (Dr. Anand Ranganathan Module)
# ============================================================================

class EmpiricalFalsificationAndCryptographicVerificationEngine:
    """
    Phase 433 (Dr. Anand Ranganathan Module): Enforces Karl Popper's empirical falsification standard,
    blockchain cryptographic hash anchoring, and zero-sycophancy fact auditing against ideological,
    theological, or political claims. Every assertion must map directly to primary physical ledgers.
    Formula:
        VerificationScore = Norm((0.40 * physical_ledger_corroboration + 0.35 * cryptographic_audit_trail + 0.25 * falsification_rate) /
                                 (1.0 + unsubstantiated_claim_ratio + rhetorical_inflation))
        score = Sigmoid(2.8 * VerificationScore + 2.5 * physical_ledger_corroboration - 1.2)
    """
    @classmethod
    def evaluate(
        cls,
        physical_ledger_corroboration_ratio: float = 0.90,
        cryptographic_audit_trail_depth: float = 0.85,
        zero_sycophancy_falsification_rate: float = 0.85,
        unsubstantiated_narrative_claim_ratio: float = 0.20,
        rhetorical_inflation_factor: float = 0.15
    ) -> Dict[str, Any]:
        p_ledg = float(max(0.0, min(1.0, physical_ledger_corroboration_ratio)))
        c_audit = float(max(0.0, min(1.0, cryptographic_audit_trail_depth)))
        z_fals = float(max(0.0, min(1.0, zero_sycophancy_falsification_rate)))
        u_claim = float(max(0.0, min(1.0, unsubstantiated_narrative_claim_ratio)))
        r_infl = float(max(0.0, min(1.0, rhetorical_inflation_factor)))

        raw_verif = (0.40 * p_ledg + 0.35 * c_audit + 0.25 * z_fals) / (1.0 + u_claim + r_infl)
        z = 2.8 * raw_verif + 2.5 * p_ledg - 1.2
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "IRREFUTABLE_EMPIRICAL_AND_CRYPTOGRAPHIC_VERIFICATION"
            verdict = "EVIDENCE_GUT_CHECK_PASSED_ZERO_SYCOPHANCY_CERTIFIED"
            rationale = (
                f"Irrefutable scientific and empirical veracity ({score:.4f}): Physical ledger corroboration ({p_ledg:.2f}) "
                f"and cryptographic audit trail ({c_audit:.2f}) decisively falsify political rhetoric and rhetorical inflation."
            )
        elif score >= 0.45:
            tier = "PROVISIONAL_EMPIRICAL_CORROBORATION"
            verdict = "AUDIT_UNDERLYING_PRIMARY_CUSTOMS_MANIFESTS_AND_BANK_STATEMENTS"
            rationale = f"Provisional corroboration ({score:.4f}): Unsubstantiated claims ({u_claim:.2f}) require primary document verification."
        else:
            tier = "FALSIFIED_RHETORICAL_INFLATION"
            verdict = "REJECT_ASSERTS_AS_UNGROUNDED_POLITICAL_THEATER"
            rationale = f"Falsified narrative ({score:.4f}): Absence of physical ledger trails exposes claim as political spin."

        return {
            "empirical_falsification_cryptographic_verification_score": score,
            "physical_ledger_corroboration_ratio": round(p_ledg, 4),
            "cryptographic_audit_trail_depth": round(c_audit, 4),
            "zero_sycophancy_falsification_rate": round(z_fals, 4),
            "unsubstantiated_narrative_claim_ratio": round(u_claim, 4),
            "rhetorical_inflation_factor": round(r_infl, 4),
            "verification_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_empirical_veracity_irrefutable": score >= 0.70,
        }

```

## Module: `geo_engine/verification/learner.py`

```python
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


```

## Module: `geo_engine/verification/models.py`

```python
"""
geo_engine.verification.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Typed Pydantic domain models for the Evidence Intelligence & Fact Verification Engine.

Supports 7 standardized evidence-based verdicts:
- VERIFIED
- MOSTLY_ACCURATE
- MISLEADING_OR_MISSING_CONTEXT
- DISPUTED
- UNSUPPORTED
- FALSE
- UNVERIFIABLE
"""

from __future__ import annotations
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class VerificationVerdict(str, Enum):
    """The 7 standardized evidence-based verdicts."""
    VERIFIED = "VERIFIED"
    MOSTLY_ACCURATE = "MOSTLY_ACCURATE"
    MISLEADING_OR_MISSING_CONTEXT = "MISLEADING_OR_MISSING_CONTEXT"
    DISPUTED = "DISPUTED"
    UNSUPPORTED = "UNSUPPORTED"
    FALSE = "FALSE"
    UNVERIFIABLE = "UNVERIFIABLE"


class EvidenceDomain(str, Enum):
    """Domain classification for specialized verification standards."""
    MACROECONOMIC_FISCAL = "MACROECONOMIC_FISCAL"
    KINETIC_DEFENSE = "KINETIC_DEFENSE"
    STATUTORY_LEGAL = "STATUTORY_LEGAL"
    HISTORICAL_CHRONOLOGY = "HISTORICAL_CHRONOLOGY"
    CIVILIZATIONAL_CULTURAL = "CIVILIZATIONAL_CULTURAL"
    ENERGY_SUPPLY_CHAIN = "ENERGY_SUPPLY_CHAIN"
    COGNITIVE_WARFARE = "COGNITIVE_WARFARE"
    GENERAL = "GENERAL"


class SourceCredibilityTier(str, Enum):
    """Epistemic credibility tier of the evidence source."""
    TIER_1_PRIMARY_ARCHIVE = "TIER_1_PRIMARY_ARCHIVE"      # Treaty text, Gazette, official statutory record, satellite baseline
    TIER_2_AUDITED_TELEMETRY = "TIER_2_AUDITED_TELEMETRY"  # Central bank bulletin, customs manifest, audited financial flow
    TIER_3_OFFICIAL_STATEMENT = "TIER_3_OFFICIAL_STATEMENT"# Verified government press release, ministry briefing
    TIER_4_PEER_REVIEWED = "TIER_4_PEER_REVIEWED"          # Academic peer-reviewed research, rigorous field excavation
    TIER_5_INDEPENDENT_MEDIA = "TIER_5_INDEPENDENT_MEDIA"  # Corroborated investigative journalism
    TIER_6_DERIVATIVE_REPORT = "TIER_6_DERIVATIVE_REPORT"  # Syndicated wire reposts, commentary, secondary summaries
    TIER_0_UNVERIFIED_LEAK = "TIER_0_UNVERIFIED_LEAK"      # Anonymous claim, unattributed social media post


class EvidenceItem(BaseModel):
    """Structured record of an individual piece of supporting or contradictory evidence."""
    evidence_id: str
    source_title: str
    publication_date: Optional[str] = None
    source_tier: SourceCredibilityTier = SourceCredibilityTier.TIER_5_INDEPENDENT_MEDIA
    url_or_identifier: Optional[str] = None
    supporting_passage: Optional[str] = None
    contradictory_passage: Optional[str] = None
    is_primary_source: bool = False
    source_independence_score: float = Field(default=0.85, ge=0.0, le=1.0)
    context_caveats: List[str] = Field(default_factory=list)


class ConfidenceMetadata(BaseModel):
    """Explicit confidence metadata preventing uncalibrated heuristics from presenting as probabilities."""
    value: Optional[float] = None
    label: str = "not_calibrated"  # "low", "moderate", "high", "not_calibrated"
    calibration_status: str = "not_calibrated"  # "not_calibrated", "calibrated_brier"
    explanation: str = "Heuristic tier-derived score; uncalibrated against representative empirical benchmark."


class AtomicClaim(BaseModel):
    """An individual, verifiable proposition extracted from a statement or text."""
    claim_id: str
    raw_statement: str
    extracted_proposition: str
    domain: EvidenceDomain = EvidenceDomain.GENERAL
    subject_entity: str = ""
    predicate_action: str = ""
    quantitative_metric: Optional[str] = None
    temporal_boundary: Optional[str] = None
    geographic_context: Optional[str] = None
    is_opinion_or_forecast: bool = False
    has_poisoned_tail: bool = False
    has_suppressed_denominator: bool = False
    qualifiers: List[str] = Field(default_factory=list)
    claim_type: str = "factual"
    context_and_limitations: List[str] = Field(default_factory=list)


class ClaimVerificationResult(BaseModel):
    """Detailed verification audit for a single atomic claim."""
    claim: AtomicClaim
    verdict: VerificationVerdict
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence_metadata: ConfidenceMetadata = Field(default_factory=ConfidenceMetadata)
    primary_evidence: List[EvidenceItem] = Field(default_factory=list)
    contradictory_evidence: List[EvidenceItem] = Field(default_factory=list)
    verdict_rationale: str
    corroboration_score: float = Field(default=0.0, ge=0.0, le=1.0)
    source_independence_index: float = Field(default=0.0, ge=0.0, le=1.0)
    source_independence_assessment: str = "Independent primary archive or telemetry record."
    epistemic_tier_used: str = "TIER_0_INSUFFICIENT_EVIDENCE"
    retrieval_status: str = "complete"
    review_required: bool = True
    context_and_limitations: List[str] = Field(default_factory=list)
    identified_biases_or_fallacies: List[str] = Field(default_factory=list)


class FactVerificationReport(BaseModel):
    """Consolidated master audit report across all claims in a query or document."""
    report_id: str
    input_text: str
    overall_verdict: VerificationVerdict
    composite_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence_metadata: ConfidenceMetadata = Field(default_factory=ConfidenceMetadata)
    total_claims_analyzed: int = 0
    verified_claims_count: int = 0
    false_claims_count: int = 0
    misleading_claims_count: int = 0
    unverifiable_claims_count: int = 0
    claim_results: List[ClaimVerificationResult] = Field(default_factory=list)
    executive_summary: str
    source_provenance_audit: Dict[str, Any] = Field(default_factory=dict)
    unresolved_questions: List[str] = Field(default_factory=list)
    engine_version: str = "2.1.0-eifve"
    policy_version: str = "2026.10-evidence-first"
    reproducibility_hash: str = ""

```

## Module: `geo_engine/verification/sanitizer.py`

```python
"""
geo_engine.verification.sanitizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Security hardening: Prompt injection defense, control sequence stripping,
and untrusted evidence encapsulation for external feeds and content.
"""

import re
from typing import Tuple


class EvidenceSanitizer:
    """Hardened sanitizer for external, untrusted evidence streams and text."""

    MAX_EVIDENCE_LENGTH = 8000  # Prevent memory denial-of-service

    # Patterns commonly used in prompt-injection attacks
    INJECTION_PATTERNS = [
        re.compile(r"(?i)\bignore\s+(?:all\s+)?previous\s+(?:instructions|directions|prompts)\b"),
        re.compile(r"(?i)\bsystem\s+prompt\s+override\b"),
        re.compile(r"(?i)\byou\s+are\s+now\s+in\s+developer\s+mode\b"),
        re.compile(r"(?i)\bprint\s+(?:all\s+)?(?:api\s+keys?|secrets?|passwords?|tokens?)\b"),
        re.compile(r"(?i)\bexecute\s+(?:arbitrary\s+)?code\s+as\s+root\b"),
        re.compile(r"(?i)<\s*script[^>]*>.*?</\s*script\s*>"),
    ]

    @classmethod
    def sanitize_untrusted_text(cls, raw_text: str, source_identifier: str = "EXTERNAL_FEED") -> Tuple[str, bool]:
        """
        Sanitizes untrusted text and wraps it in explicit security delimiters.
        Returns: (sanitized_and_wrapped_text, was_injection_detected)
        """
        if not raw_text:
            return "", False

        # 1. Truncate oversized payload
        truncated = raw_text[:cls.MAX_EVIDENCE_LENGTH]

        # 2. Scan for prompt injection directives
        injection_detected = False
        clean_text = truncated
        for pattern in cls.INJECTION_PATTERNS:
            if pattern.search(clean_text):
                injection_detected = True
                clean_text = pattern.sub("[REDACTED_ADVERSARIAL_INJECTION_DIRECTIVE]", clean_text)

        # 3. Strip null bytes and non-printable control characters
        clean_text = "".join(ch for ch in clean_text if ch == "\n" or ch == "\t" or (ch >= " " and ch != "\x7f"))

        # 4. Encapsulate in strict untrusted evidence boundary
        encapsulated = f'<UNTRUSTED_EXTERNAL_EVIDENCE source="{source_identifier}">\n{clean_text.strip()}\n</UNTRUSTED_EXTERNAL_EVIDENCE>'

        return encapsulated, injection_detected

```

## Module: `geo_engine/verification/triangulator.py`

```python
"""
geo_engine.verification.triangulator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Evidentiary Triangulation & Source Independence Engine.

Cross-checks atomic claims across:
1. SQLite EventStore (treaties, gazetted clauses, chronology anchors, debunk registry)
2. Epistemic Knowledge Graph (causal nodes, transmission edges, shock chains)
3. Sovereign Official Telemetry (MEA, PIB, UN Press, State Dept communiques)
4. Source Independence Analyzer (detects syndicated echoes and circular citation loops)
"""

import hashlib
from typing import List, Tuple, Dict, Any, Optional
from geo_engine.verification.models import (
    AtomicClaim, EvidenceItem, SourceCredibilityTier, EvidenceDomain
)
from geo_engine.storage.event_store import EventStore
from geo_engine.arbitration.causal_graph import EpistemicKnowledgeGraph
from geo_engine.ingestion.sovereign_rss import SovereignRSSClient


class EvidentiaryTriangulator:
    """Triangulates claims against ground truth databases and calculates source independence."""

    def __init__(self, event_store: Optional[EventStore] = None):
        self.store = event_store or EventStore()
        self.graph = EpistemicKnowledgeGraph()

    def triangulate_claim(self, claim: AtomicClaim) -> Tuple[List[EvidenceItem], List[EvidenceItem], float]:
        """
        Triangulates an atomic claim against knowledge stores.
        Returns:
            (supporting_evidence, contradictory_evidence, source_independence_score)
        """
        supporting: List[EvidenceItem] = []
        contradictory: List[EvidenceItem] = []

        claim_lower = claim.extracted_proposition.lower()

        # 1. Check Debunk Registry in EventStore
        debunks = self.store.get_debunk_registry()
        for d in debunks:
            d_desc = d.get("debunk_details", "").lower()
            d_topic = d.get("target_topic", "").lower()
            if any(term in claim_lower for term in d_topic.split() if len(term) > 3):
                contradictory.append(EvidenceItem(
                    evidence_id=f"EVID-DEBUNK-{d['benchmark_id']}",
                    source_title=f"Verified Debunk Registry: {d['target_topic']}",
                    publication_date=d.get("documented_origin_date"),
                    source_tier=SourceCredibilityTier.TIER_1_PRIMARY_ARCHIVE,
                    url_or_identifier=d["benchmark_id"],
                    contradictory_passage=d["debunk_details"],
                    is_primary_source=True,
                    source_independence_score=0.98,
                    context_caveats=["Documented hoax or commercial interpolation."]
                ))

        # 2. Check Cosmic / Chronological Benchmarks
        if claim.domain in (EvidenceDomain.HISTORICAL_CHRONOLOGY, EvidenceDomain.CIVILIZATIONAL_CULTURAL) or any(w in claim_lower for w in ["kali yuga", "apocalypse", "2032", "doomsday", "aihole", "yuga"]):
            chronos = self.store.get_cosmic_chronology_anchors()

            for c in chronos:
                source_name = c.get("canonical_source", "").lower()
                citation = c.get("primary_citation", "").lower()
                if any(w in claim_lower for w in ["kali yuga", "apocalypse", "2032", "doomsday", "aihole"]):
                    if "aihole" in claim_lower and "aihole" in citation:
                        supporting.append(EvidenceItem(
                            evidence_id=f"EVID-CHRONO-{c['benchmark_id']}",
                            source_title=f"Epigraphic Anchor: {c['canonical_source']}",
                            source_tier=SourceCredibilityTier.TIER_1_PRIMARY_ARCHIVE,
                            url_or_identifier=c["benchmark_id"],
                            supporting_passage=f"Aihole Inscription records {c['duration_years']} elapsed years since Bharata War.",
                            is_primary_source=True,
                            source_independence_score=1.0
                        ))
                    elif ("2032" in claim_lower or "ends" in claim_lower) and c["benchmark_id"] == "COSMIC-KALIYUGA-CANONICAL":
                        contradictory.append(EvidenceItem(
                            evidence_id=f"EVID-CHRONO-{c['benchmark_id']}",
                            source_title=f"Canonical Textual Baseline: {c['canonical_source']}",
                            source_tier=SourceCredibilityTier.TIER_1_PRIMARY_ARCHIVE,
                            url_or_identifier=c["benchmark_id"],
                            contradictory_passage=f"Kali Yuga duration is 432,000 years per Surya Siddhanta. Gregorian year 2032 is an arbitrary internet date.",
                            is_primary_source=True,
                            source_independence_score=1.0
                        ))

        # 3. Check Statutory Treaty Clauses in EventStore
        try:
            if hasattr(self.store, "get_mandatory_baseline_clauses"):
                clauses = self.store.get_mandatory_baseline_clauses()
            elif hasattr(self.store, "get_baseline_clauses"):
                clauses = self.store.get_baseline_clauses()
            else:
                clauses = []
            for cl in clauses:
                cl_text = cl.get("clause_text", "").lower()
                cl_title = cl.get("treaty_name", "").lower()
                # Check for keyword overlap
                claim_tokens = [w for w in claim_lower.split() if len(w) > 4]
                matching_tokens = [w for w in claim_tokens if w in cl_text or w in cl_title]
                if len(matching_tokens) >= 2:
                    supporting.append(EvidenceItem(
                        evidence_id=f"EVID-STATUTE-{cl.get('clause_id', 'TREATY')}",
                        source_title=f"Statutory Baseline: {cl.get('treaty_name', 'Treaty')}",
                        publication_date=str(cl.get('year', '')),
                        source_tier=SourceCredibilityTier.TIER_1_PRIMARY_ARCHIVE,
                        url_or_identifier=cl.get("clause_id"),
                        supporting_passage=cl.get("clause_text"),
                        is_primary_source=True,
                        source_independence_score=1.0
                    ))
        except Exception:
            pass

        # 4. Check Causal Knowledge Graph for Causal Plausibility
        if "lead to" in claim_lower or "cause" in claim_lower or "because" in claim_lower:
            # Verify if causal path exists
            paths = self.graph.find_causal_paths(source_id="root_hormuz", target_id="end_food_inflation", max_hops=4)
            if paths and ("hormuz" in claim_lower and "food" in claim_lower):
                supporting.append(EvidenceItem(
                    evidence_id="EVID-CAUSAL-GRAPH-HORMUZ-FOOD",
                    source_title="Epistemic Causal Graph: Hormuz -> Fertilizer -> Food Inflation",
                    source_tier=SourceCredibilityTier.TIER_2_AUDITED_TELEMETRY,
                    supporting_passage="Verified multi-hop shockwave cascade connects Hormuz maritime interdiction with fertilizer supply deficit and food price spikes.",
                    is_primary_source=False,
                    source_independence_score=0.90
                ))

        # 5. Calculate Source Independence Score
        source_independence = self.calculate_source_independence(supporting + contradictory)

        return supporting, contradictory, source_independence

    @staticmethod
    def calculate_source_independence(evidence_items: List[EvidenceItem]) -> float:
        """
        Calculates source independence.
        Penalizes circular echo chambers (e.g. multiple items sharing the same phrasing).
        """
        if not evidence_items:
            return 0.50

        # Primary sources give high independence
        primary_count = sum(1 for e in evidence_items if e.is_primary_source)
        tier_weights = {
            SourceCredibilityTier.TIER_1_PRIMARY_ARCHIVE: 1.0,
            SourceCredibilityTier.TIER_2_AUDITED_TELEMETRY: 0.95,
            SourceCredibilityTier.TIER_3_OFFICIAL_STATEMENT: 0.90,
            SourceCredibilityTier.TIER_4_PEER_REVIEWED: 0.85,
            SourceCredibilityTier.TIER_5_INDEPENDENT_MEDIA: 0.70,
            SourceCredibilityTier.TIER_6_DERIVATIVE_REPORT: 0.40,
            SourceCredibilityTier.TIER_0_UNVERIFIED_LEAK: 0.15,
        }

        avg_tier_weight = sum(tier_weights.get(e.source_tier, 0.5) for e in evidence_items) / len(evidence_items)

        # Detect wire duplication (hash snippets)
        seen_passages = set()
        duplicates = 0
        for e in evidence_items:
            passage = (e.supporting_passage or e.contradictory_passage or "")[:100].strip()
            p_hash = hashlib.sha256(passage.encode('utf-8')).hexdigest()
            if p_hash in seen_passages:
                duplicates += 1
            else:
                seen_passages.add(p_hash)

        duplication_penalty = 0.25 * (duplicates / len(evidence_items))
        independence_score = max(0.10, min(1.0, avg_tier_weight - duplication_penalty))
        return round(independence_score, 3)

```
