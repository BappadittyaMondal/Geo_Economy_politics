"""
Evidence Ingestion Package for the Geo-Engine.
Provides open-access connectors for GDELT 2.0, sovereign RSS feeds, and document loaders.
"""

from .models import ClaimType, EvidenceItem, ClaimItem
from .gdelt_client import GDELTClient
from .sovereign_rss import SovereignRSSClient
from .document_loader import DocumentLoader
from .normalizer import IngestionNormalizer

__all__ = [
    "ClaimType",
    "EvidenceItem",
    "ClaimItem",
    "GDELTClient",
    "SovereignRSSClient",
    "DocumentLoader",
    "IngestionNormalizer",
]
