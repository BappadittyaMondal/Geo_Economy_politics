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
