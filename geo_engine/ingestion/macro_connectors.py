"""
Sovereign Macro Telemetry Connectors for Geo-Engine.
Provides deterministic calculators converting raw trade, banking, and fiscal indicators
into normalized, epistemically prioritized ClaimItem objects for ingestion into EventStore.
"""

from typing import Any, Dict, Tuple
from .models import ClaimItem, ClaimType, EpistemicTier


class SovereignMacroConnectors:
    """Calculates macro forensic indicators and converts them into verified ClaimItem objects."""

    @classmethod
    def compute_china_trade_gap(
        cls,
        dgft_imports_usd_b: float,
        gacc_exports_usd_b: float
    ) -> Tuple[Dict[str, Any], ClaimItem]:
        """
        Calculates bilateral customs trade divergence between Indian DGFT and Chinese GACC data.
        Quantifies under-invoicing and tariff evasion.
        """
        trade_gap_usd_b = round(gacc_exports_usd_b - dgft_imports_usd_b, 2)
        divergence_pct = round((trade_gap_usd_b / dgft_imports_usd_b) * 100.0, 2) if dgft_imports_usd_b > 0 else 0.0

        metrics = {
            "dgft_reported_imports_usd_b": dgft_imports_usd_b,
            "gacc_reported_exports_usd_b": gacc_exports_usd_b,
            "trade_gap_usd_b": trade_gap_usd_b,
            "divergence_pct": divergence_pct,
            "under_invoicing_risk": "HIGH" if trade_gap_usd_b >= 15.0 else ("MODERATE" if trade_gap_usd_b >= 5.0 else "LOW")
        }

        fact_text = (
            f"Bilateral trade gap divergence: Chinese GACC reports ${gacc_exports_usd_b:.1f}B exports to India, "
            f"while Indian DGFT reports ${dgft_imports_usd_b:.1f}B imports (unaccounted gap: ${trade_gap_usd_b:.1f}B, {divergence_pct}% divergence), "
            f"evidencing customs under-invoicing and third-party transshipment."
        )

        claim = ClaimItem(
            claim_id=f"CLM-MACRO-TRADEGAP-{int(trade_gap_usd_b * 10)}",
            source_evidence_id="SRC-CUSTOMS-MIRROR",
            claim_type=ClaimType.GENERAL_INTEL,
            epistemic_tier=EpistemicTier.TIER_2_FINANCIAL,
            actors=["India", "China"],
            asserted_fact=fact_text,
            target_lenses=["GeoEconomistLens", "CashFlowLens"],
            metrics=metrics,
            reliability_weight=0.96,
            evidence_status="sufficient"
        )

        return metrics, claim

    @classmethod
    def compute_banking_npa_recovery_ratio(
        cls,
        write_offs_usd_b: float,
        cash_recoveries_usd_b: float,
        recap_subsidy_usd_b: float
    ) -> Tuple[Dict[str, Any], ClaimItem]:
        """
        Calculates true banking clean-up efficiency vs. balance sheet write-offs.
        """
        total_resolved = write_offs_usd_b + cash_recoveries_usd_b
        recovery_efficiency = round(cash_recoveries_usd_b / total_resolved, 2) if total_resolved > 0 else 0.0
        taxpayer_subsidy_ratio = round(recap_subsidy_usd_b / max(cash_recoveries_usd_b, 1.0), 2)

        metrics = {
            "write_offs_usd_b": write_offs_usd_b,
            "cash_recoveries_usd_b": cash_recoveries_usd_b,
            "recap_subsidy_usd_b": recap_subsidy_usd_b,
            "recovery_efficiency_ratio": recovery_efficiency,
            "taxpayer_subsidy_ratio": taxpayer_subsidy_ratio,
            "resolution_mode": "WRITE_OFF_DOMINANT" if recovery_efficiency < 0.40 else "RECOVERY_DOMINANT"
        }

        fact_text = (
            f"Banking sector asset resolution audit: Bad loans resolved via ${write_offs_usd_b:.1f}B in balance-sheet write-offs "
            f"vs. ${cash_recoveries_usd_b:.1f}B in cash recovery (efficiency ratio: {recovery_efficiency * 100:.0f}%), "
            f"subsidized by ${recap_subsidy_usd_b:.1f}B in taxpayer-funded bank recapitalization."
        )

        claim = ClaimItem(
            claim_id=f"CLM-MACRO-NPA-{int(recovery_efficiency * 100)}",
            source_evidence_id="SRC-RBI-DBIE-NPA",
            claim_type=ClaimType.FINANCIAL_CAPEX,
            epistemic_tier=EpistemicTier.TIER_2_FINANCIAL,
            actors=["India"],
            asserted_fact=fact_text,
            target_lenses=["CashFlowLens", "GeoEconomistLens"],
            metrics=metrics,
            reliability_weight=0.98,
            evidence_status="sufficient"
        )

        return metrics, claim

    @classmethod
    def compute_debt_servicing_ratio(
        cls,
        interest_payments_inr_lakh_cr: float,
        net_tax_revenue_inr_lakh_cr: float
    ) -> Tuple[Dict[str, Any], ClaimItem]:
        """
        Calculates sovereign debt servicing burden as a percentage of net tax revenue.
        Models the Kautilyan Kosha-Mula-Danda fiscal ceiling.
        """
        debt_servicing_ratio_pct = round((interest_payments_inr_lakh_cr / net_tax_revenue_inr_lakh_cr) * 100.0, 2) if net_tax_revenue_inr_lakh_cr > 0 else 0.0
        fiscal_space_risk = "HIGH" if debt_servicing_ratio_pct >= 40.0 else ("MODERATE" if debt_servicing_ratio_pct >= 25.0 else "LOW")

        metrics = {
            "interest_payments_inr_lakh_cr": interest_payments_inr_lakh_cr,
            "net_tax_revenue_inr_lakh_cr": net_tax_revenue_inr_lakh_cr,
            "debt_servicing_ratio_pct": debt_servicing_ratio_pct,
            "fiscal_space_risk": fiscal_space_risk
        }

        fact_text = (
            f"Sovereign fiscal space constraint (Kosha-Mula-Danda): Annual debt interest payments (₹{interest_payments_inr_lakh_cr:.2f}L Cr) "
            f"consume {debt_servicing_ratio_pct:.1f}% of net tax revenue (₹{net_tax_revenue_inr_lakh_cr:.2f}L Cr), "
            f"constraining discretionary capital expenditure for defense modernization."
        )

        claim = ClaimItem(
            claim_id=f"CLM-MACRO-DEBT-{int(debt_servicing_ratio_pct)}",
            source_evidence_id="SRC-CGA-UNION-ACCOUNTS",
            claim_type=ClaimType.GENERAL_INTEL,
            epistemic_tier=EpistemicTier.TIER_2_FINANCIAL,
            actors=["India"],
            asserted_fact=fact_text,
            target_lenses=["CivilizationalLens", "GeoEconomistLens", "MilitaryReadinessLens"],
            metrics=metrics,
            reliability_weight=0.99,
            evidence_status="sufficient"
        )

        return metrics, claim
