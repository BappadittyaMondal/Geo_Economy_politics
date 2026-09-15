"""
Comprehensive Unit & Integration Test Suite for the Geo-Engine.
Tests all 12 analytical lenses, epistemic truth arbitration, the 85% MOU haircut rule,
kinesic protocol baseline subtraction, negative-space communique diffing,
and the end-to-end 5-Tier Response Protocol.
"""

import pytest
from geo_engine.core.models import (
    EpistemicTier,
    TemporalMode,
    FinancialFlow,
    KinesicObservation,
    CommuniqueClause,
    SummitEvent,
    SummitAnalysisReport,
)
from geo_engine.core.epistemic_hierarchy import EpistemicArbitrator, TruthClaim
from geo_engine.core.temporal_guardrail import TemporalGuardrail
from geo_engine.lenses import (
    LENS_REGISTRY,
    DeepTechLens,
    HistoryLens,
    CivilizationalLens,
    GeoEconomistLens,
    GeopoliticalLens,
    KinesicsLens,
    CashFlowLens,
    PropagandaLens,
    PetroLogisticsLens,
    BureaucraticInertiaLens,
    DigitalSovereigntyLens,
    HybridCovertLens,
    IndiaTimelineLens,
)
from geo_engine.arbitration.negative_space import NegativeSpaceDiffEngine
from geo_engine.arbitration.synthesizer import SummitSynthesizer


class TestDomainModelsAndCalculations:
    """Tests core business logic within Pydantic models."""

    def test_85_percent_mou_haircut_rule(self):
        """Unfinanced, non-binding MOUs must receive an 85% base haircut."""
        flow_unfinanced = FinancialFlow(
            source_country="China",
            target_country="Multilateral",
            project_name="Green Transition Fund",
            nominal_mou_usd=100_000_000.0,
            is_binding_contract=False,
            secondary_sanctions_risk_score=0.0
        )
        # Expected: 100M * 0.15 = 15M
        assert flow_unfinanced.effective_capex_usd == 15_000_000.0

        # With 50% sanctions risk
        flow_sanctioned = FinancialFlow(
            source_country="Russia",
            target_country="India",
            project_name="Energy Port",
            nominal_mou_usd=100_000_000.0,
            is_binding_contract=True,
            secondary_sanctions_risk_score=0.5
        )
        # Base 100M * (1 - 0.25) = 75M
        assert flow_sanctioned.effective_capex_usd == 75_000_000.0

    def test_kinesics_protocol_baseline_subtraction(self):
        """Staged formal protocol must discount calculated warmth compared to spontaneous interactions."""
        staged_interaction = KinesicObservation(
            actor_primary="Leader A",
            actor_secondary="Leader B",
            setting="formal_photocall",
            protocol_mandated=True,
            residual_tension_score=0.1, # Smiles for camera
            handshake_torque_vector="neutral_vertical"
        )
        # Protocol mandated: max warmth heavily discounted
        assert staged_interaction.genuine_warmth_index < 0.35

        spontaneous_interaction = KinesicObservation(
            actor_primary="Leader A",
            actor_secondary="Leader B",
            setting="unscripted_corridor",
            protocol_mandated=False,
            residual_tension_score=0.1,
            handshake_torque_vector="proactive_forward"
        )
        assert spontaneous_interaction.genuine_warmth_index > 0.80


class TestEpistemicArbitration:
    """Tests priority rules when analytical lenses generate conflicting assertions."""

    def test_physical_reality_overrides_communique_rhetoric(self):
        """Tier 1 (Physical) must strictly override Tier 5 (Communique/PR)."""
        physical_claim = TruthClaim(
            lens_name="PetroLogisticsLens",
            tier=EpistemicTier.TIER_1_PHYSICAL,
            assertion="Crude shipments physically diverted away from Atlantic to Asian ports.",
            confidence=0.95
        )
        propaganda_claim = TruthClaim(
            lens_name="PropagandaLens",
            tier=EpistemicTier.TIER_5_COMMUNIQUE_PR,
            assertion="Joint declaration claims complete energy self-sufficiency and zero diversion.",
            confidence=0.80
        )

        winner, log = EpistemicArbitrator.resolve_contradiction(physical_claim, propaganda_claim)
        assert winner.lens_name == "PetroLogisticsLens"
        assert winner.tier == EpistemicTier.TIER_1_PHYSICAL
        assert "strictly overrides" in log

    def test_financial_flow_overrides_kinesics(self):
        """Tier 2 (Financial) must strictly override Tier 4 (Kinesics)."""
        cash_claim = TruthClaim(
            lens_name="CashFlowLens",
            tier=EpistemicTier.TIER_2_FINANCIAL,
            assertion="Bilateral currency settlement frozen due to illiquid VOSTRO balance.",
            confidence=0.92
        )
        kinesic_claim = TruthClaim(
            lens_name="KinesicsLens",
            tier=EpistemicTier.TIER_4_KINESICS,
            assertion="Leaders displayed warm smiles and extended handshakes.",
            confidence=0.85
        )

        winner, log = EpistemicArbitrator.resolve_contradiction(cash_claim, kinesic_claim)
        assert winner.lens_name == "CashFlowLens"
        assert winner.tier == EpistemicTier.TIER_2_FINANCIAL

    def test_kinesics_vs_security_arbitration(self):
        """Military troop deployments override photocall smiles."""
        obs = KinesicObservation(
            actor_primary="India",
            actor_secondary="China",
            setting="formal_photocall",
            protocol_mandated=True,
            residual_tension_score=0.5
        )
        status, audit = EpistemicArbitrator.arbitrate_kinesics_vs_security(obs, border_deployment_tension=0.85)
        assert status == "TACTICAL_DE_ESCALATION_PERFORMANCE"
        assert "overridden by active troop deployment" in audit


class TestTemporalGuardrail:
    """Tests prevention of future-data hallucination."""

    def test_horizon_event_mode_classification(self):
        past_summit = SummitEvent(summit_name="BRICS 2023", year=2023, host_country="South Africa", location="Johannesburg")
        mode_past, _ = TemporalGuardrail.evaluate_event_mode(past_summit)
        assert mode_past == TemporalMode.EMPIRICAL_HISTORICAL

        horizon_summit = SummitEvent(summit_name="BRICS 2026", year=2026, host_country="India", location="New Delhi")
        mode_horizon, guidance = TemporalGuardrail.evaluate_event_mode(horizon_summit)
        assert mode_horizon == TemporalMode.PROSPECTIVE_SCENARIO
        assert "Game-theoretic payoff matrix projections" in guidance

    def test_prospective_tagging(self):
        text = "UNSC permanent seat reform dropped from agenda."
        tagged = TemporalGuardrail.enforce_prospective_tagging(text, TemporalMode.PROSPECTIVE_SCENARIO)
        assert tagged.startswith("[PROSPECTIVE_MODEL]")


