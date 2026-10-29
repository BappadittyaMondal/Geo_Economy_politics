"""
The 20-Lens Analytical Matrix.
Provides specialized evaluators for deep-tech, history, civilizational statecraft,
geo-economics, geopolitics, kinesics, cash flow, propaganda, petro-logistics,
bureaucratic inertia, digital sovereignty, hybrid/covert warfare, India timeline,
demographic infiltration, critical minerals, institutional lawfare, food security,
military readiness, subsea cables, and astro-politics space defense.
"""

from typing import List, Type, Any

from .deep_tech import DeepTechLens, STEMCapitalDilutionSieve, QuantumInformationSieve
from .history import HistoryLens
from .civilizational import (
    CivilizationalLens,
    CulturalGrayzoneSieve,
    SacredCalendarProvocationSieve,
    UrbanInsurrectionRiskSieve,
    CivilizationalKshatraSieve,
    CulturalGrayzoneLegitimacySieve,
)
from .geo_economist import GeoEconomistLens, MultilateralCurrencySettlementSieve, NationalChampionSovereignSieve, SupplyChainVacuumCaptureSieve, OffshoreCapitalMagnetismSieve, ResourceCurseSieve
from .geopolitical import GeopoliticalLens, ChokepointKineticSieve, TripartiteCoherenceSieve
from .kinesics import KinesicsLens, SartorialSemioticSieve
from .cash_flow import CashFlowLens
from .propaganda import PropagandaLens, AntitheticalRhetoricSieve, CognitivePanicMonetizationFilter, CognitiveSovereigntySieve
from .petro_logistics import PetroLogisticsLens
from .bureaucratic_inertia import BureaucraticInertiaLens, BureaucraticRollbackModel
from .digital_sovereignty import (
    DigitalSovereigntyLens,
    TechSovereigntySieve,
    ImperialSubversionPipesSieve,
    ProtocolLayerSovereigntySieve,
    CorporateAstroturfingSieve,
    IndigenousHardwareTechMoatSieve,
    StrategicMetallurgySieve,
)
from .hybrid_covert import HybridCovertLens, ExtraterritorialSovereignAsymmetrySieve, DiplomaticCounterIntelSieve, NuclearAmbiguitySieve
from .india_timeline import IndiaTimelineLens
from .demographic_infiltration import DemographicInfiltrationLens, DiasporaBacklashSieve, StatutoryBorderDemographySieve
from .critical_minerals import CriticalMineralsLens, CriticalMineralsRefiningCrisisSieve
from .institutional_lawfare import (
    InstitutionalLawfareLens,
    SubNationalEndowmentSieve,
    IntraCivilizationalFaultlineSieve,
    CulturalReligiousGrayzoneSieve,
    JudicialSubversionSieve,
    CoercionPremiumSieve,
    CrowdCascadeThresholdSieve,
    StateMachiavellianSieve,
    SovereignPowerHierarchySieve,
    DataSovereigntyMediaLawfareSieve,
    StreetLawfareSieve,
)

from .food_security import FoodSecurityLens, EnergyFertilizerChokepointSieve, AgrarianWaterCartelSieve, RiparianResilienceSieve
from .military_readiness import MilitaryReadinessLens, AvionicsSovereigntySieve, AsymmetricInterceptionSieve, MaritimeForwardBasingSieve, HighAltitudeAeroDefenseSieve
from .subsea_cables import SubseaCablesLens, SubseaCableSovereigntySieve
from .astro_politics import AstroPoliticsLens, AstroSovereigntySieve

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
    "ChokepointKineticSieve",
    "AvionicsSovereigntySieve",
    "SubNationalEndowmentSieve",
    "BureaucraticRollbackModel",
    "SartorialSemioticSieve",
    "IntraCivilizationalFaultlineSieve",
    "ExtraterritorialSovereignAsymmetrySieve",
    "AntitheticalRhetoricSieve",
    "AsymmetricInterceptionSieve",
    "DiasporaBacklashSieve",
    "DiplomaticCounterIntelSieve",
    "STEMCapitalDilutionSieve",
    "QuantumInformationSieve",
    "EnergyFertilizerChokepointSieve",
    "AgrarianWaterCartelSieve",
    "CulturalReligiousGrayzoneSieve",
    "CulturalGrayzoneSieve",
    "SacredCalendarProvocationSieve",
    "JudicialSubversionSieve",
    "TechSovereigntySieve",
    "UrbanInsurrectionRiskSieve",
    "ImperialSubversionPipesSieve",
    "ProtocolLayerSovereigntySieve",
    "CoercionPremiumSieve",
    "CrowdCascadeThresholdSieve",
    "StateMachiavellianSieve",
    "CorporateAstroturfingSieve",
    "MaritimeForwardBasingSieve",
    "CivilizationalKshatraSieve",
    "SovereignPowerHierarchySieve",
    "MultilateralCurrencySettlementSieve",
    "SubseaCableSovereigntySieve",
    "CriticalMineralsRefiningCrisisSieve",
    "NationalChampionSovereignSieve",
    "CulturalGrayzoneLegitimacySieve",
    "SupplyChainVacuumCaptureSieve",
    "DataSovereigntyMediaLawfareSieve",
    "CognitivePanicMonetizationFilter",
    "IndigenousHardwareTechMoatSieve",
    "StreetLawfareSieve",
    "OffshoreCapitalMagnetismSieve",
    "ResourceCurseSieve",
    "HighAltitudeAeroDefenseSieve",
    "TripartiteCoherenceSieve",
    "StatutoryBorderDemographySieve",
    "StrategicMetallurgySieve",
    "NuclearAmbiguitySieve",
    "CognitiveSovereigntySieve",
    "AstroSovereigntySieve",
    "RiparianResilienceSieve",
]



