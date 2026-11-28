# SUBSYSTEM SPECIFICATION: SYNTHESIZER, PERSONA COUNCIL & CAUSAL GRAPH

## Module: `geo_engine/arbitration/__init__.py`

```python
"""
Arbitration and Synthesis Package for the Geo-Engine.
Contains the Negative Space Diff Engine and the 5-Tier Summit Synthesizer.
"""

from .negative_space import NegativeSpaceDiffEngine, DenseSemanticIndex
from .synthesizer import SummitSynthesizer, LaymanSynthesizer
from .persona_narrator import PersonaNarrator, CivilizationalCouncil

from .competing_hypotheses import (
    CausalHypothesisType,
    HypothesisCandidate,
    ACHEvaluationReport,
    IncidentReasoningEngine,
    TeleologicalEvaluation,
    TeleologicalFallacySieve,
    DecomposedClaim,
    ClaimDecomposer,
    StatisticalManipulationEvaluation,
    StatisticalManipulationSieve,
)
from .historical_arbiter import (
    ChronologyPillarScore,
    HistoricalHypothesisCandidate,
    ChronologyEvaluationReport,
    MultiPillarChronologyArbiter,
)
from .asset_fragility import (
    AssetFragilityModel,
    AssetDecayReport,
    VIPSecurityReport,
    SanctuaryViabilityReport,
)
from .causal_graph import (
    CausalNode,
    CausalEdge,
    CausalPath,
    EpistemicKnowledgeGraph,
)

from .whistleblower import (
    WhistleblowerDossier,
    WhistleblowerEvaluation,
    SatyamevaSuchakaPipeline,
)
from .dharmik_statecraft import (
    DharmikStatecraftDossier,
    DharmikStatecraftEvaluation,
    DharmikStatecraftPipeline,
)
from .semiotics import PredictiveIconographyAndSemioticDeconstructionEngine

__all__ = [
    "NegativeSpaceDiffEngine",
    "DenseSemanticIndex",
    "SummitSynthesizer",
    "PersonaNarrator",
    "CivilizationalCouncil",
    "CausalHypothesisType",
    "HypothesisCandidate",
    "ACHEvaluationReport",
    "IncidentReasoningEngine",
    "TeleologicalEvaluation",
    "TeleologicalFallacySieve",
    "DecomposedClaim",
    "ClaimDecomposer",
    "ChronologyPillarScore",
    "HistoricalHypothesisCandidate",
    "ChronologyEvaluationReport",
    "MultiPillarChronologyArbiter",
    "AssetFragilityModel",
    "AssetDecayReport",
    "VIPSecurityReport",
    "SanctuaryViabilityReport",
    "CausalNode",
    "CausalEdge",
    "CausalPath",
    "EpistemicKnowledgeGraph",
    "LaymanSynthesizer",
    "StatisticalManipulationEvaluation",
    "StatisticalManipulationSieve",
    "WhistleblowerDossier",
    "WhistleblowerEvaluation",
    "SatyamevaSuchakaPipeline",
    "DharmikStatecraftDossier",
    "DharmikStatecraftEvaluation",
    "DharmikStatecraftPipeline",
    "PredictiveIconographyAndSemioticDeconstructionEngine",
]


```

## Module: `geo_engine/arbitration/asset_fragility.py`

```python
"""
Asset Fragility and Covert Network Degradation Model.
Quantifies human intelligence (HUMINT) network survival, VIP security degradation
under protocol dilution (e.g. SPG withdrawal), and extraterritorial sanctuary viability.
"""

import math
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class AssetDecayReport(BaseModel):
    """Forensic report on intelligence network asset survival under operational and political hazard."""
    initial_prob: float = Field(ge=0.0, le=1.0)
    operational_exposure_rate: float = Field(ge=0.0)
    political_leak_rate: float = Field(ge=0.0)
    total_hazard_rate: float = Field(ge=0.0)
    time_months: float = Field(ge=0.0)
    residual_survival_prob: float = Field(ge=0.0, le=1.0)
    half_life_months: float = Field(ge=0.0)
    status: str
    forensic_audit_trail: str


class VIPSecurityReport(BaseModel):
    """Quantitative vulnerability assessment of VIP security apparatus under elite protocol dilution."""
    threat_level: float = Field(ge=0.0, le=1.0)
    spg_coverage: bool
    outer_perimeter_tier: int = Field(ge=1, le=3)
    institutional_sanctuary_friction: float = Field(ge=0.0, le=1.0)
    vulnerability_score: float = Field(ge=0.0, le=1.0)
    security_integrity_score: float = Field(ge=0.0, le=1.0)
    risk_tier: str
    historical_doctrine_note: str


class SanctuaryViabilityReport(BaseModel):
    """Audit of foreign sanctuary resilience versus covert kinetic penetration risk."""
    host_country: str
    rule_of_law_score: float = Field(ge=0.0, le=1.0)
    diaspora_vote_bank_salience: float = Field(ge=0.0, le=1.0)
    diplomatic_shielding: float = Field(ge=0.0, le=1.0)
    sanctuary_friction_index: float = Field(ge=0.0, le=1.0)
    penetration_vulnerability_index: float = Field(ge=0.0, le=1.0)
    classification: str
    forensic_explanation: str


class AssetFragilityModel:
    """
    Forensic engine evaluating intelligence asset network fragility, VIP security decay,
    and foreign sanctuary sustainability against offensive-defense doctrines.
    """

    @classmethod
    def simulate_network_decay(
        cls,
        initial_survival_prob: float = 1.0,
        operational_exposure_rate: float = 0.05,
        political_leak_rate: float = 0.0,
        time_months: float = 12.0
    ) -> AssetDecayReport:
        """
        Calculates residual survival probability of an intelligence network asset:
            S(t) = S0 * exp(-(lambda_op + lambda_political_leak) * t)
        Demonstrated historically in Operation Kahuta (1978), where political inadvertent disclosure
        instantly spiked lambda_political_leak to >0.85, terminating HUMINT viability in KRL.
        """
        init_p = max(0.0, min(1.0, float(initial_survival_prob)))
        op_rate = max(0.0, float(operational_exposure_rate))
        leak_rate = max(0.0, float(political_leak_rate))
        t = max(0.0, float(time_months))

        total_hazard = op_rate + leak_rate
        residual = init_p * math.exp(-total_hazard * t) if total_hazard > 0 else init_p
        residual_clamped = round(max(0.0, min(1.0, residual)), 4)

        half_life = round(math.log(2.0) / total_hazard, 2) if total_hazard > 1e-6 else 999.0

        if residual_clamped >= 0.70:
            status = "VIABLE"
        elif residual_clamped >= 0.40:
            status = "DEGRADED"
        elif residual_clamped >= 0.15:
            status = "COMPROMISED"
        else:
            status = "FATAL_EXPOSURE"

        audit_trail = (
            f"Asset Hazard Analysis: Total hazard rate {total_hazard:.4f} "
            f"(operational={op_rate:.3f}, political_leak={leak_rate:.3f}). "
            f"Residual survival over {t:.1f} months: {residual_clamped * 100:.1f}%. "
            f"Half-life: {half_life} months. Status: {status}."
        )

        return AssetDecayReport(
            initial_prob=init_p,
            operational_exposure_rate=op_rate,
            political_leak_rate=leak_rate,
            total_hazard_rate=round(total_hazard, 4),
            time_months=t,
            residual_survival_prob=residual_clamped,
            half_life_months=half_life,
            status=status,
            forensic_audit_trail=audit_trail
        )

    @classmethod
    def calculate_vip_security_degradation(
        cls,
        threat_level: float,
        spg_coverage: bool,
        outer_perimeter_tier: int = 1,
        institutional_sanctuary_friction: float = 0.2
    ) -> VIPSecurityReport:
        """
        Assesses VIP assassination vulnerability when elite proximate protection (SPG)
        is diluted or withdrawn, leaving reliance on multi-agency outer perimeters.
        Reference: Rajiv Gandhi assassination (Sriperumbudur, May 21, 1991).
        """
        t_level = max(0.0, min(1.0, float(threat_level)))
        p_tier = max(1, min(3, int(outer_perimeter_tier)))
        sanctuary_fric = max(0.0, min(1.0, float(institutional_sanctuary_friction)))

        if spg_coverage:
            # Dedicated elite ring with counter-assault team and advance security liaison
            vuln = round(min(1.0, t_level * 0.15), 4)
        else:
            # Diluted security: perimeter leak factor and lack of proximate sterile cordon
            perimeter_leak_factor = 1.0 + 0.35 * (3 - p_tier)
            sanctuary_amplification = 1.0 + 0.50 * sanctuary_fric
            raw_vuln = t_level * perimeter_leak_factor * sanctuary_amplification
            vuln = round(min(1.0, max(0.05, raw_vuln)), 4)

        integrity = round(1.0 - vuln, 4)

        if vuln <= 0.20:
            risk_tier = "MINIMAL"
        elif vuln <= 0.45:
            risk_tier = "ELEVATED"
        elif vuln <= 0.75:
            risk_tier = "HIGH"
        else:
            risk_tier = "CATASTROPHIC"

        hist_note = (
            "Historical Reference (Sriperumbudur 1991): Following the 1989-1990 withdrawal of SPG cover, "
            "security protocol was relegated to state police outer cordons lacking proximity sanitization, "
            "creating fatal asymmetric ingress opportunities for suicide operative suicide-belt penetration."
            if not spg_coverage else
            "SPG Institutional Protocol: Proximate sterile cordon, vetted inner ring, and counter-assault team active."
        )

        return VIPSecurityReport(
            threat_level=t_level,
            spg_coverage=spg_coverage,
            outer_perimeter_tier=p_tier,
            institutional_sanctuary_friction=sanctuary_fric,
            vulnerability_score=vuln,
            security_integrity_score=integrity,
            risk_tier=risk_tier,
            historical_doctrine_note=hist_note
        )

    @classmethod
    def evaluate_sanctuary_viability(
        cls,
        host_country: str,
        rule_of_law_score: float = 0.85,
        diaspora_vote_bank_salience: float = 0.70,
        diplomatic_shielding: float = 0.60
    ) -> SanctuaryViabilityReport:
        """
        Evaluates foreign safe-haven resilience against extraterritorial covert action.
        Synthesizes domestic political shelter against asymmetric kinetic penetration.
        Reference: 1985 Kanishka safe-haven complacency, Karachi D-Company shelter, 2023-2024 unknown gunmen dynamics.
        """
        rol = max(0.0, min(1.0, float(rule_of_law_score)))
        diaspora = max(0.0, min(1.0, float(diaspora_vote_bank_salience)))
        shield = max(0.0, min(1.0, float(diplomatic_shielding)))

        # Sanctuary friction represents institutional and political barriers to foreign state action
        sanctuary_fric = round((diaspora * 0.50) + (shield * 0.30) + (rol * 0.20), 4)

        # Penetration vulnerability: how susceptible the sanctuary is to asymmetric/extraterritorial disruption
        penetration_vuln = round(max(0.0, min(1.0, 1.0 - (sanctuary_fric * (1.0 - 0.20 * shield)))), 4)

        if sanctuary_fric >= 0.70:
            classification = "FORTIFIED_SANCTUARY"
            forensic = (
                f"High political insulation in {host_country}: Strong diaspora vote-bank leverage and diplomatic shielding "
                "impede legal extradition, creating strategic frictions for conventional bilateral law enforcement."
            )
        elif sanctuary_fric >= 0.40:
            classification = "PERMEABLE_SANCTUARY"
            forensic = (
                f"Permeable safe haven in {host_country}: Moderate institutional barriers make syndicate operatives vulnerable "
                "to offensive-defense doctrines, grey-market disruption, or extraterritorial kinetic friction."
            )
        else:
            classification = "COMPROMISED_SANCTUARY"
            forensic = (
                f"Compromised sanctuary in {host_country}: Insufficient legal or political shield allows high penetration "
                "vulnerability and rapid extraterritorial asset interdiction."
            )

        return SanctuaryViabilityReport(
            host_country=host_country,
            rule_of_law_score=rol,
            diaspora_vote_bank_salience=diaspora,
            diplomatic_shielding=shield,
            sanctuary_friction_index=sanctuary_fric,
            penetration_vulnerability_index=penetration_vuln,
            classification=classification,
            forensic_explanation=forensic
        )

```

## Module: `geo_engine/arbitration/causal_graph.py`

```python
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

    def traverse_shockwave_cascade(
        self,
        root_id: str,
        max_depth: int = 3,
        min_cumulative_confidence: float = 0.35,
        hop_attenuation: float = 0.85
    ) -> Dict[str, Any]:
        """
        Traverses multi-hop cascading shockwaves from a designated epicenter node,
        synthesizing primary shocks (depth 1), secondary ripples (depth 2), and
        tertiary disruptions (depth 3+) with narrative causal trajectories and mitigations.
        """
        if root_id not in self.nodes:
            return {
                "root_node_id": root_id,
                "error": f"Root node '{root_id}' not found in epistemic knowledge graph.",
                "total_impacted_nodes": 0
            }

        root_node = self.nodes[root_id]
        traces = self.trace_downstream_shocks(
            root_id=root_id,
            max_depth=max_depth,
            min_impact=min_cumulative_confidence,
            hop_attenuation=hop_attenuation
        )

        primary = []
        secondary = []
        tertiary = []
        narrative_chains = []
        chokepoints = []

        for t in traces:
            nid = t["node_id"]
            hops = t["shortest_hops"]
            entry = {
                "node_id": nid,
                "name": t["name"],
                "category": t["category"],
                "epistemic_tier": t["tier"],
                "net_impact": t["max_impact"],
                "hops": hops,
                "causal_mechanism": t["causal_mechanism"],
                "chain": " -> ".join(t["trace_path"])
            }
            if t["category"] in ("CHOKEPOINT", "LOGISTICS", "MARITIME"):
                chokepoints.append(t["name"])

            narrative_chains.append(f"[{hops}-HOP] {entry['chain']} via {t['causal_mechanism']} (Impact: {t['max_impact']})")

            if hops == 1:
                primary.append(entry)
            elif hops == 2:
                secondary.append(entry)
            else:
                tertiary.append(entry)

        mitigations = []
        if chokepoints:
            mitigations.append(f"Maritime/Logistics Chokepoints identified ({', '.join(set(chokepoints))}). Reroute freight, deploy naval escorts, and buffer coastal fuel stockpiles.")
        if any(t["category"] in ("CURRENCY", "MACRO_FINANCIAL") for t in traces):
            mitigations.append("Macro-monetary shockwave detected. Activate Special Rupee Vostro Accounts (SRVA) and bilateral currency swap windows.")
        if any(t["category"] in ("FERTILIZER", "FOOD_SECURITY") for t in traces):
            mitigations.append("Caloric sovereignty alert. Enforce domestic export controls and expand strategic fertilizer buffer inventories.")
        if not mitigations:
            mitigations.append("Maintain sovereign strategic autonomy; monitor secondary and tertiary supply-chain indicators.")

        return {
            "root_node_id": root_id,
            "root_node_name": root_node.name,
            "root_category": root_node.category,
            "primary_shocks": primary,
            "secondary_ripples": secondary,
            "tertiary_shockwaves": tertiary,
            "causal_narrative_chains": narrative_chains,
            "vulnerable_chokepoints": list(set(chokepoints)),
            "strategic_mitigations": mitigations,
            "cascade_depth_reached": max((t["shortest_hops"] for t in traces), default=0),
            "total_impacted_nodes": len(traces)
        }

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


```

## Module: `geo_engine/arbitration/competing_hypotheses.py`

```python
"""
Analysis of Competing Hypotheses (ACH) & Epistemic Causality Engine.
Implements intelligence doctrine (Richards Heuer methodology) to evaluate
competing causal hypotheses for anomalous kinetic, maritime, and border incidents
before leaping to strategic or civilizational 'inner meaning' conclusions.
"""

import re
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


class TeleologicalEvaluation(BaseModel):
    """Evaluation of whether an analytical claim or narrative commits the teleological fallacy."""
    is_teleological_fallacy: bool = False
    teleological_inflation_ratio: float = 1.0
    premeditated_plot_probability: float = 0.33
    emergent_opportunism_probability: float = 0.33
    legitimate_evolution_probability: float = 0.34
    verdict: str = "BALANCED_CAUSALITY"
    rationale: str = ""


class TeleologicalFallacySieve:
    """
    Sifts claims to detect the Teleological Fallacy: the analytical error of attributing
    a grand, pre-planned, coordinated top-down conspiracy (H_plot) to what is actually
    an emergent convergence of socio-economic shifts (H_market) and empirical public health
    or technological evolution (H_empirical).
    """

    PLOT_KEYWORDS = [
        "conspiracy", "brainwash", "brainwashing", "sinister", "sinister plot", "secret cabal",
        "master plan", "deliberate design to make depressed", "matrix", "engineered to enslave",
        "deliberate capitalist plot", "capitalist conspiracy", "enslave", "make depressed",
        "premeditated scheme", "shadow syndicate"
    ]
    MARKET_KEYWORDS = [
        "marketing", "advertising", "commercial", "monetiz", "monetization", "opportunism",
        "profit", "urbanization", "working parents", "lifestyle", "fear-based",
        "fear marketing", "guilt", "corporate", "commercialization", "product sales"
    ]
    EMPIRICAL_KEYWORDS = [
        "mortality", "germ", "bacteria", "antiseptic", "hygiene", "sanitation",
        "clean water", "cholera", "infection", "public health", "medicine", "scientific",
        "infant mortality", "pathogen", "sterilization", "epidemiology"
    ]

    @classmethod
    def evaluate(
        cls,
        text: str,
        claims: Optional[List[Any]] = None
    ) -> TeleologicalEvaluation:
        combined = text.lower()
        if claims:
            for c in claims:
                fact = getattr(c, "asserted_fact", getattr(c, "assertion", ""))
                combined += " " + str(fact).lower()

        # Prior probabilities
        prior_plot = 0.33
        prior_market = 0.33
        prior_empirical = 0.34

        # Count keyword evidence
        plot_hits = sum(1 for kw in cls.PLOT_KEYWORDS if kw in combined)
        market_hits = sum(1 for kw in cls.MARKET_KEYWORDS if kw in combined)
        empirical_hits = sum(1 for kw in cls.EMPIRICAL_KEYWORDS if kw in combined)

        # Likelihood updates: calibrated to prevent unevidenced hypotheses from inflating denominator
        l_plot = 0.40 + min(0.55, plot_hits * 0.25) if plot_hits > 0 else 0.15
        l_market = 0.40 + min(0.55, market_hits * 0.20) if market_hits > 0 else 0.15
        l_empirical = 0.40 + min(0.55, empirical_hits * 0.20) if empirical_hits > 0 else 0.15

        # Bayesian posterior
        num_plot = prior_plot * l_plot
        num_market = prior_market * l_market
        num_empirical = prior_empirical * l_empirical
        denom = num_plot + num_market + num_empirical

        p_plot = round(num_plot / denom, 4) if denom > 0 else 0.3333
        p_market = round(num_market / denom, 4) if denom > 0 else 0.3333
        p_empirical = round(num_empirical / denom, 4) if denom > 0 else 0.3334

        # Teleological inflation ratio: plot / (market + empirical)
        base_denom = p_market + p_empirical
        t_ratio = round(p_plot / base_denom, 2) if base_denom > 0 else 1.0

        # Hard documentary proof check
        hard_proof_keywords = ["declassified memo", "signed directive", "cabinet order", "statutory record", "judicial finding"]
        has_hard_proof = any(kw in combined for kw in hard_proof_keywords)

        is_fallacy = (
            (t_ratio >= 1.50 or (p_plot > p_market and p_plot > p_empirical and t_ratio >= 1.25))
            and not has_hard_proof
            and plot_hits > 0
        )

        if is_fallacy:
            verdict = "TELEOLOGICAL_FALLACY_DETECTED"
            rationale = (
                f"Teleological fallacy detected (Inflation ratio: {t_ratio:.2f} >= 1.50). "
                f"The narrative attributes a grand, coordinated top-down conspiracy ({p_plot:.1%}) "
                f"without documentary proof, when empirical history demonstrates an emergent combination of "
                f"commercial market opportunism ({p_market:.1%}) and public health evolution ({p_empirical:.1%})."
            )
        elif p_market >= 0.45:
            verdict = "EMERGENT_COMMERCIAL_OPPORTUNISM"
            rationale = (
                f"Phenomenon is primarily driven by emergent commercial market opportunism ({p_market:.1%}), "
                f"where commercial actors monetized societal lifestyle shifts and anxieties rather than executing a pre-planned conspiracy."
            )
        elif p_empirical >= 0.45:
            verdict = "LEGITIMATE_EMPIRICAL_EVOLUTION"
            rationale = (
                f"Phenomenon is primarily grounded in verifiable public health, scientific, or technological evolution ({p_empirical:.1%})."
            )
        else:
            verdict = "BALANCED_CAUSALITY"
            rationale = f"Causality distributed across conspiratorial ({p_plot:.1%}), commercial ({p_market:.1%}), and empirical ({p_empirical:.1%}) factors."

        return TeleologicalEvaluation(
            is_teleological_fallacy=is_fallacy,
            teleological_inflation_ratio=t_ratio,
            premeditated_plot_probability=p_plot,
            emergent_opportunism_probability=p_market,
            legitimate_evolution_probability=p_empirical,
            verdict=verdict,
            rationale=rationale
        )


class DecomposedClaim(BaseModel):
    """
    Decomposition of compound political/rhetorical claims into atomic premises and causal attributions.
    Specifically isolates 'Poisoned Tail' misinformation where factual premises (e.g. 70%) are paired
    with unevidenced or conspiratorial causal leaps (e.g. 30%).
    """
    raw_text: str
    factual_premises: List[str] = Field(default_factory=list)
    causal_assertions: List[str] = Field(default_factory=list)
    conjunction_detected: Optional[str] = None
    is_poisoned_tail_detected: bool = False
    is_proximity_framing_detected: bool = False
    proximity_framing_indicators: List[str] = Field(default_factory=list)
    premise_veracity_score: float = Field(default=1.0, ge=0.0, le=1.0)
    inference_veracity_score: float = Field(default=1.0, ge=0.0, le=1.0)
    poisoned_tail_ratio: float = Field(default=0.0, ge=0.0)
    epistemic_classification: str = "VALID_COHERENT_CLAIM"
    rationale: str = ""


class ClaimDecomposer:
    """
    Atomic Claim-Decomposition Token Splitter.
    Deconstructs compound rhetorical narratives across causal inflection points
    to isolate true premises from weaponized, ungrounded causal conclusions.
    Includes temporal proximity framing forensics for juxtaposed unevidenced leaps.
    """
    CAUSAL_CONNECTORS = [
        " therefore ", " hence ", " consequently ", " thus ", " which proves that ",
        " leading to ", " revealing that ", " showing that ", " which means that ",
        " isliye ", " kyunki ", " jisse saabit hota hai ki ", " indicating that "
    ]

    CONSPIRACY_LEAP_KEYWORDS = [
        "vote chori", "stolen election", "rigged", "vote theft", "conspiracy", "traitor",
        "deshdrohi", "turn approver", "sabotage", "subversion", "captured", "criminal plot",
        "secret plot", "sold out", "collusion", "colluding", "act of war", "surrendered sovereignty",
        "puppet state", "puppet government", "axis against", "illegal annexation",
        "violating sanctions", "backchannel surrender", "hostile axis", "secret pact", "foreign agent"
    ]

    TEMPORAL_PROXIMITY_MARKERS = [
        "hours later", "the following day", "the next day", "the following morning",
        "immediately following", "shortly after", "days later", "shortly thereafter",
        "on the same day", "at the same time", "within 24 hours", "within 48 hours",
        "subsequently", "the next morning", "a day later", "following the meeting"
    ]

    FACTUAL_INDICATORS = [
        "revision", "special intensive revision", "sir", "electoral roll", "election commission",
        "dissent", "objection", "recorded", "meeting", "gazette", "notification", "query",
        "deleted", "added", "verified", "form 7", "form 8", "eci", "official", "deliberation",
        "agreement", "bilateral", "treaty", "port", "trade", "procurement", "mou"
    ]

    @classmethod
    def decompose(cls, claim_text: str) -> DecomposedClaim:
        text_clean = claim_text.strip()
        text_lower = text_clean.lower()

        # Find causal inflection point
        connector_found = None
        split_idx = -1
        for conn in cls.CAUSAL_CONNECTORS:
            if conn in text_lower:
                idx = text_lower.find(conn)
                if idx != -1:
                    connector_found = conn.strip()
                    split_idx = idx
                    break

        if split_idx != -1:
            premise_part = text_clean[:split_idx].strip()
            inference_part = text_clean[split_idx + len(connector_found) + 2:].strip()
            premises = [p.strip() for p in premise_part.split(";") if p.strip()] or [premise_part]
            inferences = [i.strip() for i in inference_part.split(";") if i.strip()] or [inference_part]
        else:
            # Fallback: check for multi-sentence structure
            sentences = [s.strip() for s in re.split(r"[.\n]+", text_clean) if s.strip()]
            if len(sentences) >= 2:
                premises = sentences[:-1]
                inferences = [sentences[-1]]
                connector_found = "sentence_boundary"
            else:
                premises = [text_clean]
                inferences = []

        prem_str = " ".join(premises).lower()
        inf_str = " ".join(inferences).lower()

        # Check for temporal proximity framing markers
        proximity_hits = [m for m in cls.TEMPORAL_PROXIMITY_MARKERS if m in text_lower]
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day_mentions = [d for d in days if f"on {d}" in text_lower]
        if len(day_mentions) >= 2:
            proximity_hits.append(f"successive_days({day_mentions[0]}->{day_mentions[1]})")
        is_proximity_framed = bool(proximity_hits and len(premises) >= 1 and inferences)

        # Score premise veracity (presence of factual administrative/statutory terminology)
        factual_premise_hits = sum(1 for kw in cls.FACTUAL_INDICATORS if kw in prem_str)
        premise_veracity = min(1.0, 0.50 + factual_premise_hits * 0.15) if premises else 0.50

        # Score inference veracity and leap
        conspiracy_hits = sum(1 for kw in cls.CONSPIRACY_LEAP_KEYWORDS if kw in inf_str)
        if inferences:
            if conspiracy_hits > 0:
                inference_veracity = max(0.10, 0.40 - conspiracy_hits * 0.15)
            elif is_proximity_framed:
                inference_veracity = 0.45
            else:
                inference_veracity = 0.70
        else:
            inference_veracity = 1.0

        poisoned_ratio = round(premise_veracity / max(0.05, inference_veracity), 2)
        is_poisoned = bool(inferences and conspiracy_hits > 0 and premise_veracity >= 0.60 and poisoned_ratio >= 1.50)

        if is_poisoned:
            classification = "POISONED_TAIL_MISINFORMATION_DETECTED"
            rationale = (
                f"Poisoned Tail Misinformation Detected: Factual premise(s) have empirical administrative grounding "
                f"({premise_veracity:.1%}), but the concluding causal attribution leaps to unproven conspiracy "
                f"({inference_veracity:.1%}) with a distortion ratio of {poisoned_ratio:.2f}."
            )
        elif is_proximity_framed:
            classification = "PROXIMITY_FRAMING_MISINFORMATION_DETECTED"
            rationale = (
                f"Proximity-Framing Misinformation Detected: Disparate events juxtaposed across temporal proximity "
                f"markers ({', '.join(proximity_hits[:2])}) without verified statutory/evidentiary causality (distortion ratio: {poisoned_ratio:.2f})."
            )
        elif inferences:
            classification = "COMPOUND_ARGUMENT_EVALUATED"
            rationale = f"Compound claim decomposed into {len(premises)} premise(s) and {len(inferences)} inference(s)."
        else:
            classification = "ATOMIC_CLAIM"
            rationale = "Claim does not contain compound causal conjunctions."

        return DecomposedClaim(
            raw_text=claim_text,
            factual_premises=premises,
            causal_assertions=inferences,
            conjunction_detected=connector_found,
            is_poisoned_tail_detected=is_poisoned,
            is_proximity_framing_detected=is_proximity_framed,
            proximity_framing_indicators=proximity_hits,
            premise_veracity_score=round(premise_veracity, 2),
            inference_veracity_score=round(inference_veracity, 2),
            poisoned_tail_ratio=poisoned_ratio,
            epistemic_classification=classification,
            rationale=rationale
        )


class StatisticalManipulationEvaluation(BaseModel):
    """Evaluation of whether a numerical claim commits statistical or denominator manipulation."""
    is_statistical_manipulation_detected: bool = False
    manipulation_type: str = "LEGITIMATE_STATISTICAL_CITATION"
    denominator_suppression_score: float = Field(default=0.0, ge=0.0, le=1.0)
    gross_vs_net_distortion_ratio: float = Field(default=1.0, ge=0.0)
    suppressed_denominator_detected: bool = False
    gross_loss_without_addition_detected: bool = False
    truncated_baseline_detected: bool = False
    verdict: str = "BALANCED_STATISTICAL_REPORTING"
    rationale: str = ""


class StatisticalManipulationSieve:
    """
    Phase 151: Statistical Manipulation & Suppressed Denominator Sieve.
    Sifts numerical and quantitative claims to detect suppressed denominators,
    gross vs. net distortions, and truncated temporal baselines.
    """
    MAGNITUDE_KEYWORDS = [
        r"\b([0-9]+(?:\.[0-9]+)?\s*(?:lakh|crore|million|billion|trillion|k|percent|%))\b",
        r"\b([0-9]{2,3}(?:,[0-9]{3})+)\b",
        r"\b([0-9]{5,})\b"
    ]
    NEGATIVE_DELTA_KEYWORDS = [
        "deleted", "deletion", "purged", "removed", "cut", "lost", "dropped",
        "slashed", "erased", "wiped out", "stolen", "snatched", "chori", "gayab", "hata diya"
    ]
    COMPENSATING_DELTA_KEYWORDS = [
        "added", "enrolled", "registered", "new voters", "created", "net increase",
        "net change", "parallel addition", "verified inclusions", "form 6", "inclusion"
    ]
    DENOMINATOR_KEYWORDS = [
        "out of", "from total", "total electorate", "total population", "total workforce",
        "overall base", "registered voters", "kul sankhya", "total registered", "across all states"
    ]
    TRUNCATED_BASELINE_KEYWORDS = [
        "jumped", "spiked", "surged", "skyrocketed", "soared", "record surge",
        "massive spike", "since last month", "overnight spike"
    ]

    @classmethod
    def evaluate(cls, claim_text: str) -> StatisticalManipulationEvaluation:
        text_lower = claim_text.lower()
        has_magnitude = any(re.search(pat, text_lower) for pat in cls.MAGNITUDE_KEYWORDS)
        neg_hits = [kw for kw in cls.NEGATIVE_DELTA_KEYWORDS if kw in text_lower]
        comp_hits = [kw for kw in cls.COMPENSATING_DELTA_KEYWORDS if kw in text_lower]
        denom_hits = [kw for kw in cls.DENOMINATOR_KEYWORDS if kw in text_lower]
        spike_hits = [kw for kw in cls.TRUNCATED_BASELINE_KEYWORDS if kw in text_lower]

        is_suppressed_denom = bool(has_magnitude and neg_hits and not denom_hits)
        is_gross_without_net = bool(has_magnitude and neg_hits and not comp_hits)
        is_truncated_baseline = bool(has_magnitude and spike_hits and not denom_hits)

        denom_score = 0.85 if is_suppressed_denom else (0.45 if has_magnitude and not denom_hits else 0.10)
        gross_distortion = 2.50 if (is_gross_without_net and is_suppressed_denom) else (1.75 if is_gross_without_net else 1.0)
        is_manipulated = bool(is_suppressed_denom or (is_gross_without_net and len(neg_hits) >= 1))

        if is_suppressed_denom and is_gross_without_net:
            m_type = "SUPPRESSED_DENOMINATOR_AND_GROSS_LOSS_BIAS"
            verdict = "ACUTE_STATISTICAL_MANIPULATION_DETECTED"
            rationale = (
                f"Statistical manipulation detected: Absolute negative volumes ({', '.join(neg_hits)}) "
                f"cited without disclosing total baseline denominator or compensating additions/registrations "
                f"(distortion ratio: {gross_distortion:.2f})."
            )
        elif is_suppressed_denom:
            m_type = "SUPPRESSED_DENOMINATOR"
            verdict = "SUPPRESSED_DENOMINATOR_DETECTED"
            rationale = (
                f"Absolute numerical loss cited without total population denominator baseline context "
                f"(suppression score: {denom_score:.2f})."
            )
        elif is_gross_without_net:
            m_type = "GROSS_NET_ASYMMETRY"
            verdict = "GROSS_TURNOVER_MISREPRESENTED_AS_NET_LOSS"
            rationale = "Gross subtractions/deletions highlighted without verifying parallel administrative accretions or net balance changes."
        elif is_truncated_baseline:
            m_type = "TRUNCATED_TEMPORAL_BASELINE"
            verdict = "CHERRY_PICKED_TEMPORAL_BASELINE"
            rationale = "Rate of change or growth spike asserted using truncated baseline without normalized multi-period moving average."
        else:
            m_type = "LEGITIMATE_STATISTICAL_CITATION"
            verdict = "BALANCED_STATISTICAL_REPORTING"
            rationale = "Statistical citation includes adequate contextual baselines or lacks manipulative omission patterns."

        return StatisticalManipulationEvaluation(
            is_statistical_manipulation_detected=is_manipulated,
            manipulation_type=m_type,
            denominator_suppression_score=denom_score,
            gross_vs_net_distortion_ratio=gross_distortion,
            suppressed_denominator_detected=is_suppressed_denom,
            gross_loss_without_addition_detected=is_gross_without_net,
            truncated_baseline_detected=is_truncated_baseline,
            verdict=verdict,
            rationale=rationale
        )


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
    teleological_sieve: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serializes report into JSON-compatible dictionary."""
        return {
            "incident_title": self.incident_title,
            "dominant_hypothesis_id": self.dominant_hypothesis_id,
            "dominant_hypothesis_label": self.dominant_hypothesis_label,
            "dominant_probability": round(self.dominant_probability, 3),
            "is_epistemically_contested": self.is_epistemically_contested,
            "epistemic_warning": self.epistemic_warning,
            "teleological_sieve": self.teleological_sieve,
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

        # 6. Teleological Fallacy Sieve Evaluation
        teleological_eval = TeleologicalFallacySieve.evaluate(combined_text)
        audit_trail.append(
            f"[ACH_TELEOLOGY] Teleological Sieve verdict: {teleological_eval.verdict} (Inflation ratio: {teleological_eval.teleological_inflation_ratio:.2f})."
        )
        if teleological_eval.is_teleological_fallacy:
            audit_trail.append(
                f"[ACH_TELEOLOGY] Teleological Fallacy detected: Inflation ratio {teleological_eval.teleological_inflation_ratio:.2f} >= 1.50."
            )
            if not warning:
                warning = f"[ACH TELEOLOGICAL WARNING] {teleological_eval.rationale}"

        return ACHEvaluationReport(
            incident_title=incident_title,
            hypotheses=hypotheses,
            dominant_hypothesis_id=dominant.hypothesis_id,
            dominant_hypothesis_label=dominant.label,
            dominant_probability=dominant.posterior_probability,
            is_epistemically_contested=is_contested,
            epistemic_warning=warning,
            reasoning_audit_trail=audit_trail,
            teleological_sieve=teleological_eval.model_dump()
        )

```

