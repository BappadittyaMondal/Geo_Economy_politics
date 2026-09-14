"""
Local Document and Raw Text Loader.
Ingests user-supplied communiques, treaties, speeches, and articles into the evidence pipeline.
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List
from .models import ClaimType, EvidenceItem


class DocumentLoader:
    """Ingests raw text or local files into normalized EvidenceItem records."""

    @classmethod
    def load_from_text(
        cls,
        text: str,
        source_name: str = "Operator Ingested Text",
        source_type: str = "treaty_text",
        claim_type: ClaimType = ClaimType.LEGAL_COMMITMENT
    ) -> EvidenceItem:
        """Converts raw text input into a verified EvidenceItem."""
        ev_id = hashlib.sha256(text.encode()).hexdigest()[:12]
        return EvidenceItem(
            evidence_id=f"DOC-{ev_id}",
            source_name=source_name,
            source_type=source_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            raw_text=text.strip(),
            provenance_url="local://operator_input",
            reliability_weight=0.90,
            entities_mentioned=[],
            claim_type=claim_type
        )

    @classmethod
    def load_from_file(cls, file_path: str) -> List[EvidenceItem]:
        """Loads and segments a text file into evidentiary clauses."""
        path = Path(file_path)
        if not path.exists():
            return []

        text = path.read_text(encoding="utf-8")
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]

        items = []
        for i, p in enumerate(paragraphs, 1):
            ev_id = hashlib.md5(f"{path.name}_{i}".encode()).hexdigest()[:8]
            items.append(EvidenceItem(
                evidence_id=f"FILE-{ev_id}",
                source_name=f"Document: {path.name}",
                source_type="treaty_text",
                timestamp=datetime.now(timezone.utc).isoformat(),
                raw_text=p,
                provenance_url=str(path.absolute()),
                reliability_weight=0.92,
                entities_mentioned=[],
                claim_type=ClaimType.LEGAL_COMMITMENT
            ))
        return items
