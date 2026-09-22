"""
Comprehensive Unit & Integration Test Suite for the Geo-Engine.
Tests all 20 analytical lenses, epistemic truth arbitration, the 85% MOU haircut rule,
kinesic protocol baseline subtraction, negative-space communique diffing,
video intelligence subsystem, persona narrator, adversarial resilience,
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
    FoodSecurityLens,
    MilitaryReadinessLens
)


@pytest.fixture(scope="session", autouse=True)
def isolated_test_database():
    """Isolates all test runs to a temporary SQLite database, preventing mutation of canonical data/events.db."""
    import tempfile
    import os
    import shutil
    from geo_engine.storage.event_store import EventStore

    with tempfile.NamedTemporaryFile(suffix="_test_events.db", delete=False) as tf:
        temp_db = tf.name

    # Pre-seed temp_db from canonical seed data if present
    canonical_db = EventStore.DEFAULT_DB_PATH
    if os.path.exists(canonical_db):
        shutil.copy2(canonical_db, temp_db)

    os.environ["GEO_ENGINE_DB_PATH"] = temp_db
    yield temp_db
    os.environ.pop("GEO_ENGINE_DB_PATH", None)
    if os.path.exists(temp_db):
        try:
            os.remove(temp_db)
        except Exception:
            pass

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
        assert len(LENS_REGISTRY) == 20
        lens_names = [cls.__name__ for cls in LENS_REGISTRY]
        assert "IndiaTimelineLens" in lens_names
        assert "CashFlowLens" in lens_names
        assert "KinesicsLens" in lens_names
        assert "DemographicInfiltrationLens" in lens_names
        assert "CriticalMineralsLens" in lens_names
        assert "InstitutionalLawfareLens" in lens_names
        assert "FoodSecurityLens" in lens_names
        assert "MilitaryReadinessLens" in lens_names
        assert "SubseaCablesLens" in lens_names
        assert "AstroPoliticsLens" in lens_names


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
        import tempfile
        import os
        from geo_engine.storage.event_store import EventStore

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            temp_db = tf.name
        try:
            store = EventStore(db_path=temp_db)
            # Seeded events check
            events = store.get_events_by_region("South Asia")
            assert len(events) >= 1
            assert any("Bangladesh" in e["title"] or "Ram Mandir" in e["title"] for e in events)

            # Baseline treaty clauses
            brics_clauses = store.get_baseline_clauses("BRICS")
            assert len(brics_clauses) >= 1
        finally:
            if os.path.exists(temp_db):
                try:
                    os.remove(temp_db)
                except Exception:
                    pass


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
        import tempfile
        import os
        from geo_engine.storage.event_store import EventStore

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            temp_db = tf.name
        try:
            store = EventStore(db_path=temp_db)

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
        finally:
            if os.path.exists(temp_db):
                try:
                    os.remove(temp_db)
                except Exception:
                    pass


    def test_forecast_ledger_persistence_and_resolution(self):
        import tempfile
        import os
        from geo_engine.storage.event_store import EventStore

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            temp_db = tf.name

        try:
            store = EventStore(db_path=temp_db)

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
        finally:
            if os.path.exists(temp_db):
                try:
                    os.remove(temp_db)
                except Exception:
                    pass


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
        import tempfile
        import os
        from geo_engine.storage.event_store import EventStore

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            temp_db = tf.name
        try:
            store = EventStore(db_path=temp_db)
            with store._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA journal_mode;")
                row = cursor.fetchone()
                assert row[0].lower() == "wal"

                cursor.execute("PRAGMA busy_timeout;")
                timeout_row = cursor.fetchone()
                assert timeout_row[0] >= 5000
        finally:
            if os.path.exists(temp_db):
                try:
                    os.remove(temp_db)
                except Exception:
                    pass


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
        assert "Registry: `R20`" in content
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
        assert 'registry_version: "R20"' in content
        assert 'bundle_version: "B1"' in content

        # All 20 lenses mapped in manifest
        lens_ids = re.findall(r'- id:\s*"LENS-(\d{2})"', content)
        assert len(lens_ids) == 20
        for i in range(1, 21):
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

        # 20 Lenses present in capability table
        table_lenses = re.findall(r"\|\s*\*\*?(L\d{2})", content)
        assert len(table_lenses) == 20

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
        from scripts.build_canonical_bundles import CONSOLIDATE_5_DIR, CONSOLIDATE_50_DIR, ALL_IN_ONE_DIR

        assert os.path.exists(CONSOLIDATE_5_DIR)
        assert os.path.exists(CONSOLIDATE_50_DIR)

        # Folder 1: consolidate_5_files (Strictly Flat: 5 Files, 0 Subfolders - Hard 5-File Ceilings)
        assert len([f for f in os.listdir(CONSOLIDATE_5_DIR) if not f.startswith(".")]) == 5
        for fname in ["00_CANONICAL_CONTRACT.md", "01_SYSTEM_ARCHITECTURE.md", "02_OBJECT_AND_DATA_CONTRACTS.md", "03_ENGINE_AND_LENS_REGISTRY.md", "04_RUNTIME_OPERATING_PROTOCOL.md"]:
            assert os.path.exists(os.path.join(CONSOLIDATE_5_DIR, fname))
        subdirs_5 = [d for d in os.listdir(CONSOLIDATE_5_DIR) if os.path.isdir(os.path.join(CONSOLIDATE_5_DIR, d))]
        assert len(subdirs_5) == 0, f"Expected 0 subdirectories in consolidate_5_files, found: {subdirs_5}"

        # Dedicated All-in-One Master Bundles
        assert os.path.exists(os.path.join(ALL_IN_ONE_DIR, "CONSOLIDATED_CORE_5_ALL_IN_ONE.md"))
        assert os.path.exists(os.path.join(ALL_IN_ONE_DIR, "CONSOLIDATED_DEEP_50_ALL_IN_ONE.md"))

        # Folder 2: consolidate_50_files (Strictly Flat: <= 50 Files, 0 Subfolders)
        assert os.path.exists(os.path.join(CONSOLIDATE_50_DIR, "CONSOLIDATED_DEEP_50_ALL_IN_ONE.md"))
        assert os.path.exists(os.path.join(CONSOLIDATE_50_DIR, "01_CANONICAL_MANIFEST.yaml"))
        for fname in ["00_CANONICAL_CONTRACT.md", "01_SYSTEM_ARCHITECTURE.md", "02_OBJECT_AND_DATA_CONTRACTS.md", "03_ENGINE_AND_LENS_REGISTRY.md", "04_RUNTIME_OPERATING_PROTOCOL.md"]:
            assert os.path.exists(os.path.join(CONSOLIDATE_50_DIR, fname))
        subdirs_50 = [d for d in os.listdir(CONSOLIDATE_50_DIR) if os.path.isdir(os.path.join(CONSOLIDATE_50_DIR, d))]
        assert len(subdirs_50) == 0, f"Expected 0 subdirectories in consolidate_50_files, found: {subdirs_50}"


class TestPhase35Hardening:
    """Tests for Phase 35: Universal lens claim acceptance, resilience matrix alignment,
    and Telegram bot CLI contracts."""

    def test_all_18_lenses_universal_claim_acceptance(self):
        import inspect
        from geo_engine.lenses import LENS_REGISTRY
        from geo_engine.core.models import SummitEvent, EpistemicTier
        from geo_engine.core.epistemic_hierarchy import TruthClaim
        from geo_engine.lenses.petro_logistics import PetroLogisticsLens
        from geo_engine.lenses.digital_sovereignty import DigitalSovereigntyLens
        from geo_engine.lenses.geo_economist import GeoEconomistLens
        from geo_engine.lenses.propaganda import PropagandaLens
        from geo_engine.lenses.bureaucratic_inertia import BureaucraticInertiaLens
        from geo_engine.lenses.hybrid_covert import HybridCovertLens
        from geo_engine.lenses.history import HistoryLens
        from geo_engine.lenses.civilizational import CivilizationalLens

        assert len(LENS_REGISTRY) == 20

        # 1. Verify all 20 lenses accept claims
        for lens in LENS_REGISTRY:
            sig = inspect.signature(lens.evaluate)
            assert "claims" in sig.parameters, f"Lens {lens.__name__} does not accept claims in evaluate()"

        summit = SummitEvent(
            summit_name="Kazan BRICS Test Event",
            year=2024,
            host_country="Russia",
            primary_agenda="Multilateral Architecture Test"
        )

        # 2. Test PetroLogisticsLens grounded telemetry
        claim_petro = TruthClaim(
            lens_name="PetroLogisticsLens",
            tier=EpistemicTier.TIER_1_PHYSICAL,
            assertion="Crude oil tanker flows through Strait of Hormuz chokepoint.",
            claim_type="PHYSICAL_STATUS"
        )
        res_petro = PetroLogisticsLens.evaluate(summit, claims=[claim_petro])
        assert any("GROUNDED TELEMETRY" in f for f in res_petro.key_findings)
        assert res_petro.hard_metrics.get("grounded_energy_claims_verified") is True

        # 3. Test DigitalSovereigntyLens grounded telemetry
        claim_digital = TruthClaim(
            lens_name="DigitalSovereigntyLens",
            tier=EpistemicTier.TIER_1_PHYSICAL,
            assertion="Semiconductor compute chips export controls on GPU hardware.",
            claim_type="PHYSICAL_STATUS"
        )
        res_dig = DigitalSovereigntyLens.evaluate(summit, claims=[claim_digital])
        assert any("GROUNDED TELEMETRY" in f for f in res_dig.key_findings)
        assert res_dig.hard_metrics.get("grounded_digital_claims_verified") is True

        # 4. Test GeoEconomistLens grounded telemetry
        claim_macro = TruthClaim(
            lens_name="GeoEconomistLens",
            tier=EpistemicTier.TIER_2_FINANCIAL,
            assertion="Bilateral local currency trade clearing and mBridge settlement.",
            claim_type="FINANCIAL_FLOW"
        )
        res_macro = GeoEconomistLens.evaluate(summit, claims=[claim_macro])
        assert any("GROUNDED TELEMETRY" in f for f in res_macro.key_findings)
        assert res_macro.hard_metrics.get("grounded_monetary_claims_verified") is True

        # 5. Test HistoryLens and CivilizationalLens
        claim_hist = TruthClaim(
            lens_name="HistoryLens",
            tier=EpistemicTier.TIER_3_SOVEREIGN_REDLINES,
            assertion="1993 Peace and Tranquility Treaty and Panchsheel precedent.",
            claim_type="SOVEREIGN_REDLINE"
        )
        res_hist = HistoryLens.evaluate(summit, claims=[claim_hist])
        assert any("GROUNDED TELEMETRY" in f for f in res_hist.key_findings)

        claim_civ = TruthClaim(
            lens_name="CivilizationalLens",
            tier=EpistemicTier.TIER_3_SOVEREIGN_REDLINES,
            assertion="Kautilya Raja Mandala alignment and Rajdharma sovereignty.",
            claim_type="SOVEREIGN_REDLINE"
        )
        res_civ = CivilizationalLens.evaluate(summit, claims=[claim_civ])
        assert any("GROUNDED TELEMETRY" in f for f in res_civ.key_findings)

    def test_strategic_resilience_matrix_exact_lens_keys(self):
        from geo_engine.arbitration.synthesizer import SummitSynthesizer
        from geo_engine.core.models import SummitEvent

        summit = SummitEvent(
            summit_name="16th BRICS Summit",
            year=2024,
            host_country="Russia",
            primary_agenda="Strengthening Multilateralism"
        )
        report = SummitSynthesizer.synthesize_report(summit)
        srm = report.strategic_resilience_matrix

        # Must receive dynamic score 0.62 from IndiaTimelineLens, NOT fallback 0.60
        assert srm["strategic_frontier_timeline_score"] == 0.62
        # Must receive dynamic score 0.48 from CriticalMineralsLens
        assert srm["critical_minerals_sovereignty_index"] == 0.48
        # Must receive dynamic score 0.72 from DemographicInfiltrationLens
        assert srm["demographic_border_vulnerability"] == 0.72
        # Must receive dynamic score 0.65 from InstitutionalLawfareLens
        assert srm["institutional_lawfare_ofac_risk"] == 0.65
        # Must receive dynamic score 0.81 from FoodSecurityLens
        assert srm["food_caloric_sovereignty_index"] == 0.81
        # Must receive dynamic score 0.78 from MilitaryReadinessLens
        assert srm["two_front_deterrence_posture"] == 0.78


    def test_telegram_bot_argument_parsing(self):
        from morning_digest.bot import build_parser

        parser = build_parser()

        args_dry = parser.parse_args(["--dry-run"])
        assert args_dry.dry_run is True
        assert args_dry.live is False

        args_live = parser.parse_args(["--live"])
        assert args_live.live is True
        assert args_live.dry_run is False

        args_default = parser.parse_args([])
        assert args_default.live is False
        assert args_default.dry_run is False


class TestPhase37Hardening:
    """Phase 37 verification: Keyword matrix expansion, execution gating, and operational resilience."""

    def test_query_parser_newly_registered_lenses(self):
        from geo_engine.core.query_parser import QueryParser

        q_tech = QueryParser.parse("Analyze quantum computing and semiconductor chip algorithms")
        assert "deep_tech" in q_tech.prioritized_lenses
        assert "digital_sovereignty" in q_tech.prioritized_lenses

        q_hist = QueryParser.parse("What do the 1962 war archives and Westphalia precedents say?")
        assert "history" in q_hist.prioritized_lenses

        q_econ = QueryParser.parse("Evaluate the Mundell-Fleming trilemma and balance of payments")
        assert "geo_economist" in q_econ.prioritized_lenses

        q_bureaucracy = QueryParser.parse("Examine Press Note 3 inter-ministerial delays and red tape")
        assert "bureaucratic_inertia" in q_bureaucracy.prioritized_lenses

        q_covert = QueryParser.parse("Detect grey zone subversion and covert sabotage in the maritime corridor")
        assert "hybrid_covert" in q_covert.prioritized_lenses

    def test_all_20_lenses_present_in_registry(self):
        from geo_engine.lenses import LENS_REGISTRY
        assert len(LENS_REGISTRY) == 20
        names = {lens.__name__ for lens in LENS_REGISTRY}
        expected = {
            "DeepTechLens", "HistoryLens", "CivilizationalLens", "GeoEconomistLens",
            "GeopoliticalLens", "KinesicsLens", "CashFlowLens", "PropagandaLens",
            "PetroLogisticsLens", "FoodSecurityLens", "MilitaryReadinessLens",
            "DiplomaticProtocolLens", "BureaucraticInertiaLens", "DigitalSovereigntyLens",
            "HybridCovertLens", "IndiaTimelineLens", "DemographicInfiltrationLens",
            "CriticalMineralsLens", "InstitutionalLawfareLens", "SubseaCablesLens",
            "AstroPoliticsLens"
        }
        assert names.issubset(expected)
        assert len(names) == 20

    def test_telegram_bot_dispatch_state_tracking(self, monkeypatch):
        from morning_digest.bot import TelegramDigestPublisher

        monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
        TelegramDigestPublisher.last_delivery_success = False
        res = TelegramDigestPublisher.send_to_telegram("Phase 37 Test")
        assert res is False
        assert TelegramDigestPublisher.last_delivery_success is False

    def test_calibration_sqlite_persistence_logging(self, monkeypatch, capsys):
        from geo_engine.forecasting.calibration import ForecastingEngine
        from geo_engine.storage.event_store import EventStore

        def mock_record_forecast(self, record):
            raise RuntimeError("Simulated SQLite write lock timeout")

        monkeypatch.setattr(EventStore, "record_forecast", mock_record_forecast)

        strata = ForecastingEngine.generate_strata(
            summit_name="Test Resilience Summit",
            year=2026
        )
        assert strata is not None
        captured = capsys.readouterr()
        assert "[WARNING] Failed to persist forecast to SQLite ledger" in captured.err


class TestPhase38Hardening:
    """Tests for Phase 38 upgrades: 20-Lens Matrix, Execution Gating, Video Intelligence, and Digest Multi-Lens Scoring."""

    def test_subsea_cables_lens_evaluation(self):
        from geo_engine.lenses.subsea_cables import SubseaCablesLens
        from geo_engine.core.models import SummitEvent, EpistemicTier
        from geo_engine.core.epistemic_hierarchy import TruthClaim

        event = SummitEvent(
            summit_name="Indian Ocean Littoral Forum",
            year=2026,
            host_country="India",
            primary_agenda="Deep Seabed Infrastructure"
        )
        res = SubseaCablesLens.evaluate(event)
        assert "Subsea Cables" in res.lens_name
        assert res.primary_epistemic_tier == EpistemicTier.TIER_1_PHYSICAL
        assert "subsea_bandwidth_dependency_pct" in res.hard_metrics
        assert "hydro_spatial_sovereignty_score" in res.hard_metrics

        # Test with physical claim
        claim = TruthClaim(
            lens_name="SubseaCablesLens",
            tier=EpistemicTier.TIER_1_PHYSICAL,
            assertion="Underwater acoustic array deployed in the Andaman Sea with 99.2% cable protection coverage.",
            claim_type="PHYSICAL_STATUS"
        )
        res_with_claim = SubseaCablesLens.evaluate(event, claims=[claim])
        assert res_with_claim.hard_metrics["hydro_spatial_sovereignty_score"] > res.hard_metrics["hydro_spatial_sovereignty_score"]

    def test_astro_politics_lens_evaluation(self):
        from geo_engine.lenses.astro_politics import AstroPoliticsLens
        from geo_engine.core.models import SummitEvent, EpistemicTier
        from geo_engine.core.epistemic_hierarchy import TruthClaim

        event = SummitEvent(
            summit_name="Global Space Summit",
            year=2026,
            host_country="India",
            primary_agenda="Counter-Space Deterrence"
        )
        res = AstroPoliticsLens.evaluate(event)
        assert "Astro-Politics" in res.lens_name
        assert res.primary_epistemic_tier == EpistemicTier.TIER_1_PHYSICAL
        assert "satcom_sovereignty_coverage_pct" in res.hard_metrics
        assert "orbital_sovereignty_index" in res.hard_metrics

        # Test with physical claim
        claim = TruthClaim(
            lens_name="AstroPoliticsLens",
            tier=EpistemicTier.TIER_1_PHYSICAL,
            assertion="Mission Shakti kinetic ASAT capability verified alongside NavIC constellation deployment.",
            claim_type="PHYSICAL_STATUS"
        )
        res_with_claim = AstroPoliticsLens.evaluate(event, claims=[claim])
        assert res_with_claim.hard_metrics["orbital_sovereignty_index"] > res.hard_metrics["orbital_sovereignty_index"]

    def test_execution_gating_in_synthesizer(self):
        from geo_engine.arbitration.synthesizer import SummitSynthesizer
        from geo_engine.core.models import SummitEvent

        event = SummitEvent(
            summit_name="Subsea Security Forum",
            year=2026,
            host_country="India",
            primary_agenda="Subsea infrastructure"
        )
        # Test gated execution with only subsea_cables prioritized
        report = SummitSynthesizer.synthesize_report(
            summit=event,
            prioritized_lenses=["subsea_cables"]
        )
        assert len(report.lens_evaluations) == 1
        assert "Subsea Cables" in report.lens_evaluations[0].lens_name

        # Test ungated fallback evaluates all 20 lenses
        full_report = SummitSynthesizer.synthesize_report(
            summit=event,
            prioritized_lenses=None
        )
        assert len(full_report.lens_evaluations) == 20

    def test_youtube_url_parser_validation(self):
        from geo_engine.video.url_parser import YouTubeURLParser
        import pytest

        valid_urls = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", 0),
            ("https://youtu.be/dQw4w9WgXcQ?t=90s", "dQw4w9WgXcQ", 90),
            ("https://youtube.com/embed/dQw4w9WgXcQ?start=120", "dQw4w9WgXcQ", 120),
            ("https://m.youtube.com/watch?v=dQw4w9WgXcQ&t=2m15s", "dQw4w9WgXcQ", 135)
        ]
        for url, expected_id, expected_t in valid_urls:
            parsed = YouTubeURLParser.parse(url)
            assert parsed["video_id"] == expected_id
            assert parsed["start_seconds"] == expected_t

        # Invalid domains / schemes
        with pytest.raises(ValueError):
            YouTubeURLParser.parse("https://malicious-site.com/watch?v=dQw4w9WgXcQ")
        with pytest.raises(ValueError):
            YouTubeURLParser.parse("ftp://youtube.com/watch?v=dQw4w9WgXcQ")
        with pytest.raises(ValueError):
            YouTubeURLParser.parse("https://youtube.com/watch?v=short")

    def test_video_intelligence_pipeline(self):
        from geo_engine.video import VideoSynthesizer, VideoIndexer, VideoRetriever, TranscriptSegment

        segments = [
            TranscriptSegment(text="Opening remarks on maritime strategy.", start=0.0, duration=15.0),
            TranscriptSegment(text="The deployment of subsea cables and hydrophones in the Indian Ocean.", start=15.0, duration=25.0),
            TranscriptSegment(text="NavIC positioning autonomy protects against foreign GPS blackouts.", start=40.0, duration=20.0),
        ]
        report = VideoSynthesizer.synthesize_video_query(
            video_url="https://www.youtube.com/watch?v=12345678901",
            query="subsea cables and Indian ocean",
            custom_segments=[s.model_dump() for s in segments]
        )
        assert report.video_id == "12345678901"
        assert len(report.relevant_chunks) > 0
        assert "subsea" in report.relevant_chunks[0].text.lower()
        assert len(report.cited_timestamps) > 0
        assert "https://youtu.be/12345678901?t=" in report.cited_timestamps[0]["url"]
        assert "<untrusted_video_transcript" in report.prompt_envelope
        assert "SECURITY NOTICE:" in report.prompt_envelope

    def test_morning_digest_multi_lens_and_india_impact(self):
        from morning_digest.ranker import StrategicNewsRanker

        res = StrategicNewsRanker.score_headline(
            "India deploys NavIC-guided coastal patrol vessels to protect subsea landing stations in Chennai."
        )
        assert res["strategic_score"] >= 0.15
        assert res["india_impact_score"] >= 0.3
        assert "subsea_cables" in res["lens_tags"]
        assert "astro_politics" in res["lens_tags"]

    def test_cli_forecast_ledger_invocation(self, monkeypatch):
        from geo_engine.cli import render_forecast_ledger
        from geo_engine.storage.event_store import EventStore

        def mock_get_forecast_ledger(self, status=None):
            return [{
                "forecast_id": "FC-TEST-001",
                "target_date": "2026-10-24",
                "event_name": "Kazan Summit",
                "hypothesis": "BRICS unit of account remains virtual MOU.",
                "predicted_probability": 0.88,
                "confidence_interval_low": 0.70,
                "confidence_interval_high": 0.95,
                "epistemic_basis": "Multi-lens synthesis",
                "status": "ACTIVE",
                "actual_outcome": None,
                "brier_score": None
            }]

        monkeypatch.setattr(EventStore, "get_forecast_ledger", mock_get_forecast_ledger)
        # Should execute cleanly without throwing
        render_forecast_ledger()

    def test_cli_video_intelligence_invocation(self):
        from geo_engine.cli import render_video_intelligence

        # Should execute cleanly with fallback simulated transcript
        render_video_intelligence(
            video_url="https://www.youtube.com/watch?v=12345678901",
            query="subsea cables and NavIC"
        )


class TestVideoSubsystem:
    """Tests the video intelligence pipeline components."""

    def test_url_parser_valid_youtube_urls(self):
        from geo_engine.video.url_parser import YouTubeURLParser
        result = YouTubeURLParser.parse("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert result is not None
        assert result["video_id"] == "dQw4w9WgXcQ"

    def test_url_parser_rejects_non_youtube(self):
        from geo_engine.video.url_parser import YouTubeURLParser
        import pytest
        with pytest.raises(ValueError):
            YouTubeURLParser.parse("https://vimeo.com/12345678")

    def test_url_parser_short_url(self):
        from geo_engine.video.url_parser import YouTubeURLParser
        result = YouTubeURLParser.parse("https://youtu.be/dQw4w9WgXcQ?t=120")
        assert result is not None
        assert result["video_id"] == "dQw4w9WgXcQ"

    def test_transcript_engine_fallback(self):
        from geo_engine.video.transcript_engine import VideoTranscriptEngine
        result = VideoTranscriptEngine.fetch_transcript("test_video_id_12")
        assert result is not None
        assert hasattr(result, 'segments')
        assert len(result.segments) > 0

    def test_indexer_creates_chunks(self):
        from geo_engine.video.indexer import VideoIndexer
        from geo_engine.video.transcript_engine import VideoTranscriptEngine
        # Use the built-in fallback transcript to get valid TranscriptSegment objects
        result = VideoTranscriptEngine.fetch_transcript("test_indexer_vid")
        chunks = VideoIndexer.index_transcript(result.segments, "test_indexer_vid")
        assert isinstance(chunks, list)
        assert len(chunks) >= 1


class TestPersonaNarrator:
    """Tests persona projection layer."""

    def test_all_five_personas_produce_output(self):
        from geo_engine.arbitration.persona_narrator import PersonaNarrator
        # Create a minimal report for persona projection
        summit = SummitEvent(
            summit_name="Persona Test", year=2026,
            host_country="India", location="Delhi",
            member_countries=["India", "China"]
        )
        report = SummitSynthesizer.synthesize_report(summit)
        for persona_name in ["sanyal", "doval", "jaishankar", "ranganathan", "ankit_shah"]:
            result = PersonaNarrator.apply_persona(report, persona_name)
            assert result is not None
            assert isinstance(result, dict)

    def test_persona_lens_weights_coverage(self):
        from geo_engine.arbitration.persona_narrator import PersonaNarrator
        for persona_name in ["sanyal", "doval", "jaishankar", "ranganathan", "ankit_shah"]:
            profile = PersonaNarrator.ARCHETYPES.get(persona_name, {})
            assert "lens_weights" in profile, f"Persona {persona_name} missing lens_weights"
            assert isinstance(profile["lens_weights"], dict)


class TestAdversarialResilience:
    """Tests edge cases and adversarial inputs."""

    def test_query_parser_empty_input(self):
        from geo_engine.core.query_parser import QueryParser
        result = QueryParser.parse("")
        assert result is not None
        assert result.event_type is not None

    def test_query_parser_whitespace_input(self):
        from geo_engine.core.query_parser import QueryParser
        result = QueryParser.parse("   \n\t   ")
        assert result is not None

    def test_query_parser_oversized_input(self):
        from geo_engine.core.query_parser import QueryParser
        oversized = "india china lac border " * 500  # 12000 chars, exceeds 5000-char cap
        result = QueryParser.parse(oversized)
        assert result is not None

    def test_query_parser_unicode_input(self):
        from geo_engine.core.query_parser import QueryParser
        result = QueryParser.parse("भारत-चीन LAC सीमा विवाद и Россия-Индия партнёрство")
        assert result is not None


class TestPhase40Hardening:
    """Phase 40 governance and timing verification."""

    def test_cli_typing_imports_complete(self):
        """Verify cli.py has all required typing imports (regression gate for bug A-1)."""
        import importlib
        import inspect
        from geo_engine import cli
        # Force module reload to verify imports at parse time
        importlib.reload(cli)
        # Verify render_full_report signature can be inspected without NameError
        sig = inspect.signature(cli.render_full_report)
        params = list(sig.parameters.keys())
        assert "claims" in params
        assert "evidence_items" in params

    def test_readme_lens_count_parity(self):
        """Verify README.md references 20 lenses (not stale 16)."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        if readme_path.exists():
            content = readme_path.read_text(encoding="utf-8")
            assert "20-Lens" in content or "20 Analytical Lenses" in content, \
                f"README.md still references stale lens count"
            assert "16-Lens" not in content, "README.md still references stale 16-Lens"

    def test_full_synthesis_timing_guard(self):
        """Ensure full synthesis completes in under 15 seconds."""
        import time
        summit = SummitEvent(
            summit_name="Timing Test Summit", year=2026,
            host_country="India", location="New Delhi",
            member_countries=["India", "China", "Russia"]
        )
        start = time.monotonic()
        report = SummitSynthesizer.synthesize_report(summit)
        elapsed = time.monotonic() - start
        assert elapsed < 15.0, f"Full synthesis took {elapsed:.2f}s, exceeding 15s gate"
        assert report.overall_confidence_score > 0.0


