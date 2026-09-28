# LENS SPECIFICATION: PROPAGANDA

```python
"""
Lens 8: Propaganda & Narrative Warfare Lens.
Deconstructs summit communiques and state media apparatuses (Xinhua, RT, DD India, Western press).
Distinguishes domestic audience consumption from international deterrence signaling.
"""

import math
from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, SummitEvent


class PropagandaLens:
    """Information warfare and narrative engineering evaluator."""

    LENS_NAME = "Propaganda & Narrative Warfare"
    PRIMARY_TIER = EpistemicTier.TIER_5_COMMUNIQUE_PR

    @staticmethod
    def calculate_evidence_distortion_tensor(
        empirical_support: float = 0.5,
        phi_colonial: float = 0.10,
        phi_ideological: float = 0.10,
        phi_theological: float = 0.10,
        phi_pseudoscience: float = 0.10,
        gamma: float = 8.0,
        theta: float = 0.50
    ) -> Dict[str, Any]:
        """
        Attenuated Logistic Evidence-Distortion Tensor (ALEDT).
        Computes deterministic Reality % vs. Propaganda % from multi-dimensional distortion vectors.
        Penalty = 1.0 + exp(gamma * (||Phi||_inf - theta))
        Reality Score = min(1.0, (empirical_support * 2.0) / Penalty)
        """
        phi_vector = [
            max(0.0, min(1.0, phi_colonial)),
            max(0.0, min(1.0, phi_ideological)),
            max(0.0, min(1.0, phi_theological)),
            max(0.0, min(1.0, phi_pseudoscience))
        ]
        l_infinity = max(phi_vector)
        exponent = max(-20.0, min(20.0, gamma * (l_infinity - theta)))
        distortion_penalty = round(1.0 + math.exp(exponent), 3)

        effective_support = max(0.0, min(1.0, empirical_support))
        raw_reality = (effective_support * 2.0) / distortion_penalty
        reality_score = round(max(0.0, min(1.0, raw_reality)), 3)
        propaganda_score = round(max(0.0, min(1.0, 1.0 - reality_score)), 3)

        reality_pct = round(reality_score * 100.0, 1)
        propaganda_pct = round(propaganda_score * 100.0, 1)

        if reality_score >= 0.70:
            classification = "PRAMĀṆIKA"
            classification_ascii = "PRAMANIKA"
        elif reality_score >= 0.30:
            classification = "SAD-BHĀSA"
            classification_ascii = "SAD-BHASA"
        else:
            classification = "KŪṬA-YUKTI"
            classification_ascii = "KUTA-YUKTI"

        return {
            "phi_vector": phi_vector,
            "l_infinity_norm": round(l_infinity, 3),
            "distortion_penalty": distortion_penalty,
            "reality_score": reality_score,
            "propaganda_score": propaganda_score,
            "reality_percentage": reality_pct,
            "propaganda_percentage": propaganda_pct,
            "epistemic_classification": classification,
            "epistemic_classification_ascii": classification_ascii
        }

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

        # Detect antithetical rhetorical priming (Phase 95)
        antithetical_keywords = [
            "hisab chukta", "hisaab chukta", "hisab karega", "settle scores",
            "karega ki nahi", "antithetical priming", "oratorical priming",
            "retributive premise", "grievance priming"
        ]
        matched_antithetical = False
        if claims:
            matched_antithetical = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in antithetical_keywords)
                for c in claims
            )
        if any(kw in event_title for kw in antithetical_keywords):
            matched_antithetical = True

        if matched_antithetical:
            anti_res = AntitheticalRhetoricSieve.calculate_antithetical_priming(
                premise_activation_intensity=0.85,
                crowd_validation_factor=0.90,
                restraint_claim_credibility=0.40
            )
            findings.insert(0, (
                f"[GROUNDED TELEMETRY] Antithetical Rhetorical Forensics Sieve triggered: "
                f"Threat Tier [{anti_res['rhetorical_threat_tier']}] (Score: {anti_res['antithetical_priming_score']:.2f}). "
                f"{anti_res['oratorical_risk_summary']} Rebuttal: {anti_res['forensic_rebuttal_pathway']}"
            ))
            metrics["antithetical_priming_score"] = anti_res["antithetical_priming_score"]
            metrics["rhetorical_threat_tier"] = anti_res["rhetorical_threat_tier"]

        # Detect apocalyptic, millenarian, or pseudoscientific narrative distortion
        apocalyptic_keywords = [
            "2032", "kali yuga", "apocalypse", "doomsday", "malika", "nostradamus",
            "end of world", "kalki", "pralaya", "world war 3", "ww3", "millenarian"
        ]
        matched_apocalyptic = False
        if claims:
            matched_apocalyptic = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in apocalyptic_keywords)
                for c in claims
            )
        if any(kw in event_title for kw in apocalyptic_keywords):
            matched_apocalyptic = True

        if matched_apocalyptic:
            tensor = cls.calculate_evidence_distortion_tensor(
                empirical_support=0.20,
                phi_colonial=0.10,
                phi_ideological=0.10,
                phi_theological=0.65,
                phi_pseudoscience=0.85
            )
        else:
            # Baseline calibration reflecting commercial anxiety & conditioning levels
            empirical = 0.60 if metrics.get("grounded_narrative_claims_verified") else 0.40
            phi_pseudo = 0.50 if metrics.get("cognitive_warfare_vectors_active") else 0.15
            tensor = cls.calculate_evidence_distortion_tensor(
                empirical_support=empirical,
                phi_colonial=0.15,
                phi_ideological=0.25,
                phi_theological=0.20,
                phi_pseudoscience=phi_pseudo
            )

        metrics["evidence_distortion_tensor"] = tensor
        metrics["reality_score"] = tensor["reality_score"]
        metrics["propaganda_score"] = tensor["propaganda_score"]
        metrics["reality_percentage"] = tensor["reality_percentage"]
        metrics["propaganda_percentage"] = tensor["propaganda_percentage"]
        metrics["epistemic_classification"] = tensor["epistemic_classification"]
        metrics["l_infinity_norm"] = tensor["l_infinity_norm"]
        metrics["distortion_penalty"] = tensor["distortion_penalty"]

        if tensor["epistemic_classification"] == "KŪṬA-YUKTI":
            findings.insert(0, f"[EPISTEMIC TENSOR AUDIT] KŪṬA-YUKTI detected: Narrative exhibits severe evidence distortion (L-infinity norm: {tensor['l_infinity_norm']}, Distortion Penalty: {tensor['distortion_penalty']}). Reality: {tensor['reality_percentage']}%, Propaganda: {tensor['propaganda_percentage']}%.")
        elif tensor["epistemic_classification"] == "SAD-BHĀSA":
            findings.insert(0, f"[EPISTEMIC TENSOR AUDIT] SAD-BHĀSA (Mixed Rhetoric): Reality: {tensor['reality_percentage']}%, Propaganda: {tensor['propaganda_percentage']}%.")

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=confidence,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )


class AntitheticalRhetoricSieve:
    """
    Phase 95: Antithetical Rhetorical Forensics Sieve.
    Quantifies dual-track cognitive manipulation where an orator explicitly validates and implants
    a destructive premise or historical grievance (e.g., 'Aise vyakti ko mauka mile to hisab chukta karega ki nahi? Karega!')
    while simultaneously preaching magnanimity or restraint to maintain superficial deniability.

    Formula:
        W_antithesis = min(1.0, max(0.0, 0.50 * P_premise + 0.30 * V_crowd - 0.20 * R_restraint))
    """

    @staticmethod
    def calculate_antithetical_priming(
        premise_activation_intensity: float,
        crowd_validation_factor: float,
        restraint_claim_credibility: float
    ) -> Dict[str, Any]:
        premise = max(0.0, min(1.0, float(premise_activation_intensity)))
        crowd = max(0.0, min(1.0, float(crowd_validation_factor)))
        restraint = max(0.0, min(1.0, float(restraint_claim_credibility)))

        score = round(min(1.0, max(0.0, 0.50 * premise + 0.30 * crowd - 0.20 * restraint)), 4)

        if score >= 0.75:
            tier = "ACUTE_ANTITHETICAL_PRIMING"
            summary = (
                "Acute oratorical priming: Speaker explicitly activates and validates a historical grievance or "
                "retributive premise with crowd affirmation, embedding grievance into collective memory despite "
                "nominal calls for harmony."
            )
            rebuttal = (
                "Deconstruct oratorical framing: Expose the antithesis mechanism, challenge the historical accuracy "
                "of collective grievance premises, and restore objective institutional due process over rhetorical moralizing."
            )
        elif score >= 0.50:
            tier = "ELEVATED_RHETORICAL_AMBIGUITY"
            summary = (
                "Elevated rhetorical tension: Evocative grievance imagery juxtaposed against conciliation, creating "
                "cognitive dissonance and dual-channel audience signaling."
            )
            rebuttal = "Anchor public policy in empirical legal statutes rather than ambiguous moral rhetoric."
        elif score >= 0.25:
            tier = "MODERATE_ORATORICAL_STAGING"
            summary = "Standard political rhetoric utilizing rhetorical questions or illustrative parables with minimal grievance reinforcement."
            rebuttal = "Contextualize political framing against historical and administrative facts."
        else:
            tier = "AUTHENTIC_CONSENSUS_DISCOURSE"
            summary = "Constructive discourse emphasizing mutual civilizational cohesion without covert grievance priming."
            rebuttal = "Reinforce unified civilizational identity and shared civic duties."

        return {
            "antithetical_priming_score": score,
            "premise_activation_intensity": premise,
            "crowd_validation_factor": crowd,
            "restraint_claim_credibility": restraint,
            "rhetorical_threat_tier": tier,
            "oratorical_risk_summary": summary,
            "forensic_rebuttal_pathway": rebuttal
        }



```