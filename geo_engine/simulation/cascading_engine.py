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
    recommended_mitigations: List[str] = Field(default_factory=list)
    timestamp: str = ""

    def to_markdown(self) -> str:
        lines = [
            f"# Cascading Shock Simulation: {self.shock.shock_id}",
            f"- **Shock Domain:** `{self.shock.domain}` | **Initial Severity:** `{self.shock.severity:.2f}`",
            f"- **Description:** {self.shock.description}",
            f"- **Systemic Vulnerability Index:** `{self.systemic_vulnerability_index:.2f}`",
            f"- **Simulation Timestamp:** `{self.timestamp}`",
            "",
            "## Order 1: Direct Physical & Strategic Impacts",
        ]
        for imp in self.order_1_impacts:
            status = " [Mitigated by Resilience]" if imp.mitigated_by_resilience else ""
            lines.append(f"- **Lens `{imp.lens}`** (Impact: `{imp.impact_score:.2f}`){status}: {imp.mechanism}")
            if imp.recommendation:
                lines.append(f"  - *Action:* {imp.recommendation}")

        lines.extend(["", "## Order 2: Secondary Macro & Supply Contagion"])
        for imp in self.order_2_impacts:
            status = " [Mitigated by Resilience]" if imp.mitigated_by_resilience else ""
            lines.append(f"- **Lens `{imp.lens}`** (Impact: `{imp.impact_score:.2f}`){status}: {imp.mechanism}")
            if imp.recommendation:
                lines.append(f"  - *Action:* {imp.recommendation}")

        lines.extend(["", "## Order 3: Tertiary Geopolitical & Civilizational Realignment"])
        for imp in self.order_3_impacts:
            status = " [Mitigated by Resilience]" if imp.mitigated_by_resilience else ""
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

                # Resilience dampening
                mitigated = False
                resilience_val = 0.5  # default baseline resilience
                if resilience_matrix and lens in resilience_matrix:
                    resilience_val = float(resilience_matrix[lens])
                    # Higher resilience dampens impact: up to 50% reduction
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

        # Calculate systemic vulnerability index
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
            recommended_mitigations=unique_recs[:5],
            timestamp=ref_time
        )