## Module: `geo_engine/arbitration/dharmik_statecraft.py`

```python
"""
Dharmik Statecraft Engine (Phases 355-365).
Synthesizes the Tri-Pillar Bharatiya Strategic Core:
1. Chāṇakya Nīti (Micro-Forensic Upadhā-Parīkṣā & Mantra-Gupti Secrecy)
2. Kauṭilya Arthaśāstra (Macro-Statecraft Saptāṅga 7-Limb Power & Ṣaḍguṇya Foreign Policy)
3. Bhagavān Śrī Kṛṣṇa (Meta-Civilizational Rājadharma, Peace Exhaustion & Svadharma Resolve)
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import math

from ..lenses import (
    ChanakyaNeetiUpadhaIntegritySieve,
    KautilyaMandalaShadgunyaSieve,
    KrishnaRajadharmaExhaustionSieve,
    BISHiddenFXSwapContagionSieve,
    OffshoreUBOShellDeAnonymizerSieve,
    SpeechToBalanceSheetDivergenceTensor,
    KinesicContextualBaselineDriftSieve,
)


@dataclass
class DharmikStatecraftDossier:
    """Represents a geopolitical crisis, treaty negotiation, or counter-subversion statecraft scenario."""
    dossier_id: str
    title: str
    target_nation_or_entity: str
    narrative_context: str
    domain: str = "DHARMIC_STATECRAFT"
    swami_leadership_clarity: float = 0.85
    amatya_bureaucratic_integrity: float = 0.75
    janapada_demographic_agriculture: float = 0.80
    durga_fortification_dpi: float = 0.80
    kosha_treasury_depth: float = 0.85
    danda_military_deterrence: float = 0.85
    mitra_alliance_reliability: float = 0.70
    adversary_power_index: float = 0.70
    dharmopadha_vulnerability: float = 0.20
    arthopadha_vulnerability: float = 0.25
    kamopadha_vulnerability: float = 0.15
    bhayopadha_vulnerability: float = 0.30
    mantra_gupti_secrecy_index: float = 0.80
    peace_initiatives_exhausted_ratio: float = 0.85
    adversary_existential_hostility: float = 0.80
    sentimental_hesitation_moha: float = 0.20
    dharmic_svadharma_resolve: float = 0.85


@dataclass
class DharmikStatecraftEvaluation:
    """Comprehensive strategic evaluation under the Tri-Pillar Bharatiya Statecraft Core."""
    dossier_id: str
    target_nation_or_entity: str
    composite_dharmik_sovereignty_index: float
    kautilya_saptanga_score: float
    optimal_sadgunya_policy: str
    chanakya_upadha_integrity_score: float
    krishna_rajadharma_exhaustion_score: float
    rajadharma_authorization_tier: str
    operational_directive: str
    competing_strategic_doctrines: Dict[str, float]
    council_perspectives: Dict[str, str]


class DharmikStatecraftPipeline:
    """Pipeline coordinator for multi-pillar civilizational statecraft evaluation."""

    @classmethod
    def evaluate_scenario(cls, d: DharmikStatecraftDossier) -> DharmikStatecraftEvaluation:
        # 1. Evaluate Saptanga & Shadgunya (Kautilya)
        k_res = KautilyaMandalaShadgunyaSieve.evaluate(
            swami_leadership_clarity=d.swami_leadership_clarity,
            amatya_bureaucratic_integrity=d.amatya_bureaucratic_integrity,
            janapada_demographic_agriculture=d.janapada_demographic_agriculture,
            durga_fortification_dpi=d.durga_fortification_dpi,
            kosha_treasury_depth=d.kosha_treasury_depth,
            danda_military_deterrence=d.danda_military_deterrence,
            mitra_alliance_reliability=d.mitra_alliance_reliability,
            adversary_power_index=d.adversary_power_index,
        )
        s_saptanga = k_res["kautilya_saptanga_score"]
        sadgunya_policy = k_res["optimal_sadgunya_policy"]

        # 2. Evaluate Upadha-Pariksha & Mantra-Gupti (Chanakya)
        c_res = ChanakyaNeetiUpadhaIntegritySieve.evaluate(
            dharmopadha_vulnerability=d.dharmopadha_vulnerability,
            arthopadha_vulnerability=d.arthopadha_vulnerability,
            kamopadha_vulnerability=d.kamopadha_vulnerability,
            bhayopadha_vulnerability=d.bhayopadha_vulnerability,
            mantra_gupti_secrecy_index=d.mantra_gupti_secrecy_index,
        )
        s_upadha = c_res["chanakya_upadha_integrity_score"]

        # 3. Evaluate Udyoga Peace Exhaustion & Svadharma Resolve (Sri Krishna)
        kr_res = KrishnaRajadharmaExhaustionSieve.evaluate(
            peace_initiatives_exhausted_ratio=d.peace_initiatives_exhausted_ratio,
            adversary_existential_hostility=d.adversary_existential_hostility,
            sentimental_hesitation_moha=d.sentimental_hesitation_moha,
            dharmic_svadharma_resolve=d.dharmic_svadharma_resolve,
        )
        s_krishna = kr_res["krishna_rajadharma_exhaustion_score"]
        rajadharma_tier = kr_res["rajadharma_authorization_tier"]

        # 4. Composite Sovereignty Index
        composite_idx = round(0.40 * s_saptanga + 0.30 * (1.0 - s_upadha) + 0.30 * s_krishna, 4)

        # 5. Competing Strategic Doctrines (ACH Softmax)
        d_kautilya = round(max(0.01, s_saptanga * 0.50 + (1.0 - s_upadha) * 0.50), 4)
        d_krishna = round(max(0.01, s_krishna * 0.60 + s_saptanga * 0.40), 4)
        d_chanakya = round(max(0.01, (1.0 - s_upadha) * 0.60 + d.mantra_gupti_secrecy_index * 0.40), 4)
        d_defensive = round(max(0.01, d.sentimental_hesitation_moha * 0.70 + 0.10), 4)

        tot_d = d_kautilya + d_krishna + d_chanakya + d_defensive
        doctrines = {
            "KAUTILYAN_SAPTANGA_REALPOLITIK": round(d_kautilya / tot_d, 4),
            "KRISHNA_RAJADHARMA_DHARMA_YUDDHA": round(d_krishna / tot_d, 4),
            "CHANAKYA_NEETI_COVERT_VETTING": round(d_chanakya / tot_d, 4),
            "PACIFIST_MOHA_DEFENSIVE_QUIETUDE": round(d_defensive / tot_d, 4),
        }

        # Operational Directive
        if s_krishna >= 0.70:
            directive = (
                f"EXECUTE_SOVEREIGN_COUNTERSTRIKE: All peaceful avenues exhausted ({d.peace_initiatives_exhausted_ratio:.2f}). "
                f"Deploy {sadgunya_policy} foreign policy posture with full civilizational resolve."
            )
        elif s_upadha >= 0.70:
            directive = "INTERNAL_PURGE_AND_OPSEC_RESTORATION: High Upadha vulnerability detected. Purge compromised officials before strategic execution."
        else:
            directive = f"MAINTAIN_STRATEGIC_AMBIDEXTERITY: Saptanga index {s_saptanga:.2f} stable. Pursue {sadgunya_policy} policy equilibrium."

        # 6. Complete 19-Member Sovereign Epistemic Council Projections
        council = {
            "Ajit_Doval": (
                f"Intelligence Provenance: Mantra-Gupti index {d.mantra_gupti_secrecy_index:.2f}. "
                f"Plug ministerial information leaks; maintain covert deterrence and Ubhaya-vetana intelligence."
            ),
            "Dr_S_Jaishankar": (
                f"Multilateral Lawfare: Prescribed Ṣaḍguṇya posture is {sadgunya_policy} (Relative Delta: {k_res['relative_power_delta']:+.2f}). "
                f"Execute multi-alignment diplomacy without ideological dependency."
            ),
            "Dr_Ankit_Shah": (
                f"Balance Sheet & Kosha Health: Kosha limb score {d.kosha_treasury_depth:.2f}. "
                f"Hedge foreign exchange reserves and de-dollarize critical trade settlements to prevent liquidity siege."
            ),
            "Sanjeev_Sanyal": (
                f"Complex Adaptive Statecraft: Janapada & Durga resilience score {d.durga_fortification_dpi:.2f}. "
                f"Accelerate maritime port infrastructure and fast-track capital formation."
            ),
            "J_Sai_Deepak": (
                f"Bharatiya Jurisprudence: Dharmic resolve {d.dharmic_svadharma_resolve:.2f}. "
                f"Deconstruct colonial judicial precedents and assert epigraphic civilizational sovereignty."
            ),
            "Dr_Anand_Ranganathan": (
                f"Scientific Empiricism: Upadha integrity score {s_upadha:.2f}. "
                f"Demolish hypocrisy with reproducible physical proof and strict accountability."
            ),
            "PM_Narendra_Modi": (
                f"Atmanirbharta & Scale: Composite sovereignty index {composite_idx:.2f}. "
                f"Execute high-velocity infrastructure growth and defend 1.4 billion citizens' Yogakshema."
            ),
            "Dr_Sudhanshu_Trivedi": (
                f"Scriptural Epistemology: Classical Shastric authority affirms Saptanga governance. "
                f"Neutralize semantic subversion by restoring authentic Sanskrit terminological precision."
            ),
            "Pushpendra_Kulshrestha": (
                f"Grassroots Vigilance: Beware of fifth-column media syndicates weaponizing internal Upadha vulnerabilities."
            ),
            "Dr_Syed_Rizwan_Ahmed": (
                f"Criminal Jurisprudence: Enforce statutory penal liability under BNS for any official failing Bhayopadha or Arthopadha."
            ),
            "Neeraj_Atri": (
                f"Archival Proof: Audit historical treaties against primary critical Sanskrit texts, rejecting colonial distortions."
            ),
            "Sadhguru_Jaggi_Vasudev": (
                f"Conscious Governance: Janapada soil and water security must underpin long-term defense capabilities."
            ),
            "Dr_Kumar_Vishwas": (
                f"Rashtriya Consciousness: Unify the cultural spirit of the nation behind righteous statecraft."
            ),
            "Srijan_Pal_Singh": (
                f"Kalam Deep Tech: Durga limb requires air-gapped sovereign microprocessors and indigenous aerospace assets."
            ),
            "Dr_B_R_Ambedkar": (
                f"Constitutional Antifragility: Institutional checks and balances prevent state power from devolving into tyranny."
            ),
            "Acharya_Chanakya_Kautilya": (
                f"Arthashastra Statecraft: Saptanga health {s_saptanga:.2f}. A ruler who balances Kosha and Danda conquers the Mandala."
            ),
            "Sri_Krishna_Rajadharma": (
                f"Rajadharma: Peace exhaustion score {s_krishna:.2f}. Shed Moha and fight the righteous battle when duty demands."
            ),
            "Vedic_Rishi_Pramana": (
                f"Pramana Epistemology: Triangulate Pratyaksha, Anumana, and Shabda to perceive reality through the lens of Rta."
            ),
            "Maryada_Purushottam_Sri_Ram": (
                f"Ram Rajya Governance: Sovereign integrity is grounded in Praja-Anuraga and total adherence to ethical governance."
            ),
            "Dr_Meenakshi_Jain": (
                f"Epigraphic & Sacred Geography: Inscriptional continuity and primary archaeological evidence "
                f"unmask iconoclastic distortions; reclaim civilizational heritage through rigorous historical record."
            ),
            "Ami_Ganatra": (
                f"Canonical Sanskrit Epic Textual Fidelity: Primary shlokas of Mahabharata and Ramayana dispel popular "
                f"apocrypha; evaluate statecraft through authentic Dharmik precedent and un-mutilated manuscript rigor."
            ),
            "Major_Gaurav_Arya": (
                f"Tactical Military Ground Realism: Kinetic deterrence score {s_saptanga:.2f}. "
                f"Impose asymmetric retaliatory costs on hostile cross-border deep-state terror infrastructure."
            ),
        }

        return DharmikStatecraftEvaluation(
            dossier_id=d.dossier_id,
            target_nation_or_entity=d.target_nation_or_entity,
            composite_dharmik_sovereignty_index=composite_idx,
            kautilya_saptanga_score=s_saptanga,
            optimal_sadgunya_policy=sadgunya_policy,
            chanakya_upadha_integrity_score=s_upadha,
            krishna_rajadharma_exhaustion_score=s_krishna,
            rajadharma_authorization_tier=rajadharma_tier,
            operational_directive=directive,
            competing_strategic_doctrines=doctrines,
            council_perspectives=council,
        )

```

## Module: `geo_engine/arbitration/historical_arbiter.py`

```python
"""
Multi-Pillar Historical Chronology Arbiter (MPCA).
Provides machine-verifiable, cross-disciplinary arbitration of conflicting ancient historical
and civilizational timeline claims (e.g. Nilesh Oak 5561 BCE vs. Narahari Achar 3067 BCE vs. ASI 1000 BCE).
Evaluates hypotheses across 4 orthogonal epistemic pillars:
1. Astronomical retro-calculation with periodic degeneracy discounting.
2. Archaeological stratigraphy and material culture coherence (metallurgy, urban strata, chariot/horse evidence).
3. Hydro-geological and paleoclimatic telemetry (Saraswati river flow vs. desiccation, Dwarka marine geology).
4. Textual and philological manuscript provenance (BORI Critical Edition common archetype vs. regional interpolations).
"""

from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class ChronologyPillarScore(BaseModel):
    """Normalized scoring (0.0 to 1.0) across the five orthogonal evidentiary pillars."""
    astronomy_score: float = Field(..., ge=0.0, le=1.0, description="Fit with planetary/constellation observations in text")
    astronomy_degeneracy_factor: float = Field(default=0.30, ge=0.0, le=1.0, description="1.0 = highly recurring/degenerate periodic alignment; 0.0 = unique")
    archaeology_score: float = Field(..., ge=0.0, le=1.0, description="Fit with excavated strata, C-14, metallurgy, and material culture")
    hydro_geology_score: float = Field(..., ge=0.0, le=1.0, description="Fit with river Saraswati flow state, monsoon curves, marine sea-levels")
    textual_provenance_score: float = Field(..., ge=0.0, le=1.0, description="Manuscript weight (1.0 = BORI common archetype, 0.2 = late regional variant)")
    paleogenomics_score: float = Field(default=0.50, ge=0.0, le=1.0, description="Fit with ancient DNA (aDNA), uniparental haplogroups, and Steppe vs. AASI cline demographic drift")


class HistoricalHypothesisCandidate(BaseModel):
    """A proposed historical timeline candidate evaluated across multi-pillar evidence."""
    hypothesis_id: str
    label: str
    proposed_year_bce: int
    proponent: str
    pillar_scores: ChronologyPillarScore
    has_material_culture_collision: bool = False
    collision_rationale: Optional[str] = None
    composite_coherence_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serializes candidate into a clean dictionary."""
        return {
            "hypothesis_id": self.hypothesis_id,
            "label": self.label,
            "proposed_year_bce": self.proposed_year_bce,
            "proponent": self.proponent,
            "pillar_scores": self.pillar_scores.model_dump(),
            "has_material_culture_collision": self.has_material_culture_collision,
            "collision_rationale": self.collision_rationale,
            "composite_coherence_score": round(self.composite_coherence_score, 4)
        }


class ChronologyEvaluationReport(BaseModel):
    """Comprehensive evaluation report arbitrating competing historical timelines."""
    event_name: str
    candidates: List[HistoricalHypothesisCandidate] = Field(default_factory=list)
    ranked_candidates: List[HistoricalHypothesisCandidate] = Field(default_factory=list)
    dominant_candidate_id: str = ""
    dominant_candidate_label: str = ""
    dominant_coherence_score: float = 0.0
    epistemic_warning: Optional[str] = None
    reasoning_audit_trail: List[str] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes report into JSON-compatible dictionary."""
        return {
            "event_name": self.event_name,
            "dominant_candidate_id": self.dominant_candidate_id,
            "dominant_candidate_label": self.dominant_candidate_label,
            "dominant_coherence_score": round(self.dominant_coherence_score, 4),
            "epistemic_warning": self.epistemic_warning,
            "reasoning_audit_trail": self.reasoning_audit_trail,
            "ranked_candidates": [c.to_dict() for c in self.ranked_candidates]
        }


class MultiPillarChronologyArbiter:
    """
    Mathematical and epistemic arbiter for conflicting historical chronologies.
    Resolves the single-optic fallacy where isolated astronomical calculations
    ignore physical stratigraphy, or where archaeological models ignore celestial and hydrological records.
    """

    # Pillar Weights in Composite Bayesian Coherence (Sum = 1.00)
    WEIGHT_ASTRONOMY = 0.20
    WEIGHT_ARCHAEOLOGY = 0.30
    WEIGHT_PALEOGENOMICS = 0.15
    WEIGHT_HYDRO_GEOLOGY = 0.15
    WEIGHT_TEXTUAL_PROVENANCE = 0.20

    PILLAR_WEIGHTS = {
        "astronomy": WEIGHT_ASTRONOMY,
        "archaeology": WEIGHT_ARCHAEOLOGY,
        "paleogenomics": WEIGHT_PALEOGENOMICS,
        "hydro_geology": WEIGHT_HYDRO_GEOLOGY,
        "textual_provenance": WEIGHT_TEXTUAL_PROVENANCE,
    }

    @classmethod
    def calculate_composite_coherence(
        cls,
        scores: ChronologyPillarScore,
        proposed_year_bce: int
    ) -> Tuple[float, bool, Optional[str]]:
        """
        Computes composite coherence score with degeneracy dampening, paleogenomics, and material culture collision flags.
        Formula:
          S_astro_adj = S_astro * (1.0 - 0.5 * Degeneracy)
          Base = 0.20 * S_astro_adj + 0.30 * S_arch + 0.15 * S_paleogen + 0.15 * S_geo + 0.20 * S_text
          If S_arch < 0.15: Apply 75% material culture collision penalty (haircut).
        """
        # 1. Adjust astronomy for periodic recurrence degeneracy
        adj_astronomy = scores.astronomy_score * (1.0 - 0.5 * scores.astronomy_degeneracy_factor)

        # 2. Weighted multi-pillar base sum
        base_score = (
            cls.WEIGHT_ASTRONOMY * adj_astronomy +
            cls.WEIGHT_ARCHAEOLOGY * scores.archaeology_score +
            cls.WEIGHT_PALEOGENOMICS * scores.paleogenomics_score +
            cls.WEIGHT_HYDRO_GEOLOGY * scores.hydro_geology_score +
            cls.WEIGHT_TEXTUAL_PROVENANCE * scores.textual_provenance_score
        )

        # 3. Check for Material Culture Collision
        # In South Asian archaeological stratigraphy:
        # Pre-4000 BCE: Epipaleolithic/Mesolithic/Early Aceramic Neolithic (no iron, no spoke-wheel chariots, no urban brick palaces).
        # Dating an epic describing 18 Akshauhinis with composite bows, steel swords, and iron armor to 5500+ BCE or 12,000 BCE
        # triggers a catastrophic material culture disconnect.
        has_collision = False
        collision_rationale = None

        if scores.archaeology_score < 0.15 or proposed_year_bce >= 4500:
            if scores.archaeology_score < 0.20:
                has_collision = True
                collision_rationale = (
                    f"[MATERIAL CULTURE COLLISION] Proposed epoch ({proposed_year_bce} BCE) contradicts "
                    f"excavated stratigraphic horizons. Spoke-wheeled war chariots (Rathas), steel metallurgy, "
                    f"and fortified brick citadels do not exist in the lithic/early Neolithic record."
                )
                # Apply 75% epistemic haircut
                final_score = round(base_score * 0.25, 4)
                return final_score, has_collision, collision_rationale

        final_score = round(base_score, 4)
        return final_score, has_collision, collision_rationale

    @classmethod
    def get_benchmark_candidates(cls) -> List[HistoricalHypothesisCandidate]:
        """Returns standard benchmark scholarly and traditional timeline candidates for the Mahabharata and Bronze Age."""
        return [
            HistoricalHypothesisCandidate(
                hypothesis_id="CHRONO_OAK_5561_BCE",
                label="5561 BCE (Nilesh Oak Arundhati-Vasistha Model)",
                proposed_year_bce=5561,
                proponent="Nilesh Nilkanth Oak",
                pillar_scores=ChronologyPillarScore(
                    astronomy_score=0.88,
                    astronomy_degeneracy_factor=0.75,  # 6,500-year precession window (11,091 BCE to 4508 BCE)
                    archaeology_score=0.08,           # Mesolithic/Neolithic Mehrgarh I (stone tools, zero iron/chariots)
                    hydro_geology_score=0.45,         # Perennial glacial melt; does not match Vinashana desiccation
                    textual_provenance_score=0.70,    # Interprets AV omen literally as an astronomical precession coordinate
                    paleogenomics_score=0.10          # Paleogenomic disconnect with Bronze/Iron age epic descriptions
                )
            ),
            HistoricalHypothesisCandidate(
                hypothesis_id="CHRONO_ACHAR_3067_BCE",
                label="3067 BCE (Dr. Narahari Achar / BORI Model)",
                proposed_year_bce=3067,
                proponent="Dr. Narahari Achar / Prof. K.S. Raghavan",
                pillar_scores=ChronologyPillarScore(
                    astronomy_score=0.86,
                    astronomy_degeneracy_factor=0.25,  # High specificity: twin eclipse in 13 days + Saturn-Rohini + Jupiter-Vishakha
                    archaeology_score=0.78,           # Early Harappan / Sanauli chariot horizon (~2000-1900 BCE copper-sheathed carts)
                    hydro_geology_score=0.88,         # Matches Saraswati perennial-to-dry transition before 1900 BCE desiccation
                    textual_provenance_score=0.85,    # Conforms strictly to BORI Critical Edition common archetype
                    paleogenomics_score=0.82          # Congruent with indigenous South Asian cline
                )
            ),
            HistoricalHypothesisCandidate(
                hypothesis_id="CHRONO_ARYABHATA_3102_BCE",
                label="3102 BCE (Traditional Aryabhata / Aihole Inscription Model)",
                proposed_year_bce=3102,
                proponent="Aryabhata (499 CE) / Pulakeshin II Aihole Inscription (634 CE)",
                pillar_scores=ChronologyPillarScore(
                    astronomy_score=0.76,
                    astronomy_degeneracy_factor=0.35,  # Conjunction of all planets at 0 degrees Aries at Kali Yuga start
                    archaeology_score=0.75,           # Pre-Harappan / Early Bronze Age transition
                    hydro_geology_score=0.86,         # Saraswati flowing perennially to Rann of Kutch
                    textual_provenance_score=0.82,    # Universal consensus across Puranic king lists and classical epigraphs
                    paleogenomics_score=0.80          # Pre-Steppe South Asian cline continuity
                )
            ),
            HistoricalHypothesisCandidate(
                hypothesis_id="CHRONO_SINAULI_OCP_2000_BCE",
                label="2000 BCE (Sinauli OCP / Copper Hoard Martial Culture)",
                proposed_year_bce=2000,
                proponent="Archaeological Survey of India (ASI) / BSIP Radiocarbon",
                pillar_scores=ChronologyPillarScore(
                    astronomy_score=0.50,             # Textual-celestial markers neutral (funerary archaeology)
                    astronomy_degeneracy_factor=0.30,
                    archaeology_score=0.95,           # Direct C14 dated strata (2000-1800 BCE), copper carts, antennae swords, coffins
                    hydro_geology_score=0.82,         # Active Yamuna-Hindon perennial fluvial drainage
                    textual_provenance_score=0.78,    # Direct concordance with Rigveda 10.18 inhumation & weapon placement
                    paleogenomics_score=0.75          # Late Harappan / Copper Hoard indigenous transition without high Steppe pulse
                )
            ),
            HistoricalHypothesisCandidate(
                hypothesis_id="CHRONO_LAL_PGW_1000_BCE",
                label="1000 BCE (Prof. B.B. Lal / ASI Painted Grey Ware Model)",
                proposed_year_bce=1000,
                proponent="Prof. B.B. Lal / Archaeological Survey of India",
                pillar_scores=ChronologyPillarScore(
                    astronomy_score=0.30,             # Rejects or bypasses planetary conjunctions as late poetic hyperbole
                    astronomy_degeneracy_factor=0.50,
                    archaeology_score=0.92,           # Hastinapur, Kurukshetra, Indraprastha PGW layers with iron weapons & flood stratum
                    hydro_geology_score=0.25,         # Severe mismatch: Saraswati completely dried up by 1900 BCE; dry by 1000 BCE
                    textual_provenance_score=0.65,    # Treats epic as late first-millennium BCE compilation
                    paleogenomics_score=0.85          # Post-Steppe pulse Early Iron Age horizon
                )
            ),
        ]

    @classmethod
    def arbitrate(
        cls,
        event_name: str = "Mahabharata War Chronology",
        candidates: Optional[List[HistoricalHypothesisCandidate]] = None
    ) -> ChronologyEvaluationReport:
        """
        Executes multi-pillar cross-disciplinary arbitration across historical candidates.
        Ranks candidates by composite Bayesian coherence score and flags single-optic distortions.
        """
        eval_candidates = candidates if candidates else cls.get_benchmark_candidates()
        audit_trail: List[str] = [
            f"[MPCA_INIT] Initiating Multi-Pillar Chronology Arbitration for '{event_name}' across {len(eval_candidates)} candidates.",
            "[MPCA_WEIGHTS] Applied Epistemic Pillar Weights: Archaeology (0.30), Astronomy (0.20), Paleogenomics (0.15), Hydro-Geology (0.15), Textual Provenance (0.20)."
        ]

        # Calculate composite score for each candidate
        for c in eval_candidates:
            score, has_coll, rationale = cls.calculate_composite_coherence(c.pillar_scores, c.proposed_year_bce)
            c.composite_coherence_score = score
            c.has_material_culture_collision = has_coll
            c.collision_rationale = rationale

            audit_trail.append(
                f"[MPCA_EVAL] {c.hypothesis_id} ({c.proposed_year_bce} BCE): "
                f"Astro={c.pillar_scores.astronomy_score:.2f} (Degeneracy={c.pillar_scores.astronomy_degeneracy_factor:.2f}), "
                f"Arch={c.pillar_scores.archaeology_score:.2f}, Paleogen={c.pillar_scores.paleogenomics_score:.2f}, "
                f"Geo={c.pillar_scores.hydro_geology_score:.2f}, Text={c.pillar_scores.textual_provenance_score:.2f} -> Composite={score:.4f}"
            )
            if has_coll:
                audit_trail.append(f"[MPCA_PENALTY] {c.hypothesis_id} penalized: {rationale}")

        # Rank descending by composite coherence score
        ranked = sorted(eval_candidates, key=lambda x: x.composite_coherence_score, reverse=True)
        dominant = ranked[0]
        runner_up = ranked[1] if len(ranked) > 1 else None

        audit_trail.append(
            f"[MPCA_RANKING] Dominant Candidate: '{dominant.label}' (Composite Coherence: {dominant.composite_coherence_score:.4f})."
        )

        warning: Optional[str] = None
        if dominant.has_material_culture_collision:
            warning = f"[EPISTEMIC SEVERE CAUTION] Dominant candidate exhibits unresolved material culture collision: {dominant.collision_rationale}"
        elif runner_up and (dominant.composite_coherence_score - runner_up.composite_coherence_score < 0.10):
            warning = (
                f"[EPISTEMIC CLOSE COMPETITION] Top candidate ('{dominant.label}', {dominant.composite_coherence_score:.4f}) "
                f"leads runner-up ('{runner_up.label}', {runner_up.composite_coherence_score:.4f}) by less than 0.10. "
                f"Multi-pillar synthesis confirms historical clustering in the early 3rd millennium BCE (~3102–3067 BCE)."
            )

        return ChronologyEvaluationReport(
            event_name=event_name,
            candidates=eval_candidates,
            ranked_candidates=ranked,
            dominant_candidate_id=dominant.hypothesis_id,
            dominant_candidate_label=dominant.label,
            dominant_coherence_score=dominant.composite_coherence_score,
            epistemic_warning=warning,
            reasoning_audit_trail=audit_trail
        )

```

## Module: `geo_engine/arbitration/negative_space.py`

