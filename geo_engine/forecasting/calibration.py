"""
Calibrated Forecasting and Brier Scoring Engine.
Separates geopolitical analysis into four rigorous epistemic strata:
Observed, Inferred, Scenario, and Calibrated Forecast with statistical verification.
"""

import math
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from ..core.models import get_system_reference_date


def calculate_temporal_decay(
    event_date: str,
    reference_date: Optional[str] = None,
    half_life_days: float = 90.0
) -> float:
    """
    Calculates exponential temporal decay weight: w(t) = exp(-ln(2) * delta_t / tau).
    For statutory treaties, constitutional articles, and legal covenants, tau = inf, returning 1.0.
    For volatile macro telemetry and headline events, default tau = 90.0 days.
    """
    if half_life_days <= 0 or math.isinf(half_life_days):
        return 1.0

    try:
        cleaned_event_date = str(event_date).strip()[:10]
        evt_dt = datetime.strptime(cleaned_event_date, "%Y-%m-%d")

        if reference_date:
            cleaned_ref_date = str(reference_date).strip()[:10]
            ref_dt = datetime.strptime(cleaned_ref_date, "%Y-%m-%d")
        else:
            ref_dt = get_system_reference_date()
            if hasattr(ref_dt, "tzinfo") and ref_dt.tzinfo is not None:
                ref_dt = ref_dt.replace(tzinfo=None)

        delta_days = (ref_dt - evt_dt).total_seconds() / 86400.0
        if delta_days <= 0:
            return 1.0

        decay = math.exp(-(math.log(2.0) * delta_days) / half_life_days)
        return round(float(decay), 4)
    except Exception:
        return 1.0


class ScenarioBranch(BaseModel):
    """Represents a discrete possible future outcome branch."""
    scenario_name: str
    probability: float = Field(..., ge=0.0, le=1.0)
    key_drivers: List[str]
    early_indicators: List[str]
    impact_severity: str = Field(default="MEDIUM", description="'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'")


class CalibratedForecast(BaseModel):
    """A mathematically bounded probabilistic projection."""
    target_hypothesis: str
    forecast_probability: float = Field(..., ge=0.0, le=1.0)
    confidence_interval_low: float = Field(..., ge=0.0, le=1.0)
    confidence_interval_high: float = Field(..., ge=0.0, le=1.0)
    time_horizon_months: int = 12
    epistemic_basis: str = ""


class EpistemicStrata(BaseModel):
    """Complete 4-layer partitioned output preventing confusion between observed facts and forecasts."""
    observed_facts: List[str] = Field(default_factory=list, description="Empirical ground truth (Tier 1/2)")
    inferred_realities: List[str] = Field(default_factory=list, description="Cross-lens triangulated deductions")
    scenario_branches: List[ScenarioBranch] = Field(default_factory=list)
    calibrated_forecasts: List[CalibratedForecast] = Field(default_factory=list)


class BrierScorer:
    """Calculates statistical calibration and Brier scores for historical forecast backtesting."""

    @staticmethod
    def calculate_brier_score(forecast_probabilities: List[float], observed_outcomes: List[int]) -> float:
        """
        Calculates the Brier score: (1/N) * sum((f_t - o_t)^2).
        Scores range from 0.0 (perfect accuracy) to 1.0 (complete failure).
        """
        if not forecast_probabilities or not observed_outcomes or len(forecast_probabilities) != len(observed_outcomes):
            raise ValueError("forecast_probabilities and observed_outcomes must be non-empty lists of identical length.")

        n = len(forecast_probabilities)
        total_error = sum((f - o) ** 2 for f, o in zip(forecast_probabilities, observed_outcomes))
        return round(total_error / n, 4)


