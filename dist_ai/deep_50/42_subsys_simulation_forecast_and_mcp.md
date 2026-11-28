# SUBSYSTEM SPECIFICATION: SIMULATION, FORECASTING & MCP SERVER

## Module: `geo_engine/simulation/__init__.py`

```python
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

```

## Module: `geo_engine/simulation/cascading_engine.py`

```python
"""
Multi-Order Cascading Shock Simulation Engine.
Models transmission, secondary contagion, and tertiary realignments across
the 20 analytical lenses with resilience matrix dampening.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ..core.models import get_system_reference_date


class SimulationShock(BaseModel):
    """Represents an exogenous or endogenous systemic shock event."""
    shock_id: str
    domain: str = Field(..., description="Primary domain/lens where shock originates (e.g. petro_logistics)")
    description: str
    severity: float = Field(..., ge=0.0, le=1.0, description="Initial shock magnitude from 0.0 to 1.0")
    primary_actors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CascadingImpact(BaseModel):
    """Impact telemetry propagated to a specific lens at a specific cascade order."""
    lens: str
    order: int = Field(..., ge=1, le=3, description="Propagation order (1=Direct, 2=Secondary, 3=Tertiary)")
    impact_score: float = Field(..., ge=0.0, le=1.0, description="Adjusted impact severity on this lens")
    transmission_factor: float = Field(..., ge=0.0, le=1.0, description="Base transmission coefficient")
    mitigated_by_resilience: bool = False
    is_tipping_point: bool = False
    critical_resilience_deficit: float = 0.0
    mechanism: str = ""
    recommendation: str = ""


class CascadingSimulationResult(BaseModel):
    """Complete multi-order simulation outcome with systemic vulnerability scoring."""
    shock: SimulationShock
    order_1_impacts: List[CascadingImpact] = Field(default_factory=list)
    order_2_impacts: List[CascadingImpact] = Field(default_factory=list)
    order_3_impacts: List[CascadingImpact] = Field(default_factory=list)
    systemic_vulnerability_index: float = Field(..., ge=0.0, le=1.0)
    propagation_depth: int = 3
    critical_tipping_lenses: List[str] = Field(default_factory=list)
    systemic_phase_transition_risk: float = 0.0
    recommended_mitigations: List[str] = Field(default_factory=list)
    timestamp: str = ""

    def to_markdown(self) -> str:
        lines = [
            f"# Cascading Shock Simulation: {self.shock.shock_id}",
            f"- **Shock Domain:** `{self.shock.domain}` | **Initial Severity:** `{self.shock.severity:.2f}`",
            f"- **Description:** {self.shock.description}",
            f"- **Systemic Vulnerability Index:** `{self.systemic_vulnerability_index:.2f}`",
        ]
        if self.critical_tipping_lenses:
            tipping_str = ", ".join(sorted(set(self.critical_tipping_lenses)))
            lines.append(f"- **Critical Tipping Lenses (Non-Linear Collapse):** `{tipping_str}`")
            lines.append(f"- **Systemic Phase Transition Risk:** `{self.systemic_phase_transition_risk:.2f}`")
        lines.extend([
            f"- **Simulation Timestamp:** `{self.timestamp}`",
            "",
            "## Order 1: Direct Physical & Strategic Impacts",
        ])
        for imp in self.order_1_impacts:
            status = " [Mitigated by Resilience]" if imp.mitigated_by_resilience else ""
            if imp.is_tipping_point:
                status = " [CRITICAL TIPPING POINT / NON-LINEAR SURGE]"
            lines.append(f"- **Lens `{imp.lens}`** (Impact: `{imp.impact_score:.2f}`){status}: {imp.mechanism}")
            if imp.recommendation:
                lines.append(f"  - *Action:* {imp.recommendation}")

        lines.extend(["", "## Order 2: Secondary Macro & Supply Contagion"])
        for imp in self.order_2_impacts:
            status = " [Mitigated by Resilience]" if imp.mitigated_by_resilience else ""
            if imp.is_tipping_point:
                status = " [CRITICAL TIPPING POINT / NON-LINEAR SURGE]"
            lines.append(f"- **Lens `{imp.lens}`** (Impact: `{imp.impact_score:.2f}`){status}: {imp.mechanism}")
            if imp.recommendation:
                lines.append(f"  - *Action:* {imp.recommendation}")

        lines.extend(["", "## Order 3: Tertiary Geopolitical & Civilizational Realignment"])
        for imp in self.order_3_impacts:
            status = " [Mitigated by Resilience]" if imp.mitigated_by_resilience else ""
            if imp.is_tipping_point:
                status = " [CRITICAL TIPPING POINT / NON-LINEAR SURGE]"
            lines.append(f"- **Lens `{imp.lens}`** (Impact: `{imp.impact_score:.2f}`){status}: {imp.mechanism}")
            if imp.recommendation:
                lines.append(f"  - *Action:* {imp.recommendation}")

        if self.recommended_mitigations:
            lines.extend(["", "## Systemic Strategic Mitigations"])
            for m in self.recommended_mitigations:
                lines.append(f"- {m}")

        return "\n".join(lines)


class CascadingSimulationEngine:
    """
    Simulates multi-order shock propagation across the 20 analytical lenses.
    Dampens or amplifies shocks using the Strategic Resilience Matrix.
    """

    CONTAGION_REGISTRY: Dict[str, Dict[int, List[Dict[str, Any]]]] = {
        "petro_logistics": {
            1: [
                {
                    "lens": "petro_logistics",
                    "transmission": 1.0,
                    "mechanism": "Direct physical chokepoint transit halt; immediate spot freight and marine insurance surge.",
                    "recommendation": "Activate strategic petroleum reserves (SPR) and reroute tankers via Cape of Good Hope."
                }
            ],
            2: [
                {
                    "lens": "cash_flow",
                    "transmission": 0.85,
                    "mechanism": "Forex outflow surge and current account deficit expansion driven by energy import inflation.",
                    "recommendation": "Hedge energy import contracts with non-dollar bilateral currency lines."
                },
                {
                    "lens": "food_security",
                    "transmission": 0.75,
                    "mechanism": "Natural gas feedstock disruption choking nitrogen fertilizer (urea/DAP) production.",
                    "recommendation": "Release buffer urea stockpiles and lock sovereign long-term fertilizer imports."
                },
                {
                    "lens": "military_readiness",
                    "transmission": 0.70,
                    "mechanism": "Forward fuel rationing and naval escort deployment requirements for national-flagged tankers.",
                    "recommendation": "Execute naval anti-piracy / convoy escorts across critical chokepoints."
                },
                {
                    "lens": "geo_economist",
                    "transmission": 0.80,
                    "mechanism": "Imported inflation triggering currency depreciation pressure and interest rate volatility.",
                    "recommendation": "Deploy RBI foreign exchange swap lines and prioritize domestic energy substitution."
                }
            ],
            3: [
                {
                    "lens": "geo_economist",
                    "transmission": 0.75,
                    "mechanism": "Accelerated bilateral settlement bypass (Rupee-Dirham, Rupee-Ruble) and de-dollarization.",
                    "recommendation": "Expand mBridge central bank digital currency infrastructure and gold-settled accounts."
                },
                {
                    "lens": "institutional_lawfare",
                    "transmission": 0.65,
                    "mechanism": "Extraterritorial maritime sanctions and UNCLOS disputed passage enforcement.",
                    "recommendation": "File preemptive freedom of navigation declarations and assert sovereign transit immunities."
                },
                {
                    "lens": "civilizational",
                    "transmission": 0.60,
                    "mechanism": "Civilizational self-reliance imperative testing domestic social cohesion under austerity.",
                    "recommendation": "Reinforce national solidarity narrative and subsidize essential domestic staples."
                }
            ]
        },
        "critical_minerals": {
            1: [
                {
                    "lens": "critical_minerals",
                    "transmission": 1.0,
                    "mechanism": "Export embargo or quota restriction on rare earth elements (REEs), lithium, and gallium.",
                    "recommendation": "Mandate domestic stockpiling of strategic magnet alloys and raw battery ores."
                }
            ],
            2: [
                {
                    "lens": "digital_sovereignty",
                    "transmission": 0.85,
                    "mechanism": "Semiconductor substrate and wafer fabrication bottlenecks delaying domestic electronics manufacturing.",
                    "recommendation": "Diversify mineral processing partnerships with Quad / Global South allies."
                },
                {
                    "lens": "deep_tech",
                    "transmission": 0.80,
                    "mechanism": "AI compute accelerator hardware production slowdown due to ceramic capacitor and packaging shortage.",
                    "recommendation": "Accelerate domestic synthetic materials and substitute chemistry R&D."
                },
                {
                    "lens": "cash_flow",
                    "transmission": 0.70,
                    "mechanism": "Massive capital expenditure reallocation toward mineral refining and recycling facilities.",
                    "recommendation": "Issue sovereign critical mineral development bonds."
                }
            ],
            3: [
                {
                    "lens": "geopolitical",
                    "transmission": 0.75,
                    "mechanism": "Formation of bilateral critical mineral alliances and strategic mineral security pacts.",
                    "recommendation": "Anchor India-Australia-Africa critical minerals partnership corridor."
                },
                {
                    "lens": "institutional_lawfare",
                    "transmission": 0.70,
                    "mechanism": "Retaliatory export restrictions and WTO dispute litigation over strategic resources.",
                    "recommendation": "Invoke GATT Article XXI national security exceptions for mineral reserves."
                }
            ]
        },
        "digital_sovereignty": {
            1: [
                {
                    "lens": "digital_sovereignty",
                    "transmission": 1.0,
                    "mechanism": "Advanced node lithography/EDA export denial or sovereign cyber infrastructure attack.",
                    "recommendation": "Enforce sovereign chip design escrow and ring-fence critical telecom architectures."
                }
            ],
            2: [
                {
                    "lens": "deep_tech",
                    "transmission": 0.90,
                    "mechanism": "Indigenous AI cluster training stall due to high-performance GPU procurement bottlenecks.",
                    "recommendation": "Federate existing national compute supercomputing clusters under IndiaAI mission."
                },
                {
                    "lens": "subsea_cables",
                    "transmission": 0.75,
                    "mechanism": "Heightened surveillance and routing reroutes across sovereign data landing gates.",
                    "recommendation": "Mandate end-to-end sovereign encryption at all coastal cable landing stations."
                },
                {
                    "lens": "hybrid_covert",
                    "transmission": 0.70,
                    "mechanism": "Targeted APT cyber intrusions into critical public infrastructure and SCADA systems.",
                    "recommendation": "Deploy military cyber defense teams to air-gap state power and railway grids."
                }
            ],
            3: [
                {
                    "lens": "geo_economist",
                    "transmission": 0.75,
                    "mechanism": "Sovereign capital commitment to domestic fab construction and fabless IP ecosystems.",
                    "recommendation": "Deploy production-linked incentives (PLI) for 28nm legacy automotive and defense silicon."
                },
                {
                    "lens": "civilizational",
                    "transmission": 0.65,
                    "mechanism": "Assertion of civilizational information sovereignty against algorithmic narrative colonization.",
                    "recommendation": "Promote indigenous cultural LLMs aligned with multi-linguistic civilizational heritage."
                }
            ]
        },
        "institutional_lawfare": {
            1: [
                {
                    "lens": "institutional_lawfare",
                    "transmission": 1.0,
                    "mechanism": "Extraterritorial sanctions, FATF weaponization, or judicial/constitutional interventionism.",
                    "recommendation": "Counter with statutory anti-foreign-sanctions frameworks and constitutional sovereign immunity."
                }
            ],
            2: [
                {
                    "lens": "cash_flow",
                    "transmission": 0.85,
                    "mechanism": "FII capital flight and correspondent banking friction caused by secondary sanction threats.",
                    "recommendation": "Strengthen non-Western clearing channels and offshore Rupee markets."
                },
                {
                    "lens": "propaganda",
                    "transmission": 0.80,
                    "mechanism": "Coordinated transnational media/NGO blitz exploiting domestic judicial or statutory fault-lines.",
                    "recommendation": "Release factual forensic whitepapers debunking disinformation campaigns."
                },
                {
                    "lens": "india_timeline",
                    "transmission": 0.75,
                    "mechanism": "Foreign funding channeled through FCRA loopholes to trigger local civil unrest.",
                    "recommendation": "Strictly enforce FCRA audits and monitor border NGO bank flows."
                }
            ],
            3: [
                {
                    "lens": "civilizational",
                    "transmission": 0.80,
                    "mechanism": "Assertion of Dharmic constitutional jurisprudence against imported legal dogmas.",
                    "recommendation": "Codify Dharmic civilizational principles (Rajdharma, Nyaya) into sovereign administrative doctrine."
                },
                {
                    "lens": "geo_economist",
                    "transmission": 0.70,
                    "mechanism": "Accelerated repatriation of foreign-held gold and sovereign debt de-risking.",
                    "recommendation": "Repatriate central bank gold reserves to domestic vaults."
                }
            ]
        },
        "subsea_cables": {
            1: [
                {
                    "lens": "subsea_cables",
                    "transmission": 1.0,
                    "mechanism": "Physical undersea cable cut or chokepoint sabotage disabling intercontinental bandwidth.",
                    "recommendation": "Deploy naval repair ships under armed escort and reroute traffic through terrestrial fiber."
                }
            ],
            2: [
                {
                    "lens": "digital_sovereignty",
                    "transmission": 0.85,
                    "mechanism": "Severe internet bandwidth degradation and international latency spikes.",
                    "recommendation": "Enforce domestic data localization and prioritize essential public services."
                },
                {
                    "lens": "cash_flow",
                    "transmission": 0.75,
                    "mechanism": "Cross-border financial messaging delays and algorithmic transaction stalls.",
                    "recommendation": "Switch sovereign payment clearing to domestic RuPay/UPI/NEFT rails."
                },
                {
                    "lens": "hybrid_covert",
                    "transmission": 0.80,
                    "mechanism": "Covert undersea reconnaissance and seabed hydrophone acoustic network activation.",
                    "recommendation": "Deploy unmanned underwater vehicles (UUVs) to monitor maritime EEZ seabed assets."
                }
            ],
            3: [
                {
                    "lens": "military_readiness",
                    "transmission": 0.75,
                    "mechanism": "Naval seabed warfare doctrine operationalization and EEZ cable corridor patrols.",
                    "recommendation": "Establish joint naval-civilian seabed protection task forces."
                },
                {
                    "lens": "geo_economist",
                    "transmission": 0.70,
                    "mechanism": "Capital allocation to land-based continental fiber transit corridors (e.g. IMEC).",
                    "recommendation": "Co-finance terrestrial trans-Eurasian/Middle East fiber links."
                }
            ]
        },
        "military_readiness": {
            1: [
                {
                    "lens": "military_readiness",
                    "transmission": 1.0,
                    "mechanism": "Border escalation, Line of Actual Control confrontation, or troop mobilization crisis.",
                    "recommendation": "Elevate ORBAT readiness, disburse emergency war wastage reserves (WWR)."
                }
            ],
            2: [
                {
                    "lens": "petro_logistics",
                    "transmission": 0.80,
                    "mechanism": "Strategic aviation turbine fuel and diesel rationing for forward operational bases.",
                    "recommendation": "Pre-position underground fuel bladders and ensure secure railway pipelines."
                },
                {
                    "lens": "cash_flow",
                    "transmission": 0.85,
                    "mechanism": "Emergency defense capex surge, reallocating capital from civilian infrastructure.",
                    "recommendation": "Invoke fast-track emergency financial powers for domestic defense procurement."
                },
                {
                    "lens": "hybrid_covert",
                    "transmission": 0.75,
                    "mechanism": "Hostile cyber, electronic warfare jamming, and satellite communication spoofing.",
                    "recommendation": "Switch command networks to jam-resistant indigenous optical and SDR networks."
                }
            ],
            3: [
                {
                    "lens": "geopolitical",
                    "transmission": 0.85,
                    "mechanism": "Bilateral deterrence signaling and alignment with regional defense coalitions.",
                    "recommendation": "Signal clear punitive retaliation thresholds through strategic posture."
                },
                {
                    "lens": "civilizational",
                    "transmission": 0.80,
                    "mechanism": "Civilizational resolve testing national endurance and sovereign territorial non-negotiability.",
                    "recommendation": "Reinforce national civilizational unity and civil defense preparedness."
                }
            ]
        },
        "food_security": {
            1: [
                {
                    "lens": "food_security",
                    "transmission": 1.0,
                    "mechanism": "Severe crop failure, maritime grain corridor blockade, or fertilizer export stoppage (Urea/DAP/MOP).",
                    "recommendation": "Mobilize buffer food stocks, invoke emergency grain export bans, and release strategic potash reserves."
                }
            ],
            2: [
                {
                    "lens": "cash_flow",
                    "transmission": 0.85,
                    "mechanism": "Food and fertilizer subsidy bills spike, straining fiscal deficits and sovereign borrowing.",
                    "recommendation": "Expand direct benefit transfer (DBT) efficiency and prune non-essential fiscal expenditures."
                },
                {
                    "lens": "demographic_infiltration",
                    "transmission": 0.75,
                    "mechanism": "Regional food insecurity and famine triggers sudden refugee migrations across borders.",
                    "recommendation": "Reinforce border vigilance and coordinate humanitarian relief at regional borders."
                },
                {
                    "lens": "petro_logistics",
                    "transmission": 0.70,
                    "mechanism": "Emergency bulk grain and fertilizer maritime transport demands compete with energy shipping.",
                    "recommendation": "Prioritize sovereign charter vessels for essential food staples."
                }
            ],
            3: [
                {
                    "lens": "civilizational",
                    "transmission": 0.80,
                    "mechanism": "Public distribution system stability directly preserves internal civilizational social contract.",
                    "recommendation": "Maintain Annaraksha / grain assurance through grassroots cooperative networks."
                },
                {
                    "lens": "geopolitical",
                    "transmission": 0.75,
                    "mechanism": "Food diplomacy becomes vital strategic leverage across the Global South.",
                    "recommendation": "Establish grain-for-energy bilateral barter arrangements with partner nations."
                }
            ]
        },
        "demographic_infiltration": {
            1: [
                {
                    "lens": "demographic_infiltration",
                    "transmission": 1.0,
                    "mechanism": "Engineered mass border crossings, porous border infiltration, and illegal migrant transit networks.",
                    "recommendation": "Deploy thermal imaging surveillance, seal porous riverine frontiers, and enforce border biometric registration."
                }
            ],
            2: [
                {
                    "lens": "institutional_lawfare",
                    "transmission": 0.85,
                    "mechanism": "Extraterritorial human rights bodies and local PIL litigation networks contest border deportations.",
                    "recommendation": "Assert sovereign national security exemptions under domestic statutory immigration acts."
                },
                {
                    "lens": "hybrid_covert",
                    "transmission": 0.80,
                    "mechanism": "Adversary intelligence services utilize undocumented corridors for sleeper cell and contraband transit.",
                    "recommendation": "Intensify joint intelligence grid (NATGRID) monitoring of border transit hubs."
                },
                {
                    "lens": "india_timeline",
                    "transmission": 0.80,
                    "mechanism": "Demographic transformation in sensitive border corridors (e.g. Siliguri corridor, chicken neck).",
                    "recommendation": "Fortify strategic corridor infrastructure and conduct comprehensive census audits."
                }
            ],
            3: [
                {
                    "lens": "civilizational",
                    "transmission": 0.85,
                    "mechanism": "Long-term shifts in local civilizational demography and social cohesion in border regions.",
                    "recommendation": "Preserve indigenous civilizational ethos, linguistic continuity, and local community rights."
                },
                {
                    "lens": "geopolitical",
                    "transmission": 0.70,
                    "mechanism": "Cross-border diplomatic friction with neighbor states facilitating transit.",
                    "recommendation": "Tie bilateral economic cooperation to verified border control compliance."
                }
            ]
        },
        "astro_politics": {
            1: [
                {
                    "lens": "astro_politics",
                    "transmission": 1.0,
                    "mechanism": "Anti-satellite (ASAT) test, orbital space debris cascade (Kessler syndrome), or LEO satcom jamming.",
                    "recommendation": "Activate ISRO Project NETRA for collision avoidance and deploy maneuverable defensive satellites."
                }
            ],
            2: [
                {
                    "lens": "military_readiness",
                    "transmission": 0.90,
                    "mechanism": "PNT (Positioning, Navigation, and Timing) and battlefield satcom communication degradation.",
                    "recommendation": "Switch military navigation to indigenous NavIC constellation and ground-based inertial systems."
                },
                {
                    "lens": "deep_tech",
                    "transmission": 0.80,
                    "mechanism": "Loss of orbital Earth observation data impacting weather, defense reconnaissance, and disaster response.",
                    "recommendation": "Deploy high-altitude pseudo-satellite (HAPS) UAVs for persistent tactical reconnaissance."
                },
                {
                    "lens": "critical_minerals",
                    "transmission": 0.70,
                    "mechanism": "Space-grade radiation-hardened gallium, germanium, and solar wafer supply choke.",
                    "recommendation": "Stockpile space-qualified components and support domestic rad-hard semiconductor fabs."
                }
            ],
            3: [
                {
                    "lens": "geopolitical",
                    "transmission": 0.85,
                    "mechanism": "Multilateral contestation over lunar/orbital property rights and Artemis vs. ILRS space bloc division.",
                    "recommendation": "Anchor sovereign strategic posture in peaceful outer space exploration coalitions."
                },
                {
                    "lens": "institutional_lawfare",
                    "transmission": 0.75,
                    "mechanism": "Outer Space Treaty (OST) liability disputes and ITU orbital slot contention.",
                    "recommendation": "File protective spectrum and slot claims with International Telecommunication Union (ITU)."
                }
            ]
        },
        "geo_economist": {
            1: [
                {
                    "lens": "geo_economist",
                    "transmission": 1.0,
                    "mechanism": "Weaponization of reserve currencies, SWIFT disconnection, or sovereign debt downgrade shock.",
                    "recommendation": "Diversify foreign exchange reserves into central bank physical gold and sovereign bilateral currency lines."
                }
            ],
            2: [
                {
                    "lens": "cash_flow",
                    "transmission": 0.90,
                    "mechanism": "Immediate capital flight, equity market drawdowns, and severe exchange rate depreciation pressure.",
                    "recommendation": "Activate RBI currency swap lines, raise domestic policy rates, and manage capital outflows."
                },
                {
                    "lens": "petro_logistics",
                    "transmission": 0.85,
                    "mechanism": "Inability to settle international crude cargoes in US dollars creating physical supply panic.",
                    "recommendation": "Route crude payments through non-dollar Vostro accounts and bilateral energy barter."
                },
                {
                    "lens": "bureaucratic_inertia",
                    "transmission": 0.75,
                    "mechanism": "Inter-ministerial hesitation to authorize non-standard settlement mechanisms and regulatory bottlenecks.",
                    "recommendation": "Empower high-level economic crisis steering group to fast-track bilateral trade protocols."
                }
            ],
            3: [
                {
                    "lens": "civilizational",
                    "transmission": 0.80,
                    "mechanism": "Macroeconomic sovereign self-reliance (Atmanirbharta) affirmed as civilizational survival necessity.",
                    "recommendation": "Promote swadeshi production networks and reduce structural reliance on foreign debt."
                },
                {
                    "lens": "geopolitical",
                    "transmission": 0.85,
                    "mechanism": "Consolidation of multi-polar economic architecture and expansion of non-Western clearing unions.",
                    "recommendation": "Deepen integration with BRICS Pay, mBridge, and Asian Clearing Union (ACU)."
                }
            ]
        }
    }

    @classmethod
    def simulate_shock(
        cls,
        shock: SimulationShock,
        resilience_matrix: Optional[Dict[str, float]] = None
    ) -> CascadingSimulationResult:
        """
        Calculates multi-order impact scores across the 20 analytical lenses.
        Applies resilience dampening factors based on the resilience_matrix.
        """
        ref_time = get_system_reference_date().strftime("%Y-%m-%d %H:%M:%S UTC")
        domain_data = cls.CONTAGION_REGISTRY.get(shock.domain)

        # Fallback dynamic contagion mapping if domain not pre-configured
        if not domain_data:
            domain_data = {
                1: [
                    {
                        "lens": shock.domain,
                        "transmission": 1.0,
                        "mechanism": f"Direct primary shock manifestation in {shock.domain}.",
                        "recommendation": f"Mobilize dedicated {shock.domain} emergency protocols."
                    }
                ],
                2: [
                    {
                        "lens": "cash_flow",
                        "transmission": 0.75,
                        "mechanism": "General financial and capital allocation friction arising from domain shock.",
                        "recommendation": "Buffer fiscal reserves and monitor liquidity."
                    },
                    {
                        "lens": "geopolitical",
                        "transmission": 0.70,
                        "mechanism": "Diplomatic and strategic balance shifts resulting from primary disturbance.",
                        "recommendation": "Engage bilateral partners to reinforce mutual commitments."
                    }
                ],
                3: [
                    {
                        "lens": "civilizational",
                        "transmission": 0.65,
                        "mechanism": "Long-term civilizational resilience and institutional stability equilibrium.",
                        "recommendation": "Preserve core institutional continuity and Dharmic societal harmony."
                    },
                    {
                        "lens": "geo_economist",
                        "transmission": 0.60,
                        "mechanism": "Macro-economic structural adjustments and sovereign self-reliance.",
                        "recommendation": "Strengthen diversified domestic production capacities."
                    }
                ]
            }

        order_1: List[CascadingImpact] = []
        order_2: List[CascadingImpact] = []
        order_3: List[CascadingImpact] = []
        all_impacts: List[CascadingImpact] = []

        for order_num, impact_list in domain_data.items():
            for item in impact_list:
                lens = item["lens"]
                trans = item["transmission"]
                raw_score = shock.severity * trans

                # Order decay coefficient (Order 1: 1.0, Order 2: 0.85, Order 3: 0.70)
                order_decay = 1.0 if order_num == 1 else (0.85 if order_num == 2 else 0.70)
                base_impact = raw_score * order_decay

                # Resilience dampening & Non-Linear Tipping Dynamics
                mitigated = False
                is_tipping = False
                resilience_deficit = 0.0
                resilience_val = 0.5  # default baseline resilience
                if resilience_matrix and lens in resilience_matrix:
                    resilience_val = float(resilience_matrix[lens])
                    # Check for Critical Tipping Point (Non-Linear Contagion Surge)
                    # Critical condition: Sector resilience is severely depleted (R < 0.35)
                    # OR initial shock magnitude overwhelms absorption capacity (shock.severity >= 0.75 and R <= 0.40)
                    if resilience_val < 0.35 or (shock.severity >= 0.75 and resilience_val <= 0.40):
                        is_tipping = True
                        resilience_deficit = round(max(0.0, 0.35 - resilience_val), 4)
                        # Sigmoid surge multiplier: when R is deficient, impact accelerates non-linearly
                        import math
                        surge_factor = 1.0 + (0.50 / (1.0 + math.exp(10.0 * (resilience_val - 0.25))))
                        dampened_impact = base_impact * surge_factor
                    else:
                        # Standard linear dampening: Higher resilience dampens impact: up to 50% reduction
                        dampened_impact = base_impact * (1.0 - (0.5 * resilience_val))
                        if resilience_val >= 0.70:
                            mitigated = True
                else:
                    dampened_impact = base_impact

                final_impact = max(0.0, min(1.0, round(dampened_impact, 4)))

                imp = CascadingImpact(
                    lens=lens,
                    order=order_num,
                    impact_score=final_impact,
                    transmission_factor=trans,
                    mitigated_by_resilience=mitigated,
                    is_tipping_point=is_tipping,
                    critical_resilience_deficit=resilience_deficit,
                    mechanism=item["mechanism"],
                    recommendation=item["recommendation"]
                )

                if order_num == 1:
                    order_1.append(imp)
                elif order_num == 2:
                    order_2.append(imp)
                else:
                    order_3.append(imp)
                all_impacts.append(imp)

        # Calculate systemic vulnerability index and phase transition risk
        critical_tipping = [imp.lens for imp in all_impacts if imp.is_tipping_point]
        phase_transition_risk = 0.0
        if critical_tipping:
            tipping_ratio = len(critical_tipping) / max(1, len(all_impacts))
            phase_transition_risk = round(min(1.0, tipping_ratio * (1.0 + shock.severity * 0.5)), 4)

        if all_impacts:
            # Weighted average: Order 1 has weight 0.5, Order 2 has 0.3, Order 3 has 0.2
            weights = {1: 0.5, 2: 0.3, 3: 0.2}
            weighted_sum = sum(imp.impact_score * weights.get(imp.order, 0.1) for imp in all_impacts)
            total_weight = sum(weights.get(imp.order, 0.1) for imp in all_impacts)
            vulnerability = round(weighted_sum / total_weight, 4) if total_weight > 0 else 0.5
        else:
            vulnerability = shock.severity

        # Extract top recommendations
        unique_recs = []
        for imp in all_impacts:
            if imp.recommendation and imp.recommendation not in unique_recs:
                unique_recs.append(imp.recommendation)

        return CascadingSimulationResult(
            shock=shock,
            order_1_impacts=order_1,
            order_2_impacts=order_2,
            order_3_impacts=order_3,
            systemic_vulnerability_index=min(1.0, max(0.0, vulnerability)),
            propagation_depth=3,
            critical_tipping_lenses=critical_tipping,
            systemic_phase_transition_risk=phase_transition_risk,
            recommended_mitigations=unique_recs[:5],
            timestamp=ref_time
        )

```