class TestAnalyticalLenses:
    """Tests execution and output contract of all registered specialized lenses."""

    @pytest.mark.parametrize("lens_class", LENS_REGISTRY)
    def test_lens_evaluation_contract(self, lens_class):
        summit = SummitEvent(summit_name="BRICS 2026", year=2026, host_country="India", location="New Delhi")
        evaluation = lens_class.evaluate(summit)
        assert -1.0 <= evaluation.alignment_score <= 1.0
        assert 0.0 <= evaluation.confidence <= 1.0
        assert len(evaluation.key_findings) > 0
        assert isinstance(evaluation.primary_epistemic_tier, EpistemicTier)


class TestNegativeSpaceAndSynthesis:
    """Tests communique omission detection and 5-Tier synthesis output."""

    def test_negative_space_omissions_detected(self):
        clauses, counts, takeaways = NegativeSpaceDiffEngine.analyze_diff()
        assert counts["omitted_negative_space"] >= 2
        assert any("UNSC" in t for t in takeaways)
        assert any("CURR" in c.clause_id for c in clauses if c.dilution_status == "omitted_negative_space")

    def test_end_to_end_summit_synthesizer(self):
        summit = SummitEvent(summit_name="BRICS 2026 Summit", year=2026, host_country="India", location="New Delhi")
        report = SummitSynthesizer.synthesize_report(summit)

        assert isinstance(report, SummitAnalysisReport)
        assert len(report.tier1_negative_space_synopsis) >= 3
        assert len(report.tier2_country_ledgers) >= 7
        assert len(report.tier3_kinesic_forensics) >= 2
        assert "aggregate_haircut_pct" in report.tier4_hard_money_audit
        assert "sanatan_dharmic_statecraft" in report.tier5_civilizational_inner_meaning
        assert len(report.epistemic_arbitration_log) >= 3
        assert report.overall_confidence_score > 0.70


class TestQueryParser:
    """Tests dynamic natural language query parsing and intent extraction."""

    def test_complex_brics_prompt_parsing(self):
        from geo_engine.core import QueryParser
        prompt = (
            "Brics 2026 summit report, all member contries optics-what they achive "
            "frof this platefrom one by one countri. all leader bodylanguage photoshoot , "
            "message, all meating synopsis and meaning all aspect think deep and give realistic answar"
        )
        query = QueryParser.parse(prompt)
        assert query.target_summit == "BRICS 2026 Summit"
        assert query.year == 2026
        assert len(query.target_countries) == 10
        assert query.requires_kinesics is True
        assert query.requires_cash_audit is True
        assert query.requires_negative_space is True
        assert query.requires_civilizational_depth is True

    def test_targeted_bilateral_prompt_parsing(self):
        from geo_engine.core import QueryParser
        prompt = "Analyze India and China bilateral trade and border tension in SCO 2025"
        query = QueryParser.parse(prompt)
        assert query.target_summit == "SCO 2025 Summit"
        assert query.year == 2025
        assert "India" in query.target_countries
        assert "China" in query.target_countries


class TestEvidenceIngestion:
    """Tests open-access evidence ingestion pipeline."""

    def test_document_loader_creates_verified_record(self):
        from geo_engine.ingestion import DocumentLoader, ClaimType
        item = DocumentLoader.load_from_text(
            "The signatories agree to mutual currency clearing in local denominations.",
            source_name="Official Treaty Instrument",
            claim_type=ClaimType.LEGAL_COMMITMENT
        )
        assert item.evidence_id.startswith("DOC-")
        assert item.source_name == "Official Treaty Instrument"
        assert item.is_primary_sovereign is True
        assert item.reliability_weight >= 0.90

    def test_gdelt_and_sovereign_rss_ingestion(self):
        from geo_engine.ingestion import GDELTClient, SovereignRSSClient
        gdelt_items = GDELTClient.query_events("BRICS Summit", max_records=2)
        assert len(gdelt_items) >= 1
        assert "GDELT" in gdelt_items[0].source_name

        rss_items = SovereignRSSClient.fetch_primary_statements("India_MEA")
        assert len(rss_items) >= 1
        assert rss_items[0].is_primary_sovereign is True


class TestClaimAwareArbitration:
    """Tests claim-type aware priority matrix."""

    def test_legal_commitment_prioritizes_treaty_over_physical(self):
        treaty_claim = TruthClaim(
            lens_name="HistoryLens",
            tier=EpistemicTier.TIER_3_SOVEREIGN_REDLINES,
            assertion="Statutory treaty formally ratifies border protocol.",
            claim_type="LEGAL_COMMITMENT"
        )
        physical_claim = TruthClaim(
            lens_name="PetroLogisticsLens",
            tier=EpistemicTier.TIER_1_PHYSICAL,
            assertion="Patrol vehicle movement observed near border post.",
            claim_type="LEGAL_COMMITMENT"
        )
        winner, log = EpistemicArbitrator.resolve_claim_aware(treaty_claim, physical_claim)
        assert winner.lens_name == "HistoryLens"
        assert "LEGAL_COMMITMENT" in log

    def test_physical_presence_prioritizes_physical_over_pr(self):
        satellite_claim = TruthClaim(
            lens_name="PetroLogisticsLens",
            tier=EpistemicTier.TIER_1_PHYSICAL,
            assertion="Tanker convoy physically located at West Coast terminal.",
            claim_type="PHYSICAL_PRESENCE"
        )
        pr_claim = TruthClaim(
            lens_name="PropagandaLens",
            tier=EpistemicTier.TIER_5_COMMUNIQUE_PR,
            assertion="Press statement asserts tanker fleet is idle.",
            claim_type="PHYSICAL_PRESENCE"
        )
        winner, log = EpistemicArbitrator.resolve_claim_aware(satellite_claim, pr_claim)
        assert winner.lens_name == "PetroLogisticsLens"
        assert "PHYSICAL_PRESENCE" in log


class TestForecastingCalibration:
    """Tests Brier score verification and 4-strata output."""

    def test_brier_score_math(self):
        from geo_engine.forecasting import BrierScorer
        # Perfect prediction: prob 1.0, outcome 1
        assert BrierScorer.calculate_brier_score([1.0], [1]) == 0.0
        # Complete miss: prob 1.0, outcome 0
        assert BrierScorer.calculate_brier_score([1.0], [0]) == 1.0
        # Multi-outcome calibrated: ( (0.8-1)^2 + (0.2-0)^2 ) / 2 = (0.04 + 0.04)/2 = 0.04
        score = BrierScorer.calculate_brier_score([0.8, 0.2], [1, 0])
        assert score == 0.04

    def test_epistemic_strata_structure(self):
        from geo_engine.forecasting import ForecastingEngine
        strata = ForecastingEngine.generate_strata("BRICS 2026 Summit", 2026)
        assert len(strata.observed_facts) >= 3
        assert len(strata.inferred_realities) >= 2
        assert len(strata.scenario_branches) == 3
        assert sum(s.probability for s in strata.scenario_branches) == 1.0
        assert len(strata.calibrated_forecasts) >= 2


