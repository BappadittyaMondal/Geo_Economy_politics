"""
Local Storage and Knowledge Base Package for the Geo-Engine.
Provides zero-dependency SQLite persistence for historical events, treaties, and communique baselines.
"""

from .event_store import EventStore

__all__ = ["EventStore"]
