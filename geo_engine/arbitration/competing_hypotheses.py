"""
Analysis of Competing Hypotheses (ACH) & Epistemic Causality Engine.
Implements intelligence doctrine (Richards Heuer methodology) to evaluate
competing causal hypotheses for anomalous kinetic, maritime, and border incidents
before leaping to strategic or civilizational 'inner meaning' conclusions.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CausalHypothesisType(str, Enum):
    """The four fundamental causal hypotheses for anomalous security/maritime incidents."""
    TECHNICAL_FAILURE = "TECHNICAL_FAILURE"       # Mechanical, steering, electrical, or hydrodynamic failure
    CREW_INCOMPETENCE = "CREW_INCOMPETENCE"       # Rookie watchstander error, bridge navigation miscalculation
    TACTICAL_MASKIROVKA = "TACTICAL_MASKIROVKA"   # Deliberate surface distraction masking covert subsea/flank action
    DELIBERATE_COERCION = "DELIBERATE_COERCION"   # State-directed sub-kinetic grey-zone threshold probing


class HypothesisCandidate(BaseModel):
    """An individual competing hypothesis with Bayesian prior, likelihood, and posterior probabilities."""
    hypothesis_id: str
    hypothesis_type: CausalHypothesisType
    label: str
    description: str
    prior_probability: float = Field(default=0.25, ge=0.0, le=1.0)
    likelihood_score: float = Field(default=0.50, ge=0.0, le=1.0)
    posterior_probability: float = Field(default=0.25, ge=0.0, le=1.0)
    evidence_supporting: List[str] = Field(default_factory=list)
    evidence_contradicting: List[str] = Field(default_factory=list)
    falsification_indicators: List[str] = Field(default_factory=list)


class ACHEvaluationReport(BaseModel):
    """Synthesized Analysis of Competing Hypotheses report."""
    incident_title: str
    hypotheses: List[HypothesisCandidate] = Field(default_factory=list)
    dominant_hypothesis_id: str = ""
    dominant_hypothesis_label: str = ""
    dominant_probability: float = 0.0
    is_epistemically_contested: bool = False
    epistemic_warning: Optional[str] = None
    reasoning_audit_trail: List[str] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes report into JSON-compatible dictionary."""
        return {
            "incident_title": self.incident_title,
            "dominant_hypothesis_id": self.dominant_hypothesis_id,
            "dominant_hypothesis_label": self.dominant_hypothesis_label,
            "dominant_probability": round(self.dominant_probability, 3),
            "is_epistemically_contested": self.is_epistemically_contested,
            "epistemic_warning": self.epistemic_warning,
            "hypotheses": [
                {
                    "id": h.hypothesis_id,
                    "type": h.hypothesis_type.value,
                    "label": h.label,
                    "prior": round(h.prior_probability, 3),
                    "likelihood": round(h.likelihood_score, 3),
                    "posterior": round(h.posterior_probability, 3),
                    "supporting_count": len(h.evidence_supporting),
                    "contradicting_count": len(h.evidence_contradicting)
                }
                for h in self.hypotheses
            ],
            "reasoning_audit_trail": self.reasoning_audit_trail
        }