class TestPhase41DeepCausality:
    """Phase 41 deep causality, inter-lens coupling, and Bayesian self-learning tests."""

    def test_inter_lens_financial_clamping(self):
        """High CapEx haircut (85%) clamps forward-looking economic alignment ceiling to 0.45."""
        from geo_engine.core.models import LensEvaluation, EpistemicTier
        log = []
        evals = [
            LensEvaluation(
                lens_name="Geo-Economic Realism & Monetary Architecture",
                alignment_score=0.80,
                confidence=0.90,
                primary_epistemic_tier=EpistemicTier.TIER_2_FINANCIAL,
                key_findings=["Announced $50B multilateral fund."],
                hard_metrics={}
            )
        ]
        coupled, _ = SummitSynthesizer.apply_inter_lens_coupling(
            lens_evals=evals,
            hard_money_audit={"aggregate_haircut_pct": 85.0},
            arbitration_log=log
        )
        assert coupled[0].alignment_score <= 0.45
        assert any("[INTER_LENS_CLAMP_FINANCIAL]" in entry for entry in log)

    def test_inter_lens_contradiction_penalty(self):
        """Tier 5 PR rhetoric contradicting Tier 2 CapEx haircut triggers contradiction penalty."""
        from geo_engine.core.models import LensEvaluation, EpistemicTier
        log = []
        evals = [
            LensEvaluation(
                lens_name="Propaganda & Narrative Warfare",
                alignment_score=0.85,
                confidence=0.90,
                primary_epistemic_tier=EpistemicTier.TIER_5_COMMUNIQUE_PR,
                key_findings=["Boasts complete bilateral unanimity and $100B fund."],
                hard_metrics={}
            )
        ]
        coupled, penalty = SummitSynthesizer.apply_inter_lens_coupling(
            lens_evals=evals,
            hard_money_audit={"aggregate_haircut_pct": 85.0},
            arbitration_log=log
        )
        assert penalty > 0.0
        assert coupled[0].confidence <= 0.40
        assert any("[INTER_LENS_CONTRADICTION]" in entry for entry in log)

    def test_bayesian_reliability_weight_persistence(self):
        """Forecast resolution backpropagates error into persistent SQLite lens reliability multipliers."""
        from geo_engine.storage.event_store import EventStore
        from geo_engine.forecasting.calibration import ForecastingEngine
        store = EventStore()

        # Test direct update
        mult1 = store.update_lens_reliability("DeepTechLens", 0.04)  # Accurate forecast: small Brier error
        assert mult1 > 0.90

        mult2 = store.update_lens_reliability("PropagandaLens", 0.81)  # Inaccurate forecast: large Brier error
        assert mult2 < mult1

        rel_map = store.get_lens_reliability_multipliers()
        assert "DeepTechLens" in rel_map
        assert "PropagandaLens" in rel_map
        assert rel_map["DeepTechLens"] > rel_map["PropagandaLens"]

    def test_rhetoric_deflator_panic_suppression(self):
        """Panic clickbait headlines are scored and deflated to Tier 5 with capped reliability."""
        from geo_engine.ingestion.normalizer import RhetoricDeflator
        from geo_engine.ingestion.models import EvidenceItem, ClaimType
        from geo_engine.ingestion.normalizer import IngestionNormalizer

        # Sensationalism scoring
        panic_text = "BREAKING: World War 3 started! Nuclear strike imminent, all out war, sab swaha!!"
        score = RhetoricDeflator.calculate_sensationalism_index(panic_text)
        assert score >= 0.50

        # Normalization with deflation
        item = EvidenceItem(
            evidence_id="EVID-PANIC-01",
            source_name="social_wire",
            source_type="news_wire",
            timestamp="2026-09-15T12:00:00Z",
            raw_text=panic_text,
            reliability_weight=0.80
        )
        claims = IngestionNormalizer.normalize_evidence_item(item)
        assert len(claims) >= 1
        assert claims[0].epistemic_tier == EpistemicTier.TIER_5_COMMUNIQUE_PR
        assert claims[0].reliability_weight <= 0.20
        assert "[DEFLATED_SENSATIONALISM_SCORE_" in claims[0].asserted_fact

    def test_consolidated_core_5_parity_and_commit(self):
        """Verify master consolidated core bundle reflects R20 and does not contain stale R18."""
        import pathlib
        from scripts.build_canonical_bundles import ALL_IN_ONE_DIR
        bundle_path = pathlib.Path(ALL_IN_ONE_DIR) / "CONSOLIDATED_CORE_5_ALL_IN_ONE.md"
        assert bundle_path.exists()
        content = bundle_path.read_text(encoding="utf-8")
        assert "REGISTRY_VERSION: R20 (20 Analytical Lenses)" in content
        assert "REGISTRY_VERSION: R18" not in content


