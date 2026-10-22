"""
geo_engine.verification.claim_extractor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Atomic Claim Decomposer & Proposition Extractor.

Decomposes complex, multi-clause statements into standalone, verifiable atomic
claims, identifying:
- Subject, Predicate, Metric, Temporal & Geographic anchors
- Domain classification (Macro, Defense, Legal, Chronology, Civilizational, etc.)
- Separation of empirical propositions from opinions, forecasts, and religious tenets
- Poisoned-tail detection and suppressed denominator flagging
"""

import re
import hashlib
from typing import List, Tuple
from geo_engine.verification.models import AtomicClaim, EvidenceDomain
from geo_engine.arbitration.competing_hypotheses import ClaimDecomposer


class AtomicClaimExtractor:
    """Extracts atomic testable claims and categorizes their epistemic domain."""

    # Sentence & clause splitting boundaries (split on .!?, newlines, or semicolons unless followed by causal connectors)
    SPLIT_PATTERNS = re.compile(r'(?<=[.!?])\s+|;(?!\s*(?:therefore|hence|thus|consequently)\b)\s*|\n+', re.IGNORECASE)

    # Domain keyword indicators

    DOMAIN_MAP = {
        EvidenceDomain.STATUTORY_LEGAL: [
            "act", "section", "article", "court", "judgment", "ordinance", "amendment",
            "statute", "petition", "bail", "rpa", "places of worship", "waqf", "crpc", "bnss"
        ],
        EvidenceDomain.MACROECONOMIC_FISCAL: [
            "gdp", "capex", "deficit", "inflation", "rbi", "vostro", "mou", "currency",
            "dollar", "billion", "crore", "trillion", "npa", "gva", "trade gap", "tax"
        ],
        EvidenceDomain.KINETIC_DEFENSE: [
            "military", "missile", "drone", "troop", "border", "lac", "loc", "air defense",
            "s-400", "wwr", "ammunition", "orbat", "interceptor", "shahed", "navy", "airstrike"
        ],
        EvidenceDomain.HISTORICAL_CHRONOLOGY: [
            "bce", "ce", "century", "dynasty", "archaeology", "excavation", "inscription",
            "aihole", "dating", "chronology", "mahabharata", "epoch", "treaty of", "partition",
            "kali yuga", "yuga", "nostradamus", "apocalypse"
        ],
        EvidenceDomain.CIVILIZATIONAL_CULTURAL: [
            "temple", "sanatan", "vedic", "hrce", "kalinga", "purusha sukta", "sampradaya",
            "dharmic", "festival", "kumbha", "navratri", "sacred", "decolonial",
            "kali yuga", "yuga", "nostradamus"
        ],
        EvidenceDomain.ENERGY_SUPPLY_CHAIN: [
            "hormuz", "malacca", "crude", "oil", "lng", "pipeline", "chokepoint", "tanker",
            "shadow fleet", "rare earth", "lithium", "gallium", "refinery", "fertilizer"
        ],
        EvidenceDomain.COGNITIVE_WARFARE: [
            "psyop", "narrative", "propaganda", "disinformation", "lawfare", "media bias",
            "conspiracy", "false flag", "bot", "deepfake", "rumor"
        ],
    }

    # Temporal patterns
    YEAR_PATTERN = re.compile(r'\b(1[0-9]{3}|20[0-9]{2}|[0-9]{3,4}\s*(?:BCE|CE|BC|AD))\b', re.IGNORECASE)

    # Metric patterns (numbers, percentages, currencies)
    METRIC_PATTERN = re.compile(
        r'(\$\s*\d+(?:\.\d+)?\s*(?:billion|million|trillion|b|m)?|'
        r'₹\s*\d+(?:\.\d+)?\s*(?:lakh|crore|billion)?|'
        r'\d+(?:\.\d+)?\s*(?:%|percent|bps|tonnes|bpd|troops|days|seats))',
        re.IGNORECASE
    )

    # Qualifier patterns (truth-conditional qualifiers that must not be silently stripped)
    QUALIFIER_PATTERNS = [
        "allegedly", "reportedly", "approximately", "according to", "claimed to",
        "estimated", "purported", "preliminary", "nearly", "roughly", "first", "only", "supposedly"
    ]

    # Opinion & Forecast indicators
    OPINION_FORECAST_INDICATORS = [
        "in my opinion", "i believe", "could lead to", "might happen", "predicted to", "expected to"
    ]


    @classmethod
    def classify_domain(cls, text: str) -> EvidenceDomain:
        """Classifies the primary evidence domain of a statement."""
        text_lower = text.lower()
        domain_scores = {d: 0 for d in cls.DOMAIN_MAP}

        for domain, keywords in cls.DOMAIN_MAP.items():
            for kw in keywords:
                if kw in text_lower:
                    domain_scores[domain] += 1

        best_domain = max(domain_scores, key=domain_scores.get)
        if domain_scores[best_domain] > 0:
            return best_domain
        return EvidenceDomain.GENERAL

    @classmethod
    def extract_claims(cls, raw_text: str) -> List[AtomicClaim]:
        """Extracts atomic claims from raw text or compound arguments."""
        if not raw_text or not raw_text.strip():
            return []

        raw_sentences = [s.strip() for s in cls.SPLIT_PATTERNS.split(raw_text) if len(s.strip()) > 8]
        extracted_claims: List[AtomicClaim] = []

        for idx, sentence in enumerate(raw_sentences):
            # 1. Check for compound assertions using ClaimDecomposer
            decomposed = ClaimDecomposer.decompose(sentence)
            
            # 2. Extract temporal anchor
            year_match = cls.YEAR_PATTERN.search(sentence)
            temporal = year_match.group(0) if year_match else None

            # 3. Extract metrics
            metric_match = cls.METRIC_PATTERN.search(sentence)
            metric = metric_match.group(0) if metric_match else None

            # 4. Opinion / Forecast check
            is_opinion = any(ind in sentence.lower() for ind in cls.OPINION_FORECAST_INDICATORS)

            # 5. Domain classification
            domain = cls.classify_domain(sentence)

            # 6. Extract truth-conditional qualifiers
            sentence_lower = sentence.lower()
            detected_qualifiers = [q for q in cls.QUALIFIER_PATTERNS if q in sentence_lower]

            # 7. Determine claim type
            if is_opinion:
                c_type = "opinion"
            elif metric:
                c_type = "numerical"
            elif domain == EvidenceDomain.STATUTORY_LEGAL:
                c_type = "legal"
            elif domain == EvidenceDomain.HISTORICAL_CHRONOLOGY:
                c_type = "historical"
            elif any(c in sentence_lower for c in ["therefore", "hence", "causes", "lead to", "results in"]):
                c_type = "causal"
            elif any(a in sentence_lower for a in ["according to", "stated that", "said that", "declared"]):
                c_type = "attribution"
            else:
                c_type = "factual"

            # 8. Check for suppressed denominators (e.g. absolute counts with no base)
            has_suppressed_denom = bool(
                re.search(
                    r'\b\d+(?:\.\d+)?\s*(?:million|lakh|crore|thousand)?\s*(?:votes|people|voters|cases|names)?\s*(?:were|are|have been|got)?\s*(?:deleted|arrested|stolen|purged|lost)\b',
                    sentence,
                    re.IGNORECASE
                )
                and not re.search(r'\b(out of|total|electorate|population|base|denominator|baseline)\b', sentence, re.IGNORECASE)
            )

            # Generate deterministic claim ID
            claim_hash = hashlib.sha256(f"{idx}:{sentence}".encode('utf-8')).hexdigest()[:10]
            claim_id = f"CLAIM-{claim_hash.upper()}"

            # If decomposed into separate premise and conclusion with poisoned tail, record
            has_poisoned = decomposed.is_poisoned_tail_detected or (
                bool(decomposed.conjunction_detected) and
                bool(re.search(r'\b(?:conspirat\w*|stolen|rigged|traitors?|sabotage|plot)\b', sentence, re.IGNORECASE))
            )

            claim = AtomicClaim(
                claim_id=claim_id,
                raw_statement=sentence,
                extracted_proposition=decomposed.factual_premises[0] if decomposed.factual_premises else sentence,
                domain=domain,
                temporal_boundary=temporal,
                quantitative_metric=metric,
                is_opinion_or_forecast=is_opinion,
                has_poisoned_tail=has_poisoned,
                has_suppressed_denominator=has_suppressed_denom,
                qualifiers=detected_qualifiers,
                claim_type=c_type
            )

            extracted_claims.append(claim)

        return extracted_claims
