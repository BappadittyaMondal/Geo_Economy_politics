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