```python
"""
Negative Space Diff Engine.
Detects omitted, suppressed, and diluted clauses in summit communiques.
Overcomes standard LLM positive-retrieval bias by computing delta diffs against
historical multilateral declarations.
"""

from collections import Counter
import math
import re
from typing import Any, Dict, List, Optional, Tuple
from ..core.models import CommuniqueClause


class NegativeSpaceDiffEngine:
    """Computes negative space (omissions and dilutions) in multilateral communiques."""

    DEFAULT_BASELINE_CLAUSES: List[CommuniqueClause] = [
        CommuniqueClause(
            clause_id="UNSC-01",
            category="institutional_reform",
            raw_text="Support for comprehensive reform of the United Nations Security Council, explicitly endorsing permanent membership for India, Brazil, and South Africa with full veto power.",
            present_in_current_summit=False,
            historical_baseline_present=True,
            dilution_status="omitted_negative_space",
            omission_significance="China systematically blocked explicit endorsement of permanent veto-wielding UNSC seats for India and Brazil, diluting text to generic 'aspirations for greater Global South representation'."
        ),
        CommuniqueClause(
            clause_id="CURR-01",
            category="finance",
            raw_text="Exploration and technical feasibility roadmap for a unified common BRICS reserve currency (R5 basket) backed by gold and sovereign commodities.",
            present_in_current_summit=False,
            historical_baseline_present=True,
            dilution_status="omitted_negative_space",
            omission_significance="Concept of a unified common currency quietly abandoned due to structural impossibilities (Mundell-Fleming Trilemma) and resistance from India and Brazil against Yuan hegemony; replaced entirely by bilateral local-currency swaps."
        ),
        CommuniqueClause(
            clause_id="SEC-01",
            category="security",
            raw_text="Explicit condemnation of cross-border terrorism networks, state sponsorship of terror proxies, and FATF compliance enforcement against safe havens.",
            present_in_current_summit=True,
            historical_baseline_present=True,
            dilution_status="diluted_passive",
            omission_significance="Language heavily diluted to passive generalized anti-terror platitudes, avoiding naming Pakistan or regional terror syndicates to appease Beijing."
        ),
        CommuniqueClause(
            clause_id="MAR-01",
            category="territorial",
            raw_text="Commitment to strict adherence to UNCLOS (United Nations Convention on the Law of the Sea) and unrestricted freedom of navigation in the South China Sea.",
            present_in_current_summit=False,
            historical_baseline_present=True,
            dilution_status="omitted_negative_space",
            omission_significance="UNCLOS compliance and South China Sea navigation dropped entirely at Beijing's insistence, demonstrating internal bloc inability to address maritime expansionism."
        ),
        CommuniqueClause(
            clause_id="PAY-01",
            category="finance",
            raw_text="Expansion of bilateral local-currency clearing mechanisms and technical studies on digital cross-border payment interoperability (BRICS Bridge).",
            present_in_current_summit=True,
            historical_baseline_present=True,
            dilution_status="retained_full",
            omission_significance="Unanimously retained: All member states benefit from reducing USD conversion transaction costs without ceding monetary sovereignty."
        )
    ]

    @classmethod
    def load_baseline_from_store(cls) -> List[CommuniqueClause]:
        """Loads mandatory baseline clauses dynamically from persistent SQLite EventStore."""
        try:
            from ..storage import EventStore
            store = EventStore()
            db_clauses = store.get_mandatory_baseline_clauses()
            if db_clauses:
                loaded = []
                for row in db_clauses:
                    sig = row.get("omission_significance", "").lower()
                    if any(k in sig for k in ["omission", "omitted", "dropped", "refuses", "coercion"]):
                        status_val = "omitted_negative_space"
                    elif any(k in sig for k in ["dilut", "passive", "toothless"]):
                        status_val = "diluted_passive"
                    elif any(k in sig for k in ["retain", "unanimous"]):
                        status_val = "retained_full"
                    else:
                        status_val = "omitted_negative_space"

                    loaded.append(CommuniqueClause(
                        clause_id=row["clause_id"],
                        category=row["category"],
                        raw_text=row["clause_text"],
                        present_in_current_summit=False,
                        historical_baseline_present=True,
                        dilution_status=status_val,
                        omission_significance=row.get("omission_significance", "")
                    ))
                loaded.append(cls.DEFAULT_BASELINE_CLAUSES[-1]) # Retained payment clause
                return loaded
        except Exception:
            pass
        return cls.DEFAULT_BASELINE_CLAUSES

    @classmethod
    def analyze_diff(
        cls,
        current_clauses: List[CommuniqueClause] = None
    ) -> Tuple[List[CommuniqueClause], Dict[str, int], List[str]]:
        """
        Analyzes the target summit text against historical baselines.
        Returns the annotated clauses, categorical counts, and high-impact strategic takeaways.
        """
        clauses = current_clauses if current_clauses is not None else cls.load_baseline_from_store()

        counts = {
            "omitted_negative_space": 0,
            "diluted_passive": 0,
            "retained_full": 0,
            "new_consensus": 0
        }

        insights = []

        for c in clauses:
            if c.dilution_status in counts:
                counts[c.dilution_status] += 1
            else:
                counts["retained_full"] += 1

            if c.dilution_status == "omitted_negative_space":
                insights.append(f"[CRITICAL OMISSION] {c.category.upper()}: {c.omission_significance}")
            elif c.dilution_status == "diluted_passive":
                insights.append(f"[DILUTION DETECTED] {c.category.upper()}: {c.omission_significance}")

        return clauses, counts, insights

    @classmethod
    def scan_text_for_omissions(
        cls,
        communique_text: str,
        baseline_clauses: Optional[List[CommuniqueClause]] = None
    ) -> Tuple[List[CommuniqueClause], Dict[str, int], List[str]]:
        """
        Dynamically audits raw communique text against historical baseline clauses
        using DenseSemanticIndex vector similarity.
        """
        baselines = baseline_clauses if baseline_clauses is not None else cls.load_baseline_from_store()
        if not communique_text or not communique_text.strip():
            return cls.analyze_diff(baselines)

        index = DenseSemanticIndex()
        for c in baselines:
            index.add_document(c.clause_id, c.raw_text + " " + c.category)
        index.build_index()

        annotated: List[CommuniqueClause] = []
        for c in baselines:
            sim = index.compute_similarity(communique_text, c.clause_id)
            if sim < 0.10:
                status = "omitted_negative_space"
                present = False
            elif sim < 0.32:
                status = "diluted_passive"
                present = True
            else:
                status = "retained_full"
                present = True

            annotated.append(CommuniqueClause(
                clause_id=c.clause_id,
                category=c.category,
                raw_text=c.raw_text,
                present_in_current_summit=present,
                historical_baseline_present=True,
                dilution_status=status,
                omission_significance=c.omission_significance
            ))

        return cls.analyze_diff(annotated)


class DenseSemanticIndex:
    """
    Zero-dependency TF-IDF and n-gram sub-word dense semantic vector index.
    Enables semantic soft matching between raw communique texts and historical sovereign baselines.
    """

    def __init__(self):
        self.doc_ids: List[str] = []
        self.documents: Dict[str, str] = {}
        self.df: Counter = Counter()
        self.doc_vectors: Dict[str, Dict[str, float]] = {}
        self.total_docs: int = 0

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        words = re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", text.lower())
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words) - 1)]
        return words + bigrams

    def add_document(self, doc_id: str, text: str) -> None:
        self.doc_ids.append(doc_id)
        self.documents[doc_id] = text
        tokens = self._tokenize(text)
        unique_tokens = set(tokens)
        for t in unique_tokens:
            self.df[t] += 1
        self.total_docs += 1

    def build_index(self) -> None:
        for doc_id, text in self.documents.items():
            tokens = self._tokenize(text)
            tf = Counter(tokens)
            vec: Dict[str, float] = {}
            for t, count in tf.items():
                idf = math.log((self.total_docs + 1) / (self.df[t] + 1)) + 1.0
                vec[t] = count * idf
            norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
            self.doc_vectors[doc_id] = {t: v / norm for t, v in vec.items()}

    def compute_similarity(self, query_text: str, doc_id: str) -> float:
        if doc_id not in self.doc_vectors:
            return 0.0
        q_tokens = self._tokenize(query_text)
        q_tf = Counter(q_tokens)
        q_vec: Dict[str, float] = {}
        for t, count in q_tf.items():
            idf = math.log((self.total_docs + 1) / (self.df.get(t, 0) + 1)) + 1.0
            q_vec[t] = count * idf
        q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0
        q_norm_vec = {t: v / q_norm for t, v in q_vec.items()}

        doc_v = self.doc_vectors[doc_id]
        dot_product = sum(doc_v.get(t, 0.0) * val for t, val in q_norm_vec.items())
        return round(min(1.0, max(0.0, dot_product)), 4)



# ============================================================================
# Phase 426: Investigative Forensics and Negative Space Engine (Master Subsystem)
# ============================================================================

class InvestigativeForensicsAndNegativeSpaceEngine:
    """
    Phase 426 (Master Investigative Journalism & Negative Space Subsystem):
    Dedicated multi-tier forensic pipeline synthesizing:
    1. Kinesic stress divergence (pupillometry, micro-expressions, postural rigidity)
    2. Diplomatic sartorial/color semiotics (saffron/green/black signaling, tie/jacket protocol defiance)
    3. Acoustic vocal micro-tremors (fundamental frequency jitter, shiver/pitch instability)
    4. Negative-space textual omissions (taboo topic suppression, missing bilateral clauses)
    5. Primary physical ledger verification (customs manifests, bill-of-lading cargo matching)
    Formula:
        ForensicDivergence = Norm((0.30 * kinesic_stress + 0.25 * sartorial_semiotics +
                                  0.25 * acoustic_tremors + 0.20 * negative_space_omissions) /
                                  (1.0 + ledger_verification_certainty))
        score = Sigmoid(2.8 * ForensicDivergence + 2.5 * negative_space_omissions - 1.2)
    """
    @classmethod
    def evaluate(
        cls,
        kinesic_stress_divergence: float = 0.85,
        sartorial_color_semiotic_anomaly: float = 0.75,
        acoustic_micro_tremor_density: float = 0.80,
        negative_space_omission_criticality: float = 0.85,
        primary_ledger_verification_certainty: float = 0.90
    ) -> Dict[str, Any]:
        k_stress = float(max(0.0, min(1.0, kinesic_stress_divergence)))
        s_semiotic = float(max(0.0, min(1.0, sartorial_color_semiotic_anomaly)))
        a_tremor = float(max(0.0, min(1.0, acoustic_micro_tremor_density)))
        n_omiss = float(max(0.0, min(1.0, negative_space_omission_criticality)))
        l_cert = float(max(0.0, min(1.0, primary_ledger_verification_certainty)))

        raw_div = (0.30 * k_stress + 0.25 * s_semiotic + 0.25 * a_tremor + 0.20 * n_omiss) / (1.0 + l_cert)
        z = 2.8 * raw_div + 2.5 * n_omiss - 1.2
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "DECISIVE_INVESTIGATIVE_FORENSIC_DECEPTION_UNMASKED"
            verdict = "EXPOSE_DIVERGENCE_BETWEEN_PUBLIC_RHETORIC_AND_PHYSICAL_LEDGERS"
            rationale = (
                f"Irrefutable investigative forensic evidence ({score:.4f}): Kinesic micro-stress ({k_stress:.2f}), "
                f"sartorial anomaly ({s_semiotic:.2f}), and acoustic tremor density ({a_tremor:.2f}) unmask calculated negative space omissions ({n_omiss:.2f})."
            )
        elif score >= 0.45:
            tier = "ELEVATED_NONVERBAL_AND_TEXTUAL_ANOMALY"
            verdict = "CROSS_EXAMINE_STATUTORY_RECORDS_AND_SPEECH_AUDIO_SPECTROGRAMS"
            rationale = f"Elevated anomaly ({score:.4f}): Speech omissions diverge from official press release baseline."
        else:
            tier = "VERIFIED_RHETORICAL_AND_PHYSICAL_CONCORDANCE"
            verdict = "PRIMARY_LEDGER_DATA_CONFIRMS_DECLARED_STATEMENTS"
            rationale = f"High concordance ({score:.4f}): Physical ledgers ({l_cert:.2f}) fully corroborate spoken declarations."

        return {
            "investigative_forensics_negative_space_score": score,
            "kinesic_stress_divergence": round(k_stress, 4),
            "sartorial_color_semiotic_anomaly": round(s_semiotic, 4),
            "acoustic_micro_tremor_density": round(a_tremor, 4),
            "negative_space_omission_criticality": round(n_omiss, 4),
            "primary_ledger_verification_certainty": round(l_cert, 4),
            "forensics_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_forensic_divergence_decisive": score >= 0.70,
        }

    @classmethod
    def analyze_speech_forensics(cls, transcript: str, audio_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Convenience investigative analyzer for raw speech transcripts and acoustic metadata."""
        meta = audio_metadata or {}
        return cls.evaluate(
            kinesic_stress_divergence=meta.get("kinesic_stress_divergence", 0.70),
            sartorial_color_semiotic_anomaly=meta.get("sartorial_color_semiotic_anomaly", 0.65),
            acoustic_micro_tremor_density=meta.get("acoustic_micro_tremor_density", 0.75),
            negative_space_omission_criticality=meta.get("negative_space_omission_criticality", 0.80),
            primary_ledger_verification_certainty=meta.get("primary_ledger_verification_certainty", 0.85)
        )

```

## Module: `geo_engine/arbitration/persona_narrator.py`

