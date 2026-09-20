"""
Macro Telemetry & Asynchronous Ingestion Adapter.
Bridges external real-time data feeds (AIS shipping alerts, central bank FX reserves,
fertilizer spot prices, and bilateral Vostro balances) into structured ClaimItem models
and persistent EventStore baselines.
"""

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..core.models import EpistemicTier, get_system_reference_date
from ..storage.event_store import EventStore
from .models import ClaimItem, ClaimType, EvidenceItem


class MacroTelemetryAdapter:
    """
    Normalizes heterogeneous external macro-telemetry data feeds into
    epistemically tiered ClaimItem records for multi-lens ingestion.
    """

    DEFAULT_RELIABILITY = 0.88

    DOMAIN_LENS_MAPPING = {
        "vostro": ["GeoEconomistLens", "CashFlowLens"],
        "currency": ["GeoEconomistLens", "CashFlowLens"],
        "fx": ["GeoEconomistLens", "CashFlowLens"],
        "reserves": ["GeoEconomistLens", "CashFlowLens"],
        "ais": ["PetroLogisticsLens", "HybridCovertLens"],
        "shipping": ["PetroLogisticsLens", "FoodSecurityLens"],
        "fertilizer": ["FoodSecurityLens", "GeoEconomistLens"],
        "minerals": ["CriticalMineralsLens", "DeepTechLens"],
        "cyber": ["MilitaryReadinessLens", "HybridCovertLens"],
        "naval": ["MilitaryReadinessLens", "InstitutionalLawfareLens"]
    }

    @classmethod
    def normalize_telemetry(cls, raw_records: List[Dict[str, Any]]) -> List[ClaimItem]:
        """
        Transforms a batch of raw telemetry dictionaries into validated ClaimItems.
        Each record should contain at least 'text' or 'assertion'.
        """
        claims: List[ClaimItem] = []
        for idx, rec in enumerate(raw_records):
            text = rec.get("text") or rec.get("assertion") or rec.get("raw_text") or ""
            if not text:
                continue

            text_lower = text.lower()
            record_id = rec.get("id") or f"TEL-{hashlib.md5(f'{text}_{idx}'.encode()).hexdigest()[:8]}"
            actors = rec.get("actors") or []
            if not actors:
                # Basic actor inference
                for candidate in ["India", "China", "United States", "Russia", "Pakistan", "Iran", "Saudi Arabia"]:
                    if candidate.lower() in text_lower:
                        actors.append(candidate)

            # Determine claim type and epistemic tier
            claim_type = ClaimType.GENERAL_INTEL
            epistemic_tier = EpistemicTier.TIER_5_COMMUNIQUE_PR

            if any(k in text_lower for k in ["vostro", "dollar", "currency", "rupee", "ruble", "fx", "treasury", "reserves", "g-secs"]):
                claim_type = ClaimType.FINANCIAL_CAPEX
                epistemic_tier = EpistemicTier.TIER_2_FINANCIAL
            elif any(k in text_lower for k in ["tanker", "ais", "chokepoint", "warship", "corvette", "missile", "troop", "fertilizer", "mineral"]):
                claim_type = ClaimType.PHYSICAL_PRESENCE
                epistemic_tier = EpistemicTier.TIER_1_PHYSICAL
            elif any(k in text_lower for k in ["treaty", "accord", "colregs", "unclos", "article 51", "agreement"]):
                claim_type = ClaimType.LEGAL_COMMITMENT
                epistemic_tier = EpistemicTier.TIER_3_SOVEREIGN_REDLINES

            # Determine target lenses
            target_lenses = set(rec.get("target_lenses") or [])
            for keyword, lenses in cls.DOMAIN_LENS_MAPPING.items():
                if keyword in text_lower:
                    target_lenses.update(lenses)

            if not target_lenses:
                target_lenses.add("GeoEconomistLens")

            claims.append(ClaimItem(
                claim_id=record_id,
                source_evidence_id=rec.get("source_id", f"SRC-{record_id}"),
                claim_type=claim_type,
                epistemic_tier=epistemic_tier,
                actors=actors,
                asserted_fact=text,
                extracted_financial_mou_usd=rec.get("amount_usd"),
                is_binding_commitment=rec.get("is_binding", False),
                extracted_physical_units=rec.get("physical_units"),
                target_lenses=sorted(list(target_lenses)),
                reliability_weight=float(rec.get("reliability_weight", cls.DEFAULT_RELIABILITY)),
                evidence_status=rec.get("evidence_status", "sufficient")
            ))

        return claims

    @classmethod
    def create_claims_from_indicators(cls, indicators: Dict[str, Any]) -> List[ClaimItem]:
        """
        Synthesizes structured telemetry claims from raw numerical indicators.
        """
        records = []
        for key, val in indicators.items():
            if "vostro" in key:
                records.append({
                    "id": f"IND-{key}",
                    "text": f"Special Rupee Vostro Account indicator '{key}' registered at {val}. Verified capital recycling pathway active.",
                    "amount_usd": float(val) if isinstance(val, (int, float)) else None,
                    "target_lenses": ["GeoEconomistLens", "CashFlowLens"]
                })
            elif "spr" in key:
                records.append({
                    "id": f"IND-{key}",
                    "text": f"Strategic Petroleum Reserve indicator '{key}' recorded at {val} days import cover buffer.",
                    "physical_units": f"{val} days",
                    "target_lenses": ["PetroLogisticsLens"]
                })
            elif "fertilizer" in key or "potassium" in key:
                records.append({
                    "id": f"IND-{key}",
                    "text": f"Agricultural soil-nutrient security indicator '{key}' registered at {val}.",
                    "target_lenses": ["FoodSecurityLens"]
                })
            else:
                records.append({
                    "id": f"IND-{key}",
                    "text": f"Macro telemetry indicator '{key}' updated with value {val}.",
                    "target_lenses": ["GeoEconomistLens"]
                })

        return cls.normalize_telemetry(records)

    @classmethod
    def ingest_to_event_store(
        cls,
        claims: List[ClaimItem],
        store: Optional[EventStore] = None
    ) -> int:
        """
        Persists material telemetry claims into the SQLite EventStore.
        Returns the number of claims successfully ingested.
        """
        target_store = store or EventStore()
        ingested_count = 0
        ref_time = get_system_reference_date().strftime("%Y-%m-%d")

        with target_store._get_connection() as conn:
            cursor = conn.cursor()
            for c in claims:
                if c.reliability_weight >= 0.70 and c.evidence_status == "sufficient":
                    actor_str = ", ".join(c.actors) if c.actors else "Multi-Lateral"
                    cursor.execute("""
                        INSERT OR REPLACE INTO events
                        (event_id, date, title, actor, region, category, summary, civilizational_significance)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f"EVT-{c.claim_id}",
                        ref_time,
                        f"Macro Telemetry: {c.claim_type.value}",
                        actor_str,
                        "Global / Macro",
                        c.claim_type.value.lower(),
                        c.asserted_fact,
                        f"Targeted Lenses: {', '.join(c.target_lenses)}"
                    ))
                    ingested_count += 1
            conn.commit()

        return ingested_count
