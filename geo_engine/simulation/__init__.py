"""
Simulation and Multi-Order Cascading Engine package.
Provides strategic shock propagation and systemic contagion modeling across the 20 analytical lenses.
"""

from .cascading_engine import (
    SimulationShock,
    CascadingImpact,
    CascadingSimulationResult,
    CascadingSimulationEngine,
)
from .game_theoretic import (
    StrategicActor,
    ActionMove,
    ReactionMove,
    SystemicBacklash,
    GameTheoreticSimulationResult,
    GameTheoreticEngine,
)

from .mcmc_wargamer import (
    ConflictState,
    MCMCScenarioConfig,
    MCMCStateTrajectory,
    MCMCSimulationResult,
    MCMCGeopoliticalWargamer,
)

__all__ = [
    "SimulationShock",
    "CascadingImpact",
    "CascadingSimulationResult",
    "CascadingSimulationEngine",
    "StrategicActor",
    "ActionMove",
    "ReactionMove",
    "SystemicBacklash",
    "GameTheoreticSimulationResult",
    "GameTheoreticEngine",
    "ConflictState",
    "MCMCScenarioConfig",
    "MCMCStateTrajectory",
    "MCMCSimulationResult",
    "MCMCGeopoliticalWargamer",
]