## Module: `geo_engine/simulation/game_theoretic.py`

```python
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
        intent: str = "",
        persist: bool = False,
        store: Optional[Any] = None,
        session_id: Optional[str] = None
    ) -> GameTheoreticSimulationResult:
        """
        Executes a 3-turn sequential game-theoretic simulation.
        Optionally persists campaign session and turn state into EventStore SQLite database.
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

        sim_id = session_id or f"SIM-GT-{initiator.name[:3].upper()}-{target.name[:3].upper()}-{domain[:4].upper()}"

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

        if persist:
            import json
            from ..storage.event_store import EventStore
            target_store = store or EventStore()
            session_data = {
                "session_id": sim_id,
                "initiator": initiator.name,
                "target": target.name,
                "domain": domain,
                "action_summary": turn_1.action_description,
                "counter_summary": turn_2.action_description,
                "backlash_summary": turn_3.de_escalation_off_ramp,
                "equilibrium_payoff": stability,
                "status": "COMPLETED",
                "created_at": ref_time
            }
            turns = [
                {
                    "turn_number": 1,
                    "actor": initiator.name,
                    "domain": domain,
                    "action_description": turn_1.action_description,
                    "severity": turn_1.severity,
                    "payoff": init_payoff,
                    "details_json": json.dumps({"declared_intent": turn_1.declared_intent})
                },
                {
                    "turn_number": 2,
                    "actor": target.name,
                    "domain": counter_domain,
                    "action_description": turn_2.action_description,
                    "severity": turn_2.severity,
                    "payoff": target_payoff,
                    "details_json": json.dumps({"response_type": turn_2.response_type, "rationality": turn_2.strategic_rationality})
                },
                {
                    "turn_number": 3,
                    "actor": "SYSTEMIC_EQUILIBRIUM",
                    "domain": "systemic",
                    "action_description": turn_3.third_party_realignment,
                    "severity": turn_3.escalation_spiral_risk,
                    "payoff": stability,
                    "details_json": json.dumps({
                        "domestic_friction": turn_3.domestic_political_friction,
                        "inflation_score": turn_3.inflationary_backlash_score,
                        "off_ramp": turn_3.de_escalation_off_ramp
                    })
                }
            ]
            target_store.save_wargame_session(session_data, turns)

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

```