class TestEngineUpgrades:
    """Tests for systemic upgrades: LENS_REGISTRY, Stage 0 Normalizer, Kinesics Tier 0,
    Cash Flow Clamping, EventStore SQLite, Persona Narrators, and Strategic News Ranker."""

    def test_lens_registry_dynamic_discovery(self):
        assert len(LENS_REGISTRY) == 18
        lens_names = [cls.__name__ for cls in LENS_REGISTRY]
        assert "IndiaTimelineLens" in lens_names
        assert "CashFlowLens" in lens_names
        assert "KinesicsLens" in lens_names
        assert "DemographicInfiltrationLens" in lens_names
        assert "CriticalMineralsLens" in lens_names
        assert "InstitutionalLawfareLens" in lens_names
        assert "FoodSecurityLens" in lens_names
        assert "MilitaryReadinessLens" in lens_names


    def test_ingestion_normalizer_claim_extraction(self):
        from geo_engine.ingestion import IngestionNormalizer, DocumentLoader, ClaimType
        ev_item = DocumentLoader.load_from_text(
            "India and Bangladesh signed agreement for $5.0 billion deep sea port with binding budgetary allocation.",
            source_name="Official Bilateral Instrument",
            claim_type=ClaimType.FINANCIAL_CAPEX
        )
        claims = IngestionNormalizer.normalize_evidence_item(ev_item)
        assert len(claims) >= 1
        fin_claims = [c for c in claims if c.claim_type == ClaimType.FINANCIAL_CAPEX]
        assert len(fin_claims) >= 1
        fc = fin_claims[0]
        assert "India" in fc.actors
        assert "Bangladesh" in fc.actors
        assert fc.extracted_financial_mou_usd == 5_000_000_000.0
        assert fc.is_binding_commitment is True
        assert "CashFlowLens" in fc.target_lenses

    def test_kinesics_tier_0_text_safeguard(self):
        summit = SummitEvent(summit_name="BRICS 2026 Summit", year=2026, host_country="India", location="New Delhi")
        # Text-only general claims passed to kinesics lens without visual telemetry
        general_claim = TruthClaim(
            lens_name="PropagandaLens",
            tier=EpistemicTier.TIER_5_COMMUNIQUE_PR,
            assertion="Leaders shook hands warmly and exchanged smiles.",
            claim_type="RHETORICAL_POSTURE"
        )
        eval_res = KinesicsLens.evaluate(summit, observations=None, claims=[general_claim])
        assert eval_res.primary_epistemic_tier == EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE
        assert eval_res.evidence_status == "insufficient"
        assert eval_res.confidence == 0.0

    def test_cash_flow_clamping_gate(self):
        summit = SummitEvent(summit_name="BRICS 2026 Summit", year=2026, host_country="India", location="New Delhi")
        # Non-binding flow (85% haircut -> 15% effective CapEx)
        flow_nonbinding = [
            FinancialFlow(
                source_country="China",
                target_country="India",
                project_name="Vague Energy MOU",
                nominal_mou_usd=100_000_000.0,
                is_binding_contract=False,
                secondary_sanctions_risk_score=0.0
            )
        ]
        eval_nb = CashFlowLens.evaluate(summit, flows=flow_nonbinding)
        # capex_ratio = 15M / 100M = 0.15; clamped = 0.15 + 0.85*0.15 = 0.2775 ~ 0.28
        assert eval_nb.alignment_score <= 0.30

        # Fully binding flow (100% effective CapEx)
        flow_binding = [
            FinancialFlow(
                source_country="UAE",
                target_country="India",
                project_name="Dedicated Port Logistics Escrow",
                nominal_mou_usd=100_000_000.0,
                is_binding_contract=True,
                secondary_sanctions_risk_score=0.0
            )
        ]
        eval_b = CashFlowLens.evaluate(summit, flows=flow_binding)
        # capex_ratio = 100M / 100M = 1.0; clamped = 0.15 + 0.85*1.0 = 1.0
        assert eval_b.alignment_score == 1.0

    def test_event_store_persistence(self):
        from geo_engine.storage.event_store import EventStore
        store = EventStore()
        # Seeded events check
        events = store.get_events_by_region("South Asia")
        assert len(events) >= 1
        assert any("Bangladesh" in e["title"] or "Ram Mandir" in e["title"] for e in events)

        # Baseline treaty clauses
        brics_clauses = store.get_baseline_clauses("BRICS")
        assert len(brics_clauses) >= 1

    def test_persona_narrator_archetypes(self):
        from geo_engine.arbitration.persona_narrator import PersonaNarrator
        summit = SummitEvent(summit_name="BRICS 2026 Summit", year=2026, host_country="India", location="New Delhi")
        report = SummitSynthesizer.synthesize_report(summit)

        sanyal = PersonaNarrator.narrate(report, "sanyal")
        assert "Sanjeev Sanyal" in sanyal
        assert "Complex Adaptive Systems" in sanyal or "haircut" in sanyal or "Mundell-Fleming" in sanyal


        doval = PersonaNarrator.narrate(report, "doval")
        assert "Ajit Doval" in doval
        assert "Redline" in doval or "Intelligence" in doval or "Strategic" in doval or "security" in doval.lower()

        jaishankar = PersonaNarrator.narrate(report, "jaishankar")
        assert "Jaishankar" in jaishankar
        assert "Multi-alignment" in jaishankar or "Hedging" in jaishankar or "Strategic Autonomy" in jaishankar or "autonomy" in jaishankar.lower()

        ranganathan = PersonaNarrator.narrate(report, "ranganathan")
        assert "Anand Ranganathan" in ranganathan
        assert "empirical" in ranganathan.lower() or "civilizational" in ranganathan.lower()

        ankit = PersonaNarrator.narrate(report, "ankit_shah")
        assert "Ankit Shah" in ankit
        assert "dollar" in ankit.lower() or "bullion" in ankit.lower() or "monetary" in ankit.lower()



    def test_strategic_news_ranker_scoring(self):
        from morning_digest.ranker import StrategicNewsRanker
        from geo_engine.ingestion.models import EvidenceItem
        scored = StrategicNewsRanker.score_headline(
            "Troop disengagement along the LAC finalized with verified border buffer zones."
        )
        assert scored["primary_domain"] == "border_security"
        assert scored["strategic_score"] >= 0.35

        # Test batch ranking
        dummy_items = [
            EvidenceItem(
                evidence_id="DUMMY-1",
                source_name="Test Defense Source",
                source_type="news_wire",
                timestamp="2026-09-14T08:00:00",
                raw_text="Troop disengagement along the LAC finalized with verified border buffer zones.",
                reliability_weight=0.9
            ),
            EvidenceItem(
                evidence_id="DUMMY-2",
                source_name="Test Financial Source",
                source_type="news_wire",
                timestamp="2026-09-14T08:00:00",
                raw_text="Routine stock market closing indices and consumer retail prices in New Delhi.",
                reliability_weight=0.8
            )
        ]
        ranked = StrategicNewsRanker.rank_headlines(evidence_items=dummy_items, top_n=2)
        assert len(ranked) == 2
        assert ranked[0]["strategic_score"] > ranked[1]["strategic_score"]

    def test_historical_anniversary_matcher(self):
        from geo_engine.storage.event_store import EventStore
        store = EventStore()
        
        # Test July 31 matching Guadalete (711 AD)
        annivs_july = store.match_anniversaries(7, 31)
        assert len(annivs_july) >= 1
        guadalete = [a for a in annivs_july if "Guadalete" in a["event_title"]]
        assert len(guadalete) == 1
        assert guadalete[0]["year"] == 711
        assert "Europe / Iberia" in guadalete[0]["region"]
        assert "Tariq ibn Ziyad" in guadalete[0]["historical_summary"]

        # Test January 2 matching Granada (1492 AD)
        annivs_jan = store.match_anniversaries(1, 2)
        assert len(annivs_jan) >= 1
        granada = [a for a in annivs_jan if "Granada" in a["event_title"]]
        assert len(granada) == 1
        assert granada[0]["year"] == 1492

        # Test full month search for August (Indo-Soviet 1971 & Dhaka 2024)
        annivs_aug = store.match_anniversaries(8)
        assert len(annivs_aug) >= 2
        titles = [a["event_title"] for a in annivs_aug]
        assert any("Indo-Soviet" in t for t in titles)
        assert any("Dhaka" in t for t in titles)

    def test_forecast_ledger_persistence_and_resolution(self):
        from geo_engine.storage.event_store import EventStore
        store = EventStore()
        
        forecast_id = "FCST-TEST-SPAIN-2026"
        store.record_forecast({
            "forecast_id": forecast_id,
            "created_at": "2026-09-14T10:00:00",
            "target_date": "2026-12-31",
            "event_name": "Iberian Maritime Border Transit Stress",
            "hypothesis": "Frontex emergency intervention requested along Andalucian littoral",
            "predicted_probability": 0.75,
            "confidence_interval_low": 0.60,
            "confidence_interval_high": 0.85,
            "epistemic_basis": "Historical mirror (711 AD) and demographic infiltration lens telemetry",
            "status": "ACTIVE"
        })

        active_forecasts = store.get_forecast_ledger(status="ACTIVE")
        assert any(f["forecast_id"] == forecast_id for f in active_forecasts)

        # Resolve forecast as true event (actual_outcome = 1)
        # Brier score = (0.75 - 1.0)^2 = (-0.25)^2 = 0.0625
        brier = store.resolve_forecast(forecast_id=forecast_id, actual_outcome=1)
        assert brier == 0.0625

        resolved = store.get_forecast_ledger(status="RESOLVED")
        entry = next(f for f in resolved if f["forecast_id"] == forecast_id)
        assert entry["brier_score"] == 0.0625
        assert entry["actual_outcome"] == 1

    def test_bayesian_scenario_updating(self):
        from geo_engine.forecasting.calibration import ForecastingEngine, ScenarioBranch
        from geo_engine.core.epistemic_hierarchy import TruthClaim, EpistemicTier

        base_scenarios = [
            ScenarioBranch(
                scenario_name="Scenario A: Baseline Stability",
                probability=0.60,
                key_drivers=["Status quo trade accords"],
                early_indicators=["Calm shipping lanes"],
                impact_severity="LOW"
            ),
            ScenarioBranch(
                scenario_name="Scenario B: Sanctions & Decoupling Disruption",
                probability=0.25,
                key_drivers=["Secondary sanctions enforcement"],
                early_indicators=["Vessel seizures"],
                impact_severity="HIGH"
            ),
            ScenarioBranch(
                scenario_name="Scenario C: Sinocentric Institutional Capture Friction",
                probability=0.15,
                key_drivers=["CIPS forced settlement"],
                early_indicators=["Bilateral payment divergence"],
                impact_severity="MEDIUM"
            )
        ]

        claims = [
            TruthClaim(
                lens_name="InstitutionalLawfareLens",
                tier=EpistemicTier.TIER_3_SOVEREIGN_REDLINES,
                assertion="US OFAC secondary sanctions and asset freeze targeting shipping logistics.",
                claim_type="SOVEREIGN_REDLINE"
            ),
            TruthClaim(
                lens_name="DemographicInfiltrationLens",
                tier=EpistemicTier.TIER_1_PHYSICAL,
                assertion="Severe migrant chokepoint infiltration crossing.",
                claim_type="PHYSICAL_STATUS"
            )
        ]

        updated = ForecastingEngine.update_scenario_probabilities(base_scenarios, claims)
        assert len(updated) == 3
        # Probabilities must sum strictly to 1.0
        assert sum(s.probability for s in updated) == pytest.approx(1.0, abs=1e-3)
        # Disruption probability should have significantly increased from base 0.25
        disruption_scenario = next(s for s in updated if "Disruption" in s.scenario_name)
        baseline_scenario = next(s for s in updated if "Baseline" in s.scenario_name)
        assert disruption_scenario.probability > 0.25
        assert baseline_scenario.probability < 0.60

    def test_non_summit_query_parsing(self):
        from geo_engine.core.query_parser import QueryParser
        
        # Border security crisis with focal date
        q1 = QueryParser.parse("31st July 2026 Spain border infiltration along Andalucia coast")
        assert q1.event_type == "BORDER_SECURITY"
        assert "Spain" in q1.target_countries
        assert q1.year == 2026
        assert q1.focal_date is not None and "31" in q1.focal_date
        assert q1.requires_demographic_audit is True
        assert "Spain Border Security" in q1.target_event

        # Hybrid warfare / lawfare query
        q2 = QueryParser.parse("FATF greylisting and ICC sovereign asset freeze 2026")
        assert q2.event_type == "HYBRID_WARFARE"
        assert q2.year == 2026
        assert q2.requires_lawfare_audit is True

    def test_strategic_lenses_grounded_telemetry(self):
        from geo_engine.lenses import (
            DemographicInfiltrationLens,
            CriticalMineralsLens,
            InstitutionalLawfareLens
        )
        from geo_engine.core.models import StrategicEvent
        from geo_engine.core.epistemic_hierarchy import TruthClaim, EpistemicTier

        event = StrategicEvent(
            event_name="Strategic Test Horizon",
            year=2026,
            event_type="BORDER_SECURITY",
            location="Iberian Littoral"
        )

        # Lens 14: Demographic Infiltration
        claim_demo = TruthClaim(
            lens_name="DemographicInfiltrationLens",
            tier=EpistemicTier.TIER_1_PHYSICAL,
            assertion="Mass Spain border infiltration along Andalucia maritime transit route.",
            claim_type="PHYSICAL_STATUS"
        )
        eval_demo = DemographicInfiltrationLens.evaluate(event, claims=[claim_demo])
        assert eval_demo.alignment_score == -0.70
        assert eval_demo.hard_metrics["border_stress_index"] == 0.91
        assert any("GROUNDED TELEMETRY" in f for f in eval_demo.key_findings)

        # Lens 15: Critical Minerals
        claim_minerals = TruthClaim(
            lens_name="CriticalMineralsLens",
            tier=EpistemicTier.TIER_1_PHYSICAL,
            assertion="Rare earth export restriction and lithium processing chokepoint threat.",
            claim_type="PHYSICAL_STATUS"
        )
        eval_min = CriticalMineralsLens.evaluate(event, claims=[claim_minerals])
        assert eval_min.alignment_score == -0.60
        assert eval_min.hard_metrics["material_sovereignty_index"] == 0.32
        assert any("GROUNDED TELEMETRY" in f for f in eval_min.key_findings)

        # Lens 16: Institutional Lawfare
        claim_lawfare = TruthClaim(
            lens_name="InstitutionalLawfareLens",
            tier=EpistemicTier.TIER_3_SOVEREIGN_REDLINES,
            assertion="FATF grey-listing threat and sovereign asset freeze escalation.",
            claim_type="SOVEREIGN_REDLINE"
        )
        eval_law = InstitutionalLawfareLens.evaluate(event, claims=[claim_lawfare])
        assert eval_law.alignment_score == -0.75
        assert eval_law.hard_metrics["fatf_regulatory_friction_score"] == 0.90
        assert any("GROUNDED TELEMETRY" in f for f in eval_law.key_findings)


