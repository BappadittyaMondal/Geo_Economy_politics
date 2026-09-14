"""
Evidence Ingestion Data Models.
Defines verified evidentiary records, source categories, provenance metadata,
and reliability weighting for raw inputs ingested into the Geo-Engine.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


from ..core.models import EpistemicTier


class ClaimType(str, Enum):
    """Categorizes the nature of the claim to apply claim-aware epistemic hierarchy."""
    PHYSICAL_PRESENCE = "PHYSICAL_PRESENCE"      # Troop deployments, oil tankers, chokepoints
    FINANCIAL_CAPEX = "FINANCIAL_CAPEX"          # Central bank entries, VOSTRO, budget allocations
    LEGAL_COMMITMENT = "LEGAL_COMMITMENT"        # Ratified treaties, statutory laws, formal communiques
    RHETORICAL_POSTURE = "RHETORICAL_POSTURE"    # Speeches, press conferences, state media narrative
    KINESIC_MICRO_SIGNAL = "KINESIC_MICRO_SIGNAL" # Handshakes, spatial proxemics, body language
    GENERAL_INTEL = "GENERAL_INTEL"              # General background reporting


class EvidenceItem(BaseModel):
    """An atomic verified evidentiary record ingested from open sources or documents."""
    evidence_id: str
    source_name: str = Field(..., description="e.g., 'India MEA', 'China MFA', 'GDELT 2.0', 'BIS Data'")
    source_type: str = Field(..., description="'official_gazette', 'news_wire', 'treaty_text', 'satellite_ais', 'central_bank'")
    timestamp: str
    raw_text: str
    provenance_url: Optional[str] = None
    reliability_weight: float = Field(default=0.80, ge=0.0, le=1.0)
    entities_mentioned: List[str] = Field(default_factory=list)
    claim_type: ClaimType = ClaimType.GENERAL_INTEL
    evidence_status: str = Field(default="sufficient", description="'sufficient', 'degraded', 'insufficient'")

    @property
    def is_primary_sovereign(self) -> bool:
        """True if directly sourced from a primary sovereign gazette, ministry, or central bank."""
        return self.source_type in ["official_gazette", "treaty_text", "central_bank", "satellite_ais"]


class ClaimItem(BaseModel):
    """A normalized, structured analytical claim extracted from raw evidence."""
    claim_id: str
    source_evidence_id: str
    claim_type: ClaimType
    epistemic_tier: EpistemicTier
    actors: List[str] = Field(default_factory=list)
    asserted_fact: str
    extracted_financial_mou_usd: Optional[float] = None
    is_binding_commitment: bool = False
    extracted_physical_units: Optional[str] = None
    target_lenses: List[str] = Field(default_factory=list)
    reliability_weight: float = Field(default=0.8, ge=0.0, le=1.0)
    evidence_status: str = Field(default="sufficient", description="'sufficient', 'degraded', 'insufficient'")
