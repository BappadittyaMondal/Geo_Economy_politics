"""
Autonomous Sovereign Video Studio: Video Assembly & Rendering Orchestrator.
Compiles scene assets, Ken Burns motion, subtitles, and multi-track audio into
production-ready MP4 packages with multi-language switching for YouTube & Facebook.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .script_architect import (
    VideoLanguage,
    VideoPresentationMode,
    VideoScriptPackage,
    ScriptArchitect,
)
from .voice_synthesizer import (
    MultilingualVoiceSynthesizer,
    AudioDuckingProfile,
)


class AspectRatio(str, Enum):
    """Target video framing aspect ratios."""
    LANDSCAPE_16_9 = "16:9"     # YouTube standard (1920x1080)
    PORTRAIT_9_16 = "9:16"       # YouTube Shorts / Instagram / FB Reels (1080x1920)
    SQUARE_1_1 = "1:1"           # Social media feed (1080x1080)


@dataclass
class VideoRenderSpec:
    """Technical video rendering parameters."""
    aspect_ratio: AspectRatio = AspectRatio.LANDSCAPE_16_9
    resolution_width: int = 1920
    resolution_height: int = 1080
    fps: int = 30
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    enable_subtitles: bool = True
    crf: int = 21  # Constant Rate Factor for crisp broadcast quality

    def to_dict(self) -> Dict[str, Any]:
        return {
            "aspect_ratio": self.aspect_ratio.value,
            "resolution_width": self.resolution_width,
            "resolution_height": self.resolution_height,
            "fps": self.fps,
            "video_codec": self.video_codec,
            "audio_codec": self.audio_codec,
            "enable_subtitles": self.enable_subtitles,
            "crf": self.crf,
        }


@dataclass
class RenderJobManifest:
    """Complete executable rendering manifest for FFmpeg or local video backends."""
    manifest_id: str
    package_id: str
    spec: VideoRenderSpec
    total_scenes: int
    duration_sec: float
    audio_track_languages: List[str]
    subtitles_by_language: Dict[str, str]
    multi_audio_mux_command: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "package_id": self.package_id,
            "spec": self.spec.to_dict(),
            "total_scenes": self.total_scenes,
            "duration_sec": self.duration_sec,
            "audio_track_languages": self.audio_track_languages,
            "subtitles_by_language": self.subtitles_by_language,
            "multi_audio_mux_command": self.multi_audio_mux_command,
            "metadata": self.metadata,
        }


class VideoAssembler:
    """Orchestrates asset concatenation, motion graphics, and audio multiplexing."""

    @classmethod
    def build_render_manifest(
        cls,
        script_package: VideoScriptPackage,
        spec: Optional[VideoRenderSpec] = None,
    ) -> RenderJobManifest:
        """
        Builds the complete render manifest and multi-audio FFmpeg recipes.
        """
        render_spec = spec or VideoRenderSpec()
        manifest_id = "MNF-" + script_package.package_id[4:]

        # Build subtitle SRT files for each language
        subtitles: Dict[str, str] = {}
        for lang in script_package.supported_languages:
            cues = MultilingualVoiceSynthesizer.generate_subtitle_cues(script_package.scenes, lang)
            subtitles[lang.value] = MultilingualVoiceSynthesizer.export_srt_content(cues)

        # Build FFmpeg multi-track audio multiplexing command recipe
        # Enables YouTube's native Multi-Language Audio Track feature!
        lang_codes = [l.value for l in script_package.supported_languages]
        
        # Audio mapping flags: -map 0:v -map 1:a -map 2:a ...
        map_args = ["-map 0:v"]
        meta_args = []
        for idx, l_code in enumerate(lang_codes, start=1):
            map_args.append(f"-map {idx}:a")
            meta_args.append(f"-metadata:s:a:{idx-1} language={l_code}")
            meta_args.append(f"-metadata:s:a:{idx-1} title=\"{l_code.upper()}\"")

        input_files = ["-i video_base.mp4"] + [f"-i audio_{l}.mp3" for l in lang_codes]
        mux_cmd = (
            f"ffmpeg -y {' '.join(input_files)} "
            f"{' '.join(map_args)} -c:v copy -c:a aac "
            f"{' '.join(meta_args)} output_multiaudio_{manifest_id}.mp4"
        )

        return RenderJobManifest(
            manifest_id=manifest_id,
            package_id=script_package.package_id,
            spec=render_spec,
            total_scenes=len(script_package.scenes),
            duration_sec=float(script_package.target_duration_sec),
            audio_track_languages=lang_codes,
            subtitles_by_language=subtitles,
            multi_audio_mux_command=mux_cmd,
            metadata={
                "title": script_package.title,
                "presentation_mode": script_package.presentation_mode.value,
                "domain": script_package.metadata.get("domain", "GENERAL"),
            }
        )


class AutonomousVideoStudio:
    """
    High-level facade for autonomous sovereign video creation.
    Takes a single prompt and delivers a complete broadcast-ready production package.
    """

    @classmethod
    def produce_video_package(
        cls,
        topic_or_prompt: str,
        presentation_mode: VideoPresentationMode = VideoPresentationMode.FACELESS_DOCUMENTARY,
        target_duration_minutes: int = 3,
        languages: Optional[List[VideoLanguage]] = None,
        aspect_ratio: AspectRatio = AspectRatio.LANDSCAPE_16_9,
    ) -> Dict[str, Any]:
        """
        Executes end-to-end studio pipeline:
        1. Script & Scene Architecture (ScriptArchitect)
        2. Multilingual Voice & Subtitle Synthesis (MultilingualVoiceSynthesizer)
        3. Video Assembly & Multi-Track Audio Multiplexing (VideoAssembler)
        """
        # Step 1: Script & Storyboarding
        script_package = ScriptArchitect.create_script_package(
            topic_or_prompt=topic_or_prompt,
            presentation_mode=presentation_mode,
            target_duration_minutes=target_duration_minutes,
            languages=languages,
        )

        # Step 2: Render Spec Calibration
        width, height = (1920, 1080) if aspect_ratio == AspectRatio.LANDSCAPE_16_9 else (1080, 1920)
        spec = VideoRenderSpec(
            aspect_ratio=aspect_ratio,
            resolution_width=width,
            resolution_height=height,
        )

        # Step 3: Render Manifest
        manifest = VideoAssembler.build_render_manifest(script_package, spec)

        # Step 4: Audio Ducking Profile
        ducking = MultilingualVoiceSynthesizer.calculate_ducked_audio_mix(
            float(script_package.target_duration_sec)
        )

        return {
            "status": "PRODUCTION_READY",
            "package_id": script_package.package_id,
            "manifest_id": manifest.manifest_id,
            "title": script_package.title,
            "topic": script_package.topic,
            "presentation_mode": script_package.presentation_mode.value,
            "duration_minutes": target_duration_minutes,
            "duration_sec": script_package.target_duration_sec,
            "total_scenes": len(script_package.scenes),
            "supported_languages": [l.value for l in script_package.supported_languages],
            "word_counts": script_package.word_counts,
            "script_package": script_package.to_dict(),
            "render_manifest": manifest.to_dict(),
            "ducking_profile": ducking,
        }