class TestInstitutionalHardening:
    """Tests for institutional-grade reliability, disambiguation, WAL concurrency,
    dynamic country ledgers, and evidence integrity."""

    def test_lac_military_border_routing_disambiguation(self):
        from geo_engine.core.query_parser import QueryParser
        q = QueryParser.parse("India China LAC border troop deployment and standoff 2026")
        assert q.event_type == "BORDER_MILITARY"
        assert q.requires_demographic_audit is False
        assert "India" in q.target_countries
        assert "China" in q.target_countries
        assert "geopolitical" in q.prioritized_lenses
        assert "demographic_infiltration" not in q.prioritized_lenses
        assert "Sovereign Border Military Standoff" in q.target_event

    def test_demographic_border_routing_disambiguation(self):
        from geo_engine.core.query_parser import QueryParser
        q = QueryParser.parse("Spain Morocco Ceuta Melilla border fence migrant infiltration 2026")
        assert q.event_type == "BORDER_SECURITY"
        assert q.requires_demographic_audit is True
        assert "Spain" in q.target_countries
        assert "Morocco" in q.target_countries
        assert "demographic_infiltration" in q.prioritized_lenses
        assert "Border Security & Infiltration" in q.target_event

    def test_system_reference_date_runtime_clock(self):
        import os
        from datetime import datetime
        from geo_engine.core.models import get_system_reference_date
        from geo_engine.core.temporal_guardrail import TemporalGuardrail

        # Default clock
        baseline_dt = get_system_reference_date()
        assert baseline_dt.year == 2026
        assert baseline_dt.month == 9

        # Dynamic override via environment
        os.environ["SYSTEM_REFERENCE_DATE"] = "2027-04-15T12:00:00"
        try:
            custom_dt = get_system_reference_date()
            assert custom_dt.year == 2027
            assert custom_dt.month == 4
            assert TemporalGuardrail.get_reference_date().year == 2027
        finally:
            del os.environ["SYSTEM_REFERENCE_DATE"]

    def test_dynamic_country_ledgers_non_brics(self):
        from geo_engine.arbitration.synthesizer import SummitSynthesizer

        # Non-BRICS pair: Spain and Morocco
        ledgers = SummitSynthesizer.generate_country_ledgers(target_countries=["Spain", "Morocco"])
        assert len(ledgers) == 2
        countries = [l.country_name for l in ledgers]
        assert "Spain" in countries
        assert "Morocco" in countries
        spain_audit = next(l for l in ledgers if l.country_name == "Spain")
        assert "Schengen" in spain_audit.public_domestic_narrative
        assert "Frontex" in spain_audit.geopolitical_yield

        # Geopolitical pair: Taiwan and USA
        ledgers_tw_us = SummitSynthesizer.generate_country_ledgers(target_countries=["Taiwan", "USA"])
        assert len(ledgers_tw_us) == 2
        tw_audit = next(l for l in ledgers_tw_us if l.country_name == "Taiwan")
        assert "semiconductor" in tw_audit.public_domestic_narrative

    def test_production_fixture_mode_isolation(self):
        from geo_engine.core.models import SummitEvent, EpistemicTier
        from geo_engine.arbitration.synthesizer import SummitSynthesizer
        from geo_engine.lenses.cash_flow import CashFlowLens

        summit = SummitEvent(summit_name="BRICS 2026 Summit", year=2026, host_country="India", location="New Delhi")

        # In production mode (fixture_mode=False), absence of visual telemetry produces empty kinesics
        report = SummitSynthesizer.synthesize_report(summit, fixture_mode=False)
        assert len(report.kinesic_forensics) == 0
        assert any("EVIDENCE_DEGRADED" in log for log in report.epistemic_arbitration_log)

        # In CashFlowLens, empty claims in fixture_mode=False yield TIER_0
        cf_eval = CashFlowLens.evaluate(summit, claims=[], fixture_mode=False)
        assert cf_eval.primary_epistemic_tier == EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE
        assert cf_eval.evidence_status == "insufficient"
        assert cf_eval.hard_metrics["total_nominal_announced_usd"] == 0.0

    def test_parameterized_forecasting_event_types_mece(self):
        import pytest
        from geo_engine.forecasting.calibration import ForecastingEngine

        # Border military event
        strata_mil = ForecastingEngine.generate_strata(event_type="BORDER_MILITARY", year=2026)
        assert len(strata_mil.scenario_branches) == 4
        assert sum(s.probability for s in strata_mil.scenario_branches) == pytest.approx(1.0, abs=1e-3)
        assert any("Residual" in s.scenario_name for s in strata_mil.scenario_branches)
        assert any("patrol disengagement" in fc.target_hypothesis for fc in strata_mil.calibrated_forecasts)

        # Geo-economic event
        strata_econ = ForecastingEngine.generate_strata(event_type="GEO_ECONOMIC", year=2026)
        assert len(strata_econ.scenario_branches) == 4
        assert sum(s.probability for s in strata_econ.scenario_branches) == pytest.approx(1.0, abs=1e-3)

        # Summit with include_unmodeled=True
        strata_summit_mece = ForecastingEngine.generate_strata(include_unmodeled=True)
        assert len(strata_summit_mece.scenario_branches) == 4
        assert sum(s.probability for s in strata_summit_mece.scenario_branches) == pytest.approx(1.0, abs=1e-3)

    def test_sqlite_wal_mode_and_concurrency(self):
        from geo_engine.storage.event_store import EventStore

        store = EventStore()
        with store._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode;")
            row = cursor.fetchone()
            assert row[0].lower() == "wal"

            cursor.execute("PRAGMA busy_timeout;")
            timeout_row = cursor.fetchone()
            assert timeout_row[0] >= 5000

    def test_ingestion_wire_deduplication(self):
        from geo_engine.ingestion.models import EvidenceItem, ClaimType
        from geo_engine.ingestion.normalizer import IngestionNormalizer

        raw_wire = "Reuters: India and Bangladesh sign binding agreement on Teesta water sharing for $5 billion USD."
        item1 = EvidenceItem(
            evidence_id="wire-reuters-01",
            source_name="Reuters",
            source_type="news_wire",
            timestamp="2026-09-14T10:00:00",
            provenance_url="https://reuters.com/wire/1",
            raw_text=raw_wire,
            claim_type=ClaimType.FINANCIAL_CAPEX,
            reliability_weight=0.90
        )
        item2 = EvidenceItem(
            evidence_id="wire-syndicated-02",
            source_name="Syndicated Agency Feed",
            source_type="news_wire",
            timestamp="2026-09-14T10:05:00",
            provenance_url="https://syndicate.com/wire/2",
            raw_text=raw_wire,  # Identical wire text
            claim_type=ClaimType.FINANCIAL_CAPEX,
            reliability_weight=0.85
        )

        batch_claims = IngestionNormalizer.normalize_evidence_batch([item1, item2])
        # Deduplication must collapse identical syndicated wires into a single claim set
        fin_claims = [c for c in batch_claims if c.claim_type == ClaimType.FINANCIAL_CAPEX]
        assert len(fin_claims) == 1


