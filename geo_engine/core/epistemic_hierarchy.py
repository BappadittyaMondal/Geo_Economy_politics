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