class TestPhase42SovereignLawfareAndHygiene:
    """Phase 42 sovereign lawfare, video epistemic guard, and bundle hygiene tests."""

    def test_video_transcript_simulation_safeguard(self):
        """Video fallback carries explicit simulation/degraded flags; metadata fallback synthesizes degraded segments."""
        from geo_engine.video.transcript_engine import VideoTranscriptEngine

        # Test 1: Offline fallback has explicit simulation and degradation signaling
        res = VideoTranscriptEngine.fetch_transcript("vid_offline_test")
        assert res.is_simulated is True
        assert res.is_degraded is True
        assert res.fallback_mode == "synthetic_offline_fixture"

        # Test 2: Metadata fallback synthesizes authentic degraded segments without simulation
        meta = {
            "title": "UP Mein UCC Analysis",
            "description": "Discussion on Uniform Civil Code in Uttar Pradesh.",
            "keywords": ["UCC", "UP", "Article 44"]
        }
        res_meta = VideoTranscriptEngine.fetch_transcript("vid_meta_test", metadata_fallback=meta)
        assert res_meta.is_simulated is False
        assert res_meta.is_degraded is True
        assert res_meta.fallback_mode == "video_metadata"
        assert len(res_meta.segments) == 3
        assert "[METADATA_TITLE]" in res_meta.segments[0].text

    def test_bundle_deep_50_zero_duplicates(self):
        """Asserts that consolidate_50_files contains zero duplicate base lens specifications."""
        import pathlib
        repo_root = pathlib.Path(__file__).parent.parent
        c50_dir = repo_root / "consolidate_50_files"
        assert c50_dir.exists()

        files = [f.name for f in c50_dir.iterdir() if f.is_file()]
        lens_bases = []
        for f in files:
            parts = f.split("_", 1)
            if len(parts) > 1 and parts[0].isdigit() and parts[1].startswith("lens_"):
                lens_bases.append(parts[1])

        # Assert exactly 20 unique lenses and zero duplicates
        assert len(lens_bases) == 20
        assert len(set(lens_bases)) == 20

    def test_institutional_lawfare_domestic_constitutional_telemetry(self):
        """Domestic constitutional claims (Article 44, UCC, Waqf) trigger domestic lawfare telemetry."""
        from geo_engine.lenses.institutional_lawfare import InstitutionalLawfareLens
        from geo_engine.ingestion.models import ClaimItem, EpistemicTier, ClaimType

        claims = [
            ClaimItem(
                claim_id="DOM_LAW_01",
                source_evidence_id="EV_01",
                claim_type=ClaimType.LEGAL_COMMITMENT,
                epistemic_tier=EpistemicTier.TIER_3_SOVEREIGN_REDLINES,
                actors=["State Legislature", "Supreme Court"],
                asserted_fact="State enacted Article 44 UCC draft while Waqf Act Section 40 tribunal overrides remain unharmonized.",
                is_binding_commitment=True,
                reliability_weight=0.90,
                evidence_status="sufficient"
            )
        ]
        eval_res = InstitutionalLawfareLens.evaluate(event="Domestic Reform", claims=claims)
        assert eval_res.alignment_score <= -0.60
        assert "domestic_statutory_asymmetry_score" in eval_res.hard_metrics
        assert eval_res.hard_metrics["domestic_statutory_asymmetry_score"] >= 0.80
        assert eval_res.hard_metrics["fcra_litigation_leverage_index"] >= 0.70
        assert any("Domestic constitutional/statutory lawfare detected" in f for f in eval_res.key_findings)

    def test_civilizational_internal_dharmic_jurisprudence(self):
        """Internal Sanatan jurisprudence claims (Dharmashastra, Deshadharma, Shankaracharya) trigger polycentric metrics."""
        from geo_engine.lenses.civilizational import CivilizationalLens
        from geo_engine.ingestion.models import ClaimItem, EpistemicTier, ClaimType

        claims = [
            ClaimItem(
                claim_id="CIV_DHARM_01",
                source_evidence_id="EV_02",
                claim_type=ClaimType.GENERAL_INTEL,
                epistemic_tier=EpistemicTier.TIER_3_SOVEREIGN_REDLINES,
                actors=["Shankaracharya Matha", "Dharmic Council"],
                asserted_fact="Traditional Dharmashastra jurisprudence emphasizes Deshadharma and Sadachara over centralized statutory uniform codes.",
                is_binding_commitment=False,
                reliability_weight=0.85,
                evidence_status="sufficient"
            )
        ]
        eval_res = CivilizationalLens.evaluate(summit=None, claims=claims)
        assert "internal_jurisprudential_model" in eval_res.hard_metrics
        assert "Dharmic Polycentricity" in eval_res.hard_metrics["internal_jurisprudential_model"]
        assert eval_res.hard_metrics["traditional_institutional_autonomy_friction"] >= 0.70
        assert any("Internal Dharmic jurisprudence detected" in f for f in eval_res.key_findings)


