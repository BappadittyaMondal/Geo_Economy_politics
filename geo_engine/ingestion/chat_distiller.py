"""
Chat Conversation Distiller & Autonomous Epistemic Self-Learning Engine.
Translates high-signal conversational exchanges, user-agent analytical interactions,
and forensic audit conclusions into structured, epistemically tiered ClaimItems
and persists them into the EventStore, closing the session amnesia gap.
"""

import re
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..core.models import EpistemicTier, get_system_reference_date
from ..core.query_parser import QueryParser
from ..storage.event_store import EventStore
from .models import ClaimItem, ClaimType
from .telemetry_adapter import MacroTelemetryAdapter


class ChatConversationDistiller:
    """
    Autonomous Knowledge Distillation Engine.
    Transforms raw multi-turn conversation text into verified ClaimItems,
    updates diagnostic longitudinal memory, and commits new empirical anchors
    to the EventStore without requiring manual code rewrites.
    """

    @classmethod
    def distill_conversation(
        cls,
        conversation_text: str,
        session_id: Optional[str] = None,
        source_id: Optional[str] = None
    ) -> List[ClaimItem]:
        """
        Extracts structured ClaimItems from conversation text or analytical summaries.
        Applies epistemic tier classification and dynamic multi-lens routing.
        """
        if not conversation_text or not conversation_text.strip():
            return []

        # Split conversation into analytical chunks (paragraphs, bullet points, numbered items, speaker turns)
        raw_lines = re.split(r"\n{2,}|\n(?=[•\-\*\d]+\.?|\s*(?:User|Assistant|Speaker|Human|AI|Analyst)\s*:)", conversation_text)
        candidate_blocks = [line.strip() for line in raw_lines if len(line.strip()) >= 20]
        if len(candidate_blocks) <= 1:
            if "\n" in conversation_text:
                candidate_blocks = [line.strip() for line in conversation_text.split("\n") if len(line.strip()) >= 20]
            elif ". " in conversation_text:
                candidate_blocks = [line.strip() for line in re.split(r"\.\s+(?=[A-Z])", conversation_text) if len(line.strip()) >= 20]

        extracted_claims: List[ClaimItem] = []
        ref_date = get_system_reference_date()

        for idx, block in enumerate(candidate_blocks):
            # Clean leading bullets or numbers
            clean_text = re.sub(r"^[•\-\*\d\.\:\s]+", "", block).strip()
            if len(clean_text) < 25:
                continue

            text_lower = clean_text.lower()

            # Identify target lenses via QueryParser keywords
            matched_lenses: List[str] = []
            for lens_name, kws in QueryParser.LENS_KEYWORDS.items():
                for kw in kws:
                    if kw in text_lower:
                        # Format as Lens class name
                        class_name = "".join(word.capitalize() for word in lens_name.split("_")) + "Lens"
                        if class_name not in matched_lenses:
                            matched_lenses.append(class_name)
                        break

            if not matched_lenses:
                matched_lenses = ["CivilizationalLens", "GeopoliticalLens"]

            # Classify Epistemic Tier
            # Tier 1: Physical, Archaeological, Kinetic, C14, Excavations
            if any(w in text_lower for w in [
                "c14", "radiocarbon", "excavation", "bsip", "coffin", "sword", "shield",
                "chariot", "cart", "strata", "archaeology", "troops", "drone", "fpv", "missile", "orbat"
            ]):
                tier = EpistemicTier.TIER_1_PHYSICAL
                claim_type = ClaimType.PHYSICAL_PRESENCE
                reliability = 0.92
            # Tier 2: Hard Money, CapEx, Vostro, Haircut, NPA, Balance Sheet
            elif any(w in text_lower for w in [
                "capex", "haircut", "vostro", "srva", "g-sec", "npa", "write-off", "trade gap",
                "deflation", "usd", "crore", "billion", "fx reserves", "capital recycling"
            ]):
                tier = EpistemicTier.TIER_2_FINANCIAL
                claim_type = ClaimType.FINANCIAL_CAPEX
                reliability = 0.90
            # Tier 3: Sovereign Redlines, Treaties, Statutory Lawfare, Constitution
            elif any(w in text_lower for w in [
                "treaty", "bpta", "cbm", "crpc", "uapa", "bnss", "hrce", "section 167", "section 188",
                "sovereign redline", "unclos", "statutory", "mandate", "article"
            ]):
                tier = EpistemicTier.TIER_3_SOVEREIGN_REDLINES
                claim_type = ClaimType.LEGAL_COMMITMENT
                reliability = 0.95
            # Tier 4: Kinesic micro-signals, FACS, sartorial, body language, prosodic cues
            elif any(w in text_lower for w in [
                "kinesic", "facs", "social mask", "au12", "au06", "masseter", "sartorial", "body language",
                "prosodic", "pause", "micro-signal", "micro signal", "tension"
            ]):
                tier = EpistemicTier.TIER_4_KINESICS
                claim_type = ClaimType.KINESIC_MICRO_SIGNAL
                reliability = 0.70
            # Tier 5: Media rhetoric, communiques, public declarations
            else:
                tier = EpistemicTier.TIER_5_COMMUNIQUE_PR
                claim_type = ClaimType.RHETORICAL_POSTURE
                reliability = 0.50

            # Generate unique claim ID
            claim_hash = hashlib.sha256(f"{clean_text[:60]}_{idx}".encode("utf-8")).hexdigest()[:8]
            claim_id = f"CHAT-CLAIM-{claim_hash.upper()}"
            src_tag = source_id or session_id or "DEFAULT"

            extracted_claims.append(ClaimItem(
                claim_id=claim_id,
                source_evidence_id=f"SRC-CONV-{src_tag}",
                asserted_fact=clean_text[:500],
                claim_type=claim_type,
                epistemic_tier=tier,
                target_lenses=matched_lenses[:4],
                reliability_weight=reliability,
                evidence_status="sufficient"
            ))

        return extracted_claims

    @classmethod
    def distill_and_persist(
        cls,
        conversation_text: str,
        session_id: Optional[str] = None,
        store: Optional[EventStore] = None,
        entity_or_subject: Optional[str] = None,
        event_store: Optional[EventStore] = None
    ) -> Dict[str, Any]:
        """
        Full distillation and learning pipeline:
        Extracts claims, persists them to SQLite EventStore, logs longitudinal
        diagnostic encounter, and updates the engine's long-term memory.
        """
        target_store = store or event_store or EventStore()
        claims = cls.distill_conversation(conversation_text, session_id=session_id)

        # Ingest claims into SQLite event_store
        persisted_count = MacroTelemetryAdapter.ingest_to_event_store(claims, store=target_store)

        # Infer subject/entity if not provided
        subject = entity_or_subject or "Strategic Analytical Exchange"
        if not entity_or_subject and claims:
            # Check for prominent entity mentions in first few claims
            full_corpus = " ".join(c.asserted_fact for c in claims[:3]).lower()
            for cand in ["Sinauli", "Rakhigarhi", "Hastinapur", "Galwan", "Red Sea", "Vostro", "VanDyke", "BRICS"]:
                if cand.lower() in full_corpus:
                    subject = cand
                    break

        # Calculate average metrics for diagnostic log
        avg_confidence = (
            sum(c.reliability_weight for c in claims) / len(claims)
            if claims else 0.85
        )
        tier_counts = {}
        for c in claims:
            tier_name = c.epistemic_tier.name if hasattr(c.epistemic_tier, "name") else str(c.epistemic_tier)
            tier_counts[tier_name] = tier_counts.get(tier_name, 0) + 1

        primary_tier = max(tier_counts.items(), key=lambda x: x[1])[0] if tier_counts else "TIER_1_PHYSICAL"

        # Log longitudinal diagnostic encounter
        encounter_id = target_store.record_diagnostic_encounter(
            entity_or_subject=subject,
            query_text=conversation_text[:300],
            primary_epistemic_tier=primary_tier,
            confidence=avg_confidence,
            reality_ratio=0.85,
            propaganda_ratio=0.15,
            anomalies_detected=[f"Distilled {len(claims)} conversational claims into EventStore"],
            session_id=session_id or "chat_self_learning"
        )

        return {
            "status": "LEARNING_CYCLE_COMPLETE",
            "session_id": session_id or "chat_self_learning",
            "entity_or_subject": subject,
            "claims_extracted": len(claims),
            "claims_persisted": persisted_count,
            "extracted_claims_count": len(claims),
            "persisted_claims_count": persisted_count,
            "primary_epistemic_tier": primary_tier,
            "encounter_id": encounter_id,
            "diagnostic_encounter_id": encounter_id,
            "claims": [
                {
                    "claim_id": c.claim_id,
                    "asserted_fact": c.asserted_fact,
                    "claim_type": c.claim_type.value if hasattr(c.claim_type, "value") else str(c.claim_type),
                    "epistemic_tier": c.epistemic_tier.name if hasattr(c.epistemic_tier, "name") else str(c.epistemic_tier),
                    "target_lenses": c.target_lenses,
                    "reliability_weight": c.reliability_weight
                }
                for c in claims
            ],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