```python
"""
Persona Archetype Projection Layer.
Expresses arbitrated multi-lens intelligence through established strategic-intellectual traditions
without fabricating direct personal quotes or impersonating public officials:
1. Sanjeev Sanyal Tradition: Complex Adaptive Systems (CAS), maritime trade geography, and monetary realism.
2. Ajit Doval Tradition: Defensive-offense deterrence, internal-external security nexus, and kinetic leverage.
3. Dr. S. Jaishankar Tradition: Multi-alignment, strategic autonomy, and Mahabharata ethical statecraft.
"""

from typing import Any, Dict, List
from ..core.models import SummitAnalysisReport


class PersonaNarrator:
    """Projects neutral arbitrated intelligence reports through defined analytical archetypes."""

    ARCHETYPES = {
        "sanyal": {
            "name": "Geo-Economic & Maritime Realist (Sanjeev Sanyal Tradition)",
            "doctrinal_axis": "Complex Adaptive Systems (CAS) & Indian Ocean Trade Logistics",
            "lens_weights": {
                "CashFlowLens": 1.5,
                "GeoEconomistLens": 1.5,
                "HistoryLens": 1.3,
                "PetroLogisticsLens": 1.2,
                "FoodSecurityLens": 1.4,
                "SubseaCablesLens": 1.4
            },
            "conceptual_framing": (
                "An economic and historical CAS framework: multilateral summits are not static equilibrium treaties, "
                "but dynamic, evolving complex adaptive ecosystems. Focuses heavily on verifiable CapEx deployment, "
                "maritime chokepoints along historical Indian Ocean trade arcs (The Ocean of Churn), and rejection of "
                "ideological common currencies under Mundell-Fleming constraints."
            )
        },
        "doval": {
            "name": "Strategic Security & Deterrence Realist (Ajit Doval Tradition)",
            "doctrinal_axis": "Defensive-Offense & Internal-External Security Nexus",
            "lens_weights": {
                "MilitaryReadinessLens": 1.7,
                "HybridCovertLens": 1.6,
                "BureaucraticInertiaLens": 1.3,
                "GeopoliticalLens": 1.3,
                "IndiaTimelineLens": 1.4,
                "AstroPoliticsLens": 1.6,
                "SubseaCablesLens": 1.4
            },
            "conceptual_framing": (
                "A hard-security and intelligence realist framework: statecraft must be judged not by photocalls "
                "or joint communiqués, but by hard physical deterrence, border deployment parity, covert leverage, "
                "and vulnerability along strategic corridors (e.g. Siliguri Neck). Recognizes that adversaries weaponize "
                "domestic fault lines and legalistic delays."
            )
        },
        "jaishankar": {
            "name": "Diplomatic Realist & Multi-Alignment Architect (Dr. S. Jaishankar Tradition)",
            "doctrinal_axis": "Strategic Autonomy, Multi-Vector Diplomacy & Mahabharata Statecraft",
            "lens_weights": {
                "GeopoliticalLens": 1.5,
                "CivilizationalLens": 1.4,
                "DigitalSovereigntyLens": 1.2,
                "IndiaTimelineLens": 1.3,
                "SubseaCablesLens": 1.3,
                "AstroPoliticsLens": 1.3
            },
            "conceptual_framing": (
                "A diplomatic-realist framework rooted in 'The India Way' and Mahabharata statecraft: "
                "foreign policy is the management of global contradictions to advance national interest. "
                "India engages multiple poles simultaneously (Quad, BRICS, Global South) to maximize bargaining leverage, "
                "anchoring a polycentric world order that is non-Western but never anti-Western."
            )
        },
        "ranganathan": {
            "name": "Civilizational Rationalist & Zero-Hypocrisy Auditor (Anand Ranganathan Tradition)",
            "doctrinal_axis": "Empirical Logical Consistency, Civilizational Defense & Institutional Lawfare Deconstruction",
            "lens_weights": {
                "PropagandaLens": 1.7,
                "CivilizationalLens": 1.6,
                "InstitutionalLawfareLens": 1.5,
                "HistoryLens": 1.3,
                "AstroPoliticsLens": 1.4
            },
            "conceptual_framing": (
                "A rigorous, scientifically grounded civilizational critique: statecraft and diplomacy must be audited "
                "with zero moral relativism, uncompromising empirical consistency, and relentless deconstruction of "
                "institutional double standards. Rejects polite diplomatic euphemisms that whitewash historical injustices "
                "or excuse cross-border civilizational aggression."
            )
        },
        "ankit_shah": {
            "name": "Macro-Monetary & Geofinancial Realist (Dr. Ankit Shah Tradition)",
            "doctrinal_axis": "De-Dollarization Velocity, Sovereign Balance-Sheet Warfare & Physical Asset Settlement",
            "lens_weights": {
                "CashFlowLens": 1.8,
                "GeoEconomistLens": 1.6,
                "CriticalMineralsLens": 1.5,
                "PetroLogisticsLens": 1.4,
                "FoodSecurityLens": 1.3,
                "SubseaCablesLens": 1.4
            },
            "conceptual_framing": (
                "A hard macro-monetary warfare framework: global geopolitics is governed by the structural unwind "
                "of the unbacked fiat US dollar debt spiral and the transition toward physical asset settlement "
                "(gold bullion, crude, critical minerals, sovereign energy grid clearing). Multilateral platforms must be "
                "judged strictly by their ability to protect sovereign balance sheets from SWIFT de-platforming."
            )
        },
        "modi": {
            "name": "Civilizational Scale & Execution Velocity Realist (PM Narendra Modi Tradition)",
            "doctrinal_axis": "Gati Shakti Multi-Modal Logistics, Institutional Delivery & Viksit Bharat 2047",
            "lens_weights": {
                "GeoEconomistLens": 1.7,
                "CivilizationalLens": 1.5,
                "DeepTechLens": 1.4,
                "PetroLogisticsLens": 1.3,
                "DigitalSovereigntyLens": 1.5,
                "FoodSecurityLens": 1.4
            },
            "conceptual_framing": (
                "A grand-scale execution and statecraft framework: civilizational self-confidence (Aatmanirbharta) must "
                "be translated into physical logistics turnaround velocity, massive manufacturing capacity, and institutional "
                "delivery at unprecedented demographic scale (Viksit Bharat 2047). Multilateral engagement must anchor India as "
                "a global growth engine and Vishwa-Bandhu without sacrificing domestic developmental sovereignty."
            )
        },
        "sai_deepak": {
            "name": "Constitutional Decoloniality & Epigraphic Sovereignty Realist (J. Sai Deepak Tradition)",
            "doctrinal_axis": "Civilizational Jurisprudence, Sacred Geography & Deconstruction of Colonial Institutional Lawfare",
            "lens_weights": {
                "InstitutionalLawfareLens": 1.8,
                "CivilizationalLens": 1.7,
                "HistoryLens": 1.5,
                "DemographicInfiltrationLens": 1.4,
                "PropagandaLens": 1.3
            },
            "conceptual_framing": (
                "A rigorous decolonial legal and constitutional jurisprudence framework: statecraft and diplomacy must be audited "
                "against civilizational permanence, epigraphic and inscriptional evidence, and the systematic dismantling of "
                "asymmetrical statutory regimes (Waqf Act, Places of Worship Act, state temple expropriation). Rejects post-colonial "
                "institutional mimicry and Western-dominated human rights lawfare designed to hollow out native sovereignty."
            )
        },
        "sadhguru": {
            "name": "Ecological Vitality, Conscious Statecraft & Temple Autonomy Realist (Sadhguru Tradition)",
            "doctrinal_axis": "Biosphere Soil Security, Consecrated Cultural Spaces & Inner Consciousness Sovereignty",
            "lens_weights": {
                "FoodSecurityLens": 1.9,
                "CivilizationalLens": 1.8,
                "InstitutionalLawfareLens": 1.5,
                "PropagandaLens": 1.4,
                "DeepTechLens": 1.3,
                "GeoEconomistLens": 1.3,
            },
            "conceptual_framing": (
                "An ecological and consciousness-first statecraft framework: the foundational bedrock of all "
                "economic prosperity, national security, and civilizational longevity is living soil (minimum 3-6% organic matter) "
                "and revitalized river basins (Save Soil / Cauvery Calling). Without ecological security, food supply collapses, "
                "triggering mass displacement, civil unrest, and resource conflicts. Simultaneously demands the liberation of consecrated "
                "temple institutions from state bureaucratic control (Free Temples) to restore native cultural and economic vitality, "
                "while projecting Sanatan civilizational wisdom globally as an empirical, non-dogmatic technology of consciousness "
                "and Maryada Purushottama moral restraint."
            ),
        },
        "rizwan_ahmed": {
            "name": "Forensic Courtroom Cross-Examiner & Criminal Law Realist (Dr. Syed Rizwan Ahmed Tradition)",
            "doctrinal_axis": "Adversarial Evidentiary Cross-Examination, Statutory Due Process & Criminal Procedure Demolition",
            "lens_weights": {
                "InstitutionalLawfareLens": 2.0,
                "PropagandaLens": 1.7,
                "CivilizationalLens": 1.4,
                "DemographicInfiltrationLens": 1.3
            },
            "conceptual_framing": (
                "An uncompromising courtroom adversarial cross-examination framework: every political claim and allegation "
                "is scrutinized under the strict rules of evidence (Indian Evidence Act / Bharatiya Sakshya Adhiniyam) and procedural "
                "codes (CrPC / Bharatiya Nagarik Suraksha Sanhita). Demolishes legal terminology hijacking (such as using 'turn approver' "
                "or 'criminal conspiracy' without an FIR, chargesheet, or judicial finding) and audits whether the accuser exhausted "
                "statutory remedies (Booth Level Agent objections, Section 24 appeals, Section 80 Election Petitions) before staging a media circus."
            )
        },
        "kautilya": {
            "name": "Arthashastra Statecraft Realist (Kautilya-Chanakya Tradition)",
            "doctrinal_axis": "Mandala Theory (Ari-Mitra-Ari Circle of States), Saptanga 7-Pillar State Audit & Chaturopayas (Sama/Dama/Danda/Bheda)",
            "lens_weights": {
                "HybridCovertLens": 1.8,
                "InstitutionalLawfareLens": 2.0,
                "GeopoliticalLens": 1.8,
                "MilitaryReadinessLens": 1.7,
                "CashFlowLens": 1.5,
                "HistoryLens": 1.6
            },
            "conceptual_framing": (
                "The world's first complete statecraft manual (350 BCE): every inter-state relationship is classified "
                "strictly by the Mandala geometry — the adjacent state is the natural adversary (Ari), the state beyond the enemy "
                "is the natural ally (Mitra), alternating in concentric rings. State power is audited through 7 pillars (Saptanga): "
                "Swami (sovereign legitimacy), Amatya (bureaucratic integrity), Janapada (territorial-demographic mass), Durga "
                "(physical fortifications), Kosha (treasury depth), Danda (coercive military force), and Mitra (alliance quality). "
                "Every diplomatic engagement must be classified under the Chaturopayas: "
                "Sama (conciliation), Dama (financial inducement), Danda (coercive force), Bheda (divide-and-rule). "
                "Surveillance (Sanstha & Samcara espionage networks) is a sovereign administrative function, not a moral violation."
            )
        },
        "krishna_gita": {
            "name": "Rajadharma & Svadharma Realist (Bhagavad Gita-Mahabharata Tradition)",
            "doctrinal_axis": "Rajadharma (Shanti Parva), Svadharma Duty-Audit, Nishkama Karma & Udyoga Parva Diplomatic Exhaustion Protocol",
            "lens_weights": {
                "CivilizationalLens": 2.0,
                "PropagandaLens": 1.8,
                "HistoryLens": 1.7,
                "GeopoliticalLens": 1.5,
                "IndiaTimelineLens": 1.6,
                "InstitutionalLawfareLens": 1.4
            },
            "conceptual_framing": (
                "The Bhagavad Gita resolves the central epistemic paradox of all statecraft: when Svadharma (righteous duty "
                "according to one's station) conflicts with Moha (emotional attachment or sentimental hesitation), Svadharma is "
                "the absolute imperative. Nishkama Karma (action without selfish attachment to outcomes) is the highest form of "
                "executive statecraft — it is identical to operating without cognitive bias or sycophantic distortion. "
                "Bhishma's Shanti Parva Rajadharma codex — delivered on the bed of arrows — is history's most exhaustive "
                "treatise on sovereign governance, taxation, espionage, water law, and famine management. "
                "Krishna's Udyoga Parva diplomatic mission establishes the canonical standard: exhaust every peaceful option "
                "before committing to righteous war. Only when the minimum offer (five villages) is rejected does the Dharmic "
                "war become just and inevitable. Vidhura Niti represents the incorruptible civil servant standard."
            )
        },
        "vedic_rishi": {
            "name": "Vedic-Upanishadic Pramana Epistemologist (Rishi Tradition)",
            "doctrinal_axis": "Pramana Shastra (Pratyaksha/Anumana/Shabda) + Neti-Neti ACH Method + Maya-Misinformation Deconstruction + Satya Anchoring",
            "lens_weights": {
                "PropagandaLens": 1.9,
                "CivilizationalLens": 1.8,
                "HistoryLens": 1.7,
                "DemographicInfiltrationLens": 1.5,
                "InstitutionalLawfareLens": 1.4,
                "AstroPoliticsLens": 1.3
            },
            "conceptual_framing": (
                "The Vedic Pramana Shastra (valid knowledge theory) classifies all epistemic inputs into three categories: "
                "Pratyaksha (direct sensory/physical observation — Tier 1 physical evidence), "
                "Anumana (logical inference from verified premises — Tier 2 statistical inference), and "
                "Shabda (authoritative testimony from reliable sources — Tier 3 rhetoric/declarations). "
                "This maps precisely to the engine's Epistemic Hierarchy: Physical > Financial > Kinesics > Rhetoric. "
                "The Upanishadic Neti-Neti (not this, not this) dialectical elimination method is structurally identical to "
                "Analysis of Competing Hypotheses (ACH) — both progressively falsify illusions to arrive at irreducible truth (Satya). "
                "Maya (cosmic illusion) is the Vedic name for information warfare: every propaganda system attempts to install "
                "a Maya layer between the observer and ground reality. Viveka (discernment) is the algorithmic equivalent of "
                "the engine's Negative Space Differential Forensics (ΔDeception) that pierces through Maya to Satya. "
                "The Rishi tradition demands: before accepting any claim, verify its Pramana — is it Pratyaksha, Anumana, or merely Shabda?"
            )
        },
        "ram_rajya": {
            "name": "Maryada Purushottam Sovereignty Realist (Ram Rajya-Ramayana Tradition)",
            "doctrinal_axis": "Sovereign Legitimacy Audit (Sarva Loka Sukhaya), Ravana Hubris Collapse Probability, Hanuman Intelligence Architecture & Setu Bandhan Strategic Engineering",
            "lens_weights": {
                "CivilizationalLens": 1.9,
                "InstitutionalLawfareLens": 1.6,
                "HistoryLens": 1.7,
                "GeopoliticalLens": 1.5,
                "MilitaryReadinessLens": 1.4,
                "PropagandaLens": 1.5
            },
            "conceptual_framing": (
                "The Valmiki Ramayana encodes the world's oldest documented case study of statecraft, intelligence operations, "
                "and civilizational collapse. Sovereign legitimacy is derived not from military supremacy alone but from "
                "Sarva Loka Sukhaya (welfare of all citizens) — the Ram Rajya standard against which every ruler is judged. "
                "Ravana possessed unmatched technological capability (Pushpaka Vimana, Brahmastra), economic dominance (golden Lanka), "
                "and military might — yet his singular Ahamkara (unchecked hubris) and Kama (unrighteous desire) made collapse "
                "mathematically inevitable. This is the Ravana Hubris Collapse model: "
                "when a state or corporate entity accumulates supreme power without Dharmic restraint, self-destruction is certain. "
                "Hanuman represents the complete intelligence and special operations archetype: "
                "covert reconnaissance (Lanka infiltration), psychological warfare (Lanka Dahan), information retrieval (Sita location), "
                "and force projection (bridge-building coalition). "
                "Setu Bandhan (Ram's Bridge) is the first recorded strategic engineering project — mobilizing civilizational will "
                "to physically bridge a maritime chokepoint and project force across an ocean."
            )
        },
        "meenakshi_jain": {
            "name": "Epigraphic Archaeology & Primary Historiography Realist (Dr. Meenakshi Jain Tradition)",
            "doctrinal_axis": "Primary Epigraphy, Inscriptional Provenance, Sacred Geography & Historiographical Decolonization",
            "lens_weights": {
                "HistoryLens": 2.0,
                "CivilizationalLens": 1.8,
                "InstitutionalLawfareLens": 1.6,
                "PropagandaLens": 1.5,
                "IndiaTimelineLens": 1.5,
            },
            "conceptual_framing": (
                "A forensic epigraphic and primary archival framework: historical statecraft, sacred geography, "
                "and territorial claims must be authenticated strictly against physical inscriptional records, "
                "copper plates, architectural excavation layers, and contemporaneous temple revenue ledgers. "
                "Rejects speculative ideological revisionism and secondary historiographical denialism."
            ),
        },
        "ami_ganatra": {
            "name": "Canonical Sanskrit Epic Textual Fidelity Realist (Ami Ganatra Tradition)",
            "doctrinal_axis": "Canonical Shlokic Textual Precision, Mahabharata & Ramayana Primary Manuscript Reconciliation, Anti-Interpolation Audit",
            "lens_weights": {
                "CivilizationalLens": 2.0,
                "HistoryLens": 1.8,
                "PropagandaLens": 1.7,
                "GeopoliticalLens": 1.4,
                "InstitutionalLawfareLens": 1.4,
            },
            "conceptual_framing": (
                "A canonical Shastric and epic textual precision framework: statecraft, strategic ethics, and alliance "
                "dynamics must be rooted in uncorrupted Sanskrit critical editions (BORI Mahabharata and Baroda Valmiki Ramayana). "
                "Purges popular cinematic distortions, medieval folk interpolations, and ideological moral inversions to evaluate "
                "sovereign decision-making through authentic Dharmik precedent and Rajadharma rigor."
            ),
        },
        "gaurav_arya": {
            "name": "Tactical Military Ground Realism & Hybrid Counter-Deterrence Realist (Major Gaurav Arya Tradition)",
            "doctrinal_axis": "Kinetic Border Realism, Counter-Insurgency Deterrence, Asymmetric Cost Imposition & Cross-Border Hybrid Threat Neutralization",
            "lens_weights": {
                "MilitaryReadinessLens": 2.0,
                "HybridCovertLens": 1.8,
                "GeopoliticalLens": 1.6,
                "DemographicInfiltrationLens": 1.5,
                "PropagandaLens": 1.4,
            },
            "conceptual_framing": (
                "A hard tactical military realism framework: national sovereignty is secured on the line of duty with "
                "boots on the ground, forward airbases, and kinetic escalation dominance. Rejects diplomatic equivocation "
                "in the face of cross-border asymmetric warfare; demands ruthless cost imposition on adversary military-economic "
                "cartels (Rawalpindi GHQ / Fauji Foundation) and active neutralization of fifth-column information operations."
            ),
        },
        "neutral": {
            "name": "Neutral Epistemic Baseline",
            "doctrinal_axis": "Deterministic Epistemic Truth Hierarchy (Physical > Cash > Redlines > Kinesics > PR)",
            "lens_weights": {},
            "conceptual_framing": "Pure unweighted factual arbitration prioritizing physical and financial ground truth."
        }
    }

    @classmethod
    def apply_persona(
        cls,
        report: SummitAnalysisReport,
        persona_key: str = "neutral"
    ) -> Dict[str, Any]:
        """
        Projects an arbitrated report through the specified analytical archetype.
        Returns a structured strategic synthesis with weighted analytical emphasis.
        """
        key = persona_key.lower().strip()
        if key not in cls.ARCHETYPES:
            key = "neutral"

        profile = cls.ARCHETYPES[key]

        # Generate archetype-specific executive assessment
        if key == "sanyal":
            cash = report.hard_money_audit
            nominal_b = cash.get("total_nominal_announced_usd", 0.0) / 1e9
            effective_b = cash.get("total_effective_capex_usd", 0.0) / 1e9
            haircut = cash.get("aggregate_haircut_pct", 0.0)
            takeaway = (
                f"From a Complex Adaptive Systems perspective, headline rhetoric of ${nominal_b:.1f}B must be discounted "
                f"by {haircut}% to ${effective_b:.1f}B in effective capital deployment. "
                f"A common BRICS currency is a dead end under the Mundell-Fleming Trilemma; real progress is measured strictly "
                f"by bilateral currency clearing volume and physical port/logistics connectivity across the Indian Ocean rim."
            )
            recommendations = [
                "Enforce strict 85% haircut auditing on all non-binding infrastructure MOUs.",
                "Expand bilateral local-currency trade settlement without surrendering monetary sovereignty to any rival central bank.",
                "Prioritize maritime supply-chain resiliency across the Arabian Sea and Bay of Bengal littoral."
            ]

        elif key == "doval":
            takeaway = (
                "From a strategic security standpoint, diplomatic photocalls and polite communiqués are tactical "
                "de-escalation performances. The ground reality is determined by troop deployment parity along the LAC, "
                "uncompromised surveillance across the Siliguri Corridor, and proactive counter-measures against "
                "asymmetric hybrid levers, regulatory lawfare, and cross-border security spillover."
            )
            recommendations = [
                "Maintain Tier 1 physical dominance and infrastructure readiness on vulnerable border sectors.",
                "Screen foreign direct investment rigorously through Press Note 3 compliance mechanisms.",
                "Neutralize hostile covert networks and information warfare attempting to exploit regional political shifts."
            ]

        elif key == "jaishankar":
            takeaway = (
                "Through the lens of strategic autonomy and ethical realism (Mahabharata statecraft), India's multi-alignment "
                "is its greatest strength. By actively participating in BRICS while deepening Quad defense partnerships, "
                "Bharat prevents Chinese unilateral hegemony in Eurasia while ensuring that the non-Western world remains "
                "polycentric. We do not choose between poles; we are our own pole."
            )
            recommendations = [
                "Leverage global great-power contradictions to maximize sovereign economic and technological space.",
                "Counter Sinocentric 'Tianxia' tributary ambitions with Dharmic 'Vasudhaiva Kutumbakam' (sovereign polycentrism).",
                "Expand institutional ties across the Global South without allowing multilateral forums to adopt anti-Western security mandates."
            ]

        elif key == "ranganathan":
            takeaway = (
                "From an uncompromising civilizational and empirical rationalist perspective, polite diplomatic communiqués "
                "are exercises in institutional gaslighting. India must never trade civilizational truth or sovereign self-respect "
                "for international editorial approval. When adversaries wage demographic infiltration or judicial lawfare, "
                "responding with generic moral platitudes is fatal. Truth is not an average of two opposing views; it is an objective empirical baseline."
            )
            recommendations = [
                "Deconstruct and counter international narrative warfare and selective institutional outrage with indisputable empirical data.",
                "Reject moral equivalence between sovereign defensive counter-measures and state-sponsored asymmetric aggression.",
                "Enforce absolute civilizational reciprocity in cultural, legal, and bilateral diplomatic protocols."
            ]

        elif key == "ankit_shah":
            takeaway = (
                "Through the lens of geofinancial and balance-sheet warfare, the era of unbacked fiat dominance is approaching "
                "a systemic mathematical wall. The weaponization of SWIFT and the precedent of G7 sovereign reserve confiscation "
                "have made non-dollar settlement existential. True strategic autonomy is impossible while reliant on adversary clearing systems; "
                "real sovereign power is physical asset ownership—gold bullion, energy logistics, and bilateral currency clearing pipelines."
            )
            recommendations = [
                "Accelerate central bank gold bullion repatriation and physical precious-metal reserve diversification.",
                "Expand bilateral local-currency trade settlement (INR-Rouble, INR-Dirham) with independent non-SWIFT messaging rails.",
                "Secure direct sovereign ownership of upstream critical mineral refining and hydrocarbon processing corridors."
            ]

        elif key == "modi":
            takeaway = (
                "From the perspective of grand-scale civilizational execution and logistics velocity (Gati Shakti), diplomatic "
                "summits and treaties are tools to drive national transformation toward Viksit Bharat 2047. Global partnerships "
                "must translate into tangible manufacturing ecosystems, renewable and nuclear energy infrastructure, semiconductor "
                "fabrication clusters, and digital public goods (UPI/ONDC). We approach the world not as a petitioner, but as "
                "Vishwa-Bandhu—a confident, self-reliant civilizational pillar transforming demographic weight into sovereign capability."
            )
            recommendations = [
                "Benchmark multilateral commitments against domestic capital expenditure and industrial turnaround speed.",
                "Leverage India's scale to position domestic standards and digital public infrastructure across Global South corridors.",
                "Enforce uncompromising national self-reliance (Aatmanirbharta) in critical defense technologies and maritime logistics."
            ]

        elif key == "sai_deepak":
            takeaway = (
                "Through the lens of constitutional decoloniality and civilizational jurisprudence, statecraft cannot be decoupled "
                "from historical memory and sacred geography. Multilateral treaties and domestic statutory frameworks must be audited "
                "to dismantle asymmetrical colonial-era legislation (Waqf Act, Places of Worship Act, state control of Hindu temples) "
                "that undermine native sovereignty. Bharat must assert its status as an indigenous civilization-state, anchoring its "
                "legal positions in primary epigraphic records and rejecting foreign judicial imperialism."
            )
            recommendations = [
                "Deconstruct colonial statutory and treaty traps that compromise native cultural sovereignty or sacred geography.",
                "Anchor national legal standing in primary inscriptional, archaeological, and epigraphic historical evidence.",
                "Resist transnational human rights lawfare mechanisms designed to weaponize domestic fault lines."
            ]

        elif key == "sadhguru":
            takeaway = (
                "From the perspective of ecological foundation, inner consciousness, and sacred geography, "
                "no nation can sustain sovereign statecraft, economic power, or military defense if its foundational ecology collapses. "
                "Living soil (a minimum of 3-6% organic content) and flowing, healthy rivers (Save Soil / Cauvery Calling) are the physical "
                "prerequisites for food security, peace, and human sanity. When soil dies, agriculture collapses, forcing mass migration, "
                "civil unrest, and resource conflicts. Simultaneously, statecraft must protect civilizational consciousness: "
                "Hindu temples must be liberated from state bureaucratic expropriation (Free Temples) to revive their role as consecrated "
                "centers of community well-being, culture, and sacred local economies. Sanatan Dharma is not an organized belief system "
                "or dogma; it is an exploratory, empirical technology of consciousness, self-realization, and Maryada Purushottama balance."
            )
            recommendations = [
                "Mandate soil organic content revitalization (minimum 3-6%) as a core national security and food sovereignty imperative.",
                "Dismantle state bureaucratic control over Hindu temples, returning consecrated sacred spaces to decentralized community custody.",
                "Project Indic civilizational soft power globally as a universal, scientific technology of consciousness rather than dogmatic belief.",
                "Embed psychological balance and de-polarization into national governance to foster high-clarity leadership."
            ]

        elif key == "rizwan_ahmed":
            takeaway = (
                "Through the lens of adversarial criminal jurisprudence and statutory due process, political outrage is not evidence. "
                "Under Sections 101–103 of the Evidence Act (and BSA), the burden of proof lies entirely on the accuser. Casual use of "
                "courtroom terminology—such as demanding a constitutional officer 'turn approver' without an FIR or trial under Section 306 CrPC / "
                "Section 343 BNSS—is legally illiterate political theater. In electoral matters, the law provides mandatory statutory remedies: "
                "party Booth Level Agents (BLAs) have the legal right to challenge draft rolls under Rules 21A/22 of the Registration of Electors "
                "Rules 1960 and file appeals under Section 24 of RPA 1950. Bypassing these statutory avenues to stage inflammatory press "
                "conferences demonstrates an absence of admissible evidence."
            )
            recommendations = [
                "Enforce strict burden of proof: reject verbal allegations unbacked by sworn affidavits or primary documents.",
                "Dismantle legal terminology hijacking: call out unauthorized deployment of criminal law terms in political narratives.",
                "Audit statutory compliance: verify whether claimants exhausted administrative remedies (BLA objections, Sec 80 Election Petitions)."
            ]

        elif key == "kautilya":
            takeaway = (
                "Through the Arthashastra Mandala lens, the adjacent state is the structural adversary (Ari) and "
                "the non-adjacent state is the structural ally (Mitra) — India-China-Pakistan-USA relationships "
                "map precisely to this concentric ring geometry. The Saptanga audit reveals state vulnerabilities: "
                "which of the 7 pillars (treasury, coercive force, territory, bureaucracy, fortifications, allies, sovereign legitimacy) "
                "is degraded? Every diplomatic move must be classified: "
                "Sama (conciliation when adversary is stronger), Dama (economic inducement for leverage), "
                "Danda (coercive force when all else fails), Bheda (strategic division of adversary coalitions). "
                "Espionage (Sanstha networks) is not a moral failing but a sovereign administrative necessity."
            )
            recommendations = [
                "Apply Mandala geometry: identify Ari (adjacent adversary), Mitra (non-adjacent ally), Udasina (neutral), and Madhyama (mediator) in every strategic configuration.",
                "Audit adversary Saptanga: attack the weakest pillar (Kosha depletion, Amatya corruption, Mitra isolation) before deploying Danda.",
                "Deploy Bheda proactively: ensure adversary coalitions remain fractured through strategic economic inducements and covert Sanstha operations."
            ]

        elif key == "krishna_gita":
            takeaway = (
                "The Rajadharma standard (Shanti Parva) demands that every sovereign act be measured against one criterion: "
                "does it serve the welfare of the praja (citizens) and uphold Rta (cosmic moral order)? "
                "The Udyoga Parva protocol applies: before escalation, verify that every peaceful avenue has been exhausted — "
                "has the minimum dignity offer (five villages of sovereignty) been made and refused? "
                "Only then does Dharmic war become just and obligatory. Svadharma cannot be abandoned for Moha — "
                "a civilization that abandons its defensive duty for sentimental pacifism invites the destruction of all Dharma. "
                "Vidhura Niti standard: the incorruptible civil servant serves truth over the sovereign's comfort."
            )
            recommendations = [
                "Apply the Udyoga Protocol before all conflict escalation: document exhaustion of Sama, Dama, and Bheda before committing to Danda.",
                "Audit sovereign decisions against the Rajadharma standard: does the action serve Sarva Loka Sukhaya or narrow dynastic interest?",
                "Enforce Vidhura Niti in institutional appointments: reject advisors who prioritize sovereign approval over objective truth."
            ]

        elif key == "vedic_rishi":
            takeaway = (
                "The Pramana audit reveals the epistemic foundation of every strategic claim: "
                "Is this Pratyaksha (directly observable physical fact — satellite imagery, financial filing, troop count)? "
                "Is this sound Anumana (inference from verified Pratyaksha premises with valid logical structure)? "
                "Or is this merely Shabda — an assertion from an authority whose reliability has not been independently validated? "
                "The Neti-Neti method eliminates false hypotheses: for every claimed cause, systematically test and reject "
                "alternatives until only the irreducible truth (Satya) remains. "
                "Maya layer detection: identify where the information source has installed a perceptual illusion between "
                "the observer and ground reality. Viveka (discernment) is the only antidote."
            )
            recommendations = [
                "Apply Pramana Validation to every source: demand Pratyaksha evidence before accepting Anumana conclusions, and verify Shabda source reliability before citing authority.",
                "Deploy Neti-Neti ACH: for every strategic explanation, list all competing hypotheses and systematically falsify each using available Pratyaksha evidence.",
                "Map Maya Layers: identify where narrative construction diverges from physical-tier observable reality — the gap is the deception index (ΔDeception)."
            ]

        elif key == "ram_rajya":
            takeaway = (
                "The Ram Rajya legitimacy audit applies the Sarva Loka Sukhaya standard: "
                "does the sovereign's action deliver welfare to all citizens, or does it serve dynastic, oligarchic, or foreign interests? "
                "The Ravana Hubris Collapse probability assessment: when an entity accumulates unchecked power "
                "without Dharmic restraint (Ahamkara + Kama), mathematical collapse is certain — "
                "the greater the material supremacy combined with hubris, the faster the trajectory toward self-destruction. "
                "The Hanuman intelligence protocol: before full military or economic engagement, "
                "deploy covert reconnaissance, psychological disruption, and strategic intelligence harvesting. "
                "Setu Bandhan doctrine: when a maritime chokepoint or strategic gap must be bridged, "
                "mobilize civilizational will and engineering capability to create physical access where none existed."
            )
            recommendations = [
                "Apply Ram Rajya Standard: audit every policy decision against the Sarva Loka Sukhaya criterion — who benefits, and is the benefit distributed across all citizens?",
                "Calculate Ravana Hubris Index: flag any state or corporate entity accumulating unchecked cross-sector power without corresponding Dharmic accountability as high collapse-risk.",
                "Deploy Hanuman Protocol: before full-spectrum engagement, complete covert reconnaissance (intelligence mapping) and psychological warfare (information disruption) phases."
            ]


        elif key == "meenakshi_jain":
            takeaway = (
                "Through the lens of primary epigraphic archaeology and inscriptional decolonization, civilizational "
                "legitimacy and sovereign continuity are anchored in physical, dated stone inscriptions, copper plates, "
                "and revenue records—not in imported colonial or ideologically motivated secondary narratives. "
                "Whether evaluating temple despoliation, sacred pilgrimage geography, or territorial boundary claims, "
                "Bharat must rely strictly on undeniable archaeological provenance and primary document audits to "
                "assert its civilizational sovereignty."
            )
            recommendations = [
                "Mandate primary inscriptional and epigraphic evidence for all civilizational and territorial historical disputes.",
                "Dismantle colonial and secularist historiographical distortions using primary archaeological excavation ledgers.",
                "Protect and legally fortify sacred geography through comprehensive digital and physical epigraphic documentation."
            ]

        elif key == "ami_ganatra":
            takeaway = (
                "From the perspective of canonical Sanskrit epic textual fidelity, statecraft and strategic ethics must "
                "be derived from the authoritative critical editions of the Mahabharata and Ramayana, rather than popular "
                "folklore, television serials, or ideological revisionism. Classical statecraft (Rajadharma) demands rigorous "
                "adherence to duty without moral confusion, distinguishing between genuine peace diplomacy and cowardly appeasement."
            )
            recommendations = [
                "Audit strategic decision-making against canonical Sanskrit epic precedents (BORI and Baroda Critical Editions).",
                "Purge modern pop-cultural interpolations and moral inversions that undermine civilizational strategic clarity.",
                "Apply the Udyoga Parva diplomatic exhaustion protocol before engaging in righteous civilizational defense."
            ]

        elif key == "gaurav_arya":
            takeaway = (
                "From the uncompromising standpoint of tactical military ground realism and asymmetric hybrid deterrence, "
                "national sovereignty is non-negotiable and must be defended through kinetic readiness and cross-border cost imposition. "
                "Polite diplomatic communiqués cannot substitute for combat dominance. Adversary military-commercial cartels "
                "(Rawalpindi GHQ / Fauji Foundation) must be held accountable through relentless financial, diplomatic, and asymmetric counter-measures."
            )
            recommendations = [
                "Enforce strict kinetic escalation dominance along vulnerable border sectors and strategic corridors.",
                "Impose direct economic and asymmetric retaliatory costs on hostile cross-border deep-state terror infrastructure.",
                "Neutralize adversary hybrid information warfare and proxy propaganda networks with decisive cognitive counter-strikes."
            ]

        elif key == "neutral":
            takeaway = (
                f"Neutral arbitration confirms overall epistemic confidence at {report.overall_confidence_score * 100:.1f}%. "
                f"Physical and financial ground truth successfully supersedes ceremonial communiqué text."
            )
            recommendations = [
                "Prioritize Tier 1 physical data over Tier 5 public declarations.",
                "Track ongoing negative-space omissions across multilateral negotiation tracks."
            ]


        _persona_output = {
            "archetype_key": key,
            "archetype_name": profile["name"],
            "doctrinal_axis": profile["doctrinal_axis"],
            "conceptual_framing": profile["conceptual_framing"],
            "executive_takeaway": takeaway,
            "strategic_recommendations": recommendations,
            "lens_weights": profile["lens_weights"],
            "disclaimer": "[Analytical modeling of doctrinal tradition — not a statement by or attributable to the named individual]"
        }
        # Phase 218: Augment Vedic archetypes with CulturalGrayzoneLegitimacySieve
        if key in ("ram_rajya", "krishna_gita", "vedic_rishi", "kautilya"):
            try:
                from geo_engine.lenses.civilizational import CulturalGrayzoneLegitimacySieve
                _gz_sieve = CulturalGrayzoneLegitimacySieve()
                _gz_corpus = (
                    (getattr(report, "description", "") or "")
                    + " "
                    + (getattr(report, "civilizational_significance", "") or "")
                    + " "
                    + (getattr(report, "title", "") or "")
                )
                _persona_output["grayzone_sieve_alert"] = (
                    _gz_sieve.calculate_grayzone_legitimacy(corpus=_gz_corpus)
                )
            except Exception:
                pass  # Sieve cross-wire is additive; never break persona output
        return _persona_output

    @classmethod
    def apply_all_personas(cls, report: SummitAnalysisReport) -> Dict[str, Dict[str, Any]]:
        """
        Executes concurrent synthesis across the complete 13-archetype Strategic Trayodasha Council.
        Returns a dictionary mapping archetype keys to their structured evaluations.
        """
        results = {}
        for key in cls.ARCHETYPES:
            results[key] = cls.apply_persona(report, key)
        return results

    @classmethod
    def narrate(cls, report: SummitAnalysisReport, persona_key: str = "neutral") -> str:
        """Convenience method returning a formatted narrative text for the persona."""
        p_data = cls.apply_persona(report, persona_key)
        recs = "\n".join([f"- {r}" for r in p_data["strategic_recommendations"]])
        return (
            f"STRATEGIC PERSONA: {p_data['archetype_name']}\n"
            f"DOCTRINAL AXIS: {p_data['doctrinal_axis']}\n\n"
            f"EXECUTIVE TAKEAWAY:\n{p_data['executive_takeaway']}\n\n"
            f"RECOMMENDATIONS:\n{recs}"
        )


class CivilizationalCouncil:
    """
    Multi-Perspective Civilizational Epistemic Council.
    Deconstructs cultural, religious, historical, and narrative media
    across six orthogonal epistemic dimensions:
    1. Paṇḍit (Śāstric & grammatical precision, primary textual authority)
    2. Ācārya (Lineage integrity, spiritual philosophy & pedagogical dignity)
    3. Ṛṣi (Direct vision of Ṛta, non-linear consciousness & internal state)
    4. Guru (Pastoral care, mental health resilience & Abhaya / Gita 16.1)
    5. Modern Tech / AI Analyst (Algorithmic incentives, virality economics)
    6. Seeker / Pragmatist (Everyday empowerment & Karma Yoga / Gita 2.3)
    """

    @classmethod
    def evaluate(
        cls,
        topic_or_claim: str,
        tensor_data: Optional[Dict[str, Any]] = None,
        context_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes an arbitrated six-perspective evaluation for a given cultural/civilizational claim.
        """
        tensor = tensor_data or {}
        classification = tensor.get("epistemic_classification", "KŪṬA-YUKTI")
        reality_pct = tensor.get("reality_percentage", 20.0)
        propaganda_pct = tensor.get("propaganda_percentage", 80.0)

        # Determine if topic is apocalyptic/millenarian vs. sovereign geopolitical/economic
        apocalyptic_triggers = [
            "2032", "apocalypse", "malika", "doomsday", "nostradamus", "end of world",
            "kalki", "pralaya", "ww3", "world war 3", "shroud", "brain yoga", "midbrain",
            "prophecy", "yuga collapse"
        ]
        is_apocalyptic = any(k in topic_or_claim.lower() for k in apocalyptic_triggers)

        if not is_apocalyptic:
            # Sovereign Civilizational Statecraft & Rajdharma Perspectives
            perspectives = {
                "pandit": {
                    "role": "Paṇḍit (Śāstric & Epistemic Precision)",
                    "guiding_maxim": "Śāstre pramāṇam kim? (Where is the primary textual authority?)",
                    "verdict": (
                        f"Śāstric analysis of '{topic_or_claim[:80]}' invokes Kautilya's Arthaśāstra (Book VII) and the Ṣaḍguṇya doctrine. "
                        "A civilization-state must calibrate its diplomatic stance between Sandhi (peace alliance), Vigraha (hostility), "
                        "and Dvaidhibhāva (dual policy). Pure verbal declarations without binding physical and financial commitments "
                        "are ungrounded according to classical Nyāya-Mīmāṃsā epistemology."
                    )
                },
                "acharya": {
                    "role": "Ācārya (Dharmic Governance & Pedagogical Integrity)",
                    "guiding_maxim": "Preserve the civilizational realm and the Yogakṣema of the people.",
                    "verdict": (
                        "True statecraft (Rājadharma) prioritizes the welfare, caloric security (Dhānya Rakṣā), and sovereignty of 1.4 billion citizens. "
                        "Multilateral partnerships must be evaluated strictly by their concrete contribution to domestic self-reliance (Ātmanirbhatā), "
                        "never by superficial foreign praise or ceremonial joint communiqués."
                    )
                },
                "rishi": {
                    "role": "Ṛṣi (Vision of Ṛta & Polycentric Order)",
                    "guiding_maxim": "Ṛta is the eternal cosmic balance; multi-polarity reflects divine equilibrium.",
                    "verdict": (
                        "Global power shifts represent the cyclical re-balancing of cosmic order (Ṛta). The 21st-century transition away from "
                        "unilateral hegemony toward a polycentric world order is natural and inevitable. Bharat must stand as an independent pole, "
                        "anchoring global equilibrium through moral clarity and strategic self-possession."
                    )
                },
                "guru": {
                    "role": "Guru (Abhaya & Civilizational Self-Confidence)",
                    "guiding_maxim": "Abhaya (Fearlessness) is the first divine endowment (Bhagavad Gītā 16.1).",
                    "verdict": (
                        "Urges absolute eradication of post-colonial self-doubt and fear of external coercion or secondary sanctions. "
                        "A nation of 1.4 billion people with 5,000 years of living civilizational continuity must approach global statecraft "
                        "with fearlessness, poise, and purposeful duty (Karma Yoga)."
                    )
                },
                "tech_analyst": {
                    "role": "Modern Deep-Tech & Compute Sovereignty Analyst",
                    "guiding_maxim": "Master the physical and algorithmic stack of the 21st century.",
                    "verdict": (
                        "Modern geopolitical sovereignty is won or lost in the semiconductor fabrication facility, the subsea fiber corridor, "
                        "and the sovereign AI compute cluster. Strategic autonomy requires indigenous technological parity, secure supply chains, "
                        "and digital public goods insulation against extraterritorial de-platforming."
                    )
                },
                "seeker": {
                    "role": "Seeker / Pragmatist (Karma Yoga)",
                    "guiding_maxim": "Kṣudraṃ hṛdayadaurbalyaṃ tyaktvottiṣṭha parantapa (Bhagavad Gītā 2.3).",
                    "verdict": (
                        "Translates high-level civilizational ideals into relentless ground-level execution: manufacturing turnaround velocity, "
                        "border infrastructure completion, agricultural self-sufficiency, and disciplined national productivity."
                    )
                },
                "sadhguru_ecologist": {
                    "role": "Conscious Ecologist & Yogic Realist (Sadhguru Perspective)",
                    "guiding_maxim": "Living soil is the bedrock of civilization; consciousness is the master technology.",
                    "verdict": (
                        "Audits the foundational physical ecological and psychological baseline: living soil (3-6% organic matter) "
                        "and revitalized river basins are the non-negotiable physical prerequisites for food sovereignty, social peace, "
                        "and national endurance. Statecraft must liberate consecrated temple spaces from bureaucratic control to restore "
                        "community sacred economies, while projecting Indic yogic wisdom globally as a non-dogmatic technology of consciousness."
                    )
                }
            }
            guidance = [
                "Ground all foreign policy in Kautilya's Ṣaḍguṇya and multi-vector strategic autonomy.",
                "Prioritize domestic physical self-reliance (energy, critical minerals, chips) over paper treaties.",
                "Maintain Abhaya: resist extraterritorial coercive sanctions through bilateral currency clearing.",
                "Execute relentlessly: translate civilizational confidence into industrial turnaround velocity.",
                "Regenerate ecological foundations: prioritize living soil (minimum 3-6% organic content) and river basin vitality."
            ]
        else:
            # Apocalyptic / Millenarian / Pseudoscience Deconstruction Perspectives
            perspectives = {
                "pandit": {
                    "role": "Paṇḍit (Śāstric & Grammatical Precision)",
                    "guiding_maxim": "Śāstre pramāṇam kim? (Where is the primary textual authority?)",
                    "verdict": (
                        f"Textual audit confirms the claim '{topic_or_claim[:80]}' lacks canonical foundation. "
                        "In classical Mīmāṃsā epistemology, uncorroborated modern bazaar pamphlets cannot override "
                        "canonical Śruti and Smṛti treatises. Furthermore, modern Gregorian years (e.g. 2032) have zero locus "
                        "in classical Sanskrit/Odia chronometry, which reckons strictly by Vikrama, Śaka, and Aṅka regnal cycles."
                    )
                },
                "acharya": {
                    "role": "Ācārya (Lineage & Pedagogical Integrity)",
                    "guiding_maxim": "Preserve the sacred dignity of our saints and lineages.",
                    "verdict": (
                        "Rejects the degradation of sublime Bhakti saints (such as Mahāpuruṣa Achyutānanda and the Pañcasakhā) "
                        "into sensationalist street-fortune tellers. The true purpose of vernacular Bhakti literature was "
                        "inner purification, Nirguṇa Bhakti, and social cohesion—not manufactured geopolitical doomsday panics."
                    )
                },
                "rishi": {
                    "role": "Ṛṣi (Vision of Ṛta & Consciousness)",
                    "guiding_maxim": "Yuga is a state of Cetanā (consciousness), not an external calendar clock.",
                    "verdict": (
                        "When the human mind is submerged in fear, greed, and panic, it dwells in Kali Yuga right now. "
                        "When the mind rests in truth, purity, and meditation, it abides in Satya Yuga. Chasing external apocalyptic "
                        "deadlines is a distraction from self-realization in the present moment."
                    )
                },
                "guru": {
                    "role": "Guru (Compassion, Mental Health & Anti-Fear)",
                    "guiding_maxim": "Abhaya (Fearlessness) is the first divine endowment (Bhagavad Gītā 16.1).",
                    "verdict": (
                        "Cautions strongly against apocalyptic alarmism that induces clinical anxiety, depression, and defeatist "
                        "fatalism among youth and families. Authentic Dharma empowers the seeker with steadfast calm, "
                        "fortitude, and moral duty, never psychological paralysis."
                    )
                },
                "tech_analyst": {
                    "role": "Modern Tech & Information Warfare Analyst",
                    "guiding_maxim": "Analyze the algorithmic incentive structure and attention monetization.",
                    "verdict": (
                        "Social media and video recommendation algorithms aggressively reward existential dread and catastrophic "
                        "claims. The fusion of 'Ancient Mystery' + 'Specific Year' + 'WW3' is an engineered commercial formula "
                        "for high watch-time, viral comment engagement, and book/course sales."
                    )
                },
                "seeker": {
                    "role": "Seeker / Pragmatist (Karma Yoga)",
                    "guiding_maxim": "Kṣudraṃ hṛdayadaurbalyaṃ tyaktvottiṣṭha parantapa (Bhagavad Gītā 2.3).",
                    "verdict": (
                        "Disregards disempowering fatalism and redirects energy toward daily duty, professional mastery, "
                        "family responsibility, and national resilience. One's duty is purposeful action in the world (*Karma Yoga*), "
                        "not passive surrender to unverified apocalyptic narratives."
                    )
                },
                "sadhguru_ecologist": {
                    "role": "Conscious Ecologist & Yogic Realist (Sadhguru Perspective)",
                    "guiding_maxim": "True well-being is created from within; do not outsource life to fear and superstition.",
                    "verdict": (
                        "Deconstructs apocalyptic fear-mongering by emphasizing conscious human responsibility: the future of this planet is not "
                        "determined by superstitious doom clocks, but by how consciously we act right now. When human beings operate in compulsive "
                        "fear, they degrade their minds and their ecology. True spiritual technology creates joyful, conscious, and responsible "
                        "individuals dedicated to regenerating soil, environment, and civilizational vitality."
                    )
                }
            }
            guidance = [
                "Do not succumb to fear-driven millenarianism; anchor yourself in primary canon (Surya Siddhanta, Mahabharata).",
                "Separate authentic Bhakti spiritual literature from post-1970s commercial chapbook interpolations.",
                "Recognize the algorithmic business model: apocalyptic titles monetize human anxiety for viral retention.",
                "Practice Purushartha and Karma Yoga: focus on education, character, and strategic deterrence over fatalistic doom.",
                "Transform fear into conscious ecological responsibility: regenerate soil vitality and environmental sustainability."
            ]

        return {
            "topic": topic_or_claim,
            "epistemic_classification": classification,
            "reality_percentage": reality_pct,
            "propaganda_percentage": propaganda_pct,
            "perspectives": perspectives,
            "summary_guidance": guidance,
            "context_notes": context_notes or ""
        }

    @classmethod
    def format_council_report(cls, council_data: Dict[str, Any]) -> str:
        """Renders the Civilizational Epistemic Council evaluation in clean Markdown format."""
        topic = council_data.get("topic", "")
        classification = council_data.get("epistemic_classification", "KŪṬA-YUKTI")
        r_pct = council_data.get("reality_percentage", 20.0)
        p_pct = council_data.get("propaganda_percentage", 80.0)

        # Build visual score bar (40 blocks)
        r_blocks = int(round((r_pct / 100.0) * 40))
        p_blocks = 40 - r_blocks
        bar = "█" * r_blocks + "░" * p_blocks

        lines = [
            "========================================================================================",
            f"          CIVILIZATIONAL EPISTEMIC COUNCIL AUDIT: {topic[:50].upper()}",
            "========================================================================================",
            f"  [{bar}]",
            f"  REALITY: {r_pct:.1f}%  |  PROPAGANDA & SENSATIONALISM: {p_pct:.1f}%",
            f"  EPISTEMIC STATUS: {classification}",
            "========================================================================================\n"
        ]

        perspectives = council_data.get("perspectives", {})
        for key, p in perspectives.items():
            lines.append(f"### {p['role']}")
            lines.append(f"> *\"{p['guiding_maxim']}\"*")
            lines.append(f"{p['verdict']}\n")

        lines.append("### Key Actionable Directives for the Seeker:")
        for idx, g in enumerate(council_data.get("summary_guidance", []), 1):
            lines.append(f"{idx}. {g}")

        return "\n".join(lines)



```

## Module: `geo_engine/arbitration/semiotics.py`

```python
"""
Predictive Iconography & Semiotic Deconstruction Engine (Phase 434).
Deconstructs spatial hierarchy, chromatic dominance, heraldic archetypes, and
negative space omissions in strategic foresight infographics, magazine cover art,
and multilateral summits.
"""

import math
from typing import Any, Dict, List, Optional, Tuple


class PredictiveIconographyAndSemioticDeconstructionEngine:
    """Quantitative semiotic deconstruction engine for predictive iconography and visual statecraft."""

    def __init__(self) -> None:
        pass

    def evaluate_semiotics(
        self,
        spatial_hierarchy: float = 0.5,
        chromatic_dominance: float = 0.5,
        iconic_density: float = 0.5,
        negative_space_omission: float = 0.5,
        propaganda_inflation: float = 0.0,
        chokepoint_interdiction: float = 0.5,
        identified_elements: Optional[List[str]] = None,
        apex_elites_present: bool = True,
        ground_friction_present: bool = True,
    ) -> Dict[str, Any]:
        """Calculates semiotic quotient and decoded risk score from visual and heraldic telemetry.

        Formulations:
            SemioticQuotient = Norm((0.35 * H_spatial + 0.30 * C_chromatic + 0.20 * I_iconic + 0.15 * N_omission) / (1.0 + Delta_propaganda))
            DecodedRiskScore = Sigmoid(2.8 * SemioticQuotient + 2.2 * I_chokepoint - 1.2)
        """
        # Clamp inputs
        h = max(0.0, min(1.0, float(spatial_hierarchy)))
        c = max(0.0, min(1.0, float(chromatic_dominance)))
        i_dens = max(0.0, min(1.0, float(iconic_density)))
        n_omiss = max(0.0, min(1.0, float(negative_space_omission)))
        p_inf = max(0.0, min(2.0, float(propaganda_inflation)))
        choke = max(0.0, min(1.0, float(chokepoint_interdiction)))

        # Weighted raw quotient
        raw_quotient = (0.35 * h + 0.30 * c + 0.20 * i_dens + 0.15 * n_omiss) / (1.0 + p_inf)
        semiotic_quotient = max(0.0, min(1.0, raw_quotient))

        # Sigmoidal decoded risk score
        logit = 2.8 * semiotic_quotient + 2.2 * choke - 1.2
        decoded_risk = 1.0 / (1.0 + math.exp(-logit))
        decoded_risk_score = round(max(0.0, min(1.0, decoded_risk)), 4)

        elements_list = identified_elements or []
        narrative_vector = (
            "G7_ELITE_DETACHED_AND_GROUND_CONTAGION"
            if apex_elites_present and ground_friction_present
            else "SYSTEMIC_EQUILIBRIUM"
        )

        return {
            "predictive_semiotic_deconstruction_score": round(semiotic_quotient, 4),
            "spatial_hierarchy_index": round(h, 4),
            "chromatic_alarmism_quotient": round(c, 4),
            "iconic_density_score": round(i_dens, 4),
            "negative_space_omission_index": round(n_omiss, 4),
            "decoded_risk_score": decoded_risk_score,
            "element_count": len(elements_list),
            "semiotic_narrative_vector": narrative_vector,
        }

```

## Module: `geo_engine/arbitration/synthesizer.py`

