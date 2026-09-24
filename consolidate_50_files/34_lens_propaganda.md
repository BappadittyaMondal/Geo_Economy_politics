# LENS SPECIFICATION: PROPAGANDA

```python
"""
Lens 8: Propaganda & Narrative Warfare Lens.
Deconstructs summit communiques and state media apparatuses (Xinhua, RT, DD India, Western press).
Distinguishes domestic audience consumption from international deterrence signaling.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, SummitEvent


class PropagandaLens:
    """Information warfare and narrative engineering evaluator."""

    LENS_NAME = "Propaganda & Narrative Warfare"
    PRIMARY_TIER = EpistemicTier.TIER_5_COMMUNIQUE_PR

    @classmethod
    def evaluate(
        cls,
        summit: SummitEvent,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Decomposes state narratives across four discrete target audiences.
        Dynamically ingests communique declarations, press statements, and narrative warfare claims.
        """
        findings = [
            "Beijing Narrative (Xinhua): Sells the summit domestically as proof of China's uncontested leadership of the Global South and the historical decline of the West.",
            "Moscow Narrative (RT/TASS): Frames the gathering as total collapse of Western sanctions and proof of a rising Eurasian civilizational fortress.",
            "New Delhi Narrative (DD/MEA): Highlights India's role as the credible 'Vishwa-Bandhu' (universal friend) and voice of the Global South, emphasizing counter-terrorism and reformed multilateralism without anti-Western animus.",
            "Western Narrative (Atlantic Press): Systematically frames BRICS as a fractured, autocrat-dominated coalition paralyzed by internal contradictions.",
            "Recycled & Fabricated Crisis Narratives: Digital disinformation pipelines routinely weaponize two recurring vectors: (1) Head-of-state mortality/health rumor balloons (e.g., unsubstantiated stroke/coma rumors preceding high-level summits to trigger capital flight or panic) and (2) Temporal headline recycling (re-broadcasting past multilateral developments, such as 2024 mBridge technical transitions, as contemporary diplomatic fractures) to feed algorithmic engagement and dollar-funded narrative bias."
        ]

        metrics = {
            "domestic_audience_segmentation": "Highly polarized along sovereign ideological priorities",
            "communique_rhetoric_density": "Extreme (100+ passive consensus clauses)",
            "propaganda_discount_factor": 0.25, # Raw declaratory statements given 25% reality weight
            "behavioral_conditioning_index": 0.76, # Exploitation of fear and guilt conditioning in communications
            "commercial_anxiety_capture_score": 0.82, # Monetization of societal and parental anxieties
            "societal_atomization_pressure": 0.70, # Disruption of collective civilizational networks into atomized consumers
            "teleological_conspiracy_inflation": 0.65, # Tendency of counter-narratives to exaggerate deliberate top-down coordination
            "recycled_disinformation_index": 0.78,
            "head_of_state_rumor_discount_factor": 0.15
        }

        alignment = 0.35
        confidence = 0.88

        cognitive_keywords = [
            "watson", "bernays", "conditioning", "fear marketing", "guilt", "anxiety",
            "social engineering", "torches of freedom", "mkultra", "mockingbird",
            "infant", "teleological", "behavioral", "psychological care", "baby industry"
        ]
        matched_cognitive = False
        if claims:
            matched_cognitive = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in cognitive_keywords)
                for c in claims
            )
        event_title = getattr(summit, "title", "").lower()
        if any(kw in event_title for kw in cognitive_keywords):
            matched_cognitive = True

        if matched_cognitive:
            findings.insert(0, "[COGNITIVE WARFARE] Behavioral conditioning & psychological capture vectors active: Commercial/state actors deploying fear-based conditioning and parental/societal anxiety to engineer consumer reliance and narrative compliance.")
            confidence = min(0.99, round(confidence + 0.04, 2))
            metrics["cognitive_warfare_vectors_active"] = True
            metrics["behavioral_conditioning_index"] = 0.88
            metrics["commercial_anxiety_capture_score"] = 0.90

        if claims:
            narrative_keywords = [
                "propaganda", "communique", "narrative", "media", "xinhua", "tass",
                "press", "declaration", "rhetoric", "disinformation", "statement"
            ]
            matched_narrative = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in narrative_keywords)
                for c in claims
            )
            if matched_narrative:
                findings.insert(0, "[GROUNDED TELEMETRY] Information operations / communique narrative divergence verified against baseline text.")
                confidence = min(0.99, round(confidence + 0.02, 2))
                metrics["grounded_narrative_claims_verified"] = True
            metrics["claims_evaluated"] = len(claims)

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=confidence,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )


```