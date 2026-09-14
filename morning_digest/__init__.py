"""
Morning Digest and Telegram Delivery Package.
Decoupled automation for morning news ingestion, strategic relevance ranking (Stage A),
and Telegram briefing publication (Stage B).
"""

from .ranker import StrategicNewsRanker
from .bot import TelegramDigestPublisher

__all__ = ["StrategicNewsRanker", "TelegramDigestPublisher"]