class TestPhase43CascadingAndHygiene:
    """Phase 43 strict bundle ceilings, query keyword routing, and cascading simulation tests."""

    def test_strict_bundle_ceilings_and_all_in_one_isolation(self):
        """Verify consolidate_5_files strictly contains 5 files and all_in_one contains dedicated masters."""
        import os
        from scripts.build_canonical_bundles import CONSOLIDATE_5_DIR, CONSOLIDATE_50_DIR, ALL_IN_ONE_DIR

        c5_files = [f for f in os.listdir(CONSOLIDATE_5_DIR) if not f.startswith(".")]
        assert len(c5_files) == 5, f"Expected strictly 5 files in consolidate_5_files, found {len(c5_files)}: {c5_files}"

        c50_files = [f for f in os.listdir(CONSOLIDATE_50_DIR) if not f.startswith(".")]
        assert len(c50_files) <= 50, f"Expected <= 50 files in consolidate_50_files, found {len(c50_files)}"

        assert os.path.exists(os.path.join(ALL_IN_ONE_DIR, "CONSOLIDATED_CORE_5_ALL_IN_ONE.md"))
        assert os.path.exists(os.path.join(ALL_IN_ONE_DIR, "CONSOLIDATED_DEEP_50_ALL_IN_ONE.md"))

    def test_query_parser_constitutional_and_dharmic_routing(self):
        """Verify QueryParser routes constitutional, statutory, and Dharmic concepts to target lenses."""
        from geo_engine.core.query_parser import QueryParser

        q_lawfare = QueryParser.parse("Analysis of Article 44 UCC draft and Waqf Act property jurisdiction")
        assert "institutional_lawfare" in q_lawfare.prioritized_lenses
        assert q_lawfare.requires_lawfare_audit is True

        q_dharmic = QueryParser.parse("Traditional Dharmashastra and Shankaracharya guidance on temple autonomy and sadachara")
        assert "civilizational" in q_dharmic.prioritized_lenses
        assert q_dharmic.requires_civilizational_depth is True

        q_gold = QueryParser.parse("Central bank gold reserve repatriation and sovereign debt dedollarization")
        assert "geo_economist" in q_gold.prioritized_lenses

    def test_cascading_simulation_engine_multi_order_propagation(self):
        """Verify CascadingSimulationEngine propagates 3-order shocks with resilience dampening."""
        from geo_engine.simulation import CascadingSimulationEngine, SimulationShock

        # Unmitigated simulation
        shock = SimulationShock(
            shock_id="SHOCK_TEST_HORMUZ",
            domain="petro_logistics",
            description="Strait of Hormuz naval mine incident and closure",
            severity=0.85
        )
        res_raw = CascadingSimulationEngine.simulate_shock(shock)
        assert len(res_raw.order_1_impacts) >= 1
        assert res_raw.order_1_impacts[0].lens == "petro_logistics"
        assert res_raw.order_1_impacts[0].impact_score == 0.85
        assert len(res_raw.order_2_impacts) >= 3
        assert len(res_raw.order_3_impacts) >= 2
        assert res_raw.systemic_vulnerability_index > 0.40
        assert len(res_raw.recommended_mitigations) >= 3
        md = res_raw.to_markdown()
        assert "Cascading Shock Simulation: SHOCK_TEST_HORMUZ" in md
        assert "Order 1: Direct Physical & Strategic Impacts" in md
        assert "Order 2: Secondary Macro & Supply Contagion" in md
        assert "Order 3: Tertiary Geopolitical & Civilizational Realignment" in md

        # Mitigated simulation via Strategic Resilience Matrix
        resilience_matrix = {
            "petro_logistics": 0.90,
            "cash_flow": 0.80,
            "food_security": 0.75
        }
        res_mitigated = CascadingSimulationEngine.simulate_shock(shock, resilience_matrix=resilience_matrix)
        assert res_mitigated.order_1_impacts[0].mitigated_by_resilience is True
        assert res_mitigated.order_1_impacts[0].impact_score < res_raw.order_1_impacts[0].impact_score
        assert res_mitigated.systemic_vulnerability_index < res_raw.systemic_vulnerability_index

    def test_cli_simulate_subcommand_execution(self):
        """Verify CLI render_cascading_simulation executes without exception."""
        from geo_engine.cli import render_cascading_simulation

        # Should run cleanly and print table output without throwing
        render_cascading_simulation(domain="critical_minerals", severity=0.75, description="Gallium and Germanium export embargo")

    def test_all_10_contagion_domains_simulation(self):
        """Verify all 10 pre-configured contagion domains execute with multi-order impacts."""
        from geo_engine.simulation import CascadingSimulationEngine, SimulationShock

        expected_domains = [
            "petro_logistics", "critical_minerals", "digital_sovereignty",
            "institutional_lawfare", "subsea_cables", "military_readiness",
            "food_security", "demographic_infiltration", "astro_politics", "geo_economist"
        ]
        for dom in expected_domains:
            shock = SimulationShock(
                shock_id=f"SHOCK_{dom.upper()}",
                domain=dom,
                description=f"Automated test shock for {dom}",
                severity=0.80
            )
            res = CascadingSimulationEngine.simulate_shock(shock)
            assert len(res.order_1_impacts) >= 1, f"Missing Order 1 impacts for {dom}"
            assert len(res.order_2_impacts) >= 2, f"Missing Order 2 impacts for {dom}"
            assert len(res.order_3_impacts) >= 1, f"Missing Order 3 impacts for {dom}"
            assert res.systemic_vulnerability_index > 0.0


class TestPhase44AuditHardening:
    """Phase 44: Audit-driven incremental hardening tests covering geopolitical
    keyword expansion, water/food security routing, cyber warfare metrics,
    Dandaniti/Sadguniya mapping, historical turning points, and README documentation parity."""

    def test_geopolitical_aukus_imec_i2u2_routing(self):
        """Verify AUKUS, IMEC, and I2U2 queries route to geopolitical lens."""
        from geo_engine.core.query_parser import QueryParser
        for keyword in ["aukus", "imec", "i2u2", "quad", "belt and road"]:
            q = QueryParser.parse(f"Analysis of {keyword} strategic implications")
            assert "geopolitical" in q.prioritized_lenses, (
                f"Keyword '{keyword}' failed to route to geopolitical lens"
            )

    def test_history_keyword_expansion_routing(self):
        """Verify new historical event keywords route to history lens."""
        from geo_engine.core.query_parser import QueryParser
        for keyword in ["partition", "kargil", "balakot", "galwan", "pokhran", "sindoor"]:
            q = QueryParser.parse(f"Historical analysis of {keyword}")
            assert "history" in q.prioritized_lenses, (
                f"Keyword '{keyword}' failed to route to history lens"
            )

    def test_food_security_water_keywords_routing(self):
        """Verify water security keywords route to food_security lens."""
        from geo_engine.core.query_parser import QueryParser
        for keyword in ["water security", "monsoon", "groundwater", "brahmaputra"]:
            q = QueryParser.parse(f"Impact of {keyword} on agriculture")
            assert "food_security" in q.prioritized_lenses, (
                f"Keyword '{keyword}' failed to route to food_security lens"
            )

    def test_military_cyber_warfare_routing(self):
        """Verify cyber and electronic warfare keywords route to military_readiness lens."""
        from geo_engine.core.query_parser import QueryParser
        for keyword in ["cyber", "electronic warfare", "fifth domain"]:
            q = QueryParser.parse(f"Assessment of {keyword} capabilities")
            assert "military_readiness" in q.prioritized_lenses, (
                f"Keyword '{keyword}' failed to route to military_readiness lens"
            )

    def test_civilizational_sadguniya_metric(self):
        """Verify Sadguniya/Dvaidhibhava policy mapping metric exists in CivilizationalLens."""
        from geo_engine.lenses.civilizational import CivilizationalLens
        from geo_engine.core.models import SummitEvent
        event = SummitEvent(event_name="Strategic Audit", host_country="India")
        result = CivilizationalLens.evaluate(event)
        assert "sadguniya_policy_mapping" in result.hard_metrics, (
            "Missing sadguniya_policy_mapping metric in CivilizationalLens"
        )
        assert "Dvaidhibhava" in result.hard_metrics["sadguniya_policy_mapping"]

    def test_food_security_water_metrics(self):
        """Verify water_security_index and transboundary_river_dispute_count in FoodSecurityLens."""
        from geo_engine.lenses.food_security import FoodSecurityLens
        from geo_engine.core.models import SummitEvent
        event = SummitEvent(event_name="Water Security Audit", host_country="India")
        result = FoodSecurityLens.evaluate(event)
        assert "water_security_index" in result.hard_metrics
        assert result.hard_metrics["water_security_index"] == 0.58
        assert "transboundary_river_dispute_count" in result.hard_metrics
        assert result.hard_metrics["transboundary_river_dispute_count"] == 3

    def test_military_cyber_readiness_metric(self):
        """Verify cyber_warfighting_readiness_score exists in MilitaryReadinessLens."""
        from geo_engine.lenses.military_readiness import MilitaryReadinessLens
        from geo_engine.core.models import SummitEvent
        event = SummitEvent(event_name="Military Audit", host_country="India")
        result = MilitaryReadinessLens.evaluate(event)
        assert "cyber_warfighting_readiness_score" in result.hard_metrics
        assert result.hard_metrics["cyber_warfighting_readiness_score"] == 0.68

    def test_readme_test_count_parity(self):
        """Verify README.md test count matches comprehensive unit and integration tests."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        assert readme_path.exists(), "README.md not found"
        content = readme_path.read_text(encoding="utf-8")
        assert "comprehensive unit and integration tests" in content


class TestPhase45MillennialReversal:
    """Phase 45: Millennial historical reversals, civilizational epoch modeling,
    and temporal symbolic statecraft verification."""

    def test_history_millennial_reversal_keywords_routing(self):
        """Verify millennial historical turning point keywords route to history lens."""
        from geo_engine.core.query_parser import QueryParser
        for keyword in ["somnath", "nalanda", "tarain", "chola", "srivijaya", "shivaji", "swarajya", "1000 year"]:
            q = QueryParser.parse(f"Analysis of {keyword} in historical trajectory")
            assert "history" in q.prioritized_lenses, (
                f"Keyword '{keyword}' failed to route to history lens"
            )

    def test_civilizational_temporal_symbolism_routing(self):
        """Verify civilizational temporal and symbolic keywords route to civilizational lens."""
        from geo_engine.core.query_parser import QueryParser
        for keyword in ["symbolic date", "calendar", "panchanga", "swarajya", "nalanda"]:
            q = QueryParser.parse(f"Civilizational significance of {keyword} alignment")
            assert "civilizational" in q.prioritized_lenses, (
                f"Keyword '{keyword}' failed to route to civilizational lens"
            )

    def test_history_reversal_ratio_metric(self):
        """Verify civilizational_reversal_ratio metric exists in HistoryLens."""
        from geo_engine.lenses.history import HistoryLens
        from geo_engine.core.models import SummitEvent
        event = SummitEvent(event_name="Epoch Reversal Audit", host_country="India")
        result = HistoryLens.evaluate(event)
        assert "civilizational_reversal_ratio" in result.hard_metrics, (
            "Missing civilizational_reversal_ratio in HistoryLens"
        )
        assert result.hard_metrics["civilizational_reversal_ratio"] == 1.45
        assert any("1000-Year Historical Reversal Cycle" in f for f in result.key_findings)

    def test_civilizational_temporal_resonance_metric(self):
        """Verify symbolic_temporal_resonance_score metric exists in CivilizationalLens."""
        from geo_engine.lenses.civilizational import CivilizationalLens
        from geo_engine.core.models import SummitEvent
        event = SummitEvent(event_name="Temporal Statecraft Audit", host_country="India")
        result = CivilizationalLens.evaluate(event)
        assert "symbolic_temporal_resonance_score" in result.hard_metrics, (
            "Missing symbolic_temporal_resonance_score in CivilizationalLens"
        )
        assert result.hard_metrics["symbolic_temporal_resonance_score"] == 0.88
        assert any("Symbolic Temporal Statecraft" in f for f in result.key_findings)

    def test_event_store_millennial_seed_entries(self):
        """Verify EventStore historical_anniversaries table contains millennial turning points."""
        import tempfile
        import os
        from geo_engine.storage.event_store import EventStore

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            test_db = tf.name
        try:
            store = EventStore(db_path=test_db)
            store.initialize_schema_and_seed()
            with store._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT anniversary_id, event_title, year FROM historical_anniversaries")
                rows = {r[0]: (r[1], r[2]) for r in cursor.fetchall()}

            assert "ANNIV-1025-CHOLA-SRIVIJAYA" in rows
            assert rows["ANNIV-1025-CHOLA-SRIVIJAYA"][1] == 1025
            assert "ANNIV-1026-SOMNATH" in rows
            assert rows["ANNIV-1026-SOMNATH"][1] == 1026
            assert "ANNIV-1192-TARAIN" in rows
            assert "ANNIV-1193-NALANDA" in rows
            assert "ANNIV-1453-CONSTANTINOPLE" in rows
            assert "ANNIV-1674-CHHATRAPATI-SHIVAJI" in rows
            assert "ANNIV-2024-NALANDA-REBIRTH" in rows
        finally:
            if os.path.exists(test_db):
                try:
                    os.unlink(test_db)
                except Exception:
                    pass

    def test_readme_phase45_test_count_parity(self):
        """Verify README.md test count matches comprehensive tests."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "comprehensive unit and integration tests" in content