class TestInstitutionalExpansionPhase30:
    """Tests for Phase 30 and Phase 31 institutional upgrades:
    - Evidence propagation from batch ingestion to lens evaluation
    - Reliability-weighted Bayesian filtering
    - Multi-currency normalization (EUR, GBP, INR, USD)
    - Deterministic SHA-256 forecast IDs
    - FoodSecurityLens and MilitaryReadinessLens evaluations
    - CIVILIZATIONAL_CRISIS synthesis branch
    """

    def test_evidence_propagation_to_lenses(self):
        from geo_engine.ingestion.models import ClaimItem, ClaimType
        summit = SummitEvent(
            summit_name="Strategic Agriculture & Defense Summit 2026",
            year=2026,
            host_country="India",
            location="New Delhi",
            event_type="STRATEGIC_EVENT"
        )
        claim = ClaimItem(
            claim_id="clm-food-01",
            source_evidence_id="ev-food-01",
            claim_type=ClaimType.LEGAL_COMMITMENT,
            asserted_fact="Bilateral fertilizer supply contract for 2.5M metric tons of DAP and Urea finalized.",
            target_lenses=["FoodSecurityLens", "MilitaryReadinessLens"],
            epistemic_tier=EpistemicTier.TIER_1_PHYSICAL,
            reliability_weight=0.90
        )
        report = SummitSynthesizer.synthesize_report(summit, claims=[claim])
        assert report is not None
        assert report.event.summit_name == "Strategic Agriculture & Defense Summit 2026"

    def test_reliability_weighted_bayesian_filtering(self):
        from geo_engine.forecasting.calibration import ForecastingEngine, ScenarioBranch
        from geo_engine.ingestion.models import ClaimItem, ClaimType
        scenarios = [
            ScenarioBranch(
                scenario_name="Scenario A: Baseline Stability",
                probability=0.50,
                key_drivers=["Status quo protocols"],
                early_indicators=["Scheduled meetings"],
                impact_severity="LOW"
            ),
            ScenarioBranch(
                scenario_name="Scenario B: Sanctions & Decoupling Disruption",
                probability=0.50,
                key_drivers=["Secondary sanctions enforcement"],
                early_indicators=["Vessel seizures"],
                impact_severity="HIGH"
            )
        ]
        # Claim with reliability 0.0 must not affect probabilities
        zero_rel_claim = ClaimItem(
            claim_id="clm-zero-01",
            source_evidence_id="ev-zero-01",
            claim_type=ClaimType.LEGAL_COMMITMENT,
            asserted_fact="Secondary sanctions and OFAC asset freeze targeting logistics.",
            target_lenses=["InstitutionalLawfareLens"],
            epistemic_tier=EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE,
            reliability_weight=0.0
        )
        updated = ForecastingEngine.update_scenario_probabilities(scenarios, [zero_rel_claim])
        assert updated[0].probability == pytest.approx(0.50)
        assert updated[1].probability == pytest.approx(0.50)

        # Verified claim with high reliability should update scenario probabilities
        verified_claim = ClaimItem(
            claim_id="clm-ver-02",
            source_evidence_id="ev-ver-02",
            claim_type=ClaimType.LEGAL_COMMITMENT,
            asserted_fact="Secondary sanctions and OFAC asset freeze targeting logistics.",
            target_lenses=["InstitutionalLawfareLens"],
            epistemic_tier=EpistemicTier.TIER_1_PHYSICAL,
            reliability_weight=0.95
        )
        updated_2 = ForecastingEngine.update_scenario_probabilities(scenarios, [verified_claim])
        assert updated_2[1].probability > 0.50
        assert updated_2[0].probability < 0.50
        assert sum(s.probability for s in updated_2) == pytest.approx(1.0, abs=1e-3)

    def test_multi_currency_normalization(self):
        from geo_engine.ingestion.normalizer import IngestionNormalizer
        # Euro (€)
        eur_flow = IngestionNormalizer.extract_financial_flow("France committed €5.0 billion to joint defense co-production.")
        assert eur_flow is not None
        assert eur_flow == pytest.approx(5_000_000_000.0 * 1.09, rel=1e-2)

        # British Pound (£)
        gbp_flow = IngestionNormalizer.extract_financial_flow("UK pledged £2.0 billion for maritime engine research.")
        assert gbp_flow is not None
        assert gbp_flow == pytest.approx(2_000_000_000.0 * 1.28, rel=1e-2)

        # Indian Rupee (₹/Rs)
        inr_flow = IngestionNormalizer.extract_financial_flow("Cabinet approved ₹500 crore for critical mineral processing facility.")
        assert inr_flow is not None
        assert inr_flow > 50_000_000.0  # 500 crore INR is ~$59.5M USD

        # US Dollar ($)
        usd_flow = IngestionNormalizer.extract_financial_flow("Sovereign fund invested $10.0 billion into semiconductor fab.")
        assert usd_flow is not None
        assert usd_flow == pytest.approx(10_000_000_000.0)

    def test_forecast_id_reproducibility(self):
        import hashlib
        from geo_engine.forecasting.calibration import ForecastingEngine
        year = 2026
        target_hypothesis = "BRICS expands bilateral local currency clearing volume by >20% within 12 months"
        id_seed = f"{year}:{target_hypothesis}"
        hypo_hash = hashlib.sha256(id_seed.encode("utf-8")).hexdigest()[:8]
        fc_id_1 = f"FCST-{year}-{hypo_hash}"
        fc_id_2 = f"FCST-{year}-{hypo_hash}"
        assert fc_id_1 == fc_id_2
        assert fc_id_1.startswith("FCST-2026-")

        summit = SummitEvent(summit_name="BRICS 2026 Summit", year=2026, host_country="India", location="New Delhi")
        strata = ForecastingEngine.generate_strata(summit)
        assert len(strata.calibrated_forecasts) >= 2
        assert all(fc.forecast_probability >= 0.0 for fc in strata.calibrated_forecasts)

    def test_food_security_and_military_readiness_contracts(self):
        from geo_engine.lenses.food_security import FoodSecurityLens
        from geo_engine.lenses.military_readiness import MilitaryReadinessLens
        summit = SummitEvent(summit_name="Defense and Agriculture 2026", year=2026, host_country="India", location="New Delhi")

        food_eval = FoodSecurityLens.evaluate(summit)
        assert food_eval.hard_metrics["urea_import_dependency_pct"] == 28.4
        assert food_eval.hard_metrics["mop_potash_import_dependency_pct"] == 100.0
        assert food_eval.confidence >= 0.85
        assert food_eval.evidence_status == "sufficient"

        mil_eval = MilitaryReadinessLens.evaluate(summit)
        assert mil_eval.hard_metrics["two_front_deterrence_posture_score"] == 0.78
        assert mil_eval.hard_metrics["wwr_ammunition_reserve_days"] == 21.5
        assert mil_eval.confidence >= 0.90
        assert mil_eval.evidence_status == "sufficient"

    def test_civilizational_crisis_synthesis_branch(self):
        summit = SummitEvent(
            summit_name="Existential Civilizational Crisis Protocol",
            year=2026,
            host_country="India",
            location="New Delhi",
            event_type="CIVILIZATIONAL_CRISIS"
        )
        report = SummitSynthesizer.synthesize_report(summit)
        assert "Annaraksha" in report.civilizational_synthesis["civilizational_core"]
        assert "Dhanya Kosha" in report.civilizational_synthesis["sanatan_dharmic_statecraft"]
        assert "Ayudhadhyaksha" in report.civilizational_synthesis["sanatan_dharmic_statecraft"]

    def test_civilizational_crisis_forecasting_strata(self):
        from geo_engine.forecasting.calibration import ForecastingEngine
        strata = ForecastingEngine.generate_strata(
            summit_name="Civilizational Protocol Crisis 2026",
            year=2026,
            event_type="CIVILIZATIONAL_CRISIS"
        )
        assert len(strata.scenario_branches) == 4
        assert any("Pragmatic Diplomatic Containment" in s.scenario_name for s in strata.scenario_branches)
        assert any("Domestic Theological Backlash" in s.scenario_name for s in strata.scenario_branches)
        assert len(strata.calibrated_forecasts) >= 2
        assert any("treaties remain legally and operationally intact" in f.target_hypothesis for f in strata.calibrated_forecasts)

    def test_cli_lenses_persona_weighting(self):
        from geo_engine.cli import render_lenses_summary
        # Verify render_lenses_summary runs cleanly with persona parameter
        render_lenses_summary(summit_name="BRICS 2026 Summit", persona="doval")


