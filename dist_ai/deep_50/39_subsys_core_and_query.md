# SUBSYSTEM SPECIFICATION: CORE ENGINE, QUERY PARSER & KNOWLEDGE BRIDGE

## Module: `geo_engine/core/__init__.py`

```python
"""
Core domain models, truth hierarchy, and temporal guardrails for the Geo-Engine.
"""

from .models import (
    EpistemicTier,
    TemporalMode,
    FinancialFlow,
    KinesicObservation,
    CommuniqueClause,
    MemberCountryAudit,
    LensEvaluation,
    SummitEvent,
    SummitAnalysisReport,
)
from .epistemic_hierarchy import EpistemicArbitrator, TruthClaim
from .temporal_guardrail import TemporalGuardrail
from .query_parser import QueryParser, StrategicQuery
from .speaker_profiler import (
    SpeakerArchetype,
    SpeakerProfile,
    EpistemicSpeakerProfiler,
)
from .conversation_distiller import (
    VerificationStatus,
    DistillationAction,
    DistilledClaim,
    DistillationReport,
    ChatConversationDistiller,
)
from .investment_horizon import (
    InvestmentHorizon,
    HorizonEvidenceProfile,
    HorizonAdaptiveEvaluator,
    DynamicDiscountRateCalculator,
)

__all__ = [
    "EpistemicTier",
    "TemporalMode",
    "FinancialFlow",
    "KinesicObservation",
    "CommuniqueClause",
    "MemberCountryAudit",
    "LensEvaluation",
    "SummitEvent",
    "SummitAnalysisReport",
    "EpistemicArbitrator",
    "TruthClaim",
    "TemporalGuardrail",
    "QueryParser",
    "StrategicQuery",
    "SpeakerArchetype",
    "SpeakerProfile",
    "EpistemicSpeakerProfiler",
    "VerificationStatus",
    "DistillationAction",
    "DistilledClaim",
    "DistillationReport",
    "ChatConversationDistiller",
    "InvestmentHorizon",
    "HorizonEvidenceProfile",
    "HorizonAdaptiveEvaluator",
    "DynamicDiscountRateCalculator",
]


```

## Module: `geo_engine/core/conversation_distiller.py`

```python
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

```

## Module: `geo_engine/core/epistemic_hierarchy.py`

```python
"""
Epistemic Truth Hierarchy & Arbitration Engine.
Enforces deterministic priority across competing claims from diverse analytical lenses.
Priority: Tier 1 (Physical) > Tier 2 (Financial) > Tier 3 (Redlines) > Tier 4 (Kinesics) > Tier 5 (Communique/PR).
"""

from typing import List, Tuple
from pydantic import BaseModel, Field
from .models import EpistemicTier, FinancialFlow, KinesicObservation


class TruthClaim(BaseModel):
    """An analytical assertion produced by a specialized lens or agent."""
    lens_name: str
    tier: EpistemicTier
    assertion: str
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    hard_evidence_ref: str = ""
    claim_type: str = Field(default="GENERAL", description="'LEGAL_COMMITMENT', 'PHYSICAL_PRESENCE', 'FINANCIAL_CAPEX', 'RHETORICAL_POSTURE', 'GENERAL'")
    source_reliability: float = Field(default=1.0, ge=0.0, le=1.0)

    @property
    def effective_confidence(self) -> float:
        """Discounts claimed analytical confidence by underlying empirical source reliability."""
        return round(self.confidence * self.source_reliability, 3)


class EpistemicArbitrator:
    """
    Deterministic arbitrator that resolves contradictions between agent claims.
    Eliminates semantic smoothing and supports both universal and claim-aware priority matrices.
    """

    @staticmethod
    def resolve_claim_aware(claim_a: TruthClaim, claim_b: TruthClaim) -> Tuple[TruthClaim, str]:
        """
        Claim-type aware arbitration: Selects appropriate evidence hierarchy based on claim category.
        e.g., Legal commitments prioritize Treaty Text (Tier 3), whereas Physical presence prioritizes Tier 1.
        """
        if claim_a.tier == EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE or claim_b.tier == EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE:
            return EpistemicArbitrator.resolve_contradiction(claim_a, claim_b)

        category = claim_a.claim_type if claim_a.claim_type != "GENERAL" else claim_b.claim_type

        # Define category-specific tier rankings (lower value = higher priority)
        category_weights = {
            "LEGAL_COMMITMENT": {
                EpistemicTier.TIER_3_SOVEREIGN_REDLINES: 1, # Treaties are rank 1 for legal commitments
                EpistemicTier.TIER_1_PHYSICAL: 2,
                EpistemicTier.TIER_2_FINANCIAL: 3,
                EpistemicTier.TIER_4_KINESICS: 4,
                EpistemicTier.TIER_5_COMMUNIQUE_PR: 5,
            },
            "PHYSICAL_PRESENCE": {
                EpistemicTier.TIER_1_PHYSICAL: 1,           # Satellites/telemetry are rank 1
                EpistemicTier.TIER_2_FINANCIAL: 2,
                EpistemicTier.TIER_3_SOVEREIGN_REDLINES: 3,
                EpistemicTier.TIER_4_KINESICS: 4,
                EpistemicTier.TIER_5_COMMUNIQUE_PR: 5,
            },
            "FINANCIAL_CAPEX": {
                EpistemicTier.TIER_2_FINANCIAL: 1,          # Central bank/escrow is rank 1
                EpistemicTier.TIER_1_PHYSICAL: 2,
                EpistemicTier.TIER_3_SOVEREIGN_REDLINES: 3,
                EpistemicTier.TIER_4_KINESICS: 4,
                EpistemicTier.TIER_5_COMMUNIQUE_PR: 5,
            },
            "RHETORICAL_POSTURE": {
                EpistemicTier.TIER_5_COMMUNIQUE_PR: 1,      # Official transcript is rank 1 for spoken stance
                EpistemicTier.TIER_4_KINESICS: 2,
                EpistemicTier.TIER_3_SOVEREIGN_REDLINES: 3,
                EpistemicTier.TIER_1_PHYSICAL: 4,
                EpistemicTier.TIER_2_FINANCIAL: 5,
            }
        }

        weights = category_weights.get(category)
        if weights:
            rank_a = weights.get(claim_a.tier, claim_a.tier.value)
            rank_b = weights.get(claim_b.tier, claim_b.tier.value)
            if rank_a < rank_b:
                return claim_a, f"[CLAIM-AWARE ARBITRATION] In '{category}' domain, {claim_a.lens_name} (Rank {rank_a}) overrides {claim_b.lens_name} (Rank {rank_b})."
            elif rank_b < rank_a:
                return claim_b, f"[CLAIM-AWARE ARBITRATION] In '{category}' domain, {claim_b.lens_name} (Rank {rank_b}) overrides {claim_a.lens_name} (Rank {rank_a})."

        # Fallback to universal hierarchy
        return EpistemicArbitrator.resolve_contradiction(claim_a, claim_b)

    @staticmethod
    def resolve_contradiction(claim_a: TruthClaim, claim_b: TruthClaim) -> Tuple[TruthClaim, str]:
        """
        Resolves two mutually contradictory claims based on strict epistemic tier hierarchy.
        Returns the winning claim and an explanatory audit log.
        """
        # Tier 0 Handling (Insufficient empirical evidence yields to substantiated claims)
        if claim_a.tier == EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE and claim_b.tier != EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE:
            log = (
                f"[ARBITRATION WINNER] {claim_b.lens_name} (Tier {claim_b.tier.name}) overrides {claim_a.lens_name}. "
                f"Reason: {claim_a.lens_name} operates in TIER_0_INSUFFICIENT_EVIDENCE (void of telemetry)."
            )
            return claim_b, log
        elif claim_b.tier == EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE and claim_a.tier != EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE:
            log = (
                f"[ARBITRATION WINNER] {claim_a.lens_name} (Tier {claim_a.tier.name}) overrides {claim_b.lens_name}. "
                f"Reason: {claim_b.lens_name} operates in TIER_0_INSUFFICIENT_EVIDENCE (void of telemetry)."
            )
            return claim_a, log
        elif claim_a.tier == EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE and claim_b.tier == EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE:
            log = f"[ARBITRATION TIED] Both {claim_a.lens_name} and {claim_b.lens_name} lack empirical evidence (Tier 0)."
            return claim_a, log

        if claim_a.tier.value < claim_b.tier.value:
            log = (
                f"[ARBITRATION WINNER] {claim_a.lens_name} (Tier {claim_a.tier.name}) "
                f"strictly overrides {claim_b.lens_name} (Tier {claim_b.tier.name}). "
                f"Reason: Physical/Structural reality supersedes rhetoric or ceremonial signal."
            )
            return claim_a, log
        elif claim_b.tier.value < claim_a.tier.value:
            log = (
                f"[ARBITRATION WINNER] {claim_b.lens_name} (Tier {claim_b.tier.name}) "
                f"strictly overrides {claim_a.lens_name} (Tier {claim_a.tier.name}). "
                f"Reason: Physical/Structural reality supersedes rhetoric or ceremonial signal."
            )
            return claim_b, log
        else:
            # Same tier: Arbitrate by effective confidence discounted by source reliability
            conf_a = claim_a.effective_confidence
            conf_b = claim_b.effective_confidence
            if conf_a >= conf_b:
                winner, loser = claim_a, claim_b
            else:
                winner, loser = claim_b, claim_a

            log = (
                f"[INTRA-TIER ARBITRATION] Both claims in {claim_a.tier.name}. "
                f"{winner.lens_name} selected over {loser.lens_name} "
                f"due to higher effective confidence ({winner.effective_confidence:.2f} vs {loser.effective_confidence:.2f})."
            )
            return winner, log

    @staticmethod
    def arbitrate_financial_claim(flow: FinancialFlow) -> Tuple[float, str]:
        """
        Calculates effective capital deployment against nominal press release claims.
        Applies the 85% haircut to unfinanced MOUs and sanctions risk discount.
        """
        nominal = flow.nominal_mou_usd
        effective = flow.effective_capex_usd
        haircut_pct = round(((nominal - effective) / nominal) * 100, 1) if nominal > 0 else 0.0

        explanation = (
            f"Nominal PR Claim: ${nominal:,.2f} USD. "
            f"Effective CapEx Ground Truth: ${effective:,.2f} USD. "
            f"Haircut Applied: {haircut_pct}% (Unfinanced MOU status: {not flow.is_binding_contract}, "
            f"OFAC Secondary Sanctions Risk: {flow.secondary_sanctions_risk_score:.2f})."
        )
        return effective, explanation

    @staticmethod
    def arbitrate_kinesics_vs_security(
        kinesic: KinesicObservation,
        border_deployment_tension: float
    ) -> Tuple[str, str]:
        """
        Arbitrates between warm public body language (Tier 4/5) and live military/border tension (Tier 1/3).
        """
        warmth = kinesic.genuine_warmth_index
        if border_deployment_tension > 0.6:
            status = "TACTICAL_DE_ESCALATION_PERFORMANCE"
            audit = (
                f"Public warmth index ({warmth:.2f}) is overridden by active troop deployment "
                f"tension ({border_deployment_tension:.2f}). "
                f"Conclusion: Handshake and smiles represent managed ceremonial optics to prevent domestic panic, "
                f"not structural geopolitical reconciliation."
            )
        else:
            status = "GENUINE_STRATEGIC_ENGAGEMENT"
            audit = (
                f"Public warmth index ({warmth:.2f}) aligns with low/stable border tension "
                f"({border_deployment_tension:.2f})."
            )
        return status, audit

```

## Module: `geo_engine/core/investment_horizon.py`

```python
"""
Horizon-Adaptive Investment & Valuation Engine.
Adapts evidence requirements, weights, strictness, and discount rates according to
investment horizons (SIP, Turnaround/Multibagger, 3/10/30-Day Positional, Geopolitical Shock).
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


class InvestmentHorizon(str, Enum):
    """Investment horizons with fundamentally distinct evidentiary strictness."""
    SIP_LONG_TERM = "SIP_LONG_TERM"
    TURNAROUND_MULTIBAGGER = "TURNAROUND_MULTIBAGGER"
    POSITIONAL_SWING_3_10_30 = "POSITIONAL_SWING_3_10_30"
    GEOPOLITICAL_EVENT_SHOCK = "GEOPOLITICAL_EVENT_SHOCK"


@dataclass
class HorizonEvidenceProfile:
    """Evidence requirements, weights, and thresholds calibrated to an investment horizon."""
    horizon: InvestmentHorizon
    horizon_label: str
    min_historical_years: int
    fundamental_weight: float
    technical_momentum_weight: float
    macro_geopolitical_weight: float
    rate_of_change_delta_weight: float
    min_roce_threshold: float
    max_debt_to_equity: float
    allow_depressed_history: bool
    delivery_volume_multiplier_threshold: float
    requires_20_50_ema_alignment: bool
    capex_haircut_percentage: float
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "horizon": self.horizon.value,
            "horizon_label": self.horizon_label,
            "min_historical_years": self.min_historical_years,
            "fundamental_weight": self.fundamental_weight,
            "technical_momentum_weight": self.technical_momentum_weight,
            "macro_geopolitical_weight": self.macro_geopolitical_weight,
            "rate_of_change_delta_weight": self.rate_of_change_delta_weight,
            "min_roce_threshold": self.min_roce_threshold,
            "max_debt_to_equity": self.max_debt_to_equity,
            "allow_depressed_history": self.allow_depressed_history,
            "delivery_volume_multiplier_threshold": self.delivery_volume_multiplier_threshold,
            "requires_20_50_ema_alignment": self.requires_20_50_ema_alignment,
            "capex_haircut_percentage": self.capex_haircut_percentage,
            "description": self.description,
        }


class HorizonAdaptiveEvaluator:
    """Provides calibrated evidence requirements tailored to investment query horizons."""

    PROFILES: Dict[InvestmentHorizon, HorizonEvidenceProfile] = {
        InvestmentHorizon.SIP_LONG_TERM: HorizonEvidenceProfile(
            horizon=InvestmentHorizon.SIP_LONG_TERM,
            horizon_label="SIP / Long-Term Compounder (5-15 Years)",
            min_historical_years=10,
            fundamental_weight=0.70,
            technical_momentum_weight=0.05,
            macro_geopolitical_weight=0.15,
            rate_of_change_delta_weight=0.10,
            min_roce_threshold=15.0,
            max_debt_to_equity=0.50,
            allow_depressed_history=False,
            delivery_volume_multiplier_threshold=1.0,
            requires_20_50_ema_alignment=False,
            capex_haircut_percentage=85.0,
            description="Demands 10-year track record, ROCE > 15%, D/E < 0.5, clean governance. Bypasses 10-day chart noise.",
        ),
        InvestmentHorizon.TURNAROUND_MULTIBAGGER: HorizonEvidenceProfile(
            horizon=InvestmentHorizon.TURNAROUND_MULTIBAGGER,
            horizon_label="Turnaround / Early Multibagger (1-3 Years)",
            min_historical_years=2,
            fundamental_weight=0.25,
            technical_momentum_weight=0.15,
            macro_geopolitical_weight=0.15,
            rate_of_change_delta_weight=0.45,
            min_roce_threshold=5.0,
            max_debt_to_equity=2.5,
            allow_depressed_history=True,
            delivery_volume_multiplier_threshold=1.5,
            requires_20_50_ema_alignment=False,
            capex_haircut_percentage=50.0,
            description="Focuses on rate-of-change: debt reduction velocity, capacity utilization inflection, promoter de-pledge. Historical depressed ratios permitted.",
        ),
        InvestmentHorizon.POSITIONAL_SWING_3_10_30: HorizonEvidenceProfile(
            horizon=InvestmentHorizon.POSITIONAL_SWING_3_10_30,
            horizon_label="Positional / Swing (3 to 30 Days)",
            min_historical_years=1,
            fundamental_weight=0.05,
            technical_momentum_weight=0.65,
            macro_geopolitical_weight=0.15,
            rate_of_change_delta_weight=0.15,
            min_roce_threshold=0.0,
            max_debt_to_equity=999.0,
            allow_depressed_history=True,
            delivery_volume_multiplier_threshold=2.0,
            requires_20_50_ema_alignment=True,
            capex_haircut_percentage=0.0,
            description="Prioritizes stage-2 base breakout, delivery volume > 200% of 20-day avg, 20/50 EMA alignment, and relative strength vs Nifty.",
        ),
        InvestmentHorizon.GEOPOLITICAL_EVENT_SHOCK: HorizonEvidenceProfile(
            horizon=InvestmentHorizon.GEOPOLITICAL_EVENT_SHOCK,
            horizon_label="Geopolitical Event Shock (Immediate)",
            min_historical_years=3,
            fundamental_weight=0.30,
            technical_momentum_weight=0.10,
            macro_geopolitical_weight=0.50,
            rate_of_change_delta_weight=0.10,
            min_roce_threshold=10.0,
            max_debt_to_equity=1.0,
            allow_depressed_history=False,
            delivery_volume_multiplier_threshold=1.2,
            requires_20_50_ema_alignment=False,
            capex_haircut_percentage=85.0,
            description="Evaluates input cost elasticity (crude, gas, shipping rates), sovereign trade sanctions, currency depreciation stress test.",
        ),
    }

    @classmethod
    def get_evidence_profile(cls, horizon: InvestmentHorizon) -> HorizonEvidenceProfile:
        """Retrieve the evidence strictness profile for a given horizon."""
        return cls.PROFILES.get(horizon, cls.PROFILES[InvestmentHorizon.SIP_LONG_TERM])

    @classmethod
    def resolve_horizon_from_text(cls, query_text: str) -> InvestmentHorizon:
        """Detects the investment horizon from query keywords."""
        lower_q = query_text.lower()
        if any(w in lower_q for w in ["swing", "positional", "3 day", "10 day", "30 day", "breakout", "ema", "volume spike", "chart"]):
            return InvestmentHorizon.POSITIONAL_SWING_3_10_30
        if any(w in lower_q for w in ["turnaround", "multibagger", "micro cap", "deep value", "debt reduction", "inflection"]):
            return InvestmentHorizon.TURNAROUND_MULTIBAGGER
        if any(w in lower_q for w in ["shock", "war", "chokepoint", "sanction", "redline", "blockade", "crude spike"]):
            return InvestmentHorizon.GEOPOLITICAL_EVENT_SHOCK
        return InvestmentHorizon.SIP_LONG_TERM


class DynamicDiscountRateCalculator:
    """
    Dynamically couples geopolitical and macroeconomic risk scores to equity
    discount rates (Cost of Equity Ke / WACC), with domestic SIP liquidity buffering.
    """

    SECTOR_SENSITIVITIES: Dict[str, float] = {
        # High vulnerability to crude oil, freight rates, and import currency shocks
        "PAINTS": 1.45,
        "TYRES": 1.35,
        "AVIATION": 1.50,
        "SPECIALTY_CHEMICALS": 1.25,
        "OIL_MARKETING_OMC": 1.40,
        
        # Moderate vulnerability
        "AUTOMOBILE": 1.10,
        "CONSUMER_DURABLES": 1.05,
        "CAPITAL_GOODS": 1.00,
        "BANKING_NBFC": 0.95,
        "IT_SERVICES": 0.85,
        "PHARMACEUTICALS": 0.75,
        
        # Beneficiaries / Resilient to geopolitical tension
        "DEFENSE": 0.40,
        "DOMESTIC_UPSTREAM_OIL": 0.50,
        "MINING_METALS": 0.70,
        "PUBLIC_INFRASTRUCTURE": 0.80,
    }

    @classmethod
    def get_sector_sensitivity(cls, sector_name: str) -> float:
        """Retrieves beta sensitivity of a sector to geopolitical/energy shocks."""
        normalized = sector_name.upper().replace(" ", "_").replace("-", "_")
        for key, val in cls.SECTOR_SENSITIVITIES.items():
            if key in normalized or normalized in key:
                return val
        return 1.00

    @classmethod
    def calculate_adjusted_discount_rate(
        cls,
        base_ke: float,
        geopolitical_risk_score: float,
        sector_name: str,
        dii_sip_buffer_ratio: float = 0.70,
    ) -> Dict[str, Any]:
        """
        Computes the adjusted discount rate Ke for DCF models:
        Delta_Ke = alpha * GeoRisk * Sensitivity * (1.0 - dii_sip_buffer_ratio * DomesticResilience)
        
        Parameters:
        - base_ke: Baseline Cost of Equity (e.g. 12.0%).
        - geopolitical_risk_score: Normalized geopolitical risk [0.0 to 1.0].
        - sector_name: Target industry sector.
        - dii_sip_buffer_ratio: Domestic mutual fund SIP absorption factor (default 0.70).
        """
        sensitivity = cls.get_sector_sensitivity(sector_name)
        
        # Alpha scale factor: 1.0 risk score produces maximum +2.5% discount rate expansion
        alpha = 2.50
        
        # Net impact dampened by continuous domestic liquidity absorption
        net_risk_premium = round(alpha * geopolitical_risk_score * sensitivity * (1.0 - (dii_sip_buffer_ratio * 0.40)), 3)
        adjusted_ke = round(base_ke + net_risk_premium, 3)

        return {
            "base_ke_percent": base_ke,
            "geopolitical_risk_score": geopolitical_risk_score,
            "sector_name": sector_name,
            "sector_sensitivity": sensitivity,
            "dii_sip_buffer_ratio": dii_sip_buffer_ratio,
            "geopolitical_risk_premium_percent": net_risk_premium,
            "adjusted_ke_percent": adjusted_ke,
            "valuation_multiple_compression_factor": round(base_ke / adjusted_ke, 3),
        }

```

## Module: `geo_engine/core/models.py`

