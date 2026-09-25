"""
Arbitration and Synthesis Package for the Geo-Engine.
Contains the Negative Space Diff Engine and the 5-Tier Summit Synthesizer.
"""

from .negative_space import NegativeSpaceDiffEngine
from .synthesizer import SummitSynthesizer
from .persona_narrator import PersonaNarrator, CivilizationalCouncil
from .competing_hypotheses import (
    CausalHypothesisType,
    HypothesisCandidate,
    ACHEvaluationReport,
    IncidentReasoningEngine,
    TeleologicalEvaluation,
    TeleologicalFallacySieve,
    DecomposedClaim,
    ClaimDecomposer,
)
from .historical_arbiter import (
    ChronologyPillarScore,
    HistoricalHypothesisCandidate,
    ChronologyEvaluationReport,
    MultiPillarChronologyArbiter,
)

__all__ = [
    "NegativeSpaceDiffEngine",
    "SummitSynthesizer",
    "PersonaNarrator",
    "CivilizationalCouncil",
    "CausalHypothesisType",
    "HypothesisCandidate",
    "ACHEvaluationReport",
    "IncidentReasoningEngine",
    "TeleologicalEvaluation",
    "TeleologicalFallacySieve",
    "DecomposedClaim",
    "ClaimDecomposer",
    "ChronologyPillarScore",
    "HistoricalHypothesisCandidate",
    "ChronologyEvaluationReport",
    "MultiPillarChronologyArbiter",
]