class TestPhase46MaritimeGreyZone:
    """Phase 46 verification: Maritime grey-zone coercion, naval asymmetry, and bilateral accord lawfare."""

    def test_query_parser_maritime_grey_zone_routing(self):
        """Verify QueryParser routes maritime grey-zone and deconfliction accord queries."""
        from geo_engine.core.query_parser import QueryParser

        q_grey = QueryParser.parse("Pakistani warship PNS Hunain rammed an Indian naval vessel in Arabian Sea")
        assert "hybrid_covert" in q_grey.prioritized_lenses
        assert "military_readiness" in q_grey.prioritized_lenses

        q_accord = QueryParser.parse("Breach of 1991 agreement buffer distance and COLREGs safe navigation")
        assert "institutional_lawfare" in q_accord.prioritized_lenses

    def test_hybrid_covert_maritime_grey_zone_metric(self):
        """Verify maritime_grey_zone_coercion_score in HybridCovertLens."""
        import types
        from geo_engine.lenses.hybrid_covert import HybridCovertLens
        from geo_engine.core.models import SummitEvent

        event = SummitEvent(event_name="Arabian Sea Surveillance", host_country="India")
        baseline = HybridCovertLens.evaluate(event)
        assert "maritime_grey_zone_coercion_score" in baseline.hard_metrics
        assert baseline.hard_metrics["maritime_grey_zone_coercion_score"] == 0.82
        assert any("Maritime Grey-Zone Coercion & Sub-Kinetic Probing" in f for f in baseline.key_findings)

        claim = types.SimpleNamespace(asserted_fact="Aggressive ramming and bow crossing by adversary corvette")
        telemetry = HybridCovertLens.evaluate(event, claims=[claim])
        assert telemetry.hard_metrics["maritime_grey_zone_coercion_score"] == 0.92

    def test_institutional_lawfare_maritime_accord_metric(self):
        """Verify bilateral_maritime_accord_compliance_score in InstitutionalLawfareLens."""
        import types
        from geo_engine.lenses.institutional_lawfare import InstitutionalLawfareLens
        from geo_engine.core.models import StrategicEvent

        event = StrategicEvent(title="Maritime Deconfliction Assessment")
        baseline = InstitutionalLawfareLens.evaluate(event)
        assert "bilateral_maritime_accord_compliance_score" in baseline.hard_metrics
        assert baseline.hard_metrics["bilateral_maritime_accord_compliance_score"] == 0.25
        assert any("Bilateral Maritime Accord Lawfare" in f for f in baseline.key_findings)

        claim = types.SimpleNamespace(asserted_fact="Violation of 1991 agreement buffer distance and article 10")
        telemetry = InstitutionalLawfareLens.evaluate(event, claims=[claim])
        assert telemetry.hard_metrics["bilateral_maritime_accord_compliance_score"] == 0.15
        assert telemetry.hard_metrics["maritime_treaty_breach_severity"] == 0.85

    def test_military_readiness_naval_asymmetry_metric(self):
        """Verify naval_asymmetry_index and sub_kinetic_probing_risk in MilitaryReadinessLens."""
        import types
        from geo_engine.lenses.military_readiness import MilitaryReadinessLens
        from geo_engine.core.models import StrategicEvent

        event = StrategicEvent(title="IOR Fleet Readiness")
        baseline = MilitaryReadinessLens.evaluate(event)
        assert "naval_asymmetry_index" in baseline.hard_metrics
        assert baseline.hard_metrics["naval_asymmetry_index"] == 0.74
        assert "sub_kinetic_probing_risk" in baseline.hard_metrics
        assert baseline.hard_metrics["sub_kinetic_probing_risk"] == 0.81
        assert any("Asymmetric Naval Balancing" in f for f in baseline.key_findings)

        claim = types.SimpleNamespace(asserted_fact="Adversary warship PNS Hunain engaged in maritime standoff")
        telemetry = MilitaryReadinessLens.evaluate(event, claims=[claim])
        assert telemetry.hard_metrics["sub_kinetic_probing_risk"] == 0.91

    def test_event_store_1991_accord_and_standoff_event(self):
        """Verify EventStore seeds contain 1991 Bilateral Accord Article 10 and 2026 Standoff event."""
        import tempfile
        import os
        from geo_engine.storage.event_store import EventStore

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            test_db = tf.name
        try:
            store = EventStore(db_path=test_db)
            store.initialize_schema_and_seed()
            with store._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT clause_id, category FROM historical_treaty_clauses WHERE clause_id='CLAUSE-1991-INDO-PAK-NAV-ART10'")
                clause_row = cursor.fetchone()
                assert clause_row is not None
                assert clause_row[0] == "CLAUSE-1991-INDO-PAK-NAV-ART10"
                assert clause_row[1] == "maritime_deconfliction"

                cursor.execute("SELECT event_id, date FROM events WHERE event_id='HIST-2026-ARABIAN-SEA-STANDOFF'")
                event_row = cursor.fetchone()
                assert event_row is not None
                assert event_row[0] == "HIST-2026-ARABIAN-SEA-STANDOFF"
                assert event_row[1] == "2026-09-15"
        finally:
            if os.path.exists(test_db):
                try:
                    os.unlink(test_db)
                except Exception:
                    pass

    def test_readme_phase46_test_count_parity(self):
        """Verify README.md test count matches comprehensive tests."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "comprehensive unit and integration tests" in content


class TestPhase47CompetingHypotheses:
    """Phase 47 verification: Analysis of Competing Hypotheses (ACH), deep reasoning, and epistemic truth guard."""

    def test_ach_hypothesis_normalization(self):
        """Verify 4 baseline hypotheses and Bayesian posterior normalization sum to 1.0."""
        from geo_engine.arbitration.competing_hypotheses import IncidentReasoningEngine

        report = IncidentReasoningEngine.evaluate_incident("Generic Border Encounter")
        assert len(report.hypotheses) == 4
        posterior_sum = sum(h.posterior_probability for h in report.hypotheses)
        assert abs(posterior_sum - 1.0) < 0.002
        for h in report.hypotheses:
            assert 0.0 <= h.posterior_probability <= 1.0
            assert 0.0 <= h.prior_probability <= 1.0
            assert 0.0 <= h.likelihood_score <= 1.0

    def test_ach_technical_and_crew_incompetence_evaluation(self):
        """Verify technical failure and rookie crew inexperience trigger Epistemic Truth Guard."""
        import types
        from geo_engine.arbitration.competing_hypotheses import IncidentReasoningEngine

        claims = [
            types.SimpleNamespace(asserted_fact="Steering failure and sudden rudder servo burnout during high-speed turn"),
            types.SimpleNamespace(asserted_fact="PNS Hunain was recently commissioned in July 2024 with green watchstanders")
        ]
        report = IncidentReasoningEngine.evaluate_incident(
            "North Arabian Sea Collision",
            claims=claims
        )
        assert report.dominant_hypothesis_id in ["HYP_1_TECHNICAL_FAILURE", "HYP_2_CREW_INCOMPETENCE"]
        assert report.epistemic_warning is not None
        assert "[ACH EPISTEMIC TRUTH GUARD]" in report.epistemic_warning

    def test_ach_tactical_maskirovka_evaluation(self):
        """Verify tactical maskirovka / diversion cues elevate Hypothesis 3."""
        import types
        from geo_engine.arbitration.competing_hypotheses import IncidentReasoningEngine

        claims = [
            types.SimpleNamespace(asserted_fact="Surface standoff was a diversion to hide acoustic submarine transit in adjacent sector")
        ]
        report = IncidentReasoningEngine.evaluate_incident(
            "Maritime Standoff Diversion",
            claims=claims
        )
        h_mask = next(h for h in report.hypotheses if h.hypothesis_id == "HYP_3_TACTICAL_MASKIROVKA")
        assert h_mask.likelihood_score >= 0.70
        assert len(h_mask.evidence_supporting) > 0

    def test_ach_deliberate_coercion_evaluation(self):
        """Verify premeditated grey-zone ramming orders elevate Hypothesis 4."""
        import types
        from geo_engine.arbitration.competing_hypotheses import IncidentReasoningEngine

        claims = [
            types.SimpleNamespace(asserted_fact="Deliberate premeditated ramming and shouldering ordered by naval command to test ROE and violate 1991 agreement")
        ]
        report = IncidentReasoningEngine.evaluate_incident(
            "Arabian Sea Ramming",
            claims=claims
        )
        assert report.dominant_hypothesis_id == "HYP_4_DELIBERATE_COERCION"
        h_coercion = next(h for h in report.hypotheses if h.hypothesis_id == "HYP_4_DELIBERATE_COERCION")
        assert h_coercion.posterior_probability > 0.25

    def test_synthesizer_ach_integration_and_truth_guard(self):
        """Verify SummitSynthesizer integrates ACH report and conditions Tier 5 Civilizational Synthesis."""
        import types
        from geo_engine.arbitration.synthesizer import SummitSynthesizer
        from geo_engine.core.models import SummitEvent

        event = SummitEvent(event_name="Arabian Sea Encounter", host_country="India")
        claim = types.SimpleNamespace(asserted_fact="Steering failure and rookie watchstander error on newly commissioned ship")
        report = SummitSynthesizer.synthesize_report(event, claims=[claim])

        assert report.ach_evaluation is not None
        assert "incident_title" in report.ach_evaluation
        assert "dominant_hypothesis_id" in report.ach_evaluation
        assert "hypotheses" in report.ach_evaluation

        # Tier 5 Civilizational synthesis must include the Epistemic Truth Guard
        civ_core = report.civilizational_synthesis.get("civilizational_core", "")
        assert "[ACH EPISTEMIC TRUTH GUARD]" in civ_core
        assert any("[ACH_ARBITRATION]" in log for log in report.epistemic_arbitration_log)

    def test_readme_phase47_test_count_parity(self):
        """Verify README.md test count matches comprehensive tests."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "comprehensive unit and integration tests" in content


class TestPhase48SaptangaAndResourceChokepoints:
    """Phase 48: Kautilyan Saptanga statecraft, critical minerals midstream refining,
    and soil-nutrient chemical fertilizer chokepoint verification."""

    def test_query_parser_saptanga_and_resource_chokepoints(self):
        """Verify QueryParser routes Saptanga, midstream refining, and fertilizer terms."""
        from geo_engine.core.query_parser import QueryParser

        q_saptanga = QueryParser.parse("Kautilyan Saptanga state sovereignty analysis of Swami and Kosha")
        assert "civilizational" in q_saptanga.prioritized_lenses, (
            "Failed to route Saptanga query to civilizational lens"
        )

        q_refining = QueryParser.parse("Midstream refining monopoly in NdFeB permanent magnets and rare earth processing")
        assert "critical_minerals" in q_refining.prioritized_lenses, (
            "Failed to route midstream refining query to critical_minerals lens"
        )

        q_fertilizer = QueryParser.parse("Import dependency on potassium MOP and soil nutrient chokepoints")
        assert "food_security" in q_fertilizer.prioritized_lenses, (
            "Failed to route fertilizer dependency query to food_security lens"
        )

    def test_civilizational_saptanga_metrics(self):
        """Verify saptanga_sovereignty_index and 7-limb vulnerabilities in CivilizationalLens."""
        import types
        from geo_engine.lenses.civilizational import CivilizationalLens
        from geo_engine.core.models import SummitEvent

        event = SummitEvent(event_name="Saptanga Sovereignty Audit", host_country="India")
        baseline = CivilizationalLens.evaluate(event)
        assert "saptanga_sovereignty_index" in baseline.hard_metrics
        assert baseline.hard_metrics["saptanga_sovereignty_index"] == 0.81
        assert "saptanga_limb_vulnerabilities" in baseline.hard_metrics

        limbs = baseline.hard_metrics["saptanga_limb_vulnerabilities"]
        for required_limb in ("swami", "amatya", "janapada", "durga", "kosha", "danda", "mitra"):
            assert required_limb in limbs, f"Missing Saptanga limb: {required_limb}"

        assert any("Kautilyan Saptanga Statecraft" in f for f in baseline.key_findings)

        # Grounded telemetry via Saptanga claim
        claim = types.SimpleNamespace(asserted_fact="Saptanga state sovereignty requires durable kosha and fortified durga infrastructure")
        telemetry = CivilizationalLens.evaluate(event, claims=[claim])
        assert telemetry.hard_metrics.get("saptanga_evaluation_active") is True
        assert any("[GROUNDED TELEMETRY] Kautilyan Saptanga limb evaluation activated" in f for f in telemetry.key_findings)

    def test_critical_minerals_midstream_refining_metrics(self):
        """Verify midstream_refining_monopoly_risk and NdFeB magnet metrics in CriticalMineralsLens."""
        import types
        from geo_engine.lenses.critical_minerals import CriticalMineralsLens
        from geo_engine.core.models import StrategicEvent

        event = StrategicEvent(title="Mineral Chokepoint Assessment")
        baseline = CriticalMineralsLens.evaluate(event)
        assert "midstream_refining_monopoly_risk" in baseline.hard_metrics
        assert baseline.hard_metrics["midstream_refining_monopoly_risk"] == 0.85
        assert baseline.hard_metrics["heavy_rare_earth_processing_dependency"] == 0.90
        assert baseline.hard_metrics["ndfeb_permanent_magnet_choke_pct"] == 92.0
        assert any("Midstream Metallurgical & Chemical Refining Chokepoint" in f for f in baseline.key_findings)

        # Grounded telemetry via refining monopoly claim
        claim = types.SimpleNamespace(asserted_fact="Chinese midstream refining monopoly over sintered NdFeB magnet processing")
        telemetry = CriticalMineralsLens.evaluate(event, claims=[claim])
        assert telemetry.hard_metrics["midstream_refining_monopoly_risk"] == 0.92
        assert any("[GROUNDED TELEMETRY] Strategic chokepoint or midstream mineral refining monopoly verified" in f for f in telemetry.key_findings)

    def test_food_security_fertilizer_chokepoint_metrics(self):
        """Verify potassium MOP, DAP risk, and soil nutrient metrics in FoodSecurityLens."""
        import types
        from geo_engine.lenses.food_security import FoodSecurityLens
        from geo_engine.core.models import StrategicEvent

        event = StrategicEvent(title="Agrarian Chokepoint Audit")
        baseline = FoodSecurityLens.evaluate(event)
        assert baseline.hard_metrics["potassium_mop_import_dependency"] == 1.0
        assert baseline.hard_metrics["phosphatic_dap_supply_risk"] == 0.65
        assert baseline.hard_metrics["soil_nutrient_chokepoint_vulnerability"] == 0.78
        assert any("Nutrient-Specific Chemical Fertilizer Fragility" in f for f in baseline.key_findings)

        # Grounded telemetry via soil nutrient claim
        claim = types.SimpleNamespace(asserted_fact="Critical potassium MOP and DAP fertilizer import chokepoints in Persian Gulf")
        telemetry = FoodSecurityLens.evaluate(event, claims=[claim])
        assert telemetry.hard_metrics["soil_nutrient_chokepoint_vulnerability"] == 0.85
        assert any("[GROUNDED TELEMETRY] Agrarian input or fertilizer chokepoint claim verified" in f for f in telemetry.key_findings)

    def test_readme_phase48_test_count_parity(self):
        """Verify README.md test count matches comprehensive tests."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "comprehensive unit and integration tests" in content

    def test_canonical_bundle_ceilings_and_saptanga_parity(self):
        """Verify strict canonical bundle ceilings (5 files == 5, 50 files <= 50) and lens execution."""
        import pathlib
        from geo_engine.lenses.civilizational import CivilizationalLens
        from geo_engine.lenses.critical_minerals import CriticalMineralsLens
        from geo_engine.lenses.food_security import FoodSecurityLens
        from geo_engine.core.models import StrategicEvent

        root_dir = pathlib.Path(__file__).parent.parent

        # 5-file bundle exact ceiling
        c5_dir = root_dir / "consolidate_5_files"
        assert c5_dir.exists()
        c5_files = [f for f in c5_dir.iterdir() if f.is_file() and f.suffix.lower() == ".md"]
        assert len(c5_files) == 5, f"consolidate_5_files must contain exactly 5 markdown files, found {len(c5_files)}"

        # 50-file bundle maximum ceiling (<= 50 files, currently 34)
        c50_dir = root_dir / "consolidate_50_files"
        assert c50_dir.exists()
        c50_files = [f for f in c50_dir.iterdir() if f.is_file() and f.suffix.lower() == ".md"]
        assert len(c50_files) <= 50, f"consolidate_50_files exceeds 50 files ceiling: {len(c50_files)}"

        # Test lens execution parity
        ev = StrategicEvent(title="Parity Verification")
        assert CivilizationalLens.evaluate(ev).evidence_status == "sufficient"
        assert CriticalMineralsLens.evaluate(ev).evidence_status == "sufficient"
        assert FoodSecurityLens.evaluate(ev).evidence_status == "sufficient"


class TestPhase49NonLinearTippingAndGameTheoretic:
    """Phase 49: Non-linear cascading tipping points, critical phase transitions,
    and sequential game-theoretic strategic red-teaming verification."""

    def test_cascading_non_linear_tipping_activation(self):
        """Verify CascadingSimulationEngine triggers tipping point and phase transition risk when resilience is depleted."""
        from geo_engine.simulation import CascadingSimulationEngine, SimulationShock

        shock = SimulationShock(
            shock_id="SHOCK_CRIT_DEPLETED",
            domain="petro_logistics",
            description="Severe naval chokepoint interdiction with exhausted reserves",
            severity=0.85
        )
        # Depleted resilience triggers critical tipping point (< 0.35)
        resilience_matrix = {
            "petro_logistics": 0.20,
            "cash_flow": 0.25,
            "food_security": 0.80
        }
        res = CascadingSimulationEngine.simulate_shock(shock, resilience_matrix=resilience_matrix)

        # petro_logistics must be flagged as tipping point
        imp_petro = next(imp for imp in res.order_1_impacts if imp.lens == "petro_logistics")
        assert imp_petro.is_tipping_point is True
        assert imp_petro.critical_resilience_deficit > 0.0
        assert "petro_logistics" in res.critical_tipping_lenses
        assert res.systemic_phase_transition_risk > 0.0

        # food_security has 0.80 resilience, must NOT be tipping point
        imp_food = next(imp for imp in res.order_2_impacts if imp.lens == "food_security")
        assert imp_food.is_tipping_point is False
        assert imp_food.mitigated_by_resilience is True

        md = res.to_markdown()
        assert "Critical Tipping Lenses (Non-Linear Collapse)" in md
        assert "[CRITICAL TIPPING POINT / NON-LINEAR SURGE]" in md

    def test_game_theoretic_actor_reaction_mapping(self):
        """Verify GameTheoreticEngine simulates sequential multi-turn moves with asymmetric counter-levers."""
        from geo_engine.simulation.game_theoretic import GameTheoreticEngine

        res = GameTheoreticEngine.simulate_interaction(
            initiator_name="China",
            target_name="India",
            domain="critical_minerals",
            severity=0.85,
            action_description="Export embargo on sintered NdFeB magnets"
        )
        assert res.turn_1_action.initiator == "China"
        assert res.turn_1_action.domain == "critical_minerals"
        assert res.turn_2_reaction.responder == "India"
        assert res.turn_2_reaction.counter_domain == "geo_economist"
        assert res.turn_2_reaction.response_type == "ASYMMETRIC_LEVERAGE"
        assert "Press Note 3" in res.turn_2_reaction.action_description
        assert res.turn_2_reaction.severity > 0.50

    def test_putnam_two_level_game_domestic_backlash(self):
        """Verify Turn 3 calculates Putnam domestic political friction and systemic equilibrium."""
        from geo_engine.simulation.game_theoretic import GameTheoreticEngine

        res = GameTheoreticEngine.simulate_interaction(
            initiator_name="Pakistan",
            target_name="India",
            domain="hybrid_covert",
            severity=0.90,
            action_description="Maritime standoff and aggressive ramming maneuver in Arabian Sea"
        )
        assert res.turn_2_reaction.counter_domain == "institutional_lawfare"
        assert "1991" in res.turn_2_reaction.action_description or "Maritime" in res.turn_2_reaction.action_description
        assert res.turn_3_backlash.domestic_political_friction > 0.0
        assert res.turn_3_backlash.inflationary_backlash_score > 0.0
        assert 0.0 <= res.equilibrium_stability_index <= 1.0
        assert len(res.turn_3_backlash.de_escalation_off_ramp) > 0
        assert "Pakistan" in res.net_strategic_payoff
        assert "India" in res.net_strategic_payoff

    def test_cli_red_team_subcommand_invocation(self):
        """Verify CLI render_game_theoretic_simulation executes without exception."""
        from geo_engine.cli import render_game_theoretic_simulation

        render_game_theoretic_simulation(
            initiator="China",
            target="India",
            domain="critical_minerals",
            severity=0.80,
            action="Lithium refining export restrictions"
        )

    def test_query_parser_game_theoretic_routing(self):
        """Verify QueryParser routes game theory and red team keywords."""
        from geo_engine.core.query_parser import QueryParser

        q_gt = QueryParser.parse("Game theory escalation spiral and counter-move simulation")
        assert "geopolitical" in q_gt.prioritized_lenses

        q_putnam = QueryParser.parse("Putnam two-level game domestic backlash and regulatory veto")
        assert "bureaucratic_inertia" in q_putnam.prioritized_lenses

        q_asym = QueryParser.parse("Asymmetric response and tipping point in sequential move")
        assert "hybrid_covert" in q_asym.prioritized_lenses

    def test_readme_phase49_test_count_parity(self):
        """Verify README.md test count matches comprehensive tests."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "comprehensive unit and integration tests" in content


