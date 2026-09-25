"""
Data models and type definitions for the Geo-Engine.
Defines immutable representations for summits, financial flows, kinesics,
negative-space clauses, lens evaluations, and synthesized intelligence reports.
"""

import os
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, computed_field, model_validator


def get_system_reference_date() -> datetime:
    """
    Centralized runtime clock provider to prevent temporal drift across modules.
    Reads SYSTEM_REFERENCE_DATE environment variable (ISO format) if set,
    otherwise defaults to current UTC datetime.
    """
    env_date = os.getenv("SYSTEM_REFERENCE_DATE")
    if env_date:
        try:
            return datetime.fromisoformat(env_date)
        except Exception:
            pass
    # Default baseline reference date for deterministic 2026 horizon modeling
    return datetime(2026, 9, 14, 0, 0, 0)



class EpistemicTier(int, Enum):
    """
    Strict truth arbitration hierarchy.
    Lower numerical values represent higher epistemic priority and supersede higher tiers.
    TIER_0 represents an explicit lack of empirical evidence (degraded / null state).
    """
    TIER_0_INSUFFICIENT_EVIDENCE = 0 # Explicit lack of verifiable empirical telemetry
    TIER_1_PHYSICAL = 1              # Physical reality: troops, oil barrels, chokepoints, hardware
    TIER_2_FINANCIAL = 2             # Verified financial flows: Central bank entries, VOSTRO clearing
    TIER_3_SOVEREIGN_REDLINES = 3    # Formal treaties, statutory law, military alliances, borders
    TIER_4_KINESICS = 4              # Protocol-subtracted micro-signals, posture, spatial vectors
    TIER_5_COMMUNIQUE_PR = 5         # Public declarations, ceremonial photoshoots, state press releases


class TemporalMode(str, Enum):
    """Temporal horizon classification to prevent future-data hallucinations."""
    EMPIRICAL_HISTORICAL = "empirical_historical"  # Past verified events with full archival data
    LIVE_VERIFIED = "live_verified"                # Ongoing events with real-time ingested feeds
    PROSPECTIVE_SCENARIO = "prospective_scenario"  # Future/horizon events (e.g., 2026) modeled game-theoretically


class FinancialFlow(BaseModel):
    """Represents a bilateral or multilateral capital or trade commitment."""
    source_country: str
    target_country: str
    project_name: str
    nominal_mou_usd: float = Field(default=0.0, description="Announced headline figure in USD")
    is_binding_contract: bool = Field(default=False, description="True if legal CapEx contract signed with escrow/budget line")
    clearing_currency: str = Field(default="USD", description="Currency used for trade settlement")
    vostro_nostro_operational: bool = Field(default=False, description="True if operational bilateral bank clearing exists")
    secondary_sanctions_risk_score: float = Field(default=0.0, ge=0.0, le=1.0, description="0=none, 1=severe OFAC risk")

    @computed_field
    @property
    def effective_capex_usd(self) -> float:
        """
        Applies the 85% haircut rule on unfinanced, non-binding MOUs.
        If binding, haircut is reduced based on secondary sanctions discount.
        """
        if not self.is_binding_contract:
            # 85% haircut on headline MOUs
            base = self.nominal_mou_usd * 0.15
        else:
            base = self.nominal_mou_usd

        # Sanctions discount
        discount = 1.0 - (self.secondary_sanctions_risk_score * 0.5)
        return round(base * max(0.0, discount), 2)


class KinesicObservation(BaseModel):
    """Represents a structured kinesic/proxemic observation during a summit interaction."""
    actor_primary: str
    actor_secondary: str
    setting: str = Field(..., description="'formal_photocall', 'bilateral_table', or 'unscripted_corridor'")
    protocol_mandated: bool = Field(default=False, description="True if position/posture is compulsory by state protocol")
    handshake_torque_vector: str = Field(default="neutral_vertical", description="'proactive_forward', 'neutral_vertical', 'defensive_withdrawn'")
    torso_angle_degrees: float = Field(default=0.0, description="0 = directly facing, 90 = angled away towards exit")
    residual_tension_score: float = Field(default=0.0, ge=0.0, le=1.0, description="0.0=relaxed/natural, 1.0=extreme rigid tension")
    micro_expression_flag: str = Field(default="neutral_resting", description="'duchenne_smile', 'jaw_clench', 'gaze_avoidance', 'neutral_resting'")
    sartorial_colour_code: str = Field(default="neutral_charcoal", description="'saffron_civilizational', 'midnight_institutional', 'olive_tactical', 'neutral_charcoal'")
    prosodic_pause_index: float = Field(default=0.0, ge=0.0, le=1.0, description="Pause latency before key sovereign nouns: 0.0=fluid, 1.0=severe hesitation")
    proxemic_distance_tier: str = Field(default="bilateral_parity", description="'intimate_embrace', 'bilateral_parity', 'asymmetric_distant'")
    notes: Optional[str] = None

    @computed_field
    @property
    def genuine_warmth_index(self) -> float:
        """
        Calculates residual warmth after protocol baseline subtraction.
        If mandated by protocol, high warmth is heavily discounted.
        Integrates prosodic pause latency and spatial proxemic distance.
        """
        if self.protocol_mandated:
            # Protocol discount: Staged posture cannot be assumed as genuine affinity
            raw_warmth = (1.0 - self.residual_tension_score) * 0.3
        else:
            raw_warmth = (1.0 - self.residual_tension_score)

        if self.torso_angle_degrees > 45.0:
            raw_warmth *= 0.6
        if self.micro_expression_flag == "jaw_clench" or self.micro_expression_flag == "gaze_avoidance":
            raw_warmth *= 0.3
        if self.prosodic_pause_index > 0.6:
            raw_warmth *= (1.0 - (self.prosodic_pause_index - 0.6) * 0.5)
        if self.proxemic_distance_tier == "intimate_embrace":
            raw_warmth = min(1.0, raw_warmth * 1.15)
        elif self.proxemic_distance_tier == "asymmetric_distant":
            raw_warmth *= 0.75

        return round(max(0.0, min(1.0, raw_warmth)), 3)


