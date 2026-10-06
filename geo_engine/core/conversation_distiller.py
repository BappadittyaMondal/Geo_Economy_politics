"""
Autonomous Conversational Claim Distillation Engine.
Extracts empirical propositions, statutory citations, speaker perspectives,
and causal links from user interactions and media transcripts, categorizing them
by epistemic tiers and preparing them for autonomous persistence.
"""

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import re
from typing import Any, Dict, List, Optional, Tuple

from .models import EpistemicTier
from .speaker_profiler import EpistemicSpeakerProfiler, SpeakerProfile


class VerificationStatus(str, Enum):
    """Epistemic verification state of a distilled claim."""
    VERIFIED_EMPIRICAL = "VERIFIED_EMPIRICAL"
    UNVERIFIED_ASPIRATIONAL = "UNVERIFIED_ASPIRATIONAL"
    POLEMICAL_FRAMING = "POLEMICAL_FRAMING"
    SUSPECT_PARTIAL_TRUTH = "SUSPECT_PARTIAL_TRUTH"
    UNTESTED_HYPOTHESIS = "UNTESTED_HYPOTHESIS"


class DistillationAction(str, Enum):
    """Recommended automated action for distilled knowledge."""
    PERSIST_TO_EVENT_STORE = "PERSIST_TO_EVENT_STORE"
    AUGMENT_CAUSAL_GRAPH = "AUGMENT_CAUSAL_GRAPH"
    REGISTER_HISTORICAL_ANNIVERSARY = "REGISTER_HISTORICAL_ANNIVERSARY"
    FLAG_FOR_FORENSIC_SCRUTINY = "FLAG_FOR_FORENSIC_SCRUTINY"
    DISCARD_LOW_CONFIDENCE = "DISCARD_LOW_CONFIDENCE"


@dataclass(frozen=True)
class DistilledClaim:
    """An atomically extracted claim from unstructured discourse."""
    claim_id: str
    raw_statement: str
    proposition: str
    epistemic_tier: EpistemicTier
    verification_status: VerificationStatus
    confidence: float
    source_speaker: Optional[str] = None
    statutory_citation: Optional[str] = None
    fiscal_metric: Optional[str] = None
    causal_relation: Optional[Tuple[str, str]] = None
    recommended_action: DistillationAction = DistillationAction.PERSIST_TO_EVENT_STORE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "raw_statement": self.raw_statement,
            "proposition": self.proposition,
            "epistemic_tier": self.epistemic_tier.value,
            "verification_status": self.verification_status.value,
            "confidence": self.confidence,
            "source_speaker": self.source_speaker,
            "statutory_citation": self.statutory_citation,
            "fiscal_metric": self.fiscal_metric,
            "causal_relation": list(self.causal_relation) if self.causal_relation else None,
            "recommended_action": self.recommended_action.value,
        }


@dataclass
class DistillationReport:
    """Summary report of conversational claim distillation."""
    source_summary: str
    total_extracted: int
    claims: List[DistilledClaim] = field(default_factory=list)
    matched_speakers: List[str] = field(default_factory=list)
    empirical_ratio: float = 0.0
    actionable_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_summary": self.source_summary,
            "total_extracted": self.total_extracted,
            "claims": [c.to_dict() for c in self.claims],
            "matched_speakers": self.matched_speakers,
            "empirical_ratio": self.empirical_ratio,
            "actionable_count": self.actionable_count,
        }


