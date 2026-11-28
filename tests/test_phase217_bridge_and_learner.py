"""Phase 217 Verification Suite: AutonomousLearner db_path resolution & Knowledge Bridge snapshot parity."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from geo_engine.knowledge_bridge import build_geo_sectors_snapshot, export_geo_sectors_snapshot
from geo_engine.verification.learner import AutonomousLearner


def test_autonomous_learner_custom_db_path_harmonize():
    """Verify AutonomousLearner preserves and uses its configured db_path in auto_harmonize_quarantine."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        custom_db = str(Path(tmpdir) / "custom_geo.db")
        learner = AutonomousLearner(db_path=custom_db)
        try:
            assert learner.db_path == custom_db
            res = learner.auto_harmonize_quarantine()
            assert res["harmonizer_status"] == "HARMONIZATION_COMPLETE"
        finally:
            conn = getattr(learner.store, "conn", None) or getattr(learner.store, "_conn", None)
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass


def test_knowledge_bridge_snapshot_contract_and_export():
    """Verify cross-repo Geo-Economy JSON snapshot export preserves Section 195-198 facts."""
    payload = build_geo_sectors_snapshot()
    assert payload["source_sections"] == ["Section 195", "Section 196", "Section 197", "Section 198"]
    assert payload["regimes"]["US_SECTION_301_TARIFFS"]["india_proposed_tariff_pct"] == 25.0
    assert payload["regimes"]["US_SECTION_301_TARIFFS"]["india_conditional_deal_pct"] == 17.0
    assert payload["regimes"]["RBI_MACRO_PRUDENTIAL_FEMA"]["nbfc_securitisation_min_resale_inr"] == 10_000_000

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        out_file = export_geo_sectors_snapshot(Path(tmpdir) / "snap.json")
        loaded = json.loads(out_file.read_text(encoding="utf-8"))
        assert loaded["regimes"]["US_SECTION_301_TARIFFS"]["china_stacked_tariff_pct"] == 40.0
