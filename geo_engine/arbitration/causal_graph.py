"""
Epistemic Knowledge Graph & Multi-Hop Causal Inference Engine.
Models first-, second-, and third-order systemic ripple effects across maritime chokepoints,
macro-monetary flows, strategic mineral embargos, and historical colonial stratigraphy.
"""

from typing import Dict, List, Optional, Any, Set
from pydantic import BaseModel, Field


class CausalNode(BaseModel):
    """Represents an epistemic node within the causal graph."""
    node_id: str
    name: str
    category: str  # CHOKEPOINT, CURRENCY, SEMICONDUCTOR, COLONIAL_LEGAL, NAVAL_ATTRITION, etc.
    epistemic_tier: int = Field(default=1, ge=1, le=5)
    base_potency: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CausalEdge(BaseModel):
    """Represents a directed causal dependency link between two nodes."""
    source_id: str
    target_id: str
    coupling_weight: float = Field(default=0.5, ge=-1.0, le=1.0)
    latency_tier: str = Field(default="MEDIUM_TERM")  # IMMEDIATE, MEDIUM_TERM, STRUCTURAL_LONG_TERM
    mechanism: str = Field(default="")


class CausalPath(BaseModel):
    """Represents an end-to-end multi-hop causal trajectory."""
    source_id: str
    target_id: str
    path_nodes: List[str]
    edges: List[CausalEdge]
    hop_count: int
    net_attenuation: float
    cumulative_impact: float
    net_polarity: int  # +1 or -1