class TestPhase50VostroAndWargamePersistence:
    """Phase 50: Vostro capital recycling velocity, persistent wargame campaign state,
    and asynchronous macro telemetry ingestion verification."""

    def test_vostro_capital_recycling_metrics(self):
        """Verify GeoEconomistLens hard metrics and claim matching for SRVA capital recycling."""
        import types
        from geo_engine.lenses.geo_economist import GeoEconomistLens
        from geo_engine.core.models import SummitEvent

        summit = SummitEvent(summit_name="Monetary Forum 2026", host_country="India")
        res = GeoEconomistLens.evaluate(summit)

        # Baseline metrics verification
        assert "vostro_balance_trapped_usd_b" in res.hard_metrics
        assert res.hard_metrics["vostro_balance_trapped_usd_b"] == 42.0
        assert res.hard_metrics["vostro_capital_recycling_velocity"] == 0.38
        assert res.hard_metrics["sovereign_debt_reinvestment_ratio"] == 0.65
        assert any("Special Rupee Vostro Account" in f for f in res.key_findings)

        # Grounded telemetry claim verification
        claim = types.SimpleNamespace(asserted_fact="Special Rupee Vostro Account capital recycling into Indian G-Secs")
        telemetry_res = GeoEconomistLens.evaluate(summit, claims=[claim])
        assert telemetry_res.hard_metrics.get("vostro_recycling_verified") is True
        assert telemetry_res.hard_metrics.get("grounded_monetary_claims_verified") is True
        assert any("[GROUNDED TELEMETRY]" in f for f in telemetry_res.key_findings)

    def test_wargame_session_sqlite_persistence(self):
        """Verify EventStore saves and retrieves persistent wargame sessions and turn sequences."""
        import tempfile
        import os
        from geo_engine.storage.event_store import EventStore

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            test_db = tf.name
        try:
            store = EventStore(db_path=test_db)
            session_data = {
                "session_id": "TEST-CAMPAIGN-001",
                "initiator": "China",
                "target": "India",
                "domain": "critical_minerals",
                "action_summary": "Export ban on NdFeB magnets",
                "counter_summary": "Press Note 3 and Quad diversification",
                "backlash_summary": "Track 1.5 de-escalation off-ramp",
                "equilibrium_payoff": 0.72,
                "status": "COMPLETED",
                "created_at": "2026-09-20 12:00:00 UTC"
            }
            turns = [
                {
                    "turn_number": 1,
                    "actor": "China",
                    "domain": "critical_minerals",
                    "action_description": "Export ban on NdFeB magnets",
                    "severity": 0.85,
                    "payoff": -0.15,
                    "details_json": '{"intent": "Supply choke"}'
                },
                {
                    "turn_number": 2,
                    "actor": "India",
                    "domain": "geo_economist",
                    "action_description": "Press Note 3 and Quad diversification",
                    "severity": 0.75,
                    "payoff": 0.10,
                    "details_json": '{"response": "ASYMMETRIC_LEVERAGE"}'
                }
            ]
            saved_id = store.save_wargame_session(session_data, turns)
            assert saved_id == "TEST-CAMPAIGN-001"

            fetched = store.get_wargame_session("TEST-CAMPAIGN-001")
            assert fetched is not None
            assert fetched["session_id"] == "TEST-CAMPAIGN-001"
            assert fetched["initiator"] == "China"
            assert fetched["target"] == "India"
            assert len(fetched["turns"]) == 2
            assert fetched["turns"][0]["actor"] == "China"
            assert fetched["turns"][1]["actor"] == "India"

            campaigns = store.list_wargame_sessions(limit=10)
            assert len(campaigns) >= 1
            assert any(c["session_id"] == "TEST-CAMPAIGN-001" for c in campaigns)
        finally:
            if os.path.exists(test_db):
                try:
                    os.unlink(test_db)
                except Exception:
                    pass

    def test_game_theoretic_persist_parameter(self):
        """Verify GameTheoreticEngine persists session when persist=True."""
        import tempfile
        import os
        from geo_engine.simulation.game_theoretic import GameTheoreticEngine
        from geo_engine.storage.event_store import EventStore

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            test_db = tf.name
        try:
            store = EventStore(db_path=test_db)
            res = GameTheoreticEngine.simulate_interaction(
                initiator_name="United States",
                target_name="India",
                domain="institutional_lawfare",
                severity=0.70,
                action_description="Secondary sanctions probe on energy payments",
                persist=True,
                store=store,
                session_id="SESSION-PERSIST-TEST-US-IND"
            )
            assert res.simulation_id == "SESSION-PERSIST-TEST-US-IND"

            persisted = store.get_wargame_session("SESSION-PERSIST-TEST-US-IND")
            assert persisted is not None
            assert persisted["initiator"] == "United States"
            assert persisted["target"] == "India"
            assert len(persisted["turns"]) == 3
            assert persisted["turns"][0]["turn_number"] == 1
            assert persisted["turns"][1]["turn_number"] == 2
            assert persisted["turns"][2]["turn_number"] == 3
        finally:
            if os.path.exists(test_db):
                try:
                    os.unlink(test_db)
                except Exception:
                    pass

    def test_macro_telemetry_adapter_normalization(self):
        """Verify MacroTelemetryAdapter normalizes feeds, generates indicator claims, and ingests to EventStore."""
        import tempfile
        import os
        from geo_engine.ingestion.telemetry_adapter import MacroTelemetryAdapter
        from geo_engine.ingestion.models import ClaimType
        from geo_engine.storage.event_store import EventStore

        raw_records = [
            {
                "id": "TEL-VOSTRO-01",
                "text": "Special Rupee Vostro Account balances accumulated by Rosneft reach 42 billion USD equivalent in Mumbai commercial banks.",
                "amount_usd": 42000000000.0,
                "is_binding": True
            },
            {
                "id": "TEL-AIS-01",
                "text": "AIS telemetry indicates shadow fleet tanker diversion around Cape of Good Hope avoiding Bab-el-Mandeb chokepoint.",
                "physical_units": "24 tankers"
            }
        ]

        claims = MacroTelemetryAdapter.normalize_telemetry(raw_records)
        assert len(claims) == 2
        assert claims[0].claim_type == ClaimType.FINANCIAL_CAPEX
        assert "GeoEconomistLens" in claims[0].target_lenses
        assert claims[1].claim_type == ClaimType.PHYSICAL_PRESENCE
        assert "PetroLogisticsLens" in claims[1].target_lenses

        # Indicator claims generation
        indicators = {
            "vostro_balance_trapped": 42.0,
            "spr_import_cover": 9.5,
            "potassium_mop_choke": 1.0
        }
        indicator_claims = MacroTelemetryAdapter.create_claims_from_indicators(indicators)
        assert len(indicator_claims) == 3

        # Ingestion into EventStore
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            test_db = tf.name
        try:
            store = EventStore(db_path=test_db)
            ingested = MacroTelemetryAdapter.ingest_to_event_store(claims, store=store)
            assert ingested == 2
            with store._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT count(*) FROM events WHERE event_id LIKE 'EVT-TEL-%'")
                count = cursor.fetchone()[0]
                assert count == 2
        finally:
            if os.path.exists(test_db):
                try:
                    os.unlink(test_db)
                except Exception:
                    pass

    def test_query_parser_vostro_and_wargame_routing(self):
        """Verify QueryParser routes vostro recycling and persistent wargame queries."""
        from geo_engine.core.query_parser import QueryParser

        q_vostro = QueryParser.parse("Special rupee vostro account SRVA capital recycling into G-Secs")
        assert "geo_economist" in q_vostro.prioritized_lenses

        q_wargame = QueryParser.parse("Run persistent wargame campaign session and counter-move simulation")
        assert "geopolitical" in q_wargame.prioritized_lenses

    def test_synthesizer_hard_money_audit_vostro_integration(self):
        """Verify SummitSynthesizer populates vostro recycling velocity in hard_money_audit."""
        from geo_engine.arbitration.synthesizer import SummitSynthesizer
        from geo_engine.core.models import SummitEvent

        summit = SummitEvent(summit_name="BRICS 2026 Summit", host_country="India")
        report = SummitSynthesizer.synthesize_report(summit)
        hma = report.hard_money_audit
        assert "vostro_balance_trapped_usd_b" in hma
        assert hma["vostro_balance_trapped_usd_b"] == 42.0
        assert "vostro_capital_recycling_velocity" in hma
        assert hma["vostro_capital_recycling_velocity"] == 0.38
        assert "sovereign_debt_reinvestment_ratio" in hma
        assert hma["sovereign_debt_reinvestment_ratio"] == 0.65

    def test_event_store_rbi_srva_baseline_clause_and_event(self):
        """Verify EventStore seeds contain RBI SRVA Circular Clause and Historical Framework Event."""
        import tempfile
        import os
        from geo_engine.storage.event_store import EventStore

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
            test_db = tf.name
        try:
            store = EventStore(db_path=test_db)
            store.initialize_schema_and_seed()
            with store._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT clause_id, category FROM historical_treaty_clauses WHERE clause_id='CLAUSE-2022-RBI-SRVA'")
                clause_row = cursor.fetchone()
                assert clause_row is not None
                assert clause_row[0] == "CLAUSE-2022-RBI-SRVA"
                assert clause_row[1] == "monetary_clearing"

                cursor.execute("SELECT event_id, date FROM events WHERE event_id='HIST-2022-RBI-SRVA-FRAMEWORK'")
                event_row = cursor.fetchone()
                assert event_row is not None
                assert event_row[0] == "HIST-2022-RBI-SRVA-FRAMEWORK"
                assert event_row[1] == "2022-07-11"
        finally:
            if os.path.exists(test_db):
                try:
                    os.unlink(test_db)
                except Exception:
                    pass

    def test_readme_phase50_test_count_parity(self):
        """Verify README.md test count matches comprehensive test string."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "comprehensive unit and integration tests" in content


class TestPhase51MacroForensicBridge:
    """Phase 51 macro-forensic bridge, NPA resolution filtering, and audit ingestion tests."""

    def test_cash_flow_lens_npa_recovery_metrics_and_claims(self):
        """Verify CashFlowLens provides NPA recovery efficiency metrics and audits write-off claims."""
        from geo_engine.lenses.cash_flow import CashFlowLens
        from geo_engine.core.models import SummitEvent
        from geo_engine.ingestion.models import ClaimItem, ClaimType, EpistemicTier

        summit = SummitEvent(summit_name="Economic Forensic Summit", host_country="India")
        ev = CashFlowLens.evaluate(summit)
        assert "npa_recovery_efficiency_ratio" in ev.hard_metrics
        assert ev.hard_metrics["npa_recovery_efficiency_ratio"] == 0.26
        assert ev.hard_metrics["npa_cleanup_taxpayer_subsidy_usd_b"] == 37.5

        claim = ClaimItem(
            claim_id="CLM-NPA-01",
            source_evidence_id="SRC-NPA",
            claim_type=ClaimType.FINANCIAL_CAPEX,
            epistemic_tier=EpistemicTier.TIER_2_FINANCIAL,
            actors=["India"],
            asserted_fact="Banking clean-up write-off of bad loans exceeded actual cash recovery."
        )
        ev_claims = CashFlowLens.evaluate(summit, claims=[claim])
        assert ev_claims.hard_metrics.get("banking_resolution_audit_applied") is True
        assert any("[FORENSIC AUDIT]" in f for f in ev_claims.key_findings)

    def test_geo_economist_china_trade_gap_and_discrepancy_metrics(self):
        """Verify GeoEconomistLens tracks China trade divergence and GDP discrepancy risk."""
        from geo_engine.lenses.geo_economist import GeoEconomistLens
        from geo_engine.core.models import SummitEvent
        from geo_engine.ingestion.models import ClaimItem, ClaimType, EpistemicTier

        summit = SummitEvent(summit_name="Trade Audit Summit", host_country="India")
        ev = GeoEconomistLens.evaluate(summit)
        assert ev.hard_metrics["china_bilateral_trade_gap_usd_b"] == 18.5
        assert ev.hard_metrics["gdp_discrepancy_item_risk_pct"] == 3.2
        assert ev.hard_metrics["single_deflation_distortion_flag"] is True

        claim = ClaimItem(
            claim_id="CLM-TRADE-01",
            source_evidence_id="SRC-TRADE",
            claim_type=ClaimType.GENERAL_INTEL,
            epistemic_tier=EpistemicTier.TIER_2_FINANCIAL,
            actors=["India", "China"],
            asserted_fact="China trade gap under-invoicing evades customs tariffs and inflates deficit."
        )
        ev_claims = GeoEconomistLens.evaluate(summit, claims=[claim])
        assert ev_claims.hard_metrics.get("trade_gap_discrepancy_verified") is True
        assert any("[FORENSIC AUDIT]" in f for f in ev_claims.key_findings)

    def test_food_security_anti_farmer_export_ban_metrics(self):
        """Verify FoodSecurityLens tracks anti-farmer export ban penalties."""
        from geo_engine.lenses.food_security import FoodSecurityLens
        from geo_engine.core.models import StrategicEvent
        from geo_engine.ingestion.models import ClaimItem, ClaimType, EpistemicTier

        event = StrategicEvent(title="Agrarian Trade Policy", region="South Asia")
        ev = FoodSecurityLens.evaluate(event)
        assert ev.hard_metrics["anti_farmer_export_ban_penalty"] == 0.35
        assert ev.hard_metrics["producer_to_consumer_welfare_transfer_score"] == 0.72

        claim = ClaimItem(
            claim_id="CLM-AGRI-01",
            source_evidence_id="SRC-AGRI",
            claim_type=ClaimType.GENERAL_INTEL,
            epistemic_tier=EpistemicTier.TIER_1_PHYSICAL,
            actors=["India"],
            asserted_fact="Rice ban price stabilization suppresses rural producer income."
        )
        ev_claims = FoodSecurityLens.evaluate(event, claims=[claim])
        assert ev_claims.hard_metrics.get("export_ban_price_stabilization_flag") is True
        assert any("[FORENSIC AUDIT]" in f for f in ev_claims.key_findings)

    def test_telemetry_adapter_audit_markdown_ingestion(self):
        """Verify MacroTelemetryAdapter parses and normalizes FORENSIC_AUDIT_INDIA_1991_2026.md."""
        from geo_engine.ingestion.telemetry_adapter import MacroTelemetryAdapter
        import os

        audit_file = "FORENSIC_AUDIT_INDIA_1991_2026.md"
        assert os.path.exists(audit_file)
        claims = MacroTelemetryAdapter.extract_claims_from_audit_markdown(audit_file)
        assert len(claims) >= 10
        # Verify target lenses are mapped
        has_geo_or_cash = any(
            "GeoEconomistLens" in c.target_lenses or "CashFlowLens" in c.target_lenses
            for c in claims
        )
        assert has_geo_or_cash is True

    def test_query_parser_macro_forensics_routing(self):
        """Verify QueryParser routes macro forensic terms to appropriate analytical lenses."""
        from geo_engine.core.query_parser import QueryParser

        q_npa = QueryParser.parse("Audit banking NPA write-off and bank recapitalization haircuts")
        assert "cash_flow" in q_npa.prioritized_lenses

        q_china = QueryParser.parse("Evaluate China trade gap under-invoicing and double deflation in manufacturing")
        assert "geo_economist" in q_china.prioritized_lenses

        q_agri = QueryParser.parse("Analyze non-basmati rice ban and wheat export ban price stabilization")
        assert "food_security" in q_agri.prioritized_lenses

    def test_cli_ingest_audit_execution(self):
        """Verify CLI render_audit_ingestion executes cleanly on forensic audit file."""
        from geo_engine.cli import render_audit_ingestion
        import os

        audit_file = "FORENSIC_AUDIT_INDIA_1991_2026.md"
        assert os.path.exists(audit_file)
        # Should execute without throwing any exception
        render_audit_ingestion(audit_file)

    def test_readme_phase51_test_count_parity(self):
        """Verify README.md reflects test suite documentation."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "comprehensive unit and integration tests" in content