```python
"""
Data models and type definitions for the Geo-Engine.
Defines immutable representations for summits, financial flows, kinesics,
negative-space clauses, lens evaluations, and synthesized intelligence reports.
"""

import os
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, computed_field, model_validator


def get_system_reference_date() -> datetime:
    """
    Centralized runtime clock provider to prevent temporal drift across modules.
    Reads SYSTEM_REFERENCE_DATE environment variable (ISO format) if set,
    otherwise defaults to current UTC datetime.
    """
    env_date = os.getenv("SYSTEM_REFERENCE_DATE")
    if env_date:
        try:
            return datetime.fromisoformat(env_date)
        except Exception:
            pass
    # Default baseline reference date for deterministic 2026 horizon modeling
    return datetime(2026, 9, 14, 0, 0, 0)



class EpistemicTier(int, Enum):
    """
    Strict truth arbitration hierarchy.
    Lower numerical values represent higher epistemic priority and supersede higher tiers.
    TIER_0 represents an explicit lack of empirical evidence (degraded / null state).
    """
    TIER_0_INSUFFICIENT_EVIDENCE = 0 # Explicit lack of verifiable empirical telemetry
    TIER_1_PHYSICAL = 1              # Physical reality: troops, oil barrels, chokepoints, hardware
    TIER_2_FINANCIAL = 2             # Verified financial flows: Central bank entries, VOSTRO clearing
    TIER_3_SOVEREIGN_REDLINES = 3    # Formal treaties, statutory law, military alliances, borders
    TIER_4_KINESICS = 4              # Protocol-subtracted micro-signals, posture, spatial vectors
    TIER_5_COMMUNIQUE_PR = 5         # Public declarations, ceremonial photoshoots, state press releases


class TemporalMode(str, Enum):
    """Temporal horizon classification to prevent future-data hallucinations."""
    EMPIRICAL_HISTORICAL = "empirical_historical"  # Past verified events with full archival data
    LIVE_VERIFIED = "live_verified"                # Ongoing events with real-time ingested feeds
    PROSPECTIVE_SCENARIO = "prospective_scenario"  # Future/horizon events (e.g., 2026) modeled game-theoretically


class FinancialFlow(BaseModel):
    """Represents a bilateral or multilateral capital or trade commitment."""
    source_country: str
    target_country: str
    project_name: str
    nominal_mou_usd: float = Field(default=0.0, description="Announced headline figure in USD")
    is_binding_contract: bool = Field(default=False, description="True if legal CapEx contract signed with escrow/budget line")
    clearing_currency: str = Field(default="USD", description="Currency used for trade settlement")
    vostro_nostro_operational: bool = Field(default=False, description="True if operational bilateral bank clearing exists")
    secondary_sanctions_risk_score: float = Field(default=0.0, ge=0.0, le=1.0, description="0=none, 1=severe OFAC risk")

    @computed_field
    @property
    def effective_capex_usd(self) -> float:
        """
        Applies the 85% haircut rule on unfinanced, non-binding MOUs.
        If binding, haircut is reduced based on secondary sanctions discount.
        """
        if not self.is_binding_contract:
            # 85% haircut on headline MOUs
            base = self.nominal_mou_usd * 0.15
        else:
            base = self.nominal_mou_usd

        # Sanctions discount
        discount = 1.0 - (self.secondary_sanctions_risk_score * 0.5)
        return round(base * max(0.0, discount), 2)


class KinesicObservation(BaseModel):
    """Represents a structured kinesic/proxemic observation during a summit interaction."""
    actor_primary: str
    actor_secondary: str
    setting: str = Field(..., description="'formal_photocall', 'bilateral_table', or 'unscripted_corridor'")
    protocol_mandated: bool = Field(default=False, description="True if position/posture is compulsory by state protocol")
    handshake_torque_vector: str = Field(default="neutral_vertical", description="'proactive_forward', 'neutral_vertical', 'defensive_withdrawn'")
    torso_angle_degrees: float = Field(default=0.0, description="0 = directly facing, 90 = angled away towards exit")
    residual_tension_score: float = Field(default=0.0, ge=0.0, le=1.0, description="0.0=relaxed/natural, 1.0=extreme rigid tension")
    micro_expression_flag: str = Field(default="neutral_resting", description="'duchenne_smile', 'jaw_clench', 'gaze_avoidance', 'neutral_resting'")
    sartorial_colour_code: str = Field(default="neutral_charcoal", description="'saffron_civilizational', 'midnight_institutional', 'olive_tactical', 'neutral_charcoal'")
    prosodic_pause_index: float = Field(default=0.0, ge=0.0, le=1.0, description="Pause latency before key sovereign nouns: 0.0=fluid, 1.0=severe hesitation")
    proxemic_distance_tier: str = Field(default="bilateral_parity", description="'intimate_embrace', 'bilateral_parity', 'asymmetric_distant'")
    facs_action_units: Dict[str, float] = Field(default_factory=dict, description="Facial Action Coding System Action Units e.g. AU04, AU06, AU12, AU24 (0.0 to 1.0)")
    notes: Optional[str] = None

    @computed_field
    @property
    def genuine_warmth_index(self) -> float:
        """
        Calculates residual warmth after protocol baseline subtraction.
        If mandated by protocol, high warmth is heavily discounted.
        Integrates prosodic pause latency and spatial proxemic distance.
        """
        if self.protocol_mandated:
            # Protocol discount: Staged posture cannot be assumed as genuine affinity
            raw_warmth = (1.0 - self.residual_tension_score) * 0.3
        else:
            raw_warmth = (1.0 - self.residual_tension_score)

        if self.torso_angle_degrees > 45.0:
            raw_warmth *= 0.6
        if self.micro_expression_flag == "jaw_clench" or self.micro_expression_flag == "gaze_avoidance":
            raw_warmth *= 0.3
        if self.prosodic_pause_index > 0.6:
            raw_warmth *= (1.0 - (self.prosodic_pause_index - 0.6) * 0.5)
        if self.proxemic_distance_tier == "intimate_embrace":
            raw_warmth = min(1.0, raw_warmth * 1.15)
        elif self.proxemic_distance_tier == "asymmetric_distant":
            raw_warmth *= 0.75

        if self.facs_action_units:
            au24 = self.facs_action_units.get("AU24", 0.0)
            if au24 > 0.5:
                raw_warmth *= (1.0 - au24 * 0.5)
            au12 = self.facs_action_units.get("AU12", 0.0)
            au06 = self.facs_action_units.get("AU06", 0.0)
            if au12 > 0.6 and au06 < 0.25:
                raw_warmth *= 0.50

        return round(max(0.0, min(1.0, raw_warmth)), 3)


class CommuniqueClause(BaseModel):
    """Represents an individual clause parsed from a summit declaration."""
    clause_id: str
    category: str = Field(..., description="'energy', 'finance', 'security', 'institutional_reform', 'territorial'")
    raw_text: str
    present_in_current_summit: bool = True
    historical_baseline_present: bool = True
    dilution_status: str = Field(default="retained_full", description="'retained_full', 'diluted_passive', 'omitted_negative_space'")
    omission_significance: Optional[str] = None


class LensEvaluation(BaseModel):
    """Result of an individual specialized lens analysis."""
    lens_name: str
    alignment_score: float = Field(..., ge=-1.0, le=1.0, description="-1.0 = deep friction/hostile, +1.0 = deep synergy")
    confidence: float = Field(..., ge=0.0, le=1.0)
    primary_epistemic_tier: EpistemicTier
    key_findings: List[str] = Field(default_factory=list)
    hard_metrics: Dict[str, Any] = Field(default_factory=dict)
    evidence_status: str = Field(default="sufficient", description="'sufficient', 'degraded', 'insufficient'")


class MemberCountryAudit(BaseModel):
    """Full 4-dimensional audit for a member state."""
    country_name: str
    public_domestic_narrative: str
    geopolitical_yield: str
    hard_cash_yield_usd: float = 0.0
    concessions_or_vulnerabilities: str
    strategic_autonomy_score: float = Field(default=0.5, ge=0.0, le=1.0)
    key_bilateral_postures: Dict[str, str] = Field(default_factory=dict)


class EventType(str, Enum):
    """Categorizes the primary nature of a strategic event."""
    SUMMIT = "SUMMIT"
    BORDER_SECURITY = "BORDER_SECURITY"
    BORDER_MILITARY = "BORDER_MILITARY"
    GEO_ECONOMIC = "GEO_ECONOMIC"
    CIVILIZATIONAL_CRISIS = "CIVILIZATIONAL_CRISIS"
    HYBRID_WARFARE = "HYBRID_WARFARE"
    STRATEGIC_EVENT = "STRATEGIC_EVENT"


class StrategicEvent(BaseModel):
    """Generalized model for any strategic geopolitical, economic, or security event."""
    title: str = "Strategic Event"
    year: int = 2026
    event_type: EventType = EventType.SUMMIT
    primary_region: str = "Global"
    target_countries: List[str] = Field(default_factory=list)
    focal_date: Optional[str] = None
    temporal_mode: TemporalMode = TemporalMode.PROSPECTIVE_SCENARIO
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SummitEvent(StrategicEvent):
    """Metadata and participating framework for a summit (fully backward compatible)."""
    summit_name: str = ""
    host_country: str = "Multilateral"
    location: str = "TBD"
    member_countries: List[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def sync_summit_fields(cls, values: Any) -> Any:
        if isinstance(values, dict):
            if "summit_name" in values and "title" not in values:
                values["title"] = values["summit_name"]
            elif "title" in values and ("summit_name" not in values or not values["summit_name"]):
                values["summit_name"] = values["title"]
            if "member_countries" in values and "target_countries" not in values:
                values["target_countries"] = values["member_countries"]
            elif "target_countries" in values and ("member_countries" not in values or not values["member_countries"]):
                values["member_countries"] = values["target_countries"]
        return values


class SummitAnalysisReport(BaseModel):
    """Final de-sanitized multilateral intelligence synthesis."""
    event: Union[SummitEvent, StrategicEvent]

    lens_evaluations: List[LensEvaluation] = Field(default_factory=list)
    negative_space_synopsis: List[str] = Field(default_factory=list)
    country_ledgers: List[MemberCountryAudit] = Field(default_factory=list)
    kinesic_forensics: List[KinesicObservation] = Field(default_factory=list)
    hard_money_audit: Dict[str, Any] = Field(default_factory=dict)
    civilizational_synthesis: Dict[str, str] = Field(default_factory=dict)
    strategic_resilience_matrix: Dict[str, Any] = Field(default_factory=dict)
    ach_evaluation: Optional[Dict[str, Any]] = None
    overall_confidence_score: float = Field(default=0.8)
    diagnostic_encounter_id: Optional[str] = None
    epistemic_arbitration_log: List[str] = Field(default_factory=list)
    causal_shock_propagation: Dict[str, Any] = Field(default_factory=dict)
    layman_intuitive_summary: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")

    @classmethod
    def _remap_legacy_tier_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            mapping = {
                "tier1_negative_space_synopsis": "negative_space_synopsis",
                "tier2_country_ledgers": "country_ledgers",
                "tier3_kinesic_forensics": "kinesic_forensics",
                "tier4_hard_money_audit": "hard_money_audit",
                "tier5_civilizational_inner_meaning": "civilizational_synthesis",
            }
            for old_key, new_key in mapping.items():
                if old_key in data and new_key not in data:
                    data[new_key] = data[old_key]
        return data

    @property
    def tier1_negative_space_synopsis(self) -> List[str]:
        return self.negative_space_synopsis

    @property
    def tier2_country_ledgers(self) -> List[MemberCountryAudit]:
        return self.country_ledgers

    @property
    def tier3_kinesic_forensics(self) -> List[KinesicObservation]:
        return self.kinesic_forensics

    @property
    def tier4_hard_money_audit(self) -> Dict[str, Any]:
        return self.hard_money_audit

    @property
    def tier5_civilizational_inner_meaning(self) -> Dict[str, str]:
        return self.civilizational_synthesis

```

## Module: `geo_engine/core/query_parser.py`