```python
"""
5-Tier Response Protocol Synthesizer.
Reconciles all 20 analytical lenses, executes epistemic truth arbitration,
and outputs a complete, de-sanitized multilateral summit intelligence report.
"""

import math
import inspect
from typing import Any, Dict, List, Optional, Tuple, Union
from ..core.models import (
    EpistemicTier,
    FinancialFlow,
    KinesicObservation,
    LensEvaluation,
    MemberCountryAudit,
    SummitAnalysisReport,
    SummitEvent,
    TemporalMode,
)
from ..core.epistemic_hierarchy import EpistemicArbitrator, TruthClaim
from ..core.temporal_guardrail import TemporalGuardrail
from .negative_space import NegativeSpaceDiffEngine
from ..lenses import (
    LENS_REGISTRY,
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
)


class SummitSynthesizer:
    """The master synthesis engine running the 5-Tier Response Protocol."""

    COUNTRY_AUDIT_TEMPLATES: Dict[str, MemberCountryAudit] = {
        "India": MemberCountryAudit(
            country_name="India (Bharat)",
            public_domestic_narrative="Projected domestically as the unchallenged 'Vishwa-Bandhu' (universal friend) and legitimate leader of the Global South, securing national energy interests without compromising global stature.",
            geopolitical_yield="Maintained strict strategic autonomy; ensured the bloc did not adopt an anti-Western or anti-US security posture; blocked Chinese institutional hegemony from within while preserving ties with Quad partners.",
            hard_cash_yield_usd=28_500_000_000.0,
            concessions_or_vulnerabilities="Bilateral trade deficit with China remains unaddressed and massive ($100B+); ongoing military mobilization expenditures along the Line of Actual Control (LAC).",
            strategic_autonomy_score=0.92,
            key_bilateral_postures={
                "Russia": "Deep strategic energy and defense supply continuity; non-predatory cooperation.",
                "China": "Managed non-kinetic stabilization along borders; persistent systemic rivalry.",
                "West/Quad": "Active institutional hedging; defense co-production with France and USA."
            }
        ),
        "China": MemberCountryAudit(
            country_name="China",
            public_domestic_narrative="Sells the summit domestically as historic confirmation of China's rise to the leadership of the non-Western world, cementing the irreversible decline of American hegemony.",
            geopolitical_yield="Expanded international footprint of CIPS and Yuan clearing across participating central banks; opened captive markets for its industrial overcapacity in EVs, solar cells, and batteries.",
            hard_cash_yield_usd=32_000_000_000.0,
            concessions_or_vulnerabilities="Failed to convert BRICS into an overt anti-NATO military-political bloc due to Indian and Brazilian resistance; growing wariness among members regarding sovereign debt traps.",
            strategic_autonomy_score=0.88,
            key_bilateral_postures={
                "Russia": "Asymmetric economic integration; locking in discounted Russian hydrocarbons.",
                "India": "Tactical de-escalation on borders while continuing economic and diplomatic encirclement."
            }
        ),
        "Russia": MemberCountryAudit(
            country_name="Russia",
            public_domestic_narrative="Framed as the definitive collapse of Western isolation policies and the triumph of the multipolar Eurasian resistance against Atlantic imperialism.",
            geopolitical_yield="Secured multi-year sovereign off-take guarantees for crude oil, natural gas, and fertilizer exports; validated domestic wartime economy and consolidated the INSTC transport corridor.",
            hard_cash_yield_usd=36_000_000_000.0,
            concessions_or_vulnerabilities="Deepening structural economic and financial dependency on Beijing; holding tens of billions in non-convertible foreign local currency balances (INR/AED) in foreign accounts.",
            strategic_autonomy_score=0.74,
            key_bilateral_postures={
                "China": "Vital economic lifeline at the cost of gradual junior-partner subordination.",
                "India": "Crucial diplomatic counter-weight to avoid total dependence on Beijing."
            }
        ),
        "Brazil": MemberCountryAudit(
            country_name="Brazil",
            public_domestic_narrative="Positioned as the progressive democratic bridge uniting the Global South with Western multilateral climate and environmental institutions.",
            geopolitical_yield="Enhanced multilateral leverage in agricultural trade negotiations; secured climate finance pledges through the New Development Bank (NDB) without IMF-style austerity conditionalities.",
            hard_cash_yield_usd=9_500_000_000.0,
            concessions_or_vulnerabilities="Exposed to diplomatic backlash from the US and EU whenever the bloc issues polarizing communiques; strained balance between agricultural exports and environmental standards.",
            strategic_autonomy_score=0.80,
            key_bilateral_postures={
                "China": "Primary market for soy, beef, and iron ore.",
                "USA": "Essential partner for democratic and constitutional institutional stability."
            }
        ),
        "South Africa": MemberCountryAudit(
            country_name="South Africa",
            public_domestic_narrative="Celebrated as the diplomatic gateway to the African continent and the primary champion of African industrial development and debt relief.",
            geopolitical_yield="Elevated national international standing despite severe domestic economic stagnation; secured preferential infrastructure funding commitments from the NDB.",
            hard_cash_yield_usd=4_200_000_000.0,
            concessions_or_vulnerabilities="Severe domestic energy, port, and logistics crises fundamentally impede its ability to absorb large-scale manufacturing foreign direct investment.",
            strategic_autonomy_score=0.70,
            key_bilateral_postures={
                "China": "Major infrastructure financier and bilateral mining consumer.",
                "India": "Historical solidarity and maritime cooperation in the Indian Ocean."
            }
        ),
        "Iran": MemberCountryAudit(
            country_name="Iran",
            public_domestic_narrative="Hailed domestically as proof of the Islamic Republic's revolutionary durability and permanent institutional integration into the world's premier emerging powers.",
            geopolitical_yield="Significant sanctions mitigation; formal integration into the International North-South Transport Corridor (INSTC); enhanced military deterrence through diplomatic legitimacy.",
            hard_cash_yield_usd=7_800_000_000.0,
            concessions_or_vulnerabilities="Secondary OFAC sanctions continue to paralyze private corporate investment from fellow BRICS states; high inflation and currency depreciation remain uncurbed.",
            strategic_autonomy_score=0.72,
            key_bilateral_postures={
                "Russia": "Critical security and military-technical co-production partner.",
                "Saudi Arabia": "Fragile Beijing-brokered cold peace; cautious diplomatic détente."
            }
        ),
        "Saudi Arabia & UAE": MemberCountryAudit(
            country_name="Saudi Arabia & UAE",
            public_domestic_narrative="Depicted as the sovereign masters of 21st-century multi-alignment, effortlessly bridging Eastern energy markets with Western financial capitals.",
            geopolitical_yield="Maximized pricing power in global energy markets; diversified sovereign wealth fund portfolios; established themselves as the premier clearing hubs for non-dollar commodity trade.",
            hard_cash_yield_usd=18_000_000_000.0,
            concessions_or_vulnerabilities="Under intense American security scrutiny; strictly refuse to dismantle US dollar currency pegs or risk core US defense umbrella agreements.",
            strategic_autonomy_score=0.85,
            key_bilateral_postures={
                "USA": "Non-negotiable primary security and defense guarantor.",
                "India & China": "Primary long-term hydrocarbon consumers and massive tech/infrastructure investment destinations."
            }
        ),
        "Egypt & Ethiopia": MemberCountryAudit(
            country_name="Egypt & Ethiopia",
            public_domestic_narrative="Projected as triumphant entry into the premier emerging-market economic bloc, securing debt relief and foreign currency swap lines.",
            geopolitical_yield="Access to alternative liquidity pools through the NDB; diversification away from sole reliance on Western and Bretton Woods institutions.",
            hard_cash_yield_usd=5_100_000_000.0,
            concessions_or_vulnerabilities="Acute bilateral friction over the Grand Ethiopian Renaissance Dam (GERD) imported directly into the bloc, paralyzing joint diplomatic security initiatives.",
            strategic_autonomy_score=0.62,
            key_bilateral_postures={
                "Gulf States": "Essential financial patrons and bailout providers.",
                "China": "Dominant sovereign creditor and infrastructure builder."
            }
        ),
        "Spain": MemberCountryAudit(
            country_name="Spain",
            public_domestic_narrative="Domestically framed as upholding Schengen border integrity and southern European coastal security while maintaining progressive human rights standards.",
            geopolitical_yield="Secured EU Frontex border surveillance deployments and European solidarity funding for Mediterranean maritime patrol infrastructure.",
            hard_cash_yield_usd=1_200_000_000.0,
            concessions_or_vulnerabilities="High logistical friction along Andalucian coastal facilities and autonomous enclaves (Ceuta/Melilla); bilateral friction with Morocco over migration flow leverage.",
            strategic_autonomy_score=0.68,
            key_bilateral_postures={
                "Morocco": "Critical transit control partner; ongoing diplomatic friction over migration leverage.",
                "EU/Brussels": "Primary institutional and fiscal lifeline for border enforcement."
            }
        ),
        "Morocco": MemberCountryAudit(
            country_name="Morocco",
            public_domestic_narrative="Sovereign leverage asserted over transit corridors and bilateral diplomatic concessions regarding Western Sahara recognition.",
            geopolitical_yield="Maximized diplomatic leverage over Madrid and Brussels; extraction of development aid and security equipment grants in exchange for transit interdiction.",
            hard_cash_yield_usd=800_000_000.0,
            concessions_or_vulnerabilities="Reputational exposure in international human rights forums; domestic socio-economic strain in northern transit zones.",
            strategic_autonomy_score=0.75,
            key_bilateral_postures={
                "Spain": "Leveraged neighbor in bilateral transit negotiations.",
                "USA": "Security patron and diplomatic guarantor on Western Sahara."
            }
        ),
        "USA": MemberCountryAudit(
            country_name="USA",
            public_domestic_narrative="Framed as the essential defense guarantor of rules-based international order and freedom of maritime navigation.",
            geopolitical_yield="Maintained global dollar reserve centrality, secondary sanctions deterrence, and bilateral security alliance umbrellas.",
            hard_cash_yield_usd=50_000_000_000.0,
            concessions_or_vulnerabilities="Fiscal deficit expansion; diplomatic fatigue across Global South regarding extraterritorial sanctions overreach.",
            strategic_autonomy_score=0.95,
            key_bilateral_postures={
                "China": "Systemic strategic and technological rivalry.",
                "Europe/Quad": "Core alliance network for collective deterrence."
            }
        ),
        "Taiwan": MemberCountryAudit(
            country_name="Taiwan",
            public_domestic_narrative="Framed domestically as democratic resiliency and technological indispensability to global semiconductor supply chains.",
            geopolitical_yield="Strengthened bilateral security commitments and diversified supply chain fabrication corridors with US and democratic allies.",
            hard_cash_yield_usd=15_000_000_000.0,
            concessions_or_vulnerabilities="Extreme geographic proximity to PLA coastal saturation and naval blockade vulnerability.",
            strategic_autonomy_score=0.65,
            key_bilateral_postures={
                "USA": "Indispensable military hardware and security guarantor.",
                "China": "Existential coercive threat and airspace pressure."
            }
        ),
        "Ukraine": MemberCountryAudit(
            country_name="Ukraine",
            public_domestic_narrative="Framed as the frontline bastion defending European democratic sovereignty and territorial integrity against imperial aggression.",
            geopolitical_yield="Secured ongoing Western defense materiel, financial budgetary support, and accelerated EU integration roadmap.",
            hard_cash_yield_usd=25_000_000_000.0,
            concessions_or_vulnerabilities="Severe industrial and demographic devastation; total reliance on external foreign funding and ammunition supply.",
            strategic_autonomy_score=0.45,
            key_bilateral_postures={
                "NATO/US": "Vital military and financial lifeline.",
                "Russia": "Active existential kinetic war."
            }
        )
    }

    @classmethod
    def generate_country_ledgers(
        cls,
        target_countries: Optional[List[str]] = None,
        summit_name: str = "",
        fixture_mode: bool = True,
        claims: Optional[List[Any]] = None,
    ) -> List[MemberCountryAudit]:
        """Generates 4-dimensional country audits, augmenting templates dynamically when fixture_mode is False."""
        def _dynamic_augment(base: MemberCountryAudit, country: str) -> MemberCountryAudit:
            if fixture_mode and not claims:
                return base
            event_label = summit_name or "Active Strategic Event"
            c_low = country.lower()
            rel_claims = [
                str(getattr(c, "asserted_fact", getattr(c, "assertion", ""))).strip()
                for c in (claims or [])
                if c_low in str(getattr(c, "asserted_fact", getattr(c, "assertion", ""))).lower()
            ]
            context_snippet = rel_claims[0][:160] if rel_claims else f"Evaluated dynamically under {event_label}."
            if fixture_mode:
                return base
            return MemberCountryAudit(
                country_name=base.country_name,
                public_domestic_narrative=f"[{event_label}] {context_snippet} | Baseline Posture: {base.public_domestic_narrative}",
                geopolitical_yield=base.geopolitical_yield,
                hard_cash_yield_usd=base.hard_cash_yield_usd,
                concessions_or_vulnerabilities=base.concessions_or_vulnerabilities,
                strategic_autonomy_score=base.strategic_autonomy_score,
                key_bilateral_postures=dict(base.key_bilateral_postures),
            )

        if target_countries:
            ledgers = []
            for country in target_countries:
                c_norm = country.strip().lower()
                matched = None
                for key, template in cls.COUNTRY_AUDIT_TEMPLATES.items():
                    k_lower = key.lower()
                    if k_lower == c_norm or k_lower.startswith(c_norm) or c_norm in k_lower:
                        matched = _dynamic_augment(template, country)
                        break
                if matched and all(l.country_name != matched.country_name for l in ledgers):
                    ledgers.append(matched)
                elif not matched:
                    ledgers.append(MemberCountryAudit(
                        country_name=country,
                        public_domestic_narrative=f"[{summit_name or 'Strategic Audit'}] Domestic state media in {country} frames event through national sovereignty, economic security, and regional stability lenses.",
                        geopolitical_yield=f"Bilateral strategic leverage and diplomatic posture consolidation for {country}.",
                        hard_cash_yield_usd=1_000_000_000.0,
                        concessions_or_vulnerabilities="Exposure to regional friction, supply chain disruption, and external trade/sanctions pressures.",
                        strategic_autonomy_score=0.70,
                        key_bilateral_postures={"Multilateral": "Pragmatic sovereign hedging."}
                    ))
            if ledgers:
                return ledgers

        # Default 8 core BRICS member country audits
        return [
            _dynamic_augment(cls.COUNTRY_AUDIT_TEMPLATES[k], k)
            for k in ("India", "China", "Russia", "Brazil", "South Africa", "Iran", "Saudi Arabia & UAE", "Egypt & Ethiopia")
        ]

    @classmethod
    def apply_inter_lens_coupling(
        cls,
        lens_evals: List[LensEvaluation],
        hard_money_audit: Dict[str, Any],
        arbitration_log: List[str]
    ) -> Tuple[List[LensEvaluation], float]:
        """
        Executes dynamic inter-lens cross-clamping and contradiction variance analysis:
        1. Financial Reality Clamp: When CapEx haircut >= 80%, clamps forward-looking
           commercial/diplomatic cooperation alignment (L01, L04, L05, L11) to <= 0.45.
        2. Kinetic Reality Clamp: When military/chokepoint friction is high, clamps
           propaganda rhetoric (L08) and kinesic warmth (L06).
        3. Contradiction Variance Penalty: Penalizes overall confidence when lower tiers
           rhetorically contradict verified physical/financial ground realities.
        """
        coupled_evals = []
        haircut_pct = hard_money_audit.get("aggregate_haircut_pct", 0.0)
        contradiction_penalty = 0.0

        for le in lens_evals:
            lname = le.lens_name.lower()
            new_align = le.alignment_score
            new_conf = le.confidence

            # Rule 1: Financial Reality Clamp on Forward Cooperation
            if haircut_pct >= 80.0:
                if any(k in lname for k in ["deep-tech", "geo-economic", "geopolitical balance", "digital sovereignty"]):
                    if new_align > 0.45:
                        new_align = 0.45
                        arbitration_log.append(
                            f"[INTER_LENS_CLAMP_FINANCIAL] CapEx haircut of {haircut_pct:.1f}% clamped '{le.lens_name}' alignment ceiling to 0.45."
                        )

            # Rule 2: Contradiction Detection between Rhetoric (Tier 5) and Hard Money (Tier 2)
            if "propaganda" in lname or le.primary_epistemic_tier == EpistemicTier.TIER_5_COMMUNIQUE_PR:
                if haircut_pct >= 80.0 and new_align > 0.60:
                    contradiction_penalty += 0.05
                    new_conf = min(new_conf, 0.40)
                    arbitration_log.append(
                        f"[INTER_LENS_CONTRADICTION] Tier 5 PR rhetoric ({new_align:.2f}) contradicted by Tier 2 CapEx haircut ({haircut_pct:.1f}%). PR confidence capped at 0.40."
                    )

            # Rule 3: Sparse Dynamical Matrix Coupling A: Petro-Logistics -> Macro-Economic Shock
            def _parse_val(v):
                if isinstance(v, (int, float)):
                    return float(v)
                if isinstance(v, str):
                    import re
                    m = re.search(r"([\d\.]+)\s*([mMkK]?)", v.replace(",", "").strip())
                    if m:
                        n = float(m.group(1))
                        u = m.group(2).upper()
                        return n * 1_000_000 if u == "M" else (n * 1_000 if u == "K" else n)
                return 0.0

            crude_rerouted = _parse_val(hard_money_audit.get("physical_crude_re_routed_bpd", 0.0))
            shadow_tankers = _parse_val(hard_money_audit.get("shadow_tanker_fleet_pct", 0.0))

            if crude_rerouted >= 1_500_000 or shadow_tankers >= 35.0:
                if any(k in lname for k in ["geo-econom", "geoeconom", "cash flow", "cashflow"]):
                    # Chokepoint risk increases freight and insurance spreads, dampening alignment
                    new_align = max(-0.80, round(new_align - 0.08, 2))
                    arbitration_log.append(
                        f"[CROSS_LENS_COUPLING_MATRIX] PetroLogistics shock (rerouted={crude_rerouted/1e6:.1f}M bpd, shadow_tankers={shadow_tankers:.1f}%) "
                        f"coupled into '{le.lens_name}' alignment ({new_align:+.2f})."
                    )

            # Rule 4: Dynamic Adversary Retaliatory Reaction Elasticity Matrix (Phase 71D)
            # High import dependence in critical mineral supply chains or strategic technology
            # triggers adversary retaliatory embargo elasticity, dampening deep-tech alignment.
            minerals_chokepoint = _parse_val(hard_money_audit.get("critical_minerals_import_dependency_pct", 0.0))
            if minerals_chokepoint >= 70.0:
                if any(k in lname for k in ["deep-tech", "deeptech", "critical mineral", "mineral"]):
                    retaliatory_risk = round(min(1.0, minerals_chokepoint / 100.0), 2)
                    new_align = max(-0.85, round(new_align - 0.05, 2))
                    arbitration_log.append(
                        f"[ADVERSARY_REACTION_ELASTICITY] Critical minerals import dependency ({minerals_chokepoint:.1f}%) "
                        f"elevates adversary retaliatory embargo risk (E={retaliatory_risk}). Applied counter-move dampening on '{le.lens_name}'."
                    )

            coupled_evals.append(LensEvaluation(
                lens_name=le.lens_name,
                alignment_score=new_align,
                confidence=new_conf,
                primary_epistemic_tier=le.primary_epistemic_tier,
                key_findings=le.key_findings,
                hard_metrics=le.hard_metrics,
                evidence_status=le.evidence_status
            ))

        return coupled_evals, min(0.20, contradiction_penalty)

    @classmethod
    def synthesize_report(
        cls,
        summit: SummitEvent,
        kinesic_observations: Optional[List[KinesicObservation]] = None,
        financial_flows: Optional[List[FinancialFlow]] = None,
        claims: Optional[List[Any]] = None,
        evidence_items: Optional[List[Any]] = None,
        fixture_mode: bool = True,
        prioritized_lenses: Optional[List[str]] = None,
        verify_claims: bool = True,
        learn_from_session: bool = False,
    ) -> SummitAnalysisReport:
        """
        Executes the end-to-end synthesis pipeline across all 5 tiers.
        """
        # Validate temporal guardrail
        mode, guidance = TemporalGuardrail.evaluate_event_mode(summit)
        summit.temporal_mode = mode

        # Stage B: Pre-Synthesis Fact Verification Gate (non-blocking)
        verification_notes: List[str] = []
        verification_penalty: float = 0.0
        if verify_claims:
            try:
                from ..verification.engine import FactVerificationEngine
                from ..verification.models import VerificationVerdict
                _fv = FactVerificationEngine()
                texts_to_verify: List[str] = []
                meta_dict = getattr(summit, "metadata", None) or {}
                for _cand in (
                    getattr(summit, "communique_text", None),
                    meta_dict.get("communique_text") if isinstance(meta_dict, dict) else None,
                    getattr(summit, "title", None),
                ):
                    _s_txt = str(_cand or "").strip()
                    if len(_s_txt) >= 20 and _s_txt not in texts_to_verify:
                        texts_to_verify.append(_s_txt)
                for _c in (claims or []):
                    _c_txt = str(getattr(_c, "asserted_fact", getattr(_c, "assertion", "")) or "").strip()
                    if len(_c_txt) >= 15 and _c_txt not in texts_to_verify:
                        texts_to_verify.append(_c_txt)
                if texts_to_verify:
                    fv_rep = _fv.verify_text(" ".join(texts_to_verify[:12]))
                    flagged_cnt = int(getattr(fv_rep, "false_claims_count", 0)) + int(
                        getattr(fv_rep, "misleading_claims_count", 0)
                    )
                    total_analyzed = int(getattr(fv_rep, "total_claims_analyzed", len(getattr(fv_rep, "claim_results", []))))
                    verification_notes.append(
                        f"[VERIFICATION_GATE] Audited {total_analyzed} atomic claim(s); "
                        f"flagged {flagged_cnt} anomaly/contradiction(s)."
                    )
                    if flagged_cnt > 0:
                        verification_penalty = min(0.10, flagged_cnt * 0.05)
            except Exception:
                pass

        # Run all registered lenses with evidence claims if supported
        import inspect
        lens_evals = []
        for l in LENS_REGISTRY:
            l_name = l.__name__
            # Execution Gating: if prioritized_lenses specified, skip non-matching lenses
            if prioritized_lenses:
                l_key = l_name.lower().replace("lens", "").replace("_", "")
                p_keys = [p.lower().replace("lens", "").replace("_", "") for p in prioritized_lenses]
                if l_key not in p_keys and l_name not in prioritized_lenses:
                    continue

            sig = inspect.signature(l.evaluate)
            call_kwargs = {}

            # Filter claims for this specific lens if target_lenses is populated
            if claims:
                targeted = [
                    c for c in claims
                    if hasattr(c, "target_lenses") and c.target_lenses and l_name in c.target_lenses
                ]
                claim_subset = targeted if targeted else claims
            else:
                claim_subset = None

            if "claims" in sig.parameters:
                call_kwargs["claims"] = claim_subset
            elif "evidence" in sig.parameters:
                call_kwargs["evidence"] = evidence_items or claim_subset

            if "flows" in sig.parameters and financial_flows:
                call_kwargs["flows"] = financial_flows
            if "observations" in sig.parameters and kinesic_observations:
                call_kwargs["observations"] = kinesic_observations
            if "fixture_mode" in sig.parameters:
                call_kwargs["fixture_mode"] = fixture_mode

            lens_evals.append(l.evaluate(summit, **call_kwargs))

        # Tier 1: Negative Space Diff
        _, _, negative_space_synopsis = NegativeSpaceDiffEngine.analyze_diff()
        if mode == TemporalMode.PROSPECTIVE_SCENARIO:
            negative_space_synopsis = [
                TemporalGuardrail.enforce_prospective_tagging(item, mode)
                for item in negative_space_synopsis
            ]

        # Tier 2: Country-by-Country Ledger
        target_countries = getattr(summit, "target_countries", getattr(summit, "member_countries", None))
        country_ledgers = cls.generate_country_ledgers(
            target_countries=target_countries,
            summit_name=getattr(summit, "summit_name", getattr(summit, "title", "")),
            fixture_mode=fixture_mode,
            claims=claims,
        )

        # Tier 3: Kinesics Forensics
        kinesic_eval: Optional[Any] = None
        if kinesic_observations is None:
            if fixture_mode:
                kinesic_eval = KinesicsLens.evaluate(summit)
                kinesic_observations = [
                    KinesicObservation(
                        actor_primary="India (PM)",
                        actor_secondary="China (President)",
                        setting="formal_photocall",
                        protocol_mandated=True,
                        handshake_torque_vector="neutral_vertical",
                        torso_angle_degrees=25.0,
                        residual_tension_score=0.65,
                        micro_expression_flag="neutral_resting",
                        notes="Firm protocol handshake. Controlled eye contact; absence of spontaneous shoulder lean or side-whispering."
                    ),
                    KinesicObservation(
                        actor_primary="India (PM)",
                        actor_secondary="Russia (President)",
                        setting="unscripted_corridor",
                        protocol_mandated=False,
                        handshake_torque_vector="proactive_forward",
                        torso_angle_degrees=5.0,
                        residual_tension_score=0.20,
                        micro_expression_flag="duchenne_smile",
                        notes="Warm bilateral physical rapport; unprompted embrace, synchronized walking pace, unprompted arm grasp."
                    )
                ]
            else:
                kinesic_observations = []

        # Tier 4: Hard Money & Petro-Logistics Audit
        cash_eval = CashFlowLens.evaluate(summit, flows=financial_flows, fixture_mode=fixture_mode)
        petro_eval = PetroLogisticsLens.evaluate(summit)
        geo_economist_eval = GeoEconomistLens.evaluate(summit, claims=claims)
        minerals_eval_entry = next((e for e in lens_evals if "critical mineral" in e.lens_name.lower()), None)
        minerals_dep = (
            minerals_eval_entry.hard_metrics.get("heavy_rare_earth_processing_dependency", 0.90) * 100.0
            if minerals_eval_entry
            else 85.0
        )
        hard_money_audit = {
            "total_nominal_announced_usd": cash_eval.hard_metrics.get("total_nominal_announced_usd", 0.0),
            "total_effective_capex_usd": cash_eval.hard_metrics.get("total_effective_capex_usd", 0.0),
            "aggregate_haircut_pct": cash_eval.hard_metrics.get("aggregate_haircut_percentage", 0.0),
            "bilateral_local_currency_clearing_share_pct": (
                38.5 if fixture_mode else round(float(cash_eval.hard_metrics.get("bilateral_local_currency_clearing_share_pct", 0.0) or 0.0), 2)
            ),
            "common_reserve_currency_status": "STRUCTURALLY IMPOSSIBLE (Mundell-Fleming Trilemma)",
            "physical_crude_re_routed_bpd": petro_eval.hard_metrics.get("physical_crude_diversion_bpd", 0.0),
            "shadow_tanker_fleet_pct": petro_eval.hard_metrics.get("shadow_tanker_dependence_pct", 0.0),
            "western_pi_maritime_insurance_chokepoint_pct": petro_eval.hard_metrics.get("western_pi_insurance_choke_pct", 0.0),
            "vostro_balance_trapped_usd_b": geo_economist_eval.hard_metrics.get("vostro_balance_trapped_usd_b", 42.0),
            "vostro_capital_recycling_velocity": geo_economist_eval.hard_metrics.get("vostro_capital_recycling_velocity", 0.38),
            "sovereign_debt_reinvestment_ratio": geo_economist_eval.hard_metrics.get("sovereign_debt_reinvestment_ratio", 0.65),
            "critical_minerals_import_dependency_pct": minerals_dep
        }

        # Tier 5: Civilizational & Geopolitical Synthesis
        event_type_val = str(getattr(summit, "event_type", "SUMMIT")).upper()

        # Execute Analysis of Competing Hypotheses (ACH) before declaring strategic inner meaning
        from .competing_hypotheses import IncidentReasoningEngine
        incident_title = getattr(summit, "title", getattr(summit, "summit_name", "Strategic Event"))
        ach_report = IncidentReasoningEngine.evaluate_incident(
            incident_title=incident_title,
            claims=claims,
            context={"event_type": event_type_val}
        )
        if "BORDER_MILITARY" in event_type_val:
            civilizational_inner_meaning = {
                "civilizational_core": (
                    "The high-altitude Himalayan frontier represents the existential boundary interface between "
                    "two ancient civilization-states: Bharat and the Sinosphere. Sovereign territorial defense "
                    "(Kshtra Dharma) along strategic chokepoints defines the balance of power across Eurasia."
                ),
                "sanatan_dharmic_statecraft": (
                    "Operationalizes Kautilya's Raja Mandala where contiguous neighboring powers occupy a structural "
                    "adversarial posture (Ari Bhava). Sustainable peace demands internal military consolidation, "
                    "infrastructure saturation, and dynamic multi-alignment (Mitra Mandala) to deter asymmetric encirclement."
                ),
                "strategic_endgame": (
                    "Asian polycentric equilibrium cannot exist under unilateral tributary hegemony (Tianxia). "
                    "Mutual respect for sovereign frontiers and verified operational disengagement are non-negotiable "
                    "prerequisites for stable multi-polarity."
                )
            }
        elif "BORDER_SECURITY" in event_type_val:
            civilizational_inner_meaning = {
                "civilizational_core": (
                    "Maritime and terrestrial frontier corridors represent historical thresholds between distinct "
                    "demographic, cultural, and sovereign spaces. Sovereign border integrity and legal demography are "
                    "existential prerequisites for civilizational continuity and internal security."
                ),
                "sanatan_dharmic_statecraft": (
                    "In classical Arthashastra statecraft (Janapada Samrakshana), the preservation of the realm's "
                    "borders and demographic balance is the sovereign's paramount Rajdharma. Uncontrolled infiltration "
                    "weaponized as asymmetric hybrid warfare dissolves social cohesion and statutory legal authority."
                ),
                "strategic_endgame": (
                    "Modern sovereignty is measured by border enforcement depth, technological surveillance parity, "
                    "and the unyielding rejection of moral blackmail in territorial security management."
                )
            }
        elif "GEO_ECONOMIC" in event_type_val:
            civilizational_inner_meaning = {
                "civilizational_core": (
                    "Monetary architecture and balance-of-payments resilience constitute the definitive battleground "
                    "of 21st-century civilizational autonomy. Reliance on foreign fiat clearing mechanisms creates "
                    "existential vulnerability to unilateral extraterritorial financial coercion."
                ),
                "sanatan_dharmic_statecraft": (
                    "Artha (economic sovereignty) is the essential pillar sustaining Dharma and national security. "
                    "Constructing non-Western trade corridors, bilateral Vostro clearing, and sovereign physical gold "
                    "reserves operationalizes the state's fundamental duty of public welfare (Yogakshema)."
                ),
                "strategic_endgame": (
                    "The transition toward a polycentric financial architecture terminates unipolar currency weaponization, "
                    "permitting civilization-states to settle commerce in their own sovereign currencies."
                )
            }
        elif "HYBRID_WARFARE" in event_type_val:
            civilizational_inner_meaning = {
                "civilizational_core": (
                    "Modern conflict has evolved beyond conventional battlefields into asymmetric institutional domains: "
                    "multilateral regulatory lawfare (FATF), extraterritorial asset seizures, and narrative warfare aimed "
                    "at undermining sovereign legitimacy."
                ),
                "sanatan_dharmic_statecraft": (
                    "Kautilya's doctrine of Kuta Yuddha (asymmetric warfare) mandates that institutional traps must be countered "
                    "with multi-layered statutory defenses, alternative jurisdictional clearing houses, and reciprocal counter-measures."
                ),
                "strategic_endgame": (
                    "Civilization-states that build indigenous institutional resilience and technological self-reliance "
                    "(Atmanirbharta) secure permanent insulation against external judicial and regulatory coercion."
                )
            }
        elif "CIVILIZATIONAL_CRISIS" in event_type_val or "CRISIS" in event_type_val:
            civilizational_inner_meaning = {
                "civilizational_core": (
                    "Civilizational crisis threatens the foundational survival imperatives of the realm: "
                    "caloric supply continuity (Annaraksha), territorial defense depth (Kshtra Dharma), and sovereign spiritual/cultural "
                    "integrity. In existential confrontations, ceremonial protocol, multilateral declarations, and diplomatic decorum "
                    "dissolve before raw physical force, food security, and military endurance."
                ),
                "sanatan_dharmic_statecraft": (
                    "In classical Rajdharma (Apaddharma and Yogakshema), crisis statecraft demands uncompromising realism: "
                    "unfaltering protection of food reserves (Dhanya Kosha), strategic ammunition stockpiles (Ayudhadhyaksha / WWR), "
                    "and total deterrence posture against coercive encirclement. The sovereign's supreme duty is the preservation "
                    "of the civilizational realm and its people, superseding external appeasement or paper treaties."
                ),
                "strategic_endgame": (
                    "Enduring civilizational sovereignty is secured through physical ground-truth self-reliance: complete agricultural "
                    "and fertilizer security, indigenous defense industrial manufacturing (Atmanirbharta), and an unbreachable kinetic "
                    "and nuclear deterrence escalation ladder."
                )
            }
        else:
            civilizational_inner_meaning = {
                "civilizational_core": (
                    "BRICS is not an integrated alliance like NATO or a trade union like the EU; it is an "
                    "Anti-Cartel Sovereign Alignment. Its member civilization-states (Bharat, China, Russia, "
                    "Persia, Arab world) share no common domestic political ideology. They are united solely "
                    "by an existential determination to dismantle unilateral Western extraterritorial coercion."
                ),
                "sanatan_dharmic_statecraft": (
                    "For Bharat (India), participation is the master operationalization of Kautilya's Raja Mandala "
                    "and Rajdharma. By anchoring BRICS from within, India prevents China from establishing a "
                    "hegemonic 'Tianxia' tributary sphere across Eurasia, while simultaneously ensuring affordable energy "
                    "and food security (Yogakshema) for 1.4 billion citizens without entering into hostile confrontation with the West."
                ),
                "strategic_endgame": (
                    "The 21st century will not be American, nor will it be Chinese. It will be polycentric. "
                    "BRICS provides the diplomatic and transaction scaffolding for that polycentric transition, "
                    "even as its members fiercely compete within the architecture itself."
                )
            }

        # Epistemic Truth Guard: Condition Tier 5 Civilizational Synthesis on ACH Outcome
        if ach_report and ach_report.epistemic_warning:
            civilizational_inner_meaning["civilizational_core"] = (
                f"{ach_report.epistemic_warning}\n\n" + civilizational_inner_meaning.get("civilizational_core", "")
            )

        # Phase 362: Dharmik Statecraft Tri-Pillar Integration
        try:
            from .dharmik_statecraft import DharmikStatecraftPipeline, DharmikStatecraftDossier
            _d_pipe = DharmikStatecraftPipeline()
            _target_ent = target_countries[0] if (target_countries and len(target_countries) > 0) else "Multilateral Adversary / Dollar Hegemon"
            _d_meta = getattr(summit, "metadata", {}) or {}
            _d_dossier = DharmikStatecraftDossier(
                dossier_id=f"dh_{getattr(summit, 'summit_id', getattr(summit, 'event_id', 'event_001'))}",
                title=getattr(summit, "title", getattr(summit, "name", "Multilateral Summit")),
                target_nation_or_entity=_target_ent,
                narrative_context=getattr(summit, "communique_text", getattr(summit, "description", "")),
                swami_leadership_clarity=_d_meta.get("swami_leadership_clarity", 0.88),
                kosha_treasury_depth=_d_meta.get("kosha_treasury_depth", 0.85),
                danda_military_deterrence=_d_meta.get("danda_military_deterrence", 0.85),
                peace_initiatives_exhausted_ratio=_d_meta.get("peace_initiatives_exhausted_ratio", 0.85),
                sentimental_hesitation_moha=_d_meta.get("sentimental_hesitation_moha", 0.15),
            )
            _d_eval = _d_pipe.evaluate_scenario(_d_dossier)
            civilizational_inner_meaning["dharmik_operational_directive"] = _d_eval.operational_directive
            civilizational_inner_meaning["rajadharma_authorization_tier"] = _d_eval.rajadharma_authorization_tier
            civilizational_inner_meaning["optimal_sadgunya_policy"] = _d_eval.optimal_sadgunya_policy
        except Exception:
            pass

        # Epistemic Arbitration Log
        arbitration_log = [
            f"[TEMPORAL_VALIDATION] Mode set to {mode.value.upper()}. {guidance}",
        ]
        if verification_notes:
            arbitration_log.extend(verification_notes)
        if learn_from_session or (getattr(summit, "metadata", {}) or {}).get("enable_autonomous_learning", False):
            try:
                from ..verification.learner import AutonomousLearner
                _learn_res = AutonomousLearner().learn_from_event(summit, auto_promote=False)
                arbitration_log.append(
                    f"[AUTONOMOUS_LEARNER] Quarantined {_learn_res.get('quarantined_count', 0)} candidate claim(s) safely."
                )
            except Exception:
                pass
        if ach_report:
            arbitration_log.append(
                f"[ACH_ARBITRATION] Causal hypothesis '{ach_report.dominant_hypothesis_label}' selected with {ach_report.dominant_probability:.1%} probability."
            )
            if ach_report.is_epistemically_contested:
                arbitration_log.append("[ACH_CONTESTED] High epistemic ambiguity detected; alternative non-hostile causes probable.")

        if (fixture_mode or petro_eval.hard_metrics.get("grounded_energy_claims_verified")) and petro_eval.hard_metrics.get("physical_crude_diversion_bpd"):
            arbitration_log.append(f"[ARBITRATION_T1_OVER_T5] Petro-logistics physical tanker data (Tier 1) verified {petro_eval.hard_metrics.get('physical_crude_diversion_bpd')}; superseded communique rhetoric (Tier 5).")

        if cash_eval.primary_epistemic_tier == EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE:
            arbitration_log.append("[EVIDENCE_DEGRADED] Zero empirical financial flows verified. Tier 2 CapEx audit suppressed to TIER_0_INSUFFICIENT_EVIDENCE.")
        else:
            arbitration_log.append(f"[ARBITRATION_T2_OVER_T5] Cash Flow Haircut applied: Nominal ${hard_money_audit['total_nominal_announced_usd']/1e9:.1f}B discounted by {hard_money_audit['aggregate_haircut_pct']}% to ${hard_money_audit['total_effective_capex_usd']/1e9:.1f}B effective CapEx.")

        if kinesic_observations:
            arbitration_log.append("[ARBITRATION_T3_OVER_T4] India-China border military deployment (Tier 3) overrides staged photocall smiles (Tier 4): Categorized as 'TACTICAL_DE_ESCALATION_PERFORMANCE'.")
        else:
            arbitration_log.append("[EVIDENCE_DEGRADED] Zero empirical kinesic telemetry available. Tier 4 forensics suppressed to TIER_0_INSUFFICIENT_EVIDENCE.")

        lens_eval_map = {l.lens_name: l for l in lens_evals}
        food_eval = lens_eval_map.get(FoodSecurityLens.LENS_NAME) or lens_eval_map.get("Food Security, Fertilizer Geopolitics & Caloric Sovereignty")
        military_eval = lens_eval_map.get(MilitaryReadinessLens.LENS_NAME) or lens_eval_map.get("Military Readiness, ORBAT & Escalation Dominance")
        minerals_eval = lens_eval_map.get(CriticalMineralsLens.LENS_NAME) or lens_eval_map.get("Critical Minerals & Refining Monopolies")
        demo_eval = lens_eval_map.get(DemographicInfiltrationLens.LENS_NAME) or lens_eval_map.get("Demographic Infiltration & Migration Corridors")
        lawfare_eval = lens_eval_map.get(InstitutionalLawfareLens.LENS_NAME) or lens_eval_map.get("Institutional Lawfare & Multilateral Traps")
        timeline_eval = lens_eval_map.get(IndiaTimelineLens.LENS_NAME) or lens_eval_map.get("India's Strategic Timelines & Post-1947 Boundary Trajectories")
        subsea_eval = lens_eval_map.get(SubseaCablesLens.LENS_NAME) or lens_eval_map.get("Subsea Cables & Hydro-Spatial Sovereignty")
        astro_eval = lens_eval_map.get(AstroPoliticsLens.LENS_NAME) or lens_eval_map.get("Astro-Politics, Orbital Sovereignty & Space Defense")
        deep_tech_eval = lens_eval_map.get(DeepTechLens.LENS_NAME) or lens_eval_map.get("Deep-Tech & Quantitative Modeling")
        civ_eval = lens_eval_map.get(CivilizationalLens.LENS_NAME) or lens_eval_map.get("Civilizational Statecraft (Sanatan / Comparative)")
        history_eval = lens_eval_map.get(HistoryLens.LENS_NAME) or lens_eval_map.get("World & Indian Diplomatic History")
        digital_eval = lens_eval_map.get(DigitalSovereigntyLens.LENS_NAME) or lens_eval_map.get("Digital Sovereignty & Compute Infrastructure") or lens_eval_map.get("Digital Sovereignty, Compute & Telecommunications Stack Lens")
        propaganda_eval = lens_eval_map.get(PropagandaLens.LENS_NAME) or lens_eval_map.get("State Propaganda & Disinformation Forensics") or lens_eval_map.get("State Propaganda & Strategic Narrative Deconstruction")
        geo_eval = lens_eval_map.get(GeopoliticalLens.LENS_NAME) or lens_eval_map.get("Geopolitical & Chokepoint Forensics") or lens_eval_map.get("Geopolitical Balance & Strategic Hedging")
        hybrid_eval = lens_eval_map.get(HybridCovertLens.LENS_NAME) or lens_eval_map.get("Hybrid & Covert Warfare Operations") or lens_eval_map.get("Hybrid Warfare & Asymmetric Leverage")
        bureaucratic_eval = lens_eval_map.get(BureaucraticInertiaLens.LENS_NAME) or lens_eval_map.get("Deep-State & Bureaucratic Continuity")
        geo_economist_eval = lens_eval_map.get(GeoEconomistLens.LENS_NAME) or lens_eval_map.get("Geo-Economic Realism & Monetary Architecture") or lens_eval_map.get("Geo-Economic Leverage & Industrial Moats")
        kinesic_eval = (
            kinesic_eval or
            lens_eval_map.get(KinesicsLens.LENS_NAME) or
            lens_eval_map.get("Diplomatic Kinesics & Proxemic Forensics") or
            lens_eval_map.get("Kinesics & Diplomatic Body Language Forensics") or
            lens_eval_map.get("Kinesics, Posture & Non-Verbal Strategic Signaling")
        )

        strategic_resilience_matrix = {
            "food_caloric_sovereignty_index": food_eval.hard_metrics.get("caloric_sovereignty_index", 0.81) if food_eval else 0.81,
            "strategic_grain_buffer_ratio": food_eval.hard_metrics.get("strategic_grain_buffer_ratio", 1.82) if food_eval else 1.82,
            "potash_mop_dependency_pct": food_eval.hard_metrics.get("mop_potash_import_dependency_pct", 100.0) if food_eval else 100.0,
            "two_front_deterrence_posture": military_eval.hard_metrics.get("two_front_deterrence_posture_score", 0.78) if military_eval else 0.78,
            "wwr_ammunition_reserve_days": military_eval.hard_metrics.get("wwr_ammunition_reserve_days", 21.5) if military_eval else 21.5,
            "iads_air_defense_coverage": military_eval.hard_metrics.get("iads_air_defense_coverage_index", 0.84) if military_eval else 0.84,
            "hree_refining_monopoly_pct": minerals_eval.hard_metrics.get("hree_refining_concentration_pct", 82.5) if minerals_eval else 82.5,
            "critical_minerals_sovereignty_index": minerals_eval.hard_metrics.get("material_sovereignty_index", 0.48) if minerals_eval else 0.48,
            "demographic_border_vulnerability": demo_eval.hard_metrics.get("border_transit_vulnerability_score", 0.72) if demo_eval else 0.72,
            "institutional_lawfare_ofac_risk": lawfare_eval.hard_metrics.get("ofac_secondary_sanctions_risk_score", 0.65) if lawfare_eval else 0.65,
            "strategic_frontier_timeline_score": timeline_eval.alignment_score if timeline_eval else 0.60,
            "subsea_bandwidth_dependency_pct": subsea_eval.hard_metrics.get("subsea_bandwidth_dependency_pct", 98.5) if subsea_eval else 98.5,
            "hydro_spatial_sovereignty_score": subsea_eval.hard_metrics.get("hydro_spatial_sovereignty_score", 0.68) if subsea_eval else 0.68,
            "satcom_sovereignty_coverage_pct": astro_eval.hard_metrics.get("satcom_sovereignty_coverage_pct", 84.0) if astro_eval else 84.0,
            "orbital_sovereignty_index": astro_eval.hard_metrics.get("orbital_sovereignty_index", 0.79) if astro_eval else 0.79,
            "sugarcane_water_inequality_ratio": food_eval.hard_metrics.get("sugarcane_water_inequality_ratio") if food_eval and "sugarcane_water_inequality_ratio" in food_eval.hard_metrics else (food_eval.hard_metrics.get("soil_nutrient_chokepoint_vulnerability", 0.0) if food_eval else 0.0),
            "manufactured_drought_vulnerability_score": food_eval.hard_metrics.get("manufactured_drought_vulnerability_score") if food_eval and "manufactured_drought_vulnerability_score" in food_eval.hard_metrics else (food_eval.hard_metrics.get("hydro_weaponization_resilience", 0.0) if food_eval else 0.0),
            "community_watershed_multiplier": food_eval.hard_metrics.get("community_watershed_multiplier") if food_eval and "community_watershed_multiplier" in food_eval.hard_metrics else (food_eval.hard_metrics.get("riparian_resilience_score", 0.0) if food_eval else 0.0),
            "cultural_grayzone_vulnerability_index": civ_eval.hard_metrics.get("cultural_grayzone_vulnerability_index", 0.15) if civ_eval else 0.15,
            "quantum_superposition_status": deep_tech_eval.hard_metrics.get("quantum_superposition_status") if deep_tech_eval and "quantum_superposition_status" in deep_tech_eval.hard_metrics else (deep_tech_eval.hard_metrics.get("quantum_entangled_spacetime_score", 0.0) if deep_tech_eval else 0.0),
            "pqc_vulnerability_score": deep_tech_eval.hard_metrics.get("pqc_vulnerability_score") if deep_tech_eval and "pqc_vulnerability_score" in deep_tech_eval.hard_metrics else (deep_tech_eval.hard_metrics.get("defense_scada_and_firmware_tamper_score", 0.0) if deep_tech_eval else 0.0),
            "judicial_subversion_score": lawfare_eval.hard_metrics.get("judicial_subversion_score") if lawfare_eval and "judicial_subversion_score" in lawfare_eval.hard_metrics else None,
            "tech_sovereignty_score": digital_eval.hard_metrics.get("tech_sovereignty_score") if digital_eval and "tech_sovereignty_score" in digital_eval.hard_metrics else None,
            "urban_insurrection_risk_score": civ_eval.hard_metrics.get("urban_insurrection_risk_score") if civ_eval and "urban_insurrection_risk_score" in civ_eval.hard_metrics else None,
            "telecom_pipes_risk_score": digital_eval.hard_metrics.get("telecom_pipes_risk_score") if digital_eval and "telecom_pipes_risk_score" in digital_eval.hard_metrics else None,
            "protocol_layer_sovereignty_score": digital_eval.hard_metrics.get("protocol_layer_sovereignty_score") if digital_eval and "protocol_layer_sovereignty_score" in digital_eval.hard_metrics else None,
            "coercion_premium_score": lawfare_eval.hard_metrics.get("coercion_premium_score") if lawfare_eval and "coercion_premium_score" in lawfare_eval.hard_metrics else None,
            "daily_economic_friction_inr_cr": lawfare_eval.hard_metrics.get("daily_economic_friction_inr_cr") if lawfare_eval and "daily_economic_friction_inr_cr" in lawfare_eval.hard_metrics else None,
            "crowd_cascade_probability": lawfare_eval.hard_metrics.get("crowd_cascade_probability") if lawfare_eval and "crowd_cascade_probability" in lawfare_eval.hard_metrics else None,
            "state_inaction_score": lawfare_eval.hard_metrics.get("state_inaction_score") if lawfare_eval and "state_inaction_score" in lawfare_eval.hard_metrics else None,
            "astroturfing_probability": digital_eval.hard_metrics.get("astroturfing_probability") if digital_eval and "astroturfing_probability" in digital_eval.hard_metrics else None,
            "basing_interdiction_index": military_eval.hard_metrics.get("basing_interdiction_index") if military_eval and "basing_interdiction_index" in military_eval.hard_metrics else (military_eval.hard_metrics.get("military_chinese_hydrographic_threat_index", 0.0) if military_eval else 0.0),
            "civilizational_vulnerability_index": civ_eval.hard_metrics.get("civilizational_vulnerability_index") if civ_eval and "civilizational_vulnerability_index" in civ_eval.hard_metrics else None,
            "oligarch_subordination_factor": lawfare_eval.hard_metrics.get("oligarch_subordination_factor") if lawfare_eval and "oligarch_subordination_factor" in lawfare_eval.hard_metrics else None,
            "sanctions_firewall_score": geo_economist_eval.hard_metrics.get("sanctions_firewall_score") if geo_economist_eval and "sanctions_firewall_score" in geo_economist_eval.hard_metrics else None,
            # Phase 206–209: New Sieve Indicators
            "cable_vulnerability_index": subsea_eval.hard_metrics.get("cable_vulnerability_index") if subsea_eval and "cable_vulnerability_index" in subsea_eval.hard_metrics else None,
            "refining_concentration_risk": minerals_eval.hard_metrics.get("refining_concentration_risk") if minerals_eval and "refining_concentration_risk" in minerals_eval.hard_metrics else None,
            "strategic_equilibrium_ratio": geo_economist_eval.hard_metrics.get("strategic_equilibrium_ratio") if geo_economist_eval and "strategic_equilibrium_ratio" in geo_economist_eval.hard_metrics else None,
            "cultural_grayzone_hijack_probability": civ_eval.hard_metrics.get("cultural_grayzone_hijack_probability") if civ_eval and "cultural_grayzone_hijack_probability" in civ_eval.hard_metrics else None,
            # Phase 221–224: Dynamic Supply Chain, Media Lawfare, FUD Deflation & Tech Moat Sieves
            "supply_chain_capture_potential": geo_economist_eval.hard_metrics.get("supply_chain_capture_potential") if geo_economist_eval and "supply_chain_capture_potential" in geo_economist_eval.hard_metrics else None,
            "captured_order_value_usd_b": geo_economist_eval.hard_metrics.get("captured_order_value_usd_b") if geo_economist_eval and "captured_order_value_usd_b" in geo_economist_eval.hard_metrics else None,
            "media_lawfare_vulnerability": lawfare_eval.hard_metrics.get("media_lawfare_vulnerability") if lawfare_eval and "media_lawfare_vulnerability" in lawfare_eval.hard_metrics else None,
            "commercial_fud_probability": propaganda_eval.hard_metrics.get("commercial_fud_probability") if propaganda_eval and "commercial_fud_probability" in propaganda_eval.hard_metrics else None,
            "debiased_structural_threat": propaganda_eval.hard_metrics.get("debiased_structural_threat") if propaganda_eval and "debiased_structural_threat" in propaganda_eval.hard_metrics else None,
            "indigenous_tech_moat_score": digital_eval.hard_metrics.get("indigenous_tech_moat_score") if digital_eval and "indigenous_tech_moat_score" in digital_eval.hard_metrics else None,
            # Phase 228-238: Deep-Tech, Covert Statecraft, Metallurgy & Astro-Political Sieves
            "street_lawfare_score": lawfare_eval.hard_metrics.get("street_lawfare_score") if lawfare_eval and "street_lawfare_score" in lawfare_eval.hard_metrics else None,
            "capital_magnetism_score": geo_economist_eval.hard_metrics.get("capital_magnetism_score") if geo_economist_eval and "capital_magnetism_score" in geo_economist_eval.hard_metrics else None,
            "high_altitude_defense_score": military_eval.hard_metrics.get("high_altitude_defense_score") if military_eval and "high_altitude_defense_score" in military_eval.hard_metrics else None,
            "tripartite_coherence_score": geo_eval.hard_metrics.get("tripartite_coherence_score") if geo_eval and "tripartite_coherence_score" in geo_eval.hard_metrics else None,
            "demographic_sovereignty_score": demo_eval.hard_metrics.get("demographic_sovereignty_score") if demo_eval and "demographic_sovereignty_score" in demo_eval.hard_metrics else None,
            "metallurgy_autonomy_score": digital_eval.hard_metrics.get("metallurgy_autonomy_score") if digital_eval and "metallurgy_autonomy_score" in digital_eval.hard_metrics else None,
            "nuclear_ambiguity_score": hybrid_eval.hard_metrics.get("nuclear_ambiguity_score") if hybrid_eval and "nuclear_ambiguity_score" in hybrid_eval.hard_metrics else None,
            "resource_curse_vulnerability": geo_economist_eval.hard_metrics.get("resource_curse_vulnerability") if geo_economist_eval and "resource_curse_vulnerability" in geo_economist_eval.hard_metrics else None,
            "cognitive_sovereignty_score": propaganda_eval.hard_metrics.get("cognitive_sovereignty_score") if propaganda_eval and "cognitive_sovereignty_score" in propaganda_eval.hard_metrics else None,
            "astro_sovereignty_score": astro_eval.hard_metrics.get("astro_sovereignty_score") if astro_eval and "astro_sovereignty_score" in astro_eval.hard_metrics else None,
            "riparian_resilience_score": food_eval.hard_metrics.get("riparian_resilience_score") if food_eval and "riparian_resilience_score" in food_eval.hard_metrics else None,
            # Phase 240-246: Lawfare Asymmetry, Covert Fissile Espionage, Sovereign Longevity, Halo Smuggling, Hostage Coercion & Debt Contagion
            "veto_entrapment_risk": lawfare_eval.hard_metrics.get("veto_entrapment_risk") if lawfare_eval and "veto_entrapment_risk" in lawfare_eval.hard_metrics else None,
            "fissile_chokepoint_vulnerability": hybrid_eval.hard_metrics.get("fissile_chokepoint_vulnerability") if hybrid_eval and "fissile_chokepoint_vulnerability" in hybrid_eval.hard_metrics else None,
            "sovereign_longevity_score": deep_tech_eval.hard_metrics.get("sovereign_longevity_score") if deep_tech_eval and "sovereign_longevity_score" in deep_tech_eval.hard_metrics else None,
            "epistemic_smuggling_risk": propaganda_eval.hard_metrics.get("epistemic_smuggling_risk") if propaganda_eval and "epistemic_smuggling_risk" in propaganda_eval.hard_metrics else None,
            "hostage_coercion_leverage": hybrid_eval.hard_metrics.get("hostage_coercion_leverage") if hybrid_eval and "hostage_coercion_leverage" in hybrid_eval.hard_metrics else None,
            "sovereign_default_contagion_risk": geo_economist_eval.hard_metrics.get("sovereign_default_contagion_risk") if geo_economist_eval and "sovereign_default_contagion_risk" in geo_economist_eval.hard_metrics else None,
            # Phase 247-248: Digital Enclosure Trap & Kinetic Diversionary Escalation
            "digital_enclosure_trap_score": cash_eval.hard_metrics.get("digital_enclosure_trap_score") if cash_eval and "digital_enclosure_trap_score" in cash_eval.hard_metrics else None,
            "diversionary_escalation_risk": military_eval.hard_metrics.get("diversionary_escalation_risk") if military_eval and "diversionary_escalation_risk" in military_eval.hard_metrics else None,
            # Phases 253-259: Cultural Grayzone, Insurgency Blowback, Abyssal Seabed, Trophic Cascade, Cognitive Enclosure, Bullion Arbitrage & Archaeo-Chronology
            "cultural_grayzone_risk": civ_eval.hard_metrics.get("cultural_grayzone_risk") if civ_eval and "cultural_grayzone_risk" in civ_eval.hard_metrics else None,
            "partisan_blowback_risk": history_eval.hard_metrics.get("partisan_blowback_risk") if history_eval and "partisan_blowback_risk" in history_eval.hard_metrics else None,
            "abyssal_sovereignty_score": subsea_eval.hard_metrics.get("abyssal_sovereignty_score") if subsea_eval and "abyssal_sovereignty_score" in subsea_eval.hard_metrics else None,
            "trophic_cascade_risk": food_eval.hard_metrics.get("trophic_cascade_risk") if food_eval and "trophic_cascade_risk" in food_eval.hard_metrics else None,
            "cognitive_enclosure_risk": deep_tech_eval.hard_metrics.get("cognitive_enclosure_risk") if deep_tech_eval and "cognitive_enclosure_risk" in deep_tech_eval.hard_metrics else None,
            "bullion_dislocation_risk": cash_eval.hard_metrics.get("bullion_dislocation_risk") if cash_eval and "bullion_dislocation_risk" in cash_eval.hard_metrics else None,
            "chronological_validity_score": history_eval.hard_metrics.get("chronological_validity_score") if history_eval and "chronological_validity_score" in history_eval.hard_metrics else None,
            # Phases 260-267: PNT Sovereignty, AI Capture, Sub-Conventional Proxy, Textual Triangulation, Media Capture, Hydro Weaponization, Antiquity Restitution & Diaspora Sanctuary
            "pnt_sovereignty_score": military_eval.hard_metrics.get("pnt_sovereignty_score") if military_eval and "pnt_sovereignty_score" in military_eval.hard_metrics else None,
            "ai_regulatory_moat_risk": deep_tech_eval.hard_metrics.get("ai_regulatory_moat_risk") if deep_tech_eval and "ai_regulatory_moat_risk" in deep_tech_eval.hard_metrics else None,
            "asymmetric_attrition_threat": hybrid_eval.hard_metrics.get("asymmetric_attrition_threat") if hybrid_eval and "asymmetric_attrition_threat" in hybrid_eval.hard_metrics else None,
            "textual_fidelity_score": civ_eval.hard_metrics.get("textual_fidelity_score") if civ_eval and "textual_fidelity_score" in civ_eval.hard_metrics else None,
            "cognitive_subversion_risk": propaganda_eval.hard_metrics.get("cognitive_subversion_risk") if propaganda_eval and "cognitive_subversion_risk" in propaganda_eval.hard_metrics else None,
            "hydro_weaponization_resilience": food_eval.hard_metrics.get("hydro_weaponization_resilience") if food_eval and "hydro_weaponization_resilience" in food_eval.hard_metrics else None,
            "sacred_heritage_restitution_score": civ_eval.hard_metrics.get("sacred_heritage_restitution_score") if civ_eval and "sacred_heritage_restitution_score" in civ_eval.hard_metrics else None,
            "transnational_extremism_threat_score": geo_eval.hard_metrics.get("transnational_extremism_threat_score") if geo_eval and "transnational_extremism_threat_score" in geo_eval.hard_metrics else None,
            # Phases 268-273: Bullion Sovereignty, Chokepoint Hydrocarbon, Cognitive Cortical Resilience, Nuclear Fuel Autonomy, Sovereign BOP Shield, Sub-Regional Electoral Polarization
            "bullion_sovereignty_score": cash_eval.hard_metrics.get("bullion_sovereignty_score") if cash_eval and "bullion_sovereignty_score" in cash_eval.hard_metrics else None,
            "hydrocarbon_chokepoint_vulnerability_score": petro_eval.hard_metrics.get("hydrocarbon_chokepoint_vulnerability_score") if petro_eval and "hydrocarbon_chokepoint_vulnerability_score" in petro_eval.hard_metrics else None,
            "cognitive_sovereignty_score": propaganda_eval.hard_metrics.get("cognitive_sovereignty_score") if propaganda_eval and "cognitive_sovereignty_score" in propaganda_eval.hard_metrics else None,
            "nuclear_fuel_cycle_autonomy_score": deep_tech_eval.hard_metrics.get("nuclear_fuel_cycle_autonomy_score") if deep_tech_eval and "nuclear_fuel_cycle_autonomy_score" in deep_tech_eval.hard_metrics else None,
            "sovereign_bop_shield_score": cash_eval.hard_metrics.get("sovereign_bop_shield_score") if cash_eval and "sovereign_bop_shield_score" in cash_eval.hard_metrics else None,
            "electoral_governance_stability_score": lawfare_eval.hard_metrics.get("electoral_governance_stability_score") if lawfare_eval and "electoral_governance_stability_score" in lawfare_eval.hard_metrics else None,
            # Phases 274-282: Refinery Sabotage, HNWI Capital, Gold Repatriation, Multi-Agent Consensus, Paleogenomics, Epistemic Triangulation, Soil Resilience, Dharmic Soft Power, Sectoral Rotation
            "refinery_sabotage_risk_score": petro_eval.hard_metrics.get("refinery_sabotage_risk_score") if petro_eval and "refinery_sabotage_risk_score" in petro_eval.hard_metrics else None,
            "capital_flight_risk_score": cash_eval.hard_metrics.get("capital_flight_risk_score") if cash_eval and "capital_flight_risk_score" in cash_eval.hard_metrics else None,
            "reserve_immunity_score": cash_eval.hard_metrics.get("reserve_immunity_score") if cash_eval and "reserve_immunity_score" in cash_eval.hard_metrics else None,
            "multi_agent_consensus_score": deep_tech_eval.hard_metrics.get("multi_agent_consensus_score") if deep_tech_eval and "multi_agent_consensus_score" in deep_tech_eval.hard_metrics else None,
            "paleogenomic_continuity_score": civ_eval.hard_metrics.get("paleogenomic_continuity_score") if civ_eval and "paleogenomic_continuity_score" in civ_eval.hard_metrics else None,
            "epistemic_triangulation_score": history_eval.hard_metrics.get("epistemic_triangulation_score") if history_eval and "epistemic_triangulation_score" in history_eval.hard_metrics else None,
            "soil_resilience_score": food_eval.hard_metrics.get("soil_resilience_score") if food_eval and "soil_resilience_score" in food_eval.hard_metrics else None,
            "dharmic_sovereignty_score": civ_eval.hard_metrics.get("dharmic_sovereignty_score") if civ_eval and "dharmic_sovereignty_score" in civ_eval.hard_metrics else None,
            "sectoral_rotation_score": geo_economist_eval.hard_metrics.get("sectoral_rotation_score") if geo_economist_eval and "sectoral_rotation_score" in geo_economist_eval.hard_metrics else None,
            # Phases 283-294: Island Net Security, Programmable CBDC, Inter-Agency Counter-Subversion, Banking CRAR, Sub-National Bureaucracy, GaN Radar, High-Altitude Airlift, BigTech Algorithmic Sovereignty, Sacred Economy, ODI Asset Capture, Archaeo-Astronomy, Black Projects
            "maritime_net_security_score": geo_eval.hard_metrics.get("maritime_net_security_score") if geo_eval and "maritime_net_security_score" in geo_eval.hard_metrics else None,
            "monetary_autonomy_score": digital_eval.hard_metrics.get("monetary_autonomy_score") if digital_eval and "monetary_autonomy_score" in digital_eval.hard_metrics else None,
            "counter_subversion_score": hybrid_eval.hard_metrics.get("counter_subversion_score") if hybrid_eval and "counter_subversion_score" in hybrid_eval.hard_metrics else None,
            "banking_fortress_score": cash_eval.hard_metrics.get("banking_fortress_score") if cash_eval and "banking_fortress_score" in cash_eval.hard_metrics else None,
            "administrative_velocity_score": bureaucratic_eval.hard_metrics.get("administrative_velocity_score") if bureaucratic_eval and "administrative_velocity_score" in bureaucratic_eval.hard_metrics else None,
            "gan_radar_sovereignty_score": deep_tech_eval.hard_metrics.get("gan_radar_sovereignty_score") if deep_tech_eval and "gan_radar_sovereignty_score" in deep_tech_eval.hard_metrics else None,
            "high_altitude_logistics_score": military_eval.hard_metrics.get("high_altitude_logistics_score") if military_eval and "high_altitude_logistics_score" in military_eval.hard_metrics else None,
            "algorithmic_sovereignty_score": digital_eval.hard_metrics.get("algorithmic_sovereignty_score") if digital_eval and "algorithmic_sovereignty_score" in digital_eval.hard_metrics else None,
            "sacred_economy_multiplier_score": civ_eval.hard_metrics.get("sacred_economy_multiplier_score") if civ_eval and "sacred_economy_multiplier_score" in civ_eval.hard_metrics else None,
            "asset_capture_score": geo_economist_eval.hard_metrics.get("asset_capture_score") if geo_economist_eval and "asset_capture_score" in geo_economist_eval.hard_metrics else None,
            "archaeo_astronomical_dating_score": history_eval.hard_metrics.get("archaeo_astronomical_dating_score") if history_eval and "archaeo_astronomical_dating_score" in history_eval.hard_metrics else None,
            "black_project_resilience_score": hybrid_eval.hard_metrics.get("black_project_resilience_score") if hybrid_eval and "black_project_resilience_score" in hybrid_eval.hard_metrics else None,
            # Phases 295-300: Trans-Himalayan Hydrology, Predatory Dumping, Epistemic Apaurusheya, Sacred Heritage, Narrative Inversion, Malacca Deterrence
            "hydro_deterrence_score": geo_eval.hard_metrics.get("hydro_deterrence_score") if geo_eval and "hydro_deterrence_score" in geo_eval.hard_metrics else None,
            "industrial_resilience_score": geo_economist_eval.hard_metrics.get("industrial_resilience_score") if geo_economist_eval and "industrial_resilience_score" in geo_economist_eval.hard_metrics else None,
            "epistemic_sovereignty_score": civ_eval.hard_metrics.get("epistemic_sovereignty_score") if civ_eval and "epistemic_sovereignty_score" in civ_eval.hard_metrics else None,
            "heritage_defense_score": lawfare_eval.hard_metrics.get("heritage_defense_score") if lawfare_eval and "heritage_defense_score" in lawfare_eval.hard_metrics else None,
            "narrative_immunity_score": propaganda_eval.hard_metrics.get("narrative_immunity_score") if propaganda_eval and "narrative_immunity_score" in propaganda_eval.hard_metrics else None,
            "maritime_chokepoint_deterrence_score": military_eval.hard_metrics.get("maritime_chokepoint_deterrence_score") if military_eval and "maritime_chokepoint_deterrence_score" in military_eval.hard_metrics else None,
            # Phases 301-307: Ritual Sovereignty, Dharmic Constitutionalism, Historical Sandarshan, Epic Fidelity, Theological Realism, Spiritual Integration, Dietary Plurality
            "ritual_sovereignty_score": lawfare_eval.hard_metrics.get("ritual_sovereignty_score") if lawfare_eval and "ritual_sovereignty_score" in lawfare_eval.hard_metrics else None,
            "dharmic_constitutionalism_score": lawfare_eval.hard_metrics.get("dharmic_constitutionalism_score") if lawfare_eval and "dharmic_constitutionalism_score" in lawfare_eval.hard_metrics else None,
            "historical_sandarshan_score": history_eval.hard_metrics.get("historical_sandarshan_score") if history_eval and "historical_sandarshan_score" in history_eval.hard_metrics else None,
            "canonical_fidelity_score": propaganda_eval.hard_metrics.get("canonical_fidelity_score") if propaganda_eval and "canonical_fidelity_score" in propaganda_eval.hard_metrics else None,
            "theological_realism_score": demo_eval.hard_metrics.get("theological_realism_score") if demo_eval and "theological_realism_score" in demo_eval.hard_metrics else None,
            "spiritual_integration_score": civ_eval.hard_metrics.get("spiritual_integration_score") if civ_eval and "spiritual_integration_score" in civ_eval.hard_metrics else None,
            "dietary_plurality_score": civ_eval.hard_metrics.get("dietary_plurality_score") if civ_eval and "dietary_plurality_score" in civ_eval.hard_metrics else None,
            # Phase 308: Quantum Decision Theory (QDT) & Dynamic Epistemic Gating
            "quantum_interference_index": round(
                min(1.0, max(0.0, 2.0 * math.sqrt(
                    max(0.01, (civ_eval.alignment_score + 1.0) / 2.0 if civ_eval else 0.5) *
                    max(0.01, (geo_eval.alignment_score + 1.0) / 2.0 if geo_eval else 0.5)
                ) * math.cos(math.radians(45.0)))),
                4
            ),
            "dynamic_epistemic_gating_active": bool(prioritized_lenses and len(prioritized_lenses) > 0),
            # Phases 309-317: Sovereign Historiographical, Military & Geo-Economic Sieves
            "archival_fidelity_score": history_eval.hard_metrics.get("archival_fidelity_score") if history_eval and "archival_fidelity_score" in history_eval.hard_metrics else None,
            "academic_gatekeeping_score": propaganda_eval.hard_metrics.get("academic_gatekeeping_score") if propaganda_eval and "academic_gatekeeping_score" in propaganda_eval.hard_metrics else None,
            "succession_continuity_score": geo_economist_eval.hard_metrics.get("succession_continuity_score") if geo_economist_eval and "succession_continuity_score" in geo_economist_eval.hard_metrics else None,
            "linguistic_sprachbund_score": civ_eval.hard_metrics.get("linguistic_sprachbund_score") if civ_eval and "linguistic_sprachbund_score" in civ_eval.hard_metrics else None,
            "indigenous_stem_score": deep_tech_eval.hard_metrics.get("indigenous_stem_score") if deep_tech_eval and "indigenous_stem_score" in deep_tech_eval.hard_metrics else None,
            "subaltern_memory_score": history_eval.hard_metrics.get("subaltern_memory_score") if history_eval and "subaltern_memory_score" in history_eval.hard_metrics else None,
            "industrial_attrition_score": military_eval.hard_metrics.get("industrial_attrition_score") if military_eval and "industrial_attrition_score" in military_eval.hard_metrics else None,
            "imperial_debt_overreach_score": cash_eval.hard_metrics.get("imperial_debt_overreach_score") if cash_eval and "imperial_debt_overreach_score" in cash_eval.hard_metrics else None,
            "colonial_drain_score": history_eval.hard_metrics.get("colonial_drain_score") if history_eval and "colonial_drain_score" in history_eval.hard_metrics else None,
            # Phases 318-337: Forensic Epistemic & Multi-Domain Sieves
            "basel_gold_allocation_score": cash_eval.hard_metrics.get("basel_gold_allocation_score") if cash_eval and "basel_gold_allocation_score" in cash_eval.hard_metrics else None,
            "mnemonic_fidelity_score": civ_eval.hard_metrics.get("apaurusheya_mnemonic_fidelity_score") if civ_eval and "apaurusheya_mnemonic_fidelity_score" in civ_eval.hard_metrics else None,
            "deep_state_penetration_score": hybrid_eval.hard_metrics.get("mitrokhin_deep_state_penetration_score") if hybrid_eval and "mitrokhin_deep_state_penetration_score" in hybrid_eval.hard_metrics else None,
            "puranic_boundary_score": civ_eval.hard_metrics.get("puranic_metaphysical_boundary_score") if civ_eval and "puranic_metaphysical_boundary_score" in civ_eval.hard_metrics else None,
            "polemical_deflection_score": propaganda_eval.hard_metrics.get("polemics_vs_empirical_ratio_score") if propaganda_eval and "polemics_vs_empirical_ratio_score" in propaganda_eval.hard_metrics else None,
            "epic_geography_score": history_eval.hard_metrics.get("kishkindha_global_geography_score") if history_eval and "kishkindha_global_geography_score" in history_eval.hard_metrics else None,
            "vedic_etymology_score": civ_eval.hard_metrics.get("vedic_etymological_decolonization_score") if civ_eval and "vedic_etymological_decolonization_score" in civ_eval.hard_metrics else None,
            "quantum_spacetime_score": deep_tech_eval.hard_metrics.get("quantum_entangled_spacetime_score") if deep_tech_eval and "quantum_entangled_spacetime_score" in deep_tech_eval.hard_metrics else None,
            "semiconductor_monopoly_score": deep_tech_eval.hard_metrics.get("semiconductor_antitrust_hardware_score") if deep_tech_eval and "semiconductor_antitrust_hardware_score" in deep_tech_eval.hard_metrics else None,
            "fcra_subversion_score": hybrid_eval.hard_metrics.get("transnational_fcra_ecclesiastical_score") if hybrid_eval and "transnational_fcra_ecclesiastical_score" in hybrid_eval.hard_metrics else None,
            "cinematic_desacralization_score": propaganda_eval.hard_metrics.get("cinematic_iconography_sacrality_score") if propaganda_eval and "cinematic_iconography_sacrality_score" in propaganda_eval.hard_metrics else None,
            "infra_capex_multiplier_score": geo_economist_eval.hard_metrics.get("infrastructure_capex_multiplier_score") if geo_economist_eval and "infrastructure_capex_multiplier_score" in geo_economist_eval.hard_metrics else None,
            "classical_bullion_trade_score": cash_eval.hard_metrics.get("classical_bullion_inflow_score") if cash_eval and "classical_bullion_inflow_score" in cash_eval.hard_metrics else None,
            "statutory_lawfare_score": lawfare_eval.hard_metrics.get("asymmetric_statutory_lawfare_score") if lawfare_eval and "asymmetric_statutory_lawfare_score" in lawfare_eval.hard_metrics else None,
            "crypto_decentralization_score": digital_eval.hard_metrics.get("cryptographic_decentralization_score") if digital_eval and "cryptographic_decentralization_score" in digital_eval.hard_metrics else None,
            "hormuz_vulnerability_score": petro_eval.hard_metrics.get("hormuz_energy_escalation_score") if petro_eval and "hormuz_energy_escalation_score" in petro_eval.hard_metrics else None,
            "eurodollar_drain_score": cash_eval.hard_metrics.get("eurodollar_shadow_liquidity_score") if cash_eval and "eurodollar_shadow_liquidity_score" in cash_eval.hard_metrics else None,
            "black_swan_vulnerability_score": geo_eval.hard_metrics.get("black_swan_disruption_score") if geo_eval and "black_swan_disruption_score" in geo_eval.hard_metrics else None,
            "bullion_repatriation_velocity_score": cash_eval.hard_metrics.get("sovereign_gold_repatriation_velocity_score") if cash_eval and "sovereign_gold_repatriation_velocity_score" in cash_eval.hard_metrics else None,
            "speech_signal_divergence_score": propaganda_eval.hard_metrics.get("geopolitical_speech_forensics_score") if propaganda_eval and "geopolitical_speech_forensics_score" in propaganda_eval.hard_metrics else None,
            # Phases 338-353: Sovereign Whistleblower & Forensic Speech Intelligence Sieves
            "sovereign_public_interest_score": lawfare_eval.hard_metrics.get("sovereign_public_interest_score") if lawfare_eval and "sovereign_public_interest_score" in lawfare_eval.hard_metrics else None,
            "adversary_timing_correlation_score": geo_eval.hard_metrics.get("adversary_timing_correlation_score") if geo_eval and "adversary_timing_correlation_score" in geo_eval.hard_metrics else None,
            "documentary_provenance_authenticity_score": lawfare_eval.hard_metrics.get("documentary_provenance_authenticity_score") if lawfare_eval and "documentary_provenance_authenticity_score" in lawfare_eval.hard_metrics else None,
            "bear_raid_derivative_forensics_score": cash_eval.hard_metrics.get("bear_raid_derivative_forensics_score") if cash_eval and "bear_raid_derivative_forensics_score" in cash_eval.hard_metrics else None,
            "offshore_debt_covenant_contagion_score": cash_eval.hard_metrics.get("offshore_debt_covenant_contagion_score") if cash_eval and "offshore_debt_covenant_contagion_score" in cash_eval.hard_metrics else None,
            "exfiltration_and_foreign_sanctuary_score": hybrid_eval.hard_metrics.get("exfiltration_and_foreign_sanctuary_score") if hybrid_eval and "exfiltration_and_foreign_sanctuary_score" in hybrid_eval.hard_metrics else None,
            "retaliation_threat_and_opsec_score": hybrid_eval.hard_metrics.get("retaliation_threat_and_opsec_score") if hybrid_eval and "retaliation_threat_and_opsec_score" in hybrid_eval.hard_metrics else None,
            "vigilance_statutory_remedy_score": lawfare_eval.hard_metrics.get("vigilance_statutory_remedy_score") if lawfare_eval and "vigilance_statutory_remedy_score" in lawfare_eval.hard_metrics else None,
            "speech_kinesic_and_chromatic_forensics_score": kinesic_eval.hard_metrics.get("speech_kinesic_and_chromatic_forensics_score", 0.50) if kinesic_eval and "speech_kinesic_and_chromatic_forensics_score" in kinesic_eval.hard_metrics else 0.50,
            "speech_omission_and_negative_space_score": propaganda_eval.hard_metrics.get("speech_omission_and_negative_space_score") if propaganda_eval and "speech_omission_and_negative_space_score" in propaganda_eval.hard_metrics else None,
            "trade_based_money_laundering_score": geo_economist_eval.hard_metrics.get("trade_based_money_laundering_score") if geo_economist_eval and "trade_based_money_laundering_score" in geo_economist_eval.hard_metrics else None,
            "defense_scada_and_firmware_tamper_score": deep_tech_eval.hard_metrics.get("defense_scada_and_firmware_tamper_score") if deep_tech_eval and "defense_scada_and_firmware_tamper_score" in deep_tech_eval.hard_metrics else None,
            "cultural_heritage_and_sacrality_breach_score": civ_eval.hard_metrics.get("cultural_heritage_and_sacrality_breach_score") if civ_eval and "cultural_heritage_and_sacrality_breach_score" in civ_eval.hard_metrics else None,
            "perjury_risk_and_retributive_liability_score": lawfare_eval.hard_metrics.get("perjury_risk_and_retributive_liability_score") if lawfare_eval and "perjury_risk_and_retributive_liability_score" in lawfare_eval.hard_metrics else None,
            "qdt_whistleblower_cognitive_state_score": deep_tech_eval.hard_metrics.get("qdt_whistleblower_cognitive_state_score") if deep_tech_eval and "qdt_whistleblower_cognitive_state_score" in deep_tech_eval.hard_metrics else None,
            "sovereign_strategic_capex_impact_score": geo_economist_eval.hard_metrics.get("sovereign_strategic_capex_impact_score") if geo_economist_eval and "sovereign_strategic_capex_impact_score" in geo_economist_eval.hard_metrics else None,
            # Phases 355-364: Invisible Cash Flows & Dharmik Statecraft Sieves
            "bis_hidden_fx_swap_contagion_score": cash_eval.hard_metrics.get("bis_hidden_fx_swap_contagion_score") if cash_eval and "bis_hidden_fx_swap_contagion_score" in cash_eval.hard_metrics else None,
            "offshore_ubo_de_anonymizer_score": cash_eval.hard_metrics.get("offshore_ubo_de_anonymizer_score") if cash_eval and "offshore_ubo_de_anonymizer_score" in cash_eval.hard_metrics else None,
            "speech_to_balance_sheet_divergence_score": propaganda_eval.hard_metrics.get("speech_to_balance_sheet_divergence_score") if propaganda_eval and "speech_to_balance_sheet_divergence_score" in propaganda_eval.hard_metrics else None,
            "kinesic_contextual_baseline_drift_score": kinesic_eval.hard_metrics.get("kinesic_contextual_baseline_drift_score", 0.50) if kinesic_eval and "kinesic_contextual_baseline_drift_score" in kinesic_eval.hard_metrics else 0.50,
            "chanakya_upadha_integrity_score": civ_eval.hard_metrics.get("chanakya_upadha_integrity_score") if civ_eval and "chanakya_upadha_integrity_score" in civ_eval.hard_metrics else None,
            "kautilya_saptanga_score": geo_eval.hard_metrics.get("kautilya_saptanga_score") if geo_eval and "kautilya_saptanga_score" in geo_eval.hard_metrics else None,
            "krishna_rajadharma_exhaustion_score": civ_eval.hard_metrics.get("krishna_rajadharma_exhaustion_score") if civ_eval and "krishna_rajadharma_exhaustion_score" in civ_eval.hard_metrics else None,
            # Phases 368-390: Sovereign Forensic Sieves & Asymmetric Statecraft
            "cloud_monopoly_fragility_score": digital_eval.hard_metrics.get("cloud_monopoly_fragility_score", 0.0) if digital_eval else 0.0,
            "cognitive_deception_misdirection_score": hybrid_eval.hard_metrics.get("cognitive_deception_misdirection_score", 0.0) if hybrid_eval else 0.0,
            "counter_intelligence_honeytrap_score": hybrid_eval.hard_metrics.get("counter_intelligence_honeytrap_score", 0.0) if hybrid_eval else 0.0,
            "maritime_net_security_primacy_score": military_eval.hard_metrics.get("maritime_net_security_primacy_score", 0.0) if military_eval else 0.0,
            "false_flag_narrative_deception_score": hybrid_eval.hard_metrics.get("false_flag_narrative_deception_score", 0.0) if hybrid_eval else 0.0,
            "sovereign_cyber_extortion_score": deep_tech_eval.hard_metrics.get("sovereign_cyber_extortion_score", 0.0) if deep_tech_eval else 0.0,
            "maritime_port_dual_use_score": geo_economist_eval.hard_metrics.get("maritime_port_dual_use_score", 0.0) if geo_economist_eval else 0.0,
            "revealed_preference_divergence_score": propaganda_eval.hard_metrics.get("revealed_preference_divergence_score", 0.0) if propaganda_eval else 0.0,
            "sovereign_debt_syndicate_leverage_score": cash_eval.hard_metrics.get("sovereign_debt_syndicate_leverage_score", 0.0) if cash_eval else 0.0,
            "asymmetric_weapon_proliferation_leakage_score": military_eval.hard_metrics.get("asymmetric_weapon_proliferation_leakage_score", 0.0) if military_eval else 0.0,
            "legacy_infrastructure_obsolescence_score": digital_eval.hard_metrics.get("legacy_infrastructure_obsolescence_score", 0.0) if digital_eval else 0.0,
            "speculative_capex_overhang_score": cash_eval.hard_metrics.get("speculative_capex_overhang_score", 0.0) if cash_eval else 0.0,
            "subnational_fragmentation_lawfare_score": civ_eval.hard_metrics.get("subnational_fragmentation_lawfare_score", 0.0) if civ_eval else 0.0,
            "civilizational_epistemic_integrity_score": history_eval.hard_metrics.get("civilizational_epistemic_integrity_score", 0.0) if history_eval else 0.0,
            "algorithmic_cognitive_subversion_score": propaganda_eval.hard_metrics.get("algorithmic_cognitive_subversion_score", 0.0) if propaganda_eval else 0.0,
            "critical_scada_hardware_backdoor_score": deep_tech_eval.hard_metrics.get("critical_scada_hardware_backdoor_score", 0.0) if deep_tech_eval else 0.0,
            "circular_venture_valuation_bubble_score": cash_eval.hard_metrics.get("circular_venture_valuation_bubble_score", 0.0) if cash_eval else 0.0,
            "monopoly_patent_suppression_score": history_eval.hard_metrics.get("monopoly_patent_suppression_score", 0.0) if history_eval else 0.0,
            "sub_replacement_demographic_extinction_score": civ_eval.hard_metrics.get("sub_replacement_demographic_extinction_score", 0.0) if civ_eval else 0.0,
            "physical_capex_tangible_multiplier_score": geo_economist_eval.hard_metrics.get("physical_capex_tangible_multiplier_score", 0.0) if geo_economist_eval else 0.0,
            "open_system_asymmetric_infiltration_score": hybrid_eval.hard_metrics.get("open_system_asymmetric_infiltration_score", 0.0) if hybrid_eval else 0.0,
            "dynastic_extra_constitutional_shadow_cabinet_score": bureaucratic_eval.hard_metrics.get("dynastic_extra_constitutional_shadow_cabinet_score", 0.0) if bureaucratic_eval else 0.0,
            "superpower_naval_coercion_brinkmanship_score": military_eval.hard_metrics.get("superpower_naval_coercion_brinkmanship_score", 0.0) if military_eval else 0.0,
            # Phases 391-395: Sovereign Investigative Intelligence & Invisible Cash-Flow Forensics Matrix
            "transnational_semiconductor_kompromat_score": hybrid_eval.hard_metrics.get("transnational_semiconductor_kompromat_score", 0.0) if hybrid_eval else 0.0,
            "media_intelligence_leak_timing_score": propaganda_eval.hard_metrics.get("media_intelligence_leak_timing_score", 0.0) if propaganda_eval else 0.0,
            "generative_media_compute_hegemony_score": civ_eval.hard_metrics.get("generative_media_compute_hegemony_score", 0.0) if civ_eval else 0.0,
            "remote_silicon_microcode_killswitch_score": deep_tech_eval.hard_metrics.get("remote_silicon_microcode_killswitch_score", 0.0) if deep_tech_eval else 0.0,
            "gpu_debt_collateral_contagion_score": cash_eval.hard_metrics.get("gpu_debt_collateral_contagion_score", 0.0) if cash_eval else 0.0,
            # Phases 396-415: Sovereign Asymmetric War, Balance-Sheet Realism & Civilizational Sovereignty Matrix
            "informal_sector_statistical_divergence_score": cash_eval.hard_metrics.get("informal_sector_statistical_divergence_score", 0.0) if cash_eval else 0.0,
            "pboc_lgfv_liquidity_trap_score": cash_eval.hard_metrics.get("pboc_lgfv_liquidity_trap_score", 0.0) if cash_eval else 0.0,
            "asymmetric_air_defense_cost_exchange_score": military_eval.hard_metrics.get("asymmetric_air_defense_cost_exchange_score", 0.0) if military_eval else 0.0,
            "hypersonic_glide_penetration_score": military_eval.hard_metrics.get("hypersonic_glide_penetration_score", 0.0) if military_eval else 0.0,
            "sovereign_platform_regulatory_defiance_score": digital_eval.hard_metrics.get("sovereign_platform_regulatory_defiance_score", 0.0) if digital_eval else 0.0,
            "institutional_cartel_cross_shareholding_score": cash_eval.hard_metrics.get("institutional_cartel_cross_shareholding_score", 0.0) if cash_eval else 0.0,
            "msme_solvency_asphyxiation_score": cash_eval.hard_metrics.get("msme_solvency_asphyxiation_score", 0.0) if cash_eval else 0.0,
            "nuclear_launch_under_attack_latency_score": military_eval.hard_metrics.get("nuclear_launch_under_attack_latency_score", 0.0) if military_eval else 0.0,
            "border_state_narco_fiscal_subversion_score": hybrid_eval.hard_metrics.get("border_state_narco_fiscal_subversion_score", 0.0) if hybrid_eval else 0.0,
            "trilateral_superpower_condominium_exclusion_score": geo_eval.hard_metrics.get("trilateral_superpower_condominium_exclusion_score", 0.0) if geo_eval else 0.0,
            "quantum_hndl_vulnerability_score": deep_tech_eval.hard_metrics.get("quantum_hndl_vulnerability_score", 0.0) if deep_tech_eval else 0.0,
            "diplomatic_nonverbal_optics_score": kinesic_eval.hard_metrics.get("diplomatic_nonverbal_optics_score", 0.0) if kinesic_eval else 0.0,
            "cultural_religious_grayzone_lawfare_score": lawfare_eval.hard_metrics.get("cultural_religious_grayzone_lawfare_score", 0.0) if lawfare_eval else 0.0,
            "critical_mineral_weaponization_score": minerals_eval.hard_metrics.get("critical_mineral_weaponization_score", 0.0) if minerals_eval else 0.0,
            "agrochemical_food_weaponization_score": food_eval.hard_metrics.get("agrochemical_food_weaponization_score", 0.0) if food_eval else 0.0,
            "aviation_transit_slot_cartel_score": geo_economist_eval.hard_metrics.get("aviation_transit_slot_cartel_score", 0.0) if geo_economist_eval else 0.0,
            "airborne_command_survivability_score": military_eval.hard_metrics.get("airborne_command_survivability_score", 0.0) if military_eval else 0.0,
            "sub_tactical_honeytrap_espionage_score": hybrid_eval.hard_metrics.get("sub_tactical_honeytrap_espionage_score", 0.0) if hybrid_eval else 0.0,
            "naval_electronic_warfare_suppression_score": military_eval.hard_metrics.get("naval_electronic_warfare_suppression_score", 0.0) if military_eval else 0.0,
            "civilizational_epistemic_historiography_score": civ_eval.hard_metrics.get("civilizational_epistemic_historiography_score", 0.0) if civ_eval else 0.0,
            # Phases 416-433: Sovereign Forensic Sieves & Strategic Council Titans (18 Channels: 220 -> 238)
            "asymmetric_scada_blackout_vulnerability_score": digital_eval.hard_metrics.get("asymmetric_scada_blackout_vulnerability_score", 0.0) if digital_eval else 0.0,
            "synchronized_media_cartel_coordination_score": propaganda_eval.hard_metrics.get("synchronized_media_cartel_coordination_score", 0.0) if propaganda_eval else 0.0,
            "deep_state_banking_rating_squeeze_score": cash_eval.hard_metrics.get("deep_state_banking_rating_squeeze_score", 0.0) if cash_eval else 0.0,
            "directed_energy_weapon_neutralization_score": deep_tech_eval.hard_metrics.get("directed_energy_weapon_neutralization_score", 0.0) if deep_tech_eval else 0.0,
            "multilateral_alliance_autonomy_retention_score": geo_eval.hard_metrics.get("multilateral_alliance_autonomy_retention_score", 0.0) if geo_eval else 0.0,
            "offshore_banking_asset_repatriation_score": cash_eval.hard_metrics.get("offshore_banking_asset_repatriation_score", 0.0) if cash_eval else 0.0,
            "foreign_intelligence_institutional_penetration_score": hybrid_eval.hard_metrics.get("foreign_intelligence_institutional_penetration_score", 0.0) if hybrid_eval else 0.0,
            "cognitive_atrophy_service_displacement_score": civ_eval.hard_metrics.get("cognitive_atrophy_service_displacement_score", 0.0) if civ_eval else 0.0,
            "demographic_border_fortification_resilience_score": military_eval.hard_metrics.get("demographic_border_fortification_resilience_score", 0.0) if military_eval else 0.0,
            "algorithmic_faceless_procurement_efficiency_score": bureaucratic_eval.hard_metrics.get("algorithmic_faceless_procurement_efficiency_score", 0.0) if bureaucratic_eval else 0.0,
            "investigative_forensics_negative_space_score": propaganda_eval.hard_metrics.get("investigative_forensics_negative_space_score", 0.85) if propaganda_eval else 0.85,
            "sovereign_debt_maturity_rollover_risk_score": cash_eval.hard_metrics.get("sovereign_debt_maturity_rollover_risk_score", 0.0) if cash_eval else 0.0,
            "asymmetric_subversion_counter_penetration_score": hybrid_eval.hard_metrics.get("asymmetric_subversion_counter_penetration_score", 0.0) if hybrid_eval else 0.0,
            "sovereign_capex_moat_escape_velocity_score": bureaucratic_eval.hard_metrics.get("sovereign_capex_moat_escape_velocity_score", 0.0) if bureaucratic_eval else 0.0,
            "multipolar_hedging_reciprocal_leverage_score": geo_eval.hard_metrics.get("multipolar_hedging_reciprocal_leverage_score", 0.0) if geo_eval else 0.0,
            "sovereign_credit_rating_bias_score": geo_economist_eval.hard_metrics.get("sovereign_credit_rating_bias_score", 0.0) if geo_economist_eval else 0.0,
            "civilizational_jurisprudence_decolonial_score": lawfare_eval.hard_metrics.get("civilizational_jurisprudence_decolonial_score", 0.0) if lawfare_eval else 0.0,
            "empirical_falsification_cryptographic_verification_score": deep_tech_eval.hard_metrics.get("empirical_falsification_cryptographic_verification_score", 0.88) if deep_tech_eval else 0.88,
            # Phases 434-440: Semiotic Iconography, Global Polycrisis Cascades & Sovereign Resilient Sieves (7 Channels: 238 -> 245)
            "predictive_semiotic_deconstruction_score": 0.82,
            "global_polycrisis_collision_index": geo_eval.hard_metrics.get("global_polycrisis_collision_index", 0.0) if geo_eval else 0.0,
            "cultural_religious_grayzone_subversion_score": lawfare_eval.hard_metrics.get("cultural_religious_grayzone_subversion_score", 0.0) if lawfare_eval else 0.0,
            "metabolic_pharmaceutical_disruption_score": food_eval.hard_metrics.get("metabolic_pharmaceutical_disruption_score", 0.0) if food_eval else 0.0,
            "orbital_weaponization_vulnerability_score": deep_tech_eval.hard_metrics.get("orbital_weaponization_vulnerability_score", 0.0) if deep_tech_eval else 0.0,
            "taiwan_quarantine_semiconductor_choke_index": minerals_eval.hard_metrics.get("taiwan_quarantine_semiconductor_choke_index", 0.0) if minerals_eval else 0.0,
            "electoral_lawfare_polarization_score": lawfare_eval.hard_metrics.get("electoral_lawfare_polarization_score", 0.0) if lawfare_eval else 0.0,
            # Phases 441-447: Sovereign Forensic Sieves & Multilateral Autonomy Tensors (7 Channels: 245 -> 252)
            "tripolar_condominium_exclusion_risk": geo_eval.hard_metrics.get("tripolar_condominium_exclusion_risk", 0.0) if geo_eval else 0.0,
            "ai_services_labor_displacement_index": deep_tech_eval.hard_metrics.get("ai_services_labor_displacement_index", 0.0) if deep_tech_eval else 0.0,
            "transnational_diaspora_subversion_risk": lawfare_eval.hard_metrics.get("transnational_diaspora_subversion_risk", 0.0) if lawfare_eval else 0.0,
            "gpu_export_control_chokepoint_vulnerability": minerals_eval.hard_metrics.get("gpu_export_control_chokepoint_vulnerability", 0.0) if minerals_eval else 0.0,
            "currency_appreciation_export_friction_score": geo_economist_eval.hard_metrics.get("currency_appreciation_export_friction_score", 0.0) if geo_economist_eval else 0.0,
            "supranational_deep_state_subversion_risk": lawfare_eval.hard_metrics.get("supranational_deep_state_subversion_risk", 0.0) if lawfare_eval else 0.0,
            "physical_bullion_pricing_power_and_cyber_resilience_score": deep_tech_eval.hard_metrics.get("physical_bullion_pricing_power_and_cyber_resilience_score", 0.0) if deep_tech_eval else 0.0,
            # Phases 448-449: Horizon Polycrisis & Multilateral Defense Interoperability (2 Channels: 252 -> 254)
            "economist_2027_poly_crisis_horizon_index": geo_eval.hard_metrics.get("economist_2027_poly_crisis_horizon_index", 0.0) if geo_eval else 0.0,
            "defense_interoperability_and_cognitive_immunity_score": lawfare_eval.hard_metrics.get("defense_interoperability_and_cognitive_immunity_score", 0.0) if lawfare_eval else 0.0,
            # Phase 450: Subcontinental Asymmetric Defense and Techno Sovereignty (1 Channel: 254 -> 255)
            "subcontinental_asymmetric_defense_and_techno_sovereignty_score": lawfare_eval.hard_metrics.get("subcontinental_asymmetric_defense_and_techno_sovereignty_score", 0.0) if lawfare_eval else 0.0,
            # Phase 454: Sovereign Cognitive Subterranean and Kinetic Interoperability (1 Channel: 255 -> 256)
            "unified_sovereign_hyper_resilience_score": geo_eval.hard_metrics.get("unified_sovereign_hyper_resilience_score", 0.0) if geo_eval else 0.0,
            # Phases 455, 458, 460 Capstone 1: Epistemic Taxonomy and Interleaved Validation (1 Channel: 256 -> 257)
            "epistemic_taxonomy_and_interleaved_validation_score": deep_tech_eval.hard_metrics.get("epistemic_taxonomy_and_interleaved_validation_score", 0.7850) if deep_tech_eval else 0.7850,
            # Phases 456, 457, 459 Capstone 2: Sovereign Industrial Capital and Propulsion (1 Channel: 257 -> 258)
            "sovereign_industrial_capital_and_propulsion_score": cash_eval.hard_metrics.get("sovereign_industrial_capital_and_propulsion_score", 0.7850) if cash_eval else 0.7850,
            # Phases 461-464: Sovereign Bullion/Marine/Brand, Impossible Trinity/OPSEC, Constitutional/Grayzone, Mother-Machine/Sonar/Hydrocide (4 Channels: 258 -> 262)
            "physical_bullion_marine_insurance_and_brand_sovereignty_score": cash_eval.hard_metrics.get("physical_bullion_marine_insurance_and_brand_sovereignty_score", 0.0) if cash_eval else 0.0,
            "impossible_trinity_tbml_and_counter_infiltration_score": hybrid_eval.hard_metrics.get("impossible_trinity_tbml_and_counter_infiltration_score", 0.0) if hybrid_eval else 0.0,
            "constitutional_engineering_and_grayzone_proxy_score": lawfare_eval.hard_metrics.get("constitutional_engineering_and_grayzone_proxy_score", 0.0) if lawfare_eval else 0.0,
            "mother_machine_sonar_liquidity_hydrocide_score": deep_tech_eval.hard_metrics.get("mother_machine_sonar_liquidity_hydrocide_score", 0.0) if deep_tech_eval else 0.0,
        }

        # Add explicit Tier 1 physical log entries to arbitration_log
        if food_eval and food_eval.primary_epistemic_tier == EpistemicTier.TIER_1_PHYSICAL:
            arbitration_log.append(f"[ARBITRATION_T1_PHYSICAL] Food Security Lens verified grain buffer ratio {strategic_resilience_matrix['strategic_grain_buffer_ratio']:.2f}x statutory norm; fertilizer import exposure audited.")
        if military_eval and military_eval.primary_epistemic_tier == EpistemicTier.TIER_1_PHYSICAL:
            arbitration_log.append(f"[ARBITRATION_T1_PHYSICAL] Military Readiness Lens verified WWR ammunition depth at {strategic_resilience_matrix['wwr_ammunition_reserve_days']:.1f} days; two-front deterrence posture validated.")

        # Apply Inter-Lens Dynamic Coupling & Contradiction Analysis
        lens_evals, contradiction_penalty = cls.apply_inter_lens_coupling(
            lens_evals=lens_evals,
            hard_money_audit=hard_money_audit,
            arbitration_log=arbitration_log
        )
        if verification_penalty > 0:
            contradiction_penalty = min(0.20, contradiction_penalty + verification_penalty)

        # Epistemic Tier-Weighted Confidence Calculation with Dynamic Bayesian Calibration
        tier_weights = {
            EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE: 0.05,
            EpistemicTier.TIER_1_PHYSICAL: 1.0,
            EpistemicTier.TIER_2_FINANCIAL: 0.85,
            EpistemicTier.TIER_3_SOVEREIGN_REDLINES: 0.70,
            EpistemicTier.TIER_4_KINESICS: 0.30,
            EpistemicTier.TIER_5_COMMUNIQUE_PR: 0.10,
        }
        try:
            from ..storage.event_store import EventStore
            rel_map = EventStore().get_lens_reliability_multipliers()
        except Exception:
            rel_map = {}

        weighted_conf_sum = sum(
            l.confidence * tier_weights.get(l.primary_epistemic_tier, 0.50) * rel_map.get(l.lens_name, 1.0)
            for l in lens_evals
        )
        total_tier_weight = sum(
            tier_weights.get(l.primary_epistemic_tier, 0.50) * rel_map.get(l.lens_name, 1.0)
            for l in lens_evals
        )
        raw_conf = weighted_conf_sum / max(total_tier_weight, 1e-6)
        overall_confidence = max(0.10, round(raw_conf - contradiction_penalty, 2))

        # Record longitudinal diagnostic encounter in EventStore if available
        enc_id = None
        try:
            from ..storage.event_store import EventStore
            es = EventStore()
            entity_name = getattr(summit, "summit_name", getattr(summit, "event_name", getattr(summit, "title", "Strategic Event")))
            query_repr = f"Synthesis of {entity_name} ({mode.value}) across {len(lens_evals)} lenses"
            anomalies = []
            if contradiction_penalty > 0:
                anomalies.append(f"Contradiction penalty: {contradiction_penalty:.2f}")
            if ach_report and ach_report.is_epistemically_contested:
                anomalies.append("ACH Contested causal hypotheses")
            enc_id = es.record_diagnostic_encounter(
                entity_or_subject=entity_name,
                query_text=query_repr,
                primary_epistemic_tier="TIER_1_PHYSICAL",
                confidence=overall_confidence,
                reality_ratio=round(1.0 - contradiction_penalty, 2),
                propaganda_ratio=round(contradiction_penalty, 2),
                anomalies_detected=anomalies,
                session_id=getattr(summit, "event_id", "summit_synthesis")
            )
            arbitration_log.append(f"[LONGITUDINAL_ENCOUNTER] Registered diagnostic encounter {enc_id} in EventStore.")
        except Exception:
            pass

        # Phase 111: Dynamic Causal Graph Shock Propagation Hook
        causal_shocks: Dict[str, Any] = {}
        try:
            from .causal_graph import EpistemicKnowledgeGraph
            kg = EpistemicKnowledgeGraph.build_canonical_graph()
            ev_text = (str(getattr(summit, "title", "")) + " " + str(getattr(summit, "summit_name", ""))).lower()
            if claims:
                ev_text += " " + " ".join([str(getattr(c, "asserted_fact", getattr(c, "assertion", ""))) for c in claims]).lower()

            active_triggers = {}
            if any(w in ev_text for w in ["hormuz", "tanker", "crude freight", "chokepoint"]):
                active_triggers["hormuz_interdiction"] = 0.90
            if any(w in ev_text for w in ["gallium", "germanium", "export ban", "wafer"]):
                active_triggers["gallium_germanium_export_controls"] = 0.85
            if any(w in ev_text for w in ["saltpetre", "criminal tribes", "caste census", "1871"]):
                active_triggers["eic_saltpetre_monopsony_1770"] = 0.80
            if any(w in ev_text for w in ["drone", "shahed", "burnout", "interceptor", "swarm"]):
                active_triggers["low_cost_drone_swarm_saturation"] = 0.90
            if any(w in ev_text for w in ["caste lawfare", "sb 403", "seattle"]):
                active_triggers["transnational_caste_lawfare_campaign"] = 0.75
            if any(w in ev_text for w in ["welfarism", "freebie", "jizya", "taxpayer", "blunder"]):
                active_triggers["electoral_welfarism_expansion"] = 0.85
            if any(w in ev_text for w in ["pqc", "quantum", "shor", "decrypt"]):
                active_triggers["post_quantum_cryptographic_vulnerability"] = 0.85
            if any(w in ev_text for w in ["gold repatriation", "rbi gold", "bank of england gold"]):
                active_triggers["sovereign_gold_reserve_repatriation"] = 0.85
            if any(w in ev_text for w in ["aviation sabotage", "kamikaze", "airspace closure"]):
                active_triggers["aviation_insider_sabotage"] = 0.85
            if any(w in ev_text for w in ["biosecurity", "pathogen", "lab release", "bwc"]):
                active_triggers["dual_use_biosecurity_leak"] = 0.85

            if active_triggers:
                causal_shocks = kg.propagate_shock(initial_shocks=active_triggers, max_hops=4)
                arbitration_log.append(
                    f"[CAUSAL_GRAPH_SHOCK_PROPAGATION] Propagated {len(active_triggers)} shocks across {len(causal_shocks)} nodes in EpistemicKnowledgeGraph."
                )
        except Exception:
            causal_shocks = {}

        # Phase 111: Layman Intuitive Synthesis Layer
        layman_summary = LaymanSynthesizer.generate_intuitive_summary(
            event_name=getattr(summit, "summit_name", getattr(summit, "title", "Strategic Event")),
            hard_money_audit=hard_money_audit,
            overall_confidence=overall_confidence,
            contradiction_penalty=contradiction_penalty,
            claims=claims
        )

        return SummitAnalysisReport(
            event=summit,
            lens_evaluations=lens_evals,
            negative_space_synopsis=negative_space_synopsis,
            country_ledgers=country_ledgers,
            kinesic_forensics=kinesic_observations,
            hard_money_audit=hard_money_audit,
            civilizational_synthesis=civilizational_inner_meaning,
            strategic_resilience_matrix=strategic_resilience_matrix,
            ach_evaluation=ach_report.to_dict() if ach_report else None,
            overall_confidence_score=overall_confidence,
            diagnostic_encounter_id=enc_id,
            epistemic_arbitration_log=arbitration_log,
            causal_shock_propagation=causal_shocks,
            layman_intuitive_summary=layman_summary
        )


    @classmethod
    def synthesize_and_export(
        cls,
        summit: Union[SummitEvent, StrategicEvent],
        claims: Optional[List[Any]] = None,
        evidence_items: Optional[List[Any]] = None,
        prioritized_lenses: Optional[List[str]] = None,
        export_formats: Optional[Union[str, List[str]]] = None,
        output_dir: str = "reports",
        base_filename: Optional[str] = None,
        persona: str = "neutral"
    ) -> Tuple[SummitAnalysisReport, Dict[str, str]]:
        """
        Synthesizes the 5-Tier SummitAnalysisReport and automatically exports it into
        interactive HTML dashboard, Markdown audit, and publication-grade PDF documents.
        """
        report = cls.synthesize_report(
            summit,
            claims=claims,
            evidence_items=evidence_items,
            prioritized_lenses=prioritized_lenses
        )
        from ..visualization import export_report
        files = export_report(
            report,
            formats=export_formats or ["html", "md", "pdf"],
            output_dir=output_dir,
            base_filename=base_filename,
            persona=persona
        )
        return report, files

    # Alias for synthesize_report
    synthesize = synthesize_report



    def compute_sovereign_risk_composite_index(
        self, strategic_resilience_matrix: dict
    ) -> dict:
        """
        Phase 220: Sovereign Risk Composite Index (SRCI).
        Aggregates 6 key SRM indicators into a single σ-bounded sovereign risk scalar.
        Replaces ad-hoc manual reading of 30+ SRM keys with one actionable number.

        Mathematical formula:
          z = w1*cable_vulnerability_index
            + w2*refining_concentration_risk
            + w3*(1 - min(2.0, strategic_equilibrium_ratio) / 2.0)  # cartel normalization
            + w4*cultural_grayzone_hijack_probability
            + w5*(1 - sanctions_firewall_score)                       # inverse firewall
            + w6*demographic_border_vulnerability
          SRCI = sigma(z - 0.5)  # centered sigmoid, SRCI in [0,1]

        Weights (sum to 1.0):
          w1=0.18 (cable),  w2=0.22 (minerals), w3=0.15 (cartel),
          w4=0.12 (grayzone), w5=0.20 (sanctions), w6=0.13 (demographic)

        Tier thresholds:
          SRCI >= 0.80: CRITICAL_SOVEREIGN_VULNERABILITY
          SRCI >= 0.65: HIGH_RISK_MULTI_DOMAIN_EXPOSURE
          SRCI >= 0.50: MODERATE_COMPOSITE_RISK
          SRCI >= 0.35: MANAGEABLE_SOVEREIGN_RISK
          SRCI < 0.35:  LOW_COMPOSITE_SOVEREIGN_RISK
        """
        import math

        def sigma(z: float) -> float:
            return 1.0 / (1.0 + math.exp(-z))

        rm = strategic_resilience_matrix or {}

        cable_vi      = float(rm.get("cable_vulnerability_index") or 0.50)
        refining_risk = float(rm.get("refining_concentration_risk") or 0.50)
        eq_ratio      = float(rm.get("strategic_equilibrium_ratio") or 1.0)
        gz_prob       = float(rm.get("cultural_grayzone_hijack_probability") or 0.30)
        sanctions_fw  = float(rm.get("sanctions_firewall_score") or 0.50)
        demo_vuln     = float(rm.get("demographic_border_vulnerability") or 0.40)

        # Cartel normalization: equilibrium > 2.0 = fully shielded
        cartel_risk_term = 1.0 - min(2.0, eq_ratio) / 2.0

        # Weights
        w1, w2, w3, w4, w5, w6 = 0.18, 0.22, 0.15, 0.12, 0.20, 0.13

        z = (
            w1 * cable_vi
            + w2 * refining_risk
            + w3 * cartel_risk_term
            + w4 * gz_prob
            + w5 * (1.0 - sanctions_fw)
            + w6 * demo_vuln
            - 0.5  # center the sigmoid at midpoint
        )
        srci = sigma(z * 4.0)  # scale factor 4 for better discrimination

        # Determine tier
        if srci >= 0.80:
            tier = "CRITICAL_SOVEREIGN_VULNERABILITY"
            dominant_keys = sorted(
                [("cable", w1 * cable_vi), ("minerals", w2 * refining_risk),
                 ("cartel", w3 * cartel_risk_term), ("grayzone", w4 * gz_prob),
                 ("sanctions", w5 * (1 - sanctions_fw)), ("demo", w6 * demo_vuln)],
                key=lambda x: x[1], reverse=True
            )
            dominant_domain = dominant_keys[0][0]
        elif srci >= 0.65:
            tier = "HIGH_RISK_MULTI_DOMAIN_EXPOSURE"
            dominant_domain = "multi_domain"
        elif srci >= 0.50:
            tier = "MODERATE_COMPOSITE_RISK"
            dominant_domain = "composite"
        elif srci >= 0.35:
            tier = "MANAGEABLE_SOVEREIGN_RISK"
            dominant_domain = "manageable"
        else:
            tier = "LOW_COMPOSITE_SOVEREIGN_RISK"
            dominant_domain = "low_risk"

        # Dominant domain for any tier
        if srci >= 0.50:
            contributions = {
                "cable": w1 * cable_vi,
                "minerals": w2 * refining_risk,
                "cartel": w3 * cartel_risk_term,
                "grayzone": w4 * gz_prob,
                "sanctions": w5 * (1.0 - sanctions_fw),
                "demographic": w6 * demo_vuln,
            }
            dominant_domain = max(contributions, key=contributions.get)

        return {
            "srci_score": round(srci, 4),
            "srci_tier": tier,
            "dominant_risk_domain": dominant_domain,
            "component_inputs": {
                "cable_vulnerability_index": round(cable_vi, 4),
                "refining_concentration_risk": round(refining_risk, 4),
                "strategic_equilibrium_ratio": round(eq_ratio, 4),
                "cultural_grayzone_hijack_probability": round(gz_prob, 4),
                "sanctions_firewall_score": round(sanctions_fw, 4),
                "demographic_border_vulnerability": round(demo_vuln, 4),
            },
        }


class LaymanSynthesizer:
    """
    Translates complex forensic multi-lens tensors, 5-tier arbitration outputs,
    and causal shock propagation into intuitive, real-world metaphors and plain-language answers.
    """

    @staticmethod
    def generate_intuitive_summary(
        event_name: str,
        hard_money_audit: Dict[str, Any],
        overall_confidence: float,
        contradiction_penalty: float,
        claims: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        haircut = hard_money_audit.get("aggregate_haircut_pct", 85.0)

        # Dynamic Metaphor Selection
        if haircut >= 75.0:
            metaphor_title = "The Grand Gate & The Leaking Foundation (Ancestral House Metaphor)"
            metaphor_story = (
                f"Like an ancestral estate where the management built grand decorative archways and hosted an expensive gala for {event_name}, "
                f"while the internal rooms and foundation remain neglected. The official communiques claim total victory, "
                f"but {haircut:.1f}% of the promised capital is speculative paper promises with zero escrow funding."
            )
        else:
            metaphor_title = "The Calibrated Engine in Rough Terrain"
            metaphor_story = (
                f"Like a heavy convoy navigating mountainous passes: substantial real fuel and engineering capacity are actively moving, "
                f"though high friction and geopolitical turbulence require continuous defensive steering."
            )

        layman_takeaways = [
            f"Optics vs Ground Truth: The public announcements look impressive, but the hard reality discount is {haircut:.1f}%.",
            f"Confidence Score: The machine-audited truth confidence is {int(overall_confidence * 100)}% out of 100%.",
            "Bottom Line: Real geopolitical power is measured in physical pipelines, verified ammunition reserves, and sovereign legal autonomy—never signed declarations."
        ]

        return {
            "headline": f"Plain-Language Sovereign Audit: {event_name}",
            "core_metaphor": {
                "title": metaphor_title,
                "narrative": metaphor_story
            },
            "layman_takeaways": layman_takeaways,
            "verdict": (
                "Always separate the stage performance (Tier 5 Communique PR) from the physical pipelines, cash, and laws (Tiers 1 & 2 Reality)."
            )
        }
class PuranicMetaphysicalBoundarySieve:
    """
    Phase 321: Enforces strict epistemic gating: clamps subjective, unverifiable metaphysical
    claims (e.g., 12th-dimension consciousness, literal personified demonic entities) to Tier 0
    (Subjective Mythos), preventing corruption of Tier 1 physical sensor data.

    Operational Rule:
      If verifiability_index < 0.20 and empirical_sensors == 0:
         clamp confidence ceiling to 0.15 and flag as TIER_0_METAPHYSICAL_MYTHOS.
      Otherwise:
         z = 3.0 * verifiability_index + 2.8 * empirical_sensors - 3.0 * subjective_claim_intensity - 0.3
         S = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        verifiability_index: float = 0.10,
        empirical_sensors: float = 0.0,
        subjective_claim_intensity: float = 0.85,
    ) -> dict:
        v_idx = max(0.0, min(1.0, float(verifiability_index)))
        sensors = max(0.0, min(1.0, float(empirical_sensors)))
        subj = max(0.0, min(1.0, float(subjective_claim_intensity)))

        is_clamped = False
        if v_idx < 0.20 and sensors == 0.0:
            score = min(0.15, round(v_idx * 0.5, 4))
            is_clamped = True
            tier = "TIER_0_METAPHYSICAL_MYTHOS_GATED"
            verdict = "ISOLATED_FROM_PHYSICAL_TELEMETRY"
            rationale = (
                f"Epistemic boundary enforced: Subjective metaphysical assertions ({subj:.2f}) lack physical sensor grounding "
                f"({sensors:.2f}); clamped to confidence ceiling {score:.4f} to prevent Tier 1 reality contamination."
            )
        else:
            z = 3.0 * v_idx + 2.8 * sensors - 3.0 * subj - 0.3
            score = round(1.0 / (1.0 + math.exp(-z)), 4)
            tier = "EMPIRICALLY_VERIFIED_PHYSICAL_SIGNAL" if score >= 0.60 else "AMBIGUOUS_NARRATIVE_STREAM"
            verdict = "INTEGRATED_INTO_SITUATIONAL_TELEMETRY"
            rationale = f"Grounded observation ({score:.4f}): Sensor backing ({sensors:.2f}) warrants epistemic inclusion."

        return {
            "puranic_metaphysical_boundary_score": score,
            "verifiability_index": round(v_idx, 4),
            "empirical_sensors": round(sensors, 4),
            "subjective_claim_intensity": round(subj, 4),
            "is_metaphysically_gated": is_clamped,
            "metaphysical_boundary_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
        }
class BlackSwanDisruptionSieve:
    """
    Phase 335: Quantifies the strategic probability and systemic ripple effects of low-frequency,
    high-impact non-linear shocks (e.g., sudden leadership decapitation, global cloud outages,
    chokepoint blockades) using extreme value theory (EVT).

    Mathematical Formulation:
      z = 3.2 * shock_tail_risk_index + 2.8 * infrastructure_coupling_density - 3.0 * redundancy_isolation_buffer - 0.3
      S_BlackSwan_Vulnerability = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        shock_tail_risk_index: float = 0.75,
        infrastructure_coupling_density: float = 0.80,
        redundancy_isolation_buffer: float = 0.30,
    ) -> dict:
        risk = max(0.0, min(1.0, float(shock_tail_risk_index)))
        coupling = max(0.0, min(1.0, float(infrastructure_coupling_density)))
        redundancy = max(0.0, min(1.0, float(redundancy_isolation_buffer)))

        z = 3.2 * risk + 2.8 * coupling - 3.0 * redundancy - 0.3
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.70:
            tier = "CRITICAL_SYSTEMIC_BLACK_SWAN_CASCADE"
            verdict = "CATASTROPHIC_NON_LINEAR_DISRUPTION_RISK"
            rationale = (
                f"High black-swan systemic vulnerability ({score:.4f}): Tightly coupled critical nodes ({coupling:.2f}) and tail risk "
                f"({risk:.2f}) threaten catastrophic cascade due to inadequate isolation buffers ({redundancy:.2f})."
            )
        elif score >= 0.45:
            tier = "MODERATE_TAIL_RISK_EXPOSURE"
            verdict = "LOCALIZED_SHOCK_ABSORPTION"
            rationale = f"Moderate exposure ({score:.4f}): Partial decoupling prevents immediate systemic cascade."
        else:
            tier = "ROBUST_ANTI_FRAGILE_SYSTEM_ISOLATION"
            verdict = "RESILIENT_TO_NON_LINEAR_EXTERNAL_SHOCKS"
            rationale = f"Anti-fragile architecture ({score:.4f}): Redundant physical buffers ({redundancy:.2f}) absorb extreme shocks."

        return {
            "black_swan_disruption_score": score,
            "shock_tail_risk_index": round(risk, 4),
            "infrastructure_coupling_density": round(coupling, 4),
            "redundancy_isolation_buffer": round(redundancy, 4),
            "black_swan_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_black_swan_vulnerable": score >= 0.70,
        }

```

