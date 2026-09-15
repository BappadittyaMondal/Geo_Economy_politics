"""
Centralized Configuration for the Geo-Engine.
All environment variables, defaults, and runtime settings in one place.
Uses Pydantic for validation. Import via: from geo_engine.config import settings
"""

import os
from datetime import datetime
from typing import Optional


class GeoEngineSettings:
    """Runtime configuration read from environment variables with validated defaults."""

    @property
    def system_reference_date(self) -> datetime:
        """Reference date for temporal guardrails. Default: 2026-09-14."""
        raw = os.environ.get("SYSTEM_REFERENCE_DATE", "")
        if raw:
            try:
                return datetime.fromisoformat(raw)
            except ValueError:
                pass
        return datetime(2026, 9, 14)

    @property
    def db_path(self) -> str:
        """Path to SQLite knowledge base."""
        default = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "events.db"
        )
        return os.environ.get("GEO_ENGINE_DB_PATH", default)

    @property
    def telegram_bot_token(self) -> Optional[str]:
        """Telegram Bot API token for morning digest dispatch."""
        return os.environ.get("TELEGRAM_BOT_TOKEN")

    @property
    def telegram_chat_id(self) -> Optional[str]:
        """Telegram chat ID for dispatch target."""
        return os.environ.get("TELEGRAM_CHAT_ID")

    @property
    def inr_usd_rate(self) -> float:
        """INR/USD exchange rate for financial normalization. Default: 83.5."""
        raw = os.environ.get("INR_USD_RATE", "83.5")
        try:
            return float(raw)
        except ValueError:
            return 83.5

    @property
    def max_query_length(self) -> int:
        """Maximum allowed query string length. Default: 5000."""
        return int(os.environ.get("GEO_ENGINE_MAX_QUERY_LENGTH", "5000"))

    @property
    def lens_count(self) -> int:
        """Current number of registered analytical lenses."""
        return 20

    @property
    def version(self) -> str:
        """Engine version string."""
        return "0.40.0"


# Singleton instance
settings = GeoEngineSettings()