```python
"""
Dynamic Query Parser and Strategic Intent Extractor.
Parses arbitrary natural language queries into structured analytical instructions,
extracting entities (countries, leaders, summits), temporal horizons, and prioritized lens foci.
"""

import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field



class StrategicQuery(BaseModel):
    """Structured analytical specification derived from an arbitrary user prompt."""
    raw_prompt: str
    target_summit: str = Field(default="Multilateral Summit")
    target_event: str = Field(default="Strategic Event")
    event_type: str = Field(default="SUMMIT")
    focal_date: Optional[str] = None
    year: int = Field(default=2026)
    target_countries: List[str] = Field(default_factory=list)
    target_leaders: List[str] = Field(default_factory=list)
    prioritized_lenses: List[str] = Field(default_factory=list)
    requires_kinesics: bool = False
    requires_cash_audit: bool = False
    requires_negative_space: bool = False
    requires_civilizational_depth: bool = False
    requires_india_timeline: bool = False
    requires_demographic_audit: bool = False
    requires_minerals_audit: bool = False
    requires_lawfare_audit: bool = False
    requires_chronology_arbitration: bool = False
    requires_abyssal_sovereignty: bool = False
    requires_trophic_biosecurity: bool = False
    requires_cognitive_sovereignty: bool = False
    requires_bullion_audit: bool = False
    requires_insurgency_audit: bool = False
    requires_quantum_statecraft: bool = False
    requires_grayzone_micro_signal: bool = False
    requires_pnt_autonomy: bool = False
    requires_ai_governance: bool = False
    requires_proxy_warfare: bool = False
    requires_textual_triangulation: bool = False
    requires_media_capture: bool = False
    requires_hydro_weaponization: bool = False
    requires_antiquity_restitution: bool = False
    requires_diaspora_sanctuary: bool = False
    requires_precious_metals: bool = False
    requires_hydrocarbon_chokepoints: bool = False
    requires_cognitive_resilience: bool = False
    requires_nuclear_autonomy: bool = False
    requires_bop_shield: bool = False
    requires_electoral_polarization: bool = False
    requires_refinery_sabotage: bool = False
    requires_hnwi_capital: bool = False
    requires_gold_repatriation: bool = False
    requires_multi_agent_consensus: bool = False
    requires_paleogenomics: bool = False
    requires_epistemic_triangulation: bool = False
    requires_soil_resilience: bool = False
    requires_dharmic_sovereignty: bool = False
    requires_sectoral_rotation: bool = False
    requires_island_net_security: bool = False
    requires_cbdc_surveillance: bool = False
    requires_interagency_synergy: bool = False
    requires_bank_crar: bool = False
    requires_bureaucratic_friction: bool = False
    requires_gan_radar: bool = False
    requires_high_altitude_airlift: bool = False
    requires_bigtech_algorithmic_sovereignty: bool = False
    requires_sacred_economy: bool = False
    requires_outward_asset_capture: bool = False
    requires_archaeo_astronomy: bool = False
    requires_black_projects: bool = False
    requires_trans_himalayan_hydrology: bool = False
    requires_predatory_dumping: bool = False
    requires_apaurusheya_epistemic: bool = False
    requires_sacred_heritage_encroachment: bool = False
    requires_narrative_inversion: bool = False
    requires_malacca_chokepoint: bool = False
    requires_ritual_ecological_sovereignty: bool = False
    requires_dharmic_constitutionalism: bool = False
    requires_partition_demystification: bool = False
    requires_canonical_epic_fidelity: bool = False
    requires_theological_apostasy_velocity: bool = False
    requires_aurobindonian_integration: bool = False
    requires_shastric_dietary_plurality: bool = False
    requires_archival_primary_source: bool = False
    requires_academic_gatekeeping: bool = False
    requires_succession_continuity: bool = False
    requires_linguistic_sprachbund: bool = False
    requires_indigenous_stem: bool = False
    requires_subaltern_memory: bool = False
    requires_industrial_attrition: bool = False
    requires_imperial_debt_overreach: bool = False
    requires_colonial_drain_extraction: bool = False
    requires_basel_gold: bool = False
    requires_mnemonic_fidelity: bool = False
    requires_mitrokhin_deep_state: bool = False
    requires_puranic_boundary: bool = False
    requires_polemics_ratio: bool = False
    requires_kishkindha_geography: bool = False
    requires_vedic_decolonization: bool = False
    requires_quantum_spacetime: bool = False
    requires_semiconductor_antitrust: bool = False
    requires_fcra_ecclesiastical: bool = False
    requires_cinematic_sacrality: bool = False
    requires_infrastructure_capex_multiplier: bool = False
    requires_classical_bullion_trade: bool = False
    requires_asymmetric_statutory_lawfare: bool = False
    requires_cryptographic_decentralization: bool = False
    requires_hormuz_escalation: bool = False
    requires_eurodollar_shadow_liquidity: bool = False
    requires_black_swan_disruption: bool = False
    requires_sovereign_gold_velocity: bool = False
    requires_geopolitical_speech_forensics: bool = False
    requires_sovereign_public_interest: bool = False
    requires_adversary_timing_correlation: bool = False
    requires_documentary_provenance: bool = False
    requires_bear_raid_derivative: bool = False
    requires_offshore_debt_covenant: bool = False
    requires_exfiltration_sanctuary: bool = False
    requires_retaliation_threat: bool = False
    requires_vigilance_remedy: bool = False
    requires_speech_kinesic_chromatic: bool = False
    requires_speech_omission: bool = False
    requires_tbml_customs: bool = False
    requires_defense_scada_tamper: bool = False
    requires_cultural_sacrality_breach: bool = False
    requires_perjury_retributive_liability: bool = False
    requires_qdt_whistleblower: bool = False
    requires_sovereign_capex_impact: bool = False
    requires_bis_hidden_fx_swap: bool = False
    requires_offshore_ubo_shell: bool = False
    requires_speech_to_balance_sheet_divergence: bool = False
    requires_kinesic_contextual_baseline: bool = False
    requires_chanakya_neeti_upadha: bool = False
    requires_kautilya_mandala_shadgunya: bool = False
    requires_krishna_rajadharma_exhaustion: bool = False
    requires_cloud_monopoly_fragility: bool = False
    requires_cognitive_deception_misdirection: bool = False
    requires_counter_intel_honeytrap: bool = False
    requires_maritime_net_security: bool = False
    requires_false_flag_narrative: bool = False
    requires_sovereign_cyber_extortion: bool = False
    requires_maritime_port_dual_use: bool = False
    requires_revealed_preference_divergence: bool = False
    requires_sovereign_debt_syndicate: bool = False
    requires_asymmetric_weapon_proliferation: bool = False
    requires_legacy_infra_obsolescence: bool = False
    requires_speculative_capex_overhang: bool = False
    requires_subnational_fragmentation_lawfare: bool = False
    requires_civilizational_epistemic_integrity: bool = False
    requires_algorithmic_cognitive_subversion: bool = False
    requires_critical_scada_hardware_backdoor: bool = False
    requires_circular_venture_valuation: bool = False
    requires_monopoly_patent_suppression: bool = False
    requires_sub_replacement_demographic_extinction: bool = False
    requires_physical_capex_multiplier: bool = False
    requires_open_system_asymmetric_infiltration: bool = False
    requires_dynastic_shadow_cabinet: bool = False
    requires_superpower_naval_coercion: bool = False
    requires_semiconductor_executive_kompromat: bool = False
    requires_media_intelligence_leak_timing: bool = False
    requires_generative_media_hegemony: bool = False
    requires_silicon_microcode_killswitch: bool = False
    requires_gpu_debt_contagion: bool = False
    # Phases 396-415: Sovereign Asymmetric War, Balance-Sheet Realism & Civilizational Sovereignty Matrix
    requires_informal_sector_divergence: bool = False
    requires_pboc_lgfv_liquidity_trap: bool = False
    requires_asymmetric_air_defense_cost_exchange: bool = False
    requires_hypersonic_glide_penetration: bool = False
    requires_sovereign_platform_regulatory_defiance: bool = False
    requires_institutional_cartel_cross_shareholding: bool = False
    requires_msme_solvency_asphyxiation: bool = False
    requires_nuclear_launch_under_attack_latency: bool = False
    requires_border_state_narco_fiscal_subversion: bool = False
    requires_trilateral_superpower_condominium_exclusion: bool = False
    requires_quantum_hndl_vulnerability: bool = False
    requires_diplomatic_nonverbal_optics: bool = False
    requires_cultural_religious_grayzone_lawfare: bool = False
    requires_critical_mineral_weaponization: bool = False
    requires_agrochemical_food_weaponization: bool = False
    requires_aviation_transit_slot_cartel: bool = False
    requires_airborne_command_survivability: bool = False
    requires_sub_tactical_honeytrap_espionage: bool = False
    requires_naval_electronic_warfare_suppression: bool = False
    requires_civilizational_epistemic_historiography: bool = False
    # Phases 416-433: Sovereign Forensic Sieves & Strategic Council Titans (18 Flags)
    requires_asymmetric_scada_blackout: bool = False
    requires_synchronized_media_cartel: bool = False
    requires_deep_state_banking_lawfare: bool = False
    requires_directed_energy_weapon: bool = False
    requires_multilateral_alliance_autonomy: bool = False
    requires_offshore_banking_repatriation: bool = False
    requires_foreign_intel_penetration: bool = False
    requires_cognitive_atrophy_displacement: bool = False
    requires_demographic_border_fortification: bool = False
    requires_algorithmic_faceless_procurement: bool = False
    requires_investigative_forensics_negative_space: bool = False
    requires_sovereign_debt_rollover_risk: bool = False
    requires_asymmetric_subversion_counter_penetration: bool = False
    requires_sovereign_capex_escape_velocity: bool = False
    requires_multipolar_hedging_reciprocal_leverage: bool = False
    requires_credit_rating_cartel_bias: bool = False
    requires_civilizational_jurisprudence_decolonial: bool = False
    requires_empirical_falsification_cryptographic: bool = False
    # Phases 434-440: Semiotic Iconography, Global Polycrisis Cascades & Sovereign Resilient Sieves
    requires_semiotic_deconstruction: bool = False
    requires_polycrisis_cascade: bool = False
    requires_cultural_religious_grayzone_subversion: bool = False
    requires_glp1_metabolic_shift: bool = False
    requires_leo_orbital_weaponization: bool = False
    requires_taiwan_semiconductor_choke: bool = False
    requires_electoral_lawfare_polarization: bool = False
    # Phases 441-447: Sovereign Forensic Sieves & Multilateral Autonomy Tensors
    requires_tripolar_condominium: bool = False
    requires_ai_labor_displacement: bool = False
    requires_diaspora_subversion: bool = False
    requires_gpu_export_chokepoint: bool = False
    requires_reer_appreciation_friction: bool = False
    requires_supranational_deep_state: bool = False
    requires_bullion_cyber_sovereignty: bool = False
    # Phases 448-449: Horizon Polycrisis & Multilateral Defense Interoperability
    requires_economist_polycrisis: bool = False
    requires_defense_interoperability: bool = False
    # Phase 450: Subcontinental Proxy Risk & Silicon Venture Oligarchies
    requires_subcontinental_proxy_risk: bool = False
    # Phase 454: Sovereign Cognitive Subterranean & Kinetic Interoperability
    requires_sovereign_hyper_resilience: bool = False
    # Phases 455-460 Capstones: Epistemic Validation & Sovereign Industrial Propulsion
    requires_epistemic_validation: bool = False
    requires_industrial_propulsion: bool = False
    # Phases 461-464: Sovereign Bullion/Marine/Brand, Impossible Trinity/OPSEC, Constitutional/Grayzone, Mother-Machine/Sonar/Hydrocide
    requires_bullion_marine_brand_sovereignty: bool = False
    requires_impossible_trinity_tbml_opsec: bool = False
    requires_constitutional_grayzone_proxy: bool = False
    requires_mother_machine_sonar_hydrocide: bool = False
    speaker_profiles: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_threshold: float = Field(default=0.75, ge=0.0, le=1.0)



_COMPILED_WORD_PATTERNS: Dict[str, re.Pattern] = {}


def get_word_boundary_pattern(kw: str) -> re.Pattern:
    """Returns a compiled regex pattern matching kw at discrete word boundaries."""
    kw_key = kw.strip().lower()
    if kw_key not in _COMPILED_WORD_PATTERNS:
        escaped = re.escape(kw_key)
        pattern_str = r"(?<!\w)" + escaped + r"(?!\w)"
        _COMPILED_WORD_PATTERNS[kw_key] = re.compile(pattern_str, re.IGNORECASE)
    return _COMPILED_WORD_PATTERNS[kw_key]


class QueryParser:
    """Extracts geopolitical entities, temporal horizons, and analytical intent from raw text."""

    @classmethod
    def matches_keyword(cls, text: str, keyword: str) -> bool:
        r"""
        Determines whether a keyword matches within text with word-boundary isolation.
        Uses regex lookbehind/lookahead `(?<!\w)pattern(?!\w)` so short tokens
        (e.g., 'ai', 'sc', 'lac') do not match within larger words ('said', 'scale', 'black').
        """
        if not keyword or not text:
            return False
        return bool(get_word_boundary_pattern(keyword).search(text))

    SUMMIT_PATTERNS: Dict[str, str] = {
        r"\bbrics\b": "BRICS Summit",
        r"\bsco\b|shanghai cooperation": "SCO Summit",
        r"\bg20\b": "G20 Summit",
        r"\bg7\b": "G7 Summit",
        r"\bquad\b": "Quad Leaders Summit",
        r"\basean\b": "ASEAN Summit",
        r"\bbimstec\b": "BIMSTEC Summit",
        r"\bsaarc\b": "SAARC Regional Forum",
        r"\bimec\b": "IMEC Corridor Forum",
        r"\bunga\b|united nations": "UN General Assembly",
    }

    COUNTRY_PATTERNS: Dict[str, str] = {
        r"\bindia\b|\bindian\b|\bbharat\b|\bbharatiya\b": "India",
        r"\bchina\b|\bchinese\b|\bbeijing\b": "China",
        r"\brussia\b|\brussian\b|\bmoscow\b": "Russia",
        r"\bbrazil\b|\bbrazilian\b": "Brazil",
        r"\bsouth africa\b|\bsouth african\b": "South Africa",
        r"\biran\b|\biranian\b|\btehran\b": "Iran",
        r"\bsaudi\b|\bsaudi arabia\b|\briyadh\b": "Saudi Arabia",
        r"\buae\b|\bemirates\b|\bdubai\b|\babu dhabi\b": "UAE",
        r"\begypt\b|\begyptian\b|\bcairo\b": "Egypt",
        r"\bethiopia\b|\bethiopian\b|\baddis\b": "Ethiopia",
        r"\bbangladesh\b|\bbangladeshi\b|\bdhaka\b": "Bangladesh",
        r"\bnepal\b|\bnepali\b|\bkathmandu\b": "Nepal",
        r"\bsri lanka\b|\bsri lankan\b|\bcolombo\b": "Sri Lanka",
        r"\bmyanmar\b|\bburma\b|\bburmese\b": "Myanmar",
        r"\bpakistan\b|\bpakistani\b|\bislamabad\b": "Pakistan",
        r"\bmaldives\b|\bmaldivian\b|\bmale\b": "Maldives",
        r"\bbhutan\b|\bbhutanese\b|\bthimphu\b": "Bhutan",
        r"\bspain\b|\bspanish\b|\bmadrid\b|\bandalucia\b": "Spain",
        r"\bmorocco\b|\bmoroccan\b|\brabat\b": "Morocco",
        r"\btaiwan\b|\btaiwanese\b|\btaipei\b": "Taiwan",
        r"\bukraine\b|\bukrainian\b|\bkyiv\b": "Ukraine",
        r"\busa\b|\bunited states\b|\bamerica\b|\bamerican\b|\bwashington\b": "USA",
    }

    LEADER_PATTERNS: Dict[str, str] = {
        r"\bmodi\b": "Narendra Modi",
        r"\bxi\b|\bxi jinping\b": "Xi Jinping",
        r"\bputin\b": "Vladimir Putin",
        r"\blula\b": "Luiz Inacio Lula da Silva",
        r"\bpezeshkian\b": "Masoud Pezeshkian",
        r"\bmbs\b|\bmohammed bin salman\b": "Mohammed bin Salman",
        r"\bmbz\b": "Mohammed bin Zayed",
        r"\bsisi\b": "Abdel Fattah el-Sisi",
        r"\bhasina\b|\bsheikh hasina\b": "Sheikh Hasina",
        r"\byunus\b|\bmuhammad yunus\b": "Muhammad Yunus",
        r"\bnetaji\b|\bsubhas\b|\bsubhas chandra bose\b": "Netaji Subhas Chandra Bose",
        r"\boli\b|\bk\.?p\.?\s*oli\b": "K.P. Sharma Oli",
        r"\bdissanayake\b|\banura\b": "Anura Kumara Dissanayake",
        r"\bmuizzu\b": "Mohamed Muizzu",
        r"\bdoval\b|\bajit doval\b": "Ajit Doval",
        r"\bhimanta\b|\bhimanta biswa sarma\b|\bhbs\b": "Himanta Biswa Sarma",
        r"\bneeraj\b|\bneeraj atri\b": "Neeraj Atri",
        r"\bambedkar\b|\bbhimrao\b|\bbabasaheb\b": "B.R. Ambedkar",
        r"\bvandyke\b|\bvan dyke\b|\bmatthew vandyke\b": "Matthew VanDyke",
        r"\bansari\b|\bhamid ansari\b": "Hamid Ansari",
        r"\bsrijan\b|\bsrijan pal singh\b": "Srijan Pal Singh",
        r"\bsai deepak\b|\bj\.?\s*sai deepak\b": "J. Sai Deepak",
        r"\bmeenakshi\b|\bmeenakshi jain\b|\bdr meenakshi jain\b": "Dr. Meenakshi Jain",
        r"\bami\b|\bami ganatra\b": "Ami Ganatra",
        r"\bgaurav arya\b|\bmajor gaurav arya\b|\bmajor arya\b": "Major Gaurav Arya",
    }

    MILITARY_BORDER_KEYWORDS: List[str] = [
        "lac", "loc", "troop", "troops", "deployment", "standoff", "clash", "skirmish",
        "patrol", "patrolling", "artillery", "infantry", "galwan", "doklam", "tawang", "depasang", "demchok"
    ]
    DEMOGRAPHIC_BORDER_KEYWORDS: List[str] = [
        "infiltrat", "migrant", "migration", "ceuta", "melilla", "refugee",
        "asylum", "demographic", "andalucia", "schengen", "border fence", "human trafficking"
    ]

    COLLOQUIAL_ROUTING_MAP: Dict[str, List[str]] = {
        "food_security": ["khana peena", "roti", "kisan", "annadata", "fasal", "gehun", "chawal", "anaj", "food security", "food crisis", "grain shortage", "fertilizer subsidy", "ration", "crop failure", "urea shortage", "potash supply"],
        "military_readiness": ["fauji", "sena", "goli", "barood", "hathiyar", "fouj", "topkhana", "jang", "drone burnout", "cost exchange", "sm-2", "sm-6"],
        "geo_economist": ["dhandha", "paisa", "rupaya", "kamai", "vyapar", "karz", "byaj"],
        "cash_flow": ["munafe", "kharcha", "jama", "nikasi", "hundi"],
        "propaganda": ["afwah", "dhokhadhadi", "farzi khabar", "bhatkana", "propoganda", "hisab chukta", "hisaab chukta", "hisab karega", "settle scores", "oratorical priming", "antithetical priming"],
        "institutional_lawfare": ["kacheri", "adalat", "vakil", "mudda", "chori", "dharna", "samundari kanoon", "eez kanoon", "sc st act", "section 18a", "kashinath", "general category", "ancestral sin"],
        "hybrid_covert": ["vandyke", "van dyke", "mercenary trainer", "sons of liberty", "camp victoria", "managed off-ramp", "sovereign compromise", "hamid ansari", "tehran raw", "nusrat mirza"],
        "petro_logistics": ["tel", "petrol", "diesel", "jahaz", "tatt", "samundar", "sagar"],
        "subsea_cables": ["samundari tar", "subsea tar", "sagar cable", "undersea internet", "internet cable", "cable cut", "landing station", "undersea fiber", "data corridor"],
        "astro_politics": ["antriksh", "graha", "upagraha", "space defense", "space weapon", "orbital asset", "satellite navigation", "isro mission"],
        "civilizational": ["itihaas", "purana", "puratan", "parampara", "sanskriti"],
        "demographic_infiltration": ["diaspora under siege", "texas hanuman", "sb 403", "caste lawfare"],
        "deep_tech": ["stem dilution", "grievance curricula", "lab capex"]
    }

    LENS_KEYWORDS: Dict[str, List[str]] = {
        "deep_tech": ["ai", "deep tech", "quantum", "compute", "algorithm", "frontier tech", "supercomputer", "synthetic", "biotech", "avionics", "digital leash", "odin", "alis", "mission data file", "electronic sovereignty", "stem dilution", "grievance curricula", "engineering capex", "technological dividend", "demographic dividend liability", "hard engineering", "lab capex"],
        "history": ["treaty", "precedent", "historical", "panchsheel", "1962", "1971", "1993", "cold war", "bretton woods", "bandung", "partition", "kargil", "balakot", "galwan", "pokhran", "sindoor", "sykes-picot", "1947", "1998", "1999", "somnath", "nalanda", "tarain", "chola", "srivijaya", "shivaji", "swarajya", "reversal", "millennial", "1000 year", "watson", "bernays", "mkultra", "mockingbird", "who code", "1920", "1928", "1953", "1981", "nilesh oak", "arundhati vasistha", "5561 bce", "3067 bce", "3102 bce", "bori critical edition", "sanauli chariot", "saraswati desiccation", "chronology arbitration", "historical timeline", "kahuta", "kanishka", "air india 182", "sriperumbudur", "ic 814", "kandahar hijack", "1993 mumbai blasts", "sinauli", "sanauli", "rakhigarhi", "copper hoard", "ocp", "pgw", "antennae sword", "chariot vs cart", "paleogenomics", "adna", "bsip"],
        "civilizational": ["meaning", "inner meaning", "civilization", "sanatan", "history", "kautilya", "mandala", "rajdharma", "dharmashastra", "smriti", "sadachara", "deshadharma", "kuladharma", "shankaracharya", "peetham", "matha", "parampara", "sampradaya", "dharma", "reversal", "symbolic date", "calendar", "temporal", "panchanga", "swarajya", "nalanda", "saptanga", "swami", "amatya", "janapada", "durga", "kosha", "danda", "seven limbs", "state sovereignty", "itihasa", "itihaasa", "mahabharata timeline", "ramayana timeline", "nilesh oak", "bori", "kali yuga epoch", "paradiplomacy", "sub-national paradiplomacy", "mizo-chin", "chin refugee", "yma", "soli", "sons of liberty", "faith-based contractor", "evangelical corridor", "sinauli", "sanauli", "rakhigarhi", "copper hoard", "ocp", "rigveda 10.18", "inhumation", "shmashana", "paleogenomics", "adna", "sattra", "srimanta sankardev", "batadrava", "gamusa"],
        "geo_economist": ["geo-economic", "geoeconomic", "trilemma", "mundell-fleming", "cips", "mbridge", "swift", "de-dollarization", "dedollarization", "dedollar", "vostro", "current account", "gold reserve", "central bank gold", "sovereign debt", "srva", "trapped rupee", "capital recycling", "vostro recycling", "g-sec reinvestment", "trade gap", "under-invoicing", "china deficit", "gdp discrepancy", "double deflation", "single deflation", "iebr", "fuel tax"],
        "geopolitical": ["geopolitics", "geopolitical", "diplomacy", "diplomatic", "power", "alliance", "rivalry", "border", "lac", "loc", "military", "troops", "standoff", "hedging", "security", "aukus", "imec", "i2u2", "quad", "bri", "belt and road", "game theory", "red team", "counter-move", "escalation spiral", "wargame campaign", "persistent campaign", "wargame session", "siliguri", "chicken's neck", "chickens neck", "chumbi", "doklam", "suwalki", "wakhan", "teesta", "rangpur", "pincer", "chokepoint kinetic"],
        "kinesics": ["bodylanguage", "body language", "photoshoot", "photo", "handshake", "posture", "gaze", "facial", "gamusa", "gamosa", "sartorial", "semiotic", "sartorial dissonance", "theatrical optics", "touch feet", "touching feet", "bowing", "is it true", "deepfake", "morphed", "cropped"],
        "cash_flow": ["cash", "investment", "fdi", "capex", "mou", "currency", "settlement", "money", "vostro", "funding", "npa write-off", "bad loan", "bank recapitalization", "haircut ratio", "ibc resolution", "write-off", "hawala", "d-company", "drone drop", "illicit finance", "crime-terror nexus", "syndicate liquidity", "asset freeze"],
        "propaganda": ["optics", "narrative", "narrative warfare", "viral", "fact check", "fact-check", "message", "propaganda", "spin", "media", "watson", "bernays", "behavioral conditioning", "fear marketing", "anxiety capture", "torches of freedom", "mkultra", "mockingbird", "breast-milk substitutes", "teleological", "social engineering", "engineering of consent", "guilt marketing", "psychological warfare", "turn approver", "approver", "deshdrohi", "vote chori", "vote theft", "hisab chukta", "hisaab chukta", "hisab karega", "settle scores", "karega ki nahi", "antithetical priming", "oratorical priming", "grievance priming"],
        "petro_logistics": ["crude", "oil", "energy", "tanker", "chokepoint", "malacca", "hormuz"],
        "bureaucratic_inertia": ["bureaucracy", "bureaucratic", "press note 3", "veto", "ndrc", "rbi", "mea", "commerce", "regulatory delay", "inter-ministerial", "inertia", "putnam", "two-level game", "domestic backlash", "ugc rollback", "de-reservation", "draft guidelines", "policy rollback", "executive retreat", "clerical overreach", "bureaucratic disconnect"],
        "digital_sovereignty": ["digital sovereignty", "semiconductor", "lithography", "asml", "tsmc", "chip", "chips", "huawei", "5g", "6g", "telecom ban", "navic", "beidou", "gps", "data sovereignty"],
        "hybrid_covert": ["hybrid", "covert", "grey zone", "gray zone", "sabotage", "subversion", "intelligence", "proxy", "espionage", "psyop", "ramming", "shouldering", "bow crossing", "hunain", "pns", "naval standoff", "sub-kinetic", "technical error", "steering failure", "crew error", "inexperience", "diversion", "maskirovka", "competing hypotheses", "ach", "why did it happen", "asymmetric response", "sequential move", "tipping point", "unknown gunmen", "doval", "offensive-defense", "kahuta", "spg", "special protection group", "sriperumbudur", "ic 814", "kandahar", "d-company", "ripudaman", "malik", "nijjar", "sanctuary", "safe haven", "extraterritorial", "vandyke", "van dyke", "matthew vandyke", "soli", "sons of liberty", "camp victoria", "ukrainian drone", "mercenary trainer", "fpv proliferation", "chin national army", "cna", "sovereign compromise", "sovereign asymmetry", "diplomatic deportation", "quattrocchi", "warren anderson", "mercenary off-ramp", "hamid ansari", "tehran raw", "nusrat mirza", "counter-intel vetting", "diplomatic compromise", "diplomatic deep state", "station compromise", "raw network compromise"],
        "india_timeline": ["bangladesh", "hasina", "yunus", "netaji", "ram mandir", "ayodhya", "siliguri", "chicken neck", "teesta", "bimstec", "saarc", "neighborhood", "neighborhood first", "mizoram", "manipur", "chin state", "indo-myanmar", "zokhawthar", "champhai"],
        "demographic_infiltration": ["infiltrat", "migrant", "migration", "ceuta", "melilla", "refugee", "asylum", "demographic", "andalucia", "schengen", "human trafficking", "rangpur", "siliguri", "chicken's neck", "illegal infiltration", "border demographic", "rohingya", "cross-border infiltration", "demographic balance", "border census", "gorukhuti", "char land", "sonowal", "imdt", "external aggression", "batadrava", "diaspora under siege", "sb 403", "caste lawfare", "texas hanuman", "statue of union", "nativist backlash", "h-1b ban", "diaspora fragility", "diaspora backlash", "sugar land"],
        "critical_minerals": ["rare earth", "mineral", "lithium", "cobalt", "semiconductor", "gallium", "germanium", "supply chain", "refining monopoly", "ndfeb", "magnet", "processing monopoly", "rare earth processing", "midstream", "nickel", "graphite", "neodymium", "heavy rare earth", "clean energy minerals", "lithium refinery"],
        "institutional_lawfare": ["fatf", "lawfare", "icc", "icj", "sanctions", "ofac", "asset freeze", "jurisdiction", "blacklisting", "constitution", "constitutional", "article 44", "ucc", "uniform civil code", "waqf", "fcra", "sc/st", "reservation", "fundamental rights", "hrce", "temple control", "judicial activism", "1991 agreement", "colregs", "buffer distance", "maritime accord", "rpa", "representation of the people", "booth level agent", "bla", "special intensive revision", "sir", "electoral roll", "vote chori", "vote theft", "turn approver", "election commission", "election petition", "form 7", "form 8", "form 17c", "voter list", "voter deletion", "default bail", "section 167", "section 188", "foreigners act compounding", "piecemeal chargesheet", "statutory off-ramp", "managed off-ramp", "maritime zone", "act 80", "unclos", "eez", "exclusive economic zone", "contiguous zone", "innocent passage", "transit passage", "fonop", "maritime boundary", "coastal state", "anti-piracy", "sattra", "char land", "batadrava", "gorukhuti", "dhalpur", "waqf board", "section 40", "imdt", "section 8a", "sc st act", "section 18a", "kashinath mahajan", "subhash kashinath", "anticipatory bail denial", "hisab chukta", "ancestral sin", "general category", "caste faultline", "creamy layer", "due process erosion"],
        "food_security": ["food", "food security", "fertilizer", "urea", "dap", "mop", "grain", "wheat", "rice", "famine", "buffer stock", "pds", "agriculture", "export ban", "water security", "monsoon", "groundwater", "indus waters", "teesta", "brahmaputra", "potassium", "fertilizer import", "soil nutrient", "fertilizer dependency", "rice ban", "wheat ban", "onion duty", "price stabilization", "farmer income", "anti-farmer", "grain shortage", "fertilizer subsidy", "caloric intake", "food crisis"],
        "military_readiness": ["military readiness", "orbat", "order of battle", "wwr", "war wastage", "ammunition", "air defense", "s-400", "tejas", "nuclear triad", "deterrence", "escalation ladder", "mobilization", "cyber", "electronic warfare", "dca", "fifth domain", "naval", "warship", "pns", "hunain", "sea control", "sea denial", "ramming", "shouldering", "rudder failure", "hydrodynamic", "seamanship", "watchstander", "mechanical failure", "f-35", "f35", "odin", "alis", "su-57", "su57", "mrfa", "stealth fighter", "digital leash", "kill-switch", "kill switch", "luneburg", "rcs", "radar cross section", "tarang shakti", "jodhpur air base", "avionics sovereignty", "drone burnout", "cost-exchange ratio", "cost exchange", "interceptor exhaustion", "sm-2", "sm-6", "shahed drone", "houthi drone", "magazine depth", "asymmetric drone burnout"],
        "subsea_cables": ["subsea", "subsea cable", "underwater cable", "fiber optic", "submarine cable", "seabed", "seabed mining", "hydrophone", "eez", "polymetallic", "sea cable", "optic fiber", "landing station", "data traffic", "cable severed", "cable damage", "undersea data", "red sea cable", "mumbai landing", "chennai landing", "undersea internet", "subsea communications"],
        "astro_politics": ["space", "satellite", "orbital", "navic", "asat", "anti-satellite", "counter-space", "starlink", "isro", "leo constellation", "space situational awareness", "space program", "space weapon", "orbit", "orbital reconnaissance", "space debris", "project netra", "gsat", "space domain", "space defense", "satellite navigation"],
        "negative_space": ["synopsis", "omitted", "dropped", "communique", "declaration", "text", "agenda", "draft"],
    }

    @classmethod
    def parse(cls, prompt: str) -> StrategicQuery:
        """Parses an arbitrary query string into an actionable StrategicQuery."""
        if not prompt or not isinstance(prompt, str) or not prompt.strip():
            prompt = "Strategic Horizon Analysis"
        # Input envelope: truncate excessive prompt length to prevent ReDoS / memory exhaustion
        if len(prompt) > 5000:
            prompt = prompt[:5000]
        text_lower = prompt.lower()

        # 1. Extract Target Countries first to inform event titles
        matched_countries = []
        for pattern, country in cls.COUNTRY_PATTERNS.items():
            if re.search(pattern, text_lower):
                if country not in matched_countries:
                    matched_countries.append(country)

        # If user asks for "all member countries", populate full BRICS+ default roster
        if "all member" in text_lower or "all country" in text_lower or "one by one" in text_lower:
            matched_countries = [
                "India", "China", "Russia", "Brazil", "South Africa",
                "Iran", "Saudi Arabia", "UAE", "Egypt", "Ethiopia"
            ]

        # 2. Extract Year and Focal Date
        year_match = re.search(r"\b(20[2-3][0-9])\b", text_lower)
        year = int(year_match.group(1)) if year_match else 2026

        date_match = re.search(r"\b(\d{1,2}(?:st|nd|rd|th)?\s+(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?))\b", text_lower)
        if not date_match:
            date_match = re.search(r"\b((?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?)\b", text_lower)
        focal_date = date_match.group(1).title() if date_match else None

        # 3. Detect Summit vs. Non-Summit Crisis Classification
        summit_name = None
        for pattern, name in cls.SUMMIT_PATTERNS.items():
            if re.search(pattern, text_lower):
                summit_name = name
                break

        if summit_name:
            event_type = "SUMMIT"
            summit_full_name = f"{summit_name.split()[0]} {year} Summit"
        elif any(cls.matches_keyword(text_lower, kw) for kw in cls.MILITARY_BORDER_KEYWORDS) or ("border" in text_lower and any(cls.matches_keyword(text_lower, kw) for kw in ["military", "troop", "troops", "army", "pla", "clash", "standoff", "patrolling", "patrol"])):
            event_type = "BORDER_MILITARY"
            c_names = " - ".join(matched_countries[:2]) if matched_countries else "Regional"
            summit_full_name = f"{c_names} Sovereign Border Military Standoff ({year})"
        elif any(cls.matches_keyword(text_lower, kw) for kw in cls.DEMOGRAPHIC_BORDER_KEYWORDS):
            event_type = "BORDER_SECURITY"
            c_name = matched_countries[0] if matched_countries else "Regional"
            summit_full_name = f"{c_name} Border Security & Infiltration Event ({year})"
        elif any(cls.matches_keyword(text_lower, kw) for kw in ["de-dollar", "dollar collapse", "vostro", "currency run", "gold bullion", "bank default"]):
            event_type = "GEO_ECONOMIC"
            summit_full_name = f"Geo-Economic Liquidity & Currency Crisis ({year})"
        elif any(cls.matches_keyword(text_lower, kw) for kw in ["feet", "touch feet", "spiritual", "shirk", "blasphemy", "civilizational crisis", "existential crisis", "famine", "food embargo"]):
            event_type = "CIVILIZATIONAL_CRISIS"
            summit_full_name = f"Civilizational Protocol & Existential Crisis ({year})"
        elif any(cls.matches_keyword(text_lower, kw) for kw in ["fatf", "lawfare", "icc", "icj", "asset freeze"]):
            event_type = "HYBRID_WARFARE"
            summit_full_name = f"Institutional Lawfare & Sanctions Escalation ({year})"
        else:
            event_type = "STRATEGIC_EVENT"
            summit_full_name = f"Strategic Event Analysis ({year})"

        # 4. Extract Target Leaders
        matched_leaders = []
        for pattern, leader in cls.LEADER_PATTERNS.items():
            if re.search(pattern, text_lower):
                if leader not in matched_leaders:
                    matched_leaders.append(leader)

        # 5. Extract Prioritized Lenses
        active_lenses = []
        for lens_name, keywords in cls.LENS_KEYWORDS.items():
            colloquial = cls.COLLOQUIAL_ROUTING_MAP.get(lens_name, [])
            all_kw = keywords + colloquial
            if any(cls.matches_keyword(text_lower, kw) for kw in all_kw):
                active_lenses.append(lens_name)

        # Boolean flags
        req_kinesics = "kinesics" in active_lenses or any(cls.matches_keyword(text_lower, kw) for kw in ["photo", "photoshoot", "bodylanguage", "body language", "touch feet", "touching feet", "is it true", "deepfake", "morphed", "cropped"])
        req_cash = "cash_flow" in active_lenses or any(cls.matches_keyword(text_lower, kw) for kw in ["cash", "investment", "achieve", "achive", "yield"])
        req_neg_space = "negative_space" in active_lenses or any(cls.matches_keyword(text_lower, kw) for kw in ["synopsis", "meeting", "communique", "declaration"])
        req_civilizational = "civilizational" in active_lenses or any(cls.matches_keyword(text_lower, kw) for kw in ["meaning", "deep", "civilization", "sanatan"])
        req_timeline = "india_timeline" in active_lenses or any(cls.matches_keyword(text_lower, kw) for kw in ["bangladesh", "hasina", "netaji", "ram mandir", "siliguri"])
        req_demographic = "demographic_infiltration" in active_lenses or event_type == "BORDER_SECURITY"
        req_minerals = "critical_minerals" in active_lenses
        req_lawfare = "institutional_lawfare" in active_lenses or event_type == "HYBRID_WARFARE"
        req_chronology = (
            any(cls.matches_keyword(text_lower, kw) for kw in [
                "chronology", "timeline dispute", "nilesh oak", "5561 bce", "3067 bce",
                "3102 bce", "arundhati vasistha", "mahabharata date", "ramayana date",
                "bori critical edition", "historical timeline"
            ]) or
            ("timeline" in text_lower and any(cls.matches_keyword(text_lower, w) for w in ["mahabharat", "ramayan", "ancient", "epic", "dating", "dispute", "verdict"]))
        )

        req_abyssal = any(cls.matches_keyword(text_lower, kw) for kw in ["abyssal", "polymetallic", "matsya", "samudrayaan", "seabed", "nodule", "deep submergence"])
        req_trophic = any(cls.matches_keyword(text_lower, kw) for kw in ["trophic", "diclofenac", "vulture", "rabies", "zoonotic", "biosecurity cascade", "scavenger"])
        req_cognitive = any(cls.matches_keyword(text_lower, kw) for kw in ["cognitive enclosure", "antahkarana", "synthetic empathy", "ai colonization", "foreign model", "proprietary ai"])
        req_bullion = any(cls.matches_keyword(text_lower, kw) for kw in ["bullion", "paper gold", "comex", "lbma", "gold repatriation", "tariff arbitrage", "rbi gold", "vault drain"])
        req_insurgency = any(cls.matches_keyword(text_lower, kw) for kw in ["sub-national", "insurgency incubation", "patel vs indira", "partisan blowback", "fringe militant"])
        req_quantum = any(cls.matches_keyword(text_lower, kw) for kw in ["quantum", "superposition", "shannon alignment", "pqc", "quantum statecraft", "qubit"])
        req_grayzone_micro = any(cls.matches_keyword(text_lower, kw) for kw in ["sacred calendar", "waqf", "hr&ce", "street veto", "corridor demographic", "communal friction", "due process asymmetry"])
        req_pnt = any(cls.matches_keyword(text_lower, kw) for kw in ["pnt", "navic", "irnss", "rubidium", "clock drift", "gps denial", "missile cep", "satellite navigation"])
        req_ai_gov = any(cls.matches_keyword(text_lower, kw) for kw in ["flop", "ai safety", "ai governance", "regulatory moat", "open-source suppression", "it margin", "frontier ai"])
        req_proxy = any(cls.matches_keyword(text_lower, kw) for kw in ["operation tupac", "proxy warfare", "narco-hawala", "sleeper cell", "asymmetric attrition"])
        req_textual = any(cls.matches_keyword(text_lower, kw) for kw in ["bori", "valmiki", "vyasa", "critical edition", "textual stratigraphy", "shruti", "smriti", "pop myth", "andhe ka putra"])
        req_media = any(cls.matches_keyword(text_lower, kw) for kw in ["elite media", "underworld capital", "dopamine decay", "short-form", "media capture", "cognitive capture"])
        req_hydro = any(cls.matches_keyword(text_lower, kw) for kw in ["medog", "upper siang", "water bomb", "upstream dam", "hydro weaponization", "dam buffer", "brahmaputra flood"])
        req_antiquity = any(cls.matches_keyword(text_lower, kw) for kw in ["antiquity", "murti", "repatriation", "unesco 1970", "stolen idol", "sacred heritage", "temple plunder", "museum cartel"])
        req_diaspora = any(cls.matches_keyword(text_lower, kw) for kw in ["diaspora sanctuary", "host tolerance", "free speech pretext", "consular reciprocity", "transnational extremist", "safe haven"])
        req_pm = any(cls.matches_keyword(text_lower, kw) for kw in ["bullion", "sge", "comex", "streedhan", "gold repatriation", "physical gold", "paper derivative"])
        req_hydro_choke = any(cls.matches_keyword(text_lower, kw) for kw in ["hormuz", "brent shock", "chokepoint interdiction", "spr cover", "chabahar bypass", "tanker interdiction"])
        req_cog_res = any(cls.matches_keyword(text_lower, kw) for kw in ["cortical resilience", "dharmic stoicism", "dhriti", "viveka", "outrage-bait", "amygdala panic", "cognitive resilience"])
        req_nuc = any(cls.matches_keyword(text_lower, kw) for kw in ["fast breeder", "pfbr", "thorium cycle", "nsg cartel", "nuclear autonomy", "smr captive", "closed fuel cycle"])
        req_bop = any(cls.matches_keyword(text_lower, kw) for kw in ["bop shield", "balance of payments", "greenspan-guidotti", "dii absorption", "fii flight", "forex import cover"])
        req_elec = any(cls.matches_keyword(text_lower, kw) for kw in ["electoral polarization", "labharthi", "maryada", "caste fragmentation", "election commission neutrality", "welfare saturation"])
        req_refinery_sab = any(cls.matches_keyword(text_lower, kw) for kw in ["refinery sabotage", "ruf pit", "vizag refinery", "ot sabotage", "scada anomaly", "crack spread", "dcs anomaly"])
        req_hnwi = any(cls.matches_keyword(text_lower, kw) for kw in ["hnwi", "capital flight", "gift city", "inheritance tax", "wealth tax", "confiscation rhetoric", "onshoring"])
        req_gold_repat = any(cls.matches_keyword(text_lower, kw) for kw in ["gold repatriation", "rbi gold", "domestic vault", "bullion immunity", "counterparty default", "g7 asset freeze"])
        req_multi_agent = any(cls.matches_keyword(text_lower, kw) for kw in ["multi-agent", "agent consensus", "group chat", "agent swarm", "circular loop", "credential isolation"])
        req_paleo = any(cls.matches_keyword(text_lower, kw) for kw in ["rakhigarhi", "ancient dna", "adna", "indus periphery", "aasi", "aryan migration", "steppe pastoralist", "endogamy"])
        req_triang = any(cls.matches_keyword(text_lower, kw) for kw in ["epistemic triangulation", "archaeozoology", "harappa centenary", "faunal evidence", "zebu", "osteometry"])
        req_soil = any(cls.matches_keyword(text_lower, kw) for kw in ["soil resilience", "save soil", "soil organic carbon", "soc", "topsoil", "agroforestry", "desertification"])
        req_dharmic_sov = any(cls.matches_keyword(text_lower, kw) for kw in ["dharmic soft power", "free tn temples", "temple autonomy", "hr&ce", "cultural decolonization", "spiritual diplomacy"])
        req_sec_rot = any(cls.matches_keyword(text_lower, kw) for kw in ["sectoral rotation", "grid saturation", "data center grid", "ai capex", "index illusion", "hyperscaler capex", "sensex 2000"])
        req_island_sec = any(cls.matches_keyword(text_lower, kw) for kw in ["island net security", "eez surveillance", "agalega", "maritime bastion", "hydrographic vessel", "plan incursion", "sagar"])
        req_cbdc_surv = any(cls.matches_keyword(text_lower, kw) for kw in ["cbdc surveillance", "programmable cbdc", "monetary autonomy", "digital enclosure", "programmable money", "cash retention"])
        req_interagency = any(cls.matches_keyword(text_lower, kw) for kw in ["inter-agency synergy", "counter subversion", "nia cbi ed", "fiu-ind", "hawala crackdown", "gangster-terror", "fcra subversion"])
        req_bank_crar = any(cls.matches_keyword(text_lower, kw) for kw in ["bank crar", "asset quality", "crar ratio", "banking fortress", "net npa", "provision coverage", "treasury mtm"])
        req_bur_fric = any(cls.matches_keyword(text_lower, kw) for kw in ["bureaucratic friction", "administrative velocity", "file looping", "pil lawfare", "sub-national inertia", "statutory de-registration"])
        req_gan_radar = any(cls.matches_keyword(text_lower, kw) for kw in ["gan radar", "gallium nitride", "aesa radar", "trm density", "radar sovereignty", "indigenous aesa", "wide bandgap"])
        req_high_airlift = any(cls.matches_keyword(text_lower, kw) for kw in ["nyoma alg", "high altitude airlift", "thrust derating", "daulat beg oldi", "winter lac logistics", "heavy airlift"])
        req_algo_sov = any(cls.matches_keyword(text_lower, kw) for kw in ["algorithmic sovereignty", "big tech sovereignty", "shadow banning", "algorithmic nudging", "dpdp enforcement", "meta fir", "section 69a"])
        req_sacred_econ = any(cls.matches_keyword(text_lower, kw) for kw in ["sacred economy", "pilgrimage tourism", "ayodhya economy", "kashi corridor", "religious tourism multiplier", "temple msme"])
        req_outward_odi = any(cls.matches_keyword(text_lower, kw) for kw in ["outward direct investment", "odi asset capture", "western asset acquisition", "ip repatriation", "distressed asset capture", "corporate odi"])
        req_archaeo_astro = any(cls.matches_keyword(text_lower, kw) for kw in ["archaeo-astronomy", "planetary conjunction", "epigraphic dating", "ved veer arya", "vedic astronomy", "equinox retro-calculation", "sediment stratigraphy"])
        req_black_proj = any(cls.matches_keyword(text_lower, kw) for kw in ["black project", "special access program", "c4isr early warning", "deep state black", "nuclear alert cushion", "annie jacobsen"])
        req_trans_hydro = any(cls.matches_keyword(text_lower, kw) for kw in ["yarlung tsangpo", "upper siang", "medog dam", "trans-himalayan hydrology", "hydrological warfare", "buffer reservoir", "brahmaputra dam"])
        req_pred_dumping = any(cls.matches_keyword(text_lower, kw) for kw in ["canton fair", "predatory dumping", "overcapacity dumping", "qco enforcement", "diaper dumping", "toy dumping", "anti-dumping duty"])
        req_apaurusheya = any(cls.matches_keyword(text_lower, kw) for kw in ["apaurusheya", "apaurusheyatva", "shastric ontology", "vedic epistemology", "colonial philology", "ramnath jha", "sabda pramana"])
        req_heritage_encroach = any(cls.matches_keyword(text_lower, kw) for kw in ["heritage encroachment", "shivaji forts", "vishalgad", "lohagad", "mazar encroachment", "hilltop fort", "asi enforcement"])
        req_narr_inversion = any(cls.matches_keyword(text_lower, kw) for kw in ["narrative inversion", "ravanayana", "villain glamorization", "moral taxonomy inversion", "consumer boycott", "cinema subversion"])
        req_malacca = any(cls.matches_keyword(text_lower, kw) for kw in ["malacca strait", "great nicobar bastion", "anc strike", "malacca deterrence", "chokepoint veto", "chinese sloc"])
        req_ritual_eco = any(cls.matches_keyword(text_lower, kw) for kw in ["ritual ecological", "diwali firecrackers", "selective prohibition", "festival ban", "shastric ritual", "environmental lawfare", "firecracker ban"])
        req_dharmic_const = any(cls.matches_keyword(text_lower, kw) for kw in ["dharmic constitutionalism", "rajdharma", "decolonial jurisprudence", "borrowed constitutional dogma", "civilizational sanskriti", "decolonial law"])
        req_part_demyst = any(cls.matches_keyword(text_lower, kw) for kw in ["partition demystification", "historical sandarshan", "khilafat appeasement", "moplah atrocities", "mahatma-ism", "demystify partition", "partition causality"])
        req_epic_fidelity = any(cls.matches_keyword(text_lower, kw) for kw in ["canonical epic fidelity", "valmiki ramayana", "cinematic subversion", "adipurush", "marxist pop revisionism", "epic fidelity", "canonical fidelity"])
        req_theol_apostasy = any(cls.matches_keyword(text_lower, kw) for kw in ["theological incompatibility", "ex-muslim", "apostasy velocity", "irtidad", "surah 3:85", "sanatani muslim myth", "scriptural exclusivity"])
        req_aurobindo_integ = any(cls.matches_keyword(text_lower, kw) for kw in ["aurobindonian integration", "sri aurobindo", "spiritual integration", "shakta tantric harmony", "decentralized sanatan", "regional bastions", "integral nationalism"])
        req_shastric_diet = any(cls.matches_keyword(text_lower, kw) for kw in ["shastric dietary plurality", "dietary plurality", "shakta offering", "kamakhya dietary", "vaishnava vegetarianism", "culinary pluralism", "tantric offering"])
        req_archival_source = any(cls.matches_keyword(text_lower, kw) for kw in ["archival primary source", "primary epigraphy", "copper plate inscription", "inam register", "archival fidelity", "archival evidence"])
        req_academic_gate = any(cls.matches_keyword(text_lower, kw) for kw in ["academic gatekeeping", "literary festival gatekeeping", "foreign donor alignment", "narrative colonization", "think tank gatekeeping"])
        req_succ_cont = any(cls.matches_keyword(text_lower, kw) for kw in ["succession continuity", "leadership succession", "modi to yogi", "political transition risk", "capex statutory durability", "cadre alignment"])
        req_ling_sprach = any(cls.matches_keyword(text_lower, kw) for kw in ["linguistic sprachbund", "sprachbund convergence", "sanskrit and tamil", "proto-dravidian", "munda loanwords", "linguistic balkanization", "retroflex phonology"])
        req_indig_stem = any(cls.matches_keyword(text_lower, kw) for kw in ["indigenous stem", "wootz steel", "zawar zinc", "ancient indian metallurgy", "stem authenticity", "mathematical manuscript", "sulba sutras"])
        req_subalt_mem = any(cls.matches_keyword(text_lower, kw) for kw in ["subaltern memory", "hero stones", "viragals", "oral folk resistance", "village memorial", "subaltern history"])
        req_ind_attr = any(cls.matches_keyword(text_lower, kw) for kw in ["industrial attrition", "ammunition burn rate", "shell production surge", "drone fabrication capacity", "propellant precursor", "180-day attrition"])
        req_imp_debt = any(cls.matches_keyword(text_lower, kw) for kw in ["imperial debt overreach", "debt-to-gdp military", "basing retrenchment", "fiscal crowding out defense", "imperial overstretch"])
        req_col_drain = any(cls.matches_keyword(text_lower, kw) for kw in ["colonial drain extraction", "council bills drain", "45 trillion drain", "deindustrialization tariff", "colonial wealth drain"])
        req_basel_gold = any(cls.matches_keyword(text_lower, kw) for kw in ["basel gold", "basel iii gold", "allocated bullion", "physical bullion tier 1", "paper gold derivative", "unbacked comex gold"])
        req_mnemonic_fid = any(cls.matches_keyword(text_lower, kw) for kw in ["apaurusheya mnemonic", "ashta vikriti", "ghana patha", "jata patha", "oral mnemonic fidelity", "vedic checksum depth"])
        req_mitrokhin_ds = any(cls.matches_keyword(text_lower, kw) for kw in ["mitrokhin archive", "deep state penetration", "national advisory council", "shadow cabinet subversion", "extra constitutional power"])
        req_puranic_bound = any(cls.matches_keyword(text_lower, kw) for kw in ["puranic metaphysical boundary", "metaphysical mythos", "unverifiable metaphysical", "subjective mythos gating"])
        req_polemics_ratio = any(cls.matches_keyword(text_lower, kw) for kw in ["polemics vs empirical", "polemical ridicule", "ad hominem density", "bad faith deflection", "polemical deflection"])
        req_kishkindha_geo = any(cls.matches_keyword(text_lower, kw) for kw in ["kishkindha global geography", "sugriva atlas", "kishkindha kanda geography", "archaeo geographic exploration"])
        req_vedic_decolon = any(cls.matches_keyword(text_lower, kw) for kw in ["vedic etymological decolonization", "paninian root", "yaska nirukta", "aghnya etymology", "medha etymology", "colonial lexical distortion"])
        req_quantum_st = any(cls.matches_keyword(text_lower, kw) for kw in ["quantum entangled spacetime", "quantum decision theory", "non commutative decision", "cognitive interference term", "quantum decision dynamics"])
        req_semi_antitrust = any(cls.matches_keyword(text_lower, kw) for kw in ["semiconductor antitrust", "gpu hardware monopoly", "cuda software lockin", "open silicon diversification", "silicon monopoly"])
        req_fcra_eccles = any(cls.matches_keyword(text_lower, kw) for kw in ["transnational fcra ecclesiastical", "ecclesiastical inflow", "conversion velocity", "fcra audit enforcement", "fcra subversion"])
        req_cinematic_sac = any(cls.matches_keyword(text_lower, kw) for kw in ["cinematic iconography sacrality", "desacralization index", "western fantasy trope divergence", "sacred iconography dilution", "canonical fidelity cinematic"])
        req_infra_capex_mult = any(cls.matches_keyword(text_lower, kw) for kw in ["infrastructure capex multiplier", "public capex allocated", "capex to gdp ratio", "domestic procurement capex", "freight corridor capex"])
        req_classical_bullion = any(cls.matches_keyword(text_lower, kw) for kw in ["classical bullion inflow", "bullion trade surplus", "vikramaditya gold drain", "roman gold drain", "export surplus bullion settlement"])
        req_asym_lawfare = any(cls.matches_keyword(text_lower, kw) for kw in ["asymmetric statutory lawfare", "section 498a extortion", "matrimonial lawfare", "settlement extortion intensity", "statutory arrest asymmetry"])
        req_crypto_decent = any(cls.matches_keyword(text_lower, kw) for kw in ["cryptographic decentralization", "permissionless mathematical scarcity", "bitcoin 21m cap", "decentralized censorship resistance", "fiat debasement hedge"])
        req_hormuz_escal = any(cls.matches_keyword(text_lower, kw) for kw in ["hormuz energy escalation", "strait of hormuz interdiction", "chokepoint interdiction risk", "spr reserve buffer days", "hormuz vulnerability"])
        req_eurodollar_drain = any(cls.matches_keyword(text_lower, kw) for kw in ["eurodollar shadow liquidity", "offshore dollar collateral squeeze", "cross currency basis spread", "eurodollar liquidity drain"])
        req_black_swan = any(cls.matches_keyword(text_lower, kw) for kw in ["black swan disruption", "extreme value theory shock", "shock tail risk index", "infrastructure coupling density", "systemic black swan cascade"])
        req_sovereign_gold_vel = any(cls.matches_keyword(text_lower, kw) for kw in ["sovereign gold repatriation velocity", "bullion repatriation velocity", "repatriated bullion metric", "bank of england gold repatriation", "vault repatriation velocity"])
        req_speech_forensics = any(cls.matches_keyword(text_lower, kw) for kw in ["geopolitical speech forensics", "speech signal divergence", "lexical divergence index", "deliberate omission density", "between the lines speech"])
        req_sov_pub_int = any(cls.matches_keyword(text_lower, kw) for kw in ["sovereign public interest", "yogakshema public welfare", "casualty threat index", "toxic ecological dumping", "whistleblower public interest"])
        req_adv_timing = any(cls.matches_keyword(text_lower, kw) for kw in ["adversary timing correlation", "summit timing correlation", "coordinated timing leak", "orchestrated timing leak", "summit sensitivity timing"])
        req_doc_prov = any(cls.matches_keyword(text_lower, kw) for kw in ["documentary provenance authenticity", "bsa 2023 section 63", "bsa section 63", "electronic record certificate", "typographical anomaly ratio"])
        req_bear_raid = any(cls.matches_keyword(text_lower, kw) for kw in ["bear raid derivative", "p-notes short concentration", "put volume spike leak", "predatory short seller coordination", "bear raid options"])
        req_debt_cov = any(cls.matches_keyword(text_lower, kw) for kw in ["offshore debt covenant contagion", "eurodollar syndicated loan default", "bank letter of credit freeze", "cross default clause leak", "debt covenant squeeze"])
        req_exfil_sanc = any(cls.matches_keyword(text_lower, kw) for kw in ["exfiltration and foreign sanctuary", "asylum pipeline", "embassy sanctuary proximity", "foreign intelligence exfiltration", "visa pre-clearance leak"])
        req_retal_threat = any(cls.matches_keyword(text_lower, kw) for kw in ["retaliation threat and opsec", "whistleblower physical intimidation", "asymmetric slapp lawsuit", "witness protection mandate", "retaliation threat score"])
        req_vigil_rem = any(cls.matches_keyword(text_lower, kw) for kw in ["vigilance statutory remedy", "cvc whistleblower", "lokpal statutory remedy", "sfio corporate investigation", "sebi informant reward"])
        req_kinesic_chrom = any(cls.matches_keyword(text_lower, kw) for kw in ["speech kinesic and chromatic", "facs deception marker", "vocal pitch jitter", "chromatic incongruence", "dress color semiotics"])
        req_speech_omit = any(cls.matches_keyword(text_lower, kw) for kw in ["speech omission and negative space", "deliberate omission density", "taboo topic suppression", "negative space omission", "what was refused to say"])
        req_tbml = any(cls.matches_keyword(text_lower, kw) for kw in ["trade based money laundering", "icegate customs remittance discrepancy", "gst eway divergence", "invoice round tripping", "tbml capital flight"])
        req_scada_tamp = any(cls.matches_keyword(text_lower, kw) for kw in ["defense scada and firmware tamper", "microcode backdoor", "scada plc tampering", "firmware hash deviation", "trojan hardware firmware"])
        req_cult_sac = any(cls.matches_keyword(text_lower, kw) for kw in ["cultural heritage and sacrality breach", "temple asset misappropriation", "antiquities illicit auction", "sacral space encroachment", "temple land waqf"])
        req_perj_liab = any(cls.matches_keyword(text_lower, kw) for kw in ["perjury risk and retributive liability", "bns section 229 230", "bns section 229", "malicious slander liability", "retributive perjury penalty"])
        req_qdt_whistle = any(cls.matches_keyword(text_lower, kw) for kw in ["qdt whistleblower cognitive state", "quantum decision disclosure", "duty fear interference", "constructive duty interference", "whistleblower cognitive state"])
        req_capex_imp = any(cls.matches_keyword(text_lower, kw) for kw in ["sovereign strategic capex impact", "curative receivership", "satyam model receivership", "capex multiplier freeze", "receivership remedy viability"])
        req_bis_fx = any(cls.matches_keyword(text_lower, kw) for kw in ["bis hidden fx", "hidden fx swap", "cross currency basis spread", "shadow dollar debt", "dollar funding stress", "ois sofr spread"])
        req_ubo_shell = any(cls.matches_keyword(text_lower, kw) for kw in ["offshore ubo", "beneficial ownership shell", "pnote concentration", "category i fpi", "tax haven layering", "short syndicate de-anonymizer"])
        req_speech_balsheet = any(cls.matches_keyword(text_lower, kw) for kw in ["speech to balance sheet divergence", "rhetoric vs balance sheet", "cbam tariff barrier", "verbal harmony divergence", "hypocrisy divergence"])
        req_kinesic_baseline = any(cls.matches_keyword(text_lower, kw) for kw in ["kinesic contextual baseline", "baseline drift", "summit pressure elevation", "cultural expressiveness norm", "micro expression drift"])
        req_chanakya_upadha = any(cls.matches_keyword(text_lower, kw) for kw in ["chanakya neeti upadha", "upadha pariksha", "mantra gupti", "dharmopadha", "arthopadha", "bhayopadha", "kamopadha integrity"])
        req_kautilya_saptanga = any(cls.matches_keyword(text_lower, kw) for kw in ["kautilya mandala shadgunya", "saptanga 7-limb", "saptanga health", "shadgunya foreign policy", "sandhi vigraha", "raja mandala action"])
        req_krishna_rajadharma = any(cls.matches_keyword(text_lower, kw) for kw in ["krishna rajadharma exhaustion", "udyoga parva peace exhaustion", "peace initiatives exhausted", "dharma yuddha retaliation", "svadharma resolve", "moha hesitation"])
        req_cloud_monopoly = any(cls.matches_keyword(text_lower, kw) for kw in ["cloud monopoly fragility", "hyperscaler concentration", "sovereign compute exit", "cloud outage contagion", "hyperscaler exit barrier", "cloud dependency risk"])
        req_cognitive_deception = any(cls.matches_keyword(text_lower, kw) for kw in ["cognitive deception misdirection", "stratagem misdirection", "perception distraction", "feint narrative", "information warfare decoy", "adversarial deception channel"])
        req_ci_honeytrap = any(cls.matches_keyword(text_lower, kw) for kw in ["counter intelligence honeytrap", "kompromat recruitment", "honeytrap operational leverage", "blackmail coercion channel", "covert compromise vulnerability"])
        req_maritime_net_sec = any(cls.matches_keyword(text_lower, kw) for kw in ["maritime net security primacy", "indian ocean sea lane primacy", "naval choke control", "ior supremacy index", "anti submarine warfare perimeter"])
        req_false_flag_narrative = any(cls.matches_keyword(text_lower, kw) for kw in ["false flag narrative deception", "synthetic atrocity staging", "provocation fabrication", "casus belli manipulation", "false flag operation index"])
        req_sov_cyber_extort = any(cls.matches_keyword(text_lower, kw) for kw in ["sovereign cyber extortion", "critical infrastructure ransomware", "state backed extortion", "grid hostage exploit", "cyber extortion ransom leverage"])
        req_port_dual_use = any(cls.matches_keyword(text_lower, kw) for kw in ["maritime port dual use", "commercial port naval conversion", "dual use maritime berthing", "string of pearls port surveillance", "naval facility dual use"])
        req_revealed_pref_div = any(cls.matches_keyword(text_lower, kw) for kw in ["revealed preference divergence", "sanctions rhetoric vs trade", "diplomatic posture vs trade balance", "hypocritical trade flow", "stated policy divergence"])
        req_debt_syndicate = any(cls.matches_keyword(text_lower, kw) for kw in ["sovereign debt syndicate leverage", "paris club conditional squeeze", "predatory syndicated sovereign loan", "sovereign debt trap restructuring", "imf structural adjustment leverage"])
        req_asym_weapon_leak = any(cls.matches_keyword(text_lower, kw) for kw in ["asymmetric weapon proliferation leakage", "manpads black market leakage", "drone tech transfer to proxies", "clandestine missile proliferation", "illicit small arms diversion"])
        req_legacy_infra_obs = any(cls.matches_keyword(text_lower, kw) for kw in ["legacy infrastructure obsolescence", "scada technical debt", "grid component obsolescence", "legacy rail avionics failure", "infrastructure decay rate"])
        req_spec_capex_overhang = any(cls.matches_keyword(text_lower, kw) for kw in ["speculative capex overhang", "stranded ai compute capex", "unprofitable datacenter overbuild", "overhyped capex debt burden", "speculative asset impairment"])
        req_subnat_frag_lawfare = any(cls.matches_keyword(text_lower, kw) for kw in ["subnational fragmentation lawfare", "balkanization legal warfare", "regionalist secessionist lawfare", "provincial sovereignty weaponization", "subnational charter sabotage"])
        req_civ_epistemic_int = any(cls.matches_keyword(text_lower, kw) for kw in ["civilizational epistemic integrity", "indigenous historiography defense", "colonial historiographical distortion", "textual lineage preservation", "epistemic decolonization metric"])
        req_algo_cog_subversion = any(cls.matches_keyword(text_lower, kw) for kw in ["algorithmic cognitive subversion", "feed manipulation radicalization", "foreign recommendation algorithm bias", "cognitive echo chamber amplification", "algorithmic societal polarization"])
        req_scada_hw_backdoor = any(cls.matches_keyword(text_lower, kw) for kw in ["critical scada hardware backdoor", "silicon level kill switch", "power grid transformer backdoor", "substation plc trojan", "embedded industrial hardware backdoor"])
        req_circ_venture_val = any(cls.matches_keyword(text_lower, kw) for kw in ["circular venture valuation bubble", "round tripping ai venture capital", "synthetic unicorns mark up", "unbacked venture capital multiplier", "self dealing valuation pump"])
        req_monopoly_patent_supp = any(cls.matches_keyword(text_lower, kw) for kw in ["monopoly patent suppression", "evergreening pharmaceutical blockade", "patent thicket stifling indigenous innovation", "anti competitive patent hoarding", "compulsory licensing deterrence"])
        req_sub_replace_demog = any(cls.matches_keyword(text_lower, kw) for kw in ["sub replacement demographic extinction", "total fertility collapse rate", "demographic pyramid inversion", "societal depopulation spiral", "sub replacement tfr crisis"])
        req_phys_capex_mult = any(cls.matches_keyword(text_lower, kw) for kw in ["physical capex tangible multiplier", "hard infrastructure tangible output", "steel cement port physical capex", "productive asset capex return", "physical capital formation velocity"])
        req_open_sys_infil = any(cls.matches_keyword(text_lower, kw) for kw in ["open system asymmetric infiltration", "democratic vulnerability exploitation", "asymmetric institutional penetration", "open academic legal infiltration", "unreciprocated openness exploitation"])
        req_dynastic_shadow_cab = any(cls.matches_keyword(text_lower, kw) for kw in ["dynastic extra constitutional shadow cabinet", "unaccountable coterie governance", "extra constitutional kitchen cabinet", "nac style shadow government", "dynastic bureaucratic capture"])
        req_naval_coercion = any(cls.matches_keyword(text_lower, kw) for kw in ["superpower naval coercion brinkmanship", "gunboat diplomacy intimidation", "carrier strike group brinkmanship", "freedom of navigation coercive transit", "unilateral naval blockade posturing"])
        req_semi_kompromat = any(cls.matches_keyword(text_lower, kw) for kw in ["semiconductor smuggling", "executive kompromat", "megaspeed", "transnational semiconductor", "gpu smuggling", "chip smuggling", "semiconductor kompromat", "gpu transshipment", "silicon smuggling"])
        req_media_leak_timing = any(cls.matches_keyword(text_lower, kw) for kw in ["media intelligence leak timing", "guided missile leak", "media leak put options", "options oi spike leak", "regulatory subpoena leak", "put option spike", "put option spikes", "media intelligence leak", "leak timing correlation"])
        req_gen_media_hegemony = any(cls.matches_keyword(text_lower, kw) for kw in ["generative media compute hegemony", "generative media hegemony", "cultural compute hegemony", "bollywood render farm", "china to bollywood", "generative compute hegemony", "render farm hegemony"])
        req_silicon_microcode_killswitch = any(cls.matches_keyword(text_lower, kw) for kw in ["silicon microcode kill switch", "remote firmware kill switch", "cloud license heartbeat", "openbmc airgap", "gpu killswitch", "microcode kill switch", "firmware kill switch", "remote silicon kill switch"])
        req_gpu_debt_contagion = any(cls.matches_keyword(text_lower, kw) for kw in ["gpu collateralized private debt", "gpu debt contagion", "ai private credit contagion", "gpu asset backed loans", "gpu debt covenant breach", "private credit debt contagion", "gpu collateral debt"])

        # Phases 396-415: Sovereign Asymmetric War, Balance-Sheet Realism & Civilizational Sovereignty Matrix
        req_informal_divergence = any(cls.matches_keyword(text_lower, kw) for kw in ["informal sector divergence", "unorganized sector gdp", "arun kumar informal", "dual economy divergence", "unorganized wage compression", "household savings collapse", "informal economy accounting"])
        req_pboc_liquidity = any(cls.matches_keyword(text_lower, kw) for kw in ["pboc lgfv", "municipal debt deflation", "lgfv debt trap", "negative net new loans", "china balance sheet recession", "municipal land sale collapse", "pboc liquidity trap"])
        req_air_defense_cer = any(cls.matches_keyword(text_lower, kw) for kw in ["air defense cost exchange", "asymmetric drone cost exchange", "patriot shahed cost exchange", "cer interceptor exhaustion", "magazine depletion swarm", "air defense budget exhaustion", "asymmetric air defense"])
        req_hypersonic_glide = any(cls.matches_keyword(text_lower, kw) for kw in ["hypersonic non-keplerian", "hypersonic glide trajectory", "scramjet skip glide", "drdo hgv", "mach 7 glide", "abm radar invalidation", "hypersonic glide penetration", "non keplerian glide"])
        req_platform_defiance = any(cls.matches_keyword(text_lower, kw) for kw in ["platform regulatory defiance", "section 69a defiance", "safe harbor forfeiture", "big tech algorithmic resistance", "takedown directive defiance", "sovereign platform defiance", "intermediary safe harbor"])
        req_cartel_cross_holding = any(cls.matches_keyword(text_lower, kw) for kw in ["institutional monopoly cartel", "cross shareholding sieve", "aladdin capital flight", "common ownership index", "blackrock vanguard state street", "institutional cartel", "aladdin risk"])
        req_msme_asphyxiation = any(cls.matches_keyword(text_lower, kw) for kw in ["msme formalization", "working capital asphyxiation", "gst formalization mortality", "msme solvency stress", "treds invoice discounting", "promoter decoupling", "msme working capital"])
        req_nuclear_latency = any(cls.matches_keyword(text_lower, kw) for kw in ["nuclear launch under attack", "launch on warning latency", "72 minute escalation", "hypersonic flight time decision", "nuclear command latency", "nuclear decapitation vulnerability", "annie jacobsen"])
        req_border_narco = any(cls.matches_keyword(text_lower, kw) for kw in ["border state narco fiscal", "narco fiscal subversion", "drone narco trafficking", "border debt gsdp", "punjab narco drone", "populist freebie border debt", "border subversion index"])
        req_condominium_exclusion = any(cls.matches_keyword(text_lower, kw) for kw in ["superpower condominium", "yalta 2.0", "trilateral condominium", "g2 carve up", "superpower condominium exclusion", "imec instc transit autonomy", "shatter condominium"])
        req_quantum_hndl = any(cls.matches_keyword(text_lower, kw) for kw in ["harvest now decrypt later", "quantum hndl", "q-day vulnerability", "post-quantum cryptography", "pqc migration", "lattice cryptography", "quantum key distribution", "quantum exposure score"])
        req_diplomatic_optics = any(cls.matches_keyword(text_lower, kw) for kw in ["diplomatic non verbal optics", "attire forensics", "summit seating distance", "gamusa civilizational attire", "handshake latency", "non-verbal statecraft", "diplomatic attire forensics"])
        req_grayzone_lawfare = any(cls.matches_keyword(text_lower, kw) for kw in ["cultural religious grayzone", "waqf lawfare", "section 40 waqf", "defense buffer contestation", "siliguri corridor grayzone", "non-judicial statutory property claim", "grayzone lawfare"])
        req_mineral_weaponization = any(cls.matches_keyword(text_lower, kw) for kw in ["critical mineral weaponization", "gallium germanium export ban", "rare earth chokepoint", "neodymium magnet weaponization", "mineral supply chain decapitation", "lithium refining chokepoint", "critical mineral supply chain"])
        req_food_weaponization = any(cls.matches_keyword(text_lower, kw) for kw in ["agrochemical fertilizer weaponization", "fertilizer feedstock cartel", "potash phosphate embargo", "calorie inflation food security", "strategic grain reserve buffer", "food security weaponization", "food sovereignty stress"])
        req_aviation_cartel = any(cls.matches_keyword(text_lower, kw) for kw in ["aviation transit slot cartel", "sixth freedom cartel", "gulf airline sixth freedom", "bilateral seat imbalance", "airport slot war", "mumbai airport slot", "aviation capital leakage"])
        req_airborne_command = any(cls.matches_keyword(text_lower, kw) for kw in ["airborne command decapitation", "air india one survivability", "laircm missile defense", "flying nuclear command bunker", "type-1 satcom airborne", "airborne command survivability"])
        req_honeytrap_espionage = any(cls.matches_keyword(text_lower, kw) for kw in ["sub tactical honeytrap", "kamopadha espionage", "defense blueprint leak", "brahmos technician honeytrap", "unscreened smartphone classified", "social media honeytrap", "personnel espionage"])
        req_naval_ew = any(cls.matches_keyword(text_lower, kw) for kw in ["naval electronic warfare suppression", "non kinetic naval disablement", "rf jamming warship", "acoustic spoofing naval", "pns hunain electronic warfare", "ins kolkata ew", "standoff jamming power"])
        req_historiography_decolonial = any(cls.matches_keyword(text_lower, kw) for kw in ["civilizational epistemic historiography", "historiography decolonization", "primary epigraphic citations", "inscriptional provenance", "sanskrit grammar provenance", "colonial textbook distortion", "meenakshi jain ami ganatra"])

        # Phases 416-433: Sovereign Forensic Sieves & Council Titans Keyword Triggers
        req_scada_blackout = any(cls.matches_keyword(text_lower, kw) for kw in ["scada blackout", "polymorphic malware", "grid blackout", "ot firmware", "power grid cyber", "industroyer", "cyber blackout"])
        req_media_cartel = any(cls.matches_keyword(text_lower, kw) for kw in ["synchronized media", "media cartel", "distraction network", "coordinated press", "narrative sync", "cartel network"])
        req_banking_lawfare = any(cls.matches_keyword(text_lower, kw) for kw in ["deep state banking", "rating squeeze", "short seller lawfare", "clearing litigation", "bbb- rating", "banking lawfare"])
        req_dew_weapon = any(cls.matches_keyword(text_lower, kw) for kw in ["directed energy", "dew", "high energy laser", "thermal blooming", "counter-swarm laser", "microwave weapon", "power transmission"])
        req_alliance_autonomy = any(cls.matches_keyword(text_lower, kw) for kw in ["multilateral alliance", "hegemonic pressure", "secondary sanctions resistance", "veto posture", "autonomy retention"])
        req_offshore_repatriation = any(cls.matches_keyword(text_lower, kw) for kw in ["offshore banking", "asset repatriation", "numbered trust", "aeoi tax", "trade misinvoicing", "capital recovery"])
        req_foreign_intel_pen = any(cls.matches_keyword(text_lower, kw) for kw in ["foreign intelligence penetration", "mitrokhin archive", "dynastic foundation foreign grant", "kgb penetration", "cia think tank"])
        req_cognitive_atrophy = any(cls.matches_keyword(text_lower, kw) for kw in ["cognitive atrophy", "service displacement", "algorithmic dopamine", "it labor automation", "attention span deficit", "reading deficit"])
        req_demographic_fort = any(cls.matches_keyword(text_lower, kw) for kw in ["demographic sovereignty", "border fortification", "anti-migration quota", "border interdiction", "poland 1683", "vienna model"])
        req_faceless_procurement = any(cls.matches_keyword(text_lower, kw) for kw in ["faceless procurement", "smart contract escrow", "procurement transparency", "gem portal", "discretionary bypass"])
        req_investigative_forensics = any(cls.matches_keyword(text_lower, kw) for kw in ["investigative forensics", "negative space engine", "kinesic micro-tremor", "sartorial semiotics", "dress color optics", "acoustic tremor", "read between the lines"])
        req_sovereign_debt_rollover = any(cls.matches_keyword(text_lower, kw) for kw in ["sovereign debt maturity", "debt rollover wall", "ankit shah", "fractional reserve panic", "htm paper losses", "5-year debt wall"])
        req_doval_subversion = any(cls.matches_keyword(text_lower, kw) for kw in ["asymmetric subversion", "counter penetration", "ajit doval", "doval doctrine", "offensive-defense", "fcra shadow funding"])
        req_modi_capex = any(cls.matches_keyword(text_lower, kw) for kw in ["sovereign capex moat", "escape velocity", "narendra modi", "modi capex", "viksit bharat", "semiconductor fab sovereignty", "faceless governance"])
        req_jaishankar_hedging = any(cls.matches_keyword(text_lower, kw) for kw in ["multipolar hedging", "strategic chokepoint tensor", "jaishankar", "s jaishankar", "reciprocal leverage", "sloc command", "trade chokepoint"])
        req_sanyal_rating = any(cls.matches_keyword(text_lower, kw) for kw in ["credit rating cartel", "sanjeev sanyal", "rating bias", "logistics cost compression", "wgi bias", "fast frequency data"])
        req_deepak_jurisprudence = any(cls.matches_keyword(text_lower, kw) for kw in ["civilizational jurisprudence", "decolonial lawfare", "j sai deepak", "sai deepak", "temple property autonomy", "decolonial legal"])
        req_ranga_falsification = any(cls.matches_keyword(text_lower, kw) for kw in ["empirical falsification", "cryptographic verification", "anand ranganathan", "ranganathan", "zero sycophancy", "karl popper standard"])
        # Phases 434-440: Semiotic Iconography, Global Polycrisis Cascades & Sovereign Resilient Sieves
        req_semiotic_deconstruct = any(cls.matches_keyword(text_lower, kw) for kw in ["semiotic deconstruction", "predictive iconography", "cover art decode", "cleon peterson", "economist cover"])
        req_polycrisis_cascade = any(cls.matches_keyword(text_lower, kw) for kw in ["polycrisis", "systemic cascade", "cross-domain collision", "debt wall chokepoint", "compound crisis"])
        req_grayzone_subversion = any(cls.matches_keyword(text_lower, kw) for kw in ["cultural religious grayzone subversion", "waqf act", "statutory exemption abuse", "demographic corridor density", "grayzone subversion"])
        req_glp1_metabolic = any(cls.matches_keyword(text_lower, kw) for kw in ["glp-1", "ozempic", "wegovy", "consumer metabolic shift", "caloric demand drop", "appetite suppression"])
        req_leo_orbital = any(cls.matches_keyword(text_lower, kw) for kw in ["low earth orbit congestion", "leo weaponization", "asat debris", "kessler syndrome", "orbital congestion"])
        req_taiwan_choke = any(cls.matches_keyword(text_lower, kw) for kw in ["taiwan strait quarantine", "davidson window", "pla centenary 2027", "tsmc sub-5nm choke", "semiconductor quarantine"])
        req_electoral_lawfare = any(cls.matches_keyword(text_lower, kw) for kw in ["electoral lawfare", "judicial disqualification", "le pen disqualification", "afd ban", "post-democratic"])
        # Phases 441-447: Sovereign Forensic Sieves & Multilateral Autonomy Tensors
        req_tripolar_condominium = any(cls.matches_keyword(text_lower, kw) for kw in ["tripolar condominium", "g2 entente", "superpower carveout", "exclusion risk", "multipolar hedging capacity"])
        req_ai_labor_displacement = any(cls.matches_keyword(text_lower, kw) for kw in ["ai labor displacement", "services export displacement", "code synthesis rate", "bpo wage arbitrage decay", "voice agent displacement"])
        req_diaspora_subversion = any(cls.matches_keyword(text_lower, kw) for kw in ["transnational diaspora subversion", "diaspora lawfare", "think tank echo", "constitutional narrative export", "wedge issue amplification"])
        req_gpu_export_chokepoint = any(cls.matches_keyword(text_lower, kw) for kw in ["gpu export control", "semiconductor chokepoint", "h100 ban", "b200 export", "lithography denial", "advanced packaging chokepoint"])
        req_reer_appreciation = any(cls.matches_keyword(text_lower, kw) for kw in ["currency appreciation friction", "reer overvaluation", "it margin compression", "msme competitiveness loss", "rupee appreciation"])
        req_supranational_deep_state = any(cls.matches_keyword(text_lower, kw) for kw in ["supranational deep state", "wef pushback", "davos mandate", "oligarchical regulatory pressure", "rating cartel bias"])
        req_bullion_cyber_sovereignty = any(cls.matches_keyword(text_lower, kw) for kw in ["bullion pricing power", "gift city bullion", "scada cyber sovereignty", "physical gold settlement", "paper gold discount spread"])
        # Phases 448-449: Horizon Polycrisis & Multilateral Defense Interoperability
        req_economist_polycrisis = any(cls.matches_keyword(text_lower, kw) for kw in ["economist 2027", "polycrisis horizon", "fiscal bond squeeze", "tech compute bottleneck", "multipolar equilibrium score", "the world ahead 2027"])
        req_defense_interoperability = any(cls.matches_keyword(text_lower, kw) for kw in ["defense interoperability", "cognitive security", "live-fire pact", "fcra lawfare severance", "curriculum decolonization", "aerospace capex", "cognitive immunity"])
        # Phase 450: Subcontinental Proxy Risk & Silicon Venture Oligarchies
        req_subcontinental_proxy_risk = any(cls.matches_keyword(text_lower, kw) for kw in ["subcontinental proxy", "siliguri corridor", "chittagong", "isi forward logistics", "cholistan", "agniveer", "palantir", "starlink", "paypal mafia", "quantum information", "pqc shield", "silicon oligarchy"])
        # Phase 454: Sovereign Cognitive Subterranean & Kinetic Interoperability
        req_sovereign_hyper_resilience = any(cls.matches_keyword(text_lower, kw) for kw in ["tunnel boring machine", "tbm embargo", "temple wearable", "brainflow", "subaltern electoral", "panna pramukh", "saturation air defense", "navic encryption", "himalayan tunnel", "sovereign hyper resilience"])
        # Phases 455-460 Capstones: Epistemic Validation & Sovereign Industrial Propulsion
        req_epistemic_validation = any(cls.matches_keyword(text_lower, kw) for kw in ["i-soon", "commercial hacking", "geo-spoof", "sakshi", "interleaved retrieval", "unit conversion", "textual stratigraphy", "dpdp 2027", "dpdp", "section 301", "critical edition", "epistemic taxonomy", "epistemic validation"])
        req_industrial_propulsion = any(cls.matches_keyword(text_lower, kw) for kw in ["single-crystal", "kaveri engine", "kaveri", "rhenium", "pfbr", "liquid sodium", "pooled gold", "pgi collateral", "dicgc", "stop switch", "rfp turnover", "industrial capital", "industrial propulsion", "propulsion autonomy"])
        # Phases 461-464: Bullion/Marine/Brand, Impossible Trinity/OPSEC, Constitutional/Grayzone, Mother-Machine/Sonar/Hydrocide
        req_bullion_marine_brand_sovereignty = any(cls.matches_keyword(text_lower, kw) for kw in ["lloyds war risk", "marine p&i", "gift marine insurance", "brand india gi", "monument provenance", "physical gold vault", "rehypothecation pgi"])
        req_impossible_trinity_tbml_opsec = any(cls.matches_keyword(text_lower, kw) for kw in ["impossible trinity", "net short forward", "fema realization", "cbs lou bypass", "duty drawback tbml", "cantonment perimeter", "zero-pattern ci", "route entropy"])
        req_constitutional_grayzone_proxy = any(cls.matches_keyword(text_lower, kw) for kw in ["unprorogued session", "article 108 joint sitting", "delimitation 850", "hrce board shield", "thirupparankundram", "art 144 receivership", "juvenile street veto", "ugc equity reg"])
        req_mother_machine_sonar_hydrocide = any(cls.matches_keyword(text_lower, kw) for kw in ["5-axis cnc", "2b001", "mother machine", "halocline sonar", "cox's bazar submarine", "vrr liquidity", "spot fx drain", "river hydrocide", "dissolved oxygen", "fecal sludge management"])


        if (req_cloud_monopoly or req_legacy_infra_obs or req_platform_defiance) and "digital_sovereignty" not in active_lenses:
            active_lenses.append("digital_sovereignty")
        if (req_cognitive_deception or req_ci_honeytrap or req_false_flag_narrative or req_open_sys_infil or req_semi_kompromat or req_border_narco or req_honeytrap_espionage) and "hybrid_covert" not in active_lenses:
            active_lenses.append("hybrid_covert")
        if (req_maritime_net_sec or req_asym_weapon_leak or req_naval_coercion or req_air_defense_cer or req_hypersonic_glide or req_nuclear_latency or req_airborne_command or req_naval_ew) and "military_readiness" not in active_lenses:
            active_lenses.append("military_readiness")
        if (req_sov_cyber_extort or req_scada_hw_backdoor or req_silicon_microcode_killswitch or req_quantum_hndl) and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if (req_port_dual_use or req_phys_capex_mult or req_aviation_cartel) and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if (req_revealed_pref_div or req_algo_cog_subversion or req_media_leak_timing) and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if (req_debt_syndicate or req_spec_capex_overhang or req_circ_venture_val or req_gpu_debt_contagion or req_informal_divergence or req_pboc_liquidity or req_cartel_cross_holding or req_msme_asphyxiation) and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if (req_subnat_frag_lawfare or req_sub_replace_demog or req_gen_media_hegemony or req_historiography_decolonial) and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if (req_civ_epistemic_int or req_monopoly_patent_supp) and "history" not in active_lenses:
            active_lenses.append("history")
        if req_dynastic_shadow_cab and "bureaucratic_inertia" not in active_lenses:
            active_lenses.append("bureaucratic_inertia")
        if req_condominium_exclusion and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_diplomatic_optics and "kinesics" not in active_lenses:
            active_lenses.append("kinesics")
        if req_grayzone_lawfare and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_mineral_weaponization and "critical_minerals" not in active_lenses:
            active_lenses.append("critical_minerals")
        if req_food_weaponization and "food_security" not in active_lenses:
            active_lenses.append("food_security")

        if (req_bis_fx or req_ubo_shell) and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_speech_balsheet and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_kinesic_baseline and "kinesics" not in active_lenses:
            active_lenses.append("kinesics")
        if (req_chanakya_upadha or req_krishna_rajadharma) and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_kautilya_saptanga and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")

        if req_pnt and "military_readiness" not in active_lenses:
            active_lenses.append("military_readiness")
        if req_ai_gov and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_proxy and "hybrid_covert" not in active_lenses:
            active_lenses.append("hybrid_covert")
        if req_textual and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_media and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_hydro and "food_security" not in active_lenses:
            active_lenses.append("food_security")
        if req_antiquity and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_diaspora and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_pm and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_hydro_choke and "petro_logistics" not in active_lenses:
            active_lenses.append("petro_logistics")
        if req_cog_res and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_nuc and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_bop and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_elec and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_refinery_sab and "petro_logistics" not in active_lenses:
            active_lenses.append("petro_logistics")
        if req_hnwi and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_gold_repat and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_multi_agent and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_paleo and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_triang and "history" not in active_lenses:
            active_lenses.append("history")
        if req_soil and "food_security" not in active_lenses:
            active_lenses.append("food_security")
        if req_dharmic_sov and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_sec_rot and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if req_island_sec and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_cbdc_surv and "digital_sovereignty" not in active_lenses:
            active_lenses.append("digital_sovereignty")
        if req_interagency and "hybrid_covert" not in active_lenses:
            active_lenses.append("hybrid_covert")
        if req_bank_crar and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_bur_fric and "bureaucratic_inertia" not in active_lenses:
            active_lenses.append("bureaucratic_inertia")
        if req_gan_radar and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_high_airlift and "military_readiness" not in active_lenses:
            active_lenses.append("military_readiness")
        if req_algo_sov and "digital_sovereignty" not in active_lenses:
            active_lenses.append("digital_sovereignty")
        if req_sacred_econ and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_outward_odi and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if req_archaeo_astro and "history" not in active_lenses:
            active_lenses.append("history")
        if req_black_proj and "hybrid_covert" not in active_lenses:
            active_lenses.append("hybrid_covert")
        if req_trans_hydro and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_pred_dumping and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if req_apaurusheya and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_heritage_encroach and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_narr_inversion and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_malacca and "military_readiness" not in active_lenses:
            active_lenses.append("military_readiness")
        if req_ritual_eco and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_dharmic_const and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_part_demyst and "history" not in active_lenses:
            active_lenses.append("history")
        if req_epic_fidelity and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_theol_apostasy and "demographic_infiltration" not in active_lenses:
            active_lenses.append("demographic_infiltration")
        if req_aurobindo_integ and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_shastric_diet and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_archival_source and "history" not in active_lenses:
            active_lenses.append("history")
        if req_academic_gate and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_succ_cont and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if req_ling_sprach and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_indig_stem and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_subalt_mem and "history" not in active_lenses:
            active_lenses.append("history")
        if req_ind_attr and "military_readiness" not in active_lenses:
            active_lenses.append("military_readiness")
        if req_imp_debt and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_col_drain and "history" not in active_lenses:
            active_lenses.append("history")

        # Phases 416-433: Route active lenses for Council Titans & Sieves
        if req_scada_blackout and "digital_sovereignty" not in active_lenses:
            active_lenses.append("digital_sovereignty")
        if req_media_cartel and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_banking_lawfare and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_dew_weapon and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_alliance_autonomy and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_offshore_repatriation and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_foreign_intel_pen and "hybrid_covert" not in active_lenses:
            active_lenses.append("hybrid_covert")
        if req_cognitive_atrophy and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_demographic_fort and "military_readiness" not in active_lenses:
            active_lenses.append("military_readiness")
        if req_faceless_procurement and "bureaucratic_inertia" not in active_lenses:
            active_lenses.append("bureaucratic_inertia")
        if req_investigative_forensics:
            if "propaganda" not in active_lenses: active_lenses.append("propaganda")
            if "kinesics" not in active_lenses: active_lenses.append("kinesics")
        if req_sovereign_debt_rollover and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_doval_subversion and "hybrid_covert" not in active_lenses:
            active_lenses.append("hybrid_covert")
        if req_modi_capex and "bureaucratic_inertia" not in active_lenses:
            active_lenses.append("bureaucratic_inertia")
        if req_jaishankar_hedging and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_sanyal_rating and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if req_deepak_jurisprudence and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_ranga_falsification and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        # Phases 434-440: Semiotic Iconography, Global Polycrisis Cascades & Sovereign Resilient Sieves
        if req_semiotic_deconstruct and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_polycrisis_cascade and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_grayzone_subversion and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_glp1_metabolic and "food_security" not in active_lenses:
            active_lenses.append("food_security")
        if req_leo_orbital and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_taiwan_choke and "critical_minerals" not in active_lenses:
            active_lenses.append("critical_minerals")
        if req_electoral_lawfare and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        # Phases 441-447: Route active lenses for Sovereign Forensic Sieves
        if req_tripolar_condominium and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_ai_labor_displacement and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_diaspora_subversion and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_gpu_export_chokepoint and "critical_minerals" not in active_lenses:
            active_lenses.append("critical_minerals")
        if req_reer_appreciation and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if req_supranational_deep_state and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_bullion_cyber_sovereignty and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        # Phases 448-449: Route active lenses
        if req_economist_polycrisis and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_defense_interoperability and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        # Phase 450: Route active lenses
        if req_subcontinental_proxy_risk and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        # Phase 454: Route active lenses
        if req_sovereign_hyper_resilience and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        # Phases 461-464: Route active lenses
        if req_bullion_marine_brand_sovereignty and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_impossible_trinity_tbml_opsec and "hybrid_covert" not in active_lenses:
            active_lenses.append("hybrid_covert")
        if req_constitutional_grayzone_proxy and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_mother_machine_sonar_hydrocide and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")

        # Resolve speaker profiles
        from .speaker_profiler import EpistemicSpeakerProfiler
        resolved_profiles = []
        seen_profile_ids = set()
        for leader in matched_leaders:
            prof = EpistemicSpeakerProfiler.get_profile(leader)
            if prof and prof.canonical_id not in seen_profile_ids:
                resolved_profiles.append(prof.to_dict())
                seen_profile_ids.add(prof.canonical_id)
        for prof in EpistemicSpeakerProfiler.resolve_from_text(prompt):
            if prof.canonical_id not in seen_profile_ids:
                resolved_profiles.append(prof.to_dict())
                seen_profile_ids.add(prof.canonical_id)

        return StrategicQuery(
            raw_prompt=prompt,
            target_summit=summit_full_name,
            target_event=summit_full_name,
            event_type=event_type,
            focal_date=focal_date,
            year=year,
            target_countries=matched_countries,
            target_leaders=matched_leaders,
            prioritized_lenses=active_lenses,
            requires_kinesics=req_kinesics,
            requires_cash_audit=req_cash,
            requires_negative_space=req_neg_space,
            requires_civilizational_depth=req_civilizational,
            requires_india_timeline=req_timeline,
            requires_demographic_audit=req_demographic,
            requires_minerals_audit=req_minerals,
            requires_lawfare_audit=req_lawfare,
            requires_chronology_arbitration=req_chronology,
            requires_abyssal_sovereignty=req_abyssal,
            requires_trophic_biosecurity=req_trophic,
            requires_cognitive_sovereignty=req_cognitive,
            requires_bullion_audit=req_bullion,
            requires_insurgency_audit=req_insurgency,
            requires_quantum_statecraft=req_quantum,
            requires_grayzone_micro_signal=req_grayzone_micro,
            requires_pnt_autonomy=req_pnt,
            requires_ai_governance=req_ai_gov,
            requires_proxy_warfare=req_proxy,
            requires_textual_triangulation=req_textual,
            requires_media_capture=req_media,
            requires_hydro_weaponization=req_hydro,
            requires_antiquity_restitution=req_antiquity,
            requires_diaspora_sanctuary=req_diaspora,
            requires_precious_metals=req_pm,
            requires_hydrocarbon_chokepoints=req_hydro_choke,
            requires_cognitive_resilience=req_cog_res,
            requires_nuclear_autonomy=req_nuc,
            requires_bop_shield=req_bop,
            requires_electoral_polarization=req_elec,
            requires_refinery_sabotage=req_refinery_sab,
            requires_hnwi_capital=req_hnwi,
            requires_gold_repatriation=req_gold_repat,
            requires_multi_agent_consensus=req_multi_agent,
            requires_paleogenomics=req_paleo,
            requires_epistemic_triangulation=req_triang,
            requires_soil_resilience=req_soil,
            requires_dharmic_sovereignty=req_dharmic_sov,
            requires_sectoral_rotation=req_sec_rot,
            requires_island_net_security=req_island_sec,
            requires_cbdc_surveillance=req_cbdc_surv,
            requires_interagency_synergy=req_interagency,
            requires_bank_crar=req_bank_crar,
            requires_bureaucratic_friction=req_bur_fric,
            requires_gan_radar=req_gan_radar,
            requires_high_altitude_airlift=req_high_airlift,
            requires_bigtech_algorithmic_sovereignty=req_algo_sov,
            requires_sacred_economy=req_sacred_econ,
            requires_outward_asset_capture=req_outward_odi,
            requires_archaeo_astronomy=req_archaeo_astro,
            requires_black_projects=req_black_proj,
            requires_trans_himalayan_hydrology=req_trans_hydro,
            requires_predatory_dumping=req_pred_dumping,
            requires_apaurusheya_epistemic=req_apaurusheya,
            requires_sacred_heritage_encroachment=req_heritage_encroach,
            requires_narrative_inversion=req_narr_inversion,
            requires_malacca_chokepoint=req_malacca,
            requires_ritual_ecological_sovereignty=req_ritual_eco,
            requires_dharmic_constitutionalism=req_dharmic_const,
            requires_partition_demystification=req_part_demyst,
            requires_canonical_epic_fidelity=req_epic_fidelity,
            requires_theological_apostasy_velocity=req_theol_apostasy,
            requires_aurobindonian_integration=req_aurobindo_integ,
            requires_shastric_dietary_plurality=req_shastric_diet,
            requires_archival_primary_source=req_archival_source,
            requires_academic_gatekeeping=req_academic_gate,
            requires_succession_continuity=req_succ_cont,
            requires_linguistic_sprachbund=req_ling_sprach,
            requires_indigenous_stem=req_indig_stem,
            requires_subaltern_memory=req_subalt_mem,
            requires_industrial_attrition=req_ind_attr,
            requires_imperial_debt_overreach=req_imp_debt,
            requires_colonial_drain_extraction=req_col_drain,
            requires_basel_gold=req_basel_gold,
            requires_mnemonic_fidelity=req_mnemonic_fid,
            requires_mitrokhin_deep_state=req_mitrokhin_ds,
            requires_puranic_boundary=req_puranic_bound,
            requires_polemics_ratio=req_polemics_ratio,
            requires_kishkindha_geography=req_kishkindha_geo,
            requires_vedic_decolonization=req_vedic_decolon,
            requires_quantum_spacetime=req_quantum_st,
            requires_semiconductor_antitrust=req_semi_antitrust,
            requires_fcra_ecclesiastical=req_fcra_eccles,
            requires_cinematic_sacrality=req_cinematic_sac,
            requires_infrastructure_capex_multiplier=req_infra_capex_mult,
            requires_classical_bullion_trade=req_classical_bullion,
            requires_asymmetric_statutory_lawfare=req_asym_lawfare,
            requires_cryptographic_decentralization=req_crypto_decent,
            requires_hormuz_escalation=req_hormuz_escal,
            requires_eurodollar_shadow_liquidity=req_eurodollar_drain,
            requires_black_swan_disruption=req_black_swan,
            requires_sovereign_gold_velocity=req_sovereign_gold_vel,
            requires_geopolitical_speech_forensics=req_speech_forensics,
            requires_sovereign_public_interest=req_sov_pub_int,
            requires_adversary_timing_correlation=req_adv_timing,
            requires_documentary_provenance=req_doc_prov,
            requires_bear_raid_derivative=req_bear_raid,
            requires_offshore_debt_covenant=req_debt_cov,
            requires_exfiltration_sanctuary=req_exfil_sanc,
            requires_retaliation_threat=req_retal_threat,
            requires_vigilance_remedy=req_vigil_rem,
            requires_speech_kinesic_chromatic=req_kinesic_chrom,
            requires_speech_omission=req_speech_omit,
            requires_tbml_customs=req_tbml,
            requires_defense_scada_tamper=req_scada_tamp,
            requires_cultural_sacrality_breach=req_cult_sac,
            requires_perjury_retributive_liability=req_perj_liab,
            requires_qdt_whistleblower=req_qdt_whistle,
            requires_sovereign_capex_impact=req_capex_imp,
            requires_bis_hidden_fx_swap=req_bis_fx,
            requires_offshore_ubo_shell=req_ubo_shell,
            requires_speech_to_balance_sheet_divergence=req_speech_balsheet,
            requires_kinesic_contextual_baseline=req_kinesic_baseline,
            requires_chanakya_neeti_upadha=req_chanakya_upadha,
            requires_kautilya_mandala_shadgunya=req_kautilya_saptanga,
            requires_krishna_rajadharma_exhaustion=req_krishna_rajadharma,
            requires_cloud_monopoly_fragility=req_cloud_monopoly,
            requires_cognitive_deception_misdirection=req_cognitive_deception,
            requires_counter_intel_honeytrap=req_ci_honeytrap,
            requires_maritime_net_security=req_maritime_net_sec,
            requires_false_flag_narrative=req_false_flag_narrative,
            requires_sovereign_cyber_extortion=req_sov_cyber_extort,
            requires_maritime_port_dual_use=req_port_dual_use,
            requires_revealed_preference_divergence=req_revealed_pref_div,
            requires_sovereign_debt_syndicate=req_debt_syndicate,
            requires_asymmetric_weapon_proliferation=req_asym_weapon_leak,
            requires_legacy_infra_obsolescence=req_legacy_infra_obs,
            requires_speculative_capex_overhang=req_spec_capex_overhang,
            requires_subnational_fragmentation_lawfare=req_subnat_frag_lawfare,
            requires_civilizational_epistemic_integrity=req_civ_epistemic_int,
            requires_algorithmic_cognitive_subversion=req_algo_cog_subversion,
            requires_critical_scada_hardware_backdoor=req_scada_hw_backdoor,
            requires_circular_venture_valuation=req_circ_venture_val,
            requires_monopoly_patent_suppression=req_monopoly_patent_supp,
            requires_sub_replacement_demographic_extinction=req_sub_replace_demog,
            requires_physical_capex_multiplier=req_phys_capex_mult,
            requires_open_system_asymmetric_infiltration=req_open_sys_infil,
            requires_dynastic_shadow_cabinet=req_dynastic_shadow_cab,
            requires_superpower_naval_coercion=req_naval_coercion,
            requires_semiconductor_executive_kompromat=req_semi_kompromat,
            requires_media_intelligence_leak_timing=req_media_leak_timing,
            requires_generative_media_hegemony=req_gen_media_hegemony,
            requires_silicon_microcode_killswitch=req_silicon_microcode_killswitch,
            requires_gpu_debt_contagion=req_gpu_debt_contagion,
            # Phases 396-415: Sovereign Asymmetric War, Balance-Sheet Realism & Civilizational Sovereignty Matrix
            requires_informal_sector_divergence=req_informal_divergence,
            requires_pboc_lgfv_liquidity_trap=req_pboc_liquidity,
            requires_asymmetric_air_defense_cost_exchange=req_air_defense_cer,
            requires_hypersonic_glide_penetration=req_hypersonic_glide,
            requires_sovereign_platform_regulatory_defiance=req_platform_defiance,
            requires_institutional_cartel_cross_shareholding=req_cartel_cross_holding,
            requires_msme_solvency_asphyxiation=req_msme_asphyxiation,
            requires_nuclear_launch_under_attack_latency=req_nuclear_latency,
            requires_border_state_narco_fiscal_subversion=req_border_narco,
            requires_trilateral_superpower_condominium_exclusion=req_condominium_exclusion,
            requires_quantum_hndl_vulnerability=req_quantum_hndl,
            requires_diplomatic_nonverbal_optics=req_diplomatic_optics,
            requires_cultural_religious_grayzone_lawfare=req_grayzone_lawfare,
            requires_critical_mineral_weaponization=req_mineral_weaponization,
            requires_agrochemical_food_weaponization=req_food_weaponization,
            requires_aviation_transit_slot_cartel=req_aviation_cartel,
            requires_airborne_command_survivability=req_airborne_command,
            requires_sub_tactical_honeytrap_espionage=req_honeytrap_espionage,
            requires_naval_electronic_warfare_suppression=req_naval_ew,
            requires_civilizational_epistemic_historiography=req_historiography_decolonial,
            # Phases 416-433: Sovereign Forensic Sieves & Strategic Council Titans
            requires_asymmetric_scada_blackout=req_scada_blackout,
            requires_synchronized_media_cartel=req_media_cartel,
            requires_deep_state_banking_lawfare=req_banking_lawfare,
            requires_directed_energy_weapon=req_dew_weapon,
            requires_multilateral_alliance_autonomy=req_alliance_autonomy,
            requires_offshore_banking_repatriation=req_offshore_repatriation,
            requires_foreign_intel_penetration=req_foreign_intel_pen,
            requires_cognitive_atrophy_displacement=req_cognitive_atrophy,
            requires_demographic_border_fortification=req_demographic_fort,
            requires_algorithmic_faceless_procurement=req_faceless_procurement,
            requires_investigative_forensics_negative_space=req_investigative_forensics,
            requires_sovereign_debt_rollover_risk=req_sovereign_debt_rollover,
            requires_asymmetric_subversion_counter_penetration=req_doval_subversion,
            requires_sovereign_capex_escape_velocity=req_modi_capex,
            requires_multipolar_hedging_reciprocal_leverage=req_jaishankar_hedging,
            requires_credit_rating_cartel_bias=req_sanyal_rating,
            requires_civilizational_jurisprudence_decolonial=req_deepak_jurisprudence,
            requires_empirical_falsification_cryptographic=req_ranga_falsification,
            # Phases 434-440: Semiotic Iconography, Global Polycrisis Cascades & Sovereign Resilient Sieves
            requires_semiotic_deconstruction=req_semiotic_deconstruct,
            requires_polycrisis_cascade=req_polycrisis_cascade,
            requires_cultural_religious_grayzone_subversion=req_grayzone_subversion,
            requires_glp1_metabolic_shift=req_glp1_metabolic,
            requires_leo_orbital_weaponization=req_leo_orbital,
            requires_taiwan_semiconductor_choke=req_taiwan_choke,
            requires_electoral_lawfare_polarization=req_electoral_lawfare,
            # Phases 441-447: Sovereign Forensic Sieves & Multilateral Autonomy Tensors
            requires_tripolar_condominium=req_tripolar_condominium,
            requires_ai_labor_displacement=req_ai_labor_displacement,
            requires_diaspora_subversion=req_diaspora_subversion,
            requires_gpu_export_chokepoint=req_gpu_export_chokepoint,
            requires_reer_appreciation_friction=req_reer_appreciation,
            requires_supranational_deep_state=req_supranational_deep_state,
            requires_bullion_cyber_sovereignty=req_bullion_cyber_sovereignty,
            # Phases 448-449: Horizon Polycrisis & Multilateral Defense Interoperability
            requires_economist_polycrisis=req_economist_polycrisis,
            requires_defense_interoperability=req_defense_interoperability,
            # Phase 450: Subcontinental Proxy Risk & Silicon Venture Oligarchies
            requires_subcontinental_proxy_risk=req_subcontinental_proxy_risk,
            # Phase 454: Sovereign Cognitive Subterranean & Kinetic Interoperability
            requires_sovereign_hyper_resilience=req_sovereign_hyper_resilience,
            # Phases 455-460 Capstones: Epistemic Validation & Sovereign Industrial Propulsion
            requires_epistemic_validation=req_epistemic_validation,
            requires_industrial_propulsion=req_industrial_propulsion,
            # Phases 461-464: Bullion/Marine/Brand, Impossible Trinity/OPSEC, Constitutional/Grayzone, Mother-Machine/Sonar/Hydrocide
            requires_bullion_marine_brand_sovereignty=req_bullion_marine_brand_sovereignty,
            requires_impossible_trinity_tbml_opsec=req_impossible_trinity_tbml_opsec,
            requires_constitutional_grayzone_proxy=req_constitutional_grayzone_proxy,
            requires_mother_machine_sonar_hydrocide=req_mother_machine_sonar_hydrocide,
            speaker_profiles=resolved_profiles,
            confidence_threshold=0.80
        )



```