## Module: `geo_engine/simulation/mcmc_wargamer.py`

```python
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

    @classmethod
    def seed_from_lens_evaluations(
        cls,
        evaluations: List[Any],
        initiator: str = "India",
        target: str = "China",
        horizon_months: int = 24,
        num_simulations: int = 1000
    ) -> MCMCScenarioConfig:
        """
        Phase 85: Dynamic Lens-Coupled MCMC Configuration Generator.
        Bridges the isolated Markov Chain Monte Carlo simulator directly to the outputs of LENS_REGISTRY.
        Extracts:
        - MilitaryReadinessLens: WWR days and deterrence posture
        - CashFlowLens & GeoEconomistLens: FX cover and effective CapEx
        - GeopoliticalLens & ChokepointKineticSieve: Initial conflict state (S0 to S4)
        - BureaucraticInertiaLens & PropagandaLens: Domestic friction factor
        """
        eval_map = {}
        for ev in evaluations:
            name = getattr(ev, "lens_name", "")
            eval_map[name] = ev

        geo_eval = None
        mil_eval = None
        cash_eval = None
        bureau_eval = None

        for k, v in eval_map.items():
            k_lower = k.lower()
            if "geopolitical" in k_lower or "chokepoint" in k_lower:
                geo_eval = v
            elif "military" in k_lower or "avionics" in k_lower:
                mil_eval = v
            elif "cash" in k_lower or "geo-economist" in k_lower or "geoeconomic" in k_lower:
                cash_eval = v
            elif "bureaucratic" in k_lower or "propaganda" in k_lower:
                bureau_eval = v

        geo_score = getattr(geo_eval, "alignment_score", 0.0) if geo_eval else 0.0
        v_choke = getattr(geo_eval, "hard_metrics", {}).get("chokepoint_vulnerability_index", 0.0) if geo_eval else 0.0

        if v_choke >= 0.75 or geo_score <= -0.70:
            init_state = ConflictState.S3_LOCALIZED_KINETIC
        elif v_choke >= 0.50 or geo_score <= -0.40:
            init_state = ConflictState.S1_GREY_ZONE_FRICTION
        elif v_choke >= 0.30 or geo_score < 0.0:
            init_state = ConflictState.S2_ECONOMIC_ATTRITION
        else:
            init_state = ConflictState.S0_DETERRENCE_EQUILIBRIUM

        mil_metrics = getattr(mil_eval, "hard_metrics", {}) if mil_eval else {}
        initiator_wwr = float(mil_metrics.get("wwr_ammunition_reserve_days", 20.0))

        cash_metrics = getattr(cash_eval, "hard_metrics", {}) if cash_eval else {}
        fx_cover = float(cash_metrics.get("fx_import_cover_months", 11.5))

        bureau_metrics = getattr(bureau_eval, "hard_metrics", {}) if bureau_eval else {}
        domestic_friction = float(bureau_metrics.get("bureaucratic_delay_index", 0.35))
        domestic_friction = max(0.05, min(0.95, domestic_friction))

        return MCMCScenarioConfig(
            initiator_name=initiator,
            target_name=target,
            initial_state=init_state,
            horizon_months=horizon_months,
            num_simulations=num_simulations,
            initiator_wwr_days=initiator_wwr,
            target_wwr_days=25.0,
            initiator_fx_cover_months=fx_cover,
            target_fx_cover_months=14.0,
            domestic_friction_factor=domestic_friction
        )


```

## Module: `geo_engine/forecasting/__init__.py`

```python
"""
Forecasting and calibration package for the Geo-Engine.
"""

from .calibration import (
    ScenarioBranch,
    CalibratedForecast,
    EpistemicStrata,
    BrierScorer,
    ForecastingEngine,
    calculate_temporal_decay,
)
from .resolution_daemon import ForecastResolutionDaemon

__all__ = [
    "ScenarioBranch",
    "CalibratedForecast",
    "EpistemicStrata",
    "BrierScorer",
    "ForecastingEngine",
    "calculate_temporal_decay",
    "ForecastResolutionDaemon",
]


```

## Module: `geo_engine/forecasting/calibration.py`