class ChatConversationDistiller:
    """
    Autonomous engine that distills structured empirical claims from user dialogues,
    podcast transcripts, and forensic audits into verifiable knowledge primitives.
    """

    # Empirical pattern matchers for statutory clauses, budgets, and physical infrastructure
    STATUTORY_PATTERNS = [
        (r"\b(?:section|sec\.?)\s*([0-9]+[a-z]?)\b", "Section Citation"),
        (r"\b(?:act|ordinance|amendment)\s*(?:of\s*)?([0-9]{4})\b", "Statutory Year"),
        (r"\b([0-9]{4})\s*(?:[a-zA-Z\s]{0,20})?\s*(?:act|ordinance|amendment)\b", "Pre-Statutory Year"),
        (r"\b(sc\s*/\s*st\s*(?:prevention\s*of\s*atrocities\s*)?act|places\s*of\s*worship\s*act|waqf\s*act|pmla|fcra|uapa|crpc|bns)\b", "Named Statute"),
        (r"\b(bengal\s*eastern\s*frontier\s*regulation|befr|inner\s*line\s*permit|ilp|article\s*[0-9]+[a-z]?|hr&ce\s*act)\b", "Named Statute/Regulation"),
    ]

    EPIGRAPHIC_CORRIDOR_PATTERNS = [
        (r"\b(nidhanpur|dubi|haruppeswara|kamarupa|pragjyotisha|bhaskaravarman|dah\s*parbatia|lauhitya|brahmaputra\s*trade)\b", "Northeast Classical Epigraphy"),
        (r"\b(moplah|swami\s*shraddhanand|noakhali|khilafat\s*movement|unilateral\s*pacifism|ahimsa\s*absolutism)\b", "Pacifist Vulnerability Vector"),
        (r"\b(flydubai|fz1073|cockpit\s*crash\s*axe|hammam\s*al\s*hammami|smit\s*machchhar|kamikaze\s*dive)\b", "Commercial Aviation Counter-Terrorism"),
        (r"\b(yersinia\s*pestis|plague\s*pathogen|biopreparat|vector\s*institute|bsl-4|pneumonia\s*of\s*unknown\s*aetiology)\b", "Dual-Use Biosecurity Vector"),
        (r"\b(shor(?:'s)?\s*algorithm|post-quantum\s*cryptography|pqc|kyber|dilithium|hndl|harvest\s*now\s*decrypt\s*later|quantum\s*supremacy)\b", "Post-Quantum Cryptography & Deep Tech"),
        (r"\b(gold\s*repatriation|physical\s*bullion|bank\s*of\s*england\s*vault|basel\s*iii\s*tier\s*1|700\s*(?:chinese\s*)?banks)\b", "Sovereign Balance Sheet Asset"),
        (r"\b(multibagger|turnaround\s*(?:play|story|stock)|delivery\s*volume\s*spike|200\s*ema\s*bounce|stage-2\s*breakout|sip\s*compounder)\b", "Equity Horizon Vector"),
    ]

    FISCAL_PATTERNS = [
        (r"([0-9]+(?:\.[0-9]+)?)\s*(?:lakh\s*crore|crore|trillion|billion|bn|tn)\s*(?:inr|usd|rs\.?|\$)?", "Large Capital Flow"),
        (r"([0-9]+(?:\.[0-9]+)?)\s*%\s*(?:gdp|capex|growth|inflation|tariff|haircut|discount)", "Economic Percentage"),
        (r"(?:direct\s*tax|gst\s*collection|forex\s*reserves|fiscal\s*deficit)\s*(?:of\s*)?([0-9]+(?:\.[0-9]+)?)", "Macro Metric"),
    ]

    CAUSAL_INDICATORS = [
        r"\b(?:causes|leads to|results in|triggers|catalyzes|drives|creates|generates)\b",
        r"\b(?:because of|due to|as a consequence of|owing to)\b",
        r"\b(?:thereby|consequently|inevitably forcing)\b",
    ]

    @classmethod
    def distill_text(cls, text: str, source_context: str = "user_conversation") -> DistillationReport:
        """
        Parses text and extracts structured DistilledClaim instances.
        """
        if not text or not text.strip():
            return DistillationReport(source_summary=source_context, total_extracted=0)

        # 1. Match speakers
        speakers = EpistemicSpeakerProfiler.resolve_from_text(text)
        speaker_names = [s.name for s in speakers]

        # 2. Split into sentences/propositions
        raw_sentences = re.split(r"(?<=[.!?\n])\s+", text)
        sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 15]

        distilled_claims: List[DistilledClaim] = []

        for idx, sentence in enumerate(sentences):
            lower_s = sentence.lower()

            # Detect statutory references
            statute_match = None
            for pattern, _ in cls.STATUTORY_PATTERNS:
                m = re.search(pattern, lower_s)
                if m:
                    statute_match = m.group(0).upper()
                    break

            # Detect fiscal metrics
            fiscal_match = None
            for pattern, _ in cls.FISCAL_PATTERNS:
                m = re.search(pattern, lower_s)
                if m:
                    fiscal_match = m.group(0)
                    break

            # Detect epigraphic / civilizational corridor references
            epigraphic_match = None
            for pattern, label in cls.EPIGRAPHIC_CORRIDOR_PATTERNS:
                m = re.search(pattern, lower_s)
                if m:
                    epigraphic_match = f"{label}: {m.group(0).upper()}"
                    break

            # Detect causal links
            causal_relation = None
            for c_pat in cls.CAUSAL_INDICATORS:
                parts = re.split(c_pat, sentence, maxsplit=1, flags=re.IGNORECASE)
                if len(parts) == 2 and len(parts[0].strip()) > 5 and len(parts[1].strip()) > 5:
                    causal_relation = (parts[0].strip(), parts[1].strip())
                    break

            # Check for physical infrastructure or military deployment
            is_physical = bool(re.search(r"\b(missile|frigate|aircraft|troops|chokepoint|railway|pipeline|port|transponder|satellite|border)\b", lower_s))

            # Epistemic tier determination
            if is_physical:
                tier = EpistemicTier.TIER_1_PHYSICAL
                status = VerificationStatus.VERIFIED_EMPIRICAL
                confidence = 0.92 if (statute_match or fiscal_match) else 0.86
                action = DistillationAction.PERSIST_TO_EVENT_STORE
            elif epigraphic_match:
                tier = EpistemicTier.TIER_1_PHYSICAL
                status = VerificationStatus.VERIFIED_EMPIRICAL
                confidence = 0.91
                action = DistillationAction.PERSIST_TO_EVENT_STORE
            elif fiscal_match:
                tier = EpistemicTier.TIER_2_FINANCIAL
                status = VerificationStatus.VERIFIED_EMPIRICAL
                confidence = 0.88
                action = DistillationAction.PERSIST_TO_EVENT_STORE
            elif statute_match:
                tier = EpistemicTier.TIER_3_SOVEREIGN_REDLINES
                status = VerificationStatus.VERIFIED_EMPIRICAL
                confidence = 0.90
                action = DistillationAction.PERSIST_TO_EVENT_STORE
            elif causal_relation:
                tier = EpistemicTier.TIER_3_SOVEREIGN_REDLINES
                status = VerificationStatus.UNTESTED_HYPOTHESIS
                confidence = 0.75
                action = DistillationAction.AUGMENT_CAUSAL_GRAPH
            elif any(w in lower_s for w in ["propaganda", "narrative", "perception", "bias", "communique", "press release"]):
                tier = EpistemicTier.TIER_5_COMMUNIQUE_PR
                status = VerificationStatus.POLEMICAL_FRAMING
                confidence = 0.60
                action = DistillationAction.FLAG_FOR_FORENSIC_SCRUTINY
            else:
                # Default to general aspirational or unverified
                tier = EpistemicTier.TIER_5_COMMUNIQUE_PR
                status = VerificationStatus.UNVERIFIED_ASPIRATIONAL
                confidence = 0.50
                action = DistillationAction.DISCARD_LOW_CONFIDENCE

            # Filter out pure low-confidence noise unless explicit causal link exists
            if confidence >= 0.70 or statute_match or fiscal_match or causal_relation or epigraphic_match:
                # Generate deterministic claim ID
                claim_id = "CLM-" + hashlib.sha256(sentence.encode("utf-8")).hexdigest()[:10].upper()
                primary_speaker = speaker_names[0] if speaker_names else None

                claim = DistilledClaim(
                    claim_id=claim_id,
                    raw_statement=sentence,
                    proposition=sentence[:140] + ("..." if len(sentence) > 140 else ""),
                    epistemic_tier=tier,
                    verification_status=status,
                    confidence=confidence,
                    source_speaker=primary_speaker,
                    statutory_citation=statute_match or epigraphic_match,
                    fiscal_metric=fiscal_match,
                    causal_relation=causal_relation,
                    recommended_action=action,
                )
                distilled_claims.append(claim)

        # Calculate metrics
        total = len(distilled_claims)
        empirical_count = sum(1 for c in distilled_claims if c.verification_status == VerificationStatus.VERIFIED_EMPIRICAL)
        actionable_count = sum(1 for c in distilled_claims if c.recommended_action in [
            DistillationAction.PERSIST_TO_EVENT_STORE,
            DistillationAction.AUGMENT_CAUSAL_GRAPH,
            DistillationAction.REGISTER_HISTORICAL_ANNIVERSARY,
        ])
        ratio = round(empirical_count / total, 3) if total > 0 else 0.0

        return DistillationReport(
            source_summary=source_context,
            total_extracted=total,
            claims=distilled_claims,
            matched_speakers=speaker_names,
            empirical_ratio=ratio,
            actionable_count=actionable_count,
        )