class EpistemicKnowledgeGraph:
    """
    Zero-dependency directed acyclic epistemic knowledge graph
    enabling multi-hop causal reasoning and downstream shock projection.
    """

    def __init__(self):
        self.nodes: Dict[str, CausalNode] = {}
        self.adjacency: Dict[str, List[CausalEdge]] = {}
        self.reverse_adjacency: Dict[str, List[CausalEdge]] = {}

    def add_node(self, node: CausalNode) -> None:
        """Registers a node into the causal graph."""
        self.nodes[node.node_id] = node
        if node.node_id not in self.adjacency:
            self.adjacency[node.node_id] = []
        if node.node_id not in self.reverse_adjacency:
            self.reverse_adjacency[node.node_id] = []

    def add_edge(self, edge: CausalEdge) -> None:
        """Registers a directed causal edge between two existing nodes."""
        if edge.source_id not in self.nodes:
            raise ValueError(f"Source node '{edge.source_id}' not registered in graph.")
        if edge.target_id not in self.nodes:
            raise ValueError(f"Target node '{edge.target_id}' not registered in graph.")
        
        self.adjacency[edge.source_id].append(edge)
        self.reverse_adjacency[edge.target_id].append(edge)

    def find_causal_paths(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 5,
        hop_attenuation: float = 0.85
    ) -> List[CausalPath]:
        """
        Finds all directed causal paths from source to target within max_depth hops.
        Calculates cumulative impact:
            Impact = Base_Potency * Prod(|weight_i|) * (hop_attenuation ^ (hops - 1))
        """
        if source_id not in self.nodes or target_id not in self.nodes:
            return []

        results: List[CausalPath] = []
        visited: Set[str] = set()

        def dfs(current_id: str, current_path: List[str], current_edges: List[CausalEdge]):
            if len(current_path) > max_depth + 1:
                return
            if current_id == target_id and current_edges:
                hops = len(current_edges)
                base_p = self.nodes[source_id].base_potency
                attenuation = hop_attenuation ** max(0, hops - 1)
                
                # Compute cumulative impact & polarity
                impact_prod = 1.0
                polarity = 1
                for e in current_edges:
                    impact_prod *= abs(e.coupling_weight)
                    if e.coupling_weight < 0:
                        polarity *= -1
                
                cum_impact = round(base_p * impact_prod * attenuation, 4)
                results.append(
                    CausalPath(
                        source_id=source_id,
                        target_id=target_id,
                        path_nodes=list(current_path),
                        edges=list(current_edges),
                        hop_count=hops,
                        net_attenuation=round(attenuation, 4),
                        cumulative_impact=cum_impact,
                        net_polarity=polarity
                    )
                )
                return

            visited.add(current_id)
            for edge in self.adjacency.get(current_id, []):
                next_node = edge.target_id
                if next_node not in visited:
                    dfs(next_node, current_path + [next_node], current_edges + [edge])
            visited.remove(current_id)

        dfs(source_id, [source_id], [])
        results.sort(key=lambda p: p.cumulative_impact, reverse=True)
        return results

    def trace_downstream_shocks(
        self,
        root_id: str,
        max_depth: int = 4,
        min_impact: float = 0.05,
        hop_attenuation: float = 0.85
    ) -> List[Dict[str, Any]]:
        """
        Traces all downstream nodes impacted by a root shock, returning impacted nodes,
        maximum cumulative impact, and shortest hop distance.
        """
        if root_id not in self.nodes:
            return []

        downstream: Dict[str, Dict[str, Any]] = {}
        queue: List[tuple[str, float, int, List[str]]] = [(root_id, self.nodes[root_id].base_potency, 0, [root_id])]

        while queue:
            curr_id, curr_impact, depth, path = queue.pop(0)
            if depth >= max_depth:
                continue

            for edge in self.adjacency.get(curr_id, []):
                tgt = edge.target_id
                atten = hop_attenuation if depth > 0 else 1.0
                next_impact = round(curr_impact * abs(edge.coupling_weight) * atten, 4)
                
                if next_impact >= min_impact:
                    if tgt not in downstream or downstream[tgt]["max_impact"] < next_impact:
                        downstream[tgt] = {
                            "node_id": tgt,
                            "name": self.nodes[tgt].name,
                            "category": self.nodes[tgt].category,
                            "tier": self.nodes[tgt].epistemic_tier,
                            "max_impact": next_impact,
                            "shortest_hops": depth + 1,
                            "causal_mechanism": edge.mechanism,
                            "trace_path": path + [tgt]
                        }
                    queue.append((tgt, next_impact, depth + 1, path + [tgt]))

        res = list(downstream.values())
        res.sort(key=lambda x: x["max_impact"], reverse=True)
        return res

    def propagate_shock(
        self,
        initial_shocks: Dict[str, float],
        max_hops: int = 4,
        hop_attenuation: float = 0.85
    ) -> Dict[str, float]:
        """
        Propagates multiple concurrent shocks across the graph using independent cascade probabilistic union.
        Formula:
            S_target = 1.0 - Prod(1.0 - min(1.0, S_i * impact_i))
        """
        cumulative: Dict[str, float] = {}
        for root_id, severity in initial_shocks.items():
            if root_id not in self.nodes:
                continue
            traces = self.trace_downstream_shocks(root_id=root_id, max_depth=max_hops, hop_attenuation=hop_attenuation)
            for t in traces:
                tgt = t["node_id"]
                imp = t["max_impact"] * severity
                if tgt not in cumulative:
                    cumulative[tgt] = round(imp, 4)
                else:
                    cumulative[tgt] = round(1.0 - (1.0 - cumulative[tgt]) * (1.0 - min(1.0, imp)), 4)
        return cumulative

    def augment_from_distilled_claims(self, claims: List[Any]) -> int:
        """
        Dynamically augments the causal graph from atomically distilled propositions
        extracted by ChatConversationDistiller or persisted in EventStore.
        """
        import re
        added_edges = 0
        for claim in claims:
            causal_rel = getattr(claim, "causal_relation", None)
            if not causal_rel and isinstance(claim, dict):
                causal_rel = claim.get("causal_relation")
            if isinstance(causal_rel, str) and causal_rel.strip().startswith("["):
                try:
                    import json
                    causal_rel = json.loads(causal_rel)
                except Exception:
                    pass

            confidence = float(getattr(claim, "confidence", 0.85) if not isinstance(claim, dict) else claim.get("confidence", 0.85))
            raw_statement = getattr(claim, "raw_statement", "") if not isinstance(claim, dict) else claim.get("raw_statement", "")
            tier_val = getattr(claim, "epistemic_tier", 1) if not isinstance(claim, dict) else claim.get("epistemic_tier", 1)
            tier_int = tier_val.value if hasattr(tier_val, "value") and isinstance(tier_val.value, int) else 1

            if causal_rel and isinstance(causal_rel, (list, tuple)) and len(causal_rel) == 2:
                cause_text = str(causal_rel[0]).strip()
                effect_text = str(causal_rel[1]).strip()
                if len(cause_text) >= 3 and len(effect_text) >= 3:
                    clean_cause = re.sub(r'[^a-zA-Z0-9]+', '_', cause_text[:60].lower()).strip('_')
                    src_id = clean_cause if clean_cause.startswith("node_") else f"node_{clean_cause}"
                    clean_effect = re.sub(r'[^a-zA-Z0-9]+', '_', effect_text[:60].lower()).strip('_')
                    tgt_id = clean_effect if clean_effect.startswith("node_") else f"node_{clean_effect}"

                    if src_id not in self.nodes:
                        self.add_node(CausalNode(
                            node_id=src_id,
                            name=cause_text,
                            category="DISTILLED_ANTECEDENT",
                            epistemic_tier=tier_int,
                            base_potency=round(min(1.0, confidence), 2)
                        ))

                    if tgt_id not in self.nodes:
                        self.add_node(CausalNode(
                            node_id=tgt_id,
                            name=effect_text,
                            category="DISTILLED_CONSEQUENCE",
                            epistemic_tier=tier_int,
                            base_potency=round(min(1.0, confidence), 2)
                        ))

                    edge_exists = any(e.target_id == tgt_id for e in self.adjacency.get(src_id, []))
                    if not edge_exists:
                        coupling = min(0.95, max(0.40, confidence))
                        self.add_edge(CausalEdge(
                            source_id=src_id,
                            target_id=tgt_id,
                            coupling_weight=coupling,
                            latency_tier="MEDIUM_TERM",
                            mechanism=raw_statement[:120] if raw_statement else f"{cause_text} leads to {effect_text}"
                        ))
                        added_edges += 1

        return added_edges

    def augment_from_event_store(self, event_store: Any, limit: int = 50) -> int:
        """Synchronizes causal graph nodes and edges with persisted claim distillations in SQLite WAL."""
        if hasattr(event_store, "list_distilled_claims"):
            claims = event_store.list_distilled_claims(limit=limit)
            return self.augment_from_distilled_claims(claims)
        return 0

    @classmethod
    def build_canonical_graph(cls) -> "EpistemicKnowledgeGraph":

        """
        Instantiates and populates the canonical multi-century epistemic knowledge graph
        anchored in historical precedents, macro-monetary flows, and strategic chokepoints.
        """
        graph = cls()

        # =========================================================================
        # 1. MARITIME CHOKEPOINTS & CURRENCY DRAIN NODES
        # =========================================================================
        graph.add_node(CausalNode(
            node_id="hormuz_interdiction",
            name="Strait of Hormuz Tanker Interdiction",
            category="CHOKEPOINT",
            epistemic_tier=1,
            base_potency=1.0,
            metadata={"region": "Middle East", "chokepoint": "Hormuz"}
        ))
        graph.add_node(CausalNode(
            node_id="crude_freight_spike",
            name="Crude Oil Freight & Insurance Premium Surge",
            category="LOGISTICS",
            epistemic_tier=2,
            base_potency=0.95
        ))
        graph.add_node(CausalNode(
            node_id="refining_margin_compression",
            name="Domestic Refining Margin Compression",
            category="GEOECONOMIC",
            epistemic_tier=2,
            base_potency=0.90
        ))
        graph.add_node(CausalNode(
            node_id="inr_depreciation_pressure",
            name="Rupee Current Account Drain & FX Depreciation",
            category="CURRENCY",
            epistemic_tier=2,
            base_potency=0.88
        ))
        graph.add_node(CausalNode(
            node_id="foreign_portfolio_capital_flight",
            name="Foreign Institutional Investor Capital Outflow",
            category="FINANCIAL_FLOW",
            epistemic_tier=2,
            base_potency=0.85
        ))

        graph.add_edge(CausalEdge(
            source_id="hormuz_interdiction",
            target_id="crude_freight_spike",
            coupling_weight=0.88,
            latency_tier="IMMEDIATE",
            mechanism="War risk hull insurance and tanker charter rates double overnight."
        ))
        graph.add_edge(CausalEdge(
            source_id="crude_freight_spike",
            target_id="refining_margin_compression",
            coupling_weight=0.78,
            latency_tier="MEDIUM_TERM",
            mechanism="Landed cost of crude rises faster than domestic retail product pricing."
        ))
        graph.add_edge(CausalEdge(
            source_id="refining_margin_compression",
            target_id="inr_depreciation_pressure",
            coupling_weight=0.72,
            latency_tier="MEDIUM_TERM",
            mechanism="Surging US dollar oil import bills deplete foreign exchange liquidity."
        ))
        graph.add_edge(CausalEdge(
            source_id="inr_depreciation_pressure",
            target_id="foreign_portfolio_capital_flight",
            coupling_weight=0.65,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="FX depreciation risk triggers liquid equity and debt portfolio re-balancing."
        ))

        # =========================================================================
        # 2. CRITICAL MINERALS & ADVANCED SEMICONDUCTORS
        # =========================================================================
        graph.add_node(CausalNode(
            node_id="gallium_germanium_export_ban",
            name="Gallium and Germanium Critical Mineral Export Controls",
            category="CRITICAL_MINERALS",
            epistemic_tier=1,
            base_potency=0.95
        ))
        graph.add_node(CausalNode(
            node_id="high_purity_wafer_deficit",
            name="Compound Semiconductor Substrate & High-Purity Wafer Deficit",
            category="SUPPLY_CHAIN",
            epistemic_tier=2,
            base_potency=0.90
        ))
        graph.add_node(CausalNode(
            node_id="advanced_packaging_fab_bottleneck",
            name="Advanced ATMP & OSAT Packaging Yield Bottleneck",
            category="DEEP_TECH",
            epistemic_tier=2,
            base_potency=0.85
        ))
        graph.add_node(CausalNode(
            node_id="aesa_radar_production_lag",
            name="AESA Radar & Electronic Warfare Defense Hardware Production Lag",
            category="MILITARY_READINESS",
            epistemic_tier=3,
            base_potency=0.80
        ))

        graph.add_edge(CausalEdge(
            source_id="gallium_germanium_export_ban",
            target_id="high_purity_wafer_deficit",
            coupling_weight=0.85,
            latency_tier="IMMEDIATE",
            mechanism="Export licensing delays choke overseas wafer crystal growth foundries."
        ))
        graph.add_edge(CausalEdge(
            source_id="high_purity_wafer_deficit",
            target_id="advanced_packaging_fab_bottleneck",
            coupling_weight=0.80,
            latency_tier="MEDIUM_TERM",
            mechanism="Shortage of raw epi-wafers halts packaging and clean-room assembly lines."
        ))
        graph.add_edge(CausalEdge(
            source_id="advanced_packaging_fab_bottleneck",
            target_id="aesa_radar_production_lag",
            coupling_weight=0.70,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="GaN TR module delivery lags disrupt fighter aircraft radar installation schedules."
        ))

        # =========================================================================
        # 3. COLONIAL DISENFRANCHISEMENT & CASTE STATIGRAPHY
        # =========================================================================
        graph.add_node(CausalNode(
            node_id="eic_1770_saltpetre_monopsony",
            name="British East India Company 1770 Saltpetre State Monopsony",
            category="COLONIAL_ECONOMIC",
            epistemic_tier=1,
            base_potency=1.0,
            metadata={"historical_year": 1770}
        ))
        graph.add_node(CausalNode(
            node_id="artisan_guild_economic_collapse",
            name="Noniya & Artisan Guild Economic Disenfranchisement",
            category="SOCIO_ECONOMIC",
            epistemic_tier=2,
            base_potency=0.92
        ))
        graph.add_node(CausalNode(
            node_id="1871_criminal_tribes_act_criminalization",
            name="1871 Criminal Tribes Act Statutory Collective Criminalization",
            category="COLONIAL_LAWFARE",
            epistemic_tier=1,
            base_potency=0.95,
            metadata={"historical_year": 1871}
        ))
        graph.add_node(CausalNode(
            node_id="1901_risley_caste_crystallization",
            name="1901 Risley Census Racialized Caste Hierarchy Standardization",
            category="COLONIAL_CENSUS",
            epistemic_tier=2,
            base_potency=0.88,
            metadata={"historical_year": 1901}
        ))
        graph.add_node(CausalNode(
            node_id="1935_goi_depressed_classes_schedule",
            name="1935 GOI Act & 1936 Scheduled Castes Statutory Order",
            category="STATUTORY_SCHEDULE",
            epistemic_tier=1,
            base_potency=0.85,
            metadata={"historical_year": 1935}
        ))

        graph.add_edge(CausalEdge(
            source_id="eic_1770_saltpetre_monopsony",
            target_id="artisan_guild_economic_collapse",
            coupling_weight=0.92,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="EIC monopsony fixes raw prices below subsistence, destroying autonomous artisan wealth."
        ))
        graph.add_edge(CausalEdge(
            source_id="artisan_guild_economic_collapse",
            target_id="1871_criminal_tribes_act_criminalization",
            coupling_weight=0.86,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Impoverished nomadic extraction artisans criminalized to prevent unregulated mineral trade."
        ))
        graph.add_edge(CausalEdge(
            source_id="1871_criminal_tribes_act_criminalization",
            target_id="1901_risley_caste_crystallization",
            coupling_weight=0.82,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Herbert Risley's anthropometric census formalizes criminal tribe lists into fixed hierarchical jati tables."
        ))
        graph.add_edge(CausalEdge(
            source_id="1901_risley_caste_crystallization",
            target_id="1935_goi_depressed_classes_schedule",
            coupling_weight=0.78,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Colonial administration codifies the 1901 socio-economic degradation into statutory Depressed Classes schedules."
        ))

        # =========================================================================
        # 4. ASYMMETRIC SATURATION & NAVAL ATTRITION
        # =========================================================================
        graph.add_node(CausalNode(
            node_id="low_cost_drone_swarm_saturation",
            name="Low-Cost Loitering Munition & Drone Swarm Saturation",
            category="MILITARY_ATTRITION",
            epistemic_tier=1,
            base_potency=1.0
        ))
        graph.add_node(CausalNode(
            node_id="interceptor_magazine_burnout",
            name="High-End Naval Interceptor Magazine Depth Burnout",
            category="MILITARY_ATTRITION",
            epistemic_tier=2,
            base_potency=0.92
        ))
        graph.add_node(CausalNode(
            node_id="naval_corridor_escort_retreat",
            name="Naval Task Force Standoff & Escort Corridor Rationing",
            category="NAVAL_POSTURE",
            epistemic_tier=2,
            base_potency=0.86
        ))
        graph.add_node(CausalNode(
            node_id="commercial_cape_rerouting",
            name="Commercial Freight Re-Routing Around Cape of Good Hope",
            category="LOGISTICS",
            epistemic_tier=2,
            base_potency=0.88
        ))

        graph.add_edge(CausalEdge(
            source_id="low_cost_drone_swarm_saturation",
            target_id="interceptor_magazine_burnout",
            coupling_weight=0.90,
            latency_tier="IMMEDIATE",
            mechanism="Expenditure of $2M+ interceptors (SM-2/Aster) against $20,000 loitering threats depletes vertical launch cells."
        ))
        graph.add_edge(CausalEdge(
            source_id="interceptor_magazine_burnout",
            target_id="naval_corridor_escort_retreat",
            coupling_weight=0.82,
            latency_tier="MEDIUM_TERM",
            mechanism="Warships retreat out of anti-ship ballistic missile envelope to preserve defensive magazines."
        ))
        graph.add_edge(CausalEdge(
            source_id="naval_corridor_escort_retreat",
            target_id="commercial_cape_rerouting",
            coupling_weight=0.85,
            latency_tier="MEDIUM_TERM",
            mechanism="Loss of naval escort confidence prompts commercial container lines to bypass Bab-el-Mandeb."
        ))

        # =========================================================================
        # 5. TRANSNATIONAL CASTE LAWFARE & DIASPORA MARGINALIZATION
        # =========================================================================
        graph.add_node(CausalNode(
            node_id="transnational_caste_lawfare_campaign",
            name="Transnational Progressive Caste Lawfare Legislative Campaign",
            category="LAWFARE",
            epistemic_tier=1,
            base_potency=0.90
        ))
        graph.add_node(CausalNode(
            node_id="diaspora_institutional_marginalization",
            name="Expatriate Community Corporate & Academic Marginalization",
            category="DEMOGRAPHIC_SQUEEZE",
            epistemic_tier=2,
            base_potency=0.82
        ))
        graph.add_node(CausalNode(
            node_id="sovereign_advocacy_paralysis",
            name="Bilateral Grassroots Diaspora Advocacy Paralysis",
            category="STRATEGIC_AUTONOMY",
            epistemic_tier=3,
            base_potency=0.76
        ))

        graph.add_edge(CausalEdge(
            source_id="transnational_caste_lawfare_campaign",
            target_id="diaspora_institutional_marginalization",
            coupling_weight=0.78,
            latency_tier="MEDIUM_TERM",
            mechanism="Introduction of ambiguous protected category clauses creates HR liability for hiring Hindu engineers."
        ))
        graph.add_edge(CausalEdge(
            source_id="diaspora_institutional_marginalization",
            target_id="sovereign_advocacy_paralysis",
            coupling_weight=0.72,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Fear of professional censure chills diaspora political donations and national-interest advocacy."
        ))

        # =========================================================================
        # 6. INTRA-CIVILIZATIONAL BASE FRACTURING & COALITION COMPROMISE
        # =========================================================================
        graph.add_node(CausalNode(
            node_id="electoral_welfarism_expansion",
            name="Universal Subsidy & Electoral Welfarism Expansion",
            category="GEOECONOMIC",
            epistemic_tier=2,
            base_potency=0.92
        ))
        graph.add_node(CausalNode(
            node_id="middle_class_direct_tax_fatigue",
            name="Productive Salaried Middle-Class Direct Tax Fatigue",
            category="FISCAL_SQUEEZE",
            epistemic_tier=2,
            base_potency=0.88
        ))
        graph.add_node(CausalNode(
            node_id="core_voter_base_alienation",
            name="Core Civilizational Voter Apathy & Third-Party Protest Voting",
            category="POLITICAL_ALIGNMENT",
            epistemic_tier=3,
            base_potency=0.85
        ))
        graph.add_node(CausalNode(
            node_id="legislative_majority_loss",
            name="Parliamentary Single-Party Majority Loss",
            category="INSTITUTIONAL",
            epistemic_tier=3,
            base_potency=0.80
        ))
        graph.add_node(CausalNode(
            node_id="coalition_compromise_and_policy_paralysis",
            name="Coalition Management Friction & Strategic Policy Retraction",
            category="STATECRAFT",
            epistemic_tier=3,
            base_potency=0.75
        ))

        graph.add_edge(CausalEdge(
            source_id="electoral_welfarism_expansion",
            target_id="middle_class_direct_tax_fatigue",
            coupling_weight=0.85,
            latency_tier="MEDIUM_TERM",
            mechanism="Funding saturation welfarism without broadening direct tax base concentrates fiscal extraction on narrow salaried demographic."
        ))
        graph.add_edge(CausalEdge(
            source_id="middle_class_direct_tax_fatigue",
            target_id="core_voter_base_alienation",
            coupling_weight=0.78,
            latency_tier="MEDIUM_TERM",
            mechanism="Absence of middle-class social safety nets and perceived merit dilution induces voter apathy and abstention."
        ))
        graph.add_edge(CausalEdge(
            source_id="core_voter_base_alienation",
            target_id="legislative_majority_loss",
            coupling_weight=0.80,
            latency_tier="MEDIUM_TERM",
            mechanism="Turnout drop among foundational base in key constituencies flips marginal parliamentary seats to opposition."
        ))
        graph.add_edge(CausalEdge(
            source_id="legislative_majority_loss",
            target_id="coalition_compromise_and_policy_paralysis",
            coupling_weight=0.82,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Dependence on regional coalition allies forces executive retreats on structural reforms (land, labor, farm, education)."
        ))

        # =========================================================================
        # 7. VEDANTIC ONTOLOGY, INSTITUTIONAL LAWFARE & MARITIME THALASSOCRACY
        # =========================================================================
        graph.add_node(CausalNode(
            node_id="civilizational_virtue_organic",
            name="Organic Vedic Social Synthesis (Purusha Sukta & Vyadha Gita)",
            category="CIVILIZATIONAL_EPISTEMOLOGY",
            epistemic_tier=1,
            base_potency=0.95
        ))
        graph.add_node(CausalNode(
            node_id="institutional_temple_lawfare",
            name="Asymmetric Temple HR&CE Capital Extraction & Article 25-30 Lawfare",
            category="INSTITUTIONAL_LAWFARE",
            epistemic_tier=1,
            base_potency=0.92
        ))
        graph.add_node(CausalNode(
            node_id="kalinga_maritime_thalassocracy",
            name="Kalinga Maritime Thalassocracy & Indo-Pacific Trade Corridor",
            category="MARITIME_GEOPOLITICS",
            epistemic_tier=1,
            base_potency=0.90
        ))
        graph.add_node(CausalNode(
            node_id="kinesic_cognitive_warfare",
            name="World Leader Kinesic Deflection & Synthetic Narrative Warfare",
            category="COGNITIVE_WARFARE",
            epistemic_tier=2,
            base_potency=0.85
        ))

        graph.add_edge(CausalEdge(
            source_id="civilizational_virtue_organic",
            target_id="core_voter_base_alienation",
            coupling_weight=-0.75,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Organic civilizational unity and de-hyphenated dharmic education counteracts base fracturing and voter apathy."
        ))
        graph.add_edge(CausalEdge(
            source_id="institutional_temple_lawfare",
            target_id="sovereign_advocacy_paralysis",
            coupling_weight=0.76,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Depletion of independent temple trusts starves indigenous think tanks and civilizational defense endowments."
        ))
        graph.add_edge(CausalEdge(
            source_id="kalinga_maritime_thalassocracy",
            target_id="commercial_cape_rerouting",
            coupling_weight=-0.68,
            latency_tier="MEDIUM_TERM",
            mechanism="Alternative Indian Ocean SAGAR and IMEC trade routes reduce dependence on vulnerable Western maritime chokepoints."
        ))
        graph.add_edge(CausalEdge(
            source_id="kinesic_cognitive_warfare",
            target_id="transnational_caste_lawfare_campaign",
            coupling_weight=0.74,
            latency_tier="IMMEDIATE",
            mechanism="Synthetic media campaigns and weaponized perception optics amplify hostile transnational legislative targeting."
        ))

        # =========================================================================
        # 8. PRE-AHOM RIVERINE THALASSOCRACY & ASYMMETRICAL PACIFISM VULNERABILITY
        # =========================================================================
        graph.add_node(CausalNode(
            node_id="brahmaputra_riverine_thalassocracy",
            name="Brahmaputra Riverine Thalassocracy & Pre-Ahom Kamarupa Trade",
            category="MARITIME_GEOPOLITICS",
            epistemic_tier=1,
            base_potency=0.93
        ))
        graph.add_node(CausalNode(
            node_id="asymmetrical_pacifism_vulnerability",
            name="Asymmetrical Pacifism Vulnerability & Synthetic Moral Restraint",
            category="COGNITIVE_WARFARE",
            epistemic_tier=1,
            base_potency=0.88
        ))

        graph.add_edge(CausalEdge(
            source_id="brahmaputra_riverine_thalassocracy",
            target_id="commercial_cape_rerouting",
            coupling_weight=-0.72,
            latency_tier="MEDIUM_TERM",
            mechanism="Arterial riverine connectivity linking Lauhitya, Bengal Delta, and Bay of Bengal trade buffers against continental chokepoint disruptions."
        ))
        graph.add_edge(CausalEdge(
            source_id="brahmaputra_riverine_thalassocracy",
            target_id="sovereign_advocacy_paralysis",
            coupling_weight=-0.65,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Restoring Northeast pre-Ahom antiquity and sacred geography inoculates eastern frontier against external balkanization narratives."
        ))
        graph.add_edge(CausalEdge(
            source_id="asymmetrical_pacifism_vulnerability",
            target_id="sovereign_advocacy_paralysis",
            coupling_weight=0.78,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Internalized pacifist guilt and moral absolutism disarms proactive sovereign strategic defense."
        ))
        graph.add_edge(CausalEdge(
            source_id="asymmetrical_pacifism_vulnerability",
            target_id="naval_corridor_escort_retreat",
            coupling_weight=0.72,
            latency_tier="MEDIUM_TERM",
            mechanism="Reluctance to deploy forward kinetic naval escorts under pacifist doctrine accelerates maritime domain concession."
        ))

        # =========================================================================
        # 9. COMMERCIAL AVIATION SABOTAGE & DUAL-USE BIOSECURITY SHOCK
        # =========================================================================
        graph.add_node(CausalNode(
            node_id="aviation_insider_sabotage",
            name="Commercial Aviation Insider Infiltration & Asymmetric Kamikaze Threat",
            category="COGNITIVE_WARFARE",
            epistemic_tier=1,
            base_potency=0.91
        ))
        graph.add_node(CausalNode(
            node_id="dual_use_biosecurity_leak",
            name="Dual-Use Pathogen Laboratory Release & BWC Verification Grayzone",
            category="DEEP_TECH_SOVEREIGNTY",
            epistemic_tier=1,
            base_potency=0.94
        ))

        graph.add_edge(CausalEdge(
            source_id="aviation_insider_sabotage",
            target_id="commercial_cape_rerouting",
            coupling_weight=0.76,
            latency_tier="IMMEDIATE",
            mechanism="Targeting GCC-Israel commercial aviation routes triggers immediate airspace closures and war-risk insurance spikes."
        ))
        graph.add_edge(CausalEdge(
            source_id="aviation_insider_sabotage",
            target_id="sovereign_advocacy_paralysis",
            coupling_weight=0.68,
            latency_tier="MEDIUM_TERM",
            mechanism="Disinformation laundering by transnational media pathologizing terrorism as workplace fatigue disarms counter-terror vigilance."
        ))
        graph.add_edge(CausalEdge(
            source_id="dual_use_biosecurity_leak",
            target_id="sovereign_advocacy_paralysis",
            coupling_weight=0.75,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Concealment of Class-A pathogen leaks under 'unknown aetiology' paralyzes international multilateral biosecurity responses."
        ))
        graph.add_edge(CausalEdge(
            source_id="dual_use_biosecurity_leak",
            target_id="foreign_portfolio_capital_flight",
            coupling_weight=0.70,
            latency_tier="MEDIUM_TERM",
            mechanism="Contagion fears trigger regional quarantine lockdowns and rapid foreign capital withdrawal."
        ))

        # =========================================================================
        # 10. POST-QUANTUM CRYPTOGRAPHY & SOVEREIGN ASSET REPATRIATION
        # =========================================================================
        graph.add_node(CausalNode(
            node_id="post_quantum_cryptographic_vulnerability",
            name="Post-Quantum Cryptographic Vulnerability & Shor's Algorithm Decryption Threat",
            category="DEEP_TECH_SOVEREIGNTY",
            epistemic_tier=1,
            base_potency=0.95
        ))
        graph.add_node(CausalNode(
            node_id="sovereign_gold_reserve_repatriation",
            name="Sovereign Physical Gold Repatriation & Basel III De-Dollarization Buffer",
            category="GEOECONOMIC",
            epistemic_tier=1,
            base_potency=0.92
        ))

        graph.add_edge(CausalEdge(
            source_id="post_quantum_cryptographic_vulnerability",
            target_id="foreign_portfolio_capital_flight",
            coupling_weight=0.74,
            latency_tier="MEDIUM_TERM",
            mechanism="Compromise of legacy public-key encryption (RSA/ECC) threatens banking and transactional ledger integrity, driving capital flight."
        ))
        graph.add_edge(CausalEdge(
            source_id="post_quantum_cryptographic_vulnerability",
            target_id="sovereign_advocacy_paralysis",
            coupling_weight=0.72,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="'Harvest Now, Decrypt Later' espionage leaks compromise sovereign strategic decision-making and diplomatic autonomy."
        ))
        graph.add_edge(CausalEdge(
            source_id="sovereign_gold_reserve_repatriation",
            target_id="inr_depreciation_pressure",
            coupling_weight=-0.70,
            latency_tier="STRUCTURAL_LONG_TERM",
            mechanism="Repatriating unencumbered physical gold bullion establishes an asset-backed sovereign liquidity anchor that dampens currency depreciation."
        ))
        graph.add_edge(CausalEdge(
            source_id="sovereign_gold_reserve_repatriation",
            target_id="foreign_portfolio_capital_flight",
            coupling_weight=-0.65,
            latency_tier="MEDIUM_TERM",
            mechanism="Physical gold reserves backstop domestic sovereign creditworthiness against speculative foreign capital panics."
        ))

        return graph