```python
"""
Calibrated Forecasting and Brier Scoring Engine.
Separates geopolitical analysis into four rigorous epistemic strata:
Observed, Inferred, Scenario, and Calibrated Forecast with statistical verification.
"""

import math
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from ..core.models import get_system_reference_date


def calculate_temporal_decay(
    event_date: str,
    reference_date: Optional[str] = None,
    half_life_days: float = 90.0
) -> float:
    """
    Calculates exponential temporal decay weight: w(t) = exp(-ln(2) * delta_t / tau).
    For statutory treaties, constitutional articles, and legal covenants, tau = inf, returning 1.0.
    For volatile macro telemetry and headline events, default tau = 90.0 days.
    """
    if half_life_days <= 0 or math.isinf(half_life_days):
        return 1.0

    try:
        cleaned_event_date = str(event_date).strip()[:10]
        evt_dt = datetime.strptime(cleaned_event_date, "%Y-%m-%d")

        if reference_date:
            cleaned_ref_date = str(reference_date).strip()[:10]
            ref_dt = datetime.strptime(cleaned_ref_date, "%Y-%m-%d")
        else:
            ref_dt = get_system_reference_date()
            if hasattr(ref_dt, "tzinfo") and ref_dt.tzinfo is not None:
                ref_dt = ref_dt.replace(tzinfo=None)

        delta_days = (ref_dt - evt_dt).total_seconds() / 86400.0
        if delta_days <= 0:
            return 1.0

        decay = math.exp(-(math.log(2.0) * delta_days) / half_life_days)
        return round(float(decay), 4)
    except Exception:
        return 1.0


class ScenarioBranch(BaseModel):
    """Represents a discrete possible future outcome branch."""
    scenario_name: str
    probability: float = Field(..., ge=0.0, le=1.0)
    key_drivers: List[str]
    early_indicators: List[str]
    impact_severity: str = Field(default="MEDIUM", description="'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'")


class CalibratedForecast(BaseModel):
    """A mathematically bounded probabilistic projection."""
    target_hypothesis: str
    forecast_probability: float = Field(..., ge=0.0, le=1.0)
    confidence_interval_low: float = Field(..., ge=0.0, le=1.0)
    confidence_interval_high: float = Field(..., ge=0.0, le=1.0)
    time_horizon_months: int = 12
    epistemic_basis: str = ""


class EpistemicStrata(BaseModel):
    """Complete 4-layer partitioned output preventing confusion between observed facts and forecasts."""
    observed_facts: List[str] = Field(default_factory=list, description="Empirical ground truth (Tier 1/2)")
    inferred_realities: List[str] = Field(default_factory=list, description="Cross-lens triangulated deductions")
    scenario_branches: List[ScenarioBranch] = Field(default_factory=list)
    calibrated_forecasts: List[CalibratedForecast] = Field(default_factory=list)


class BrierScorer:
    """Calculates statistical calibration and Brier scores for historical forecast backtesting."""

    @staticmethod
    def calculate_brier_score(forecast_probabilities: List[float], observed_outcomes: List[int]) -> float:
        """
        Calculates the Brier score: (1/N) * sum((f_t - o_t)^2).
        Scores range from 0.0 (perfect accuracy) to 1.0 (complete failure).
        """
        if not forecast_probabilities or not observed_outcomes or len(forecast_probabilities) != len(observed_outcomes):
            raise ValueError("forecast_probabilities and observed_outcomes must be non-empty lists of identical length.")

        n = len(forecast_probabilities)
        total_error = sum((f - o) ** 2 for f, o in zip(forecast_probabilities, observed_outcomes))
        return round(total_error / n, 4)


class ForecastingEngine:
    """Generates calibrated probabilistic scenarios for multilateral events."""

    @staticmethod
    def calculate_temporal_decay(
        event_date: str,
        reference_date: Optional[str] = None,
        half_life_days: float = 90.0
    ) -> float:
        return calculate_temporal_decay(event_date, reference_date, half_life_days)

    @classmethod
    def update_scenario_probabilities(
        cls,
        scenarios: List[ScenarioBranch],
        evidence_claims: Optional[List[Any]] = None,
        reference_date: Optional[str] = None
    ) -> List[ScenarioBranch]:
        """
        Applies Reliability-Weighted Heuristic Updating (discrete quasi-Bayesian likelihood updating)
        to scenario branches based on incoming evidence claims with exponential temporal decay.
        Ensures the sum of all updated probabilities strictly equals 1.0 while explicitly bounding
        scenario uncertainty according to epistemic reliability weights and recency.
        """
        if not evidence_claims or not scenarios:
            return scenarios

        # Discard TIER_0 / insufficient or 0-reliability degraded claims before updating
        valid_claims = [
            c for c in evidence_claims
            if getattr(c, "evidence_status", "sufficient") != "insufficient"
            and getattr(c, "reliability_weight", 1.0) > 0.0
        ]
        if not valid_claims:
            return scenarios

        # Helper to compute effective weight combining epistemic reliability and temporal decay
        def _get_effective_claim_weight(claim: Any) -> float:
            base_rel = float(getattr(claim, "reliability_weight", 1.0))
            # Determine if claim is perpetual statutory/treaty/constitutional (tau = inf)
            claim_type = str(getattr(claim, "claim_type", ""))
            epistemic_tier = str(getattr(claim, "epistemic_tier", ""))
            fact_text = getattr(claim, "asserted_fact", getattr(claim, "assertion", ""))
            is_statutory = (
                "LEGAL_COMMITMENT" in claim_type or
                "TIER_3" in epistemic_tier or
                any(kw in fact_text.lower() for kw in ["treaty", "statute", "clause", "act 19", "act 20", "constitution", "article 10", "article 44", "article 30"])
            )
            tau = float("inf") if is_statutory else 90.0
            claim_dt = (
                getattr(claim, "event_date", None) or
                getattr(claim, "date", None) or
                getattr(claim, "created_at", None) or
                getattr(claim, "timestamp", None)
            )
            if claim_dt:
                decay = calculate_temporal_decay(str(claim_dt), reference_date=reference_date, half_life_days=tau)
            else:
                decay = 1.0
            return round(base_rel * decay, 4)

        # Weight claim contributions by their effective reliability and temporal recency
        # 6 named domain groups replacing the original 2 — covers all scenario types
        sanction_or_covert_count = sum(
            _get_effective_claim_weight(c) for c in valid_claims
            if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in [
                "sanction", "fatf", "ofac", "intercept", "chokepoint", "infiltrat", "migrant",
                "lawfare", "icc", "icj", "asset freeze", "secondary sanction", "blacklist"
            ])
        )
        sinocentric_or_friction_count = sum(
            _get_effective_claim_weight(c) for c in valid_claims
            if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in [
                "cips", "yuan", "pla", "border tension", "dispute", "lac", "china", "beijing",
                "belt and road", "bri", "debt trap", "sinosphere"
            ])
        )
        energy_petro_count = sum(
            _get_effective_claim_weight(c) for c in valid_claims
            if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in [
                "crude", "oil", "tanker", "hormuz", "bab el-mandeb", "malacca", "shadow fleet",
                "energy", "petro", "lng", "natural gas", "opec", "refinery"
            ])
        )
        food_fertilizer_count = sum(
            _get_effective_claim_weight(c) for c in valid_claims
            if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in [
                "food", "fertilizer", "urea", "dap", "mop", "potash", "grain", "wheat", "rice",
                "famine", "buffer stock", "caloric", "agriculture", "monsoon", "groundwater"
            ])
        )
        military_conflict_count = sum(
            _get_effective_claim_weight(c) for c in valid_claims
            if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in [
                "troop", "military", "orbat", "standoff", "clash", "galwan", "doklam",
                "nuclear", "missile", "escalation", "conflict", "war", "operation sindoor", "balakot"
            ])
        )
        tech_minerals_count = sum(
            _get_effective_claim_weight(c) for c in valid_claims
            if any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower() for kw in [
                "semiconductor", "chip", "rare earth", "lithium", "gallium", "germanium",
                "critical mineral", "refining monopoly", "ndfeb", "huawei", "5g", "compute"
            ])
        )

        likelihoods = []
        for s in scenarios:
            l = 1.0
            s_name = s.scenario_name.lower()
            if "disruption" in s_name or "decoupling" in s_name or "sanctions" in s_name or "lawfare" in s_name:
                l += sanction_or_covert_count * 0.35
            elif "sinocentric" in s_name or "capture" in s_name or "friction" in s_name or "china" in s_name:
                l += sinocentric_or_friction_count * 0.35
            elif "energy" in s_name or "oil" in s_name or "petro" in s_name or "hormuz" in s_name:
                l += energy_petro_count * 0.35
            elif "food" in s_name or "fertilizer" in s_name or "famine" in s_name or "caloric" in s_name:
                l += food_fertilizer_count * 0.35
            elif "conflict" in s_name or "military" in s_name or "escalation" in s_name or "war" in s_name:
                l += military_conflict_count * 0.35
            elif "tech" in s_name or "mineral" in s_name or "semiconductor" in s_name or "supply chain" in s_name:
                l += tech_minerals_count * 0.35
            else:
                total_evidence_weight = (
                    sanction_or_covert_count + sinocentric_or_friction_count +
                    energy_petro_count + food_fertilizer_count +
                    military_conflict_count + tech_minerals_count
                )
                if total_evidence_weight > 0:
                    l = max(0.4, 1.0 - (0.10 * total_evidence_weight))
            likelihoods.append(l)


        unnormalized = [s.probability * l for s, l in zip(scenarios, likelihoods)]
        total_prob = sum(unnormalized)

        if total_prob <= 0:
            return scenarios

        updated_branches = []
        for s, unnorm in zip(scenarios, unnormalized):
            norm_prob = round(unnorm / total_prob, 3)
            updated_branches.append(ScenarioBranch(
                scenario_name=s.scenario_name,
                probability=norm_prob,
                key_drivers=s.key_drivers,
                early_indicators=s.early_indicators,
                impact_severity=s.impact_severity
            ))

        diff = round(1.0 - sum(b.probability for b in updated_branches), 3)
        if diff != 0:
            updated_branches[0].probability = round(updated_branches[0].probability + diff, 3)

        return updated_branches

    @classmethod
    def generate_strata(
        cls,
        summit_name: str = "BRICS 2026 Summit",
        year: int = 2026,
        evidence_claims: Optional[List[Any]] = None,
        event_type: Optional[str] = None,
        include_unmodeled: bool = False
    ) -> EpistemicStrata:
        """
        Generates calibrated 4-strata intelligence for the summit or crisis event with optional Bayesian evidence updates.
        Supports parameterization by event_type (SUMMIT, BORDER_MILITARY, BORDER_SECURITY, GEO_ECONOMIC, HYBRID_WARFARE).
        """
        if event_type == "BORDER_MILITARY":
            observed = [
                "Forward military deployments and logistics lines established along frontline sectors.",
                "Regular bilateral military commander and diplomatic working mechanism (WMCC) meetings active.",
                "High-altitude drone surveillance and border radar infrastructure operational.",
                "Bilateral disengagement protocols maintain demarcated buffer zones."
            ]
            inferred = [
                "Neither sovereign actor seeks systemic kinetic escalation across high-altitude terrain.",
                "Dual-use border infrastructure buildup creates permanent forward mobilization capability.",
                "Long-term stability requires formalized protocol demilitarization rather than rhetorical declarations."
            ]
            scenarios = [
                ScenarioBranch(
                    scenario_name="Scenario A: Managed Bilateral Patrolling & Buffer Zone Status Quo (Baseline)",
                    probability=0.60,
                    key_drivers=["Adherence to frontline commander protocols", "Mutual recognition of buffer boundaries"],
                    early_indicators=["Scheduled border flag meetings", "Zero unilateral forward patrol intrusions"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario B: Friction-Driven Tactical Standoff & Mobilization Surge",
                    probability=0.25,
                    key_drivers=["Infrastructure development near friction points", "Airspace or patrol transgressions"],
                    early_indicators=["Sudden deployment of mechanized armor", "Breakdown in weekly hotline communications"],
                    impact_severity="HIGH"
                ),
                ScenarioBranch(
                    scenario_name="Scenario C: Diplomatic Disengagement & Mutual Demarcation Accord",
                    probability=0.10,
                    key_drivers=["High-level political consensus", "Mutual strategic redeployment to peace-time garrisons"],
                    early_indicators=["Joint verification mechanism announcement", "Synchronized troop pullbacks"],
                    impact_severity="LOW"
                ),
                ScenarioBranch(
                    scenario_name="Scenario D: Exogenous Skirmish / Unmodeled Tactical Spillover (Residual)",
                    probability=0.05,
                    key_drivers=["Unplanned frontline encounter", "Asymmetric third-party border provocation"],
                    early_indicators=["Unplanned kinetic exchange", "Emergency security cabinet mobilization"],
                    impact_severity="CRITICAL"
                )
            ]
            forecasts = [
                CalibratedForecast(
                    target_hypothesis=f"Bilateral frontline commander protocols sustain patrol disengagement along border sectors without kinetic casualties throughout {year}",
                    forecast_probability=0.78,
                    confidence_interval_low=0.70,
                    confidence_interval_high=0.85,
                    time_horizon_months=12,
                    epistemic_basis="Backed by operational buffer zone agreements and bilateral military hotline mechanisms."
                ),
                CalibratedForecast(
                    target_hypothesis="Unilateral sovereign alteration of existing territorial control line through offensive conventional operation",
                    forecast_probability=0.04,
                    confidence_interval_low=0.01,
                    confidence_interval_high=0.08,
                    time_horizon_months=12,
                    epistemic_basis="Deterred by forward defense deployment depth and nuclear escalation thresholds."
                )
            ]
        elif event_type == "BORDER_SECURITY":
            observed = [
                "Sovereign border perimeter and maritime coastal surveillance radar operational.",
                "Frontex and border guard interdiction checkpoints active across designated sectors.",
                "Asymmetric migrant transit and irregular border crossings documented along coastal routes."
            ]
            inferred = [
                "Transit state leverages border flow interdiction as diplomatic bargaining leverage.",
                "Destination state domestic political polarization constrains unilateral deterrence options."
            ]
            scenarios = [
                ScenarioBranch(
                    scenario_name="Scenario A: Fortified Interdiction & Bilateral Repatriation Protocols (Baseline)",
                    probability=0.55,
                    key_drivers=["Joint maritime surveillance coordination", "Transit state security funding allocation"],
                    early_indicators=["Operational coastal interception agreements", "Decline in maritime transit vessels"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario B: Asymmetric Hybrid Infiltration Surge & Perimeter Saturation",
                    probability=0.30,
                    key_drivers=["Relaxation of transit country coastal enforcement", "Socio-economic crisis in origin regions"],
                    early_indicators=["Perimeter fence breaches", "Emergency reception center saturation"],
                    impact_severity="HIGH"
                ),
                ScenarioBranch(
                    scenario_name="Scenario C: Formal Bilateral Border Control Accord & Legal Transit Quota",
                    probability=0.10,
                    key_drivers=["Comprehensive bilateral diplomatic agreement", "EU-level mobility partnership ratification"],
                    early_indicators=["Treaty signing on migration management", "Co-located consular checkpoints"],
                    impact_severity="LOW"
                ),
                ScenarioBranch(
                    scenario_name="Scenario D: Sovereign Perimeter Breakdown / Unmodeled Humanitarian Shock (Residual)",
                    probability=0.05,
                    key_drivers=["Catastrophic transit zone collapse", "Unforeseen regional military conflict"],
                    early_indicators=["Mass perimeter storming", "Emergency martial border mobilization"],
                    impact_severity="CRITICAL"
                )
            ]
            forecasts = [
                CalibratedForecast(
                    target_hypothesis="Sovereign authorities execute bilateral coastal interdiction and repatriation protocols within 12 months",
                    forecast_probability=0.74,
                    confidence_interval_low=0.65,
                    confidence_interval_high=0.82,
                    time_horizon_months=12,
                    epistemic_basis="Backed by mutual bilateral security interests and EU Frontex surveillance funding."
                ),
                CalibratedForecast(
                    target_hypothesis="Complete unilateral demilitarization and unmonitored opening of sovereign border perimeter",
                    forecast_probability=0.02,
                    confidence_interval_low=0.00,
                    confidence_interval_high=0.05,
                    time_horizon_months=12,
                    epistemic_basis="Constitutional redlines and statutory national border laws prohibit unmonitored entry."
                )
            ]
        elif event_type == "GEO_ECONOMIC":
            observed = [
                "Bilateral local-currency clearing mechanisms and central bank currency swap lines active.",
                "Diversified central bank sovereign reserve asset allocations across gold and non-dollar instruments.",
                "US Dollar clearing dominates primary global commodities trade settlements."
            ]
            inferred = [
                "De-dollarization remains strictly bilateral and incremental; a supranational currency is structurally unviable.",
                "Secondary sanctions risks constrain commercial bank participation in non-SWIFT financial switches."
            ]
            scenarios = [
                ScenarioBranch(
                    scenario_name="Scenario A: Fragmented Local-Currency Clearance & Continued USD Hedging (Baseline)",
                    probability=0.60,
                    key_drivers=["Expansion of bilateral swap arrangements", "Preservation of Western financial linkages"],
                    early_indicators=["Growth in bilateral local-currency invoices", "Continued USD debt issuance"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario B: Secondary Sanctions Freezes & Liquidity Disruption",
                    probability=0.25,
                    key_drivers=["US OFAC enforcement on intermediary commercial banks", "Asset freezes in correspondent accounts"],
                    early_indicators=["Sudden cessation of trade credit facilities", "Foreign exchange liquidity squeezes"],
                    impact_severity="HIGH"
                ),
                ScenarioBranch(
                    scenario_name="Scenario C: Alternative Clearing Switch (CIPS/SPFS) Accelerated Adoption",
                    probability=0.10,
                    key_drivers=["Direct interconnectivity between national central bank RTGS systems", "Gold-backed commodity trade contracts"],
                    early_indicators=["Non-Western clearing switch volume surges", "Official reserve conversion to alternative currencies"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario D: Sovereign Debt Default Cascade / Unmodeled Financial Shock (Residual)",
                    probability=0.05,
                    key_drivers=["Global sovereign debt restructuring crisis", "Systemic banking contagion"],
                    early_indicators=["Sudden sovereign bond yields spike", "Emergency IMF liquidity requests"],
                    impact_severity="CRITICAL"
                )
            ]
            forecasts = [
                CalibratedForecast(
                    target_hypothesis="Bilateral non-SWIFT local-currency settlement volume expands by >20% across participating central banks in 12 months",
                    forecast_probability=0.80,
                    confidence_interval_low=0.72,
                    confidence_interval_high=0.88,
                    time_horizon_months=12,
                    epistemic_basis="Grounded in central bank currency swap lines and sanctions risk mitigation."
                ),
                CalibratedForecast(
                    target_hypothesis="Complete immediate replacement or collapse of US Dollar global reserve currency status within 12 months",
                    forecast_probability=0.01,
                    confidence_interval_low=0.00,
                    confidence_interval_high=0.03,
                    time_horizon_months=12,
                    epistemic_basis="Directly constrained by global capital account openness requirements and Mundell-Fleming Trilemma."
                )
            ]
        elif event_type == "HYBRID_WARFARE":
            observed = [
                "Multilateral sanctions, export control frameworks, and compliance lists (FATF/OFAC) enforced.",
                "Cross-border sovereign assets held across foreign custodial banking jurisdictions."
            ]
            inferred = [
                "Legal, regulatory, and economic institutions weaponized as primary instruments of non-kinetic coercion.",
                "Target states deploy multi-jurisdictional intermediary corporate architectures to maintain capital flows."
            ]
            scenarios = [
                ScenarioBranch(
                    scenario_name="Scenario A: Institutional Lawfare Impasse & Structured Compliance Hedging (Baseline)",
                    probability=0.55,
                    key_drivers=["Legal challenges in international arbitration tribunals", "Continued intermediary asset shielding"],
                    early_indicators=["Prolonged litigation in European courts", "Creation of offshore holding structures"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario B: Multilateral Secondary Sanctions Escalation & Sovereign Asset Confiscation",
                    probability=0.30,
                    key_drivers=["Statutory legislation mandating foreign sovereign asset transfer", "Expansion of extraterritorial penalties"],
                    early_indicators=["Direct seizure of central bank reserves", "Secondary blacklist designations"],
                    impact_severity="CRITICAL"
                ),
                ScenarioBranch(
                    scenario_name="Scenario C: Negotiated Diplomatic Compromise & Reciprocal De-listing",
                    probability=0.10,
                    key_drivers=["Strategic peace settlement framework", "Mutual economic concessions"],
                    early_indicators=["Temporary sanctions waivers issued", "Asset freeze thaw agreements"],
                    impact_severity="LOW"
                ),
                ScenarioBranch(
                    scenario_name="Scenario D: Critical Infrastructure Cyber Retaliation / Unmodeled Shock (Residual)",
                    probability=0.05,
                    key_drivers=["Asymmetric state-sponsored cyber warfare", "Sabotage of undersea cable communications"],
                    early_indicators=["Major clearing switch outages", "Severe maritime logistics disruption"],
                    impact_severity="CRITICAL"
                )
            ]
            forecasts = [
                CalibratedForecast(
                    target_hypothesis="Target sovereign entities maintain operational non-Western trade and escrow settlement channels without systemic banking insolvency throughout 12 months",
                    forecast_probability=0.76,
                    confidence_interval_low=0.68,
                    confidence_interval_high=0.84,
                    time_horizon_months=12,
                    epistemic_basis="Backed by operational alternative clearing corridors and institutional hedging."
                ),
                CalibratedForecast(
                    target_hypothesis="Unconditional immediate revocation of all multilateral asset freeze orders and sanctions within 12 months",
                    forecast_probability=0.03,
                    confidence_interval_low=0.01,
                    confidence_interval_high=0.06,
                    time_horizon_months=12,
                    epistemic_basis="Geopolitical inertia and statutory legislative barriers prevent rapid sanctions repeal."
                )
            ]
        elif event_type == "CIVILIZATIONAL_CRISIS":
            observed = [
                "Sovereign leadership engages in cross-civilizational spiritual, cultural, or existential protocol interaction.",
                "Intense theological and political perception management operations triggered across domestic and regional media.",
                "Core bilateral strategic channels (energy off-take, security coordination, trade transit) remain operational."
            ]
            inferred = [
                "Domestic clerical and political backlash is managed via selective state media framing, categorizing the event as diplomatic etiquette or host courtesy.",
                "Pragmatic statecraft (Apaddharma / Yogakshema) dictates that core economic and defense yields supersede symbolic theological polarization.",
                "Civilizational pluralism and sovereign autonomy cannot be subordinated to external ideological or moral coercion."
            ]
            scenarios = [
                ScenarioBranch(
                    scenario_name="Scenario A: Pragmatic Diplomatic Containment & De-escalation (Baseline)",
                    probability=0.62,
                    key_drivers=["Sovereign prioritization of energy and security accords", "Controlled state narrative emphasizing statecraft pragmatism"],
                    early_indicators=["Scheduled bilateral ministerial meetings proceed uninterrupted", "Absence of formal diplomatic reprimands"],
                    impact_severity="MEDIUM"
                ),
                ScenarioBranch(
                    scenario_name="Scenario B: Domestic Theological Backlash & Diplomatic Retraction",
                    probability=0.23,
                    key_drivers=["Clerical and hardline faction mobilization in home state", "State media issuing clarificatory disclaimers"],
                    early_indicators=["Official diplomatic communique asserting ideological redlines", "Temporary suspension of cultural exchanges"],
                    impact_severity="HIGH"
                ),
                ScenarioBranch(
                    scenario_name="Scenario C: Institutional Civilizational Detente Accord",
                    probability=0.10,
                    key_drivers=["Mutual recognition of civilizational statecraft traditions", "Bilateral code of conduct on spiritual/cultural respect"],
                    early_indicators=["Joint declaration acknowledging mutual civilizational respect", "Formal protocol harmonization guidelines"],
                    impact_severity="LOW"
                ),
                ScenarioBranch(
                    scenario_name="Scenario D: Sectarian Provocation / Unmodeled Radical Escalation (Residual)",
                    probability=0.05,
                    key_drivers=["Third-party extremist proxy mobilization", "Coordinated information warfare campaign on social platforms"],
                    early_indicators=["Violent street demonstrations outside diplomatic missions", "Emergency security cordons deployed"],
                    impact_severity="CRITICAL"
                )
            ]
            forecasts = [
                CalibratedForecast(
                    target_hypothesis="Bilateral diplomatic, energy, and infrastructure transit treaties remain legally and operationally intact within 12 months",
                    forecast_probability=0.84,
                    confidence_interval_low=0.76,
                    confidence_interval_high=0.90,
                    time_horizon_months=12,
                    epistemic_basis="Grounded in mutual economic necessity, energy trade continuity, and strategic transit corridors."
                ),
                CalibratedForecast(
                    target_hypothesis="Immediate unilateral severance of formal bilateral diplomatic ties triggered solely by the civilizational protocol incident",
                    forecast_probability=0.02,
                    confidence_interval_low=0.00,
                    confidence_interval_high=0.05,
                    time_horizon_months=12,
                    epistemic_basis="Directly deterred by core geopolitical equities, defense supply lines, and sovereign balance-of-payments interests."
                )
            ]
        else:
            observed = [
                "10 member states physically participating in summit institutional track.",
                "4.2M barrels/day of Russian crude actively diverted to Indian and Chinese refiners.",
                "Intra-bloc bilateral local-currency invoicing established across India-Russia and China-Russia corridors.",
                "Zero unified fiscal or supranational central banking apparatus exists within the bloc."
            ]

            inferred = [
                "India will maintain strict non-anti-Western posture, preventing the bloc from issuing an anti-Quad communique.",
                "China will leverage the summit to offload industrial clean-tech overcapacity into Global South partner markets.",
                "A unified 'BRICS common reserve currency' remains structurally impossible under the Mundell-Fleming Trilemma."
            ]

            if include_unmodeled:
                scenarios = [
                    ScenarioBranch(
                        scenario_name="Scenario A: Managed Polycentric Hedging (Baseline)",
                        probability=0.65,
                        key_drivers=[
                            "India and Brazil maintain multi-alignment and ties with Western capital markets.",
                            "Bilateral currency swaps expand without creating a supranational currency."
                        ],
                        early_indicators=[
                            "Continuation of current Indian border patrolling protocols.",
                            "No joint military exercises conducted under the BRICS banner."
                        ],
                        impact_severity="HIGH"
                    ),
                    ScenarioBranch(
                        scenario_name="Scenario B: Sinocentric Institutional Capture (Friction)",
                        probability=0.20,
                        key_drivers=[
                            "Beijing aggressively pushes CIPS as the sole alternative payment switch.",
                            "Russia accepts greater junior-partner subordination to Yuan hegemony."
                        ],
                        early_indicators=[
                            "Public Indian diplomatic dissent or reservation notes on summit communiques.",
                            "Expansion of Chinese non-performing debt renegotiations in African member states."
                        ],
                        impact_severity="CRITICAL"
                    ),
                    ScenarioBranch(
                        scenario_name="Scenario C: Western Secondary Sanctions Disruption (Decoupling)",
                        probability=0.10,
                        key_drivers=[
                            "US OFAC enforces direct secondary sanctions on tier-1 Indian, Chinese, and UAE commercial banks.",
                            "Western P&I maritime insurance clubs systematically intercept shadow fleet tankers."
                        ],
                        early_indicators=[
                            "Sudden freeze in Indian VOSTRO account remittances.",
                            "Sharp jump in Brent crude tanker freight risk premia."
                        ],
                        impact_severity="CRITICAL"
                    ),
                    ScenarioBranch(
                        scenario_name="Scenario D: Exogenous Sovereign Shock / Unmodeled Divergence (Residual)",
                        probability=0.05,
                        key_drivers=[
                            "Sudden domestic regime rupture in key member state.",
                            "Unmodeled geopolitical maritime kinetic escalation."
                        ],
                        early_indicators=[
                            "Emergency summit postponement or walkout.",
                            "Abrupt bilateral border closure."
                        ],
                        impact_severity="CRITICAL"
                    )
                ]
            else:
                scenarios = [
                    ScenarioBranch(
                        scenario_name="Scenario A: Managed Polycentric Hedging (Baseline)",
                        probability=0.68,
                        key_drivers=[
                            "India and Brazil maintain multi-alignment and ties with Western capital markets.",
                            "Bilateral currency swaps expand without creating a supranational currency."
                        ],
                        early_indicators=[
                            "Continuation of current Indian border patrolling protocols.",
                            "No joint military exercises conducted under the BRICS banner."
                        ],
                        impact_severity="HIGH"
                    ),
                    ScenarioBranch(
                        scenario_name="Scenario B: Sinocentric Institutional Capture (Friction)",
                        probability=0.22,
                        key_drivers=[
                            "Beijing aggressively pushes CIPS as the sole alternative payment switch.",
                            "Russia accepts greater junior-partner subordination to Yuan hegemony."
                        ],
                        early_indicators=[
                            "Public Indian diplomatic dissent or reservation notes on summit communiques.",
                            "Expansion of Chinese non-performing debt renegotiations in African member states."
                        ],
                        impact_severity="CRITICAL"
                    ),
                    ScenarioBranch(
                        scenario_name="Scenario C: Western Secondary Sanctions Disruption (Decoupling)",
                        probability=0.10,
                        key_drivers=[
                            "US OFAC enforces direct secondary sanctions on tier-1 Indian, Chinese, and UAE commercial banks.",
                            "Western P&I maritime insurance clubs systematically intercept shadow fleet tankers."
                        ],
                        early_indicators=[
                            "Sudden freeze in Indian VOSTRO account remittances.",
                            "Sharp jump in Brent crude tanker freight risk premia."
                        ],
                        impact_severity="CRITICAL"
                    )
                ]

            forecasts = [
                CalibratedForecast(
                    target_hypothesis="BRICS expands bilateral local currency clearing volume by >20% within 12 months without adopting a unified currency",
                    forecast_probability=0.82,
                    confidence_interval_low=0.74,
                    confidence_interval_high=0.89,
                    time_horizon_months=12,
                    epistemic_basis="Backed by operational central bank bilateral swap lines and Mundell-Fleming constraints."
                ),
                CalibratedForecast(
                    target_hypothesis="India formally ratifies an anti-Western collective security clause in the summit declaration",
                    forecast_probability=0.03,
                    confidence_interval_low=0.01,
                    confidence_interval_high=0.06,
                    time_horizon_months=12,
                    epistemic_basis="Directly contradicts India's constitutional and historical doctrine of strategic autonomy (Panchsheel / Vishwamitra)."
                )
            ]

        # Persist forecasts to SQLite ledger
        try:
            import hashlib
            from datetime import timedelta
            from ..storage.event_store import EventStore
            store = EventStore()
            created_dt = get_system_reference_date()
            for fc in forecasts:
                # Deterministic SHA-256 forecast ID (stable across process restarts)
                id_seed = f"{year}:{fc.target_hypothesis}"
                hypo_hash = hashlib.sha256(id_seed.encode("utf-8")).hexdigest()[:8]
                fc_id = f"FCST-{year}-{hypo_hash}"
                # Dynamically calculate target date based on forecast horizon months
                target_dt = created_dt + timedelta(days=fc.time_horizon_months * 30)
                store.record_forecast({
                    "forecast_id": fc_id,
                    "created_at": created_dt.isoformat(),
                    "target_date": target_dt.strftime("%Y-%m-%d"),
                    "event_name": summit_name,
                    "hypothesis": fc.target_hypothesis,
                    "predicted_probability": fc.forecast_probability,
                    "confidence_interval_low": fc.confidence_interval_low,
                    "confidence_interval_high": fc.confidence_interval_high,
                    "epistemic_basis": fc.epistemic_basis,
                    "status": "ACTIVE"
                })
        except Exception as e:
            import sys
            print(f"[WARNING] Failed to persist forecast to SQLite ledger: {e}", file=sys.stderr)

        return EpistemicStrata(
            observed_facts=observed,
            inferred_realities=inferred,
            scenario_branches=scenarios,
            calibrated_forecasts=forecasts
        )

    @classmethod
    def resolve_forecast_with_bayesian_update(
        cls,
        forecast_id: str,
        actual_outcome: int,
        contributing_lenses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Resolves a forecast, calculates Brier score, and backpropagates error
        to update persistent epistemic reliability multipliers for contributing lenses.
        """
        from ..storage.event_store import EventStore
        store = EventStore()
        brier = store.resolve_forecast(forecast_id, actual_outcome)

        updated_multipliers = {}
        target_lenses = contributing_lenses or [
            "GeoEconomistLens", "GeopoliticalLens", "DeepTechLens", "CashFlowLens"
        ]
        for lname in target_lenses:
            mult = store.update_lens_reliability(lname, brier)
            updated_multipliers[lname] = mult

        return {
            "forecast_id": forecast_id,
            "actual_outcome": actual_outcome,
            "brier_score": brier,
            "updated_multipliers": updated_multipliers
        }

    @classmethod
    def compute_longitudinal_brier_from_store(
        cls,
        event_store: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Phase 86: Computes the longitudinal Brier calibration score by querying the
        resolved forecast records in the SQLite forecast_ledger table.
        Bridges the episodic in-memory forecasting engine to historical longitudinal ground truth.
        """
        if event_store is None:
            try:
                from ..storage.event_store import EventStore
                event_store = EventStore()
            except Exception:
                pass

        if event_store is None:
            return {
                "status": "STORE_UNAVAILABLE",
                "total_resolved_forecasts": 0,
                "longitudinal_brier_score": 0.11,
                "epistemic_calibration_grade": "EPISODIC_DEFAULT",
                "calibration_records": []
            }

        records = event_store.get_forecast_ledger(status="RESOLVED")
        if not records:
            all_records = event_store.get_forecast_ledger()
            records = [r for r in all_records if r.get("actual_outcome") is not None]

        if not records:
            return {
                "status": "NO_RESOLVED_RECORDS",
                "total_resolved_forecasts": 0,
                "longitudinal_brier_score": 0.11,
                "epistemic_calibration_grade": "EPISODIC_HEURISTIC",
                "calibration_records": []
            }

        probs = [float(r["predicted_probability"]) for r in records]
        outcomes = [int(r["actual_outcome"]) for r in records]
        bs = BrierScorer.calculate_brier_score(probs, outcomes)

        if bs <= 0.10:
            grade = "WORLD_CLASS_EXEMPLARY"
        elif bs <= 0.15:
            grade = "SUPERIOR_CALIBRATION"
        elif bs <= 0.22:
            grade = "MODERATE_RELIABILITY"
        else:
            grade = "OVERCONFIDENCE_DEGRADED"

        return {
            "status": "LONGITUDINAL_CALIBRATED",
            "total_resolved_forecasts": len(records),
            "longitudinal_brier_score": bs,
            "epistemic_calibration_grade": grade,
            "mean_predicted_probability": round(sum(probs) / len(probs), 4),
            "empirical_base_rate": round(sum(outcomes) / len(outcomes), 4),
            "calibration_records": [
                {
                    "forecast_id": r.get("forecast_id"),
                    "hypothesis": r.get("hypothesis", "")[:80],
                    "predicted_probability": r.get("predicted_probability"),
                    "actual_outcome": r.get("actual_outcome"),
                    "brier_score": r.get("brier_score")
                }
                for r in records[:10]
            ]
        }




```

