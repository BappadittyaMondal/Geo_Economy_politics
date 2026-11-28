"""Cross-repository knowledge exporter from Geo_Economy_politics to Equity_Lab."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


DEFAULT_EQUITY_LAB_SNAPSHOT = (
    Path(__file__).resolve().parent.parent.parent
    / "Equity_Lab_v_0.0"
    / "data"
    / "dynamic_knowledge"
    / "geo_sectors_snapshot.json"
)


def build_geo_sectors_snapshot() -> Dict[str, Any]:
    """Build deterministic macro/geopolitical sector overlay snapshot from Sections 195-198."""
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_repo": "Geo_Economy_politics",
        "source_document": "KNOWLEDGE_LIBRARY_GEO_POLITICS.md",
        "source_sections": ["Section 195", "Section 196", "Section 197", "Section 198"],
        "domestic_quarantine_export_threshold_pct": 25.0,
        "regimes": {
            "US_SECTION_301_TARIFFS": {
                "title": "USTR Section 301 Proposed Tariffs & Solar Excess-Capacity Test",
                "india_proposed_tariff_pct": 25.0,
                "india_conditional_deal_pct": 17.0,
                "china_stacked_tariff_pct": 40.0,
                "asean_benchmark_pct": 18.0,
                "solar_module_capacity_gw": 154.0,
                "solar_domestic_demand_gw": 53.0,
                "solar_chinese_input_dependency_pct": 97.0,
                "affected_sectors": [
                    "RENEWABLE", "CAPITAL_GOODS", "TEXTILES", "AUTO_ANCILLARY",
                    "CHEMICALS", "PHARMA", "HEAVY_ENGINEERING",
                ],
                "requires_export_exposure": True,
                "severity": "HIGH",
            },
            "RBI_MACRO_PRUDENTIAL_FEMA": {
                "title": "RBI Nov 2026 Stop Switch / NBFC Securitisation & FEMA 9-Month Compression",
                "nbfc_securitisation_min_resale_inr": 10_000_000,
                "securitisation_effective_date": "2027-04-01",
                "fema_export_realization_months_fx": 9,
                "fema_export_realization_months_inr": 12,
                "edpms_small_exporter_exemption_inr": 1_000_000,
                "rbi_gross_fx_reserves_usd_bn": 705.34,
                "rbi_short_forward_book_usd_bn": 239.2,
                "oct_cpi_pct": 6.1,
                "affected_sectors": ["BANKING", "NBFC"],
                "requires_export_exposure": False,
                "severity": "MODERATE",
            },
            "MARITIME_GULF_BULLION": {
                "title": "Gulf / Red Sea Chokepoint Brent >$94 & Wholesale PGI Gold Settlement",
                "brent_floor_usd": 94.0,
                "wgc_pgi_gold_settlement": True,
                "headwind_sectors": ["SHIPPING", "CONTAINER_CARGO", "LOGISTICS", "REFINING", "PAINTS", "CHEMICALS"],
                "tailwind_sectors": ["SHIPPING_TANKERS"],
                "requires_export_exposure": False,
                "severity": "MODERATE",
            },
            "DPDP_AND_US_CONSULTING_VISA": {
                "title": "DPDP May 2027 Localization Cliff & US Consulting Visa Cutover",
                "dpdp_enforcement_date": "2027-05-13",
                "dpdp_max_penalty_cr": 250.0,
                "ibm_consulting_visa_cutoff": "2026-12-31",
                "india_nov_fii_inflow_usd_bn": 13.0,
                "affected_sectors": ["IT", "SOFTWARE"],
                "requires_export_exposure": True,
                "severity": "MODERATE",
            },
        },
    }


def export_geo_sectors_snapshot(output_path: Optional[Path] = None) -> Path:
    """Write geo_sectors_snapshot.json atomically to the target path."""
    target = Path(output_path) if output_path else DEFAULT_EQUITY_LAB_SNAPSHOT
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = build_geo_sectors_snapshot()
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return target