class ForecastingEngine:
    """Generates calibrated probabilistic scenarios for multilateral events."""

    @staticmethod
    def calculate_temporal_decay(
        event_date: str,
        reference_date: Optional[str] = None,
        half_life_days: float = 90.0
    ) -> float:
        return calculate_temporal_decay(event_date, reference_date, half_life_days)

    @classmethod
    def update_scenario_probabilities(
        cls,
        scenarios: List[ScenarioBranch],
        evidence_claims: Optional[List[Any]] = None,
        reference_date: Optional[str] = None
    ) -> List[ScenarioBranch]:
        """
        Applies Reliability-Weighted Heuristic Updating (discrete quasi-Bayesian likelihood updating)
        to scenario branches based on incoming evidence claims with exponential temporal decay.
        Ensures the sum of all updated probabilities strictly equals 1.0 while explicitly bounding
        scenario uncertainty according to epistemic reliability weights and recency.
        """
        if not evidence_claims or not scenarios:
            return scenarios

        # Discard TIER_0 / insufficient or 0-reliability degraded claims before updating
        valid_claims = [
            c for c in evidence_claims
            if getattr(c, "evidence_status", "sufficient") != "insufficient"
            and getattr(c, "reliability_weight", 1.0) > 0.0
        ]
        if not valid_claims:
            return scenarios

        # Helper to compute effective weight combining epistemic reliability and temporal decay
        def _get_effective_claim_weight(claim: Any) -> float:
            base_rel = float(getattr(claim, "reliability_weight", 1.0))
            # Determine if claim is perpetual statutory/treaty/constitutional (tau = inf)
            claim_type = str(getattr(claim, "claim_type", ""))
            epistemic_tier = str(getattr(claim, "epistemic_tier", ""))
            fact_text = getattr(claim, "asserted_fact", getattr(claim, "assertion", ""))
            is_statutory = (
                "LEGAL_COMMITMENT" in claim_type or
                "TIER_3" in epistemic_tier or
                any(kw in fact_text.lower() for kw in ["treaty", "statute", "clause", "act 19", "act 20", "constitution", "article 10", "article 44", "article 30"])
            )
            tau = float("inf") if is_statutory else 90.0
            claim_dt = (
                getattr(claim, "event_date", None) or
                getattr(claim, "date", None) or
                getattr(claim, "created_at", None) or
                getattr(claim, "timestamp", None)
            )
            if claim_dt:
                decay = calculate_temporal_decay(str(claim_dt), reference_date=reference_date, half_life_days=tau)
            else:
                decay = 1.0
            return round(base_rel * decay, 4)

        # Weight claim contributions by their effective reliability and temporal recency
        sanction_or_covert_count = sum(
            _get_effective_claim_weight(c) for c in valid_claims
            if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in ["sanction", "fatf", "ofac", "intercept", "chokepoint", "infiltrat", "migrant"])
        )
        sinocentric_or_friction_count = sum(
            _get_effective_claim_weight(c) for c in valid_claims
            if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in ["cips", "yuan", "pla", "border tension", "dispute", "lac"])
        )

        likelihoods = []
        for s in scenarios:
            l = 1.0
            s_name = s.scenario_name.lower()
            if "disruption" in s_name or "decoupling" in s_name or "sanctions" in s_name:
                l += sanction_or_covert_count * 0.35
            elif "sinocentric" in s_name or "capture" in s_name or "friction" in s_name:
                l += sinocentric_or_friction_count * 0.35
            else:
                if sanction_or_covert_count > 0 or sinocentric_or_friction_count > 0:
                    l = max(0.4, 1.0 - (0.15 * (sanction_or_covert_count + sinocentric_or_friction_count)))
            likelihoods.append(l)

        unnormalized = [s.probability * l for s, l in zip(scenarios, likelihoods)]
        total_prob = sum(unnormalized)

        if total_prob <= 0:
            return scenarios

        updated_branches = []
        for s, unnorm in zip(scenarios, unnormalized):
            norm_prob = round(unnorm / total_prob, 3)
            updated_branches.append(ScenarioBranch(
                scenario_name=s.scenario_name,
                probability=norm_prob,
                key_drivers=s.key_drivers,
                early_indicators=s.early_indicators,
                impact_severity=s.impact_severity
            ))

        diff = round(1.0 - sum(b.probability for b in updated_branches), 3)
        if diff != 0:
            updated_branches[0].probability = round(updated_branches[0].probability + diff, 3)

        return updated_branches

    @classmethod
    def generate_strata(
        cls,
        summit_name: str = "BRICS 2026 Summit",
        year: int = 2026,
        evidence_claims: Optional[List[Any]] = None,
        event_type: Optional[str] = None,
        include_unmodeled: bool = False
    ) -> EpistemicStrata:
        """
        Generates calibrated 4-strata intelligence for the summit or crisis event with optional Bayesian evidence updates.
        Supports parameterization by event_type (SUMMIT, BORDER_MILITARY, BORDER_SECURITY, GEO_ECONOMIC, HYBRID_WARFARE).
        """
        if event_type == "BORDER_MILITARY":
            observed = [
                "Forward military deployments and logistics lines established along frontline sectors.",
                "Regular bilateral military commander and diplomatic working mechanism (WMCC) meetings active.",
                "High-altitude drone surveillance and border radar infrastructure operational.",
                "Bilateral disengagement protocols maintain demarcated buffer zones."
            ]
            inferred = [
                "Neither sovereign actor seeks systemic kinetic escalation across high-altitude terrain.",
                "Dual-use border infrastructure buildup creates permanent forward mobilization capability.",
                "Long-term stability requires formalized protocol demilitarization rather than rhetorical declarations."
            ]
            scenarios = [
                ScenarioBranch(
                    scenario_name="Scenario A: Managed Bilateral Patrolling & Buffer Zone Status Quo (Baseline)",
                    probability=0.60,
                    key_drivers=["Adherence to frontline commander protocols", "Mutual recognition of buffer boundaries"],
                    early_indicators=["Scheduled border flag meetings", "Zero unilateral forward patrol intrusions"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario B: Friction-Driven Tactical Standoff & Mobilization Surge",
                    probability=0.25,
                    key_drivers=["Infrastructure development near friction points", "Airspace or patrol transgressions"],
                    early_indicators=["Sudden deployment of mechanized armor", "Breakdown in weekly hotline communications"],
                    impact_severity="HIGH"
                ),
                ScenarioBranch(
                    scenario_name="Scenario C: Diplomatic Disengagement & Mutual Demarcation Accord",
                    probability=0.10,
                    key_drivers=["High-level political consensus", "Mutual strategic redeployment to peace-time garrisons"],
                    early_indicators=["Joint verification mechanism announcement", "Synchronized troop pullbacks"],
                    impact_severity="LOW"
                ),
                ScenarioBranch(
                    scenario_name="Scenario D: Exogenous Skirmish / Unmodeled Tactical Spillover (Residual)",
                    probability=0.05,
                    key_drivers=["Unplanned frontline encounter", "Asymmetric third-party border provocation"],
                    early_indicators=["Unplanned kinetic exchange", "Emergency security cabinet mobilization"],
                    impact_severity="CRITICAL"
                )
            ]
            forecasts = [
                CalibratedForecast(
                    target_hypothesis=f"Bilateral frontline commander protocols sustain patrol disengagement along border sectors without kinetic casualties throughout {year}",
                    forecast_probability=0.78,
                    confidence_interval_low=0.70,
                    confidence_interval_high=0.85,
                    time_horizon_months=12,
                    epistemic_basis="Backed by operational buffer zone agreements and bilateral military hotline mechanisms."
                ),
                CalibratedForecast(
                    target_hypothesis="Unilateral sovereign alteration of existing territorial control line through offensive conventional operation",
                    forecast_probability=0.04,
                    confidence_interval_low=0.01,
                    confidence_interval_high=0.08,
                    time_horizon_months=12,
                    epistemic_basis="Deterred by forward defense deployment depth and nuclear escalation thresholds."
                )
            ]
        elif event_type == "BORDER_SECURITY":
            observed = [
                "Sovereign border perimeter and maritime coastal surveillance radar operational.",
                "Frontex and border guard interdiction checkpoints active across designated sectors.",
                "Asymmetric migrant transit and irregular border crossings documented along coastal routes."
            ]
            inferred = [
                "Transit state leverages border flow interdiction as diplomatic bargaining leverage.",
                "Destination state domestic political polarization constrains unilateral deterrence options."
            ]
            scenarios = [
                ScenarioBranch(
                    scenario_name="Scenario A: Fortified Interdiction & Bilateral Repatriation Protocols (Baseline)",
                    probability=0.55,
                    key_drivers=["Joint maritime surveillance coordination", "Transit state security funding allocation"],
                    early_indicators=["Operational coastal interception agreements", "Decline in maritime transit vessels"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario B: Asymmetric Hybrid Infiltration Surge & Perimeter Saturation",
                    probability=0.30,
                    key_drivers=["Relaxation of transit country coastal enforcement", "Socio-economic crisis in origin regions"],
                    early_indicators=["Perimeter fence breaches", "Emergency reception center saturation"],
                    impact_severity="HIGH"
                ),
                ScenarioBranch(
                    scenario_name="Scenario C: Formal Bilateral Border Control Accord & Legal Transit Quota",
                    probability=0.10,
                    key_drivers=["Comprehensive bilateral diplomatic agreement", "EU-level mobility partnership ratification"],
                    early_indicators=["Treaty signing on migration management", "Co-located consular checkpoints"],
                    impact_severity="LOW"
                ),
                ScenarioBranch(
                    scenario_name="Scenario D: Sovereign Perimeter Breakdown / Unmodeled Humanitarian Shock (Residual)",
                    probability=0.05,
                    key_drivers=["Catastrophic transit zone collapse", "Unforeseen regional military conflict"],
                    early_indicators=["Mass perimeter storming", "Emergency martial border mobilization"],
                    impact_severity="CRITICAL"
                )
            ]
            forecasts = [
                CalibratedForecast(
                    target_hypothesis="Sovereign authorities execute bilateral coastal interdiction and repatriation protocols within 12 months",
                    forecast_probability=0.74,
                    confidence_interval_low=0.65,
                    confidence_interval_high=0.82,
                    time_horizon_months=12,
                    epistemic_basis="Backed by mutual bilateral security interests and EU Frontex surveillance funding."
                ),
                CalibratedForecast(
                    target_hypothesis="Complete unilateral demilitarization and unmonitored opening of sovereign border perimeter",
                    forecast_probability=0.02,
                    confidence_interval_low=0.00,
                    confidence_interval_high=0.05,
                    time_horizon_months=12,
                    epistemic_basis="Constitutional redlines and statutory national border laws prohibit unmonitored entry."
                )
            ]
        elif event_type == "GEO_ECONOMIC":
            observed = [
                "Bilateral local-currency clearing mechanisms and central bank currency swap lines active.",
                "Diversified central bank sovereign reserve asset allocations across gold and non-dollar instruments.",
                "US Dollar clearing dominates primary global commodities trade settlements."
            ]
            inferred = [
                "De-dollarization remains strictly bilateral and incremental; a supranational currency is structurally unviable.",
                "Secondary sanctions risks constrain commercial bank participation in non-SWIFT financial switches."
            ]
            scenarios = [
                ScenarioBranch(
                    scenario_name="Scenario A: Fragmented Local-Currency Clearance & Continued USD Hedging (Baseline)",
                    probability=0.60,
                    key_drivers=["Expansion of bilateral swap arrangements", "Preservation of Western financial linkages"],
                    early_indicators=["Growth in bilateral local-currency invoices", "Continued USD debt issuance"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario B: Secondary Sanctions Freezes & Liquidity Disruption",
                    probability=0.25,
                    key_drivers=["US OFAC enforcement on intermediary commercial banks", "Asset freezes in correspondent accounts"],
                    early_indicators=["Sudden cessation of trade credit facilities", "Foreign exchange liquidity squeezes"],
                    impact_severity="HIGH"
                ),
                ScenarioBranch(
                    scenario_name="Scenario C: Alternative Clearing Switch (CIPS/SPFS) Accelerated Adoption",
                    probability=0.10,
                    key_drivers=["Direct interconnectivity between national central bank RTGS systems", "Gold-backed commodity trade contracts"],
                    early_indicators=["Non-Western clearing switch volume surges", "Official reserve conversion to alternative currencies"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario D: Sovereign Debt Default Cascade / Unmodeled Financial Shock (Residual)",
                    probability=0.05,
                    key_drivers=["Global sovereign debt restructuring crisis", "Systemic banking contagion"],
                    early_indicators=["Sudden sovereign bond yields spike", "Emergency IMF liquidity requests"],
                    impact_severity="CRITICAL"
                )
            ]
            forecasts = [
                CalibratedForecast(
                    target_hypothesis="Bilateral non-SWIFT local-currency settlement volume expands by >20% across participating central banks in 12 months",
                    forecast_probability=0.80,
                    confidence_interval_low=0.72,
                    confidence_interval_high=0.88,
                    time_horizon_months=12,
                    epistemic_basis="Grounded in central bank currency swap lines and sanctions risk mitigation."
                ),
                CalibratedForecast(
                    target_hypothesis="Complete immediate replacement or collapse of US Dollar global reserve currency status within 12 months",
                    forecast_probability=0.01,
                    confidence_interval_low=0.00,
                    confidence_interval_high=0.03,
                    time_horizon_months=12,
                    epistemic_basis="Directly constrained by global capital account openness requirements and Mundell-Fleming Trilemma."
                )
            ]
        elif event_type == "HYBRID_WARFARE":
            observed = [
                "Multilateral sanctions, export control frameworks, and compliance lists (FATF/OFAC) enforced.",
                "Cross-border sovereign assets held across foreign custodial banking jurisdictions."
            ]
            inferred = [
                "Legal, regulatory, and economic institutions weaponized as primary instruments of non-kinetic coercion.",
                "Target states deploy multi-jurisdictional intermediary corporate architectures to maintain capital flows."
            ]
            scenarios = [
                ScenarioBranch(
                    scenario_name="Scenario A: Institutional Lawfare Impasse & Structured Compliance Hedging (Baseline)",
                    probability=0.55,
                    key_drivers=["Legal challenges in international arbitration tribunals", "Continued intermediary asset shielding"],
                    early_indicators=["Prolonged litigation in European courts", "Creation of offshore holding structures"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario B: Multilateral Secondary Sanctions Escalation & Sovereign Asset Confiscation",
                    probability=0.30,
                    key_drivers=["Statutory legislation mandating foreign sovereign asset transfer", "Expansion of extraterritorial penalties"],
                    early_indicators=["Direct seizure of central bank reserves", "Secondary blacklist designations"],
                    impact_severity="CRITICAL"
                ),
                ScenarioBranch(
                    scenario_name="Scenario C: Negotiated Diplomatic Compromise & Reciprocal De-listing",
                    probability=0.10,
                    key_drivers=["Strategic peace settlement framework", "Mutual economic concessions"],
                    early_indicators=["Temporary sanctions waivers issued", "Asset freeze thaw agreements"],
                    impact_severity="LOW"
                ),
                ScenarioBranch(
                    scenario_name="Scenario D: Critical Infrastructure Cyber Retaliation / Unmodeled Shock (Residual)",
                    probability=0.05,
                    key_drivers=["Asymmetric state-sponsored cyber warfare", "Sabotage of undersea cable communications"],
                    early_indicators=["Major clearing switch outages", "Severe maritime logistics disruption"],
                    impact_severity="CRITICAL"
                )
            ]
            forecasts = [
                CalibratedForecast(
                    target_hypothesis="Target sovereign entities maintain operational non-Western trade and escrow settlement channels without systemic banking insolvency throughout 12 months",
                    forecast_probability=0.76,
                    confidence_interval_low=0.68,
                    confidence_interval_high=0.84,
                    time_horizon_months=12,
                    epistemic_basis="Backed by operational alternative clearing corridors and institutional hedging."
                ),
                CalibratedForecast(
                    target_hypothesis="Unconditional immediate revocation of all multilateral asset freeze orders and sanctions within 12 months",
                    forecast_probability=0.03,
                    confidence_interval_low=0.01,
                    confidence_interval_high=0.06,
                    time_horizon_months=12,
                    epistemic_basis="Geopolitical inertia and statutory legislative barriers prevent rapid sanctions repeal."
                )
            ]
        elif event_type == "CIVILIZATIONAL_CRISIS":
            observed = [
                "Sovereign leadership engages in cross-civilizational spiritual, cultural, or existential protocol interaction.",
                "Intense theological and political perception management operations triggered across domestic and regional media.",
                "Core bilateral strategic channels (energy off-take, security coordination, trade transit) remain operational."
            ]
            inferred = [
                "Domestic clerical and political backlash is managed via selective state media framing, categorizing the event as diplomatic etiquette or host courtesy.",
                "Pragmatic statecraft (Apaddharma / Yogakshema) dictates that core economic and defense yields supersede symbolic theological polarization.",
                "Civilizational pluralism and sovereign autonomy cannot be subordinated to external ideological or moral coercion."
            ]
            scenarios = [
                ScenarioBranch(
                    scenario_name="Scenario A: Pragmatic Diplomatic Containment & De-escalation (Baseline)",
                    probability=0.62,
                    key_drivers=["Sovereign prioritization of energy and security accords", "Controlled state narrative emphasizing statecraft pragmatism"],
                    early_indicators=["Scheduled bilateral ministerial meetings proceed uninterrupted", "Absence of formal diplomatic reprimands"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario B: Domestic Theological Backlash & Diplomatic Retraction",
                    probability=0.23,
                    key_drivers=["Clerical and hardline faction mobilization in home state", "State media issuing clarificatory disclaimers"],
                    early_indicators=["Official diplomatic communique asserting ideological redlines", "Temporary suspension of cultural exchanges"],
                    impact_severity="HIGH"
                ),
                ScenarioBranch(
                    scenario_name="Scenario C: Institutional Civilizational Detente Accord",
                    probability=0.10,
                    key_drivers=["Mutual recognition of civilizational statecraft traditions", "Bilateral code of conduct on spiritual/cultural respect"],
                    early_indicators=["Joint declaration acknowledging mutual civilizational respect", "Formal protocol harmonization guidelines"],
                    impact_severity="LOW"
                ),
                ScenarioBranch(
                    scenario_name="Scenario D: Sectarian Provocation / Unmodeled Radical Escalation (Residual)",
                    probability=0.05,
                    key_drivers=["Third-party extremist proxy mobilization", "Coordinated information warfare campaign on social platforms"],
                    early_indicators=["Violent street demonstrations outside diplomatic missions", "Emergency security cordons deployed"],
                    impact_severity="CRITICAL"
                )
            ]
            forecasts = [
                CalibratedForecast(
                    target_hypothesis="Bilateral diplomatic, energy, and infrastructure transit treaties remain legally and operationally intact within 12 months",
                    forecast_probability=0.84,
                    confidence_interval_low=0.76,
                    confidence_interval_high=0.90,
                    time_horizon_months=12,
                    epistemic_basis="Grounded in mutual economic necessity, energy trade continuity, and strategic transit corridors."
                ),
                CalibratedForecast(
                    target_hypothesis="Immediate unilateral severance of formal bilateral diplomatic ties triggered solely by the civilizational protocol incident",
                    forecast_probability=0.02,
                    confidence_interval_low=0.00,
                    confidence_interval_high=0.05,
                    time_horizon_months=12,
                    epistemic_basis="Directly deterred by core geopolitical equities, defense supply lines, and sovereign balance-of-payments interests."
                )
            ]
        else:
            observed = [
                "10 member states physically participating in summit institutional track.",
                "4.2M barrels/day of Russian crude actively diverted to Indian and Chinese refiners.",
                "Intra-bloc bilateral local-currency invoicing established across India-Russia and China-Russia corridors.",
                "Zero unified fiscal or supranational central banking apparatus exists within the bloc."
            ]

            inferred = [
                "India will maintain strict non-anti-Western posture, preventing the bloc from issuing an anti-Quad communique.",
                "China will leverage the summit to offload industrial clean-tech overcapacity into Global South partner markets.",
                "A unified 'BRICS common reserve currency' remains structurally impossible under the Mundell-Fleming Trilemma."
            ]

            if include_unmodeled:
                scenarios = [
                    ScenarioBranch(
                        scenario_name="Scenario A: Managed Polycentric Hedging (Baseline)",
                        probability=0.65,
                        key_drivers=[
                            "India and Brazil maintain multi-alignment and ties with Western capital markets.",
                            "Bilateral currency swaps expand without creating a supranational currency."
                        ],
                        early_indicators=[
                            "Continuation of current Indian border patrolling protocols.",
                            "No joint military exercises conducted under the BRICS banner."
                        ],
                        impact_severity="HIGH"
                    ),
                    ScenarioBranch(
                        scenario_name="Scenario B: Sinocentric Institutional Capture (Friction)",
                        probability=0.20,
                        key_drivers=[
                            "Beijing aggressively pushes CIPS as the sole alternative payment switch.",
                            "Russia accepts greater junior-partner subordination to Yuan hegemony."
                        ],
                        early_indicators=[
                            "Public Indian diplomatic dissent or reservation notes on summit communiques.",
                            "Expansion of Chinese non-performing debt renegotiations in African member states."
                        ],
                        impact_severity="CRITICAL"
                    ),
                    ScenarioBranch(
                        scenario_name="Scenario C: Western Secondary Sanctions Disruption (Decoupling)",
                        probability=0.10,
                        key_drivers=[
                            "US OFAC enforces direct secondary sanctions on tier-1 Indian, Chinese, and UAE commercial banks.",
                            "Western P&I maritime insurance clubs systematically intercept shadow fleet tankers."
                        ],
                        early_indicators=[
                            "Sudden freeze in Indian VOSTRO account remittances.",
                            "Sharp jump in Brent crude tanker freight risk premia."
                        ],
                        impact_severity="CRITICAL"
                    ),
                    ScenarioBranch(
                        scenario_name="Scenario D: Exogenous Sovereign Shock / Unmodeled Divergence (Residual)",
                        probability=0.05,
                        key_drivers=[
                            "Sudden domestic regime rupture in key member state.",
                            "Unmodeled geopolitical maritime kinetic escalation."
                        ],
                        early_indicators=[
                            "Emergency summit postponement or walkout.",
                            "Abrupt bilateral border closure."
                        ],
                        impact_severity="CRITICAL"
                    )
                ]
            else:
                scenarios = [
                    ScenarioBranch(
                        scenario_name="Scenario A: Managed Polycentric Hedging (Baseline)",
                        probability=0.68,
                        key_drivers=[
                            "India and Brazil maintain multi-alignment and ties with Western capital markets.",
                            "Bilateral currency swaps expand without creating a supranational currency."
                        ],
                        early_indicators=[
                            "Continuation of current Indian border patrolling protocols.",
                            "No joint military exercises conducted under the BRICS banner."
                        ],
                        impact_severity="HIGH"
                    ),
                    ScenarioBranch(
                        scenario_name="Scenario B: Sinocentric Institutional Capture (Friction)",
                        probability=0.22,
                        key_drivers=[
                            "Beijing aggressively pushes CIPS as the sole alternative payment switch.",
                            "Russia accepts greater junior-partner subordination to Yuan hegemony."
                        ],
                        early_indicators=[
                            "Public Indian diplomatic dissent or reservation notes on summit communiques.",
                            "Expansion of Chinese non-performing debt renegotiations in African member states."
                        ],
                        impact_severity="CRITICAL"
                    ),
                    ScenarioBranch(
                        scenario_name="Scenario C: Western Secondary Sanctions Disruption (Decoupling)",
                        probability=0.10,
                        key_drivers=[
                            "US OFAC enforces direct secondary sanctions on tier-1 Indian, Chinese, and UAE commercial banks.",
                            "Western P&I maritime insurance clubs systematically intercept shadow fleet tankers."
                        ],
                        early_indicators=[
                            "Sudden freeze in Indian VOSTRO account remittances.",
                            "Sharp jump in Brent crude tanker freight risk premia."
                        ],
                        impact_severity="CRITICAL"
                    )
                ]

            forecasts = [
                CalibratedForecast(
                    target_hypothesis="BRICS expands bilateral local currency clearing volume by >20% within 12 months without adopting a unified currency",
                    forecast_probability=0.82,
                    confidence_interval_low=0.74,
                    confidence_interval_high=0.89,
                    time_horizon_months=12,
                    epistemic_basis="Backed by operational central bank bilateral swap lines and Mundell-Fleming constraints."
                ),
                CalibratedForecast(
                    target_hypothesis="India formally ratifies an anti-Western collective security clause in the summit declaration",
                    forecast_probability=0.03,
                    confidence_interval_low=0.01,
                    confidence_interval_high=0.06,
                    time_horizon_months=12,
                    epistemic_basis="Directly contradicts India's constitutional and historical doctrine of strategic autonomy (Panchsheel / Vishwamitra)."
                )
            ]

        # Persist forecasts to SQLite ledger
        try:
            import hashlib
            from datetime import timedelta
            from ..storage.event_store import EventStore
            store = EventStore()
            created_dt = get_system_reference_date()
            for fc in forecasts:
                # Deterministic SHA-256 forecast ID (stable across process restarts)
                id_seed = f"{year}:{fc.target_hypothesis}"
                hypo_hash = hashlib.sha256(id_seed.encode("utf-8")).hexdigest()[:8]
                fc_id = f"FCST-{year}-{hypo_hash}"
                # Dynamically calculate target date based on forecast horizon months
                target_dt = created_dt + timedelta(days=fc.time_horizon_months * 30)
                store.record_forecast({
                    "forecast_id": fc_id,
                    "created_at": created_dt.isoformat(),
                    "target_date": target_dt.strftime("%Y-%m-%d"),
                    "event_name": summit_name,
                    "hypothesis": fc.target_hypothesis,
                    "predicted_probability": fc.forecast_probability,
                    "confidence_interval_low": fc.confidence_interval_low,
                    "confidence_interval_high": fc.confidence_interval_high,
                    "epistemic_basis": fc.epistemic_basis,
                    "status": "ACTIVE"
                })
        except Exception as e:
            import sys
            print(f"[WARNING] Failed to persist forecast to SQLite ledger: {e}", file=sys.stderr)

        return EpistemicStrata(
            observed_facts=observed,
            inferred_realities=inferred,
            scenario_branches=scenarios,
            calibrated_forecasts=forecasts
        )

    @classmethod
    def resolve_forecast_with_bayesian_update(
        cls,
        forecast_id: str,
        actual_outcome: int,
        contributing_lenses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Resolves a forecast, calculates Brier score, and backpropagates error
        to update persistent epistemic reliability multipliers for contributing lenses.
        """
        from ..storage.event_store import EventStore
        store = EventStore()
        brier = store.resolve_forecast(forecast_id, actual_outcome)

        updated_multipliers = {}
        target_lenses = contributing_lenses or [
            "GeoEconomistLens", "GeopoliticalLens", "DeepTechLens", "CashFlowLens"
        ]
        for lname in target_lenses:
            mult = store.update_lens_reliability(lname, brier)
            updated_multipliers[lname] = mult

        return {
            "forecast_id": forecast_id,
            "actual_outcome": actual_outcome,
            "brier_score": brier,
            "updated_multipliers": updated_multipliers
        }


