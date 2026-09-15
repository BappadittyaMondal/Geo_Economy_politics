"""
Stage 0 Ingestion Normalizer.
Parses raw unstructured text from GDELT 2.0, Sovereign RSS, and official gazettes
into typed ClaimItems with actor resolution, financial parsing, physical metrics,
and targeted lens dispatch tags.
"""

import re
import hashlib
from typing import List, Optional
from ..core.models import EpistemicTier
from .models import ClaimType, EvidenceItem, ClaimItem


class IngestionNormalizer:
    """Normalizes raw unstructured open-source evidence into structured claims."""

    ACTOR_PATTERNS = {
        "India": r"\b(India|Indian|Bharat|New Delhi|Modi|MEA)\b",
        "China": r"\b(China|Chinese|Beijing|Xi Jinping|PLA|MFA)\b",
        "Russia": r"\b(Russia|Russian|Moscow|Putin|Kremlin)\b",
        "Brazil": r"\b(Brazil|Brazilian|Brasilia|Lula)\b",
        "South Africa": r"\b(South Africa|South African|Pretoria|Ramaphosa)\b",
        "Iran": r"\b(Iran|Iranian|Tehran|Pezeshkian|IRGC)\b",
        "Saudi Arabia": r"\b(Saudi Arabia|Saudi|Riyadh|MBS|Crown Prince)\b",
        "UAE": r"\b(UAE|United Arab Emirates|Emirati|Abu Dhabi|Dubai|MBZ)\b",
        "Egypt": r"\b(Egypt|Egyptian|Cairo|Sisi)\b",
        "Ethiopia": r"\b(Ethiopia|Ethiopian|Addis Ababa|Abiy)\b",
        "Bangladesh": r"\b(Bangladesh|Bangladeshi|Dhaka|Hasina|Yunus)\b",
        "United States": r"\b(United States|US|USA|Washington|White House|Biden|Trump)\b",
    }

    FINANCIAL_AMOUNT_REGEX = re.compile(
        r"(?:([\$€£]|USD|INR|Rs\.?)\s*)?(\d+(?:\.\d+)?|\.\d+)\s*(billion|million|trillion|crore|bn|m)\b",
        re.IGNORECASE
    )

    BINDING_KEYWORDS = [
        "binding", "ratified", "signed agreement", "escrow", "contract executed",
        "line of credit approved", "budgetary allocation", "vostro operational"
    ]

    PHYSICAL_KEYWORDS = [
        "troops", "deployment", "tanker", "crude", "barrels per day", "bpd",
        "pipeline", "patrol", "hardware", "satellite", "chokepoint", "lac", "border"
    ]

    LEGAL_KEYWORDS = [
        "treaty", "statutory", "unsc", "convention", "ratification", "bilateral pact",
        "communique", "declaration", "charter"
    ]

    @classmethod
    def extract_actors(cls, text: str) -> List[str]:
        """Detects mentioned sovereign actors from text."""
        detected = []
        for actor, pattern in cls.ACTOR_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(actor)
        return detected or ["Global/Multilateral"]

    @classmethod
    def extract_financial_flow(cls, text: str) -> Optional[float]:
        """Extracts nominal monetary figures normalized to USD."""
        match = cls.FINANCIAL_AMOUNT_REGEX.search(text)
        if not match:
            return None

        currency_marker = (match.group(1) or "$").upper()
        number = float(match.group(2))
        unit = match.group(3).lower()

        # Base multiplier by scale unit
        if unit in ["billion", "bn"]:
            base_amount = number * 1_000_000_000.0
        elif unit in ["million", "m"]:
            base_amount = number * 1_000_000.0
        elif unit == "trillion":
            base_amount = number * 1_000_000_000_000.0
        elif unit == "crore":
            base_amount = number * 10_000_000.0
            currency_marker = "INR"
        else:
            return None

        # Currency conversion to USD
        import os
        inr_rate = float(os.environ.get("INR_USD_RATE", "83.5"))
        eur_rate = float(os.environ.get("EUR_USD_RATE", "1.08"))
        gbp_rate = float(os.environ.get("GBP_USD_RATE", "1.28"))

        if "INR" in currency_marker or "RS" in currency_marker:
            return round(base_amount / inr_rate, 2)
        elif "€" in currency_marker or "EUR" in currency_marker:
            return round(base_amount * eur_rate, 2)
        elif "£" in currency_marker or "GBP" in currency_marker:
            return round(base_amount * gbp_rate, 2)
        else:
            return round(base_amount, 2)

    @classmethod
    def normalize_evidence_item(cls, item: EvidenceItem) -> List[ClaimItem]:
        """Transforms an atomic EvidenceItem into one or more structured ClaimItems."""
        text = item.raw_text
        actors = cls.extract_actors(text)
        claims: List[ClaimItem] = []

        # Check for degraded / insufficient evidence status
        if item.evidence_status == "insufficient" or item.reliability_weight == 0.0:
            claim_id = f"CLAIM-INSUFFICIENT-{item.evidence_id[:8]}"
            claims.append(ClaimItem(
                claim_id=claim_id,
                source_evidence_id=item.evidence_id,
                claim_type=item.claim_type,
                epistemic_tier=EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE,
                actors=actors,
                asserted_fact=item.raw_text,
                target_lenses=["DeepTechLens"],
                reliability_weight=0.0,
                evidence_status="insufficient"
            ))
            return claims

        # Check for Financial claims
        fin_amount = cls.extract_financial_flow(text)
        is_binding = any(kw in text.lower() for kw in cls.BINDING_KEYWORDS)
        if fin_amount or "currency" in text.lower() or "vostro" in text.lower() or "investment" in text.lower():
            claims.append(ClaimItem(
                claim_id=f"CLAIM-FIN-{hashlib.md5(text.encode()).hexdigest()[:8]}",
                source_evidence_id=item.evidence_id,
                claim_type=ClaimType.FINANCIAL_CAPEX,
                epistemic_tier=EpistemicTier.TIER_2_FINANCIAL,
                actors=actors,
                asserted_fact=text,
                extracted_financial_mou_usd=fin_amount,
                is_binding_commitment=is_binding,
                target_lenses=["CashFlowLens", "GeoEconomistLens"],
                reliability_weight=item.reliability_weight,
                evidence_status="sufficient"
            ))

        # Check for Physical Presence / Energy claims
        if any(kw in text.lower() for kw in cls.PHYSICAL_KEYWORDS):
            claims.append(ClaimItem(
                claim_id=f"CLAIM-PHYS-{hashlib.md5(text.encode()).hexdigest()[:8]}",
                source_evidence_id=item.evidence_id,
                claim_type=ClaimType.PHYSICAL_PRESENCE,
                epistemic_tier=EpistemicTier.TIER_1_PHYSICAL,
                actors=actors,
                asserted_fact=text,
                target_lenses=["PetroLogisticsLens", "HybridCovertLens", "GeopoliticalLens"],
                reliability_weight=item.reliability_weight,
                evidence_status="sufficient"
            ))

        # Check for Legal / Sovereign Redline claims
        if any(kw in text.lower() for kw in cls.LEGAL_KEYWORDS):
            claims.append(ClaimItem(
                claim_id=f"CLAIM-LEGAL-{hashlib.md5(text.encode()).hexdigest()[:8]}",
                source_evidence_id=item.evidence_id,
                claim_type=ClaimType.LEGAL_COMMITMENT,
                epistemic_tier=EpistemicTier.TIER_3_SOVEREIGN_REDLINES,
                actors=actors,
                asserted_fact=text,
                target_lenses=["CivilizationalLens", "HistoryLens", "BureaucraticInertiaLens"],
                reliability_weight=item.reliability_weight,
                evidence_status="sufficient"
            ))

        # Default fallback to Rhetorical Posture / General Intel if no specific tier matched
        if not claims:
            claims.append(ClaimItem(
                claim_id=f"CLAIM-RHET-{hashlib.md5(text.encode()).hexdigest()[:8]}",
                source_evidence_id=item.evidence_id,
                claim_type=ClaimType.RHETORICAL_POSTURE,
                epistemic_tier=EpistemicTier.TIER_5_COMMUNIQUE_PR,
                actors=actors,
                asserted_fact=text,
                target_lenses=["PropagandaLens", "GeopoliticalLens"],
                reliability_weight=item.reliability_weight,
                evidence_status="sufficient"
            ))

        return [RhetoricDeflator.deflate_claim(c) for c in claims]

    @classmethod
    def normalize_evidence_batch(cls, items: List[EvidenceItem]) -> List[ClaimItem]:
        """Normalizes an entire batch of ingested EvidenceItems into structured claims with wire deduplication."""
        all_claims = []
        seen_hashes = set()
        for item in items:
            # Deduplicate syndicated stories / identical wire text
            text_norm = re.sub(r'\s+', ' ', item.raw_text.strip().lower())
            content_hash = hashlib.sha256(text_norm.encode()).hexdigest()
            if content_hash in seen_hashes:
                continue
            seen_hashes.add(content_hash)
            all_claims.extend(cls.normalize_evidence_item(item))
        return all_claims