## Module: `geo_engine/core/speaker_profiler.py`

```python
"""
Epistemic Speaker Archetype Registry & Profiling Engine.
Maps prominent political, civilizational, economic, and strategic thinkers
to structured cognitive persona profiles that track baseline priors,
epistemic strengths, characteristic blind spots, and discourse vectors.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import re


class SpeakerArchetype(str, Enum):
    """Canonical intellectual and statecraft archetypes."""
    TRADITIONALIST_MERITOCRACY = "TRADITIONALIST_MERITOCRACY"
    INDIC_DECOLONIAL_JURISPRUDENCE = "INDIC_DECOLONIAL_JURISPRUDENCE"
    DEEP_TECH_NATIONALISM = "DEEP_TECH_NATIONALISM"
    SUBALTERN_CONSTITUTIONALISM = "SUBALTERN_CONSTITUTIONALISM"
    BUREAUCRATIC_INSTITUTIONALISM = "BUREAUCRATIC_INSTITUTIONALISM"
    PRAGMATIC_SOVEREIGN_STATECRAFT = "PRAGMATIC_SOVEREIGN_STATECRAFT"
    SCIENTIFIC_EMPIRICISM = "SCIENTIFIC_EMPIRICISM"
    GEOECONOMIC_TIMELINE_MAPPING = "GEOECONOMIC_TIMELINE_MAPPING"
    INDIC_CULTURAL_RHETORIC = "INDIC_CULTURAL_RHETORIC"
    VEDIC_SCIENTIFIC_NATIONALISM = "VEDIC_SCIENTIFIC_NATIONALISM"
    ECOLOGICAL_CONSCIOUSNESS_REALISM = "ECOLOGICAL_CONSCIOUSNESS_REALISM"
    EPIGRAPHIC_ARCHAEOLOGY_HISTORIOGRAPHY = "EPIGRAPHIC_ARCHAEOLOGY_HISTORIOGRAPHY"
    CANONICAL_EPIC_TEXTUAL_FIDELITY = "CANONICAL_EPIC_TEXTUAL_FIDELITY"
    TACTICAL_MILITARY_REALISM = "TACTICAL_MILITARY_REALISM"
    INDEPENDENT_ANALYST = "INDEPENDENT_ANALYST"


@dataclass(frozen=True)
class SpeakerProfile:
    """Immutable cognitive and epistemic profile for a strategic commentator or leader."""
    name: str
    canonical_id: str
    archetype: SpeakerArchetype
    core_frameworks: List[str] = field(default_factory=list)
    characteristic_strengths: List[str] = field(default_factory=list)
    primary_blind_spots: List[str] = field(default_factory=list)
    frequent_thematic_tokens: List[str] = field(default_factory=list)
    baseline_reliability_weight: float = 0.85

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "canonical_id": self.canonical_id,
            "archetype": self.archetype.value,
            "core_frameworks": list(self.core_frameworks),
            "characteristic_strengths": list(self.characteristic_strengths),
            "primary_blind_spots": list(self.primary_blind_spots),
            "frequent_thematic_tokens": list(self.frequent_thematic_tokens),
            "baseline_reliability_weight": self.baseline_reliability_weight,
        }


class EpistemicSpeakerProfiler:
    """Registry and resolver for speaker epistemic profiles."""

    _REGISTRY: Dict[str, SpeakerProfile] = {}

    @classmethod
    def register_profile(cls, profile: SpeakerProfile) -> None:
        """Registers or updates a speaker profile in the registry."""
        cls._REGISTRY[profile.canonical_id.lower()] = profile
        cls._REGISTRY[profile.name.lower()] = profile

    @classmethod
    def get_profile(cls, name_or_id: str) -> Optional[SpeakerProfile]:
        """Looks up a speaker profile by name or canonical ID."""
        if not name_or_id:
            return None
        key = name_or_id.strip().lower()
        if key in cls._REGISTRY:
            return cls._REGISTRY[key]
        for p in cls._REGISTRY.values():
            if key in p.name.lower() or p.name.lower() in key:
                return p
        return None

    @classmethod
    def resolve_from_text(cls, text: str) -> List[SpeakerProfile]:
        """Scans arbitrary text for mentions of registered speaker profiles."""
        if not text:
            return []
        text_lower = text.lower()
        matched: List[SpeakerProfile] = []
        seen = set()

        for p in cls._REGISTRY.values():
            if p.canonical_id in seen:
                continue
            # Regex word boundary check for name
            escaped_name = re.escape(p.name.lower())
            if re.search(r"(?<!\w)" + escaped_name + r"(?!\w)", text_lower):
                matched.append(p)
                seen.add(p.canonical_id)
                continue
            # Check frequent thematic tokens if 2 or more appear together
            token_matches = [t for t in p.frequent_thematic_tokens if re.search(r"(?<!\w)" + re.escape(t.lower()) + r"(?!\w)", text_lower)]
            if len(token_matches) >= 2:
                matched.append(p)
                seen.add(p.canonical_id)

        return matched

    @classmethod
    def list_profiles(cls) -> List[SpeakerProfile]:
        """Returns all uniquely registered speaker profiles."""
        unique = {}
        for p in cls._REGISTRY.values():
            unique[p.canonical_id] = p
        return list(unique.values())


# ---------------------------------------------------------------------------
# Canonical Pre-Seeded Speaker Profiles (The 7-Master Council & Key Thinkers)
# ---------------------------------------------------------------------------

_CANONICAL_PROFILES = [
    SpeakerProfile(
        name="Neeraj Atri",
        canonical_id="PROF-NEERAJ-ATRI",
        archetype=SpeakerArchetype.TRADITIONALIST_MERITOCRACY,
        core_frameworks=[
            "Traditionalist Savarna meritocracy",
            "NCERT textbook & historical distortion critique",
            "Anti-welfarism & middle-class direct tax burden",
            "SC/ST Act due process & Section 18A critique",
        ],
        characteristic_strengths=[
            "High forensic rigor on educational syllabus distortions",
            "Sharp identification of statutory asymmetries and presumption of guilt",
            "Direct exposure of middle-class fiscal exploitation without social safety nets",
            "Unflinching critique of ruling establishment's failure to build independent intellectual ecosystems",
        ],
        primary_blind_spots=[
            "Underestimates macro-geopolitical necessity of social welfarism as a stability floor",
            "Downplays historical subaltern socio-economic exclusion and need for integration",
            "Conflates pragmatic electoral de-escalation with civilizational cowardice",
        ],
        frequent_thematic_tokens=["neeraj atri", "blunder called modi", "sc st act", "section 18a", "kashinath mahajan", "jizya", "middle class tax"],
        baseline_reliability_weight=0.88,
    ),
    SpeakerProfile(
        name="J. Sai Deepak",
        canonical_id="PROF-J-SAI-DEEPAK",
        archetype=SpeakerArchetype.INDIC_DECOLONIAL_JURISPRUDENCE,
        core_frameworks=[
            "Indic decoloniality & civilizational constitutionalism",
            "Temple autonomy & HRCE statutory dismantling",
            "Statutory double-standards (Places of Worship Act, Waqf Act Section 40)",
            "Epistemic decolonization of Indian jurisprudence",
        ],
        characteristic_strengths=[
            "Exhaustive legal and constitutional analysis of colonial continuities",
            "Deep textual and historical grounding in Indic jurisprudence and Sanatan traditions",
            "Rigorous courtroom advocacy for institutional autonomy of Hindu institutions",
        ],
        primary_blind_spots=[
            "Over-reliance on legal and constitutional remedies for deep socioeconomic fractures",
            "Less emphasis on industrial manufacturing, defense technology, and kinetic deterrence",
        ],
        frequent_thematic_tokens=["j. sai deepak", "sai deepak", "india that is bharat", "india bharat and pakistan", "temple autonomy", "places of worship act", "waqf act"],
        baseline_reliability_weight=0.92,
    ),
    SpeakerProfile(
        name="Srijan Pal Singh",
        canonical_id="PROF-SRIJAN-PAL-SINGH",
        archetype=SpeakerArchetype.DEEP_TECH_NATIONALISM,
        core_frameworks=[
            "Dr. A.P.J. Abdul Kalam techno-nationalist vision",
            "Indigenous defense R&D CapEx & semiconductor roadmaps",
            "Youth demographic dividend mobilization",
            "Aerospace, avionics & high-tech supply chain sovereignty",
        ],
        characteristic_strengths=[
            "Data-driven focus on science, technology, engineering, and mathematics (STEM)",
            "Clear articulation of deep-tech industrial autonomy and defense manufacturing",
            "Optimistic, forward-looking youth and educational mobilization frameworks",
        ],
        primary_blind_spots=[
            "Technocratic optimism that may underestimate entrenched bureaucratic inertia",
            "Less emphasis on domestic socio-legal fault lines and ideological warfare",
        ],
        frequent_thematic_tokens=["srijan pal singh", "srijan", "kalam", "semi-conductor", "defense r&d", "deep tech", "demographic dividend"],
        baseline_reliability_weight=0.90,
    ),
    SpeakerProfile(
        name="B.R. Ambedkar",
        canonical_id="PROF-BR-AMBEDKAR",
        archetype=SpeakerArchetype.SUBALTERN_CONSTITUTIONALISM,
        core_frameworks=[
            "Annihilation of caste & subaltern emancipation",
            "Constitutional democracy as a moral framework",
            "Critique of communist totalitarianism and uncritical political Bhakti",
            "Economic self-reliance and monetary reform (Problem of the Rupee)",
        ],
        characteristic_strengths=[
            "Uncompromising defense of individual dignity and institutional equality",
            "Prescient warning against hero-worship in politics eroding constitutional democracy",
            "Rigorous economic understanding of currency, taxation, and labor rights",
            "Explicit rejection of violent Marxism and communal factionalism",
        ],
        primary_blind_spots=[
            "Modern political misappropriation that reduces his comprehensive philosophy to perpetual reservation politics",
        ],
        frequent_thematic_tokens=["b.r. ambedkar", "ambedkar", "babasaheb", "annihilation of caste", "rajya sabha 1953", "hero worship", "constitutional morality"],
        baseline_reliability_weight=0.96,
    ),
    SpeakerProfile(
        name="Hamid Ansari",
        canonical_id="PROF-HAMID-ANSARI",
        archetype=SpeakerArchetype.BUREAUCRATIC_INSTITUTIONALISM,
        core_frameworks=[
            "Nehruvian diplomatic institutionalism",
            "West Asian diplomatic equilibrium & Non-Alignment (NAM)",
            "Minority protection within constitutional secularism",
            "Protocol-driven multilateral engagement",
        ],
        characteristic_strengths=[
            "Decades of institutional diplomatic experience across West Asia and the UN",
            "Strict adherence to diplomatic protocol and institutional proceduralism",
        ],
        primary_blind_spots=[
            "Severe vulnerability to covert intelligence asset compromises (e.g. 1992 Tehran RAW network)",
            "Reluctance to deploy hard sovereign power or asymmetric kinetic deterrence",
            "Detachment from indigenous civilizational consciousness",
        ],
        frequent_thematic_tokens=["hamid ansari", "ansari", "tehran embassy", "nehruvian diplomacy", "institutional secularism"],
        baseline_reliability_weight=0.78,
    ),
    SpeakerProfile(
        name="Narendra Modi",
        canonical_id="PROF-NARENDRA-MODI",
        archetype=SpeakerArchetype.PRAGMATIC_SOVEREIGN_STATECRAFT,
        core_frameworks=[
            "Saturation DBT welfarism & subaltern electoral consolidation",
            "Civilizational revivalism (Kashi, Ayodhya, Ujjain, Sengol)",
            "Mass physical infrastructure CapEx (highways, ports, railway freight, DPI)",
            "Pragmatic strategic autonomy & kinetic deterrence (Balakot, Article 370)",
        ],
        characteristic_strengths=[
            "Unmatched electoral mobilization and subaltern demographic consolidation",
            "Decisive execution of long-pending constitutional changes (Article 370, CAA)",
            "Building high-velocity digital public infrastructure and macroeconomic social safety floor",
            "Assertive non-aligned foreign policy resisting Western moral pressure",
        ],
        primary_blind_spots=[
            "Prone to high-decibel PR theatrics that outpace structural ground reforms",
            "Persistent fiscal squeeze on salaried middle-class taxpayers",
            "Vulnerability to street vetoes causing sudden strategic policy retreats (Farm Laws)",
            "Neglect of independent intellectual and academic ecosystem building",
        ],
        frequent_thematic_tokens=["narendra modi", "modi", "vishwa bandhu", "viksit bharat", "dbt", "swachh bharat", "temple of democracy"],
        baseline_reliability_weight=0.92,
    ),
    SpeakerProfile(
        name="Ajit Doval",
        canonical_id="PROF-AJIT-DOVAL",
        archetype=SpeakerArchetype.PRAGMATIC_SOVEREIGN_STATECRAFT,
        core_frameworks=[
            "Defensive-offense doctrine & cross-domain deterrence",
            "Nexus between internal security subversion and external sovereignty",
            "Cyber-kinetic and intelligence synergy",
            "Border infrastructure hardening & non-kinetic retaliation",
        ],
        characteristic_strengths=[
            "Operational mastery of counter-terrorism and covert intelligence operations",
            "Clear strategic doctrine linking domestic stability to external deterrence",
            "Rapid tactical crisis management across volatile borders (Doklam, Galwan)",
        ],
        primary_blind_spots=[
            "High concentration of strategic decision-making within small executive cabals",
            "Less focus on macroeconomic fiscal policies and global trade architecture",
        ],
        frequent_thematic_tokens=["ajit doval", "doval", "defensive offense", "doval doctrine", "internal external security", "kinetic deterrence"],
        baseline_reliability_weight=0.94,
    ),
    SpeakerProfile(
        name="S. Jaishankar",
        canonical_id="PROF-S-JAISHANKAR",
        archetype=SpeakerArchetype.PRAGMATIC_SOVEREIGN_STATECRAFT,
        core_frameworks=[
            "The India Way & strategic multi-alignment",
            "Mahabharata ethical statecraft (Artha and Dharma equilibrium)",
            "Weaponized interdependence & critical supply chain hedging",
            "Rejection of Western moral lecturing & diplomatic realism",
        ],
        characteristic_strengths=[
            "Razor-sharp articulation of Indian strategic interests on global stages",
            "Skillful maneuvering between Quad, BRICS, and Russian hydrocarbon supplies",
            "Deep comprehension of China's revisionist strategy along the Himalayan frontier",
        ],
        primary_blind_spots=[
            "Diplomatic success occasionally masks deep underlying domestic manufacturing bottlenecks",
            "Vulnerability of overseas Indian diaspora communities to host-nation lawfare and nativism",
        ],
        frequent_thematic_tokens=["s. jaishankar", "jaishankar", "india way", "strategic autonomy", "multi-alignment", "mahabharata statecraft"],
        baseline_reliability_weight=0.95,
    ),
    SpeakerProfile(
        name="Sanjeev Sanyal",
        canonical_id="PROF-SANJEEV-SANYAL",
        archetype=SpeakerArchetype.PRAGMATIC_SOVEREIGN_STATECRAFT,
        core_frameworks=[
            "Complex Adaptive Systems (CAS) & agile policy formulation",
            "Indian Ocean maritime trade history & naval civilizational heritage",
            "Supply-side economic CapEx over demand-side populist stimulus",
            "Judicial, administrative, and legal system deregulation",
        ],
        characteristic_strengths=[
            "Sophisticated application of complexity theory and feedback loops to macroeconomics",
            "Rigorous debunking of colonial and Eurocentric maritime historical narratives",
            "Data-driven focus on logistics friction, court delays, and process simplification",
        ],
        primary_blind_spots=[
            "May underestimate political survival imperatives that compel governments to prioritize populist welfarism",
        ],
        frequent_thematic_tokens=["sanjeev sanyal", "sanyal", "complex adaptive systems", "ocean of churn", "maritime history", "supply side"],
        baseline_reliability_weight=0.93,
    ),
    SpeakerProfile(
        name="Anand Ranganathan",
        canonical_id="PROF-ANAND-RANGANATHAN",
        archetype=SpeakerArchetype.SCIENTIFIC_EMPIRICISM,
        core_frameworks=[
            "Scientific empiricism & evidentiary rigor",
            "Absolute free speech defense & anti-censorship advocacy",
            "Relentless exposure of statutory double-standards and appeasement",
            "Separation of state and religious institutions",
        ],
        characteristic_strengths=[
            "Methodical, data-backed confrontation of political and religious hypocrisy across all parties",
            "Fearless defense of freedom of expression against statutory blasphemy and speech codes",
            "Clear empirical exposure of state-enforced religious asymmetries",
        ],
        primary_blind_spots=[
            "Purity of principle occasionally conflicts with messy realpolitik compromises needed to govern a 1.4B diverse society",
        ],
        frequent_thematic_tokens=["anand ranganathan", "ranganathan", "hindus in hindu rashtra", "free speech", "statutory double standards", "scientific empiricism"],
        baseline_reliability_weight=0.91,
    ),
    SpeakerProfile(
        name="Ankit Shah",
        canonical_id="PROF-ANKIT-SHAH",
        archetype=SpeakerArchetype.GEOECONOMIC_TIMELINE_MAPPING,
        core_frameworks=[
            "Global geoeconomic timeline mapping & dedollarization cycles",
            "Western sovereign debt saturation & US Treasury weaponization",
            "Bilateral currency settlement & commodity-backed reserves",
            "Geopolitical inflection points (2019-2029-2039 financial warfare)",
        ],
        characteristic_strengths=[
            "Macro-level integration of financial flows, sovereign debt traps, and currency warfare",
            "Longitudinal perspective connecting historical monetary agreements to current supply chain ruptures",
        ],
        primary_blind_spots=[
            "Timeline projections can be overly deterministic regarding exact dates of global financial collapses",
        ],
        frequent_thematic_tokens=["ankit shah", "dedollarization", "currency war", "brics currency", "sovereign debt", "geoeconomic timeline"],
        baseline_reliability_weight=0.87,
    ),
    SpeakerProfile(
        name="Kumar Vishwas",
        canonical_id="PROF-KUMAR-VISHWAS",
        archetype=SpeakerArchetype.INDIC_CULTURAL_RHETORIC,
        core_frameworks=[
            "Apne Apne Ram civilizational synthesis",
            "Poetic cultural mobilization & mass Hindi-Awadhi resonance",
            "Ramcharitmanas ethical statecraft (Ramrajya ideal)",
            "Subaltern cultural bridging & anti-hypocrisy political satire",
        ],
        characteristic_strengths=[
            "Unrivaled oratorical, literary, and poetic mass engagement across demographics",
            "De-hyphenating classical Indic traditions from sectarian dogma into accessible cultural pride",
            "Deep textual mastery of Tulsidas, Valmiki, Nirala, Dinkar, and Bharti",
            "Effective use of humor and satire to dismantle moral sanctimony in contemporary politics",
        ],
        primary_blind_spots=[
            "Literary and poetic romanticism that can understate hard macroeconomic fiscal constraints",
            "Less emphasis on kinetic military technicalities, global supply chains, and industrial manufacturing",
        ],
        frequent_thematic_tokens=[
            "kumar vishwas", "dr kumar vishwas", "apne apne ram", "ramcharitmanas",
            "kavi sammelan", "tulsidas", "koi deewana kehta hai", "ram katha",
        ],
        baseline_reliability_weight=0.89,
    ),
    SpeakerProfile(
        name="Sudhanshu Trivedi",
        canonical_id="PROF-SUDHANSHU-TRIVEDI",
        archetype=SpeakerArchetype.VEDIC_SCIENTIFIC_NATIONALISM,
        core_frameworks=[
            "Vedic scientific-astronomical correlation & historical chronology",
            "Parliamentary dialectics & forensic political debate",
            "Rebuttal of Marxist, Eurocentric, and colonial historiography",
            "Civilizational constitutionalism & Sanatan philosophical defense",
        ],
        characteristic_strengths=[
            "Encyclopedic recall of Sanskrit scriptures, Vedic astronomy, and Indian political history",
            "Mechanical engineering analytical background applied to scriptural and scientific validation",
            "Razor-sharp parliamentary and televised debate forensic rebuttal",
            "Articulate deconstruction of linguistic and historical distortions in national discourse",
        ],
        primary_blind_spots=[
            "Party-line organizational defense that can lead to defensiveness on government economic lapses",
            "Tendency to deflect administrative friction into broad historical and civilizational polemics",
        ],
        frequent_thematic_tokens=[
            "sudhanshu trivedi", "dr sudhanshu trivedi", "vedic science", "rajya sabha",
            "sanatan parampara", "bjp spokesperson", "kalpa", "yuga chronology", "shastra",
        ],
        baseline_reliability_weight=0.91,
    ),
    SpeakerProfile(
        name="Pushpendra Kulshrestha",
        canonical_id="PROF-PUSHPENDRA-KULSHRESTHA",
        archetype=SpeakerArchetype.INDIC_CULTURAL_RHETORIC,
        core_frameworks=[
            "Civilizational nationalism & Hindutva historical reinterpretation",
            "Counter-narrative journalism against alleged media bias & colonial liberal historiography",
            "Grassroots Hindu awakening & Sanatan cultural mobilization",
            "Deconstruction of political-media nexus & dominant narrative fraud",
        ],
        characteristic_strengths=[
            "Mass grassroots reach on digital platforms (Instagram, Facebook, YouTube) with high emotional resonance",
            "High-energy populist framing making complex civilizational history accessible to non-academic audiences",
            "Persistent counter-programmatic journalism targeting dominant media narratives",
            "Rapid mobilization of civilizational pride as a unifying emotional force",
        ],
        primary_blind_spots=[
            "High ideological intensity may reduce factual granularity and nuance in contested historical claims",
            "Populist emotional packaging can amplify partially verified or single-source claims",
            "Limited engagement with cross-ideological empirical counter-evidence or comparative historical data",
        ],
        frequent_thematic_tokens=[
            "pushpendra kulshrestha", "pushpendra", "kulshrestha",
            "sanatan dharma", "hindutva", "media bias", "hindu jagriti",
            "sansad tv", "cultural nationalism", "bharat mata",
        ],
        baseline_reliability_weight=0.82,
    ),
    SpeakerProfile(
        name="Sadhguru (Jaggi Vasudev)",
        canonical_id="PROF-SADHGURU",
        archetype=SpeakerArchetype.ECOLOGICAL_CONSCIOUSNESS_REALISM,
        core_frameworks=[
            "Conscious Planet & Save Soil ecological foundation (minimum 3-6% soil organic content)",
            "Yogic science & empirical inner technology (Adiyogi, Inner Engineering, consecrated spaces)",
            "Temple revitalization & liberation from state bureaucratic control (Free Temples movement)",
            "Civilizational soft power & de-polarized global leadership (WEF, UN COP, Oxford/Harvard)",
            "Maryada Purushottama civilizational consciousness (Rama as supreme balance and restraint)",
            "River revitalization & agro-forestry water security (Cauvery Calling)",
        ],
        characteristic_strengths=[
            "Massive global and grassroots ecological mobilization cutting across national and political borders",
            "Articulating Indic spiritual technologies in universal, non-dogmatic, and scientific language",
            "Fearless advocacy for institutional temple autonomy and restoration of sacred local economies",
            "De-escalating toxic political polarization through inner mental balance and conscious statecraft",
            "Demonstrating that soil organic vitality is the non-negotiable physical prerequisite for human peace",
        ],
        primary_blind_spots=[
            "Ecological soil transformation requires long generational horizons that face short-term electoral inertia",
            "State bureaucracies resist relinquishing lucrative temple revenue streams without statutory or judicial compulsion",
        ],
        frequent_thematic_tokens=[
            "sadhguru", "jaggi vasudev", "save soil", "conscious planet", "cauvery calling", "inner engineering",
            "adiyogi", "free temples", "dhyanalinga", "isha foundation", "soil extinction", "soil organic content",
            "isha", "maryada", "consecrated spaces", "living soil",
        ],
        baseline_reliability_weight=0.94,
    ),
    SpeakerProfile(
        name="Dr. Meenakshi Jain",
        canonical_id="PROF-MEENAKSHI-JAIN",
        archetype=SpeakerArchetype.EPIGRAPHIC_ARCHAEOLOGY_HISTORIOGRAPHY,
        core_frameworks=[
            "Primary epigraphic archaeology & inscriptional evidence",
            "Temple destruction ledgers & revenue settlement records reconciliation",
            "Deconstruction of secularist and colonial historiographical denialism",
            "Sacred geography and pilgrimage continuity (Rama and Ayodhya, Kashi, Mathura, Sati)",
        ],
        characteristic_strengths=[
            "Forensic reliance on primary inscriptional and archaeological excavation records",
            "Refusal to cite ideologically filtered secondary narratives",
            "Meticulous archival citation of Persian, British, and Sanskrit primary sources",
            "Irrefutable evidentiary standards accepted in judicial proceedings (Ayodhya Supreme Court verdict)",
        ],
        primary_blind_spots=[
            "Focuses predominantly on medieval and ancient historical/religious documentation rather than modern kinetic or macroeconomic mechanics",
        ],
        frequent_thematic_tokens=[
            "meenakshi jain", "dr meenakshi jain", "epigraphy", "inscriptions", "rama and ayodhya",
            "kashi vishwanath", "vasudeva krishna", "archaeological survey", "temple demolition records",
            "sacred geography", "flight of deities", "sati historical record",
        ],
        baseline_reliability_weight=0.96,
    ),
    SpeakerProfile(
        name="Ami Ganatra",
        canonical_id="PROF-AMI-GANATRA",
        archetype=SpeakerArchetype.CANONICAL_EPIC_TEXTUAL_FIDELITY,
        core_frameworks=[
            "Canonical Sanskrit epic critical editions (BORI Mahabharata, Baroda Valmiki Ramayana)",
            "Shlokic textual precision and manuscript variant reconciliation",
            "Purging modern pop-cultural revisionism, cinematic interpolations, and fictional tropes",
            "Shastric statecraft, ethics, and strategic decision-making analysis",
        ],
        characteristic_strengths=[
            "Exact chapter-and-verse Sanskrit citations dispelling popular myths",
            "Rigorous textual methodology debunking Marxist and modern moral inversion theories",
            "Accessible exposition of classical statecraft (Mahabharata Unravelled, Ramayana Unravelled)",
            "High analytical integrity reconciling complex moral dilemmas without whitewashing",
        ],
        primary_blind_spots=[
            "Exclusively textual and manuscript focused; less engagement with contemporary international trade or fiscal instruments",
        ],
        frequent_thematic_tokens=[
            "ami ganatra", "ganatra", "mahabharata unravelled", "ramayana unravelled",
            "bori critical edition", "baroda critical edition", "shlokic evidence", "karna myth",
            "dharma yuddha ethics", "canonical epic fidelity", "valmiki shlokas",
        ],
        baseline_reliability_weight=0.95,
    ),
    SpeakerProfile(
        name="Major Gaurav Arya",
        canonical_id="PROF-GAURAV-ARYA",
        archetype=SpeakerArchetype.TACTICAL_MILITARY_REALISM,
        core_frameworks=[
            "Kinetic border realism & counter-insurgency deterrence",
            "Asymmetric retaliatory cost imposition on hostile deep-state proxy networks",
            "Deconstruction of adversary cognitive warfare and hybrid propaganda",
            "Information operations, veterans' perspectives, and national security clarity",
        ],
        characteristic_strengths=[
            "Direct infantry operational experience along the LoC and counter-terror theatres",
            "Hard-hitting, accessible strategic communication exposing state-sponsored terror financing",
            "Zero tolerance for diplomatic equivocation or appeasement narratives",
            "Clear strategic foresight regarding adversary military-economic vulnerabilities (e.g. Pakistan army commercial empire / Fauji Foundation)",
        ],
        primary_blind_spots=[
            "High-intensity tactical focus can occasionally prioritize immediate kinetic retaliation over long-term diplomatic or multilateral balancing nuances",
        ],
        frequent_thematic_tokens=[
            "gaurav arya", "major gaurav arya", "major arya", "the chanakya dialogues",
            "kinetic deterrence", "cross border terror", "hybrid warfare", "line of control",
            "rawalpindi ghq", "asymmetric cost", "tactical deterrence", "military realism",
        ],
        baseline_reliability_weight=0.90,
    ),
]

for _prof in _CANONICAL_PROFILES:
    EpistemicSpeakerProfiler.register_profile(_prof)

```

