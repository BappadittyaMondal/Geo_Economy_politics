"""
Arbitration and Synthesis Package for the Geo-Engine.
Contains the Negative Space Diff Engine and the 5-Tier Summit Synthesizer.
"""

from .negative_space import NegativeSpaceDiffEngine
from .synthesizer import SummitSynthesizer
from .persona_narrator import PersonaNarrator
from .competing_hypotheses import (
    CausalHypothesisType,
    HypothesisCandidate,
    ACHEvaluationReport,
    IncidentReasoningEngine,
)

__all__ = [
    "NegativeSpaceDiffEngine",
    "SummitSynthesizer",
    "PersonaNarrator",
    "CausalHypothesisType",
    "HypothesisCandidate",
    "ACHEvaluationReport",
    "IncidentReasoningEngine",
]
