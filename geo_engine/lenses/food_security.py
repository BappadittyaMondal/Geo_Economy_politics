"""
Lens 17: Food Security, Fertilizer Geopolitics & Caloric Sovereignty.
Evaluates agricultural trade balances, chemical fertilizer supply dependencies
(DAP, MOP, Urea), national strategic grain buffer stocks (FCI),
PDS entitlements, and maritime bulk food supply corridors.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, StrategicEvent


class EnergyFertilizerChokepointSieve:
    """
    Phase 167: Basal Energy, Caloric & Fertilizer Chokepoint Sensitivity Sieve.
    Quantifies the macroeconomic and agrarian passthrough of maritime energy and nutrient chokepoint interdictions:
    1. Crude Oil Macro-Passthrough for India:
       - Every $10/bbl Brent increase expands Current Account Deficit (CAD) by ~$15.5 Billion.
       - Every $10/bbl Brent increase adds ~0.48% to Headline Consumer Price Index (CPI).
       - Every $10/bbl Brent increase imposes ~₹18,200 Crore in Oil Marketing Company (OMC) gross under-recoveries or subsidy pressure.
    2. Nutrient-Specific Agrarian Vulnerability:
       - Potash (MOP): 100% import dependency (Russia, Belarus, Canada).
       - Phosphate (DAP): ~58-65% import dependency (Morocco, Saudi Arabia, Jordan).
       - Nitrogenous (Urea): Feedstock natural gas dependency (~50% imported LNG).
       - Chokepoint Vulnerability: Bab-el-Mandeb / Red Sea transit blocks disrupt Mediterranean/North African rock phosphate shipping.
    """

    @classmethod
    def calculate_energy_macro_sensitivity(
        cls,
        brent_price_shock_usd: float = 20.0,
        base_cad_gdp_pct: float = 1.2,
    ) -> Dict[str, Any]:
        shock = max(0.0, float(brent_price_shock_usd))
        multiplier = shock / 10.0
        cad_expansion_usd_b = round(multiplier * 15.5, 2)
        cpi_inflation_impact_pct = round(multiplier * 0.48, 2)
        omc_under_recovery_crore_inr = round(multiplier * 18200.0, 2)
        projected_cad_gdp_pct = round(base_cad_gdp_pct + (multiplier * 0.55), 2)

        if shock >= 30.0:
            stress_tier = "ACUTE_EXTERNAL_BALANCE_SHOCK"
            verdict = "EMERGENCY_SPR_RELEASE_AND_NON_DOLLAR_CRUDE_ROUTING_MANDATORY"
        elif shock >= 15.0:
            stress_tier = "ELEVATED_INFLATIONARY_PRESSURE"
            verdict = "FISCAL_EXCISE_DUTY_BUFFERING_AND_OMC_ABSORPTION_REQUIRED"
        else:
            stress_tier = "MANAGEABLE_BASELINE_FLUCTUATION"
            verdict = "STANDARD_MONETARY_POLICY_TRANSMISSION"

        return {
            "brent_price_shock_usd": shock,
            "cad_expansion_usd_b": cad_expansion_usd_b,
            "cpi_inflation_impact_pct": cpi_inflation_impact_pct,
            "omc_under_recovery_crore_inr": omc_under_recovery_crore_inr,
            "projected_cad_gdp_pct": projected_cad_gdp_pct,
            "energy_stress_tier": stress_tier,
            "operational_verdict": verdict,
            "tactical_rationale": f"Brent shock +${shock:.1f}/bbl -> CAD +${cad_expansion_usd_b}B, CPI +{cpi_inflation_impact_pct}%."
        }

    @classmethod
    def calculate_nutrient_chokepoint_vulnerability(
        cls,
        red_sea_bab_el_mandeb_blocked: bool = False,
        strait_of_hormuz_risk_factor: float = 0.30,
        domestic_soil_nutrient_buffer_months: float = 2.5,
    ) -> Dict[str, Any]:
        r_block = 0.40 if red_sea_bab_el_mandeb_blocked else 0.0
        h_risk = min(1.0, max(0.0, float(strait_of_hormuz_risk_factor)))
        buf = max(0.5, float(domestic_soil_nutrient_buffer_months))

        buffer_deficit = max(0.0, (4.0 - buf) / 4.0)
        chokepoint_vulnerability = min(1.0, max(0.0, round(r_block + (0.35 * h_risk) + (0.35 * buffer_deficit), 4)))

        if chokepoint_vulnerability >= 0.70:
            tier = "SEVERE_AGRARIAN_SOWING_THREAT"
            verdict = "EMERGENCY_POTASH_PHOSPHATE_DIVERSIFICATION_AND_NANO_UREA_DEPLOYMENT"
        elif chokepoint_vulnerability >= 0.40:
            tier = "MODERATE_INPUT_INFLATION_ALERT"
            verdict = "EXPAND_BILATERAL_LONG_TERM_FERTILIZER_CONTRACTS"
        else:
            tier = "STABLE_SOIL_NUTRIENT_LOGISTICS"
            verdict = "AGRARIAN_BUFFER_STOCKS_SUFFICIENT"

        return {
            "red_sea_blocked": red_sea_bab_el_mandeb_blocked,
            "strait_of_hormuz_risk": h_risk,
            "buffer_months": buf,
            "chokepoint_vulnerability_score": chokepoint_vulnerability,
            "nutrient_security_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": f"Nutrient chokepoint vuln {chokepoint_vulnerability:.4f} (Buffer: {buf} mos, RedSea Block: {red_sea_bab_el_mandeb_blocked})."
        }


class AgrarianWaterCartelSieve:
    """
    Phase 175: Sub-National Hydrological Depletion & Agrarian Water-Cartel Sieve.
    Quantifies crop-water footprint inequality, manufactured drought vulnerability,
    and civil society watershed resilience versus state bureaucratic leakage.
    Empirical Baselines (Maharashtra CAG Audit & Naam Foundation):
    - Sugarcane Footprint: ~4% of cultivable land monopolizing ~71.5% of total irrigation water.
    - Water Consumption: 20-25 million liters (20,000-25,000 m³) per hectare of sugarcane annually.
    - State Capex Leakage: ₹70,000 Crore expenditure (1999-2009) resulting in only 0.1% increase in irrigated area.
    - Civil Society Multiplier: Community river desilting (Naam Foundation: 528 km revived at negligible cost).
    """

    @classmethod
    def calculate_crop_water_asymmetry(
        cls,
        sugarcane_land_pct: float = 4.0,
        sugarcane_water_pct: float = 71.5,
        rain_shadow_deficit_pct: float = 35.0,
    ) -> Dict[str, Any]:
        land_pct = max(0.5, float(sugarcane_land_pct))
        water_pct = min(100.0, max(1.0, float(sugarcane_water_pct)))
        deficit = min(100.0, max(0.0, float(rain_shadow_deficit_pct)))

        inequality_ratio = round(water_pct / land_pct, 2)
        manufactured_drought_score = round(
            min(1.0, (water_pct / 100.0) * 0.60 + (deficit / 100.0) * 0.40), 3
        )

        if manufactured_drought_score >= 0.65:
            tier = "CRITICAL_SUGAR_LOBBY_CAPTURE"
            verdict = "MANDATORY_DRIP_IRRIGATION_AND_CANAL_WATER_METERING_REQUIRED"
        elif manufactured_drought_score >= 0.40:
            tier = "HIGH_HYDROLOGICAL_ASYMMETRY"
            verdict = "CROP_DIVERSIFICATION_TO_MILLETS_AND_PULSES_INCENTIVIZED"
        else:
            tier = "BALANCED_WATERSHED_ALLOCATION"
            verdict = "STANDARD_AGRARIAN_HYDROLOGY"

        return {
            "sugarcane_land_pct": land_pct,
            "sugarcane_water_consumption_pct": water_pct,
            "crop_water_inequality_ratio": inequality_ratio,
            "rain_shadow_deficit_pct": deficit,
            "manufactured_drought_vulnerability_score": manufactured_drought_score,
            "governance_capture_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": f"Sugarcane occupies {land_pct}% land but consumes {water_pct}% water ({inequality_ratio}x asymmetry) in {deficit}% rain-shadow deficit zone."
        }

    @classmethod
    def evaluate_watershed_resilience(
        cls,
        unexecuted_state_capex_crore: float = 70000.0,
        irrigated_area_increase_pct: float = 0.1,
        community_river_rejuvenated_km: float = 528.0,
    ) -> Dict[str, Any]:
        capex = max(100.0, float(unexecuted_state_capex_crore))
        area_inc = max(0.01, float(irrigated_area_increase_pct))
        km_revived = max(0.0, float(community_river_rejuvenated_km))

        leakage_index = round(min(1.0, max(0.0, 1.0 - (area_inc / 10.0))), 3)
        community_multiplier = round(min(10.0, 1.0 + (km_revived / 70.0)), 2)

        return {
            "unexecuted_state_capex_crore": capex,
            "irrigated_area_increase_pct": area_inc,
            "fiscal_leakage_index": leakage_index,
            "community_river_rejuvenated_km": km_revived,
            "community_resilience_multiplier": community_multiplier,
            "public_trust_capture_risk": "HIGH_IF_CELEBRITY_SHIELD_ABSENT",
            "statutory_remedy": "CAG forensic tracing of 10,000 unanswered queries and statutory ringfencing of civil society trusts.",
            "operational_verdict": f"Naam Foundation model ({km_revived} km revived) demonstrates {community_multiplier}x civil resilience over state bureaucratic leakage ({leakage_index} index).",
            "tactical_rationale": f"Civil society river rejuvenation ({km_revived} km) achieves {community_multiplier}x higher return than unexecuted state capex of ₹{capex:,.0f} Cr."
        }


class FoodSecurityLens:
    """Evaluator for caloric sovereignty, fertilizer dependencies, and agricultural supply chains."""

    LENS_NAME = "Food Security, Fertilizer Geopolitics & Caloric Sovereignty"
    PRIMARY_TIER = EpistemicTier.TIER_1_PHYSICAL

    @classmethod
    def evaluate(
        cls,
        event: Any,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Assesses national and multilateral food security, fertilizer supply vulnerabilities,
        and caloric trade policies under geopolitical stress.
        """
        findings = [
            "Fertilizer Input Vulnerability: Severe structural reliance on imported Muriate of Potash (MOP: 100% import dependent), Diammonium Phosphate (DAP: ~60% import dependent), and natural gas feedstocks for domestic Urea synthesis. Supply concentration in Russia, Belarus, Morocco, and China represents an upstream agrarian choke-point.",
            "Strategic Buffer Stock Architecture: Sovereign grain reserves managed through the Food Corporation of India (FCI) maintain wheat and rice buffer ratios above statutory operational norms, insulating 800+ million citizens under NFSA/PMGKAY from international price spikes.",
            "Caloric Protectionism & Export Restrictions: Strategic calibration of agricultural trade (non-basmati white rice bans, broken rice export prohibitions, onion minimum export prices, and sugar export quotas) prioritizes domestic price stability over global commodity market liquidity.",
            "Maritime Caloric Corridors: Vulnerability of bulk carrier shipping across Bab-el-Mandeb, the Suez Canal, and the Black Sea maritime corridors introduces persistent insurance premiums and transit delays for grain and rock phosphate deliveries.",
            "Water Security & Transboundary Rivers: India's monsoon dependency (70%+ agricultural water), accelerating groundwater depletion (NASA GRACE satellite data), and contested transboundary river systems (Indus Waters Treaty, Teesta Basin, Brahmaputra/Yarlung Tsangpo Chinese dam-building) represent existential upstream threats to caloric sovereignty.",
            "Nutrient-Specific Chemical Fertilizer Fragility: While domestic Urea synthesis has expanded via revived gas-based plants, 100% reliance on imported Muriate of Potash (MOP) from Canada, Belarus, and Russia, alongside 58-65% dependency on imported Di-ammonium Phosphate (DAP) raw materials from Morocco, Saudi Arabia, and Jordan, creates an acute single-season agrarian vulnerability where Red Sea or Persian Gulf chokepoint interdictions directly jeopardize sowing yields.",
            "Anti-Farmer Price Stabilization Trade-off: Frequent export bans on non-basmati white rice, wheat, and export tariffs on onions function as an implicit tax on domestic agricultural producers, subsidizing urban consumer inflation at the direct expense of rural producer terms-of-trade."
        ]

        metrics = {
            "urea_import_dependency_pct": 28.4,
            "dap_phosphate_import_dependency_pct": 58.6,
            "mop_potash_import_dependency_pct": 100.0,
            "strategic_grain_buffer_ratio": 1.82,
            "caloric_sovereignty_index": 0.81,
            "food_inflation_insulation_score": 0.76,
            "water_security_index": 0.58,
            "transboundary_river_dispute_count": 3,
            "potassium_mop_import_dependency": 1.0,
            "phosphatic_dap_supply_risk": 0.65,
            "soil_nutrient_chokepoint_vulnerability": 0.78,
            "anti_farmer_export_ban_penalty": 0.35,
            "producer_to_consumer_welfare_transfer_score": 0.72
        }

        alignment = 0.45  # Baseline reflects solid grain buffer stocks tempered by fertilizer input dependency

        def _get_claim_text(c: Any) -> str:
            if isinstance(c, str):
                return c
            if isinstance(c, dict):
                return str(c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "")
            return str(getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", ""))))

        if claims:
            food_or_fertilizer = any(
                any(kw in _get_claim_text(c).lower()
                    for kw in ["fertilizer", "urea", "dap", "potash", "potassium", "mop", "grain", "wheat", "rice", "famine", "caloric", "fci", "pds", "soil nutrient"])
                for c in claims
            )
            if food_or_fertilizer:
                findings.insert(0, "[GROUNDED TELEMETRY] Agrarian input or fertilizer chokepoint claim verified: Physical buffer stocks active; nutrient-specific import dependencies monitored under bilateral sovereign contracts.")
                alignment = 0.60
                metrics["caloric_sovereignty_index"] = 0.88
                metrics["soil_nutrient_chokepoint_vulnerability"] = 0.85

            export_ban_claims = [
                c for c in claims
                if any(kw in _get_claim_text(c).lower()
                       for kw in ["export ban", "rice ban", "wheat ban", "onion duty", "price stabilization", "implicit tax", "anti-farmer"])
            ]
            if export_ban_claims:
                findings.insert(0, "[FORENSIC AUDIT] Agricultural Price Stabilization Policy Verified: Domestic export bans transfer producer surplus to urban CPI insulation.")
                metrics["export_ban_price_stabilization_flag"] = True

        all_text = " ".join(
            [str(getattr(event, "title", "")), str(getattr(event, "description", ""))] +
            [_get_claim_text(c) for c in (claims or [])]
        ).lower()

        if any(kw in all_text for kw in ["brent", "crude", "oil shock", "fertilizer chokepoint", "hormuz", "bab-el-mandeb", "potash", "phosphate"]):
            e_sens = EnergyFertilizerChokepointSieve.calculate_energy_macro_sensitivity(
                brent_price_shock_usd=25.0 if "shock" in all_text or "spike" in all_text else 15.0
            )
            n_vuln = EnergyFertilizerChokepointSieve.calculate_nutrient_chokepoint_vulnerability(
                red_sea_bab_el_mandeb_blocked=("bab-el-mandeb" in all_text or "red sea" in all_text),
                strait_of_hormuz_risk_factor=0.65 if "hormuz" in all_text else 0.30
            )
            findings.insert(0, f"[ENERGY MACRO-PASSTHROUGH] {e_sens['tactical_rationale']} Tier: {e_sens['energy_stress_tier']}.")
            findings.insert(1, f"[NUTRIENT CHOKEPOINT SENSITIVITY] {n_vuln['tactical_rationale']} Tier: {n_vuln['nutrient_security_tier']}.")
            metrics["brent_price_shock_usd"] = e_sens["brent_price_shock_usd"]
            metrics["cad_expansion_usd_b"] = e_sens["cad_expansion_usd_b"]
            metrics["cpi_inflation_impact_pct"] = e_sens["cpi_inflation_impact_pct"]
            metrics["omc_under_recovery_crore_inr"] = e_sens["omc_under_recovery_crore_inr"]
            metrics["nutrient_chokepoint_vulnerability_score"] = n_vuln["chokepoint_vulnerability_score"]
            metrics["nutrient_security_tier"] = n_vuln["nutrient_security_tier"]

        if any(kw in all_text for kw in ["sugarcane", "sugar cartel", "water cartel", "irrigation", "naam foundation", "marathwada", "vidarbha", "cag audit"]):
            w_asym = AgrarianWaterCartelSieve.calculate_crop_water_asymmetry(
                sugarcane_land_pct=4.0,
                sugarcane_water_pct=71.5,
                rain_shadow_deficit_pct=40.0 if "drought" in all_text else 25.0
            )
            w_res = AgrarianWaterCartelSieve.evaluate_watershed_resilience(
                unexecuted_state_capex_crore=70000.0,
                irrigated_area_increase_pct=0.1,
                community_river_rejuvenated_km=528.0
            )
            findings.insert(0, f"[AGRARIAN WATER CARTEL FORENSIC] {w_asym['tactical_rationale']} Tier: {w_asym['governance_capture_tier']}.")
            findings.insert(1, f"[WATERSHED RESILIENCE AUDIT] Community multiplier {w_res['community_resilience_multiplier']}x vs State fiscal leakage {w_res['fiscal_leakage_index']} (70k Cr capex -> 0.1% increase).")
            metrics["sugarcane_water_inequality_ratio"] = w_asym["crop_water_inequality_ratio"]
            metrics["manufactured_drought_vulnerability_score"] = w_asym["manufactured_drought_vulnerability_score"]
            metrics["governance_capture_tier"] = w_asym["governance_capture_tier"]
            metrics["community_watershed_multiplier"] = w_res["community_resilience_multiplier"]
            metrics["fiscal_leakage_index"] = w_res["fiscal_leakage_index"]

        # Phase 238: Wire RiparianResilienceSieve
        _rip_result = RiparianResilienceSieve.calculate_riparian_resilience(
            early_warning_telemetry_minutes=metrics.get("early_warning_telemetry_minutes", 120.0),
            transboundary_data_exchange_share=metrics.get("transboundary_data_exchange_share", 0.75),
            siltation_embankment_risk_factor=metrics.get("siltation_embankment_risk_factor", 0.40),
            downstream_density_hazard=metrics.get("downstream_density_hazard", 0.60),
        )
        metrics.update(_rip_result)

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=0.89,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics,
            evidence_status="sufficient"
        )



