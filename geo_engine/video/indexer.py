"""
Video transcript indexer and chunking module.
Partitions granular transcript segments into coherent, timestamp-referenced chunks with clickable video URLs.
"""

from typing import List
from pydantic import BaseModel, Field
from geo_engine.video.transcript_engine import TranscriptSegment


class VideoChunk(BaseModel):
    """A coherent chunk of video transcript text spanning a defined time window."""
    chunk_id: int
    video_id: str
    start_time: float
    end_time: float
    text: str
    timestamp_str: str
    youtube_url: str
    token_estimate: int = Field(default=0)

    @classmethod
    def create(cls, chunk_id: int, video_id: str, start_time: float, end_time: float, text: str) -> "VideoChunk":
        total_seconds = int(start_time)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        t_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours > 0 else f"{minutes:02d}:{seconds:02d}"
        yt_url = f"https://youtu.be/{video_id}?t={total_seconds}s"
        # Rough token estimate: ~1.3 tokens per word
        word_count = len(text.split())
        return cls(
            chunk_id=chunk_id,
            video_id=video_id,
            start_time=start_time,
            end_time=end_time,
            text=text.strip(),
            timestamp_str=t_str,
            youtube_url=yt_url,
            token_estimate=int(word_count * 1.3)
        )


class VideoIndexer:
    """Indexes granular transcript segments into timestamped chunks."""

    @classmethod
    def index_transcript(
        cls,
        segments: List[TranscriptSegment],
        video_id: str,
        window_seconds: float = 45.0,
        overlap_seconds: float = 10.0
    ) -> List[VideoChunk]:
        """
        Groups transcript segments into rolling time-window chunks.
        Each chunk is annotated with start time, end time, and direct jump URL.
        """
        if not segments:
            return []

        chunks: List[VideoChunk] = []
        chunk_idx = 0
        total_duration = max(s.end for s in segments)
        current_start = 0.0

        while current_start < total_duration:
            current_end = current_start + window_seconds
            matching_segments = [
                s for s in segments
                if (s.start >= current_start and s.start < current_end) or
                   (s.end > current_start and s.end <= current_end) or
                   (s.start <= current_start and s.end >= current_end)
            ]

            if matching_segments:
                combined_text = " ".join(s.text.strip() for s in matching_segments if s.text.strip())
                actual_start = min(s.start for s in matching_segments)
                actual_end = max(s.end for s in matching_segments)
                
                chunk = VideoChunk.create(
                    chunk_id=chunk_idx,
                    video_id=video_id,
                    start_time=actual_start,
                    end_time=actual_end,
                    text=combined_text
                )
                chunks.append(chunk)
                chunk_idx += 1

            current_start += (window_seconds - overlap_seconds)

        return chunks
