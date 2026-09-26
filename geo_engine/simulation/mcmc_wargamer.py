"""
Indefinite-Horizon Markov Chain Monte Carlo (MCMC) Geopolitical Wargamer.
Simulates multi-stage, multi-year stochastic geopolitical conflicts and attritional standoffs,
transcending finite 3-turn games to model dynamic transitions, absorbing states,
and systemic economic costs across 12-60 month strategic horizons.
"""

import math
import random
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from .game_theoretic import GameTheoreticEngine, StrategicActor


class ConflictState(str, Enum):
    """The 6 strategic conflict states in the Markov chain."""
    S0_DETERRENCE_EQUILIBRIUM = "S0_DETERRENCE_EQUILIBRIUM"       # Normal diplomatic parity / deterrence
    S1_GREY_ZONE_FRICTION = "S1_GREY_ZONE_FRICTION"               # Maritime/border grey-zone maneuvers below kinetic threshold
    S2_ECONOMIC_ATTRITION = "S2_ECONOMIC_ATTRITION"               # Sanctions, trade embargoes, supply chain decoupling
    S3_LOCALIZED_KINETIC = "S3_LOCALIZED_KINETIC"                 # Tactical border clash, precision retaliatory strikes
    S4_HIGH_INTENSITY_ESCALATION = "S4_HIGH_INTENSITY_ESCALATION" # Theatre-wide kinetic warfare
    S5_NEGOTIATED_SETTLEMENT = "S5_NEGOTIATED_SETTLEMENT"         # Formal ceasefire or de-escalation treaty


class MCMCScenarioConfig(BaseModel):
    """Configuration for an MCMC wargaming campaign."""
    initiator_name: str = "India"
    target_name: str = "China"
    initial_state: ConflictState = ConflictState.S1_GREY_ZONE_FRICTION
    horizon_months: int = Field(default=24, ge=1, le=120)
    num_simulations: int = Field(default=1000, ge=50, le=10000)
    initiator_wwr_days: float = Field(default=20.0, description="War Wastage Reserve ammunition days")
    target_wwr_days: float = Field(default=25.0, description="Opponent War Wastage Reserve days")
    initiator_fx_cover_months: float = Field(default=11.5, description="Foreign exchange import cover in months")
    target_fx_cover_months: float = Field(default=14.0, description="Opponent FX cover in months")
    domestic_friction_factor: float = Field(default=0.35, ge=0.0, le=1.0)
    random_seed: Optional[int] = 42


class MCMCStateTrajectory(BaseModel):
    """State probability distribution at a given monthly epoch."""
    month: int
    distribution: Dict[ConflictState, float]
    dominant_state: ConflictState