## Module: `geo_engine/core/temporal_guardrail.py`

```python
"""
Temporal Guardrail to prevent future-data hallucinations and temporal conflation.
Enforces strict boundaries between verified empirical archives, live data,
and prospective/horizon (e.g., 2026) game-theoretic projections.
"""

from datetime import datetime
from typing import Tuple
from .models import TemporalMode, SummitEvent, get_system_reference_date


class TemporalGuardrail:
    """
    Validates the temporal frame of an analysis request.
    Prevents confusing retrospective reporting with prospective scenario projections.
    """

    REFERENCE_DATE = get_system_reference_date()

    CONSTITUTIONAL_TENURE_REGISTRY = {
        "gyanesh_kumar": [
            {
                "office": "Chief Election Commissioner",
                "start_date": "2025-02-19",
                "end_date": "2029-01-26",
                "predecessor": "Rajiv Kumar"
            },
            {
                "office": "Election Commissioner",
                "start_date": "2024-03-15",
                "end_date": "2025-02-18",
                "predecessor": "Anup Chandra Pandey"
            },
            {
                "office": "Secretary, Ministry of Cooperation",
                "start_date": "2022-05-01",
                "end_date": "2024-01-31",
                "predecessor": "Devendra Kumar Singh"
            }
        ],
        "rajiv_kumar": [
            {
                "office": "Chief Election Commissioner",
                "start_date": "2022-05-15",
                "end_date": "2025-02-18",
                "predecessor": "Sushil Chandra"
            }
        ],
        "sukhbir_singh_sandhu": [
            {
                "office": "Election Commissioner",
                "start_date": "2024-03-15",
                "end_date": "2029-02-01",
                "predecessor": "Arun Goel"
            }
        ]
    }

    @classmethod
    def verify_chronological_feasibility(
        cls,
        person_key: str,
        office_keyword: str,
        event_date_str: str
    ) -> dict:
        """
        Level-0 Atomic Epistemic Gate:
        Mathematically asserts whether a constitutional officer was legally in office on event_date.
        Prevents anachronistic fabrications from entering macro-analytic evaluation.
        """
        normalized_key = person_key.lower().strip().replace(" ", "_")
        tenures = cls.CONSTITUTIONAL_TENURE_REGISTRY.get(normalized_key, [])

        if not tenures:
            return {
                "is_chronologically_feasible": True,
                "verified": False,
                "message": f"Officer '{person_key}' not in static gazette registry; defaulting to open verification."
            }

        # Match office
        office_match = None
        for t in tenures:
            if office_keyword.lower() in t["office"].lower():
                office_match = t
                break

        if not office_match:
            return {
                "is_chronologically_feasible": False,
                "verified": True,
                "classification": "ANACHRONISTIC_OFFICE_MISMATCH",
                "message": f"'{person_key}' never held office matching '{office_keyword}'."
            }

        start = office_match["start_date"]
        end = office_match["end_date"]
        event_clean = event_date_str.strip()[:10]

        if event_clean < start:
            predecessor = office_match.get("predecessor", "Predecessor")
            return {
                "is_chronologically_feasible": False,
                "verified": True,
                "classification": "ANACHRONISTIC_FABRICATION",
                "message": (
                    f"Chronologically impossible: '{person_key}' did not assume office as '{office_match['office']}' "
                    f"until {start}. Event occurred on {event_date_str} under predecessor '{predecessor}'."
                )
            }
        elif event_clean > end:
            return {
                "is_chronologically_feasible": False,
                "verified": True,
                "classification": "ANACHRONISTIC_FABRICATION",
                "message": (
                    f"Chronologically impossible: '{person_key}' demitted office as '{office_match['office']}' "
                    f"on {end}. Event occurred on {event_date_str}."
                )
            }

        return {
            "is_chronologically_feasible": True,
            "verified": True,
            "classification": "CHRONOLOGICALLY_VERIFIED",
            "message": f"Verified: '{person_key}' was incumbent in '{office_match['office']}' on {event_date_str}."
        }

    @classmethod
    def get_reference_date(cls) -> datetime:
        """Returns the centralized runtime reference date."""
        return get_system_reference_date()

    @classmethod
    def evaluate_event_mode(cls, summit: SummitEvent) -> Tuple[TemporalMode, str]:
        """
        Determines the epistemic temporal mode of the summit.
        """
        current_year = get_system_reference_date().year
        if summit.year < current_year:
            mode = TemporalMode.EMPIRICAL_HISTORICAL
            guidance = (
                f"Summit year {summit.year} is in the historical past. "
                "Analysis must be grounded in ratified communiques and empirical balance-of-payments archives."
            )
        elif summit.year == current_year:
            mode = TemporalMode.PROSPECTIVE_SCENARIO
            guidance = (
                f"Summit year {summit.year} is current/horizon. "
                "Analysis must be strictly partitioned into: "
                "(1) Verified institutional trajectory & established national redlines, and "
                "(2) Game-theoretic payoff matrix projections. "
                "Zero hallucinated treaties permitted."
            )
        else:
            mode = TemporalMode.PROSPECTIVE_SCENARIO
            guidance = (
                f"Summit year {summit.year} is in the prospective future. "
                "All outputs must be branded as [PROSPECTIVE_GAME_THEORETIC_MODELING]."
            )
        return mode, guidance

    @classmethod
    def enforce_prospective_tagging(cls, text: str, mode: TemporalMode) -> str:
        """
        Ensures prospective projections are explicitly tagged so user interfaces
        do not present future simulations as historical facts.
        """
        if mode == TemporalMode.PROSPECTIVE_SCENARIO and not text.startswith("[PROSPECTIVE_MODEL]"):
            return f"[PROSPECTIVE_MODEL] {text}"
        return text

```

## Module: `geo_engine/knowledge_bridge.py`

```python
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

```
