"""
Sovereign RSS and Primary Foreign Ministry Feed Parser.
Ingests direct statements from sovereign foreign offices and international institutions
without editorial intermediaries.
"""

import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import List, Optional
import urllib.request
from .models import ClaimType, EvidenceItem


class SovereignRSSClient:
    """Ingests official diplomatic and foreign ministry dispatches."""

    SOVEREIGN_FEEDS = {
        "India_MEA": "https://www.mea.gov.in/rss-feed.htm",
        "India_PIB": "https://pib.gov.in/RssMain.aspx?ModId=1",
        "UN_Press": "https://press.un.org/en/feed.xml",
        "US_StateDept": "https://www.state.gov/rss-feed/press-releases/feed/",
        "Russia_MFA": "https://mid.ru/en/rss/",
        "Iran_IRNA": "https://en.irna.ir/rss",
        "China_MFA": "https://www.fmprc.gov.cn/eng/xwfw_665399/s2510_665401/rss.xml",
    }

    @classmethod
    def fetch_primary_statements(cls, feed_key: str = "India_MEA", timeout: float = 3.0) -> List[EvidenceItem]:
        """Fetches and parses primary sovereign announcements."""
        items = []
        url = cls.SOVEREIGN_FEEDS.get(feed_key)
        if not url:
            return items

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GeoEngine-RSS/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    tree = ET.fromstring(resp.read())
                    for elem in tree.findall(".//item")[:5]:
                        title = elem.findtext("title", "")
                        link = elem.findtext("link", "")
                        desc = elem.findtext("description", "")
                        pub_date = elem.findtext("pubDate", datetime.now(timezone.utc).isoformat())
                        ev_id = hashlib.sha256((link + title).encode()).hexdigest()[:10]
                        items.append(EvidenceItem(
                            evidence_id=f"SOV-{feed_key}-{ev_id}",
                            source_name=f"Official Gazette: {feed_key.replace('_', ' ')}",
                            source_type="official_gazette",
                            timestamp=pub_date,
                            raw_text=f"{title}. {desc}",
                            provenance_url=link,
                            reliability_weight=0.95,
                            entities_mentioned=["India", "Multilateral"],
                            claim_type=ClaimType.LEGAL_COMMITMENT
                        ))
        except Exception:
            # Explicit degraded mode when sovereign gazette feed is unreachable
            items = [
                EvidenceItem(
                    evidence_id=f"SOV-{feed_key}-DEGRADED",
                    source_name=f"Official Gazette: {feed_key.replace('_', ' ')} (Offline)",
                    source_type="official_gazette",
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    raw_text=f"Primary sovereign feed for '{feed_key}' is unreachable. Ingestion running in degraded state without verified gazette input.",
                    provenance_url="https://www.mea.gov.in",
                    reliability_weight=0.0,
                    entities_mentioned=["India"],
                    claim_type=ClaimType.LEGAL_COMMITMENT,
                    evidence_status="insufficient"
                )
            ]

        return items

    @classmethod
    def fetch_all_sovereign_feeds(
        cls,
        feed_keys: Optional[List[str]] = None,
        timeout_per_feed: float = 2.0
    ) -> List[EvidenceItem]:
        """
        Polls multiple registered sovereign feeds, collapses duplicate wire claims via SHA-256 hashes,
        and aggregates verified evidence while suppressing redundant offline placeholders when live items exist.
        """
        targets = feed_keys or list(cls.SOVEREIGN_FEEDS.keys())
        all_items = []
        seen_ids = set()
        has_live_items = False

        for fk in targets:
            feed_items = cls.fetch_primary_statements(feed_key=fk, timeout=timeout_per_feed)
            for it in feed_items:
                if it.evidence_status != "insufficient" and it.reliability_weight > 0.0:
                    has_live_items = True
                if it.evidence_id not in seen_ids:
                    seen_ids.add(it.evidence_id)
                    all_items.append(it)

        # If at least one live feed succeeded, filter out individual offline degraded placeholders
        if has_live_items:
            all_items = [it for it in all_items if it.evidence_status != "insufficient" and it.reliability_weight > 0.0]

        return all_items
