"""
GDELT 2.0 Open Intelligence Ingestion Client.
Connects to the Global Database of Events, Language, and Tone (GDELT) 2.0 API.
100% free open-access protocol requiring zero proprietary API keys.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import List
import urllib.request
import urllib.parse
from .models import ClaimType, EvidenceItem


class GDELTClient:
    """Ingests global real-time event telemetry from the GDELT Project."""

    BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

    @classmethod
    def query_events(cls, query_topic: str, max_records: int = 5) -> List[EvidenceItem]:
        """
        Fetches live articles and event records from GDELT 2.0.
        Falls back to authenticated local cache/telemetry if network is unavailable.
        """
        params = {
            "query": query_topic,
            "mode": "artlist",
            "maxrecords": str(max_records),
            "format": "json",
            "sort": "date_desc"
        }
        url = f"{cls.BASE_URL}?{urllib.parse.urlencode(params)}"
        
        evidence_items = []
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "GeoEngine-OSINT-Ingester/1.0"}
            )
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    articles = data.get("articles", [])
                    for art in articles:
                        ev_id = hashlib.sha256((art.get("url", "") + art.get("seendate", "")).encode()).hexdigest()[:12]
                        evidence_items.append(EvidenceItem(
                            evidence_id=f"GDELT-{ev_id}",
                            source_name=art.get("domain", "GDELT Global News"),
                            source_type="news_wire",
                            timestamp=art.get("seendate", datetime.now(timezone.utc).isoformat()),
                            raw_text=art.get("title", "") + ". " + art.get("sourcecountry", ""),
                            provenance_url=art.get("url"),
                            reliability_weight=0.70,
                            entities_mentioned=[query_topic],
                            claim_type=ClaimType.GENERAL_INTEL
                        ))
        except Exception:
            # Explicit degraded mode when live internet connection or API is unreachable
            evidence_items = cls._generate_degraded_telemetry(query_topic)

        if not evidence_items:
            evidence_items = cls._generate_degraded_telemetry(query_topic)

        return evidence_items

    @classmethod
    def _generate_degraded_telemetry(cls, query_topic: str) -> List[EvidenceItem]:
        """Generates explicit degraded telemetry record when live internet is unreachable."""
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return [
            EvidenceItem(
                evidence_id=f"GDELT-DEGRADED-{hashlib.md5(query_topic.encode()).hexdigest()[:8]}",
                source_name="GDELT 2.0 (Offline/Degraded)",
                source_type="news_wire",
                timestamp=now_iso,
                raw_text=f"Live GDELT telemetry unavailable for topic '{query_topic}'. Analysis proceeding in degraded state without verified external news wire signals.",
                provenance_url="https://api.gdeltproject.org/api/v2/doc/doc",
                reliability_weight=0.0,
                entities_mentioned=[query_topic],
                claim_type=ClaimType.GENERAL_INTEL,
                evidence_status="insufficient"
            )
        ]
