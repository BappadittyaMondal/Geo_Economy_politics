"""
Headless Audio Stream & Media Transcript Connector.
Bypasses dynamic client-side JavaScript lockouts on YouTube, podcasts, and video URLs,
providing headless transcript extraction, timestamped parsing, and automated ClaimItem normalization.
"""

import hashlib
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from .transcript_engine import TranscriptResult, TranscriptSegment, VideoTranscriptEngine
from .url_parser import YouTubeURLParser
from ..ingestion.models import ClaimItem, ClaimType
from ..ingestion.telemetry_adapter import MacroTelemetryAdapter
from ..core.models import EpistemicTier
from ..storage.event_store import EventStore


class AudioStreamMetadata(BaseModel):
    """Metadata for an external audio/video media stream."""
    media_id: str
    source_url: str
    source_type: str = "youtube"  # 'youtube', 'podcast', 'stream', 'audio_file'
    title: Optional[str] = None
    duration_seconds: Optional[float] = None
    language: str = "en"


class AudioTranscript(BaseModel):
    """Structured transcript output from an audio or video stream."""
    media_id: str
    source_url: Optional[str] = None
    language: str = "en"
    full_text: str = ""
    segments: List[TranscriptSegment] = Field(default_factory=list)
    is_degraded: bool = False
    is_simulated: bool = False
    extraction_method: str = "caption_stream"


class AudioStreamConnector:
    """
    Connects to external media URLs, bypassing dynamic client-side JavaScript lockouts
    by extracting caption tracks, headless metadata, or streaming transcript segments,
    and transforming them into verified ClaimItem records for the multi-lens engine.
    """

    @classmethod
    def extract_media_id(cls, url_or_id: str) -> str:
        """
        Extracts a clean 11-character YouTube video ID or generates a deterministic
        media ID hash for arbitrary media/audio URLs.
        """
        raw = str(url_or_id).strip()
        # Direct 11-char YouTube ID match
        if re.match(r"^[a-zA-Z0-9_-]{11}$", raw):
            return raw

        try:
            parsed = YouTubeURLParser.parse(raw)
            return parsed["video_id"]
        except Exception:
            # Fallback for podcast, audio stream, or non-standard media URLs
            media_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:11]
            return f"MED-{media_hash}"

    @classmethod
    def fetch_stream_transcript(
        cls,
        url_or_id: str,
        preferred_languages: Optional[List[str]] = None,
        metadata_fallback: Optional[Dict[str, Any]] = None
    ) -> AudioTranscript:
        """
        Headless extraction of timestamped transcript from video/audio stream URL.
        Bypasses client-side minified JS lockouts using YouTube caption tracks and fallback heuristics.
        """
        media_id = cls.extract_media_id(url_or_id)
        langs = preferred_languages or ["en", "hi"]

        result: TranscriptResult = VideoTranscriptEngine.fetch_transcript(
            video_id=media_id,
            preferred_languages=langs,
            metadata_fallback=metadata_fallback
        )

        return AudioTranscript(
            media_id=media_id,
            source_url=url_or_id if url_or_id.startswith("http") else None,
            language=result.language,
            full_text=result.full_text,
            segments=result.segments,
            is_degraded=result.is_degraded,
            is_simulated=result.is_simulated,
            extraction_method=result.fallback_mode or "caption_stream"
        )

    @classmethod
    def transcript_to_claims(
        cls,
        transcript: AudioTranscript,
        target_lenses: Optional[List[str]] = None,
        default_reliability: float = 0.85
    ) -> List[ClaimItem]:
        """
        Transforms transcript segments into epistemically tiered ClaimItem records
        suitable for ingestion into the SQLite EventStore and multi-lens evaluators.
        """
        raw_records = []
        # Group transcript segments into ~30-60 second chunks for coherent claim representation
        chunk_text = []
        chunk_start = 0.0
        chunk_idx = 0

        for seg in transcript.segments:
            chunk_text.append(seg.text)
            if (seg.start - chunk_start) >= 45.0 or seg == transcript.segments[-1]:
                combined = " ".join(chunk_text).strip()
                if combined:
                    raw_records.append({
                        "id": f"AUD-{transcript.media_id}-{chunk_idx:02d}",
                        "text": combined,
                        "source_id": f"SRC-AUDIO-{transcript.media_id}",
                        "target_lenses": target_lenses or ["InstitutionalLawfareLens", "GeopoliticalLens"],
                        "reliability_weight": default_reliability
                    })
                    chunk_idx += 1
                chunk_text = []
                chunk_start = seg.end

        if not raw_records and transcript.full_text:
            raw_records.append({
                "id": f"AUD-{transcript.media_id}-00",
                "text": transcript.full_text[:500],
                "source_id": f"SRC-AUDIO-{transcript.media_id}",
                "target_lenses": target_lenses or ["InstitutionalLawfareLens", "GeopoliticalLens"],
                "reliability_weight": default_reliability
            })

        return MacroTelemetryAdapter.normalize_telemetry(raw_records)

    @classmethod
    def ingest_media_url(
        cls,
        url_or_id: str,
        store: Optional[EventStore] = None,
        metadata_fallback: Optional[Dict[str, Any]] = None,
        target_lenses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        High-level pipeline: fetches transcript for media URL, normalizes into ClaimItems,
        and persists into the EventStore. Returns summary ingestion statistics.
        """
        target_store = store or EventStore()
        transcript = cls.fetch_stream_transcript(url_or_id, metadata_fallback=metadata_fallback)
        claims = cls.transcript_to_claims(transcript, target_lenses=target_lenses)

        ingested_count = MacroTelemetryAdapter.ingest_to_event_store(claims, store=target_store)

        return {
            "media_id": transcript.media_id,
            "language": transcript.language,
            "extraction_method": transcript.extraction_method,
            "is_degraded": transcript.is_degraded,
            "total_segments": len(transcript.segments),
            "claims_generated": len(claims),
            "claims_ingested": ingested_count
        }