class IncidentReasoningEngine:
    """
    Executes deep multi-hypothesis causal arbitration for security, maritime, and border incidents.
    Guarantees that mechanical failure and crew incompetence (Occam's and Hanlon's razors)
    are formally tested and arbitrated against strategic deception and state-sponsored coercion.
    """

    @classmethod
    def evaluate_incident(
        cls,
        incident_title: str,
        claims: Optional[List[Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> ACHEvaluationReport:
        """
        Evaluates an incident across the four competing hypotheses using Bayesian inference.
        """
        audit_trail: List[str] = []
        audit_trail.append(f"[ACH_INIT] Initializing Analysis of Competing Hypotheses for incident: '{incident_title}'.")

        # 1. Instantiate the 4 baseline competing hypotheses
        h_tech = HypothesisCandidate(
            hypothesis_id="HYP_1_TECHNICAL_FAILURE",
            hypothesis_type=CausalHypothesisType.TECHNICAL_FAILURE,
            label="Technical / Mechanical Steering Failure (Occam's Razor)",
            description="Loss of rudder control, steering servo blackout, propulsion governor surge, or hydrodynamic Bernoulli hull suction.",
            prior_probability=0.25,
            likelihood_score=0.40,
            falsification_indicators=[
                "Broadcast of 5 short blasts (COLREGs Rule 34 danger/doubt signal)",
                "VHF Ch 16 'Not Under Command' (NUC) navigational warning broadcast",
                "Subsequent shipyard casualty log corroborating hydraulic/servo failure"
            ]
        )

        h_crew = HypothesisCandidate(
            hypothesis_id="HYP_2_CREW_INCOMPETENCE",
            hypothesis_type=CausalHypothesisType.CREW_INCOMPETENCE,
            label="Navigational Inexperience / Watchstander Error (Hanlon's Razor)",
            description="Rookie Bridge team on newly-commissioned vessel miscalculating closing vectors, speed over ground, or hydrodynamic interaction.",
            prior_probability=0.25,
            likelihood_score=0.45,
            falsification_indicators=[
                "Vessel commissioned within past 12 months with green watchstanders",
                "Sudden erratic rudder change immediately preceding contact",
                "Severe disproportionate hull damage sustained by own OPV hull compared to adversary warship"
            ]
        )

        h_mask = HypothesisCandidate(
            hypothesis_id="HYP_3_TACTICAL_MASKIROVKA",
            hypothesis_type=CausalHypothesisType.TACTICAL_MASKIROVKA,
            label="Tactical Maskirovka / Clandestine Distraction Cover",
            description="High-visibility surface provocation staged to fix maritime patrol radar and sensor coverage away from an undersea or flank covert asset.",
            prior_probability=0.25,
            likelihood_score=0.35,
            falsification_indicators=[
                "Unusual sonar/acoustic contacts detected in adjacent maritime sectors",
                "Prolonged visual engagement without offensive weapons engagement",
                "Simultaneous covert transit or seabed infrastructure interference"
            ]
        )

        h_coercion = HypothesisCandidate(
            hypothesis_id="HYP_4_DELIBERATE_COERCION",
            hypothesis_type=CausalHypothesisType.DELIBERATE_COERCION,
            label="Deliberate State-Directed Grey-Zone Coercion",
            description="Premeditated sub-kinetic bow crossing or shouldering ordered to probe adversary Rules of Engagement (ROE) below Article 51 threshold.",
            prior_probability=0.25,
            likelihood_score=0.55,
            falsification_indicators=[
                "Aggressive high-speed closing course maintained despite repeated bridge-to-bridge warnings",
                "Pattern of identical South China Sea shouldering tactics deployed by strategic partners",
                "State media deployment of pre-planned nationalist victory narrative"
            ]
        )

        # 2. Extract telemetry text from claims and title
        combined_text = incident_title.lower()
        if claims:
            for c in claims:
                fact = getattr(c, "asserted_fact", getattr(c, "assertion", ""))
                combined_text += " " + str(fact).lower()

        if context:
            for k, v in context.items():
                combined_text += f" {k} {v}".lower()

        # 3. Dynamic Likelihood Calibration based on empirical telemetry
        # A. Technical Failure Evidence
        tech_keywords = ["steering", "rudder", "blackout", "engine", "gyro", "mechanical", "failure", "breakdown", "hydrodynamic", "suction", "bernoulli", "not under command"]
        if any(kw in combined_text for kw in tech_keywords):
            h_tech.likelihood_score = min(0.95, h_tech.likelihood_score + 0.35)
            h_tech.evidence_supporting.append("Telemetry references mechanical, steering, electrical, or hydrodynamic anomaly.")
            audit_trail.append(f"[ACH_EVIDENCE] Technical/mechanical keywords elevated Technical Failure likelihood to {h_tech.likelihood_score:.2f}.")

        # B. Crew Inexperience Evidence (e.g. PNS Hunain commissioned July 2024)
        crew_keywords = ["inexperience", "rookie", "commissioned", "recently commissioned", "new vessel", "watchstander", "poor seamanship", "navigation error", "misjudged", "colregs error", "young crew", "july 2024", "hunain"]
        if any(kw in combined_text for kw in crew_keywords):
            h_crew.likelihood_score = min(0.95, h_crew.likelihood_score + 0.30)
            h_crew.evidence_supporting.append("Vessel commissioning chronology (July 2024) and tactical profile indicate green watchstander crew.")
            audit_trail.append(f"[ACH_EVIDENCE] Vessel age and seamanship profile elevated Crew Incompetence likelihood to {h_crew.likelihood_score:.2f}.")

        # C. Tactical Maskirovka Evidence
        mask_keywords = ["distraction", "diversion", "maskirovka", "submarine", "subsea", "covert", "hide", "decoy", "acoustic", "shadowing other", "unwanted thing"]
        if any(kw in combined_text for kw in mask_keywords):
            h_mask.likelihood_score = min(0.95, h_mask.likelihood_score + 0.40)
            h_mask.evidence_supporting.append("Telemetry indicates surface confrontation coincided with multi-domain distraction cues.")
            audit_trail.append(f"[ACH_EVIDENCE] Deception/distraction cues elevated Tactical Maskirovka likelihood to {h_mask.likelihood_score:.2f}.")

        # D. Deliberate Coercion Evidence
        coercion_keywords = ["deliberate", "ramming", "shouldering", "provocation", "grey zone", "orders", "pakistan navy", "roe", "protest", "demarche", "1991 agreement", "sindoor"]
        if any(kw in combined_text for kw in coercion_keywords):
            h_coercion.likelihood_score = min(0.95, h_coercion.likelihood_score + 0.25)
            h_coercion.evidence_supporting.append("Tactical maneuvering profile and diplomatic demarche align with premeditated sub-kinetic probing.")
            audit_trail.append(f"[ACH_EVIDENCE] Grey-zone provocation indicators elevated Deliberate Coercion likelihood to {h_coercion.likelihood_score:.2f}.")

        # 4. Bayesian Posterior Normalization: P(H_i | E) = (P(E | H_i) * P(H_i)) / sum(P(E | H_j) * P(H_j))
        hypotheses = [h_tech, h_crew, h_mask, h_coercion]
        numerators = [h.prior_probability * h.likelihood_score for h in hypotheses]
        denominator = sum(numerators)

        if denominator > 0:
            for h, num in zip(hypotheses, numerators):
                h.posterior_probability = round(num / denominator, 4)
        else:
            for h in hypotheses:
                h.posterior_probability = 0.25

        # 5. Determine Dominant Hypothesis and Epistemic Contestability
        sorted_hypotheses = sorted(hypotheses, key=lambda x: x.posterior_probability, reverse=True)
        dominant = sorted_hypotheses[0]
        runner_up = sorted_hypotheses[1]

        diff = dominant.posterior_probability - runner_up.posterior_probability
        is_contested = (diff < 0.15)

        warning: Optional[str] = None
        if dominant.hypothesis_type in [CausalHypothesisType.TECHNICAL_FAILURE, CausalHypothesisType.CREW_INCOMPETENCE]:
            warning = (
                f"[ACH EPISTEMIC TRUTH GUARD] Non-hostile causal hypothesis ('{dominant.label}') "
                f"dominates with probability {dominant.posterior_probability:.1%}. "
                f"Strategic analysts must strictly avoid over-attributing deliberate geopolitical malice "
                f"to what empirical evidence indicates is an engineering casualty or bridge watchstander error."
            )
            audit_trail.append(f"[ACH_WARNING] Truth Guard triggered: Non-conspiratorial hypothesis dominant ({dominant.hypothesis_id}).")
        elif is_contested:
            warning = (
                f"[ACH EPISTEMIC CAUTION] Result is epistemically contested: Top hypothesis ('{dominant.label}', {dominant.posterior_probability:.1%}) "
                f"leads runner-up ('{runner_up.label}', {runner_up.posterior_probability:.1%}) by only {diff:.1%}. "
                f"Alternative non-malicious hypotheses cannot be ruled out."
            )
            audit_trail.append(f"[ACH_CONTESTED] Contested margin ({diff:.3f} < 0.150). Caution flag raised.")
        else:
            audit_trail.append(f"[ACH_RESOLVED] Dominant hypothesis confirmed: {dominant.hypothesis_id} ({dominant.posterior_probability:.1%}).")

        return ACHEvaluationReport(
            incident_title=incident_title,
            hypotheses=hypotheses,
            dominant_hypothesis_id=dominant.hypothesis_id,
            dominant_hypothesis_label=dominant.label,
            dominant_probability=dominant.posterior_probability,
            is_epistemically_contested=is_contested,
            epistemic_warning=warning,
            reasoning_audit_trail=audit_trail
        )
