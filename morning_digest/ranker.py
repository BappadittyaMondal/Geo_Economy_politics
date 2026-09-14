"""
Stage A: Strategic News Ranker.
Ingests 150-300 open-source headlines from sovereign gazettes, wires, and RSS feeds,
scores their strategic relevance across national security, geo-economics, and civilizational diplomacy,
and outputs the prioritized Top-50 Morning Intelligence Digest.
"""

import re
from typing import Any, Dict, List, Optional
from geo_engine.ingestion import SovereignRSSClient, GDELTClient, EvidenceItem


class StrategicNewsRanker:
    """Ranks and filters raw news feeds into a structured Top-50 strategic digest."""

    STRATEGIC_DOMAINS = {
        "border_security": {
            "weight": 0.35,
            "keywords": [
                "border", "lac", "loc", "troops", "disengagement", "siliguri",
                "china", "pla", "pakistan", "bangladesh", "dhaka", "hasina",
                "defense", "missile", "patrol", "navy", "indian ocean"
            ]
        },
        "geo_economics": {
            "weight": 0.30,
            "keywords": [
                "capex", "rbi", "rupee", "inr", "vostro", "crude", "oil", "petro",
                "trade deficit", "sanctions", "ofac", "cips", "central bank",
                "inflation", "currency swap", "ndb", "sovereign fund"
            ]
        },
        "multilateral_diplomacy": {
            "weight": 0.20,
            "keywords": [
                "brics", "quad", "sco", "g20", "asean", "bimstec", "mea", "jaishankar",
                "modi", "summit", "bilateral", "unsc", "treaty", "communique"
            ]
        },
        "digital_sovereignty": {
            "weight": 0.15,
            "keywords": [
                "semiconductor", "chip", "fab", "telecom", "huawei", "5g", "compute",
                "ai", "satellite", "navic", "critical minerals", "lithium"
            ]
        }
    }

    @classmethod
    def score_headline(cls, text: str) -> Dict[str, Any]:
        """Calculates strategic relevance score (0.0 to 1.0) and primary category for a headline."""
        text_lower = text.lower()
        domain_scores = {}
        total_score = 0.0

        for domain, meta in cls.STRATEGIC_DOMAINS.items():
            matches = sum(1 for kw in meta["keywords"] if re.search(rf"\b{re.escape(kw)}\b", text_lower))
            normalized = min(1.0, matches * 0.35)
            domain_scores[domain] = normalized
            total_score += normalized * meta["weight"]

        # Determine primary domain
        best_domain = max(domain_scores.items(), key=lambda x: x[1])[0] if domain_scores else "general_intel"
        final_score = round(min(1.0, total_score), 3)

        return {
            "strategic_score": final_score,
            "primary_domain": best_domain,
            "requires_deep_dive": final_score >= 0.70
        }

    @classmethod
    def rank_headlines(
        cls,
        evidence_items: Optional[List[EvidenceItem]] = None,
        top_n: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Ranks ingested evidence items and outputs the top-N strategic digest.
        If evidence_items is not supplied, queries default live open sources.
        """
        if not evidence_items:
            evidence_items = SovereignRSSClient.fetch_primary_statements()
            evidence_items += GDELTClient.query_events("India geopolitical economy", max_records=25)
            evidence_items += GDELTClient.query_events("BRICS multilateral trade", max_records=25)

        scored_items = []
        seen_texts = set()

        for item in evidence_items:
            # Skip explicit empty/degraded records in ranking
            if item.reliability_weight == 0.0 or getattr(item, "evidence_status", "") == "insufficient" or "No live telemetry" in item.raw_text:
                continue

            cleaned_text = item.raw_text.strip()
            if cleaned_text in seen_texts or len(cleaned_text) < 15:
                continue
            seen_texts.add(cleaned_text)

            meta = cls.score_headline(cleaned_text)
            scored_items.append({
                "source": item.source_name,
                "timestamp": item.timestamp[:16],
                "headline": cleaned_text,
                "category": meta["primary_domain"].replace("_", " ").title(),
                "strategic_score": meta["strategic_score"],
                "requires_deep_dive": meta["requires_deep_dive"],
                "provenance_url": item.provenance_url
            })

        # Sort by strategic relevance descending
        scored_items.sort(key=lambda x: x["strategic_score"], reverse=True)
        return scored_items[:top_n]