## Module: `geo_engine/forecasting/resolution_daemon.py`

```python
"""
Automated Prospective Forecast Resolution Daemon.
Monitors the persistent forecast ledger in EventStore, evaluates elapsed forecasts
against empirical ground truth, and computes calibrated Brier scores deterministically.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from ..core.models import get_system_reference_date
from ..storage.event_store import EventStore


class ForecastResolutionDaemon:
    """
    Autonomous evaluation engine for forward-looking probabilistic projections.
    Scans active forecast entries, evaluates target dates against system clocks,
    and resolves outcomes with rigorous Brier calibration.
    """

    @classmethod
    def get_reference_date_str(cls, override_date: Optional[str] = None) -> str:
        """Resolves the active reference date string (YYYY-MM-DD)."""
        if override_date:
            return str(override_date).strip()[:10]
        ref = get_system_reference_date()
        if isinstance(ref, datetime):
            return ref.strftime("%Y-%m-%d")
        return str(ref)[:10]

    @classmethod
    def check_elapsed_forecasts(
        cls,
        store: EventStore,
        current_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves all ACTIVE forecast records whose target_date has arrived or passed.
        """
        ref_date = cls.get_reference_date_str(current_date)
        active_forecasts = store.get_forecast_ledger(status="ACTIVE")
        elapsed = []

        for fc in active_forecasts:
            target_str = str(fc.get("target_date", "")).strip()[:10]
            if target_str and target_str <= ref_date:
                elapsed.append(fc)

        return elapsed

    @classmethod
    def auto_resolve_elapsed(
        cls,
        store: EventStore,
        ground_truth_map: Optional[Dict[str, int]] = None,
        current_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Resolves elapsed forecasts matching provided ground truth binary outcomes (0 or 1).
        Updates database status to 'RESOLVED' and computes Brier score (predicted - actual)^2.
        """
        gt_map = ground_truth_map or {}
        elapsed = cls.check_elapsed_forecasts(store, current_date=current_date)
        resolved_records = []
        brier_scores = []
        unresolved = []

        for fc in elapsed:
            fid = fc["forecast_id"]
            if fid in gt_map:
                outcome = int(gt_map[fid])
                if outcome not in (0, 1):
                    outcome = 1 if outcome > 0 else 0
                brier = store.resolve_forecast(fid, outcome)
                brier_scores.append(brier)
                resolved_records.append({
                    "forecast_id": fid,
                    "event_name": fc.get("event_name", ""),
                    "hypothesis": fc.get("hypothesis", ""),
                    "predicted_probability": fc.get("predicted_probability", 0.5),
                    "actual_outcome": outcome,
                    "brier_score": brier
                })
            else:
                unresolved.append(fid)

        mean_brier = round(sum(brier_scores) / len(brier_scores), 4) if brier_scores else None

        return {
            "elapsed_count": len(elapsed),
            "resolved_count": len(resolved_records),
            "unresolved_count": len(unresolved),
            "resolved_records": resolved_records,
            "mean_brier_score": mean_brier,
            "unresolved_forecast_ids": unresolved
        }

    @classmethod
    def get_ledger_calibration_summary(cls, store: EventStore) -> Dict[str, Any]:
        """
        Computes aggregate statistical calibration metrics across all records in the ledger.
        """
        all_records = store.get_forecast_ledger()
        total_count = len(all_records)
        active_count = sum(1 for r in all_records if r.get("status") == "ACTIVE")
        resolved_records = [r for r in all_records if r.get("status") == "RESOLVED" and r.get("brier_score") is not None]
        resolved_count = len(resolved_records)

        if not resolved_records:
            return {
                "total_forecasts": total_count,
                "active_forecasts": active_count,
                "resolved_forecasts": 0,
                "mean_brier_score": None,
                "calibration_grade": "INSUFFICIENT_RESOLVED_DATA",
                "best_forecast": None,
                "worst_forecast": None
            }

        brier_values = [float(r["brier_score"]) for r in resolved_records]
        mean_brier = round(sum(brier_values) / len(brier_values), 4)

        # Grade calibration: 0.0 - 0.10: Exceptional, 0.10 - 0.20: Strong, 0.20 - 0.25: Neutral, > 0.25: Degraded
        if mean_brier <= 0.10:
            grade = "EXCEPTIONAL_CALIBRATION"
        elif mean_brier <= 0.20:
            grade = "STRONG_PREDICTIVE_CALIBRATION"
        elif mean_brier <= 0.25:
            grade = "BASELINE_RANDOM_BOUNDARY"
        else:
            grade = "SUB_OPTIMAL_CALIBRATION"

        sorted_records = sorted(resolved_records, key=lambda x: float(x["brier_score"]))
        best_fc = sorted_records[0]
        worst_fc = sorted_records[-1]

        return {
            "total_forecasts": total_count,
            "active_forecasts": active_count,
            "resolved_forecasts": resolved_count,
            "mean_brier_score": mean_brier,
            "calibration_grade": grade,
            "best_forecast": {
                "forecast_id": best_fc["forecast_id"],
                "hypothesis": best_fc["hypothesis"],
                "brier_score": best_fc["brier_score"]
            },
            "worst_forecast": {
                "forecast_id": worst_fc["forecast_id"],
                "hypothesis": worst_fc["hypothesis"],
                "brier_score": worst_fc["brier_score"]
            }
        }

```