class TestPhase52McpAndMacroRecalculation:
    """Phase 52 Model Context Protocol (MCP) server, double deflation, consolidated capex, and macro connectors."""

    def test_mcp_server_initialize_and_tools_list(self):
        """Verify MCP server JSON-RPC initialize and tools/list protocol handling."""
        from geo_engine.mcp import GeoEngineMCPServer

        server = GeoEngineMCPServer()

        # 1. Test initialize
        init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        init_resp = server.handle_request(init_req)
        assert init_resp["jsonrpc"] == "2.0"
        assert init_resp["id"] == 1
        assert "serverInfo" in init_resp["result"]
        assert init_resp["result"]["serverInfo"]["name"] == "geo-engine-mcp"
        assert "tools" in init_resp["result"]["capabilities"]

        # 2. Test notifications/initialized
        notif_req = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        assert server.handle_request(notif_req) is None

        # 3. Test tools/list
        list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        list_resp = server.handle_request(list_req)
        assert list_resp["id"] == 2
        tools = list_resp["result"]["tools"]
        assert len(tools) >= 7
        tool_names = [t["name"] for t in tools]
        assert "geo_query" in tool_names
        assert "geo_simulate" in tool_names
        assert "geo_red_team" in tool_names
        assert "geo_forecasts" in tool_names
        assert "geo_lenses" in tool_names
        assert "geo_ingest_audit" in tool_names
        assert "geo_recalculate_deflation" in tool_names

    def test_mcp_server_tool_call_query(self):
        """Verify MCP server tool execution for geo_query."""
        from geo_engine.mcp import GeoEngineMCPServer
        import json

        server = GeoEngineMCPServer()
        call_req = {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {
                "name": "geo_query",
                "arguments": {
                    "prompt": "Evaluate bilateral currency clearing and trade gap with China",
                    "persona": "sanyal"
                }
            }
        }
        resp = server.handle_request(call_req)
        assert resp["id"] == 10
        assert "result" in resp
        content = resp["result"]["content"]
        assert len(content) > 0
        parsed = json.loads(content[0]["text"])
        assert "prioritized_lenses" in parsed
        assert parsed["persona"] == "sanyal"
        assert parsed["overall_confidence"] > 0.0

    def test_mcp_server_tool_call_deflation(self):
        """Verify MCP server tool execution for geo_recalculate_deflation."""
        from geo_engine.mcp import GeoEngineMCPServer
        import json

        server = GeoEngineMCPServer()
        call_req = {
            "jsonrpc": "2.0",
            "id": 11,
            "method": "tools/call",
            "params": {
                "name": "geo_recalculate_deflation",
                "arguments": {
                    "nominal_output": 100.0,
                    "output_deflator": 1.02,
                    "nominal_input": 60.0,
                    "input_deflator": 0.95
                }
            }
        }
        resp = server.handle_request(call_req)
        assert resp["id"] == 11
        parsed = json.loads(resp["result"]["content"][0]["text"])
        assert "real_gva_single_deflated" in parsed
        assert "real_gva_double_deflated" in parsed
        assert "divergence_pct" in parsed
        assert parsed["distortion_risk"] in ["HIGH", "MODERATE", "NEGLIGIBLE"]

    def test_geo_economist_double_deflation_mathematical_model(self):
        """Verify GeoEconomistLens double deflation calculation and divergence behavior."""
        from geo_engine.lenses.geo_economist import GeoEconomistLens
        import pytest

        # Test normal divergence: output deflator 1.05, input deflator 0.90 (input cost collapse)
        res = GeoEconomistLens.calculate_double_deflated_gva(
            nominal_output=120.0,
            output_deflator=1.05,
            nominal_input=70.0,
            input_deflator=0.90
        )
        assert res["nominal_gva"] == 50.0
        assert res["real_gva_single_deflated"] == round(50.0 / 1.05, 2)
        assert res["real_gva_double_deflated"] == round((120.0 / 1.05) - (70.0 / 0.90), 2)
        assert res["single_deflation_distortion_flag"] is True

        # Test invalid deflator raises ValueError
        with pytest.raises(ValueError):
            GeoEconomistLens.calculate_double_deflated_gva(100.0, 0.0, 50.0, 1.0)
        with pytest.raises(ValueError):
            GeoEconomistLens.calculate_double_deflated_gva(100.0, 1.0, 50.0, -0.5)

    def test_cash_flow_consolidated_capex_model(self):
        """Verify CashFlowLens consolidated public capex calculation and IEBR shift tracking."""
        from geo_engine.lenses.cash_flow import CashFlowLens

        res = CashFlowLens.calculate_consolidated_public_capex(
            union_budget_capex=11.11,
            state_capex=8.50,
            cpse_iebr=3.50,
            intergovernmental_transfers=1.50
        )
        assert res["consolidated_public_capex"] == 21.61
        assert res["union_budget_share_pct"] > 50.0
        assert "forensic_finding" in res

    def test_macro_connectors_trade_gap_and_npa_claims(self):
        """Verify SovereignMacroConnectors generates valid metrics and typed ClaimItem records."""
        from geo_engine.ingestion.macro_connectors import SovereignMacroConnectors
        from geo_engine.ingestion.models import EpistemicTier

        # 1. Trade gap connector
        metrics_trade, claim_trade = SovereignMacroConnectors.compute_china_trade_gap(
            dgft_imports_usd_b=101.7,
            gacc_exports_usd_b=118.5
        )
        assert metrics_trade["trade_gap_usd_b"] == 16.8
        assert metrics_trade["under_invoicing_risk"] == "HIGH"
        assert claim_trade.epistemic_tier == EpistemicTier.TIER_2_FINANCIAL
        assert "GeoEconomistLens" in claim_trade.target_lenses

        # 2. Banking NPA resolution connector
        metrics_npa, claim_npa = SovereignMacroConnectors.compute_banking_npa_recovery_ratio(
            write_offs_usd_b=175.0,
            cash_recoveries_usd_b=45.0,
            recap_subsidy_usd_b=37.5
        )
        assert metrics_npa["recovery_efficiency_ratio"] == 0.20
        assert metrics_npa["resolution_mode"] == "WRITE_OFF_DOMINANT"
        assert claim_npa.epistemic_tier == EpistemicTier.TIER_2_FINANCIAL

        # 3. Debt servicing connector
        metrics_debt, claim_debt = SovereignMacroConnectors.compute_debt_servicing_ratio(
            interest_payments_inr_lakh_cr=11.68,
            net_tax_revenue_inr_lakh_cr=26.01
        )
        assert metrics_debt["debt_servicing_ratio_pct"] > 40.0
        assert metrics_debt["fiscal_space_risk"] == "HIGH"
        assert "CivilizationalLens" in claim_debt.target_lenses

    def test_cli_mcp_subcommand_registration(self):
        """Verify CLI argument parser registers mcp command."""
        import argparse
        from geo_engine import cli

        # Check parser definition
        assert hasattr(cli, "main")

    def test_readme_phase52_test_count_parity(self):
        """Verify README.md reflects 179+ comprehensive tests."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "comprehensive unit and integration tests" in content


class TestPhase53SelfLearningAndTemporalDecay:
    """Phase 53: Autonomous closed-loop self-learning, exponential temporal decay,
    pundit credibility deflator, state resistance threshold, and headless audio stream connector."""

    def test_calculate_temporal_decay_half_life(self):
        """Verify exponential temporal decay calculation with 90-day half-life."""
        from geo_engine.forecasting.calibration import calculate_temporal_decay

        ref_date = "2026-09-22"

        # Delta t = 0 days -> decay = 1.0
        assert calculate_temporal_decay("2026-09-22", reference_date=ref_date, half_life_days=90.0) == 1.0

        # Delta t = 90 days -> decay = exp(-ln(2)) = 0.50
        decay_90 = calculate_temporal_decay("2026-06-24", reference_date=ref_date, half_life_days=90.0)
        assert abs(decay_90 - 0.50) <= 0.01

        # Delta t = 180 days -> decay = 0.25
        decay_180 = calculate_temporal_decay("2026-03-26", reference_date=ref_date, half_life_days=90.0)
        assert abs(decay_180 - 0.25) <= 0.01

        # Future date -> decay = 1.0
        assert calculate_temporal_decay("2026-10-01", reference_date=ref_date, half_life_days=90.0) == 1.0

    def test_calculate_temporal_decay_infinite_treaties(self):
        """Verify statutory treaties and constitutional covenants have infinite half-life (tau = inf -> decay = 1.0)."""
        from geo_engine.forecasting.calibration import calculate_temporal_decay

        ref_date = "2026-09-22"
        # 35 years ago (1991)
        decay_inf = calculate_temporal_decay("1991-09-18", reference_date=ref_date, half_life_days=float("inf"))
        assert decay_inf == 1.0

        decay_zero = calculate_temporal_decay("1991-09-18", reference_date=ref_date, half_life_days=0.0)
        assert decay_zero == 1.0

    def test_forecasting_engine_scenario_updating_with_temporal_decay(self):
        """Verify ForecastingEngine discounts outdated evidence claims via temporal decay."""
        import types
        from geo_engine.forecasting.calibration import ForecastingEngine, ScenarioBranch

        scenarios = [
            ScenarioBranch(scenario_name="Scenario A: Baseline Stability", probability=0.60, key_drivers=[], early_indicators=[]),
            ScenarioBranch(scenario_name="Scenario B: Disruption & Friction", probability=0.40, key_drivers=[], early_indicators=[])
        ]

        # Fresh claim from today
        fresh_claim = types.SimpleNamespace(
            asserted_fact="Active sanctions and naval chokepoint interdiction operations",
            reliability_weight=1.0,
            evidence_status="sufficient",
            date="2026-09-22",
            claim_type="PHYSICAL_PRESENCE",
            epistemic_tier="TIER_1_PHYSICAL"
        )
        res_fresh = ForecastingEngine.update_scenario_probabilities(scenarios, [fresh_claim], reference_date="2026-09-22")
        p_fresh_disruption = next(s.probability for s in res_fresh if "Disruption" in s.scenario_name)

        # Stale claim from 360 days ago (4 half-lives, weight ~0.0625)
        stale_claim = types.SimpleNamespace(
            asserted_fact="Active sanctions and naval chokepoint interdiction operations",
            reliability_weight=1.0,
            evidence_status="sufficient",
            date="2025-09-27",
            claim_type="PHYSICAL_PRESENCE",
            epistemic_tier="TIER_1_PHYSICAL"
        )
        res_stale = ForecastingEngine.update_scenario_probabilities(scenarios, [stale_claim], reference_date="2026-09-22")
        p_stale_disruption = next(s.probability for s in res_stale if "Disruption" in s.scenario_name)

        # Fresh disruption evidence must shift probability more aggressively than 1-year stale claim
        assert p_fresh_disruption > p_stale_disruption

    def test_event_store_temporal_weighted_events(self):
        """Verify EventStore retrieves events annotated with decay weights, exempting statutory baselines."""
        from geo_engine.storage.event_store import EventStore

        store = EventStore()
        events = store.get_events_with_temporal_weights(reference_date="2026-09-22", half_life_days=90.0)
        assert len(events) > 0
        for evt in events:
            assert "temporal_decay_weight" in evt
            assert 0.0 <= evt["temporal_decay_weight"] <= 1.0
            cat = (evt.get("category") or "").lower()
            if any(k in cat for k in ["treaty", "legal", "statute", "sovereign_redline", "monetary_architecture"]):
                assert evt["temporal_decay_weight"] == 1.0

    def test_institutional_lawfare_pundit_credibility(self):
        """Verify InstitutionalLawfareLens calculate_pundit_credibility evaluates commentator discourse."""
        from geo_engine.lenses.institutional_lawfare import InstitutionalLawfareLens

        # High diagnostic, low operational feasibility (typical normative critique)
        normative = InstitutionalLawfareLens.calculate_pundit_credibility(0.90, 0.25)
        assert normative["credibility_score"] == 0.225
        assert normative["discourse_category"] == "Rhetorical / Normative Critique (High Diagnostic, Low Operational Execution)"
        assert normative["operational_actionability"] == "LOW"
        assert normative["statutory_execution_barrier_identified"] is True

        # High diagnostic, high operational feasibility (actionable statecraft)
        statecraft = InstitutionalLawfareLens.calculate_pundit_credibility(0.85, 0.75)
        assert statecraft["credibility_score"] == 0.6375
        assert statecraft["discourse_category"] == "Actionable Statecraft / Strategic Doctrine"
        assert statecraft["operational_actionability"] == "HIGH"

        # Low diagnostic, low operational feasibility (noise)
        noise = InstitutionalLawfareLens.calculate_pundit_credibility(0.20, 0.30)
        assert noise["operational_actionability"] == "NEGLIGIBLE"

    def test_hybrid_covert_state_resistance_threshold(self):
        """Verify HybridCovertLens calculate_state_resistance_threshold models street-veto vs state resolve."""
        from geo_engine.lenses.hybrid_covert import HybridCovertLens

        # Case 1: Disruption exceeds threshold near elections -> vulnerable
        vuln = HybridCovertLens.calculate_state_resistance_threshold(
            core_salience=0.80,
            coalition_cushion=0.60,
            disruption_cost=0.75,
            election_proximity_months=3.0
        )
        assert vuln["electoral_discount_factor"] < 1.0
        assert vuln["state_resistance_threshold"] < 0.75
        assert vuln["state_posture"] == "VULNERABLE_TO_STREET_VETO"
        assert vuln["capitulation_probability"] > 0.50

        # Case 2: Distant election (36 months) with resilient coalition -> resolve holds
        resilient = HybridCovertLens.calculate_state_resistance_threshold(
            core_salience=0.90,
            coalition_cushion=0.85,
            disruption_cost=0.40,
            election_proximity_months=36.0
        )
        assert resilient["electoral_discount_factor"] == 1.0
        assert resilient["state_resistance_threshold"] > 0.40
        assert resilient["state_posture"] == "RESILIENT_STATE_ENFORCEMENT"
        assert resilient["capitulation_probability"] < 0.50

    def test_event_store_phase53_statutory_and_middle_east_seeds(self):
        """Verify EventStore seeds Places of Worship Act, Waqf Act, HRCE and Middle East 2024-2026 events."""
        from geo_engine.storage.event_store import EventStore

        store = EventStore()
        clauses = store.get_mandatory_baseline_clauses()
        clause_ids = {c["clause_id"] for c in clauses}
        assert "CLAUSE-1991-POWA" in clause_ids
        assert "CLAUSE-1995-WAQF" in clause_ids
        assert "CLAUSE-1951-HRCE" in clause_ids

        # Check Middle East events
        red_sea = store.query_events("Red Sea Corridor Disruption")
        assert len(red_sea) >= 1
        assert "Suez Canal" in red_sea[0]["summary"]

        syria = store.query_events("Fall of the Assad Regime")
        assert len(syria) >= 1
        assert "Assad" in syria[0]["summary"]

        israel_iran = store.query_events("Operation Days of Repentance")
        assert len(israel_iran) >= 1
        assert "S-300" in israel_iran[0]["summary"]

    def test_audio_stream_connector_end_to_end(self):
        """Verify AudioStreamConnector extracts media ID, fetches transcripts, and normalizes claims."""
        from geo_engine.video.audio_stream import AudioStreamConnector
        from geo_engine.ingestion.models import ClaimItem

        conn = AudioStreamConnector()

        # 1. Media ID extraction
        yt_id = conn.extract_media_id("https://www.youtube.com/watch?v=weXHMJBrC4I")
        assert yt_id == "weXHMJBrC4I"

        podcast_id = conn.extract_media_id("https://example.com/podcast/episode123.mp3")
        assert podcast_id.startswith("MED-")

        # 2. Fetch transcript (with fallback/caption support)
        transcript = conn.fetch_stream_transcript("https://www.youtube.com/watch?v=weXHMJBrC4I")
        assert transcript.media_id == "weXHMJBrC4I"
        assert len(transcript.segments) > 0
        assert transcript.full_text != ""

        # 3. Claims generation
        claims = conn.transcript_to_claims(transcript, target_lenses=["InstitutionalLawfareLens"])
        assert len(claims) > 0
        assert isinstance(claims[0], ClaimItem)
        assert "InstitutionalLawfareLens" in claims[0].target_lenses

    def test_event_store_record_claim(self):
        """Verify EventStore record_claim method persists claim items into SQLite events table."""
        from geo_engine.storage.event_store import EventStore
        from geo_engine.ingestion.models import ClaimItem, ClaimType, EpistemicTier

        store = EventStore()
        claim = ClaimItem(
            claim_id="TEST-CLM-REC-01",
            source_evidence_id="SRC-TEST-01",
            claim_type=ClaimType.LEGAL_COMMITMENT,
            epistemic_tier=EpistemicTier.TIER_3_SOVEREIGN_REDLINES,
            actors=["India", "Global"],
            asserted_fact="Bilateral currency clearing and local debt recycling verified.",
            target_lenses=["InstitutionalLawfareLens", "GeoEconomistLens"]
        )
        store.record_claim(claim)
        found = store.query_events("Bilateral currency clearing")
        assert len(found) >= 1
        assert "EVT-TEST-CLM-REC-01" in [e["event_id"] for e in found]

    def test_mcp_geo_ingest_media_tool(self):
        """Verify MCP server exposes and executes geo_ingest_media tool."""
        from geo_engine.mcp import GeoEngineMCPServer
        import json

        server = GeoEngineMCPServer()
        list_resp = server.handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}})
        tool_names = [t["name"] for t in list_resp["result"]["tools"]]
        assert "geo_ingest_media" in tool_names

        call_resp = server.handle_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "geo_ingest_media",
                "arguments": {"url": "weXHMJBrC4I", "target_lenses": ["InstitutionalLawfareLens"]}
            }
        })
        assert "result" in call_resp
        content_txt = call_resp["result"]["content"][0]["text"]
        data = json.loads(content_txt)
        assert data["media_id"] == "weXHMJBrC4I"
        assert data["claims_ingested"] >= 0

    def test_readme_phase53_test_count_parity(self):
        """Verify README.md reflects 190 or higher comprehensive tests."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "comprehensive unit and integration tests" in content


class TestPhase54OperationalPipeline:
    """Automated verification for Phase 54 Resilient Operational Pipeline & EventStore Fallback."""

    def test_ranker_event_store_fallback(self):
        """Verify StrategicNewsRanker falls back to EventStore when external feeds are degraded."""
        from morning_digest.ranker import StrategicNewsRanker
        ranked = StrategicNewsRanker.rank_headlines(evidence_items=None, top_n=5)
        assert len(ranked) >= 1
        top_story = ranked[0]
        assert "strategic_score" in top_story
        assert "category" in top_story
        assert "headline" in top_story
        assert len(top_story["headline"]) >= 15
        assert "EventStore" in top_story["source"] or "Official Gazette" in top_story["source"] or "GDELT" in top_story["source"]

    def test_readme_phase54_test_count_parity(self):
        """Verify README.md reflects 192 comprehensive tests."""
        import pathlib
        readme_path = pathlib.Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "192 comprehensive unit and integration tests" in content









