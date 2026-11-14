# LENS SPECIFICATION: CASH_FLOW

```python
"""
Lens 7: Cash Flow & Investment Optics Lens.
Applies strict corporate finance and forensic accounting filters to summit announcements:
The 85% Haircut Rule on unfinanced MOUs, Sovereign Wealth Fund (SWF) deployment realities,
and secondary sanctions capital discount.
"""

import math
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
                "npa_cleanup_taxpayer_subsidy_usd_b": 37.5,
                "illicit_crime_terror_hawala_index": 0.72,
                "transnational_syndicate_asset_freeze_leverage": 0.68
            }
            # Phase 247: Wire DigitalEnclosureTrapSieve fallback
            det_meta = getattr(summit, "metadata", {}) or {}
            det_params = det_meta.get("digital_enclosure_trap", {}) if isinstance(det_meta, dict) else {}
            _det_res = DigitalEnclosureTrapSieve.calculate_digital_enclosure(
                crypto_capital_flight_ratio=det_params.get("crypto_capital_flight_ratio", 0.50),
                offshore_exchange_opacity=det_params.get("offshore_exchange_opacity", 0.60),
                cbdc_programmability_index=det_params.get("cbdc_programmability_index", 0.65),
                physical_gold_reserve_ratio=det_params.get("physical_gold_reserve_ratio", 0.40)
            )
            metrics["digital_enclosure_trap_score"] = _det_res["digital_enclosure_trap_score"]
            metrics["digital_enclosure_trap_tier"] = _det_res["digital_enclosure_trap_tier"]
            # Phase 258: Wire BullionPaperArbitrageDislocationSieve fallback
            bdr_params = det_meta.get("bullion_dislocation", {}) if isinstance(det_meta, dict) else {}
            _bdr_res = BullionPaperArbitrageDislocationSieve.calculate_bullion_dislocation_risk(
                paper_to_physical_leverage=bdr_params.get("paper_to_physical_leverage", 0.70),
                vault_drain_velocity=bdr_params.get("vault_drain_velocity", 0.60),
                tariff_arbitrage_spread=bdr_params.get("tariff_arbitrage_spread", 0.40),
                sovereign_bullion_repatriation=bdr_params.get("sovereign_bullion_repatriation", 0.80),
            )
            metrics.update(_bdr_res)

            # Phase 268: Wire PreciousMetalSovereignArbitrageSieve
            pms_params = det_meta.get("precious_metal_arbitrage", {}) if isinstance(det_meta, dict) else {}
            _pms_res = PreciousMetalSovereignArbitrageSieve.calculate_bullion_sovereignty(
                physical_vault_inventory=pms_params.get("physical_vault_inventory", 0.60),
                paper_derivative_claims=pms_params.get("paper_derivative_claims", 0.50),
                sge_comex_premium_usd=pms_params.get("sge_comex_premium_usd", 25.0),
                central_bank_repatriation_rate=pms_params.get("central_bank_repatriation_rate", 0.70),
                household_streedhan_buffer=pms_params.get("household_streedhan_buffer", 0.85),
            )
            metrics.update(_pms_res)
    
            # Phase 272: Wire SovereignBalanceSheetShieldSieve
            bop_params = det_meta.get("sovereign_bop_shield", {}) if isinstance(det_meta, dict) else {}
            _bop_res = SovereignBalanceSheetShieldSieve.calculate_bop_shield(
                forex_reserves_usd_b=bop_params.get("forex_reserves_usd_b", 700.0),
                short_term_external_debt_usd_b=bop_params.get("short_term_external_debt_usd_b", 140.0),
                dii_retail_absorption_rate=bop_params.get("dii_retail_absorption_rate", 0.80),
                cad_pressure_index=bop_params.get("cad_pressure_index", 0.40),
                fii_flight_velocity=bop_params.get("fii_flight_velocity", 0.50),
            )
            metrics.update(_bop_res)
            # Phase 275 & 276: Wire DomesticHNWICapitalFormationSieve & SovereignGoldRepatriationSieve
            hnwi_params = det_meta.get("hnwi_capital", {}) if isinstance(det_meta, dict) else {}
            _hnwi_res = DomesticHNWICapitalFormationSieve.calculate_capital_flight_risk(
                hnwi_cohort_growth_rate=hnwi_params.get("hnwi_cohort_growth_rate", 0.12),
                gift_city_onshoring_ratio=hnwi_params.get("gift_city_onshoring_ratio", 0.65),
                confiscation_rhetoric_intensity=hnwi_params.get("confiscation_rhetoric_intensity", 0.35),
                tax_unpredictability_index=hnwi_params.get("tax_unpredictability_index", 0.40),
            )
            metrics.update(_hnwi_res)
    
            gold_params = det_meta.get("gold_reserves", {}) if isinstance(det_meta, dict) else {}
            _gold_res = SovereignGoldRepatriationSieve.calculate_reserve_immunity(
                domestic_physical_gold_tonnes=gold_params.get("domestic_physical_gold_tonnes", 500.0),
                total_sovereign_gold_tonnes=gold_params.get("total_sovereign_gold_tonnes", 850.0),
                local_currency_settlement_pct=gold_params.get("local_currency_settlement_pct", 0.25),
                g7_custody_exposure_pct=gold_params.get("g7_custody_exposure_pct", 0.40),
            )
            metrics.update(_gold_res)

            # Phase 286: Wire CommercialBankAssetQualityAndCRARSieve
            bank_params = det_meta.get("bank_asset_quality", {}) if isinstance(det_meta, dict) else {}
            _bank_res = CommercialBankAssetQualityAndCRARSieve.calculate_banking_fortress(
                crar_ratio=bank_params.get("crar_ratio", 0.80),
                provision_coverage=bank_params.get("provision_coverage", 0.75),
                net_npa_ratio=bank_params.get("net_npa_ratio", 0.15),
                mtm_treasury_exposure=bank_params.get("mtm_treasury_exposure", 0.20),
            )
            metrics.update(_bank_res)
    
            if claims:
                banking_npa_claims = [
                    c for c in claims
                    if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower()
                           for kw in ["npa", "bad loan", "write-off", "recapitalization", "banking clean", "ibc recovery"])
                ]
                hawala_claims = [
                    c for c in claims
                    if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower()
                           for kw in ["hawala", "d-company", "drone drop", "illicit finance", "crime-terror", "syndicate", "asset freeze"])
                ]
                if banking_npa_claims or hawala_claims:
                    if banking_npa_claims:
                        findings.append(
                            "[FORENSIC AUDIT] Banking NPA Resolution vs. Write-Off Reality: Bad loans cleaned up primarily via balance-sheet write-offs ($175B written off vs. ~$45B cash recovered, efficiency ~26%), funded by >$37B in taxpayer bank recapitalization."
                        )
                        metrics["banking_resolution_audit_applied"] = True
                    if hawala_claims:
                        findings.append(
                            "[FORENSIC HAWALA AUDIT] Transnational Crime-Terror Hawala Nexus: Disrupted grey-market capital conduits funding cross-border drone payloads and hostile proxy logistics; leveraged bilateral UAE/Saudi extradition and asset-freeze treaties to restrict syndicate liquidity."
                        )
                        metrics["hawala_nexus_disrupted"] = True
                        metrics["illicit_crime_terror_hawala_index"] = 0.88
                        metrics["transnational_syndicate_asset_freeze_leverage"] = 0.85
                    return LensEvaluation(
                        lens_name=cls.LENS_NAME,
                        alignment_score=0.45 if (banking_npa_claims and hawala_claims) else (0.35 if banking_npa_claims else 0.40),
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
            "npa_cleanup_taxpayer_subsidy_usd_b": 37.5,
            "illicit_crime_terror_hawala_index": 0.72,
            "transnational_syndicate_asset_freeze_leverage": 0.68
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

            hawala_claims = [
                c for c in claims
                if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower()
                       for kw in ["hawala", "d-company", "drone drop", "illicit finance", "crime-terror", "syndicate", "asset freeze"])
            ]
            if hawala_claims:
                findings.append(
                    "[FORENSIC HAWALA AUDIT] Transnational Crime-Terror Hawala Nexus: Disrupted grey-market capital conduits funding cross-border drone payloads and hostile proxy logistics; leveraged bilateral UAE/Saudi extradition and asset-freeze treaties to restrict syndicate liquidity."
                )
                metrics["hawala_nexus_disrupted"] = True
                metrics["illicit_crime_terror_hawala_index"] = 0.88
                metrics["transnational_syndicate_asset_freeze_leverage"] = 0.85

        # Mathematical Validation Gate: Clamps alignment score to the ratio of effective to nominal CapEx
        capex_ratio = total_effective / max(total_nominal, 1.0)
        clamped_alignment = round(min(1.0, 0.15 + (0.85 * capex_ratio)), 2)

        # Quantitative consolidated public capex model baseline (Union: ₹11.11L Cr, States: ₹8.5L Cr, IEBR: ₹3.5L Cr, Transfers: ₹1.5L Cr)
        capex_calc = cls.calculate_consolidated_public_capex(
            union_budget_capex=11.11,
            state_capex=8.50,
            cpse_iebr=3.50,
            intergovernmental_transfers=1.50
        )
        metrics["consolidated_capex_model"] = capex_calc
        metrics["consolidated_public_capex_usd_or_inr_trillion"] = capex_calc["consolidated_public_capex"]

        # Phase 247: Wire DigitalEnclosureTrapSieve
        det_meta = getattr(summit, "metadata", {}) or {}
        det_params = det_meta.get("digital_enclosure_trap", {}) if isinstance(det_meta, dict) else {}
        _det_res = DigitalEnclosureTrapSieve.calculate_digital_enclosure(
            crypto_capital_flight_ratio=det_params.get("crypto_capital_flight_ratio", 0.50),
            offshore_exchange_opacity=det_params.get("offshore_exchange_opacity", 0.60),
            cbdc_programmability_index=det_params.get("cbdc_programmability_index", 0.65),
            physical_gold_reserve_ratio=det_params.get("physical_gold_reserve_ratio", 0.40)
        )
        metrics["digital_enclosure_trap_score"] = _det_res["digital_enclosure_trap_score"]
        metrics["digital_enclosure_trap_tier"] = _det_res["digital_enclosure_trap_tier"]
        # Phase 258: Wire BullionPaperArbitrageDislocationSieve
        bdr_params = det_meta.get("bullion_dislocation", {}) if isinstance(det_meta, dict) else {}
        _bdr_res = BullionPaperArbitrageDislocationSieve.calculate_bullion_dislocation_risk(
            paper_to_physical_leverage=bdr_params.get("paper_to_physical_leverage", 0.70),
            vault_drain_velocity=bdr_params.get("vault_drain_velocity", 0.60),
            tariff_arbitrage_spread=bdr_params.get("tariff_arbitrage_spread", 0.40),
            sovereign_bullion_repatriation=bdr_params.get("sovereign_bullion_repatriation", 0.80),
        )
        metrics.update(_bdr_res)

        # Phase 268: Wire PreciousMetalSovereignArbitrageSieve
        pms_params = det_meta.get("precious_metal_arbitrage", {}) if isinstance(det_meta, dict) else {}
        _pms_res = PreciousMetalSovereignArbitrageSieve.calculate_bullion_sovereignty(
            physical_vault_inventory=pms_params.get("physical_vault_inventory", 0.60),
            paper_derivative_claims=pms_params.get("paper_derivative_claims", 0.50),
            sge_comex_premium_usd=pms_params.get("sge_comex_premium_usd", 25.0),
            central_bank_repatriation_rate=pms_params.get("central_bank_repatriation_rate", 0.70),
            household_streedhan_buffer=pms_params.get("household_streedhan_buffer", 0.85),
        )
        metrics.update(_pms_res)

        # Phase 272: Wire SovereignBalanceSheetShieldSieve
        bop_params = det_meta.get("sovereign_bop_shield", {}) if isinstance(det_meta, dict) else {}
        _bop_res = SovereignBalanceSheetShieldSieve.calculate_bop_shield(
            forex_reserves_usd_b=bop_params.get("forex_reserves_usd_b", 700.0),
            short_term_external_debt_usd_b=bop_params.get("short_term_external_debt_usd_b", 140.0),
            dii_retail_absorption_rate=bop_params.get("dii_retail_absorption_rate", 0.80),
            cad_pressure_index=bop_params.get("cad_pressure_index", 0.40),
            fii_flight_velocity=bop_params.get("fii_flight_velocity", 0.50),
        )
        metrics.update(_bop_res)
        # Phase 275 & 276: Wire DomesticHNWICapitalFormationSieve & SovereignGoldRepatriationSieve
        hnwi_params = det_meta.get("hnwi_capital", {}) if isinstance(det_meta, dict) else {}
        _hnwi_res = DomesticHNWICapitalFormationSieve.calculate_capital_flight_risk(
            hnwi_cohort_growth_rate=hnwi_params.get("hnwi_cohort_growth_rate", 0.12),
            gift_city_onshoring_ratio=hnwi_params.get("gift_city_onshoring_ratio", 0.65),
            confiscation_rhetoric_intensity=hnwi_params.get("confiscation_rhetoric_intensity", 0.35),
            tax_unpredictability_index=hnwi_params.get("tax_unpredictability_index", 0.40),
        )
        metrics.update(_hnwi_res)

        gold_params = det_meta.get("gold_reserves", {}) if isinstance(det_meta, dict) else {}
        _gold_res = SovereignGoldRepatriationSieve.calculate_reserve_immunity(
            domestic_physical_gold_tonnes=gold_params.get("domestic_physical_gold_tonnes", 500.0),
            total_sovereign_gold_tonnes=gold_params.get("total_sovereign_gold_tonnes", 850.0),
            local_currency_settlement_pct=gold_params.get("local_currency_settlement_pct", 0.25),
            g7_custody_exposure_pct=gold_params.get("g7_custody_exposure_pct", 0.40),
        )
        metrics.update(_gold_res)

        # Phase 286: Wire CommercialBankAssetQualityAndCRARSieve
        bank_params = det_meta.get("bank_asset_quality", {}) if isinstance(det_meta, dict) else {}
        _bank_res = CommercialBankAssetQualityAndCRARSieve.calculate_banking_fortress(
            crar_ratio=bank_params.get("crar_ratio", 0.80),
            provision_coverage=bank_params.get("provision_coverage", 0.75),
            net_npa_ratio=bank_params.get("net_npa_ratio", 0.15),
            mtm_treasury_exposure=bank_params.get("mtm_treasury_exposure", 0.20),
        )
        metrics.update(_bank_res)

        # Phase 316: Wire ImperialDebtOverreachSieve
        debt_params = det_meta.get("imperial_debt_overreach", {}) if isinstance(det_meta, dict) else {}
        _debt_res = ImperialDebtOverreachSieve.calculate(
            debt_service_annual=debt_params.get("debt_service_annual", 0.85),
            annual_defense_budget=debt_params.get("annual_defense_budget", 0.35),
            public_debt_to_gdp=debt_params.get("public_debt_to_gdp", 0.80),
            fiscal_revenue_headroom=debt_params.get("fiscal_revenue_headroom", 0.20),
        )
        metrics["imperial_debt_overreach_score"] = _debt_res["imperial_debt_overreach_score"]

        # Phases 318, 330, 334, 336: Basel Gold, Bullion Trade, Eurodollar, Sovereign Gold Velocity
        bg_params = det_meta.get("basel_gold", {}) if isinstance(det_meta, dict) else {}
        _bg_res = BaselGoldAllocationSieve.calculate(
            physical_bullion=bg_params.get("physical_bullion", 0.85),
            paper_derivatives=bg_params.get("paper_derivatives", 0.35),
            domestic_vault_immunity=bg_params.get("domestic_vault_immunity", 0.90),
            fx_sanctions_vulnerability=bg_params.get("fx_sanctions_vulnerability", 0.20),
        )
        metrics["basel_gold_allocation_score"] = _bg_res["basel_gold_allocation_score"]

        cb_params = det_meta.get("classical_bullion_trade", {}) if isinstance(det_meta, dict) else {}
        _cb_res = ClassicalBullionInflowTradeSieve.calculate(
            export_surplus_bullion_settlement=cb_params.get("export_surplus_bullion_settlement", 0.80),
            domestic_vault_repatriation=cb_params.get("domestic_vault_repatriation", 0.85),
            fiat_debt_dependency=cb_params.get("fiat_debt_dependency", 0.25),
        )
        metrics["classical_bullion_inflow_score"] = _cb_res["classical_bullion_inflow_score"]

        ed_params = det_meta.get("eurodollar_liquidity", {}) if isinstance(det_meta, dict) else {}
        _ed_res = EurodollarShadowLiquiditySieve.calculate(
            eurodollar_liquidity_drain=ed_params.get("eurodollar_liquidity_drain", 0.75),
            cross_currency_basis_spread=ed_params.get("cross_currency_basis_spread", 0.70),
            domestic_fx_reserve_cushion=ed_params.get("domestic_fx_reserve_cushion", 0.85),
        )
        metrics["eurodollar_shadow_liquidity_score"] = _ed_res["eurodollar_shadow_liquidity_score"]

        gv_params = det_meta.get("gold_repatriation_velocity", {}) if isinstance(det_meta, dict) else {}
        _gv_res = SovereignGoldRepatriationVelocitySieve.calculate(
            repatriated_bullion_metric=gv_params.get("repatriated_bullion_metric", 102.0),
            foreign_custody_gold=gv_params.get("foreign_custody_gold", 350.0),
            domestic_vault_security=gv_params.get("domestic_vault_security", 0.90),
            fx_sanction_exposure=gv_params.get("fx_sanction_exposure", 0.20),
        )
        metrics["sovereign_gold_repatriation_velocity_score"] = _gv_res["sovereign_gold_repatriation_velocity_score"]
        metrics["imperial_debt_overreach_tier"] = _debt_res["imperial_debt_overreach_tier"]
        metrics["fiscal_basing_retrenchment_index"] = _debt_res["fiscal_basing_retrenchment_index"]

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=clamped_alignment,
            confidence=0.95 if total_nominal > 0 else 0.20,
            primary_epistemic_tier=cls.PRIMARY_TIER if total_nominal > 0 else EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE,
            key_findings=findings,
            hard_metrics=metrics,
            evidence_status="sufficient" if total_nominal > 0 else "insufficient"
        )

    @classmethod
    def calculate_consolidated_public_capex(
        cls,
        union_budget_capex: float,
        state_capex: float,
        cpse_iebr: float,
        intergovernmental_transfers: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates consolidated public sector capex and quantifies the IEBR off-budget shift.
        Exposes how moving off-budget PSU borrowing onto the Union balance sheet inflated
        headline budget capex without expanding consolidated public capex at the same rate.
        """
        consolidated_capex = union_budget_capex + state_capex + cpse_iebr - intergovernmental_transfers
        headline_budget_share_pct = (union_budget_capex / consolidated_capex * 100.0) if consolidated_capex > 0 else 0.0
        cpse_iebr_share_pct = (cpse_iebr / consolidated_capex * 100.0) if consolidated_capex > 0 else 0.0

        return {
            "union_budget_capex": round(union_budget_capex, 2),
            "state_capex": round(state_capex, 2),
            "cpse_iebr": round(cpse_iebr, 2),
            "intergovernmental_transfers": round(intergovernmental_transfers, 2),
            "consolidated_public_capex": round(consolidated_capex, 2),
            "union_budget_share_pct": round(headline_budget_share_pct, 2),
            "cpse_iebr_share_pct": round(cpse_iebr_share_pct, 2),
            "iebr_shift_flag": cpse_iebr_share_pct < 20.0,
            "forensic_finding": (
                "While headline Union Budget capex tripled nominally, total public capex "
                "expanded by ~80% because off-budget PSU borrowing (IEBR) was shifted onto the sovereign budget."
            )
        }

    @classmethod
    def calculate_hawala_disruption_leverage(
        cls,
        estimated_illicit_flow_usd_b: float,
        bilateral_asset_treaty_score: float,
        swift_and_crypto_tracing_reach: float
    ) -> Dict[str, Any]:
        """
        Forensically models the squeeze on transnational crime-terror hawala pipelines:
            squeeze_leverage = (bilateral_asset_treaty_score * 1.5 * swift_and_crypto_tracing_reach) / max(0.10, estimated_illicit_flow_usd_b / 5.0)
        """
        flow_b = max(0.01, float(estimated_illicit_flow_usd_b))
        treaty = max(0.0, min(1.0, float(bilateral_asset_treaty_score)))
        tracing = max(0.0, min(1.0, float(swift_and_crypto_tracing_reach)))

        squeeze_ratio = round((treaty * 1.5 * tracing) / max(0.10, flow_b / 5.0), 4)
        liquidity_suppression_pct = min(92.0, max(5.0, round(squeeze_ratio * 45.0, 2)))
        syndicate_risk_tier = "CRITICAL_SQUEEZE" if squeeze_ratio >= 1.20 else ("MODERATE_FRICTION" if squeeze_ratio >= 0.60 else "RESILIENT_HAVEN")

        return {
            "estimated_illicit_flow_usd_b": flow_b,
            "bilateral_asset_treaty_score": treaty,
            "swift_and_crypto_tracing_reach": tracing,
            "hawala_squeeze_ratio": squeeze_ratio,
            "liquidity_suppression_pct": liquidity_suppression_pct,
            "syndicate_risk_tier": syndicate_risk_tier,
            "forensic_verdict": (
                "Syndicate liquidity severely restricted via bilateral extradition/freezing accords (UAE/Gulf hubs)."
                if syndicate_risk_tier == "CRITICAL_SQUEEZE"
                else "Syndicate retains alternative hawala channels; requires deeper financial intelligence coordination."
            )
        }


class DigitalEnclosureTrapSieve:
    """
    Phase 247: Models retail/corporate capital entrapment in non-jurisdictional offshore
    crypto platforms vs. sovereign physical gold accumulation ahead of programmable CBDC resets.
    """

    @classmethod
    def calculate_digital_enclosure(
        cls,
        crypto_capital_flight_ratio: float = 0.50,
        offshore_exchange_opacity: float = 0.60,
        cbdc_programmability_index: float = 0.65,
        physical_gold_reserve_ratio: float = 0.40
    ) -> Dict[str, Any]:
        """
        Calculates the digital enclosure vulnerability using bounded logistic sigmoid:
            z = 2.8*CCFR + 2.4*OEO + 2.2*CPI - 3.0*PGR - 0.8
            score = 1 / (1 + exp(-z))
        """
        ccfr = max(0.0, min(1.0, float(crypto_capital_flight_ratio)))
        oeo = max(0.0, min(1.0, float(offshore_exchange_opacity)))
        cpi = max(0.0, min(1.0, float(cbdc_programmability_index)))
        pgr = max(0.0, min(1.0, float(physical_gold_reserve_ratio)))

        z = 2.8 * ccfr + 2.4 * oeo + 2.2 * cpi - 3.0 * pgr - 0.8
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "CRITICAL_DIGITAL_ENCLOSURE_RISK"
            verdict = "ACUTE_CAPITAL_ENTRAPMENT_IN_UNBACKED_CRYPTO_OR_PROGRAMMABLE_FIAT"
            rationale = (
                f"Critical digital enclosure risk ({score:.4f}): High capital flight to offshore crypto platforms "
                f"({ccfr:.2f}) and exchange opacity ({oeo:.2f}) expose domestic private wealth to sudden liquidation "
                f"without statutory lender-of-last-resort protections."
            )
        elif score >= 0.55:
            tier = "ELEVATED_CUSTODIAL_VULNERABILITY"
            verdict = "MODERATE_OFFSHORE_EXPOSURE_REQUIRING_GOLD_ACCUMULATION"
            rationale = (
                f"Elevated custodial vulnerability ({score:.4f}): Programmable CBDC risk ({cpi:.2f}) outpaces "
                f"physical gold reserve buffers ({pgr:.2f})."
            )
        elif score >= 0.35:
            tier = "MODERATE_EXPOSURE"
            verdict = "BALANCED_SOVEREIGN_RESERVE_DIVERSIFICATION"
            rationale = (
                f"Moderate exposure ({score:.4f}): Physical gold holdings ({pgr:.2f}) provide baseline macroeconomic insulation."
            )
        else:
            tier = "FORTIFIED_PHYSICAL_ASSET_ANCHOR"
            verdict = "SOVEREIGN_BULLION_HEGEMONY_AND_DEBT_INSULATION"
            rationale = (
                f"Fortified physical anchor ({score:.4f}): High gold reserve ratio ({pgr:.2f}) and minimal unbacked crypto flight "
                f"({ccfr:.2f}) shield sovereign balance sheet from digital reset shocks."
            )

        return {
            "digital_enclosure_trap_score": score,
            "crypto_capital_flight_ratio": round(ccfr, 4),
            "offshore_exchange_opacity": round(oeo, 4),
            "cbdc_programmability_index": round(cpi, 4),
            "physical_gold_reserve_ratio": round(pgr, 4),
            "digital_enclosure_trap_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_enclosure_risk_acute": score >= 0.70
        }

class BullionPaperArbitrageDislocationSieve:
    """
    Phase 258: Bullion Paper-Physical Arbitrage Dislocation Sieve.
    Quantifies the decoupling of COMEX/LBMA unallocated paper gold claims (~100:1 leverage)
    from vaulted physical bullion during geopolitical de-dollarization shocks.
    Models vault drain velocity, customs tariff arbitrage (15% to 6% duty spread), and RBI physical bullion repatriation.
    """

    @staticmethod
    def calculate_bullion_dislocation_risk(
        paper_to_physical_leverage: float = 0.7,
        vault_drain_velocity: float = 0.6,
        tariff_arbitrage_spread: float = 0.4,
        sovereign_bullion_repatriation: float = 0.8,
    ) -> Dict[str, Any]:
        ppl = min(1.0, max(0.0, float(paper_to_physical_leverage)))
        vdv = min(1.0, max(0.0, float(vault_drain_velocity)))
        tas = min(1.0, max(0.0, float(tariff_arbitrage_spread)))
        sbr = min(1.0, max(0.0, float(sovereign_bullion_repatriation)))

        z = (2.8 * ppl + 2.5 * vdv + 2.2 * tas - 3.0 * sbr - 0.8)
        risk = 1.0 / (1.0 + math.exp(-z))
        risk = round(min(1.0, max(0.0, risk)), 4)

        if risk >= 0.75:
            tier = "ACUTE_PAPER_BULLION_DISLOCATION_AND_DEFAULT_RISK"
            verdict = "SEVERE_COMEX_LBMA_PHYSICAL_DELIVERY_FAILURE_RISK"
        elif risk >= 0.55:
            tier = "ELEVATED_PHYSICAL_DELIVERY_PREMIUM"
            verdict = "HIGH_PAPER_DECOUPLING_AND_EASTERN_ACCUMULATION"
        elif risk >= 0.35:
            tier = "CONTROLLED_ARBITRAGE_VOLATILITY"
            verdict = "BALANCED_TARIFF_AND_DELIVERY_EQUILIBRIUM"
        else:
            tier = "FORTIFIED_SOVEREIGN_BULLION_ANCHOR"
            verdict = "SECURE_DOMESTIC_PHYSICAL_VAULT_ANCHOR"

        return {
            "bullion_dislocation_risk": risk,
            "bullion_dislocation_tier": tier,
            "bullion_dislocation_verdict": verdict,
            "paper_to_physical_leverage": ppl,
            "vault_drain_velocity": vdv,
            "tariff_arbitrage_spread": tas,
            "sovereign_bullion_repatriation": sbr,
            "is_bullion_dislocated": risk >= 0.55
        }


class PreciousMetalSovereignArbitrageSieve:
    """
    Phase 268: Precious Metal Sovereign Arbitrage Sieve.
    Quantifies sovereign bullion resilience by evaluating physical vs paper vault ratios,
    Shanghai Gold Exchange (SGE) physical delivery premiums over COMEX spot,
    central bank physical repatriation velocity (RBI 100+ tonnes from Bank of England),
    and decentralized household Streedhan gold reserves (~25,000 tonnes macro-buffer).
    """

    @staticmethod
    def calculate_bullion_sovereignty(
        physical_vault_inventory: float = 0.60,
        paper_derivative_claims: float = 0.50,
        sge_comex_premium_usd: float = 25.0,
        central_bank_repatriation_rate: float = 0.70,
        household_streedhan_buffer: float = 0.85,
    ) -> dict:
        import math
        pvi = max(0.0, float(physical_vault_inventory))
        pdc = max(0.0, float(paper_derivative_claims))
        vault_ratio = min(5.0, pvi / (max(0.001, pdc) + 1e-5))

        cbr = min(1.0, max(0.0, float(central_bank_repatriation_rate)))
        hsb = min(1.0, max(0.0, float(household_streedhan_buffer)))
        sge_norm = min(2.0, max(0.0, float(sge_comex_premium_usd) / 25.0))

        z = (2.2 * vault_ratio + 2.5 * cbr + 2.6 * hsb + 1.5 * sge_norm - 1.8)
        score = 1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z))))
        score = round(min(1.0, max(0.0, score)), 4)

        if score >= 0.75:
            tier = "FORTIFIED_PHYSICAL_BULLION_SOVEREIGNTY"
            verdict = "UNASSAILABLE_PHYSICAL_VAULT_AND_STREEDHAN_ANCHOR"
        elif score >= 0.55:
            tier = "ADEQUATE_CENTRAL_BANK_GOLD_BACKING"
            verdict = "SUBSTANTIAL_REPATRIATION_AND_RESERVE_STABILITY"
        elif score >= 0.35:
            tier = "VULNERABLE_PAPER_DERIVATIVE_EXPOSURE"
            verdict = "MODERATE_EXPOSURE_TO_WESTERN_SYNTHETIC_PAPER_SHOCKS"
        else:
            tier = "CRITICAL_FIAT_DEBASEMENT_VULNERABILITY"
            verdict = "SEVERE_UNBACKED_FIAT_AND_CUSTODIAL_FREEZE_RISK"

        return {
            "bullion_sovereignty_score": score,
            "vault_physical_to_paper_ratio": round(vault_ratio, 4),
            "streedhan_macro_buffer_index": round(hsb, 4),
            "central_bank_repatriation_rate": round(cbr, 4),
            "sge_comex_arbitrage_premium_usd": round(float(sge_comex_premium_usd), 2),
            "bullion_sovereignty_tier": tier,
            "bullion_sovereignty_verdict": verdict,
            "is_bullion_sovereign": score >= 0.55
        }


class SovereignBalanceSheetShieldSieve:
    """
    Phase 272: Sovereign Balance Sheet Shield Sieve.
    Quantifies macro balance-of-payments immunity under the Greenspan-Guidotti rule:
    ratio of foreign exchange reserves to short-term external debt maturing within 1 year,
    and domestic institutional investor (DII) retail SIP inflow velocity neutralizing
    foreign institutional investor (FII) equity flight during global liquidity freezes.
    """

    @staticmethod
    def calculate_bop_shield(
        forex_reserves_usd_b: float = 700.0,
        short_term_external_debt_usd_b: float = 140.0,
        dii_retail_absorption_rate: float = 0.80,
        cad_pressure_index: float = 0.40,
        fii_flight_velocity: float = 0.50,
    ) -> dict:
        import math
        fx = max(0.0, float(forex_reserves_usd_b))
        std = max(0.0, float(short_term_external_debt_usd_b))
        cover_ratio = min(5.0, fx / (max(0.001, std) + 1e-5))

        dii = min(1.0, max(0.0, float(dii_retail_absorption_rate)))
        cad = min(1.0, max(0.0, float(cad_pressure_index)))
        fii = min(1.0, max(0.0, float(fii_flight_velocity)))

        z = (2.5 * cover_ratio + 2.8 * dii - 2.4 * cad - 2.2 * fii - 1.5)
        score = 1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z))))
        score = round(min(1.0, max(0.0, score)), 4)

        if score >= 0.75:
            tier = "FORTIFIED_SOVEREIGN_BOP_SHIELD"
            verdict = "ROBUST_IMPORT_COVER_AND_RETAIL_DII_INSULATION"
        elif score >= 0.55:
            tier = "ADEQUATE_DOMESTIC_CAPITAL_ABSORPTION"
            verdict = "STABLE_LIQUIDITY_BUFFER_AGAINST_FII_OUTFLOWS"
        elif score >= 0.35:
            tier = "CONTESTED_EXTERNAL_LIQUIDITY_PRESSURE"
            verdict = "ELEVATED_CURRENT_ACCOUNT_DEFICIT_SQUEEZE"
        else:
            tier = "ACUTE_BALANCE_OF_PAYMENTS_VULNERABILITY"
            verdict = "CRITICAL_EXTERNAL_DEBT_ROLLOVER_AND_LIQUIDITY_RISK"

        return {
            "sovereign_bop_shield_score": score,
            "forex_to_short_term_debt_ratio": round(cover_ratio, 4),
            "dii_capital_flight_insulation": round(dii, 4),
            "cad_pressure_index": round(cad, 4),
            "fii_flight_velocity": round(fii, 4),
            "bop_shield_tier": tier,
            "bop_shield_verdict": verdict,
            "is_bop_shield_resilient": score >= 0.55
        }


class DomesticHNWICapitalFormationSieve:
    """
    Phase 275: Domestic HNWI Capital Formation & Tax Wealth Sieve.
    Quantifies the balance between expanding domestic risk capital cohorts (₹8.5 Cr+ wealth)
    and capital flight incentives driven by populist wealth-confiscation / inheritance tax rhetoric,
    arbitraged against IFSC GIFT City onshoring incentives.
    """

    @staticmethod
    def calculate_capital_flight_risk(
        hnwi_cohort_growth_rate: float = 0.12,
        gift_city_onshoring_ratio: float = 0.65,
        confiscation_rhetoric_intensity: float = 0.35,
        tax_unpredictability_index: float = 0.40,
    ) -> dict:
        import math
        hnwi = max(0.0, float(hnwi_cohort_growth_rate))
        gift = min(1.0, max(0.0, float(gift_city_onshoring_ratio)))
        conf = min(1.0, max(0.0, float(confiscation_rhetoric_intensity)))
        tax = min(1.0, max(0.0, float(tax_unpredictability_index)))

        z = (2.4 * conf + 2.2 * tax - 2.6 * gift - 2.0 * min(1.0, hnwi) - 0.4)
        flight_risk = 1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z))))
        flight_risk = round(min(1.0, max(0.0, flight_risk)), 4)
        retention = round(1.0 - flight_risk, 4)

        if flight_risk >= 0.75:
            tier = "ACUTE_HNWI_CAPITAL_FLIGHT_RISK"
            verdict = "HEAVY_OUTFLOW_TO_DUBAI_AND_SINGAPORE_TAX_HAVENS"
        elif flight_risk >= 0.55:
            tier = "ELEVATED_DOMESTIC_CAPITAL_EROSION"
            verdict = "WEALTH_RETENTION_PRESSURED_BY_POPULIST_RHETORIC"
        elif flight_risk >= 0.35:
            tier = "STABLE_DOMESTIC_WEALTH_FORMATION"
            verdict = "BALANCED_CAPITAL_EXPANSION_WITH_GIFT_CITY_ABSORPTION"
        else:
            tier = "FORTIFIED_SOVEREIGN_CAPITAL_MAGNET"
            verdict = "ROBUST_DOMESTIC_RISK_CAPITAL_ACCUMULATION_AND_ONSHORING"

        return {
            "capital_flight_risk_score": flight_risk,
            "capital_retention_score": retention,
            "hnwi_cohort_growth_rate": round(hnwi, 4),
            "gift_city_onshoring_ratio": round(gift, 4),
            "confiscation_rhetoric_intensity": round(conf, 4),
            "tax_unpredictability_index": round(tax, 4),
            "capital_formation_tier": tier,
            "capital_formation_verdict": verdict,
            "is_capital_flight_critical": flight_risk >= 0.55,
        }


class SovereignGoldRepatriationSieve:
    """
    Phase 276: Sovereign Gold Repatriation & Fiat Counterparty Default Sieve.
    Measures sovereign bullion immunity against foreign custodial freezes (e.g., Bank of England, G7 sanctions)
    based on the ratio of physical gold repatriated to domestic vaults plus local currency bilateral trade settlement pacts.
    """

    @staticmethod
    def calculate_reserve_immunity(
        domestic_physical_gold_tonnes: float = 500.0,
        total_sovereign_gold_tonnes: float = 850.0,
        local_currency_settlement_pct: float = 0.25,
        g7_custody_exposure_pct: float = 0.40,
    ) -> dict:
        import math
        dom = max(0.0, float(domestic_physical_gold_tonnes))
        tot = max(1.0, float(total_sovereign_gold_tonnes))
        repat_ratio = min(1.0, dom / tot)
        local_curr = min(1.0, max(0.0, float(local_currency_settlement_pct)))
        g7_exp = min(1.0, max(0.0, float(g7_custody_exposure_pct)))

        z = (3.0 * repat_ratio + 2.2 * local_curr - 2.8 * g7_exp - 0.2)
        score = 1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z))))
        score = round(min(1.0, max(0.0, score)), 4)

        if score >= 0.75:
            tier = "FORTIFIED_SOVEREIGN_BULLION_IMMUNITY"
            verdict = "MINIMAL_COUNTERPARTY_RISK_DOMESTIC_VAULT_DOMINANCE"
        elif score >= 0.55:
            tier = "RESILIENT_REPATRIATED_RESERVES"
            verdict = "ADEQUATE_SWIFT_DISCONNECTION_AND_SANCTION_BUFFER"
        elif score >= 0.35:
            tier = "MODERATE_CUSTODIAL_DEPENDENCE"
            verdict = "VULNERABLE_TO_G7_ASSET_FREEZE_AND_THIRD_PARTY_DEFAULT"
        else:
            tier = "HIGH_EXTERNAL_RESERVE_PERIL"
            verdict = "CRITICAL_EXPOSURE_TO_FOREIGN_JURISDICTION_SEIZURE"

        return {
            "reserve_immunity_score": score,
            "gold_repatriation_ratio": round(repat_ratio, 4),
            "domestic_gold_tonnes": round(dom, 2),
            "total_gold_tonnes": round(tot, 2),
            "local_currency_settlement_pct": round(local_curr, 4),
            "g7_custody_exposure_pct": round(g7_exp, 4),
            "bullion_immunity_tier": tier,
            "bullion_immunity_verdict": verdict,
            "is_reserve_immunity_secure": score >= 0.55,
        }


class CommercialBankAssetQualityAndCRARSieve:
    """
    Phase 286: Commercial Bank Asset Quality & CRAR Sieve.
    Quantifies sovereign commercial bank balance sheet fortress: Capital to Risk-Weighted Assets Ratios (CRAR > 16.5%),
    Net Non-Performing Asset (NNPA) ratios, Provision Coverage Ratios (PCR), and insulation from Western mark-to-market bond losses.
    """

    @classmethod
    def calculate_banking_fortress(
        cls,
        crar_ratio: float = 0.80,
        provision_coverage: float = 0.75,
        net_npa_ratio: float = 0.15,
        mtm_treasury_exposure: float = 0.20,
    ) -> Dict[str, Any]:
        """
        Calculates Banking Fortress Score using calibrated logistic sigmoid:
            z = 2.8 * crar + 2.5 * provision - 3.2 * npa - 2.6 * mtm - 0.2
            score = 1 / (1 + exp(-z))
        """
        import math
        crar = max(0.0, min(1.0, float(crar_ratio)))
        pcr = max(0.0, min(1.0, float(provision_coverage)))
        npa = max(0.0, min(1.0, float(net_npa_ratio)))
        mtm = max(0.0, min(1.0, float(mtm_treasury_exposure)))

        z = 2.8 * crar + 2.5 * pcr - 3.2 * npa - 2.6 * mtm - 0.2
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "FORTIFIED_SOVEREIGN_BANKING_FORTRESS"
            verdict = "PRISTINE_BANK_BALANCE_SHEETS_INSULATED_FROM_WESTERN_RUNS"
            rationale = (
                f"Fortified banking fortress ({score:.4f}): Robust CRAR adequacy ({crar:.2f}) and high provision coverage ({pcr:.2f}) "
                f"with minimal NNPA ({npa:.2f}) fully insulate banking system from SVB-style duration and liquidity shocks."
            )
        elif score >= 0.55:
            tier = "SOUND_DOMESTIC_BALANCE_SHEET"
            verdict = "RESILIENT_DOMESTIC_CREDIT_CAPACITY"
            rationale = (
                f"Sound balance sheet ({score:.4f}): Healthy capitalization buffers absorb localized stress without systemic impairment."
            )
        elif score >= 0.35:
            tier = "ELEVATED_DURATION_MISMATCH_EXPOSURE"
            verdict = "TREASURY_MTM_VULNERABILITY_ACCELERATING"
            rationale = (
                f"Elevated duration mismatch ({score:.4f}): Higher bond yield volatility ({mtm:.2f}) exerts drag on bank net worth."
            )
        else:
            tier = "CRITICAL_BANKING_LIQUIDITY_RUN_RISK"
            verdict = "SYSTEMIC_INSOLVENCY_AND_NON_PERFORMING_SPIRAL"
            rationale = (
                f"Critical liquidity risk ({score:.4f}): High bad loan ratios ({npa:.2f}) and unhedged Treasury losses threaten solvency."
            )

        npa_cushion = round(max(0.0, pcr - npa), 4)

        return {
            "banking_fortress_score": score,
            "crar_ratio": round(crar, 4),
            "provision_coverage": round(pcr, 4),
            "net_npa_ratio": round(npa, 4),
            "mtm_treasury_exposure": round(mtm, 4),
            "crar_capital_adequacy_index": round(crar, 4),
            "non_performing_asset_cushion": npa_cushion,
            "banking_resilience_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_banking_resilient": score >= 0.55,
        }


class ImperialDebtOverreachSieve:
    """
    Phase 316: Evaluates the fiscal sustainability of global military basing and power projection,
    modeling debt-service crowding-out of defense budgets and inevitable force retrenchment.
    
    Mathematical Formulation:
      ratio = debt_service_annual / (annual_defense_budget + eps)
      z = 3.0 * (ratio / 2.5) + 2.5 * public_debt_to_gdp - 3.2 * fiscal_revenue_headroom - 0.3
      S_Imperial_Debt_Overreach = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        debt_service_annual: float = 0.85,
        annual_defense_budget: float = 0.35,
        public_debt_to_gdp: float = 0.80,
        fiscal_revenue_headroom: float = 0.20,
    ) -> Dict[str, Any]:
        service = max(0.0, min(1.0, float(debt_service_annual)))
        defense = max(0.0, min(1.0, float(annual_defense_budget)))
        debt_gdp = max(0.0, min(1.0, float(public_debt_to_gdp)))
        headroom = max(0.0, min(1.0, float(fiscal_revenue_headroom)))

        ratio = min(5.0, service / (defense + 1e-6))
        z = 3.0 * (ratio / 2.5) + 2.5 * debt_gdp - 3.2 * headroom - 0.3
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "TERMINAL_FISCAL_RETRENCHMENT_IMMINENT"
            verdict = "INEVITABLE_GLOBAL_BASING_WITHDRAWAL"
            rationale = (
                f"Terminal fiscal retrenchment ({score:.4f}): Debt service ({service:.2f}) completely crowds out the defense "
                f"budget ({defense:.2f}) under elevated debt-to-GDP ({debt_gdp:.2f}), making overseas bases financially unviable."
            )
        elif score >= 0.55:
            tier = "ELEVATED_BASING_AUSTERITY_PRESSURE"
            verdict = "FORCE_STRUCTURE_DOWNSIZING"
            rationale = (
                f"Elevated austerity ({score:.4f}): Fiscal crowding-out forces reduction in forward-deployed military deployments."
            )
        elif score >= 0.35:
            tier = "CONTESTED_DEFENSE_DEBT_BALANCING"
            verdict = "STRAINED_FISCAL_MILITARY_EQUILIBRIUM"
            rationale = (
                f"Contested fiscal position ({score:.4f}): Moderate debt service requires deficit financing to maintain basing."
            )
        else:
            tier = "FISCALLY_STABLE_MILITARY_PROJECTION"
            verdict = "SUSTAINABLE_GLOBAL_EXPEDITIONARY_POWER"
            rationale = (
                f"Fiscally stable ({score:.4f}): Robust tax headroom ({headroom:.2f}) easily finances expeditionary defense."
            )

        retrenchment_idx = round(min(1.0, (score * 0.65) + (debt_gdp * 0.35)), 4)

        return {
            "imperial_debt_overreach_score": score,
            "debt_service_to_defense_ratio": round(ratio, 4),
            "debt_service_annual": round(service, 4),
            "annual_defense_budget": round(defense, 4),
            "public_debt_to_gdp": round(debt_gdp, 4),
            "fiscal_revenue_headroom": round(headroom, 4),
            "fiscal_basing_retrenchment_index": retrenchment_idx,
            "imperial_debt_overreach_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_retrenchment_imminent": score >= 0.55,
        }
class BaselGoldAllocationSieve:
    """
    Phase 318: Differentiates physical allocated bullion from unbacked paper gold derivatives
    (COMEX/LBMA) under Basel III zero-risk Tier 1 rules; models sovereign reserve immunity
    against G7 unilateral asset freezes.

    Mathematical Formulation:
      z = 3.0 * (physical_bullion / (paper_derivatives + 1e-6)) + 2.5 * domestic_vault_immunity - 3.2 * fx_sanctions_vulnerability - 0.4
      S_Basel_Gold = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        physical_bullion: float = 0.85,
        paper_derivatives: float = 0.35,
        domestic_vault_immunity: float = 0.90,
        fx_sanctions_vulnerability: float = 0.20,
    ) -> dict:
        phys = max(0.0, float(physical_bullion))
        paper = max(0.0, float(paper_derivatives))
        vault = max(0.0, min(1.0, float(domestic_vault_immunity)))
        sanctions = max(0.0, min(1.0, float(fx_sanctions_vulnerability)))

        ratio = phys / (paper + 1e-6)
        z = 3.0 * ratio + 2.5 * vault - 3.2 * sanctions - 0.4
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.75:
            tier = "FORTRESS_TIER1_ALLOCATED_BULLION"
            verdict = "IMMUNE_TO_PAPER_DEFAULT_AND_SANCTIONS"
            rationale = (
                f"Sovereign gold fortress ({score:.4f}): Physical bullion ratio ({ratio:.2f}) and domestic vault "
                f"storage ({vault:.2f}) completely insulate sovereign reserves from unbacked paper defaults."
            )
        elif score >= 0.50:
            tier = "MODERATE_BULLION_PROTECTION"
            verdict = "PARTIAL_CUSTODIAL_VULNERABILITY"
            rationale = (
                f"Moderate protection ({score:.4f}): Adequate bullion backing but partial reliance on foreign custody."
            )
        else:
            tier = "CRITICAL_PAPER_DERIVATIVE_EXPOSURE"
            verdict = "HIGH_CONFISCATION_AND_DEFAULT_RISK"
            rationale = (
                f"Severe vulnerability ({score:.4f}): Heavy exposure to unbacked paper claims under foreign legal jurisdiction."
            )

        return {
            "basel_gold_allocation_score": score,
            "physical_to_paper_bullion_ratio": round(ratio, 4),
            "domestic_vault_immunity": round(vault, 4),
            "fx_sanctions_vulnerability": round(sanctions, 4),
            "basel_gold_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_sovereign_gold_fortress": score >= 0.75,
        }
class ClassicalBullionInflowTradeSieve:
    """
    Phase 330: Reconstructs historical and modern trade surplus settlement in physical gold bullion,
    analyzing the balance-of-payments mechanics of classical export power (Vikramaditya-era Roman gold drain)
    vs. modern sovereign reserve immunity.

    Mathematical Formulation:
      z = 3.0 * export_surplus_bullion_settlement + 2.6 * domestic_vault_repatriation - 3.0 * fiat_debt_dependency - 0.4
      S_Bullion_Inflow = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        export_surplus_bullion_settlement: float = 0.80,
        domestic_vault_repatriation: float = 0.85,
        fiat_debt_dependency: float = 0.25,
    ) -> dict:
        bullion = max(0.0, min(1.0, float(export_surplus_bullion_settlement)))
        vault = max(0.0, min(1.0, float(domestic_vault_repatriation)))
        fiat = max(0.0, min(1.0, float(fiat_debt_dependency)))

        z = 3.0 * bullion + 2.6 * vault - 3.0 * fiat - 0.4
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.75:
            tier = "CLASSICAL_GOLD_DRAIN_SOVEREIGN_SURPLUS"
            verdict = "NON_FIAT_TRADE_IMMUNITY_ACHIEVED"
            rationale = (
                f"Fortress sovereign surplus ({score:.4f}): Bilateral physical bullion trade settlement ({bullion:.2f}) and domestic "
                f"vault repatriation ({vault:.2f}) insulate external balances from fiat currency debasement."
            )
        elif score >= 0.50:
            tier = "HYBRID_BULLION_FIAT_SETTLEMENT"
            verdict = "BALANCED_RESERVE_ACCUMULATION"
            rationale = f"Hybrid settlement ({score:.4f}): Growing bullion allocation complementing conventional foreign exchange."
        else:
            tier = "PERPETUAL_FIAT_DEBT_DEPENDENCY"
            verdict = "EXTERNAL_LIQUIDITY_VULNERABILITY"
            rationale = f"High fiat vulnerability ({score:.4f}): Heavy reliance on unhedged dollar reserves ({fiat:.2f})."

        return {
            "classical_bullion_inflow_score": score,
            "export_surplus_bullion_settlement": round(bullion, 4),
            "domestic_vault_repatriation": round(vault, 4),
            "fiat_debt_dependency": round(fiat, 4),
            "bullion_trade_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_bullion_surplus_fortress": score >= 0.75,
        }
class EurodollarShadowLiquiditySieve:
    """
    Phase 334: Models the offshore Eurodollar shadow banking liquidity drain, cross-currency
    basis swaps, and collateral shortages that trigger emerging market currency devaluations
    during US Fed rate tightening cycles.

    Mathematical Formulation:
      z = 3.0 * eurodollar_liquidity_drain + 2.8 * cross_currency_basis_spread - 3.2 * domestic_fx_reserve_cushion - 0.4
      S_Eurodollar_Drain = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        eurodollar_liquidity_drain: float = 0.75,
        cross_currency_basis_spread: float = 0.70,
        domestic_fx_reserve_cushion: float = 0.85,
    ) -> dict:
        drain = max(0.0, min(1.0, float(eurodollar_liquidity_drain)))
        spread = max(0.0, min(1.0, float(cross_currency_basis_spread)))
        cushion = max(0.0, min(1.0, float(domestic_fx_reserve_cushion)))

        z = 3.0 * drain + 2.8 * spread - 3.2 * cushion - 0.4
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "ACUTE_OFFSHORE_DOLLAR_COLLATERAL_SQUEEZE"
            verdict = "EMERGING_MARKET_CURRENCY_DEVALUATION_PRESSURE"
            rationale = (
                f"Severe Eurodollar liquidity drain ({score:.4f}): Shadow banking collateral shortage ({drain:.2f}) and basis swap "
                f"widening ({spread:.2f}) threaten vulnerable currencies lacking adequate sovereign reserves."
            )
        elif score >= 0.45:
            tier = "MODERATE_OFFSHORE_LIQUIDITY_TIGHTENING"
            verdict = "MANAGED_CURRENCY_VOLATILITY"
            rationale = f"Moderate tightening ({score:.4f}): Domestic FX buffers ({cushion:.2f}) absorb cross-currency volatility."
        else:
            tier = "SOVEREIGN_FX_FORTRESS_INSULATION"
            verdict = "COMPLETE_SHADOW_BANKING_IMMUNITY"
            rationale = f"Sovereign insulation ({score:.4f}): Abundant FX reserves ({cushion:.2f}) insulate domestic credit markets."

        return {
            "eurodollar_shadow_liquidity_score": score,
            "eurodollar_liquidity_drain": round(drain, 4),
            "cross_currency_basis_spread": round(spread, 4),
            "domestic_fx_reserve_cushion": round(cushion, 4),
            "eurodollar_drain_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_dollar_squeeze_acute": score >= 0.70,
        }


class SovereignGoldRepatriationVelocitySieve:
    """
    Phase 336: Tracks the rate at which non-Western central banks withdraw physical gold bullion
    from Western custodians (Bank of England, NY Fed) to domestic vaults, modeling sovereign
    immunity against unilateral foreign asset freezes.

    Mathematical Formulation:
      z = 3.2 * (repatriated_bullion_metric / (foreign_custody_gold + 1e-6)) + 2.6 * domestic_vault_security - 3.0 * fx_sanction_exposure - 0.4
      S_Bullion_Repatriation = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        repatriated_bullion_metric: float = 102.0,
        foreign_custody_gold: float = 350.0,
        domestic_vault_security: float = 0.90,
        fx_sanction_exposure: float = 0.20,
    ) -> dict:
        repat = max(0.0, float(repatriated_bullion_metric))
        custody = max(0.0, float(foreign_custody_gold))
        sec = max(0.0, min(1.0, float(domestic_vault_security)))
        sanct = max(0.0, min(1.0, float(fx_sanction_exposure)))

        ratio = repat / (custody + 1e-6)
        z = 3.2 * ratio + 2.6 * sec - 3.0 * sanct - 0.4
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.75:
            tier = "RAPID_SOVEREIGN_BULLION_REPATRIATION"
            verdict = "PHYSICAL_CUSTODIAL_IMMUNITY_ACHIEVED"
            rationale = (
                f"High repatriation velocity ({score:.4f}): Aggressive withdrawal of physical bullion to domestic vaults "
                f"({sec:.2f}) decisively eliminates Western custodial freezing vulnerability."
            )
        elif score >= 0.50:
            tier = "ACTIVE_GRADUAL_REPATRIATION"
            verdict = "ONGOING_CUSTODIAL_RISK_REDUCTION"
            rationale = f"Active repatriation ({score:.4f}): Substantial gold holdings repatriated amidst residual foreign custody."
        else:
            tier = "HIGH_FOREIGN_CUSTODIAL_VULNERABILITY"
            verdict = "EXTREME_UNILATERAL_FREEZE_EXPOSURE"
            rationale = f"Critical vulnerability ({score:.4f}): Majority reserves stored in Western jurisdictions vulnerable to sanctions."

        return {
            "sovereign_gold_repatriation_velocity_score": score,
            "repatriation_to_custody_ratio": round(ratio, 4),
            "repatriated_bullion_metric": round(repat, 4),
            "foreign_custody_gold": round(custody, 4),
            "domestic_vault_security": round(sec, 4),
            "fx_sanction_exposure": round(sanct, 4),
            "repatriation_velocity_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_repatriation_velocity_high": score >= 0.75,
        }

```