class TestPhase32Hardening:
    """Tests Phase 32 Release Engineering, Epistemic Tier-Weighted Confidence & Strategic Resilience Matrix."""

    def test_epistemic_tier_weighted_confidence(self):
        from geo_engine.core.models import SummitEvent, EpistemicTier
        from geo_engine.arbitration.synthesizer import SummitSynthesizer

        summit = SummitEvent(summit_name="BRICS 2026 Summit", year=2026, host_country="India", location="New Delhi")
        report = SummitSynthesizer.synthesize_report(summit)

        # Overall confidence score must be mathematically bound between 0.0 and 1.0
        assert 0.0 <= report.overall_confidence_score <= 1.0
        # Tier 1 physical lenses (0.85-0.95 confidence) weighted heavily must ensure robust confidence
        assert report.overall_confidence_score >= 0.70

    def test_clause_dilution_status_categorization(self):
        from geo_engine.arbitration.negative_space import NegativeSpaceDiffEngine

        clauses = NegativeSpaceDiffEngine.load_baseline_from_store()
        assert len(clauses) >= 4

        # Check status assignments
        unsc_clause = next((c for c in clauses if "UNSC" in c.clause_id or "UNSC" in c.raw_text), None)
        if unsc_clause:
            assert unsc_clause.dilution_status == "omitted_negative_space"

        terror_clause = next((c for c in clauses if "TERROR" in c.clause_id or "terror" in c.raw_text.lower()), None)
        if terror_clause:
            assert terror_clause.dilution_status == "diluted_passive"

        pay_clause = next((c for c in clauses if "PAY" in c.clause_id or "local-currency" in c.raw_text.lower()), None)
        if pay_clause:
            assert pay_clause.dilution_status == "retained_full"

    def test_strategic_resilience_matrix_in_report(self):
        from geo_engine.core.models import SummitEvent
        from geo_engine.arbitration.synthesizer import SummitSynthesizer

        summit = SummitEvent(summit_name="Strategic Frontier 2026", year=2026, host_country="India", location="New Delhi")
        report = SummitSynthesizer.synthesize_report(summit)

        matrix = report.strategic_resilience_matrix
        assert matrix is not None
        assert "food_caloric_sovereignty_index" in matrix
        assert matrix["strategic_grain_buffer_ratio"] >= 1.0
        assert "two_front_deterrence_posture" in matrix
        assert matrix["wwr_ammunition_reserve_days"] >= 10.0
        assert "critical_minerals_sovereignty_index" in matrix
        assert "demographic_border_vulnerability" in matrix

        # Verify arbitration log contains Tier 1 physical reality citations
        physical_logs = [log for log in report.epistemic_arbitration_log if "[ARBITRATION_T1_PHYSICAL]" in log]
        assert len(physical_logs) >= 2

    def test_cli_render_full_report_with_resilience_matrix(self):
        from geo_engine.core.models import SummitEvent
        from geo_engine.arbitration.synthesizer import SummitSynthesizer
        from geo_engine.cli import render_full_report

        summit = SummitEvent(summit_name="BRICS 2026 Summit", year=2026, host_country="India", location="New Delhi")
        report = SummitSynthesizer.synthesize_report(summit)

        # Verify render_full_report renders cleanly with the new strategic resilience matrix and persona
        render_full_report(target_event=summit, persona="jaishankar")


