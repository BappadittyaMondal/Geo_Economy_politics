"""
Geo-Economic & Geopolitical Intelligence Engine
Operationalizing the 12-Lens Matrix, Epistemic Truth Hierarchy, and 5-Tier Response Protocol.
"""

__version__ = "1.0.0"

from .arbitration.causal_graph import (
    CausalNode,
    CausalEdge,
    CausalPath,
    EpistemicKnowledgeGraph,
)
from .core.speaker_profiler import (
    SpeakerArchetype,
    SpeakerProfile,
    EpistemicSpeakerProfiler,
)
from .arbitration.synthesizer import LaymanSynthesizer
from .arbitration.negative_space import DenseSemanticIndex
from .lenses.institutional_lawfare import CulturalReligiousGrayzoneSieve
from .video.audio_stream import (
    DiscourseVectorDecomposition,
    DiscourseDecompositionEngine,
    StreamingAudioChunk,
    StreamingDiscourseAlert,
    ChunkAuditTelemetry,
    StreamingChunkAuditor,
)
from .core.conversation_distiller import (
    VerificationStatus,
    DistillationAction,
    DistilledClaim,
    DistillationReport,
    ChatConversationDistiller,
)
from .arbitration.competing_hypotheses import (
    StatisticalManipulationEvaluation,
    StatisticalManipulationSieve,
)
from .lenses.civilizational import (
    CulturalGrayzoneSieve,
    SacredCalendarProvocationSieve,
)
from .lenses.food_security import AgrarianWaterCartelSieve
from .forecasting.resolution_daemon import ForecastResolutionDaemon
from .studio.frame_renderer import LocalFrameRenderer
from .ingestion.sovereign_rss import SovereignRSSClient
from .verification import (
    VerificationVerdict,
    EvidenceDomain,
    SourceCredibilityTier,
    EvidenceItem,
    AtomicClaim,
    ClaimVerificationResult,
    FactVerificationReport,
    ConfidenceMetadata,
    AtomicClaimExtractor,
    EvidentiaryTriangulator,
    FactVerificationEngine,
    EvidenceSanitizer,
)

__all__ = [
    "CausalNode",
    "CausalEdge",
    "CausalPath",
    "EpistemicKnowledgeGraph",
    "SpeakerArchetype",
    "SpeakerProfile",
    "EpistemicSpeakerProfiler",
    "CulturalReligiousGrayzoneSieve",
    "LaymanSynthesizer",
    "DenseSemanticIndex",
    "DiscourseVectorDecomposition",
    "DiscourseDecompositionEngine",
    "StreamingAudioChunk",
    "StreamingDiscourseAlert",
    "ChunkAuditTelemetry",
    "StreamingChunkAuditor",
    "VerificationStatus",
    "DistillationAction",
    "DistilledClaim",
    "DistillationReport",
    "ChatConversationDistiller",
    "StatisticalManipulationEvaluation",
    "StatisticalManipulationSieve",
    "CulturalGrayzoneSieve",
    "SacredCalendarProvocationSieve",
    "AgrarianWaterCartelSieve",
    "ForecastResolutionDaemon",
    "LocalFrameRenderer",
    "SovereignRSSClient",
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
]





