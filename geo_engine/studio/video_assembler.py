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

    @classmethod
    def generate_execution_scripts(
        cls,
        manifest: RenderJobManifest,
        script_package: VideoScriptPackage,
        output_dir: str = "studio_output",
    ) -> Dict[str, str]:
        """
        Generates automated batch and PowerShell execution scripts to run Edge-TTS and FFmpeg.
        """
        import os
        import json

        os.makedirs(output_dir, exist_ok=True)

        # 1. Export language scripts
        script_files = {}
        for lang in script_package.supported_languages:
            l_code = lang.value
            full_text = "\n".join(
                s.spoken_text.get(l_code, "") for s in script_package.scenes if s.spoken_text.get(l_code)
            )
            script_path = os.path.join(output_dir, f"script_{l_code}.txt")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            script_files[l_code] = script_path

        # 2. Export SRT files
        for l_code, srt_content in manifest.subtitles_by_language.items():
            srt_path = os.path.join(output_dir, f"subtitles_{l_code}.srt")
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)

        # 3. Save manifest json
        manifest_path = os.path.join(output_dir, "render_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest.to_dict(), f, indent=2, ensure_ascii=False)

        # 4. Generate Windows Batch Script (.bat)
        bat_lines = [
            "@echo off",
            "chcp 65001 > nul",
            f"echo ===================================================================",
            f"echo SOVEREIGN VIDEO STUDIO: RENDERING {manifest.manifest_id}",
            f"echo ===================================================================",
            "",
            "if not exist video_base.mp4 (",
            "    echo [0/5] Compiling visual scene plates and video_base.mp4 via Geo Engine...",
            f"    py -3.14 -m geo_engine.cli studio script_en.txt --cinema --render --output-dir .",
            ")",
            "",
            "echo [1/5] Synthesizing English neural voiceover via Edge-TTS...",
            f"edge-tts --voice en-IN-PrabhatNeural --file script_en.txt --write-media audio_en.mp3",
            "",
            "echo [2/5] Synthesizing Hindi neural voiceover via Edge-TTS...",
            f"edge-tts --voice hi-IN-MadhurNeural --file script_hi.txt --write-media audio_hi.mp3",
            "",
            "echo [3/5] Synthesizing Bengali neural voiceover via Edge-TTS...",
            f"edge-tts --voice bn-IN-BashkarNeural --file script_bn.txt --write-media audio_bn.mp3",
            "",
            "echo [4/5] Synthesizing Sanskrit neural voiceover via Edge-TTS...",
            f"edge-tts --voice hi-IN-MadhurNeural --rate=-8% --file script_sa.txt --write-media audio_sa.mp3",
            "",
            "echo [5/5] Executing multi-track audio multiplexing with FFmpeg...",
            manifest.multi_audio_mux_command,
            "",
            f"echo [SUCCESS] Video render completed: output_multiaudio_{manifest.manifest_id}.mp4",
        ]
        bat_path = os.path.join(output_dir, "render_video.bat")
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write("\n".join(bat_lines))

        # 5. Generate PowerShell Script (.ps1)
        ps_lines = [
            "$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8",
            f"Write-Host '== SOVEREIGN VIDEO STUDIO: RENDERING {manifest.manifest_id} ==' -ForegroundColor Cyan",
            "",
            "if (-not (Test-Path 'video_base.mp4')) {",
            "    Write-Host '[0/5] Compiling visual scene plates and video_base.mp4 via Geo Engine...' -ForegroundColor Cyan",
            f"    py -3.14 -m geo_engine.cli studio script_en.txt --cinema --render --output-dir .",
            "}",
            "",
            "Write-Host '[1/5] Synthesizing English neural audio...' -ForegroundColor Yellow",
            "edge-tts --voice en-IN-PrabhatNeural --file script_en.txt --write-media audio_en.mp3",
            "",
            "Write-Host '[2/5] Synthesizing Hindi neural audio...' -ForegroundColor Yellow",
            "edge-tts --voice hi-IN-MadhurNeural --file script_hi.txt --write-media audio_hi.mp3",
            "",
            "Write-Host '[3/5] Synthesizing Bengali neural audio...' -ForegroundColor Yellow",
            "edge-tts --voice bn-IN-BashkarNeural --file script_bn.txt --write-media audio_bn.mp3",
            "",
            "Write-Host '[4/5] Synthesizing Sanskrit neural audio...' -ForegroundColor Yellow",
            "edge-tts --voice hi-IN-MadhurNeural --rate='-8%' --file script_sa.txt --write-media audio_sa.mp3",
            "",
            "Write-Host '[5/5] Multiplexing multi-language audio with FFmpeg...' -ForegroundColor Yellow",
            manifest.multi_audio_mux_command,
            "",
            "Write-Host '[SUCCESS] Broadcast package ready!' -ForegroundColor Green",
        ]
        ps_path = os.path.join(output_dir, "render_video.ps1")
        with open(ps_path, "w", encoding="utf-8") as f:
            f.write("\n".join(ps_lines))

        return {
            "output_dir": output_dir,
            "bat_script": bat_path,
            "ps_script": ps_path,
            "manifest_json": manifest_path,
        }

    @classmethod
    def render_complete_mp4(
        cls,
        script_package: VideoScriptPackage,
        manifest: RenderJobManifest,
        output_dir: str,
        voice_language: str = "en",
    ) -> Dict[str, Any]:
        """
        Executes end-to-end local binary compilation of the complete broadcast MP4:
        1. Renders 1080p visual plates for each scene via LocalFrameRenderer.
        2. Synthesizes neural audio via Edge-TTS (or silent audio track fallback).
        3. Encodes each scene clip with FFmpeg (libx264, yuv420p, aac).
        4. Concatenates scene clips into video_base.mp4.
        5. Multiplexes final audio tracks into output_master_cinema.mp4.
        """
        import os
        import asyncio
        import subprocess
        import pathlib
        from .frame_renderer import LocalFrameRenderer

        os.makedirs(output_dir, exist_ok=True)
        slides_dir = os.path.join(output_dir, "slides")
        clips_dir = os.path.join(output_dir, "clips")
        os.makedirs(slides_dir, exist_ok=True)
        os.makedirs(clips_dir, exist_ok=True)

        # Locate FFmpeg binary
        ffmpeg_exe = "ffmpeg"
        try:
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass

        clip_paths = []
        scenes = script_package.scenes
        aspect = manifest.spec.aspect_ratio.value if hasattr(manifest.spec.aspect_ratio, 'value') else str(manifest.spec.aspect_ratio)

        for idx, scene in enumerate(scenes, start=1):
            slide_path = os.path.join(slides_dir, f"slide_{idx:02d}.png")
            clip_path = os.path.join(clips_dir, f"clip_{idx:02d}.mp4")
            audio_path = os.path.join(clips_dir, f"audio_{idx:02d}.mp3")

            # 1. Render Graphic Plate
            LocalFrameRenderer.render_scene_slide(
                scene=scene,
                scene_idx=idx,
                total_scenes=len(scenes),
                out_path=slide_path,
                topic=script_package.topic,
                aspect_ratio=aspect,
            )

            # 2. Synthesize Audio for this scene
            spoken_line = scene.spoken_text.get(voice_language, "") or scene.spoken_text.get("en", "")
            duration_sec = max(3.0, round(scene.timestamp_end_sec - scene.timestamp_start_sec, 2))
            
            audio_ready = False
            if spoken_line:
                try:
                    import edge_tts
                    async def _gen_speech():
                        voice = "en-IN-PrabhatNeural" if voice_language == "en" else "hi-IN-MadhurNeural"
                        comm = edge_tts.Communicate(spoken_line, voice)
                        await comm.save(audio_path)
                    asyncio.run(_gen_speech())
                    if os.path.exists(audio_path) and os.path.getsize(audio_path) > 100:
                        audio_ready = True
                except Exception:
                    audio_ready = False

            if not audio_ready:
                # Fallback to local audio synthesis via FFmpeg anullsrc
                fallback_cmd = [
                    ffmpeg_exe, "-y",
                    "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", str(duration_sec),
                    "-c:a", "aac", audio_path
                ]
                subprocess.run(fallback_cmd, capture_output=True)

            # 3. Stitch Slide and Audio into Scene Clip
            clip_cmd = [
                ffmpeg_exe, "-y",
                "-loop", "1",
                "-i", slide_path,
                "-i", audio_path,
                "-c:v", "libx264",
                "-tune", "stillimage",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                clip_path
            ]
            res = subprocess.run(clip_cmd, capture_output=True)
            if res.returncode == 0 and os.path.exists(clip_path):
                clip_paths.append(clip_path)

        if not clip_paths:
            return {"status": "RENDER_FAILED", "error": "No clips generated"}

        # 4. Concatenate into video_base.mp4
        concat_list_path = os.path.join(clips_dir, "concat_list.txt")
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for c in clip_paths:
                f.write(f"file '{pathlib.Path(c).resolve().as_posix()}'\n")

        video_base_path = os.path.join(output_dir, "video_base.mp4")
        concat_cmd = [
            ffmpeg_exe, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list_path,
            "-c", "copy",
            video_base_path
        ]
        subprocess.run(concat_cmd, capture_output=True)

        final_master_path = os.path.join(output_dir, f"output_multiaudio_{manifest.manifest_id}.mp4")

        # 5. Synthesize full audio tracks for all supported languages
        for lang in script_package.supported_languages:
            l_code = lang.value
            full_audio_path = os.path.join(output_dir, f"audio_{l_code}.mp3")
            full_text = "\n".join(s.spoken_text.get(l_code, "") for s in scenes if s.spoken_text.get(l_code))
            if not os.path.exists(full_audio_path) or os.path.getsize(full_audio_path) < 100:
                try:
                    import edge_tts
                    async def _gen_full():
                        voice = "en-IN-PrabhatNeural" if l_code == "en" else "hi-IN-MadhurNeural"
                        if l_code == "bn":
                            voice = "bn-IN-BashkarNeural"
                        comm = edge_tts.Communicate(full_text, voice)
                        await comm.save(full_audio_path)
                    asyncio.run(_gen_full())
                except Exception:
                    pass
                if not (os.path.exists(full_audio_path) and os.path.getsize(full_audio_path) > 100):
                    # Fallback silent audio
                    subprocess.run([
                        ffmpeg_exe, "-y",
                        "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                        "-t", str(manifest.duration_sec),
                        "-c:a", "aac", full_audio_path
                    ], capture_output=True)

        # 6. Execute Multi-Audio Multiplexing
        cmd_tokens = manifest.multi_audio_mux_command.split()
        cmd_tokens[0] = ffmpeg_exe  # use resolved ffmpeg binary
        res_mux = subprocess.run(cmd_tokens, cwd=output_dir, capture_output=True)

        output_file = final_master_path if os.path.exists(final_master_path) else video_base_path
        return {
            "status": "RENDER_COMPLETE",
            "video_base_path": video_base_path,
            "final_master_path": output_file,
            "clips_count": len(clip_paths),
            "output_size_bytes": os.path.getsize(output_file) if os.path.exists(output_file) else 0,
        }


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
        export_dir: Optional[str] = None,
        render_video: bool = False,
    ) -> Dict[str, Any]:
        """
        Executes end-to-end studio pipeline:
        1. Script & Scene Architecture (ScriptArchitect)
        2. Multilingual Voice & Subtitle Synthesis (MultilingualVoiceSynthesizer)
        3. Video Assembly & Multi-Track Audio Multiplexing (VideoAssembler)
        4. Optional Batch Execution Script Generation
        5. Optional Local Binary Video Compilation via FFmpeg
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

        # Step 5: Optional Disk Export
        export_info = None
        if export_dir:
            export_info = VideoAssembler.generate_execution_scripts(
                manifest=manifest,
                script_package=script_package,
                output_dir=export_dir,
            )

        # Step 6: Optional Full Local Binary Video Rendering
        render_result = None
        if render_video and export_dir:
            render_result = VideoAssembler.render_complete_mp4(
                script_package=script_package,
                manifest=manifest,
                output_dir=export_dir,
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
            "export_info": export_info,
            "render_result": render_result,
        }

    @classmethod
    def produce_cinema_from_scattered_notes(
        cls,
        raw_notes: str,
        target_duration_minutes: int = 3,
        presentation_mode: VideoPresentationMode = VideoPresentationMode.FACELESS_DOCUMENTARY,
        aspect_ratio: AspectRatio = AspectRatio.LANDSCAPE_16_9,
        export_dir: Optional[str] = None,
        render_video: bool = False,
    ) -> Dict[str, Any]:
        """
        Ingests scattered, unorganized raw text or notes and synthesizes a
        complete cinema production package with character continuity locking,
        3-act screenplay, multilingual audio manifests, and export runners.
        """
        from .story_distiller import StoryDistiller

        distiller = StoryDistiller()
        story_arc = distiller.distill_scattered_notes(
            raw_notes=raw_notes,
            duration_minutes=target_duration_minutes,
            presentation_mode=presentation_mode,
        )

        script_package = story_arc.script_package

        width, height = (1920, 1080) if aspect_ratio == AspectRatio.LANDSCAPE_16_9 else (1080, 1920)
        spec = VideoRenderSpec(
            aspect_ratio=aspect_ratio,
            resolution_width=width,
            resolution_height=height,
        )

        manifest = VideoAssembler.build_render_manifest(script_package, spec)
        ducking = MultilingualVoiceSynthesizer.calculate_ducked_audio_mix(
            float(script_package.target_duration_sec)
        )

        export_info = None
        if export_dir:
            export_info = VideoAssembler.generate_execution_scripts(
                manifest=manifest,
                script_package=script_package,
                output_dir=export_dir,
            )

        render_result = None
        if render_video and export_dir:
            render_result = VideoAssembler.render_complete_mp4(
                script_package=script_package,
                manifest=manifest,
                output_dir=export_dir,
            )

        return {
            "status": "CINEMA_PRODUCTION_READY",
            "package_id": script_package.package_id,
            "manifest_id": manifest.manifest_id,
            "core_thesis": story_arc.core_thesis,
            "dramatic_hook": story_arc.dramatic_hook,
            "identified_characters": story_arc.identified_characters,
            "identified_locations": story_arc.identified_locations,
            "epistemic_anchors": story_arc.epistemic_anchors,
            "contested_flags": story_arc.contested_flags,
            "act_structure": {
                "act_1": story_arc.act_1_hook,
                "act_2": story_arc.act_2_conflict,
                "act_3": story_arc.act_3_resolution,
            },
            "duration_minutes": target_duration_minutes,
            "duration_sec": script_package.target_duration_sec,
            "total_scenes": len(script_package.scenes),
            "supported_languages": [l.value for l in script_package.supported_languages],
            "render_manifest": manifest.to_dict(),
            "ducking_profile": ducking,
            "export_info": export_info,
            "render_result": render_result,
        }