class CommuniqueClause(BaseModel):
    """Represents an individual clause parsed from a summit declaration."""
    clause_id: str
    category: str = Field(..., description="'energy', 'finance', 'security', 'institutional_reform', 'territorial'")
    raw_text: str
    present_in_current_summit: bool = True
    historical_baseline_present: bool = True
    dilution_status: str = Field(default="retained_full", description="'retained_full', 'diluted_passive', 'omitted_negative_space'")
    omission_significance: Optional[str] = None


class LensEvaluation(BaseModel):
    """Result of an individual specialized lens analysis."""
    lens_name: str
    alignment_score: float = Field(..., ge=-1.0, le=1.0, description="-1.0 = deep friction/hostile, +1.0 = deep synergy")
    confidence: float = Field(..., ge=0.0, le=1.0)
    primary_epistemic_tier: EpistemicTier
    key_findings: List[str] = Field(default_factory=list)
    hard_metrics: Dict[str, Any] = Field(default_factory=dict)
    evidence_status: str = Field(default="sufficient", description="'sufficient', 'degraded', 'insufficient'")


class MemberCountryAudit(BaseModel):
    """Full 4-dimensional audit for a member state."""
    country_name: str
    public_domestic_narrative: str
    geopolitical_yield: str
    hard_cash_yield_usd: float = 0.0
    concessions_or_vulnerabilities: str
    strategic_autonomy_score: float = Field(default=0.5, ge=0.0, le=1.0)
    key_bilateral_postures: Dict[str, str] = Field(default_factory=dict)


class EventType(str, Enum):
    """Categorizes the primary nature of a strategic event."""
    SUMMIT = "SUMMIT"
    BORDER_SECURITY = "BORDER_SECURITY"
    BORDER_MILITARY = "BORDER_MILITARY"
    GEO_ECONOMIC = "GEO_ECONOMIC"
    CIVILIZATIONAL_CRISIS = "CIVILIZATIONAL_CRISIS"
    HYBRID_WARFARE = "HYBRID_WARFARE"
    STRATEGIC_EVENT = "STRATEGIC_EVENT"


class StrategicEvent(BaseModel):
    """Generalized model for any strategic geopolitical, economic, or security event."""
    title: str = "Strategic Event"
    year: int = 2026
    event_type: EventType = EventType.SUMMIT
    primary_region: str = "Global"
    target_countries: List[str] = Field(default_factory=list)
    focal_date: Optional[str] = None
    temporal_mode: TemporalMode = TemporalMode.PROSPECTIVE_SCENARIO


class SummitEvent(StrategicEvent):
    """Metadata and participating framework for a summit (fully backward compatible)."""
    summit_name: str = ""
    host_country: str = "Multilateral"
    location: str = "TBD"
    member_countries: List[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def sync_summit_fields(cls, values: Any) -> Any:
        if isinstance(values, dict):
            if "summit_name" in values and "title" not in values:
                values["title"] = values["summit_name"]
            elif "title" in values and ("summit_name" not in values or not values["summit_name"]):
                values["summit_name"] = values["title"]
            if "member_countries" in values and "target_countries" not in values:
                values["target_countries"] = values["member_countries"]
            elif "target_countries" in values and ("member_countries" not in values or not values["member_countries"]):
                values["member_countries"] = values["target_countries"]
        return values


class SummitAnalysisReport(BaseModel):
    """Final de-sanitized multilateral intelligence synthesis."""
    event: Union[SummitEvent, StrategicEvent]

    lens_evaluations: List[LensEvaluation] = Field(default_factory=list)
    negative_space_synopsis: List[str] = Field(default_factory=list)
    country_ledgers: List[MemberCountryAudit] = Field(default_factory=list)
    kinesic_forensics: List[KinesicObservation] = Field(default_factory=list)
    hard_money_audit: Dict[str, Any] = Field(default_factory=dict)
    civilizational_synthesis: Dict[str, str] = Field(default_factory=dict)
    strategic_resilience_matrix: Dict[str, Any] = Field(default_factory=dict)
    ach_evaluation: Optional[Dict[str, Any]] = None
    overall_confidence_score: float = Field(default=0.8)
    epistemic_arbitration_log: List[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _remap_legacy_tier_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            mapping = {
                "tier1_negative_space_synopsis": "negative_space_synopsis",
                "tier2_country_ledgers": "country_ledgers",
                "tier3_kinesic_forensics": "kinesic_forensics",
                "tier4_hard_money_audit": "hard_money_audit",
                "tier5_civilizational_inner_meaning": "civilizational_synthesis",
            }
            for old_key, new_key in mapping.items():
                if old_key in data and new_key not in data:
                    data[new_key] = data[old_key]
        return data

    @property
    def tier1_negative_space_synopsis(self) -> List[str]:
        return self.negative_space_synopsis

    @property
    def tier2_country_ledgers(self) -> List[MemberCountryAudit]:
        return self.country_ledgers

    @property
    def tier3_kinesic_forensics(self) -> List[KinesicObservation]:
        return self.kinesic_forensics

    @property
    def tier4_hard_money_audit(self) -> Dict[str, Any]:
        return self.hard_money_audit

    @property
    def tier5_civilizational_inner_meaning(self) -> Dict[str, str]:
        return self.civilizational_synthesis
