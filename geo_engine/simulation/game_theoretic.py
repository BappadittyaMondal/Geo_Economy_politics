"""
Game-Theoretic Sequential Red-Teaming & Strategic Interaction Engine.
Simulates 3-turn dynamic strategic maneuvers:
Turn 1: Initiating Move (Action)
Turn 2: Counter-Move & Asymmetric Response (Reaction)
Turn 3: Domestic Friction & Alliance Realignment (Putnam Two-Level Game & Kautilyan Mitra Balance)
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ..core.models import get_system_reference_date


class StrategicActor(BaseModel):
    """Represents a sovereign or institutional actor in a strategic game."""
    name: str
    strategic_autonomy_score: float = Field(..., ge=0.0, le=1.0)
    risk_tolerance: float = Field(..., ge=0.0, le=1.0)
    primary_asymmetric_levers: List[str] = Field(default_factory=list)
    operational_code: str = "PRAGMATIC_REALISM"


class ActionMove(BaseModel):
    """Turn 1: The opening move by the initiating state."""
    turn: int = 1
    initiator: str
    target: str
    domain: str
    severity: float = Field(..., ge=0.0, le=1.0)
    action_description: str
    declared_intent: str = ""


class ReactionMove(BaseModel):
    """Turn 2: Counter-move executed by the target state."""
    turn: int = 2
    responder: str
    target: str
    counter_domain: str
    response_type: str = Field(..., description="ASYMMETRIC_LEVERAGE, SYMMETRIC_RECIPROCITY, DECONFLICTION_OFFRAMP, or DETERRENCE_POSTURING")
    severity: float = Field(..., ge=0.0, le=1.0)
    action_description: str
    strategic_rationality: str = ""


class SystemicBacklash(BaseModel):
    """Turn 3: Systemic equilibrium, domestic political backlash (Putnam), and alliance shifts."""
    turn: int = 3
    domestic_political_friction: float = Field(..., ge=0.0, le=1.0, description="Putnam Two-Level Game domestic political drag")
    inflationary_backlash_score: float = Field(..., ge=0.0, le=1.0)
    third_party_realignment: str = ""
    escalation_spiral_risk: float = Field(..., ge=0.0, le=1.0)
    de_escalation_off_ramp: str = ""


class GameTheoreticSimulationResult(BaseModel):
    """Complete 3-turn strategic interaction simulation outcome."""
    simulation_id: str
    initiator: StrategicActor
    target: StrategicActor
    turn_1_action: ActionMove
    turn_2_reaction: ReactionMove
    turn_3_backlash: SystemicBacklash
    equilibrium_stability_index: float = Field(..., ge=0.0, le=1.0)
    net_strategic_payoff: Dict[str, float] = Field(default_factory=dict)
    summary: str = ""
    timestamp: str = ""

    def to_markdown(self) -> str:
        lines = [
            f"# Game-Theoretic Strategic Red-Team: {self.simulation_id}",
            f"- **Initiator:** `{self.initiator.name}` (Autonomy: `{self.initiator.strategic_autonomy_score:.2f}`, Risk Tol: `{self.initiator.risk_tolerance:.2f}`)",
            f"- **Target:** `{self.target.name}` (Autonomy: `{self.target.strategic_autonomy_score:.2f}`, Risk Tol: `{self.target.risk_tolerance:.2f}`)",
            f"- **Equilibrium Stability Index:** `{self.equilibrium_stability_index:.2f}`",
            f"- **Simulation Timestamp:** `{self.timestamp}`",
            "",
            "## Turn 1: Opening Initiating Action",
            f"- **Domain:** `{self.turn_1_action.domain}` | **Severity:** `{self.turn_1_action.severity:.2f}`",
            f"- **Action:** {self.turn_1_action.action_description}",
            f"- **Declared Intent:** {self.turn_1_action.declared_intent}",
            "",
            "## Turn 2: Target Counter-Move (Asymmetric Reaction)",
            f"- **Counter Domain:** `{self.turn_2_reaction.counter_domain}` | **Response Type:** `{self.turn_2_reaction.response_type}`",
            f"- **Counter Severity:** `{self.turn_2_reaction.severity:.2f}`",
            f"- **Counter Action:** {self.turn_2_reaction.action_description}",
            f"- **Strategic Rationality:** {self.turn_2_reaction.strategic_rationality}",
            "",
            "## Turn 3: Systemic Equilibrium & Putnam Two-Level Backlash",
            f"- **Domestic Political Friction:** `{self.turn_3_backlash.domestic_political_friction:.2f}`",
            f"- **Inflationary / Economic Backlash:** `{self.turn_3_backlash.inflationary_backlash_score:.2f}`",
            f"- **Escalation Spiral Risk:** `{self.turn_3_backlash.escalation_spiral_risk:.2f}`",
            f"- **Third-Party Realignment:** {self.turn_3_backlash.third_party_realignment}",
            f"- **Optimal De-escalation Off-Ramp:** {self.turn_3_backlash.de_escalation_off_ramp}",
            "",
            "## Strategic Payoff Matrix",
            f"- **{self.initiator.name} Net Payoff:** `{self.net_strategic_payoff.get(self.initiator.name, 0.0):+.2f}`",
            f"- **{self.target.name} Net Payoff:** `{self.net_strategic_payoff.get(self.target.name, 0.0):+.2f}`",
            "",
            f"**Synthesis:** {self.summary}"
        ]
        return "\n".join(lines)


class GameTheoreticEngine:
    """
    Simulates sequential game-theoretic interactions between sovereign actors.
    Models counter-moves, Putnam Two-Level domestic friction, and Kautilyan Mitra balancing.
    """

    ACTOR_ROSTER: Dict[str, StrategicActor] = {
        "India": StrategicActor(
            name="India",
            strategic_autonomy_score=0.92,
            risk_tolerance=0.68,
            primary_asymmetric_levers=["geo_economist", "military_readiness", "institutional_lawfare", "food_security"],
            operational_code="DVAIDHIBHAVA_MULTI_ALIGNMENT"
        ),
        "China": StrategicActor(
            name="China",
            strategic_autonomy_score=0.88,
            risk_tolerance=0.74,
            primary_asymmetric_levers=["critical_minerals", "digital_sovereignty", "hybrid_covert", "cash_flow"],
            operational_code="TIANXIA_ASYMMETRIC_LEVERAGE"
        ),
        "United States": StrategicActor(
            name="United States",
            strategic_autonomy_score=0.95,
            risk_tolerance=0.70,
            primary_asymmetric_levers=["cash_flow", "institutional_lawfare", "digital_sovereignty", "military_readiness"],
            operational_code="LIBERAL_HEGEMONIC_CONTAINMENT"
        ),
        "Pakistan": StrategicActor(
            name="Pakistan",
            strategic_autonomy_score=0.42,
            risk_tolerance=0.82,
            primary_asymmetric_levers=["hybrid_covert", "propaganda", "military_readiness"],
            operational_code="BRINKMANSHIP_PROXY_WARFARE"
        ),
        "Russia": StrategicActor(
            name="Russia",
            strategic_autonomy_score=0.85,
            risk_tolerance=0.88,
            primary_asymmetric_levers=["petro_logistics", "critical_minerals", "military_readiness"],
            operational_code="EURASIAN_STRATEGIC_ATTRITION"
        )
    }

    @classmethod
    def simulate_interaction(
        cls,
        initiator_name: str,
        target_name: str,
        domain: str,
        severity: float,
        action_description: str,
        intent: str = ""
    ) -> GameTheoreticSimulationResult:
        """
        Executes a 3-turn sequential game-theoretic simulation.
        """
        ref_time = get_system_reference_date().strftime("%Y-%m-%d %H:%M:%S UTC")
        clamped_severity = max(0.0, min(1.0, float(severity)))

        initiator = cls.ACTOR_ROSTER.get(
            initiator_name,
            StrategicActor(name=initiator_name, strategic_autonomy_score=0.70, risk_tolerance=0.60)
        )
        target = cls.ACTOR_ROSTER.get(
            target_name,
            StrategicActor(name=target_name, strategic_autonomy_score=0.70, risk_tolerance=0.60)
        )

        sim_id = f"SIM-GT-{initiator.name[:3].upper()}-{target.name[:3].upper()}-{domain[:4].upper()}"

        # Turn 1: Action Move
        turn_1 = ActionMove(
            turn=1,
            initiator=initiator.name,
            target=target.name,
            domain=domain,
            severity=clamped_severity,
            action_description=action_description,
            declared_intent=intent or f"Exert coercive pressure on {target.name} via {domain} chokepoints."
        )

        # Turn 2: Counter-Move (Reaction)
        # Select best asymmetric counter lever based on target's strengths
        counter_domain = "geopolitical"
        response_type = "ASYMMETRIC_LEVERAGE"
        counter_action = f"{target.name} mobilizes diplomatic coalitions to neutralize {domain} disruption."
        rationality = "Minimize direct economic attrition while imposing multi-lateral isolation."

        if target.name == "India":
            if domain in ["critical_minerals", "digital_sovereignty"]:
                counter_domain = "geo_economist"
                response_type = "ASYMMETRIC_LEVERAGE"
                counter_action = "Accelerate bilateral non-dollar currency trade, expand Quad critical minerals pact, and tighten Press Note 3 foreign investment screening."
                rationality = "Neutralize supply choke by diversifying supply chains and restricting adversary market access."
            elif domain in ["hybrid_covert", "military_readiness"]:
                counter_domain = "institutional_lawfare"
                response_type = "DETERRENCE_POSTURING"
                counter_action = "Invoke 1991 Maritime/Border Accord compliance, surge P-8I maritime domain awareness patrols, and file formal international maritime safety protests."
                rationality = "Expose sub-kinetic threshold probing while establishing unambiguous kinetic redlines."
            elif domain in ["petro_logistics", "cash_flow"]:
                counter_domain = "cash_flow"
                response_type = "SYMMETRIC_RECIPROCITY"
                counter_action = "Release strategic crude reserves (SPR), deploy RBI forex swap lines, and enforce sovereign import currency hedges."
                rationality = "Insulate domestic inflation and absorb monetary volatility through robust reserves."
        elif target.name == "China":
            counter_domain = "critical_minerals"
            response_type = "ASYMMETRIC_LEVERAGE"
            counter_action = "Impose upstream export licensing and end-user verification on Gallium, Germanium, and NdFeB magnet processing."
            rationality = "Exploit near-total midstream refining monopoly to inflict high-tech supply chain pain."
        elif target.name == "United States":
            counter_domain = "institutional_lawfare"
            response_type = "ASYMMETRIC_LEVERAGE"
            counter_action = "Deploy OFAC Specially Designated Nationals (SDN) secondary sanctions and export entity-list inclusions."
            rationality = "Leverage dollar clearing centrality and extraterritorial regulatory jurisdiction."
        else:
            counter_domain = target.primary_asymmetric_levers[0] if target.primary_asymmetric_levers else "geopolitical"
            counter_action = f"{target.name} executes calibrated counter-maneuver in {counter_domain}."

        # Reaction severity is modulated by target's autonomy and risk tolerance
        reaction_severity = round(min(1.0, max(0.1, clamped_severity * (0.8 + 0.4 * target.risk_tolerance))), 4)

        turn_2 = ReactionMove(
            turn=2,
            responder=target.name,
            target=initiator.name,
            counter_domain=counter_domain,
            response_type=response_type,
            severity=reaction_severity,
            action_description=counter_action,
            strategic_rationality=rationality
        )

        # Turn 3: Putnam Two-Level Game Domestic Backlash & Systemic Equilibrium
        # Severe actions inflict domestic inflation / economic friction on initiator
        domestic_friction = round(min(1.0, clamped_severity * 0.65 + reaction_severity * 0.35 * (1.0 - initiator.strategic_autonomy_score)), 4)
        inflation_score = round(min(1.0, (clamped_severity + reaction_severity) * 0.45), 4)
        spiral_risk = round(min(1.0, (clamped_severity * reaction_severity) * 1.2), 4)

        if spiral_risk >= 0.60:
            realignment = f"Third-party neutral states accelerate defensive hedging; Quad and BRICS blocs harden regional containment."
            off_ramp = f"Mutual de-escalation via backchannel Track 1.5 diplomacy and technical working group buffer agreements."
        else:
            realignment = f"Regional powers absorb frictional shock through localized bilateral swap lines and rerouted shipping."
            off_ramp = f"Reversion to status quo ante via established bilateral consultation mechanisms."

        turn_3 = SystemicBacklash(
            turn=3,
            domestic_political_friction=domestic_friction,
            inflationary_backlash_score=inflation_score,
            third_party_realignment=realignment,
            escalation_spiral_risk=spiral_risk,
            de_escalation_off_ramp=off_ramp
        )

        # Calculate equilibrium stability index & net payoffs
        stability = round(max(0.0, min(1.0, 1.0 - (spiral_risk * 0.6 + domestic_friction * 0.4))), 4)

        init_payoff = round(clamped_severity * 0.5 - reaction_severity * 0.6 - domestic_friction * 0.4, 4)
        target_payoff = round(reaction_severity * 0.5 - clamped_severity * 0.6 - (1.0 - target.strategic_autonomy_score) * 0.3, 4)

        summary_text = (
            f"Simulation demonstrates that {initiator.name}'s initial move in '{domain}' triggers an asymmetric counter "
            f"in '{counter_domain}' by {target.name}. Systemic equilibrium stability is scored at {stability:.2f}. "
            f"Putnam Two-Level analysis indicates {initiator.name} faces {domestic_friction:.2f} domestic political friction, "
            f"with optimal off-ramp centering on: {off_ramp}"
        )

        return GameTheoreticSimulationResult(
            simulation_id=sim_id,
            initiator=initiator,
            target=target,
            turn_1_action=turn_1,
            turn_2_reaction=turn_2,
            turn_3_backlash=turn_3,
            equilibrium_stability_index=stability,
            net_strategic_payoff={initiator.name: init_payoff, target.name: target_payoff},
            summary=summary_text,
            timestamp=ref_time
        )