## Module: `geo_engine/mcp/__init__.py`

```python
"""
Model Context Protocol (MCP) Server for Geo-Engine.
Enables external LLM agents to invoke live engine capabilities via standard JSON-RPC 2.0 over stdio.
"""

from .server import GeoEngineMCPServer, run_stdio_server

__all__ = ["GeoEngineMCPServer", "run_stdio_server"]

```

## Module: `geo_engine/mcp/server.py`

```python
"""
JSON-RPC 2.0 Model Context Protocol (MCP) Server for Geo-Engine.
Implements stdio protocol for tools/list and tools/call, bridging external LLMs
(Claude Desktop, Cursor, Gemini CLI, NotebookLM sidecars) directly to the live engine.
"""

import sys
import json
from typing import Any, Dict, List, Optional

from ..core.models import SummitEvent
from ..core.query_parser import QueryParser
from ..arbitration.synthesizer import SummitSynthesizer
from ..arbitration.persona_narrator import PersonaNarrator
from ..simulation.cascading_engine import CascadingSimulationEngine, SimulationShock
from ..simulation.game_theoretic import GameTheoreticEngine
from ..storage.event_store import EventStore
from ..lenses import LENS_REGISTRY
from ..lenses.geo_economist import GeoEconomistLens
from ..ingestion.telemetry_adapter import MacroTelemetryAdapter


class GeoEngineMCPServer:
    """Zero-dependency JSON-RPC 2.0 MCP server executing live geo_engine tools."""

    PROTOCOL_VERSION = "2024-11-05"
    SERVER_NAME = "geo-engine-mcp"
    SERVER_VERSION = "0.1.0"

    TOOLS_MANIFEST = [
        {
            "name": "geo_query",
            "description": "Run full 20-lens forensic geopolitical and geoeconomic analysis on an event or prompt.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The strategic query or event description to analyze."
                    },
                    "persona": {
                        "type": "string",
                        "enum": list(PersonaNarrator.ARCHETYPES.keys()),
                        "default": "neutral",
                        "description": "Strategic persona projection tradition to apply."
                    }
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "geo_simulate",
            "description": "Simulate multi-order cascading shock propagation across 20 analytical lenses with non-linear tipping points.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Domain of the initial shock (e.g., petro_logistics, critical_minerals, subsea_cables)."
                    },
                    "severity": {
                        "type": "number",
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "description": "Shock severity magnitude between 0.0 and 1.0."
                    },
                    "description": {
                        "type": "string",
                        "description": "Textual context and parameters of the shock."
                    }
                },
                "required": ["domain", "severity", "description"]
            }
        },
        {
            "name": "geo_red_team",
            "description": "Run 3-turn sequential game-theoretic strategic interaction (Action, Asymmetric Reaction, Domestic Backlash).",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "initiator": {"type": "string", "description": "Initiating state actor (e.g., China, USA)."},
                    "target": {"type": "string", "description": "Target state actor (e.g., India)."},
                    "domain": {"type": "string", "description": "Strategic domain of confrontation."},
                    "severity": {"type": "number", "minimum": 0.0, "maximum": 1.0, "description": "Severity of opening move."},
                    "action": {"type": "string", "description": "Description of initiating move."},
                    "intent": {"type": "string", "default": "", "description": "Declared intent."}
                },
                "required": ["initiator", "target", "domain", "severity", "action"]
            }
        },
        {
            "name": "geo_forecasts",
            "description": "Query calibrated forecasts and Brier score validation records from the SQLite ledger.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["ALL", "ACTIVE", "RESOLVED"],
                        "default": "ALL",
                        "description": "Filter forecasts by status."
                    }
                }
            }
        },
        {
            "name": "geo_lenses",
            "description": "Inspect the 20 analytical lenses, their primary epistemic tiers, and persona weights.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "persona": {
                        "type": "string",
                        "enum": list(PersonaNarrator.ARCHETYPES.keys()),
                        "default": "neutral",
                        "description": "Persona tradition to retrieve weight multipliers for."
                    }
                }
            }
        },
        {
            "name": "geo_ingest_audit",
            "description": "Ingest structured macroeconomic and geopolitical audit findings into SQLite EventStore.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "default": "FORENSIC_AUDIT_INDIA_1991_2026.md",
                        "description": "File path to the markdown audit document."
                    }
                }
            }
        },
        {
            "name": "geo_recalculate_deflation",
            "description": "Compute double-deflated vs single-deflated manufacturing GVA and calculate the statistical distortion divergence percentage.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "nominal_output": {"type": "number", "description": "Nominal value of gross manufacturing output."},
                    "output_deflator": {"type": "number", "description": "Deflator index for gross output (e.g., 1.02 for 2% inflation)."},
                    "nominal_input": {"type": "number", "description": "Nominal value of intermediate inputs consumed."},
                    "input_deflator": {"type": "number", "description": "Deflator index for inputs (e.g., 0.95 for 5% input deflation)."}
                },
                "required": ["nominal_output", "output_deflator", "nominal_input", "input_deflator"]
            }
        },
        {
            "name": "geo_ingest_media",
            "description": "Extract captions/transcript and ingest verified claims from a YouTube or media URL.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "YouTube or media stream URL to ingest."
                    },
                    "target_lenses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of lenses to tag the extracted claims with."
                    }
                },
                "required": ["url"]
            }
        },
        {
            "name": "geo_arbitrate_chronology",
            "description": "Arbitrate conflicting ancient historical timelines and civilizational claims across 4 orthogonal pillars (Astronomy, Archaeology/C-14, Hydro-Geology/Saraswati, Textual/BORI).",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "event_name": {
                        "type": "string",
                        "default": "Mahabharata War Chronology",
                        "description": "Historical event to arbitrate (e.g., 'Mahabharata War Chronology', 'Ramayana Epoch')."
                    }
                }
            }
        },
        {
            "name": "geo_export_report",
            "description": "Export an intelligence report into interactive HTML dashboard, forensic Markdown, and publication-grade PDF with multilingual audio controls.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "event_name": {
                        "type": "string",
                        "default": "BRICS 2026 Summit",
                        "description": "Strategic event or summit to synthesize and export."
                    },
                    "formats": {
                        "type": "array",
                        "items": {"type": "string"},
                        "default": ["html", "md", "pdf"],
                        "description": "Formats to export ('html', 'md', 'pdf')."
                    },
                    "persona": {
                        "type": "string",
                        "default": "neutral",
                        "description": "Strategic persona projection tradition."
                    },
                    "output_dir": {
                        "type": "string",
                        "default": "reports",
                        "description": "Directory where exported files will be written."
                    }
                }
            }
        },
        {
            "name": "geo_learn_conversation",
            "description": "Distill an analytical conversation, Q&A exchange, or audit conclusion into structured ClaimItems and persist them to EventStore long-term memory.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "conversation_text": {
                        "type": "string",
                        "description": "The raw conversation text, analytical summary, or audit conclusion to learn from."
                    },
                    "session_id": {
                        "type": "string",
                        "default": "mcp_chat_learning",
                        "description": "Unique session identifier for the encounter."
                    },
                    "entity_or_subject": {
                        "type": "string",
                        "description": "Optional focal entity or subject (e.g., 'Sinauli Necropolis', 'Galwan Standoff')."
                    },
                    "parent_encounter_id": {
                        "type": "string",
                        "description": "Optional parent encounter ID (e.g., 'ENC-...') for multi-turn longitudinal encounter chaining."
                    }
                },
                "required": ["conversation_text"]
            }
        },
        {
            "name": "geo_verify_evidence",
            "description": "Run Evidence Intelligence & Fact Verification Engine to audit claims, detect statistical manipulation, verify against statutory baselines, and assign one of the 7 formal verdicts.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The statement, claim, speech excerpt, or article to verify."
                    }
                },
                "required": ["text"]
            }
        },
        {
            "name": "geo_quantum_evaluation",
            "description": "Evaluate quantum information statecraft: multi-vector alignment superposition, Shannon entropy, collapse thresholds, observer disturbance, and Post-Quantum Cryptography (PQC) vulnerability.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "statement": {"type": "string", "default": "Multi-vector strategic alignment", "description": "Scenario statement to evaluate."},
                    "c_west": {"type": "number", "default": 0.45, "description": "Western alignment amplitude."},
                    "c_eurasia": {"type": "number", "default": 0.55, "description": "Eurasian alignment amplitude."},
                    "c_south": {"type": "number", "default": 0.70, "description": "Global South alignment amplitude."},
                    "kinetic_escalation_score": {"type": "number", "default": 0.20, "description": "Kinetic or sanctions escalation score (0.0 to 1.0)."},
                    "collapse_threshold": {"type": "number", "default": 0.75, "description": "Superposition collapse threshold."}
                }
            }
        },
        {
            "name": "geo_chokepoint_sensitivity",
            "description": "Quantify macroeconomic crude oil price shocks (CAD, CPI, OMC under-recoveries) and agrarian nutrient chokepoint vulnerabilities.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "crude_shock_usd": {"type": "number", "default": 20.0, "description": "Brent crude price shock in USD/bbl."},
                    "red_sea_blocked": {"type": "boolean", "default": False, "description": "Whether Red Sea / Bab-el-Mandeb transit is interdicted."},
                    "hormuz_risk": {"type": "number", "default": 0.30, "description": "Strait of Hormuz risk factor (0.0 to 1.0)."},
                    "buffer_months": {"type": "number", "default": 2.5, "description": "Domestic fertilizer buffer stocks in months."}
                }
            }
        },
        {
            "name": "geo_quarantine_learn",
            "description": "Execute governed autonomous safe learning: extract propositions, quarantine in SQLite, cross-verify against EIFVE, and safely promote without codebase mutation.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to ingest, extract propositions, and learn from."},
                    "source": {"type": "string", "default": "MCP Ingestion", "description": "Source provenance identifier."},
                    "auto_promote": {"type": "boolean", "default": True, "description": "Auto-promote high-confidence verified claims."}
                },
                "required": ["text"]
            }
        }
    ]


    def __init__(self, store: Optional[EventStore] = None):
        self.store = store or EventStore()

    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processes a single JSON-RPC 2.0 request dict and returns the response dict."""
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        # Handle notifications (no id)
        if req_id is None and method == "notifications/initialized":
            return None

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": self.PROTOCOL_VERSION,
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": self.SERVER_NAME,
                        "version": self.SERVER_VERSION
                    }
                }
            }

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": self.TOOLS_MANIFEST
                }
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            try:
                result_content = self.execute_tool(tool_name, arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result_content, indent=2, default=str)
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32000,
                        "message": f"Tool execution failed: {str(e)}"
                    }
                }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Executes the specified tool with arguments and returns structured Python objects."""
        if tool_name == "geo_query":
            prompt = arguments.get("prompt", "")
            persona = arguments.get("persona", "neutral")
            parsed_query = QueryParser.parse(prompt)
            target_countries = parsed_query.target_countries if parsed_query.target_countries else [
                "India", "China", "Russia"
            ]
            host_c = parsed_query.target_countries[0] if parsed_query.target_countries else "India"
            target_event = SummitEvent(
                summit_name=parsed_query.target_summit,
                year=parsed_query.year,
                event_type=parsed_query.event_type,
                host_country=host_c,
                location=host_c,
                member_countries=target_countries,
                focal_date=parsed_query.focal_date
            )
            report = SummitSynthesizer.synthesize_report(
                summit=target_event,
                prioritized_lenses=parsed_query.prioritized_lenses,
                fixture_mode=bool(arguments.get("fixture_mode", True)),
            )
            persona_view = PersonaNarrator.apply_persona(report, persona_key=persona)
            return {
                "query": prompt,
                "event_type": str(target_event.event_type),
                "prioritized_lenses": parsed_query.prioritized_lenses,
                "overall_confidence": report.overall_confidence_score,
                "persona": persona,
                "country_ledgers_count": len(report.country_ledgers),
                "negative_space_omissions": report.negative_space_synopsis,
                "civilizational_synthesis": persona_view.get("synthesized_text", ""),
                "key_findings": [f for l in report.lens_evaluations[:2] for f in l.key_findings[:2]]
            }

        elif tool_name == "geo_simulate":
            domain = arguments["domain"]
            severity = float(arguments["severity"])
            description = arguments["description"]
            shock = SimulationShock(
                shock_id=f"MCP-{domain.upper()}",
                domain=domain,
                severity=severity,
                description=description,
            )
            result = CascadingSimulationEngine.simulate_shock(shock)
            return {
                "domain": result.shock.domain,
                "severity": result.shock.severity,
                "systemic_vulnerability_index": result.systemic_vulnerability_index,
                "is_tipping_point": result.systemic_phase_transition_risk,
                "critical_resilience_deficit": result.critical_tipping_lenses,
                "order_1_impacts": [i.model_dump() for i in result.order_1_impacts],
                "order_2_impacts": [i.model_dump() for i in result.order_2_impacts],
                "order_3_impacts": [i.model_dump() for i in result.order_3_impacts],
                "strategic_hedges": result.recommended_mitigations,
            }

        elif tool_name == "geo_red_team":
            initiator = arguments["initiator"]
            target = arguments["target"]
            domain = arguments["domain"]
            severity = float(arguments["severity"])
            action = arguments["action"]
            intent = arguments.get("intent", "")
            interaction = GameTheoreticEngine.simulate_interaction(
                initiator_name=initiator,
                target_name=target,
                domain=domain,
                severity=severity,
                action_description=action,
                intent=intent,
            )
            return interaction.model_dump()

        elif tool_name == "geo_forecasts":
            status_filter = arguments.get("status", "ALL")
            status = None if status_filter == "ALL" else status_filter
            records = self.store.get_forecast_ledger(status=status)
            return {
                "status_filter": status_filter,
                "count": len(records),
                "forecasts": records
            }

        elif tool_name == "geo_lenses":
            persona = arguments.get("persona", "neutral")
            archetype = PersonaNarrator.ARCHETYPES.get(persona, PersonaNarrator.ARCHETYPES["neutral"])
            lenses_meta = []
            for name, lens_cls in LENS_REGISTRY.items():
                lenses_meta.append({
                    "registry_key": name,
                    "lens_name": getattr(lens_cls, "LENS_NAME", name),
                    "primary_tier": getattr(lens_cls, "PRIMARY_TIER", 1).name,
                    "persona_weight": archetype.get("lens_weights", {}).get(name, 1.0)
                })
            return {
                "persona": persona,
                "persona_description": archetype.get("description", ""),
                "lens_count": len(lenses_meta),
                "lenses": lenses_meta
            }

        elif tool_name == "geo_ingest_audit":
            path = arguments.get("path", "FORENSIC_AUDIT_INDIA_1991_2026.md")
            claims = MacroTelemetryAdapter.extract_claims_from_audit_markdown(path)
            for claim in claims:
                self.store.record_claim(claim)
            return {
                "status": "SUCCESS",
                "source_file": path,
                "claims_ingested": len(claims),
                "message": f"Successfully ingested {len(claims)} verified claims into SQLite events.db"
            }

        elif tool_name == "geo_recalculate_deflation":
            output_nom = float(arguments["nominal_output"])
            output_def = float(arguments["output_deflator"])
            input_nom = float(arguments["nominal_input"])
            input_def = float(arguments["input_deflator"])
            res = GeoEconomistLens.calculate_double_deflated_gva(
                nominal_output=output_nom,
                output_deflator=output_def,
                nominal_input=input_nom,
                input_deflator=input_def
            )
            return res

        elif tool_name == "geo_ingest_media":
            from ..video import AudioStreamConnector
            url = str(arguments["url"])
            target_lenses = arguments.get("target_lenses")
            res = AudioStreamConnector.ingest_media_url(
                url_or_id=url,
                store=self.store,
                target_lenses=target_lenses
            )
            return res

        elif tool_name == "geo_arbitrate_chronology":
            from ..arbitration.historical_arbiter import MultiPillarChronologyArbiter
            event_name = arguments.get("event_name", "Mahabharata War Chronology")
            report = MultiPillarChronologyArbiter.arbitrate(event_name=event_name)
            return report.to_dict()

        elif tool_name == "geo_export_report":
            event_name = arguments.get("event_name", "BRICS 2026 Summit")
            formats = arguments.get("formats", ["html", "md", "pdf"])
            persona = arguments.get("persona", "neutral")
            output_dir = arguments.get("output_dir", "reports")
            summit = SummitEvent(summit_name=event_name, year=2026)
            report, files = SummitSynthesizer.synthesize_and_export(
                summit,
                export_formats=formats,
                output_dir=output_dir,
                persona=persona
            )
            return {
                "status": "SUCCESS",
                "event_name": event_name,
                "exported_files": files,
                "confidence": round(report.overall_confidence_score * 100, 1)
            }

        elif tool_name == "geo_learn_conversation":
            from ..ingestion.chat_distiller import ChatConversationDistiller
            conversation_text = arguments.get("conversation_text", "")
            session_id = arguments.get("session_id", "mcp_chat_learning")
            entity_or_subject = arguments.get("entity_or_subject")
            parent_encounter_id = arguments.get("parent_encounter_id")
            res = ChatConversationDistiller.distill_and_persist(
                conversation_text=conversation_text,
                session_id=session_id,
                store=self.store,
                entity_or_subject=entity_or_subject,
                parent_encounter_id=parent_encounter_id
            )
            return res

        elif tool_name == "geo_verify_evidence":
            from ..verification import FactVerificationEngine
            text = arguments.get("text", "")
            engine = FactVerificationEngine(self.store)
            report = engine.verify_text(text)
            return report.model_dump()

        elif tool_name == "geo_quantum_evaluation":
            from ..lenses.deep_tech import QuantumInformationSieve
            statement = arguments.get("statement", "Multi-vector strategic alignment")
            c_west = float(arguments.get("c_west", 0.45))
            c_eurasia = float(arguments.get("c_eurasia", 0.55))
            c_south = float(arguments.get("c_south", 0.70))
            k_score = float(arguments.get("kinetic_escalation_score", 0.20))
            thresh = float(arguments.get("collapse_threshold", 0.75))
            diag = QuantumInformationSieve.calculate_geopolitical_superposition(
                c_west=c_west,
                c_eurasia=c_eurasia,
                c_south=c_south,
                kinetic_escalation_score=k_score,
                collapse_threshold=thresh,
            )
            pqc = QuantumInformationSieve.evaluate_pqc_sovereignty()
            obs = QuantumInformationSieve.calculate_channel_observer_disturbance()
            return {
                "statement": statement,
                "superposition": diag,
                "pqc_sovereignty": pqc,
                "observer_disturbance": obs,
            }

        elif tool_name == "geo_chokepoint_sensitivity":
            from ..lenses.food_security import EnergyFertilizerChokepointSieve
            crude_shock = float(arguments.get("crude_shock_usd", 20.0))
            red_sea = bool(arguments.get("red_sea_blocked", False))
            hormuz = float(arguments.get("hormuz_risk", 0.30))
            buffer_m = float(arguments.get("buffer_months", 2.5))
            macro = EnergyFertilizerChokepointSieve.calculate_energy_macro_sensitivity(
                brent_price_shock_usd=crude_shock
            )
            nutrient = EnergyFertilizerChokepointSieve.calculate_nutrient_chokepoint_vulnerability(
                red_sea_bab_el_mandeb_blocked=red_sea,
                strait_of_hormuz_risk_factor=hormuz,
                domestic_soil_nutrient_buffer_months=buffer_m,
            )
            return {
                "crude_macro_sensitivity": macro,
                "nutrient_chokepoint_vulnerability": nutrient,
            }

        elif tool_name == "geo_quarantine_learn":
            from ..verification.learner import AutonomousLearner
            text = arguments.get("text", "")
            source = arguments.get("source", "MCP Ingestion")
            auto_promote = bool(arguments.get("auto_promote", True))
            learner = AutonomousLearner()
            res = learner.learn_from_text(
                raw_text=text,
                source_name=source,
                auto_promote=auto_promote,
            )
            return res

        else:
            raise ValueError(f"Unknown tool: {tool_name}")



def run_stdio_server():
    """Runs the MCP server over standard input and standard output."""
    server = GeoEngineMCPServer()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = server.handle_request(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

```
