"""
Autonomous Sovereign Video Studio Engine.
End-to-end multi-agent pipeline for automated faceless and avatar video production
supporting English, Hindi, Bengali, and Sanskrit.
"""

from .script_architect import (
    VideoLanguage,
    VideoPresentationMode,
    VideoDurationTier,
    SceneSegment,
    VideoScriptPackage,
    ScriptArchitect,
)
from .voice_synthesizer import (
    VoiceProfile,
    AudioDuckingProfile,
    SubtitleCue,
    MultilingualVoiceSynthesizer,
)
from .video_assembler import (
    AspectRatio,
    VideoRenderSpec,
    RenderJobManifest,
    VideoAssembler,
    AutonomousVideoStudio,
)

__all__ = [
    "VideoLanguage",
    "VideoPresentationMode",
    "VideoDurationTier",
    "SceneSegment",
    "VideoScriptPackage",
    "ScriptArchitect",
    "VoiceProfile",
    "AudioDuckingProfile",
    "SubtitleCue",
    "MultilingualVoiceSynthesizer",
    "AspectRatio",
    "VideoRenderSpec",
    "RenderJobManifest",
    "VideoAssembler",
    "AutonomousVideoStudio",
]
