"""
Arbitration and Synthesis Package for the Geo-Engine.
Contains the Negative Space Diff Engine and the 5-Tier Summit Synthesizer.
"""

from .negative_space import NegativeSpaceDiffEngine, DenseSemanticIndex
from .synthesizer import SummitSynthesizer, LaymanSynthesizer
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
from .asset_fragility import (
    AssetFragilityModel,
    AssetDecayReport,
    VIPSecurityReport,
    SanctuaryViabilityReport,
)
from .causal_graph import (
    CausalNode,
    CausalEdge,
    CausalPath,
    EpistemicKnowledgeGraph,
)

__all__ = [
    "NegativeSpaceDiffEngine",
    "DenseSemanticIndex",
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
    "AssetFragilityModel",
    "AssetDecayReport",
    "VIPSecurityReport",
    "SanctuaryViabilityReport",
    "CausalNode",
    "CausalEdge",
    "CausalPath",
    "EpistemicKnowledgeGraph",
    "LaymanSynthesizer",
]