class TestCanonicalBundlesAndGovernance:
    """Rigorous machine-verifiable tests for Phase 33 Canonical Multi-AI Distribution Architecture."""

    @classmethod
    def setup_class(cls):
        import os
        cls.repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @classmethod
    def resolve_path(cls, rel_path: str) -> str:
        import os
        import re
        base = os.path.basename(rel_path)
        candidates = [
            os.path.join(cls.repo_root, rel_path),
            os.path.join(cls.repo_root, "consolidate_50_files", rel_path),
            os.path.join(cls.repo_root, "dist_ai", "deep_50", rel_path),
            os.path.join(cls.repo_root, "consolidate_5_files", base),
            os.path.join(cls.repo_root, "dist_ai", "core_5", base),
            os.path.join(cls.repo_root, "consolidate_50_files", base),
            os.path.join(cls.repo_root, "dist_ai", "deep_50", base),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        for search_dir in [
            os.path.join(cls.repo_root, "consolidate_50_files"),
            os.path.join(cls.repo_root, "dist_ai", "deep_50"),
            os.path.join(cls.repo_root, "consolidate_5_files"),
            os.path.join(cls.repo_root, "dist_ai", "core_5"),
            cls.repo_root
        ]:
            if os.path.exists(search_dir):
                for f in os.listdir(search_dir):
                    if f == base or f.endswith(base) or base.endswith(f):
                        return os.path.join(search_dir, f)
                    core_keyword = re.sub(r"^\d+_", "", base)
                    if core_keyword in f:
                        return os.path.join(search_dir, f)
        return candidates[0]

    def test_canonical_governance_contract_and_tier_weights(self):
        import os
        contract_path = self.resolve_path("00_CANONICAL/00_CANONICAL_CONTRACT.md")
        assert os.path.exists(contract_path)
        with open(contract_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check supreme contract headers and release
        assert "CANONICAL-CONTRACT-V1.0" in content
        assert "Contract: `C2`" in content
        assert "Architecture: `A3`" in content
        assert "Registry: `R18`" in content
        assert "https://github.com/BappadittyaMondal/Geo_Economy_politics.git" in content

        # Check 5 Epistemic Tiers and Mathematical Weights
        assert "Tier 1: Physical Reality" in content and "1.00" in content
        assert "Tier 2: Hard Financial Flows" in content and "0.85" in content
        assert "Tier 3: Sovereign Redlines" in content and "0.70" in content
        assert "Tier 4: Filtered Kinesics" in content and "0.30" in content
        assert "Tier 5: Communiqué / PR" in content and "0.10" in content

        # Check mathematical clamping laws
        assert "0.15" in content  # 85% haircut rule
        assert "Mundell-Fleming" in content
        assert "Protocol Baseline Subtraction" in content or "Protocol Subtraction" in content

    def test_canonical_manifest_structure_and_lens_parity(self):
        import os
        import re
        manifest_path = self.resolve_path("00_CANONICAL/01_CANONICAL_MANIFEST.yaml")
        assert os.path.exists(manifest_path)
        with open(manifest_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Version Matrix
        assert 'project_version: "0.0.5"' in content
        assert 'contract_version: "C2"' in content
        assert 'architecture_version: "A3"' in content
        assert 'registry_version: "R18"' in content
        assert 'bundle_version: "B1"' in content

        # All 18 lenses mapped in manifest
        lens_ids = re.findall(r'- id:\s*"LENS-(\d{2})"', content)
        assert len(lens_ids) == 18
        for i in range(1, 19):
            expected = f"{i:02d}"
            assert expected in lens_ids

    def test_evidence_capability_matrix_confidence_ceilings(self):
        import os
        import re
        matrix_path = self.resolve_path("00_CANONICAL/02_EVIDENCE_CAPABILITY_MATRIX.md")
        assert os.path.exists(matrix_path)
        with open(matrix_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 5-State Capability Maturity Model
        for state in ["DESIGNED", "IMPLEMENTED", "TESTED", "EVIDENCE-CONN.", "RELEASE-ELIGIBLE"]:
            assert state in content

        # 18 Lenses present in capability table
        table_lenses = re.findall(r"\|\s*\*\*?(L\d{2})", content)
        assert len(table_lenses) == 18

    def test_anti_drift_quality_gates_execution(self):
        import os
        from scripts.build_canonical_bundles import verify_anti_drift_gates, CORE_5_DIR, DEEP_50_DIR

        # Execute the 10 quality gates verification
        result = verify_anti_drift_gates()
        assert result is True

        # Verify Core-5 strict file count and format
        core_files = [f for f in os.listdir(CORE_5_DIR) if not f.startswith(".")]
        assert len(core_files) == 5
        assert all(f.endswith(".md") for f in core_files)

        # Verify Deep-50 file count and format
        deep_files = [f for f in os.listdir(DEEP_50_DIR) if not f.startswith(".")]
        assert len(deep_files) <= 50
        assert all(f.endswith(".md") for f in deep_files)

    def test_rag_context_headers_and_zero_db_contamination(self):
        import os
        from scripts.build_canonical_bundles import CORE_5_DIR, DEEP_50_DIR

        # Core 5 must have RAG context headers and zero .db files
        for fname in os.listdir(CORE_5_DIR):
            fpath = os.path.join(CORE_5_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            assert "<!-- RAG_CONTEXT_HEADER" in content
            assert "CANONICAL_COMMIT:" in content
            assert "CANONICAL_REPO:" in content
            assert not fname.endswith(".db")

        # Deep 50 must have zero .db files and serialized database markdown
        for fname in os.listdir(DEEP_50_DIR):
            assert not fname.endswith(".db")
        assert os.path.exists(os.path.join(DEEP_50_DIR, "38_spec_historical_treaty_archive.md"))

    def test_consolidate_folders_structure_and_subfolders(self):
        import os
        from scripts.build_canonical_bundles import CONSOLIDATE_5_DIR, CONSOLIDATE_50_DIR

        assert os.path.exists(CONSOLIDATE_5_DIR)
        assert os.path.exists(CONSOLIDATE_50_DIR)

        # Folder 1: consolidate_5_files
        assert os.path.exists(os.path.join(CONSOLIDATE_5_DIR, "CONSOLIDATED_CORE_5_ALL_IN_ONE.md"))
        for fname in ["00_CANONICAL_CONTRACT.md", "01_SYSTEM_ARCHITECTURE.md", "02_OBJECT_AND_DATA_CONTRACTS.md", "03_ENGINE_AND_LENS_REGISTRY.md", "04_RUNTIME_OPERATING_PROTOCOL.md"]:
            assert os.path.exists(os.path.join(CONSOLIDATE_5_DIR, fname))
        # Subfolders validation if present (backward compatible with nested or flat modes)
        for sdir in ["00_CANONICAL", "01_ARCHITECTURE", "02_CONTRACTS", "03_REGISTRY", "04_PROTOCOLS"]:
            subpath = os.path.join(CONSOLIDATE_5_DIR, sdir)
            if os.path.exists(subpath):
                assert os.path.isdir(subpath)

        # Folder 2: consolidate_50_files
        assert os.path.exists(os.path.join(CONSOLIDATE_50_DIR, "CONSOLIDATED_DEEP_50_ALL_IN_ONE.md"))
        for fname in ["00_CANONICAL_CONTRACT.md", "01_SYSTEM_ARCHITECTURE.md", "02_OBJECT_AND_DATA_CONTRACTS.md", "03_ENGINE_AND_LENS_REGISTRY.md", "04_RUNTIME_OPERATING_PROTOCOL.md"]:
            assert os.path.exists(os.path.join(CONSOLIDATE_50_DIR, fname))
        for sdir in ["00_CANONICAL", "01_ARCHITECTURE", "02_CONTRACTS", "03_REGISTRY", "04_PROTOCOLS", "05_LENSES", "06_GOVERNANCE", "07_ARCHIVE"]:
            subpath = os.path.join(CONSOLIDATE_50_DIR, sdir)
            if os.path.exists(subpath):
                assert os.path.isdir(subpath)







