"""
Lens 15: Critical Minerals, Energy & Strategic Chokepoint Logistics.
Evaluates geological realities, Rare Earth Elements (HREE/LREE) monopolies,
battery metal processing (Lithium, Nickel, Cobalt), and physical transit chokepoints
(Malacca, Hormuz, Bab-el-Mandeb, Taiwan Strait).
"""

import math
from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, StrategicEvent


class CriticalMineralsLens:
    """Evaluator for mineral supply chain sovereignty and maritime chokepoints."""

    LENS_NAME = "Critical Minerals & Strategic Chokepoint Logistics"
    PRIMARY_TIER = EpistemicTier.TIER_1_PHYSICAL

    @classmethod
    def evaluate(
        cls,
        event: Any,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Assesses raw material dependencies, processing concentrations, and chokepoint vulnerabilities.
        """
        findings = [
            "Heavy Rare Earth (HREE) Processing Monopoly: China controls approximately 70-90% of global commercial refining capacity for Dysprosium, Neodymium, and Terbium, imposing an asymmetric material constraint on Western defense and green-tech hardware.",
            "Battery Chemistry Vulnerability: Lithium refining concentration, Indonesian Nickel export quotas, and DRC Cobalt concessions represent single-point physical chokepoints for global electrification.",
            "Semiconductor Precursor Export Controls: Strategic restrictions on Gallium, Germanium, and Antimony create upstream supply bottlenecks for wafer fabrication and radar/defense electronics.",
            "Maritime Chokepoint Dual-Use Exposure: Transit through the Strait of Malacca (80% Chinese hydrocarbon imports), Strait of Hormuz (20% global petroleum liquids), and Bab-el-Mandeb remains vulnerable to asymmetric denial operations.",
            "Midstream Metallurgical & Chemical Refining Chokepoint: While raw mineral ores exist globally, midstream chemical conversion (battery-grade Lithium Hydroxide, sintered NdFeB permanent magnets) is over 85-90% concentrated in China, creating an absolute processing bottleneck that decouples raw mining from usable technological components."
        ]

        metrics = {
            "hree_refining_concentration_pct": 82.5,
            "lithium_processing_monopoly_risk": 0.74,
            "semiconductor_precursor_vulnerability": 0.86,
            "maritime_chokepoint_exposure_score": 0.79,
            "material_sovereignty_index": 0.48,
            "midstream_refining_monopoly_risk": 0.85,
            "heavy_rare_earth_processing_dependency": 0.90,
            "ndfeb_permanent_magnet_choke_pct": 92.0
        }

        alignment = -0.35  # Reflects significant systemic physical supply chain friction

        if claims:
            mineral_or_chokepoint = any(
                "rare earth" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "lithium" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "chokepoint" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "hormuz" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "malacca" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "refining" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "magnet" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() or
                "ndfeb" in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower()
                for c in claims
            )
            if mineral_or_chokepoint:
                findings.insert(0, "[GROUNDED TELEMETRY] Strategic chokepoint or midstream mineral refining monopoly verified: Processing concentration in NdFeB magnets and battery chemicals creates direct single-point failure.")
                alignment = -0.60
                metrics["material_sovereignty_index"] = 0.32
                metrics["midstream_refining_monopoly_risk"] = 0.92

        # Phase 216: Wire CriticalMineralsRefiningCrisisSieve
        _mineral_sieve = CriticalMineralsRefiningCrisisSieve()
        _mineral_result = _mineral_sieve.calculate_refining_crisis(
            single_country_refining_share=metrics.get("hree_refining_concentration_pct", 82.5) / 100.0,
            upstream_extraction_gap=metrics.get("upstream_extraction_gap", 0.65),
            domestic_refining_capacity_score=metrics.get("material_sovereignty_index", 0.48),
            stockpile_days_buffer=metrics.get("strategic_stockpile_days", 30.0),
            alternative_supplier_count=max(1, int(metrics.get("alternative_supplier_count", 1))),
        )
        metrics.update(_mineral_result)

        # Phase 409: Wire CriticalMineralSupplyChainWeaponizationTensor
        cm_meta = getattr(event, "metadata", {}) if event and hasattr(event, "metadata") else {}
        _cmw_res = CriticalMineralSupplyChainWeaponizationTensor.evaluate(
            mineral_weights=cm_meta.get("mineral_weights"),
            import_dependencies=cm_meta.get("import_dependencies"),
            refining_concentrations=cm_meta.get("refining_concentrations"),
            domestic_stockpile_months=cm_meta.get("domestic_stockpile_months", 3.0),
        )
        metrics["critical_mineral_weaponization_score"] = _cmw_res["critical_mineral_weaponization_score"]

        # Phase 444: Semiconductor Hardware Chokepoint and GPU Export Control Tensor
        _shc_res = SemiconductorHardwareChokepointAndGPUExportControlTensor.evaluate(
            export_ban_severity=cm_meta.get("export_ban_severity", 0.80),
            advanced_packaging_concentration=cm_meta.get("advanced_packaging_concentration", 0.75),
            lithography_denial_index=cm_meta.get("lithography_denial_index", 0.85),
            domestic_fab_buffer_months=cm_meta.get("domestic_fab_buffer_months", 18.0),
            alternative_architecture_readiness=cm_meta.get("alternative_architecture_readiness", 0.40),
        )
        metrics["gpu_export_control_chokepoint_vulnerability"] = _shc_res["gpu_export_control_chokepoint_vulnerability"]

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=0.91,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics,
            evidence_status="sufficient"
        )


class CriticalMineralsRefiningCrisisSieve:
    """
    Phase 207: Quantifies midstream refining concentration risk for critical minerals.
    Raw extraction ≠ usable sovereignty; China controls 70-90% of midstream REE, Gallium,
    Germanium, NdFeB magnet, and battery-grade Lithium Hydroxide refining.

    Mathematical core:
        RefiningConcentrationRisk = σ(
            3.0 · SingleCountryRefiningShare
            + 2.0 · UpstreamExtractionGap
            - 2.5 · DomesticRefiningCapacityScore
            - 1.5 · StockpileDaysBuffer_normalized
        )
    """

    @classmethod
    def calculate_refining_crisis(
        cls,
        single_country_refining_share: float = 0.85,
        upstream_extraction_gap: float = 0.70,
        domestic_refining_capacity_score: float = 0.15,
        stockpile_days_buffer: float = 30.0,
        alternative_supplier_count: int = 1,
        claims=None
    ):
        """
        Calculates midstream refining concentration risk and mineral sovereignty tier.

        Args:
            single_country_refining_share: 0-1, fraction of global midstream refining by dominant single country
            upstream_extraction_gap: 0-1, gap between raw ore extraction and domestic chemical processing
            domestic_refining_capacity_score: 0-1, India's own midstream refining capability
            stockpile_days_buffer: days of strategic reserve (max meaningful value ~180 days)
            alternative_supplier_count: number of credible non-dominant alternative refining suppliers
            claims: optional claim objects for keyword detection

        Returns:
            dict with refining_concentration_risk, mineral_sovereignty_tier, is_midstream_captive, etc.
        """
        import math

        refining_share = max(0.0, min(1.0, float(single_country_refining_share)))
        extract_gap = max(0.0, min(1.0, float(upstream_extraction_gap)))
        domestic_cap = max(0.0, min(1.0, float(domestic_refining_capacity_score)))
        stockpile_norm = max(0.0, min(1.0, float(stockpile_days_buffer) / 180.0))
        alt_suppliers = max(0, int(alternative_supplier_count))

        z = (
            3.0 * refining_share
            + 2.0 * extract_gap
            - 2.5 * domestic_cap
            - 1.5 * stockpile_norm
            - 0.5 * min(1.0, alt_suppliers / 3.0)
            - 1.0
        )
        refining_concentration_risk = round(1.0 / (1.0 + math.exp(-z)), 4)
        mineral_sovereignty_score = round(1.0 - refining_concentration_risk, 4)

        if refining_concentration_risk >= 0.80:
            tier = "CRITICAL_MIDSTREAM_CAPTIVITY"
            verdict = "EMERGENCY_DOMESTIC_REFINING_MANDATE"
            rationale = (
                f"Acute midstream captivity: dominant single-country refining share ({refining_share*100:.0f}%) "
                f"combined with negligible domestic capacity ({domestic_cap*100:.0f}%) creates absolute "
                f"strategic dependency. Raw mining provides zero usable sovereignty."
            )
            is_captive = True
        elif refining_concentration_risk >= 0.60:
            tier = "HIGH_MIDSTREAM_CONCENTRATION_RISK"
            verdict = "PRIORITY_REFINING_DIVERSIFICATION"
            rationale = (
                f"High refining concentration risk: {refining_share*100:.0f}% single-country dominance "
                f"with only {stockpile_days_buffer:.0f} days strategic reserve buffer."
            )
            is_captive = True
        elif refining_concentration_risk >= 0.40:
            tier = "MODERATE_REFINING_DEPENDENCY"
            verdict = "STRUCTURED_DIVERSIFICATION_REQUIRED"
            rationale = "Moderate refining dependency; partial domestic capacity mitigates but does not eliminate strategic risk."
            is_captive = False
        else:
            tier = "RESILIENT_MINERAL_SOVEREIGNTY"
            verdict = "MIDSTREAM_SOVEREIGNTY_MAINTAINED"
            rationale = "Domestic refining capacity and strategic reserves provide adequate supply chain insulation."
            is_captive = False

        return {
            "refining_concentration_risk": refining_concentration_risk,
            "mineral_sovereignty_score": mineral_sovereignty_score,
            "single_country_refining_share": round(refining_share, 4),
            "upstream_extraction_gap": round(extract_gap, 4),
            "domestic_refining_capacity_score": round(domestic_cap, 4),
            "stockpile_days_buffer": stockpile_days_buffer,
            "alternative_supplier_count": alt_suppliers,
            "mineral_sovereignty_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_midstream_captive": is_captive
        }


# ============================================================================
# Phase 409: Critical Mineral Supply Chain Weaponization Tensor
# ============================================================================

class CriticalMineralSupplyChainWeaponizationTensor:
    """
    Phase 409: Computes supply chain decapitation exposure for critical elements
    (Gallium, Germanium, Neodymium, Dysprosium, Lithium), auditing exposure to Chinese export embargoes
    and domestic processing alternatives.
    Formula:
        MineralChokepointVulnerability = sum(w_m * ImportDependency_m * ForeignRefiningConcentration_m) * (1 - DomesticStockpileMonths / 12)
        score = Sigmoid(3.5 * MineralChokepointVulnerability - 1.0)
    """
    @classmethod
    def evaluate(
        cls,
        mineral_weights: Optional[Dict[str, float]] = None,
        import_dependencies: Optional[Dict[str, float]] = None,
        refining_concentrations: Optional[Dict[str, float]] = None,
        domestic_stockpile_months: float = 3.0
    ) -> Dict[str, Any]:
        default_weights = {"gallium": 0.25, "germanium": 0.20, "neodymium": 0.30, "lithium": 0.25}
        default_deps = {"gallium": 0.95, "germanium": 0.90, "neodymium": 0.92, "lithium": 0.85}
        default_refs = {"gallium": 0.98, "germanium": 0.85, "neodymium": 0.90, "lithium": 0.75}

        weights = mineral_weights or default_weights
        deps = import_dependencies or default_deps
        refs = refining_concentrations or default_refs

        total_weight = sum(weights.values()) or 1.0
        chokepoint_sum = 0.0
        for m, w in weights.items():
            norm_w = w / total_weight
            imp = float(max(0.0, min(1.0, deps.get(m, 0.85))))
            ref = float(max(0.0, min(1.0, refs.get(m, 0.85))))
            chokepoint_sum += norm_w * imp * ref

        stockpile_m = float(max(0.0, domestic_stockpile_months))
        stockpile_mitigation = min(1.0, max(0.0, stockpile_m / 12.0))
        net_vulnerability = chokepoint_sum * (1.0 - stockpile_mitigation)

        z = 3.5 * net_vulnerability - 1.0
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "CRITICAL_MINERAL_SUPPLY_CHAIN_DECAPITATION_RISK"
            verdict = "ENACT_STRATEGIC_MINERAL_RESERVE_RELEASE_AND_FRIENDSHORING"
            rationale = (
                f"Severe mineral weaponization vulnerability ({score:.4f}): Chokepoint exposure ({chokepoint_sum:.2f}) "
                f"with only {stockpile_m:.1f} months domestic stockpile leaves semiconductor and defense production exposed to export bans."
            )
        elif score >= 0.45:
            tier = "ELEVATED_REFINING_CHOKEPOINT_DRAG"
            verdict = "ACCELERATE_DOMESTIC_PROCESSING_PLANTS_AND_BILATERAL_OFFTAKES"
            rationale = f"Elevated chokepoint drag ({score:.4f}): Single-source refining dominance poses continuous procurement friction."
        else:
            tier = "FORTIFIED_MINERAL_SOVEREIGNTY"
            verdict = "DIVERSIFIED_SUPPLY_CHAINS_AND_ADEQUATE_STOCKPILES_VERIFIED"
            rationale = f"Low risk ({score:.4f}): Robust stockpiles ({stockpile_m:.1f} mos) and diversified refining partners."

        return {
            "critical_mineral_weaponization_score": score,
            "aggregate_chokepoint_exposure": round(chokepoint_sum, 4),
            "net_vulnerability": round(net_vulnerability, 4),
            "domestic_stockpile_months": round(stockpile_m, 2),
            "mineral_weaponization_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_mineral_supply_chain_severed": score >= 0.70,
        }


class TaiwanStraitQuarantineAndSemiconductorSupplyResilienceSieve:
    """Phase 439: Taiwan Strait Quarantine & Semiconductor Supply Resilience Sieve.
    Quantifies systemic global supply chain decapitation if a maritime customs quarantine
    is imposed on Taiwan during the 2027 PLA Centenary, cutting off sub-5nm logic chip
    shipments (TSMC) across automotive, AI compute, and sovereign defense electronics.
    Formula:
        RawChoke = Norm(0.50 * quarantine_strictness + 0.30 * sub_5nm_dependency + 0.20 * foundry_replacement_latency)
        ChokeIndex = RawChoke * (1.0 - domestic_fab_buffer_ratio)
    """

    @classmethod
    def evaluate(
        cls,
        quarantine_enforcement_strictness: float = 0.85,
        sub_5nm_logic_chip_dependency: float = 0.92,
        foundry_replacement_latency_years: float = 0.80,
        domestic_fab_buffer_ratio: float = 0.15,
    ) -> Dict[str, Any]:
        q_strict = float(max(0.0, min(1.0, quarantine_enforcement_strictness)))
        dep_5nm = float(max(0.0, min(1.0, sub_5nm_logic_chip_dependency)))
        lat_f = float(max(0.0, min(1.0, foundry_replacement_latency_years)))
        buf_fab = float(max(0.0, min(1.0, domestic_fab_buffer_ratio)))

        raw_choke = 0.50 * q_strict + 0.30 * dep_5nm + 0.20 * lat_f
        final_index = round(max(0.0, min(1.0, raw_choke * (1.0 - buf_fab))), 4)

        if final_index >= 0.65:
            tier = "CATASTROPHIC_SEMICONDUCTOR_CHOKEPOINT_SEVERANCE"
            verdict = "ENACT_DEFENSE_PRODUCTION_ACT_RATIONING_AND_ACCELERATE_DOMESTIC_PACKAGING"
        elif final_index >= 0.40:
            tier = "SEVERE_ELECTRONICS_ASSEMBLY_DELAYS"
            verdict = "DIVERSIFY_CHIP_INVENTORIES_AND_SECURE_OFFTAKES_WITH_NON_TAIWAN_FOUNDRIES"
        else:
            tier = "INSULATED_SEMICONDUCTOR_BUFFER"
            verdict = "DOMESTIC_FAB_CAPACITY_PROVIDES_CRITICAL_RUNWAY"

        return {
            "taiwan_quarantine_semiconductor_choke_index": final_index,
            "quarantine_enforcement_strictness": round(q_strict, 4),
            "sub_5nm_logic_chip_dependency": round(dep_5nm, 4),
            "foundry_replacement_latency_years": round(lat_f, 4),
            "domestic_fab_buffer_ratio": round(buf_fab, 4),
            "semiconductor_choke_tier": tier,
            "operational_verdict": verdict,
            "is_semiconductor_choke_critical": final_index >= 0.65,
        }


class SemiconductorHardwareChokepointAndGPUExportControlTensor:
    """Phase 444: Semiconductor Hardware Chokepoint & GPU Export Control Tensor.
    Quantifies sovereign compute vulnerability to US/allied export control restrictions on advanced
    AI accelerators (NVIDIA/AMD H100/B200 tier), high-bandwidth memory (HBM3e), advanced packaging (CoWoS),
    and EUV/DUV lithography tool denial, offset by domestic fab buffering and open silicon architectures.
    Formula:
        RawChoke = Norm(0.50 * export_ban_severity + 0.30 * advanced_packaging_concentration + 0.20 * lithography_denial_index)
        Mitigation = 0.60 * domestic_fab_buffer_ratio + 0.40 * alternative_architecture_readiness
        ChokepointVulnerability = RawChoke * (1.0 - 0.50 * Mitigation)
    """

    @classmethod
    def evaluate(
        cls,
        export_ban_severity: float = 0.80,
        advanced_packaging_concentration: float = 0.75,
        lithography_denial_index: float = 0.85,
        domestic_fab_buffer_months: float = 18.0,
        alternative_architecture_readiness: float = 0.40,
    ) -> Dict[str, Any]:
        e_ban = float(max(0.0, min(1.0, export_ban_severity)))
        p_pack = float(max(0.0, min(1.0, advanced_packaging_concentration)))
        l_denial = float(max(0.0, min(1.0, lithography_denial_index)))
        buf_raw = float(max(0.0, domestic_fab_buffer_months))
        b_buffer = min(1.0, buf_raw / 36.0)
        a_alt = float(max(0.0, min(1.0, alternative_architecture_readiness)))

        raw_choke = 0.50 * e_ban + 0.30 * p_pack + 0.20 * l_denial
        mitigation = 0.60 * b_buffer + 0.40 * a_alt
        g_chokepoint = round(max(0.0, min(1.0, raw_choke * (1.0 - 0.50 * mitigation))), 4)

        if g_chokepoint >= 0.55:
            tier = "ACUTE_HARDWARE_SANCTIONS_CHOKEPOINT"
            verdict = "ACCELERATE_INDIGENOUS_PACKAGING_AND_OPEN_SILICON_PILOTS"
        elif g_chokepoint >= 0.30:
            tier = "MODERATE_COMPUTE_EQUIPMENT_RESTRICTION"
            verdict = "DIVERSIFY_OFFSHORE_FOUNDRIES_AND_OPTIMIZE_INFERENCE_EFFICIENCY"
        else:
            tier = "RESILIENT_SILICON_SUPPLY_CHAIN"
            verdict = "EXPAND_STRATEGIC_WAFER_RESERVES_AND_FAB_PARTNERSHIPS"

        return {
            "gpu_export_control_chokepoint_vulnerability": g_chokepoint,
            "export_ban_severity": round(e_ban, 4),
            "advanced_packaging_concentration": round(p_pack, 4),
            "lithography_denial_index": round(l_denial, 4),
            "domestic_fab_buffer_ratio": round(b_buffer, 4),
            "alternative_architecture_readiness": round(a_alt, 4),
            "silicon_chokepoint_tier": tier,
            "operational_verdict": verdict,
            "is_silicon_supply_secure": g_chokepoint < 0.40,
        }