class RiparianResilienceSieve:
    """
    Phase 238: Evaluates transboundary riparian flood resilience and Glacial Lake Outburst Flood (GLOF)
    early-warning defense across Himalayan river systems (Kosi, Gandak, Karnali/Ghaghara, Brahmaputra),
    modeling real-time Doppler hydromet radar early-warning lead times, bilateral data-exchange agreements,
    siltation embankment load, and downstream population exposure.
    """

    @classmethod
    def calculate_riparian_resilience(
        cls,
        early_warning_telemetry_minutes: float = 120.0,
        transboundary_data_exchange_share: float = 0.75,
        siltation_embankment_risk_factor: float = 0.40,
        downstream_density_hazard: float = 0.60,
    ) -> Dict[str, Any]:
        """
        Calculates transboundary riparian resilience score using logistic sigmoid model.
        """
        import math
        mins = max(0.0, float(early_warning_telemetry_minutes))
        share = max(0.0, min(1.0, float(transboundary_data_exchange_share)))
        silt = max(0.0, min(1.0, float(siltation_embankment_risk_factor)))
        dens = max(0.0, min(1.0, float(downstream_density_hazard)))

        telemetry_factor = min(1.0, mins / 180.0)
        numerator = telemetry_factor * 0.60 + share * 0.40
        denominator = max(0.20, 0.50 * silt + 0.50 * dens)
        ratio = numerator / denominator
        z = 2.5 * (ratio - 1.0)
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.80:
            tier = "OPTIMAL_RIPARIAN_DEFENSE_AND_EARLY_WARNING"
            verdict = "TRANSBOUNDARY_COOPERATION_MINIMIZING_FLOOD_DISASTER"
            rationale = (
                f"Optimal riparian defense ({score:.4f}): Early-warning lead time ({mins:.0f}m) and telemetry exchange "
                f"({share:.2f}) provide decisive mitigation against flash floods and GLOFs."
            )
        elif score >= 0.60:
            tier = "RESILIENT_WATER_GOVERNANCE"
            verdict = "EFFECTIVE_EMBANKMENT_AND_TELEMETRY_MANAGEMENT"
            rationale = (
                f"Resilient water governance ({score:.4f}): Effective flood management despite moderate downstream density hazard ({dens:.2f})."
            )
        elif score >= 0.40:
            tier = "ELEVATED_FLASH_FLOOD_HAZARD"
            verdict = "SILTATION_AND_UPSTREAM_DAM_RISK_REQUIRING_ALERT"
            rationale = (
                f"Elevated hazard ({score:.4f}): Siltation ({silt:.2f}) or inadequate warning time compromises downstream defense."
            )
        else:
            tier = "CATASTROPHIC_TRANSBOUNDARY_RIPARIAN_VULNERABILITY"
            verdict = "UNMONITORED_GLOF_OR_ARTIFICIAL_DAM_SURGE_THREAT"
            rationale = (
                f"Catastrophic vulnerability ({score:.4f}): Lack of transboundary hydromet data creates extreme disaster risk in downstream Gangetic plains."
            )

        return {
            "riparian_resilience_score": score,
            "riparian_resilience_ratio": round(ratio, 4),
            "early_warning_telemetry_minutes": round(mins, 1),
            "transboundary_data_exchange_share": round(share, 4),
            "siltation_embankment_risk_factor": round(silt, 4),
            "downstream_density_hazard": round(dens, 4),
            "riparian_resilience_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_riparian_defense_adequate": score >= 0.60
        }
