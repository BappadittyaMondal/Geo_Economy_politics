"""
The 20-Lens Analytical Matrix.
Provides specialized evaluators for deep-tech, history, civilizational statecraft,
geo-economics, geopolitics, kinesics, cash flow, propaganda, petro-logistics,
bureaucratic inertia, digital sovereignty, hybrid/covert warfare, India timeline,
demographic infiltration, critical minerals, institutional lawfare, food security,
military readiness, subsea cables, and astro-politics space defense.
"""

from typing import List, Type, Any

from .deep_tech import DeepTechLens
from .history import HistoryLens
from .civilizational import CivilizationalLens
from .geo_economist import GeoEconomistLens
from .geopolitical import GeopoliticalLens
from .kinesics import KinesicsLens
from .cash_flow import CashFlowLens
from .propaganda import PropagandaLens
from .petro_logistics import PetroLogisticsLens
from .bureaucratic_inertia import BureaucraticInertiaLens
from .digital_sovereignty import DigitalSovereigntyLens
from .hybrid_covert import HybridCovertLens
from .india_timeline import IndiaTimelineLens
from .demographic_infiltration import DemographicInfiltrationLens
from .critical_minerals import CriticalMineralsLens
from .institutional_lawfare import InstitutionalLawfareLens
from .food_security import FoodSecurityLens
from .military_readiness import MilitaryReadinessLens
from .subsea_cables import SubseaCablesLens
from .astro_politics import AstroPoliticsLens

LENS_REGISTRY: List[Type[Any]] = [
    DeepTechLens,
    HistoryLens,
    CivilizationalLens,
    GeoEconomistLens,
    GeopoliticalLens,
    KinesicsLens,
    CashFlowLens,
    PropagandaLens,
    PetroLogisticsLens,
    BureaucraticInertiaLens,
    DigitalSovereigntyLens,
    HybridCovertLens,
    IndiaTimelineLens,
    DemographicInfiltrationLens,
    CriticalMineralsLens,
    InstitutionalLawfareLens,
    FoodSecurityLens,
    MilitaryReadinessLens,
    SubseaCablesLens,
    AstroPoliticsLens,
]

__all__ = [
    "LENS_REGISTRY",
    "DeepTechLens",
    "HistoryLens",
    "CivilizationalLens",
    "GeoEconomistLens",
    "GeopoliticalLens",
    "KinesicsLens",
    "CashFlowLens",
    "PropagandaLens",
    "PetroLogisticsLens",
    "BureaucraticInertiaLens",
    "DigitalSovereigntyLens",
    "HybridCovertLens",
    "IndiaTimelineLens",
    "DemographicInfiltrationLens",
    "CriticalMineralsLens",
    "InstitutionalLawfareLens",
    "FoodSecurityLens",
    "MilitaryReadinessLens",
    "SubseaCablesLens",
    "AstroPoliticsLens",
]