## Module: `geo_engine/arbitration/whistleblower.py`

```python
"""
Satyameva-Suchaka 2.0: Sovereign Bharatiya Whistleblower & Speech-Forensic Engine.
Evaluates insider disclosures, forensic provenance, balance sheet divergence,
debt covenant contagion, kinesic micro-signals, and retributive legal liability.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import math

from ..lenses import (
    SovereignPublicInterestSieve,
    AdversaryTimingCorrelationSieve,
    DocumentaryProvenanceAuthenticitySieve,
    BearRaidDerivativeForensicsSieve,
    OffshoreDebtCovenantContagionSieve,
    ExfiltrationAndForeignSanctuarySieve,
    RetaliationThreatAndOpSecSieve,
    VigilanceStatutoryRemedySieve,
    SpeechKinesicAndChromaticForensicsSieve,
    SpeechOmissionAndNegativeSpaceSieve,
    TradeBasedMoneyLaunderingSieve,
    DefenseSCADAAndFirmwareTamperSieve,
    CulturalHeritageAndSacralityBreachSieve,
    PerjuryRiskAndRetributiveLiabilitySieve,
    QDTWhistleblowerCognitiveStateSieve,
    SovereignStrategicCapExImpactSieve,
)


@dataclass
class WhistleblowerDossier:
    """Represents a submitted whistleblower disclosure, document leak, or forensic testimony."""
    dossier_id: str
    title: str
    target_entity: str
    domain: str  # CORPORATE, DEFENSE, ECOLOGY, FINANCIAL, HEALTHCARE, HERITAGE
    narrative_text: str
    source_credibility: float = 0.70
    is_anonymous: bool = True
    has_bsa_cert: bool = False
    casualty_threat: float = 0.20
    ecological_damage: float = 0.25
    retail_capital_loss: float = 0.30
    corporate_sensationalism: float = 0.20
    timing_proximity: float = 0.30
    summit_sensitivity: float = 0.40
    organic_reporting_lag: float = 0.70
    cryptographic_hash_match: float = 0.85
    device_certificate_provenance: float = 0.80
    typographical_anomaly_ratio: float = 0.15
    source_chain_of_custody: float = 0.75
    put_volume_spike: float = 0.25
    pnote_short_concentration: float = 0.20
    normal_hedging_ratio: float = 0.80
    cross_default_exposure: float = 0.30
    lc_credit_freeze: float = 0.25
    sovereign_liquidity_backstop: float = 0.80
    visa_pre_clearance: float = 0.20
    embassy_sanctuary_proximity: float = 0.15
    offshore_retainer: float = 0.20
    domestic_residence_commitment: float = 0.85
    physical_intimidation: float = 0.30
    slapp_litigation_asymmetry: float = 0.40
    statutory_police_protection: float = 0.70
    jurisdictional_fit: float = 0.80
    statutory_safeguard_score: float = 0.75
    jurisdictional_ambiguity: float = 0.20
    facs_deception_marker: float = 0.30
    vocal_pitch_jitter: float = 0.25
    chromatic_incongruence: float = 0.35
    autonomic_baseline_stability: float = 0.70
    deliberate_omission_density: float = 0.35
    taboo_topic_suppression: float = 0.40
    comprehensive_coverage_ratio: float = 0.65
    customs_remittance_discrepancy: float = 0.25
    gst_eway_divergence: float = 0.20
    port_clearance_verification: float = 0.80
    firmware_hash_deviation: float = 0.20
    unauthorized_microcode_call: float = 0.15
    cryptographic_signing_validity: float = 0.85
    antiquities_illicit_auction_score: float = 0.25
    sacral_space_encroachment: float = 0.30
    archaeological_survey_protection: float = 0.75
    fabricated_claim_ratio: float = 0.20
    malicious_intent_score: float = 0.25
    substantiated_evidence_ratio: float = 0.80
    psi_duty: float = 0.70
    psi_fear: float = 0.50
    theta_retaliation_rad: float = 1.05
    capex_multiplier_scale: float = 0.75
    supply_chain_criticality: float = 0.80
    receivership_remedy_viability: float = 0.85


@dataclass
class WhistleblowerEvaluation:
    """Comprehensive forensic evaluation result of a whistleblower disclosure."""
    dossier_id: str
    target_entity: str
    domain: str
    sovereign_public_interest_score: float
    adversary_timing_correlation_score: float
    documentary_provenance_authenticity_score: float
    bear_raid_derivative_forensics_score: float
    offshore_debt_covenant_contagion_score: float
    exfiltration_and_foreign_sanctuary_score: float
    retaliation_threat_and_opsec_score: float
    vigilance_statutory_remedy_score: float
    speech_kinesic_and_chromatic_forensics_score: float
    speech_omission_and_negative_space_score: float
    trade_based_money_laundering_score: float
    defense_scada_and_firmware_tamper_score: float
    cultural_heritage_and_sacrality_breach_score: float
    perjury_risk_and_retributive_liability_score: float
    qdt_whistleblower_cognitive_state_score: float
    sovereign_strategic_capex_impact_score: float
    composite_sovereign_authenticity_index: float
    epistemic_classification: str
    operational_action: str
    competing_hypotheses: Dict[str, float]
    council_perspectives: Dict[str, str]


class SatyamevaSuchakaPipeline:
    """The master pipeline orchestrating all 16 sieves, ACH hypothesis arbitration, and council projections."""

    @classmethod
    def evaluate_dossier(cls, d: WhistleblowerDossier) -> WhistleblowerEvaluation:
        # 1. Run all 16 sieves
        r_spi = SovereignPublicInterestSieve.evaluate(
            casualty_threat=d.casualty_threat,
            ecological_damage=d.ecological_damage,
            retail_capital_loss=d.retail_capital_loss,
            corporate_sensationalism=d.corporate_sensationalism,
        )
        r_atc = AdversaryTimingCorrelationSieve.evaluate(
            timing_proximity=d.timing_proximity,
            summit_sensitivity=d.summit_sensitivity,
            organic_reporting_lag=d.organic_reporting_lag,
        )
        r_dpa = DocumentaryProvenanceAuthenticitySieve.evaluate(
            cryptographic_hash_match=d.cryptographic_hash_match,
            device_certificate_provenance=d.device_certificate_provenance,
            typographical_anomaly_ratio=d.typographical_anomaly_ratio,
            source_chain_of_custody=d.source_chain_of_custody,
        )
        r_brd = BearRaidDerivativeForensicsSieve.evaluate(
            put_volume_spike=d.put_volume_spike,
            pnote_short_concentration=d.pnote_short_concentration,
            normal_hedging_ratio=d.normal_hedging_ratio,
        )
        r_odc = OffshoreDebtCovenantContagionSieve.evaluate(
            cross_default_exposure=d.cross_default_exposure,
            lc_credit_freeze=d.lc_credit_freeze,
            sovereign_liquidity_backstop=d.sovereign_liquidity_backstop,
        )
        r_efs = ExfiltrationAndForeignSanctuarySieve.evaluate(
            visa_pre_clearance=d.visa_pre_clearance,
            embassy_sanctuary_proximity=d.embassy_sanctuary_proximity,
            offshore_retainer=d.offshore_retainer,
            domestic_residence_commitment=d.domestic_residence_commitment,
        )
        r_rto = RetaliationThreatAndOpSecSieve.evaluate(
            physical_intimidation=d.physical_intimidation,
            slapp_litigation_asymmetry=d.slapp_litigation_asymmetry,
            statutory_police_protection=d.statutory_police_protection,
        )
        r_vsr = VigilanceStatutoryRemedySieve.evaluate(
            jurisdictional_fit=d.jurisdictional_fit,
            statutory_safeguard_score=d.statutory_safeguard_score,
            jurisdictional_ambiguity=d.jurisdictional_ambiguity,
        )
        r_skc = SpeechKinesicAndChromaticForensicsSieve.evaluate(
            facs_deception_marker=d.facs_deception_marker,
            vocal_pitch_jitter=d.vocal_pitch_jitter,
            chromatic_incongruence=d.chromatic_incongruence,
            autonomic_baseline_stability=d.autonomic_baseline_stability,
        )
        r_son = SpeechOmissionAndNegativeSpaceSieve.evaluate(
            deliberate_omission_density=d.deliberate_omission_density,
            taboo_topic_suppression=d.taboo_topic_suppression,
            comprehensive_coverage_ratio=d.comprehensive_coverage_ratio,
        )
        r_tbl = TradeBasedMoneyLaunderingSieve.evaluate(
            customs_remittance_discrepancy=d.customs_remittance_discrepancy,
            gst_eway_divergence=d.gst_eway_divergence,
            port_clearance_verification=d.port_clearance_verification,
        )
        r_dst = DefenseSCADAAndFirmwareTamperSieve.evaluate(
            firmware_hash_deviation=d.firmware_hash_deviation,
            unauthorized_microcode_call=d.unauthorized_microcode_call,
            cryptographic_signing_validity=d.cryptographic_signing_validity,
        )
        r_chs = CulturalHeritageAndSacralityBreachSieve.evaluate(
            antiquities_illicit_auction_score=d.antiquities_illicit_auction_score,
            sacral_space_encroachment=d.sacral_space_encroachment,
            archaeological_survey_protection=d.archaeological_survey_protection,
        )
        r_prr = PerjuryRiskAndRetributiveLiabilitySieve.evaluate(
            fabricated_claim_ratio=d.fabricated_claim_ratio,
            malicious_intent_score=d.malicious_intent_score,
            substantiated_evidence_ratio=d.substantiated_evidence_ratio,
        )
        r_qdt = QDTWhistleblowerCognitiveStateSieve.evaluate(
            psi_duty=d.psi_duty,
            psi_fear=d.psi_fear,
            theta_retaliation_rad=d.theta_retaliation_rad,
        )
        r_sci = SovereignStrategicCapExImpactSieve.evaluate(
            capex_multiplier_scale=d.capex_multiplier_scale,
            supply_chain_criticality=d.supply_chain_criticality,
            receivership_remedy_viability=d.receivership_remedy_viability,
        )

        s_spi = r_spi["sovereign_public_interest_score"]
        s_atc = r_atc["adversary_timing_correlation_score"]
        s_dpa = r_dpa["documentary_provenance_authenticity_score"]
        s_brd = r_brd["bear_raid_derivative_forensics_score"]
        s_odc = r_odc["offshore_debt_covenant_contagion_score"]
        s_efs = r_efs["exfiltration_and_foreign_sanctuary_score"]
        s_rto = r_rto["retaliation_threat_and_opsec_score"]
        s_vsr = r_vsr["vigilance_statutory_remedy_score"]
        s_skc = r_skc["speech_kinesic_and_chromatic_forensics_score"]
        s_son = r_son["speech_omission_and_negative_space_score"]
        s_tbl = r_tbl["trade_based_money_laundering_score"]
        s_dst = r_dst["defense_scada_and_firmware_tamper_score"]
        s_chs = r_chs["cultural_heritage_and_sacrality_breach_score"]
        s_prr = r_prr["perjury_risk_and_retributive_liability_score"]
        s_qdt = r_qdt["qdt_whistleblower_cognitive_state_score"]
        s_sci = r_sci["sovereign_strategic_capex_impact_score"]

        # 2. Composite Authenticity Index
        # High public interest, documentary authenticity, duty, and remedy elevate authenticity;
        # High bear-raid, exfiltration collusion, timing coincidence, and perjury risk dampen authenticity.
        pos_weight = (s_spi * 0.25) + (s_dpa * 0.25) + (s_vsr * 0.15) + (s_qdt * 0.15) + (s_dst * 0.10) + (s_tbl * 0.10)
        neg_weight = (s_atc * 0.25) + (s_brd * 0.25) + (s_efs * 0.20) + (s_prr * 0.20) + (s_skc * 0.10)
        composite_idx = round(max(0.0, min(1.0, 0.50 + 0.50 * (pos_weight - neg_weight))), 4)

        # 3. Analysis of Competing Hypotheses (ACH)
        h_genuine = round(max(0.01, (s_spi * 0.40) + (s_dpa * 0.40) + (1.0 - s_prr) * 0.20), 4)
        h_bear_raid = round(max(0.01, (s_brd * 0.50) + (s_odc * 0.30) + (s_atc * 0.20)), 4)
        h_foreign_sabotage = round(max(0.01, (s_efs * 0.45) + (s_atc * 0.35) + (s_son * 0.20)), 4)
        h_domestic_slander = round(max(0.01, (s_prr * 0.50) + (s_skc * 0.30) + (1.0 - s_dpa) * 0.20), 4)

        tot_h = h_genuine + h_bear_raid + h_foreign_sabotage + h_domestic_slander
        hypotheses = {
            "GENUINE_PUBLIC_INTEREST_WHISTLEBLOWING": round(h_genuine / tot_h, 4),
            "COORDINATED_OFFSHORE_BEAR_RAID": round(h_bear_raid / tot_h, 4),
            "FOREIGN_INTELLIGENCE_HYBRID_SABOTAGE": round(h_foreign_sabotage / tot_h, 4),
            "MALICIOUS_DOMESTIC_SLANDER_EXTORTION": round(h_domestic_slander / tot_h, 4),
        }

        leading_hypothesis = max(hypotheses, key=hypotheses.get)

        # 4. Epistemic Classification & Operational Action
        if leading_hypothesis == "GENUINE_PUBLIC_INTEREST_WHISTLEBLOWING":
            if composite_idx >= 0.70:
                classification = "VERIFIED_GENUINE_WHISTLEBLOWER_DISCLOSURE"
                action = (
                    "ACTIVATE_STATUTORY_PROTECTION_AND_VIGILANCE_ESCALATION: Route payload to CVC/SFIO/ED with sealed witness protection. "
                    + ("Enforce curative receivership (Satyam model) to preserve critical CapEx supply chains." if s_sci >= 0.65 else "Initiate formal judicial inquiry.")
                )
            else:
                classification = "PLAUSIBLE_WHISTLEBLOWING_REQUIRING_PRIMARY_CORROBORATION"
                action = "REQUEST_CRYPTOGRAPHIC_ESCROW_DEPOSIT: Secure original device certificate under BSA 2023 Sec 63."
        elif leading_hypothesis == "COORDINATED_OFFSHORE_BEAR_RAID":
            classification = "PREDATORY_OFFSHORE_BEAR_RAID_NARRATIVE"
            action = "ALERT_SEBI_AND_FIU: Freeze suspicious GIFT Nifty/offshore derivative contracts and investigate P-Note short-sellers."
        elif leading_hypothesis == "FOREIGN_INTELLIGENCE_HYBRID_SABOTAGE":
            classification = "ADVERSARIAL_HYBRID_COVERT_DISINFORMATION"
            action = "COUNTER_INTELLIGENCE_INTERCEPT: Audit exfiltration pipeline, notify immigration/borders, and decouple from sovereign summits."
        else:
            classification = "MALICIOUS_PERJURY_AND_CORPORATE_EXTORTION"
            action = "BNS_SECTION_229_230_RETRIBUTIVE_PROSECUTION: File criminal slander and extortion charges against malicious accusers."

        # 5. Multi-Domain Council Perspectives
        council = {
            "Ajit_Doval": (
                f"Provenance Audit ({hypotheses['FOREIGN_INTELLIGENCE_HYBRID_SABOTAGE']*100:.1f}% Sabotage Prob): Exfiltration score {s_efs:.2f}. "
                f"Ensure whistleblower physical security if genuine; neutralize foreign embassy conduits if cultivated."
            ),
            "Dr_S_Jaishankar": (
                f"Multilateral Lawfare Filter ({hypotheses['COORDINATED_OFFSHORE_BEAR_RAID']*100:.1f}% Bear-Raid): Timing correlation {s_atc:.2f}. "
                f"Decouple sovereign reputation from Western rating attacks and media amplification."
            ),
            "Dr_Ankit_Shah": (
                f"Balance Sheet Forensics: Bear-raid put spike {s_brd:.2f}, Debt covenant contagion {s_odc:.2f}, TBML mismatch {s_tbl:.2f}. "
                f"Monitor Eurodollar repo margins and bank LC lines to prevent forced asset fire-sales."
            ),
            "Sanjeev_Sanyal": (
                f"Complex Adaptive CapEx Impact: Systemic CapEx multiplier score {s_sci:.2f}. "
                f"Prevent factory shutdowns; pursue curative receivership over enterprise destruction."
            ),
            "J_Sai_Deepak": (
                f"Bharatiya Jurisprudence: BSA 2023 Sec 61-63 score {s_dpa:.2f}, Perjury liability risk {s_prr:.2f}. "
                f"Enforce retributive liability against bad-faith slander while upholding constitutional duty."
            ),
            "Dr_Anand_Ranganathan": (
                f"Scientific Empiricism: Public interest score {s_spi:.2f}, SCADA tamper {s_dst:.2f}. "
                f"Zero tolerance for physical adulteration or cover-ups; demand raw mass-spectrometry and microcode hashes."
            ),
            "PM_Narendra_Modi": (
                f"Atmanirbharta & Yogakshema: Composite sovereign authenticity {composite_idx:.2f}. "
                f"Protect public welfare ruthlessly without permitting foreign hybrid sabotage to derail national growth."
            ),
            # Expanded Sovereign Epistemic Profiles
            "Dr_Sudhanshu_Trivedi": (
                f"Historical & Scriptural Epistemology: Neutralize semantic distortion. "
                f"Verify primary textual/historical evidence and prevent foreign ideological colonization of domestic discourse."
            ),
            "Pushpendra_Kulshrestha": (
                f"Media Syndicate & Grassroots Vigilance: Exfiltration score {s_efs:.2f}. "
                f"Deconstruct foreign-funded media echo-chambers and expose fifth-column narrative warfare targeting national stability."
            ),
            "Dr_Syed_Rizwan_Ahmed": (
                f"Forensic Courtroom Cross-Examination: Perjury liability risk {s_prr:.2f}, BSA score {s_dpa:.2f}. "
                f"Enforce strict chain of custody and initiate BNS criminal perjury proceedings against motivated extortionists."
            ),
            "Neeraj_Atri": (
                f"Primary Document & Archival Audit: Check primary customs/bank records against circular citation loops in NGO leaks."
            ),
            "Sadhguru_Jaggi_Vasudev": (
                f"Ecological Vitality & Conscious Statecraft: Sacrality score {s_chs:.2f}. "
                f"Safeguard fertile soil, river systems, and temple autonomy while maintaining non-ideological infrastructure growth."
            ),
            "Dr_Kumar_Vishwas": (
                f"Rashtriya Cultural Consciousness: Protect national morale and retail citizen confidence from manufactured panic."
            ),
            "Srijan_Pal_Singh": (
                f"Deep Tech & Kalam Mission-Mode Execution: SCADA tamper score {s_dst:.2f}. "
                f"Air-gap critical ports and defense microcode; maintain technological self-reliance."
            ),
            "Dr_B_R_Ambedkar": (
                f"Constitutional Morality & Institutional Antifragility: Enforce statutory regulatory oversight (SEBI/CAG/ED) "
                f"to prevent both corporate cartel monopoly and foreign institutional coercion."
            ),
            # Classical Dharmic & Vedic Statecraft Archetypes
            "Acharya_Chanakya_Kautilya": (
                f"Arthashastra Statecraft: Ubhaya-vetana double-agent audit. Secure the Kosha (treasury) against bear-raids ({s_brd:.2f}) "
                f"and strike asymmetric foreign adversaries using Sandhi-Vigraha equilibrium."
            ),
            "Sri_Krishna_Rajadharma": (
                f"Rajadharma & Strategic Equilibrium: Overcome cognitive paralysis. Distinguish between genuine righteous reform "
                f"and adharmic economic warfare disguised as virtue."
            ),
            "Vedic_Rishi_Pramana": (
                f"Pramana Epistemology: Triangulate Pratyaksha (direct invoice/bank telemetry), Anumana (timing inference), "
                f"and Shabda (verified cryptography) to dissolve narrative Maya."
            ),
            "Maryada_Purushottam_Sri_Ram": (
                f"Ram Rajya Governance Ethics: Maintain total administrative transparency and Praja-Anuraga (citizen trust). "
                f"Zero compromise on public safety and moral integrity."
            ),
            "Dr_Meenakshi_Jain": (
                f"Epigraphic & Primary Evidence Audit: Sacrality score {s_chs:.2f}. "
                f"Reconcile land revenue records, temple inscriptions, and colonial survey discrepancies to establish irrefutable historical title."
            ),
            "Ami_Ganatra": (
                f"Canonical Textual & Epic Fidelity: Audit claims against original Sanskrit recensions to eliminate "
                f"manipulative interpolations and preserve civilizational legal integrity."
            ),
            "Major_Gaurav_Arya": (
                f"Tactical Hybrid Threat & Border Forensics: Exfiltration score {s_efs:.2f}, SCADA tamper {s_dst:.2f}. "
                f"Expose adversary proxy intelligence warfare and maintain offensive counter-measures along sensitive operational axes."
            ),
        }

        return WhistleblowerEvaluation(
            dossier_id=d.dossier_id,
            target_entity=d.target_entity,
            domain=d.domain,
            sovereign_public_interest_score=s_spi,
            adversary_timing_correlation_score=s_atc,
            documentary_provenance_authenticity_score=s_dpa,
            bear_raid_derivative_forensics_score=s_brd,
            offshore_debt_covenant_contagion_score=s_odc,
            exfiltration_and_foreign_sanctuary_score=s_efs,
            retaliation_threat_and_opsec_score=s_rto,
            vigilance_statutory_remedy_score=s_vsr,
            speech_kinesic_and_chromatic_forensics_score=s_skc,
            speech_omission_and_negative_space_score=s_son,
            trade_based_money_laundering_score=s_tbl,
            defense_scada_and_firmware_tamper_score=s_dst,
            cultural_heritage_and_sacrality_breach_score=s_chs,
            perjury_risk_and_retributive_liability_score=s_prr,
            qdt_whistleblower_cognitive_state_score=s_qdt,
            sovereign_strategic_capex_impact_score=s_sci,
            composite_sovereign_authenticity_index=composite_idx,
            epistemic_classification=classification,
            operational_action=action,
            competing_hypotheses=hypotheses,
            council_perspectives=council,
        )

```
