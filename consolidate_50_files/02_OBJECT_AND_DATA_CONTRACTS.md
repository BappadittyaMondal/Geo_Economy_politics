<!-- RAG_CONTEXT_HEADER
BUNDLE: Geo_Engine_Core_5
MODULE: 02_OBJECT_AND_DATA_CONTRACTS.md
CANONICAL_COMMIT: c384ca7
CANONICAL_REPO: https://github.com/BappadittyaMondal/Geo_Economy_politics.git
-->

# 02 OBJECT AND DATA CONTRACTS
**Document Reference:** `OBJECT-CONTRACTS-V2.0`  
**System Identity:** Geo-Economic & Geopolitical Intelligence Engine (`Geo_Economy_politics`)  
**Canonical Repository:** `https://github.com/BappadittyaMondal/Geo_Economy_politics.git`  

---

## 1. CANONICAL ENUMS

```python
class EpistemicTier(int, Enum):
    TIER_0_INSUFFICIENT_EVIDENCE = 0  # Degraded telemetry / null state
    TIER_1_PHYSICAL = 1               # Troops, oil barrels, grain, chokepoints
    TIER_2_FINANCIAL = 2              # Central bank flows, operational Vostro
    TIER_3_SOVEREIGN_REDLINES = 3     # Treaties, boundary agreements, alliances
    TIER_4_KINESICS = 4               # Protocol-subtracted spatial vectors
    TIER_5_COMMUNIQUE_PR = 5          # Communiques, ceremonial photocalls, spin

class TemporalMode(str, Enum):
    EMPIRICAL_HISTORICAL = "empirical_historical"
    LIVE_VERIFIED = "live_verified"
    PROSPECTIVE_SCENARIO = "prospective_scenario"

class EventType(str, Enum):
    SUMMIT = "SUMMIT"
    BORDER_SECURITY = "BORDER_SECURITY"
    BORDER_MILITARY = "BORDER_MILITARY"
    GEO_ECONOMIC = "GEO_ECONOMIC"
    CIVILIZATIONAL_CRISIS = "CIVILIZATIONAL_CRISIS"
    HYBRID_WARFARE = "HYBRID_WARFARE"
    STRATEGIC_EVENT = "STRATEGIC_EVENT"
```

---

## 2. INTER-MODULE DATA STRUCTURES

### A. FinancialFlow
Represents an announced or executed bilateral or multilateral capital or trade commitment.
- `source_country`: str
- `target_country`: str
- `project_name`: str
- `nominal_mou_usd`: float (Announced headline figure in USD)
- `is_binding_contract`: bool (True if escrow/budget line exists)
- `clearing_currency`: str (e.g. "USD", "INR", "CNY", "RUB")
- `vostro_nostro_operational`: bool
- `secondary_sanctions_risk_score`: float [0.0, 1.0]
- **Computed Property `effective_capex_usd`:**
  - If `is_binding_contract == False`: $\text{base} = \text{nominal\_mou\_usd} \times 0.15$.
  - If `is_binding_contract == True`: $\text{base} = \text{nominal\_mou\_usd}$.
  - Discount applied: $\text{base} \times (1.0 - 0.5 \times \text{secondary\_sanctions\_risk\_score})$.

### B. KinesicObservation
Represents a structured kinesic/proxemic observation during a bilateral interaction.
- `actor_primary`: str
- `actor_secondary`: str
- `setting`: str ("formal_photocall", "bilateral_table", "unscripted_corridor")
- `protocol_mandated`: bool
- `handshake_torque_vector`: str ("proactive_forward", "neutral_vertical", "defensive_withdrawn")
- `torso_angle_degrees`: float [0.0, 90.0]
- `residual_tension_score`: float [0.0, 1.0]
- `micro_expression_flag`: str ("duchenne_smile", "jaw_clench", "gaze_avoidance", "neutral_resting")
- **Computed Property `genuine_warmth_index`:**
  - If `protocol_mandated == True`: $\text{raw\_warmth} = (1.0 - \text{residual\_tension\_score}) \times 0.30$.
  - If `torso_angle_degrees > 45.0`: $\text{raw\_warmth} \times 0.60$.
  - If `jaw_clench` or `gaze_avoidance`: $\text{raw\_warmth} \times 0.30$.

### C. CommuniqueClause
Represents an individual clause parsed from a summit declaration.
- `clause_id`: str (e.g. "UNSC-01", "PAY-01")
- `category`: str ("energy", "finance", "security", "institutional_reform", "territorial")
- `raw_text`: str
- `present_in_current_summit`: bool
- `historical_baseline_present`: bool
- `dilution_status`: str ("retained_full", "diluted_passive", "omitted_negative_space")
- `omission_significance`: Optional[str]

### D. LensEvaluation
Result of an individual specialized lens evaluation.
- `lens_name`: str
- `alignment_score`: float [-1.0, 1.0]
- `confidence`: float [0.0, 1.0]
- `primary_epistemic_tier`: EpistemicTier
- `key_findings`: List[str]
- `hard_metrics`: Dict[str, Any]
- `evidence_status`: str ("sufficient", "degraded", "insufficient")

### E. MemberCountryAudit
Full four-dimensional audit for a participating sovereign nation.
- `country_name`: str
- `public_domestic_narrative`: str
- `geopolitical_yield`: str
- `hard_cash_yield_usd`: float
- `concessions_or_vulnerabilities`: str
- `strategic_autonomy_score`: float [0.0, 1.0]
- `key_bilateral_postures`: Dict[str, str]

### F. StrategicEvent & SummitEvent
Base polymorphic container for any crisis or summit.
- `title`: str
- `year`: int
- `event_type`: EventType
- `primary_region`: str
- `target_countries`: List[str]
- `focal_date`: Optional[str]
- `temporal_mode`: TemporalMode
- (SummitEvent adds backward-compatible `summit_name`, `host_country`, `member_countries`).

### G. SummitAnalysisReport
The master synthesized intelligence report.
- `event`: Union[SummitEvent, StrategicEvent]
- `negative_space_synopsis`: List[str]
- `country_ledgers`: List[MemberCountryAudit]
- `kinesic_forensics`: List[KinesicObservation]
- `hard_money_audit`: Dict[str, Any]
- `civilizational_synthesis`: Dict[str, str]
- `strategic_resilience_matrix`: Dict[str, Any] (Food buffer, WWR ammunition, IADS coverage, HREE monopoly, OFAC risk)
- `overall_confidence_score`: float [0.0, 1.0] (Calculated via Epistemic Tier-Weighted Mean)
- `epistemic_arbitration_log`: List[str]

### H. ForecastRecord
Deterministic prospective calibrated forecast.
- `forecast_id`: str (`FCST-{year}-{sha256[:8]}`)
- `target_hypothesis`: str
- `predicted_probability`: float [0.0, 1.0]
- `time_horizon_months`: int
- `epistemic_basis`: str
- `status`: str ("ACTIVE", "RESOLVED")
- `actual_outcome`: Optional[int] (0 or 1)
- `brier_score`: Optional[float] ($(p - o)^2$)
