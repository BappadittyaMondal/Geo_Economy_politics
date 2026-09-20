# LENS SPECIFICATION: CASH_FLOW

```python
"""
Lens 7: Cash Flow & Investment Optics Lens.
Applies strict corporate finance and forensic accounting filters to summit announcements:
The 85% Haircut Rule on unfinanced MOUs, Sovereign Wealth Fund (SWF) deployment realities,
and secondary sanctions capital discount.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, FinancialFlow, LensEvaluation, SummitEvent


class CashFlowLens:
    """Forensic financial auditor for multilateral investment commitments."""

    LENS_NAME = "Cash Flow Realism & Investment Forensics"
    PRIMARY_TIER = EpistemicTier.TIER_2_FINANCIAL

    @classmethod
    def evaluate(
        cls,
        summit: SummitEvent,
        flows: Optional[List[FinancialFlow]] = None,
        claims: Optional[List[Any]] = None,
        fixture_mode: bool = True
    ) -> LensEvaluation:
        """
        Filters announced nominal investment headline figures through effective CapEx haircuts.
        Enforces mathematical clamping gate bounding alignment to verifiable capital deployment.
        """
        if not flows and claims is not None:
            dynamic_flows = []
            for c in claims:
                val = getattr(c, "extracted_financial_mou_usd", None)
                if val is not None and val > 0:
                    actors = getattr(c, "actors", ["Global"])
                    dynamic_flows.append(FinancialFlow(
                        source_country=actors[0] if actors else "Multilateral",
                        target_country=actors[1] if len(actors) > 1 else "India",
                        project_name=getattr(c, "asserted_fact", "Extracted CapEx Project")[:60],
                        nominal_mou_usd=val,
                        is_binding_contract=getattr(c, "is_binding_commitment", False),
                        secondary_sanctions_risk_score=0.20
                    ))
            flows = dynamic_flows

        if not flows and claims is None and fixture_mode:
            flows = [
                FinancialFlow(
                    source_country="China",
                    target_country="Multilateral (BRICS)",
                    project_name="Green Energy & Industrial Transition Fund",
                    nominal_mou_usd=50_000_000_000.0, # $50 Billion headline
                    is_binding_contract=False,
                    clearing_currency="Yuan",
                    vostro_nostro_operational=True,
                    secondary_sanctions_risk_score=0.10
                ),
                FinancialFlow(
                    source_country="Russia",
                    target_country="India",
                    project_name="Hydrocarbon & Petro-Refining Long-Term Settlement",
                    nominal_mou_usd=25_000_000_000.0,
                    is_binding_contract=True,
                    clearing_currency="Local / INR / Dirham",
                    vostro_nostro_operational=True,
                    secondary_sanctions_risk_score=0.45
                ),
                FinancialFlow(
                    source_country="Gulf Partners (UAE/Saudi)",
                    target_country="India",
                    project_name="High-Tech Infrastructure & Port Logistics Corridors",
                    nominal_mou_usd=15_000_000_000.0,
                    is_binding_contract=True,
                    clearing_currency="USD / Local",
                    vostro_nostro_operational=True,
                    secondary_sanctions_risk_score=0.05
                )
            ]

        if not flows:
            findings = ["Zero empirical financial flows or binding CapEx contracts verified for this event."]
            metrics = {
                "total_nominal_announced_usd": 0.0,
                "total_effective_capex_usd": 0.0,
                "aggregate_haircut_percentage": 0.0,
                "active_vostro_accounts_operational": False,
                "npa_recovery_efficiency_ratio": 0.26,
                "npa_cleanup_taxpayer_subsidy_usd_b": 37.5
            }
            if claims:
                banking_npa_claims = [
                    c for c in claims
                    if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower()
                           for kw in ["npa", "bad loan", "write-off", "recapitalization", "banking clean", "ibc recovery"])
                ]
                if banking_npa_claims:
                    findings.append(
                        "[FORENSIC AUDIT] Banking NPA Resolution vs. Write-Off Reality: Bad loans cleaned up primarily via balance-sheet write-offs ($175B written off vs. ~$45B cash recovered, efficiency ~26%), funded by >$37B in taxpayer bank recapitalization."
                    )
                    metrics["banking_resolution_audit_applied"] = True
                    return LensEvaluation(
                        lens_name=cls.LENS_NAME,
                        alignment_score=0.35,
                        confidence=0.85,
                        primary_epistemic_tier=cls.PRIMARY_TIER,
                        key_findings=findings,
                        hard_metrics=metrics,
                        evidence_status="sufficient"
                    )

            return LensEvaluation(
                lens_name=cls.LENS_NAME,
                alignment_score=0.0,
                confidence=0.0,
                primary_epistemic_tier=EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE,
                key_findings=findings,
                hard_metrics=metrics,
                evidence_status="insufficient"
            )

        total_nominal = sum(f.nominal_mou_usd for f in flows)
        total_effective = sum(f.effective_capex_usd for f in flows)
        haircut_pct = round(((total_nominal - total_effective) / total_nominal) * 100, 1) if total_nominal > 0 else 0.0

        findings = [
            f"Nominal Headline Commitments: ${total_nominal / 1e9:.2f} Billion USD.",
            f"Effective Verified CapEx (Post-Haircut): ${total_effective / 1e9:.2f} Billion USD (Aggregate Haircut: {haircut_pct}%).",
            "The 85% Haircut Rule: Non-binding MOUs lacking explicit sovereign budget lines or escrow facilities discounted by 85%.",
            "Secondary Sanctions Capital Discount: Cross-border Russian-Indian/Iranian pipelines discounted due to OFAC compliance caution among commercial tier-1 banks."
        ]

        metrics = {
            "total_nominal_announced_usd": total_nominal,
            "total_effective_capex_usd": total_effective,
            "aggregate_haircut_percentage": haircut_pct,
            "active_vostro_accounts_operational": all(f.vostro_nostro_operational for f in flows),
            "npa_recovery_efficiency_ratio": 0.26,
            "npa_cleanup_taxpayer_subsidy_usd_b": 37.5
        }

        if claims:
            banking_npa_claims = [
                c for c in claims
                if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower()
                       for kw in ["npa", "bad loan", "write-off", "recapitalization", "banking clean", "ibc recovery"])
            ]
            if banking_npa_claims:
                findings.append(
                    "[FORENSIC AUDIT] Banking NPA Resolution vs. Write-Off Reality: Bad loans cleaned up primarily via balance-sheet write-offs ($175B written off vs. ~$45B cash recovered, efficiency ~26%), funded by >$37B in taxpayer bank recapitalization."
                )
                metrics["banking_resolution_audit_applied"] = True

        # Mathematical Validation Gate: Clamps alignment score to the ratio of effective to nominal CapEx
        capex_ratio = total_effective / max(total_nominal, 1.0)
        clamped_alignment = round(min(1.0, 0.15 + (0.85 * capex_ratio)), 2)

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=clamped_alignment,
            confidence=0.95 if total_nominal > 0 else 0.20,
            primary_epistemic_tier=cls.PRIMARY_TIER if total_nominal > 0 else EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE,
            key_findings=findings,
            hard_metrics=metrics,
            evidence_status="sufficient" if total_nominal > 0 else "insufficient"
        )

```