class MCMCSimulationResult(BaseModel):
    """Aggregated outcomes from multi-trajectory Monte Carlo simulation."""
    simulation_id: str
    initiator: str
    target: str
    horizon_months: int
    num_simulations: int
    trajectories: List[MCMCStateTrajectory]
    terminal_distribution: Dict[ConflictState, float]
    settlement_probability: float
    high_intensity_escalation_probability: float
    mean_months_to_settlement: Optional[float]
    expected_economic_loss_usd_b: Dict[str, float]
    resilience_verdict: str
    summary: str

    def to_markdown(self) -> str:
        lines = [
            f"# Indefinite-Horizon MCMC Wargaming Campaign: {self.simulation_id}",
            f"- **Actors:** `{self.initiator}` vs `{self.target}`",
            f"- **Horizon:** `{self.horizon_months} Months` | **Monte Carlo Iterations:** `{self.num_simulations}`",
            f"- **Probability of Negotiated Settlement:** `{self.settlement_probability * 100:.1f}%`",
            f"- **Probability of High-Intensity Escalation:** `{self.high_intensity_escalation_probability * 100:.1f}%`",
            f"- **Expected Months to Settlement:** `{f'{self.mean_months_to_settlement:.1f}' if self.mean_months_to_settlement else 'N/A'}`",
            "",
            "## Expected Economic & Attrition Cost (USD Billions)",
            f"- **{self.initiator} Estimated Loss:** `${self.expected_economic_loss_usd_b.get(self.initiator, 0.0):.2f}B`",
            f"- **{self.target} Estimated Loss:** `${self.expected_economic_loss_usd_b.get(self.target, 0.0):.2f}B`",
            "",
            "## Strategic Trajectory Milestones",
            "| Month | Dominant State | Deterrence (S0) | Grey-Zone (S1) | Economic (S2) | Localized (S3) | Escalated (S4) | Settlement (S5) |",
            "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
        ]

        sample_months = [0, max(1, self.horizon_months // 4), max(2, self.horizon_months // 2), max(3, (self.horizon_months * 3) // 4), self.horizon_months]
        sample_months = sorted(list(set(sample_months)))

        for m in sample_months:
            if m < len(self.trajectories):
                traj = self.trajectories[m]
                d = traj.distribution
                lines.append(
                    f"| M{traj.month:02d} | `{traj.dominant_state.name}` | "
                    f"{d.get(ConflictState.S0_DETERRENCE_EQUILIBRIUM, 0.0)*100:.1f}% | "
                    f"{d.get(ConflictState.S1_GREY_ZONE_FRICTION, 0.0)*100:.1f}% | "
                    f"{d.get(ConflictState.S2_ECONOMIC_ATTRITION, 0.0)*100:.1f}% | "
                    f"{d.get(ConflictState.S3_LOCALIZED_KINETIC, 0.0)*100:.1f}% | "
                    f"{d.get(ConflictState.S4_HIGH_INTENSITY_ESCALATION, 0.0)*100:.1f}% | "
                    f"{d.get(ConflictState.S5_NEGOTIATED_SETTLEMENT, 0.0)*100:.1f}% |"
                )

        lines.extend([
            "",
            f"**Strategic Assessment:** {self.summary}"
        ])
        return "\n".join(lines)


class MCMCGeopoliticalWargamer:
    """
    Monte Carlo Markov Chain (MCMC) simulator for multi-year geopolitical standoffs.
    Calculates dynamic state transition matrices modulated by material reserves (WWR ammunition,
    central bank FX covers, and domestic political tolerance).
    """

    STATE_ORDER: List[ConflictState] = [
        ConflictState.S0_DETERRENCE_EQUILIBRIUM,
        ConflictState.S1_GREY_ZONE_FRICTION,
        ConflictState.S2_ECONOMIC_ATTRITION,
        ConflictState.S3_LOCALIZED_KINETIC,
        ConflictState.S4_HIGH_INTENSITY_ESCALATION,
        ConflictState.S5_NEGOTIATED_SETTLEMENT,
    ]

    BASE_TRANSITION_MATRIX: Dict[ConflictState, Dict[ConflictState, float]] = {
        ConflictState.S0_DETERRENCE_EQUILIBRIUM: {
            ConflictState.S0_DETERRENCE_EQUILIBRIUM: 0.75,
            ConflictState.S1_GREY_ZONE_FRICTION: 0.15,
            ConflictState.S2_ECONOMIC_ATTRITION: 0.08,
            ConflictState.S3_LOCALIZED_KINETIC: 0.02,
            ConflictState.S4_HIGH_INTENSITY_ESCALATION: 0.00,
            ConflictState.S5_NEGOTIATED_SETTLEMENT: 0.00,
        },
        ConflictState.S1_GREY_ZONE_FRICTION: {
            ConflictState.S0_DETERRENCE_EQUILIBRIUM: 0.15,
            ConflictState.S1_GREY_ZONE_FRICTION: 0.50,
            ConflictState.S2_ECONOMIC_ATTRITION: 0.20,
            ConflictState.S3_LOCALIZED_KINETIC: 0.10,
            ConflictState.S4_HIGH_INTENSITY_ESCALATION: 0.02,
            ConflictState.S5_NEGOTIATED_SETTLEMENT: 0.03,
        },
        ConflictState.S2_ECONOMIC_ATTRITION: {
            ConflictState.S0_DETERRENCE_EQUILIBRIUM: 0.05,
            ConflictState.S1_GREY_ZONE_FRICTION: 0.15,
            ConflictState.S2_ECONOMIC_ATTRITION: 0.55,
            ConflictState.S3_LOCALIZED_KINETIC: 0.12,
            ConflictState.S4_HIGH_INTENSITY_ESCALATION: 0.03,
            ConflictState.S5_NEGOTIATED_SETTLEMENT: 0.10,
        },
        ConflictState.S3_LOCALIZED_KINETIC: {
            ConflictState.S0_DETERRENCE_EQUILIBRIUM: 0.02,
            ConflictState.S1_GREY_ZONE_FRICTION: 0.10,
            ConflictState.S2_ECONOMIC_ATTRITION: 0.20,
            ConflictState.S3_LOCALIZED_KINETIC: 0.40,
            ConflictState.S4_HIGH_INTENSITY_ESCALATION: 0.15,
            ConflictState.S5_NEGOTIATED_SETTLEMENT: 0.13,
        },
        ConflictState.S4_HIGH_INTENSITY_ESCALATION: {
            ConflictState.S0_DETERRENCE_EQUILIBRIUM: 0.01,
            ConflictState.S1_GREY_ZONE_FRICTION: 0.04,
            ConflictState.S2_ECONOMIC_ATTRITION: 0.10,
            ConflictState.S3_LOCALIZED_KINETIC: 0.25,
            ConflictState.S4_HIGH_INTENSITY_ESCALATION: 0.40,
            ConflictState.S5_NEGOTIATED_SETTLEMENT: 0.20,
        },
        ConflictState.S5_NEGOTIATED_SETTLEMENT: {
            ConflictState.S0_DETERRENCE_EQUILIBRIUM: 0.40,
            ConflictState.S1_GREY_ZONE_FRICTION: 0.10,
            ConflictState.S2_ECONOMIC_ATTRITION: 0.05,
            ConflictState.S3_LOCALIZED_KINETIC: 0.02,
            ConflictState.S4_HIGH_INTENSITY_ESCALATION: 0.00,
            ConflictState.S5_NEGOTIATED_SETTLEMENT: 0.43,
        }
    }

    # Monthly economic burn rates per state (in USD Billions)
    ECONOMIC_BURN_RATES: Dict[ConflictState, Tuple[float, float]] = {
        ConflictState.S0_DETERRENCE_EQUILIBRIUM: (0.1, 0.1),
        ConflictState.S1_GREY_ZONE_FRICTION: (0.5, 0.6),
        ConflictState.S2_ECONOMIC_ATTRITION: (3.5, 4.0),
        ConflictState.S3_LOCALIZED_KINETIC: (8.0, 9.5),
        ConflictState.S4_HIGH_INTENSITY_ESCALATION: (25.0, 30.0),
        ConflictState.S5_NEGOTIATED_SETTLEMENT: (0.2, 0.2),
    }

    @classmethod
    def calibrate_transition_matrix(
        cls,
        config: MCMCScenarioConfig
    ) -> Dict[ConflictState, Dict[ConflictState, float]]:
        """
        Dynamically modulates the base Markov transition probabilities
        based on material buffers: WWR ammunition days, FX cover, and political friction.
        """
        matrix: Dict[ConflictState, Dict[ConflictState, float]] = {}

        # If WWR ammunition is depleted (< 15 days), kinetic staying power collapses -> settlement or de-escalation probability rises
        min_wwr = min(config.initiator_wwr_days, config.target_wwr_days)
        ammo_exhaustion_factor = max(0.0, (20.0 - min_wwr) / 20.0) if min_wwr < 20.0 else 0.0

        # If FX cover is deep (> 10 months), economic warfare staying power is high
        min_fx = min(config.initiator_fx_cover_months, config.target_fx_cover_months)
        fx_stress_factor = max(0.0, (6.0 - min_fx) / 6.0) if min_fx < 6.0 else 0.0

        for current_state, row in cls.BASE_TRANSITION_MATRIX.items():
            new_row = dict(row)

            # Ammo exhaustion increases shift from kinetic states (S3/S4) to settlement (S5)
            if current_state in [ConflictState.S3_LOCALIZED_KINETIC, ConflictState.S4_HIGH_INTENSITY_ESCALATION]:
                if ammo_exhaustion_factor > 0:
                    shift = new_row[ConflictState.S4_HIGH_INTENSITY_ESCALATION] * (0.35 * ammo_exhaustion_factor)
                    new_row[ConflictState.S4_HIGH_INTENSITY_ESCALATION] -= shift
                    new_row[ConflictState.S5_NEGOTIATED_SETTLEMENT] += shift

            # High domestic friction increases pressure to settle from economic attrition (S2)
            if current_state == ConflictState.S2_ECONOMIC_ATTRITION:
                friction_shift = (config.domestic_friction_factor * 0.15) + (fx_stress_factor * 0.15)
                shift = new_row[ConflictState.S2_ECONOMIC_ATTRITION] * friction_shift
                new_row[ConflictState.S2_ECONOMIC_ATTRITION] -= shift
                new_row[ConflictState.S5_NEGOTIATED_SETTLEMENT] += shift

            # Normalize row to strictly sum to 1.0
            total_prob = sum(new_row.values())
            if total_prob > 0:
                matrix[current_state] = {k: v / total_prob for k, v in new_row.items()}
            else:
                matrix[current_state] = dict(row)

        return matrix

    @classmethod
    def simulate_campaign(
        cls,
        config: MCMCScenarioConfig
    ) -> MCMCSimulationResult:
        """
        Runs Monte Carlo Markov Chain simulation over specified horizon.
        Generates probability distributions, expected time-to-settlement, and attrition costs.
        """
        if config.random_seed is not None:
            rng = random.Random(config.random_seed)
        else:
            rng = random.Random()

        matrix = cls.calibrate_transition_matrix(config)
        states = cls.STATE_ORDER
        sim_id = f"MCMC-{config.initiator_name[:3].upper()}-{config.target_name[:3].upper()}-{config.horizon_months}M"

        # Trajectory tally: month -> {state: count}
        monthly_counts: List[Dict[ConflictState, int]] = [
            {s: 0 for s in states} for _ in range(config.horizon_months + 1)
        ]

        settlement_times: List[int] = []
        economic_losses_initiator = []
        economic_losses_target = []

        for _ in range(config.num_simulations):
            current_state = config.initial_state
            monthly_counts[0][current_state] += 1
            reached_settlement_at = None

            traj_loss_init = 0.0
            traj_loss_target = 0.0

            burn_init, burn_target = cls.ECONOMIC_BURN_RATES[current_state]
            traj_loss_init += burn_init
            traj_loss_target += burn_target

            for month in range(1, config.horizon_months + 1):
                probs = [matrix[current_state][s] for s in states]
                # Sample next state via cumulative distribution
                r = rng.random()
                cum = 0.0
                next_state = states[-1]
                for idx, p in enumerate(probs):
                    cum += p
                    if r <= cum:
                        next_state = states[idx]
                        break

                current_state = next_state
                monthly_counts[month][current_state] += 1

                # Track burn rate
                b_init, b_target = cls.ECONOMIC_BURN_RATES[current_state]
                traj_loss_init += b_init
                traj_loss_target += b_target

                if current_state == ConflictState.S5_NEGOTIATED_SETTLEMENT and reached_settlement_at is None:
                    reached_settlement_at = month

            if reached_settlement_at is not None:
                settlement_times.append(reached_settlement_at)

            economic_losses_initiator.append(traj_loss_init)
            economic_losses_target.append(traj_loss_target)

        # Convert counts into probabilities
        trajectories: List[MCMCStateTrajectory] = []
        for m in range(config.horizon_months + 1):
            dist = {
                s: round(monthly_counts[m][s] / float(config.num_simulations), 4)
                for s in states
            }
            dom_state = max(dist.items(), key=lambda x: x[1])[0]
            trajectories.append(MCMCStateTrajectory(
                month=m,
                distribution=dist,
                dominant_state=dom_state
            ))

        terminal_dist = trajectories[-1].distribution
        p_settlement = terminal_dist.get(ConflictState.S5_NEGOTIATED_SETTLEMENT, 0.0)
        p_escalation = terminal_dist.get(ConflictState.S4_HIGH_INTENSITY_ESCALATION, 0.0)

        mean_settle_month = round(sum(settlement_times) / len(settlement_times), 1) if settlement_times else None
        avg_loss_init = round(sum(economic_losses_initiator) / len(economic_losses_initiator), 2)
        avg_loss_target = round(sum(economic_losses_target) / len(economic_losses_target), 2)

        if p_settlement >= 0.50:
            verdict = "DIPLOMATIC_SETTLEMENT_DOMINANT"
        elif p_escalation >= 0.20:
            verdict = "HIGH_ESCALATION_RISK"
        elif terminal_dist.get(ConflictState.S2_ECONOMIC_ATTRITION, 0.0) >= 0.40:
            verdict = "PROTRACTED_ECONOMIC_STALEMATE"
        else:
            verdict = "PROTRACTED_GREY_ZONE_FRICTION"

        summary = (
            f"Over a {config.horizon_months}-month horizon, simulation indicates a {p_settlement * 100:.1f}% "
            f"probability of negotiated settlement and {p_escalation * 100:.1f}% risk of high-intensity escalation. "
            f"Cumulative projected attritional burn totals ${avg_loss_init:.1f}B for {config.initiator_name} and "
            f"${avg_loss_target:.1f}B for {config.target_name}."
        )

        return MCMCSimulationResult(
            simulation_id=sim_id,
            initiator=config.initiator_name,
            target=config.target_name,
            horizon_months=config.horizon_months,
            num_simulations=config.num_simulations,
            trajectories=trajectories,
            terminal_distribution=terminal_dist,
            settlement_probability=p_settlement,
            high_intensity_escalation_probability=p_escalation,
            mean_months_to_settlement=mean_settle_month,
            expected_economic_loss_usd_b={
                config.initiator_name: avg_loss_init,
                config.target_name: avg_loss_target
            },
            resilience_verdict=verdict,
            summary=summary
        )
