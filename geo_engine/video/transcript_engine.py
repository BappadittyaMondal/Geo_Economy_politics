"""
Transcript retrieval engine for YouTube videos.
Supports extraction of timestamped caption segments with resilient fallback for offline/simulated analysis.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TranscriptSegment(BaseModel):
    """A single timestamped caption segment from a video transcript."""
    text: str
    start: float
    duration: float

    @property
    def end(self) -> float:
        return self.start + self.duration

    @property
    def timestamp_str(self) -> str:
        """Formats start time as MM:SS or HH:MM:SS."""
        total_seconds = int(self.start)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"


class TranscriptResult(BaseModel):
    """Container for parsed video transcript segments."""
    video_id: str
    segments: List[TranscriptSegment] = Field(default_factory=list)
    language: str = "en"
    is_simulated: bool = False
    is_degraded: bool = False
    fallback_mode: Optional[str] = None

    @property
    def full_text(self) -> str:
        return " ".join(s.text.strip() for s in self.segments if s.text.strip())


class VideoTranscriptEngine:
    """Fetches or simulates timestamped transcripts for YouTube videos."""

    SIMULATED_CORPUS = [
        TranscriptSegment(
            text="Welcome everyone. Today we analyze the shifting dynamics of the Indian Ocean and critical maritime routes.",
            start=0.0,
            duration=12.0
        ),
        TranscriptSegment(
            text="The Malacca Dilemma and the Sunda Strait represent vital chokepoints where energy security meets naval strategy.",
            start=12.0,
            duration=18.0
        ),
        TranscriptSegment(
            text="India's deployment of deep-sea hydrophone arrays and subsea cable protection around the Andaman and Nicobar Islands is pivotal.",
            start=30.0,
            duration=22.0
        ),
        TranscriptSegment(
            text="Looking at the financial ledger, bilateral rupee-dirham settlements and Vostro accounts have insulated petro-imports.",
            start=52.0,
            duration=20.0
        ),
        TranscriptSegment(
            text="Meanwhile, in low Earth orbit, NavIC satellite constellation expansion provides sovereign positioning against external GPS denial.",
            start=72.0,
            duration=24.0
        ),
        TranscriptSegment(
            text="To conclude, strategic autonomy relies not on grand rhetoric, but on hard physical buffers in grain, energy, and subsea cables.",
            start=96.0,
            duration=24.0
        ),
    ]

    @classmethod
    def fetch_transcript(
        cls,
        video_id: str,
        custom_segments: Optional[List[Dict[str, Any]]] = None,
        preferred_languages: Optional[List[str]] = None,
        metadata_fallback: Optional[Dict[str, Any]] = None
    ) -> TranscriptResult:
        """
        Retrieves transcript for a video ID.
        If custom_segments are provided, parses and returns them.
        Attempts youtube_transcript_api if installed.
        If captions are unavailable and metadata_fallback is provided, synthesizes degraded segments from metadata.
        Else returns structured simulated transcript marked with explicit simulation and degradation flags.
        """
        if custom_segments:
            segments = [
                TranscriptSegment(
                    text=str(s.get("text", "")),
                    start=float(s.get("start", 0.0)),
                    duration=float(s.get("duration", 0.0))
                )
                for s in custom_segments
            ]
            return TranscriptResult(
                video_id=video_id,
                segments=segments,
                language="en",
                is_simulated=False,
                is_degraded=False,
                fallback_mode=None
            )

        # Attempt dynamic import of youtube_transcript_api if available
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            langs = preferred_languages or ["en", "hi"]
            fetched = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
            segments = [
                TranscriptSegment(
                    text=item["text"],
                    start=float(item["start"]),
                    duration=float(item.get("duration", 0.0))
                )
                for item in fetched
            ]
            return TranscriptResult(
                video_id=video_id,
                segments=segments,
                language=langs[0],
                is_simulated=False,
                is_degraded=False,
                fallback_mode=None
            )
        except Exception:
            # Check for authentic video metadata fallback before resorting to synthetic corpus
            if metadata_fallback:
                title = metadata_fallback.get("title", "")
                desc = metadata_fallback.get("description", "")
                kws = metadata_fallback.get("keywords", [])
                meta_segments = []
                if title:
                    meta_segments.append(TranscriptSegment(text=f"[METADATA_TITLE] {title}", start=0.0, duration=10.0))
                if desc:
                    meta_segments.append(TranscriptSegment(text=f"[METADATA_DESCRIPTION] {desc[:800]}", start=10.0, duration=30.0))
                if kws:
                    kw_str = ", ".join(kws) if isinstance(kws, list) else str(kws)
                    meta_segments.append(TranscriptSegment(text=f"[METADATA_KEYWORDS] {kw_str}", start=40.0, duration=20.0))
                if meta_segments:
                    return TranscriptResult(
                        video_id=video_id,
                        segments=meta_segments,
                        language="hi" if any(ord(c) > 127 for c in title) else "en",
                        is_simulated=False,
                        is_degraded=True,
                        fallback_mode="video_metadata"
                    )

            # Resilient fallback: return structured simulated transcript with explicit simulation and degradation flags
            return TranscriptResult(
                video_id=video_id,
                segments=cls.SIMULATED_CORPUS,
                language="en",
                is_simulated=True,
                is_degraded=True,
                fallback_mode="synthetic_offline_fixture"
            )
