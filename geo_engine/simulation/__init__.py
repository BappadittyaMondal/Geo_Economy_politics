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

__all__ = [
    "SimulationShock",
    "CascadingImpact",
    "CascadingSimulationResult",
    "CascadingSimulationEngine",
]
