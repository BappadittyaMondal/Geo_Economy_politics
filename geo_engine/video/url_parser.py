"""
YouTube URL parser and sanitization engine.
Validates YouTube domains, extracts 11-character video identifiers, and parses start timestamps safely.
"""

import re
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse


class YouTubeURLParser:
    """Safe parser for YouTube URLs with domain validation and timestamp parsing."""

    ALLOWED_DOMAINS = {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtu.be",
        "www.youtu.be"
    }

    VIDEO_ID_REGEX = re.compile(r"^[a-zA-Z0-9_-]{11}$")

    @classmethod
    def extract_start_seconds(cls, time_str: str) -> int:
        """Parses time strings like '120s', '2m15s', '1h2m3s', or '120' into total seconds."""
        if not time_str:
            return 0
        time_str = str(time_str).strip().lower()
        if time_str.isdigit():
            return int(time_str)

        total = 0
        h_match = re.search(r"(\d+)h", time_str)
        if h_match:
            total += int(h_match.group(1)) * 3600
        m_match = re.search(r"(\d+)m", time_str)
        if m_match:
            total += int(m_match.group(1)) * 60
        s_match = re.search(r"(\d+)s", time_str)
        if s_match:
            total += int(s_match.group(1))
        return total if total > 0 else (int(time_str) if time_str.isdigit() else 0)

    @classmethod
    def parse(cls, url: str) -> Dict[str, Any]:
        """
        Parses and validates a YouTube URL.
        Returns a dict with 'video_id', 'start_seconds', and 'canonical_url'.
        Raises ValueError if invalid or untrusted domain.
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string.")

        parsed = urlparse(url.strip())
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Invalid URL scheme: {parsed.scheme}")

        hostname = (parsed.hostname or "").lower()
        if hostname not in cls.ALLOWED_DOMAINS:
            raise ValueError(f"Untrusted YouTube domain: {hostname}")

        video_id: Optional[str] = None
        start_seconds: int = 0

        # Case 1: youtu.be/VIDEO_ID
        if "youtu.be" in hostname:
            path_parts = parsed.path.strip("/").split("/")
            if path_parts and path_parts[0]:
                video_id = path_parts[0]
            # check ?t= in query
            qs = parse_qs(parsed.query)
            if "t" in qs:
                start_seconds = cls.extract_start_seconds(qs["t"][0])

        # Case 2: youtube.com/watch?v=VIDEO_ID or youtube.com/embed/VIDEO_ID
        else:
            qs = parse_qs(parsed.query)
            if "v" in qs:
                video_id = qs["v"][0]
            elif parsed.path.startswith("/embed/"):
                parts = parsed.path.split("/embed/")
                if len(parts) > 1:
                    video_id = parts[1].split("/")[0].split("?")[0]
            elif parsed.path.startswith("/v/"):
                parts = parsed.path.split("/v/")
                if len(parts) > 1:
                    video_id = parts[1].split("/")[0].split("?")[0]

            if "t" in qs:
                start_seconds = cls.extract_start_seconds(qs["t"][0])
            elif "start" in qs:
                start_seconds = cls.extract_start_seconds(qs["start"][0])

        if not video_id or not cls.VIDEO_ID_REGEX.match(video_id):
            raise ValueError(f"Invalid or missing 11-character YouTube video ID: {video_id}")

        canonical_url = f"https://www.youtube.com/watch?v={video_id}"
        return {
            "video_id": video_id,
            "start_seconds": start_seconds,
            "canonical_url": canonical_url
        }