class RhetoricDeflator:
    """
    Detects hyperbolic panic language, clickbait sensationalism, and uncorroborated
    apocalyptic rhetoric in media / OSINT wire inputs.
    Deflates hyperbolic claims to TIER_5_COMMUNIQUE_PR or TIER_0_INSUFFICIENT_EVIDENCE
    and caps confidence until verified by physical ground telemetry.
    """
    PANIC_KEYWORDS = [
        "sab swaha", "swaha", "ww3", "world war 3", "apocalypse", "apocalyptic",
        "annihilation", "annihilated", "total destruction", "all out war",
        "nuke", "nuclear strike", "nuclear holocaust", "armageddon", "tabahi",
        "parmanu hamla", "khatam", "sarvanash"
    ]

    @classmethod
    def calculate_sensationalism_index(cls, text: str) -> float:
        """
        Calculates a sensationalism index in [0.0, 1.0] based on density
        of panic keywords, excessive exclamation marks, and hyperbolic phrasing.
        """
        if not text:
            return 0.0
        lower = text.lower()
        matched_keywords = sum(1 for kw in cls.PANIC_KEYWORDS if kw in lower)
        exclamation_count = text.count("!") + text.count("‼️")
        all_caps_words = sum(1 for w in text.split() if len(w) > 2 and w.isupper())

        score = (matched_keywords * 0.35) + (min(exclamation_count, 5) * 0.08) + (min(all_caps_words, 5) * 0.05)
        return min(1.0, round(score, 2))

    @classmethod
    def deflate_claim(cls, claim: ClaimItem) -> ClaimItem:
        """
        Applies epistemic deflation: if sensationalism_index >= 0.40,
        downgrades claim epistemic tier to TIER_5 or TIER_0, caps reliability,
        and adds deflator warning tags.
        """
        s_idx = cls.calculate_sensationalism_index(claim.asserted_fact)
        if s_idx >= 0.40:
            claim.epistemic_tier = EpistemicTier.TIER_5_COMMUNIQUE_PR
            claim.reliability_weight = min(claim.reliability_weight, 0.20)
            if "PropagandaLens" not in claim.target_lenses:
                claim.target_lenses.append("PropagandaLens")
            claim.asserted_fact = f"[DEFLATED_SENSATIONALISM_SCORE_{s_idx:.2f}] {claim.asserted_fact}"
        return claim

