"""
Autonomous Sovereign Video Studio: Multilingual Voice & Acoustic Synthesizer.
Orchestrates neural speech generation, word-level subtitle generation (.srt/.vtt),
and background music audio ducking across English, Hindi, Bengali, and Sanskrit.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .script_architect import VideoLanguage, SceneSegment


@dataclass
class VoiceProfile:
    """Neural text-to-speech voice configuration."""
    language: VideoLanguage
    voice_id: str
    display_name: str
    gender: str
    rate: str = "+0%"
    pitch: str = "+0Hz"
    volume: str = "+0%"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "language": self.language.value,
            "voice_id": self.voice_id,
            "display_name": self.display_name,
            "gender": self.gender,
            "rate": self.rate,
            "pitch": self.pitch,
            "volume": self.volume,
        }


@dataclass
class AudioDuckingProfile:
    """Acoustic parameter profile for mixing voiceover and background score."""
    speech_volume_db: float = 0.0
    music_volume_db: float = -18.0
    ducking_floor_db: float = -26.0
    fade_in_duration_sec: float = 1.0
    fade_out_duration_sec: float = 2.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "speech_volume_db": self.speech_volume_db,
            "music_volume_db": self.music_volume_db,
            "ducking_floor_db": self.ducking_floor_db,
            "fade_in_duration_sec": self.fade_in_duration_sec,
            "fade_out_duration_sec": self.fade_out_duration_sec,
        }


@dataclass
class SubtitleCue:
    """Synchronized subtitle line with millisecond precision."""
    index: int
    start_time_sec: float
    end_time_sec: float
    text: str

    def to_srt_time(self, seconds: float) -> str:
        """Formats seconds into standard SRT timestamp HH:MM:SS,mmm."""
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milli = int(round((seconds - int(seconds)) * 1000))
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{milli:03d}"

    def to_srt_entry(self) -> str:
        """Renders single SRT block."""
        return f"{self.index}\n{self.to_srt_time(self.start_time_sec)} --> {self.to_srt_time(self.end_time_sec)}\n{self.text}\n"


class MultilingualVoiceSynthesizer:
    """
    Manages neural speech profiles and acoustic mixing protocols for multi-lingual broadcast.
    """

    VOICE_CATALOG: Dict[str, VoiceProfile] = {
        # English
        "en_male": VoiceProfile(VideoLanguage.ENGLISH, "en-IN-PrabhatNeural", "Prabhat (Indian English Male)", "MALE"),
        "en_female": VoiceProfile(VideoLanguage.ENGLISH, "en-IN-NeerjaNeural", "Neerja (Indian English Female)", "FEMALE"),
        "en_us_male": VoiceProfile(VideoLanguage.ENGLISH, "en-US-GuyNeural", "Guy (US English Male)", "MALE"),

        # Hindi
        "hi_male": VoiceProfile(VideoLanguage.HINDI, "hi-IN-MadhurNeural", "Madhur (Hindi Male)", "MALE"),
        "hi_female": VoiceProfile(VideoLanguage.HINDI, "hi-IN-SwaraNeural", "Swara (Hindi Female)", "FEMALE"),

        # Bengali
        "bn_male": VoiceProfile(VideoLanguage.BENGALI, "bn-IN-BashkarNeural", "Bashkar (Bengali Male)", "MALE"),
        "bn_female": VoiceProfile(VideoLanguage.BENGALI, "bn-IN-TanishaaNeural", "Tanishaa (Bengali Female)", "FEMALE"),

        # Sanskrit (Phonetically mapped to classical Devanagari high-clarity neural models)
        "sa_male": VoiceProfile(VideoLanguage.SANSKRIT, "hi-IN-MadhurNeural", "Madhur Vedic (Sanskrit Male)", "MALE", rate="-8%"),
        "sa_female": VoiceProfile(VideoLanguage.SANSKRIT, "hi-IN-SwaraNeural", "Swara Vedic (Sanskrit Female)", "FEMALE", rate="-8%"),
    }

    @classmethod
    def get_voice_profile(cls, language: VideoLanguage, gender: str = "MALE") -> VoiceProfile:
        """Retrieves optimal neural voice profile for a language and gender."""
        key = f"{language.value}_{gender.lower()}"
        return cls.VOICE_CATALOG.get(key, cls.VOICE_CATALOG["en_male"])

    @classmethod
    def generate_subtitle_cues(cls, scenes: List[SceneSegment], language: VideoLanguage) -> List[SubtitleCue]:
        """Generates synchronized SubtitleCues from scene segments for a given language."""
        cues: List[SubtitleCue] = []
        for s in scenes:
            text = s.spoken_text.get(language.value, "")
            if text:
                cues.append(SubtitleCue(
                    index=s.scene_id,
                    start_time_sec=s.timestamp_start_sec,
                    end_time_sec=s.timestamp_end_sec,
                    text=text,
                ))
        return cues

    @classmethod
    def export_srt_content(cls, cues: List[SubtitleCue]) -> str:
        """Renders complete SRT subtitle file text."""
        return "\n".join(cue.to_srt_entry() for cue in cues)

    @classmethod
    def calculate_ducked_audio_mix(
        cls,
        total_duration_sec: float,
        ducking_profile: Optional[AudioDuckingProfile] = None
    ) -> Dict[str, Any]:
        """
        Calculates mathematical parameters for dynamic background audio ducking.
        """
        prof = ducking_profile or AudioDuckingProfile()
        return {
            "total_duration_sec": total_duration_sec,
            "speech_volume_db": prof.speech_volume_db,
            "music_volume_db": prof.music_volume_db,
            "ducking_floor_db": prof.ducking_floor_db,
            "fade_in_sec": prof.fade_in_duration_sec,
            "fade_out_sec": prof.fade_out_duration_sec,
            "filter_complex_recipe": (
                f"[1:a]volume={prof.music_volume_db}dB,afade=t=in:st=0:d={prof.fade_in_duration_sec},"
                f"afade=t=out:st={total_duration_sec - prof.fade_out_duration_sec}:d={prof.fade_out_duration_sec}[bg];"
                f"[0:a][bg]amix=inputs=2:duration=first[aout]"
            ),
        }
