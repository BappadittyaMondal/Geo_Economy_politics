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
]



