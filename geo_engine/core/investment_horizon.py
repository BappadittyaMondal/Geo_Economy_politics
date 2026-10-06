"""
Horizon-Adaptive Investment & Valuation Engine.
Adapts evidence requirements, weights, strictness, and discount rates according to
investment horizons (SIP, Turnaround/Multibagger, 3/10/30-Day Positional, Geopolitical Shock).
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


class InvestmentHorizon(str, Enum):
    """Investment horizons with fundamentally distinct evidentiary strictness."""
    SIP_LONG_TERM = "SIP_LONG_TERM"
    TURNAROUND_MULTIBAGGER = "TURNAROUND_MULTIBAGGER"
    POSITIONAL_SWING_3_10_30 = "POSITIONAL_SWING_3_10_30"
    GEOPOLITICAL_EVENT_SHOCK = "GEOPOLITICAL_EVENT_SHOCK"


@dataclass
class HorizonEvidenceProfile:
    """Evidence requirements, weights, and thresholds calibrated to an investment horizon."""
    horizon: InvestmentHorizon
    horizon_label: str
    min_historical_years: int
    fundamental_weight: float
    technical_momentum_weight: float
    macro_geopolitical_weight: float
    rate_of_change_delta_weight: float
    min_roce_threshold: float
    max_debt_to_equity: float
    allow_depressed_history: bool
    delivery_volume_multiplier_threshold: float
    requires_20_50_ema_alignment: bool
    capex_haircut_percentage: float
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "horizon": self.horizon.value,
            "horizon_label": self.horizon_label,
            "min_historical_years": self.min_historical_years,
            "fundamental_weight": self.fundamental_weight,
            "technical_momentum_weight": self.technical_momentum_weight,
            "macro_geopolitical_weight": self.macro_geopolitical_weight,
            "rate_of_change_delta_weight": self.rate_of_change_delta_weight,
            "min_roce_threshold": self.min_roce_threshold,
            "max_debt_to_equity": self.max_debt_to_equity,
            "allow_depressed_history": self.allow_depressed_history,
            "delivery_volume_multiplier_threshold": self.delivery_volume_multiplier_threshold,
            "requires_20_50_ema_alignment": self.requires_20_50_ema_alignment,
            "capex_haircut_percentage": self.capex_haircut_percentage,
            "description": self.description,
        }


class HorizonAdaptiveEvaluator:
    """Provides calibrated evidence requirements tailored to investment query horizons."""

    PROFILES: Dict[InvestmentHorizon, HorizonEvidenceProfile] = {
        InvestmentHorizon.SIP_LONG_TERM: HorizonEvidenceProfile(
            horizon=InvestmentHorizon.SIP_LONG_TERM,
            horizon_label="SIP / Long-Term Compounder (5-15 Years)",
            min_historical_years=10,
            fundamental_weight=0.70,
            technical_momentum_weight=0.05,
            macro_geopolitical_weight=0.15,
            rate_of_change_delta_weight=0.10,
            min_roce_threshold=15.0,
            max_debt_to_equity=0.50,
            allow_depressed_history=False,
            delivery_volume_multiplier_threshold=1.0,
            requires_20_50_ema_alignment=False,
            capex_haircut_percentage=85.0,
            description="Demands 10-year track record, ROCE > 15%, D/E < 0.5, clean governance. Bypasses 10-day chart noise.",
        ),
        InvestmentHorizon.TURNAROUND_MULTIBAGGER: HorizonEvidenceProfile(
            horizon=InvestmentHorizon.TURNAROUND_MULTIBAGGER,
            horizon_label="Turnaround / Early Multibagger (1-3 Years)",
            min_historical_years=2,
            fundamental_weight=0.25,
            technical_momentum_weight=0.15,
            macro_geopolitical_weight=0.15,
            rate_of_change_delta_weight=0.45,
            min_roce_threshold=5.0,
            max_debt_to_equity=2.5,
            allow_depressed_history=True,
            delivery_volume_multiplier_threshold=1.5,
            requires_20_50_ema_alignment=False,
            capex_haircut_percentage=50.0,
            description="Focuses on rate-of-change: debt reduction velocity, capacity utilization inflection, promoter de-pledge. Historical depressed ratios permitted.",
        ),
        InvestmentHorizon.POSITIONAL_SWING_3_10_30: HorizonEvidenceProfile(
            horizon=InvestmentHorizon.POSITIONAL_SWING_3_10_30,
            horizon_label="Positional / Swing (3 to 30 Days)",
            min_historical_years=1,
            fundamental_weight=0.05,
            technical_momentum_weight=0.65,
            macro_geopolitical_weight=0.15,
            rate_of_change_delta_weight=0.15,
            min_roce_threshold=0.0,
            max_debt_to_equity=999.0,
            allow_depressed_history=True,
            delivery_volume_multiplier_threshold=2.0,
            requires_20_50_ema_alignment=True,
            capex_haircut_percentage=0.0,
            description="Prioritizes stage-2 base breakout, delivery volume > 200% of 20-day avg, 20/50 EMA alignment, and relative strength vs Nifty.",
        ),
        InvestmentHorizon.GEOPOLITICAL_EVENT_SHOCK: HorizonEvidenceProfile(
            horizon=InvestmentHorizon.GEOPOLITICAL_EVENT_SHOCK,
            horizon_label="Geopolitical Event Shock (Immediate)",
            min_historical_years=3,
            fundamental_weight=0.30,
            technical_momentum_weight=0.10,
            macro_geopolitical_weight=0.50,
            rate_of_change_delta_weight=0.10,
            min_roce_threshold=10.0,
            max_debt_to_equity=1.0,
            allow_depressed_history=False,
            delivery_volume_multiplier_threshold=1.2,
            requires_20_50_ema_alignment=False,
            capex_haircut_percentage=85.0,
            description="Evaluates input cost elasticity (crude, gas, shipping rates), sovereign trade sanctions, currency depreciation stress test.",
        ),
    }

    @classmethod
    def get_evidence_profile(cls, horizon: InvestmentHorizon) -> HorizonEvidenceProfile:
        """Retrieve the evidence strictness profile for a given horizon."""
        return cls.PROFILES.get(horizon, cls.PROFILES[InvestmentHorizon.SIP_LONG_TERM])

    @classmethod
    def resolve_horizon_from_text(cls, query_text: str) -> InvestmentHorizon:
        """Detects the investment horizon from query keywords."""
        lower_q = query_text.lower()
        if any(w in lower_q for w in ["swing", "positional", "3 day", "10 day", "30 day", "breakout", "ema", "volume spike", "chart"]):
            return InvestmentHorizon.POSITIONAL_SWING_3_10_30
        if any(w in lower_q for w in ["turnaround", "multibagger", "micro cap", "deep value", "debt reduction", "inflection"]):
            return InvestmentHorizon.TURNAROUND_MULTIBAGGER
        if any(w in lower_q for w in ["shock", "war", "chokepoint", "sanction", "redline", "blockade", "crude spike"]):
            return InvestmentHorizon.GEOPOLITICAL_EVENT_SHOCK
        return InvestmentHorizon.SIP_LONG_TERM


class DynamicDiscountRateCalculator:
    """
    Dynamically couples geopolitical and macroeconomic risk scores to equity
    discount rates (Cost of Equity Ke / WACC), with domestic SIP liquidity buffering.
    """

    SECTOR_SENSITIVITIES: Dict[str, float] = {
        # High vulnerability to crude oil, freight rates, and import currency shocks
        "PAINTS": 1.45,
        "TYRES": 1.35,
        "AVIATION": 1.50,
        "SPECIALTY_CHEMICALS": 1.25,
        "OIL_MARKETING_OMC": 1.40,
        
        # Moderate vulnerability
        "AUTOMOBILE": 1.10,
        "CONSUMER_DURABLES": 1.05,
        "CAPITAL_GOODS": 1.00,
        "BANKING_NBFC": 0.95,
        "IT_SERVICES": 0.85,
        "PHARMACEUTICALS": 0.75,
        
        # Beneficiaries / Resilient to geopolitical tension
        "DEFENSE": 0.40,
        "DOMESTIC_UPSTREAM_OIL": 0.50,
        "MINING_METALS": 0.70,
        "PUBLIC_INFRASTRUCTURE": 0.80,
    }

    @classmethod
    def get_sector_sensitivity(cls, sector_name: str) -> float:
        """Retrieves beta sensitivity of a sector to geopolitical/energy shocks."""
        normalized = sector_name.upper().replace(" ", "_").replace("-", "_")
        for key, val in cls.SECTOR_SENSITIVITIES.items():
            if key in normalized or normalized in key:
                return val
        return 1.00

    @classmethod
    def calculate_adjusted_discount_rate(
        cls,
        base_ke: float,
        geopolitical_risk_score: float,
        sector_name: str,
        dii_sip_buffer_ratio: float = 0.70,
    ) -> Dict[str, Any]:
        """
        Computes the adjusted discount rate Ke for DCF models:
        Delta_Ke = alpha * GeoRisk * Sensitivity * (1.0 - dii_sip_buffer_ratio * DomesticResilience)
        
        Parameters:
        - base_ke: Baseline Cost of Equity (e.g. 12.0%).
        - geopolitical_risk_score: Normalized geopolitical risk [0.0 to 1.0].
        - sector_name: Target industry sector.
        - dii_sip_buffer_ratio: Domestic mutual fund SIP absorption factor (default 0.70).
        """
        sensitivity = cls.get_sector_sensitivity(sector_name)
        
        # Alpha scale factor: 1.0 risk score produces maximum +2.5% discount rate expansion
        alpha = 2.50
        
        # Net impact dampened by continuous domestic liquidity absorption
        net_risk_premium = round(alpha * geopolitical_risk_score * sensitivity * (1.0 - (dii_sip_buffer_ratio * 0.40)), 3)
        adjusted_ke = round(base_ke + net_risk_premium, 3)

        return {
            "base_ke_percent": base_ke,
            "geopolitical_risk_score": geopolitical_risk_score,
            "sector_name": sector_name,
            "sector_sensitivity": sensitivity,
            "dii_sip_buffer_ratio": dii_sip_buffer_ratio,
            "geopolitical_risk_premium_percent": net_risk_premium,
            "adjusted_ke_percent": adjusted_ke,
            "valuation_multiple_compression_factor": round(base_ke / adjusted_ke, 3),
        }
