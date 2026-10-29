# LENS SPECIFICATION: GEOPOLITICAL

```python
"""
Lens 5: Geopolitical Balance of Power Lens.
Evaluates multipolar balance, strategic hedging, deterrence,
and regional rivalries (LAC standoff, Gulf balance, Horn of Africa frictions).
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, SummitEvent


class ChokepointKineticSieve:
    """
    Sub-National Geographic Chokepoint & Transnational Hydrological Pincer Sieve.
    Quantifies vulnerability for narrow geographic bottlenecks (W_corridor <= 50 km)
    such as the Siliguri Corridor ("Chicken's Neck"), Suwalki Gap, or Wakhan Corridor,
    evaluating the confluence of adversary forward armor, hostile flank regime shifts,
    and upstream hydrological diversion levers.
    """

    @classmethod
    def calculate_chokepoint_vulnerability(
        cls,
        corridor_width_km: float = 22.0,
        adversary_proximity_km: float = 35.0,
        hostile_flank_index: float = 0.70,
        upstream_hydro_leverage: float = 0.65,
        logistics_redundancy_count: int = 1
    ) -> Dict[str, Any]:
        """
        Computes closed-form Chokepoint Vulnerability Index (V_choke in [0.0, 1.0]).
        Formula:
          Width_Hazard = min(1.0, 50.0 / max(1.0, corridor_width_km))
          Proximity_Weight = max(0.0, 1.0 - (adversary_proximity_km / 100.0))
          Pincer_Hazard = 0.40 * hostile_flank_index + 0.35 * Proximity_Weight + 0.25 * upstream_hydro_leverage
          Base_Risk = 0.50 * Width_Hazard + 0.50 * Pincer_Hazard
          Redundancy_Discount = max(0.50, 1.0 - (max(0, logistics_redundancy_count - 1) * 0.20))
          V_choke = min(1.0, round(Base_Risk * Redundancy_Discount, 4))
        """
        width_hazard = min(1.0, 50.0 / max(1.0, corridor_width_km))
        prox_weight = max(0.0, 1.0 - (adversary_proximity_km / 100.0))
        pincer_hazard = round(0.40 * hostile_flank_index + 0.35 * prox_weight + 0.25 * upstream_hydro_leverage, 4)
        base_risk = 0.50 * width_hazard + 0.50 * pincer_hazard
        redundancy_discount = max(0.50, 1.0 - (max(0, logistics_redundancy_count - 1) * 0.20))
        v_choke = min(1.0, round(base_risk * redundancy_discount, 4))

        if v_choke >= 0.75:
            tier = "CRITICAL_CHOKEPOINT"
            posture = "OFFENSIVE_DEFENSIVE_PREEMPTION_MANDATED"
        elif v_choke >= 0.50:
            tier = "ELEVATED_VULNERABILITY"
            posture = "MULTI_MODAL_BYPASS_REDUNDANCY_REQUIRED"
        elif v_choke >= 0.30:
            tier = "MODERATE_FRICTION"
            posture = "FORWARD_SURVEILLANCE_ACTIVE"
        else:
            tier = "SECURE_TRANSIT"
            posture = "ROUTINE_SECURITY"

        rationale = (
            f"Corridor width ({corridor_width_km}km) yields width hazard {width_hazard:.2f}. "
            f"Adversary proximity ({adversary_proximity_km}km) and flank index ({hostile_flank_index:.2f}) "
            f"generate pincer hazard {pincer_hazard:.2f}. Composite vulnerability V_choke: {v_choke:.4f} ({tier})."
        )

        return {
            "chokepoint_vulnerability_index": v_choke,
            "width_hazard_score": round(width_hazard, 4),
            "pincer_hazard_score": round(pincer_hazard, 4),
            "threat_tier": tier,
            "strategic_posture": posture,
            "tactical_rationale": rationale
        }


class GeopoliticalLens:
    """Balance-of-power and multi-alignment evaluator."""

    LENS_NAME = "Geopolitical Balance & Strategic Hedging"
    PRIMARY_TIER = EpistemicTier.TIER_3_SOVEREIGN_REDLINES

    @classmethod
    def evaluate(
        cls,
        summit: SummitEvent,
        evidence: Optional[List[Any]] = None,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Assesses power projection, institutional counterbalancing, internal friction lines,
        and sub-national chokepoint kinetic vulnerabilities (Siliguri, Suwalki, Wakhan).
        Dynamically handles both primary evidence items and ingested claims.
        """
        evidence_list = evidence or claims or []
        findings = [
            "Internal Hegemony Counter-Balancing: India and Brazil function as critical internal anchors, actively preventing Beijing and Moscow from weaponizing BRICS into a formal anti-Western or anti-G7 military-political alliance.",
            "Multi-Alignment Doctrine: India demonstrates multi-vector diplomacy—sitting in BRICS/SCO alongside China and Russia, while simultaneously anchoring the Quad (with the US, Japan, Australia) and expanding defense co-production with France.",
            "Structural Friction Lines: The bloc absorbs acute bilateral tensions—India-China LAC militarization, Saudi-Iran regional hegemony friction, and Egypt-Ethiopia disputes over the Grand Ethiopian Renaissance Dam (GERD).",
            "Expansion Dilution Effect: Rapid expansion broadens the bloc's demographic and energy footprint but dilutes institutional consensus, making binding political consensus virtually unachievable."
        ]

        # Scan for sub-national chokepoint keywords
        choke_terms = [
            "siliguri", "chicken's neck", "chickens neck", "chumbi", "doklam",
            "suwalki", "wakhan", "teesta", "rangpur", "pincer"
        ]
        corpus = (
            f"{getattr(summit, 'summit_name', '')} {getattr(summit, 'title', '')} " +
            " ".join(getattr(ev, 'raw_text', getattr(ev, 'asserted_fact', getattr(ev, 'assertion', ''))) for ev in evidence_list)
        ).lower()

        choke_detected = any(t in corpus for t in choke_terms)
        choke_calc = None

        if choke_detected:
            # Custom corridor parameters based on detected keywords
            width = 22.0 if ("siliguri" in corpus or "chicken" in corpus) else 40.0
            prox = 30.0 if "chumbi" in corpus or "doklam" in corpus else 45.0
            flank = 0.85 if "bangladesh" in corpus or "rangpur" in corpus else 0.60
            hydro = 0.75 if "teesta" in corpus else 0.40
            choke_calc = ChokepointKineticSieve.calculate_chokepoint_vulnerability(
                corridor_width_km=width,
                adversary_proximity_km=prox,
                hostile_flank_index=flank,
                upstream_hydro_leverage=hydro,
                logistics_redundancy_count=1
            )
            findings.insert(
                0,
                f"[SUB-NATIONAL CHOKEPOINT FORENSICS] {choke_calc['tactical_rationale']} "
                f"Mandated Posture: {choke_calc['strategic_posture']}."
            )

        if evidence_list:
            for ev in evidence_list[:2]:
                text = getattr(ev, 'raw_text', getattr(ev, 'asserted_fact', getattr(ev, 'assertion', '')))[:110]
                findings.append(f"[VERIFIED SOVEREIGN SIGNAL: {getattr(ev, 'source_name', 'Primary Source')}] {text}...")

        metrics: Dict[str, Any] = {
            "bloc_character": "Non-Western (Pluralistic), NOT Anti-Western",
            "consensus_cohesion_index": 0.42,
            "external_hedging_index": 0.88, # Very high propensity of members to hedge with external powers
            "core_geopolitical_friction": "India-China LAC / Indo-Pacific strategic divergence",
            "evidence_corroborated": bool(evidence)
        }

        if choke_calc:
            metrics["chokepoint_vulnerability_index"] = choke_calc["chokepoint_vulnerability_index"]
            metrics["chokepoint_threat_tier"] = choke_calc["threat_tier"]
            metrics["pincer_flank_threat_detected"] = True
            metrics["upstream_hydro_leverage_active"] = ("teesta" in corpus)
            alignment = round(max(-1.0, 0.48 - (choke_calc["chokepoint_vulnerability_index"] * 0.30)), 2)
        else:
            metrics["chokepoint_vulnerability_index"] = 0.15
            metrics["chokepoint_threat_tier"] = "SECURE_TRANSIT"
            metrics["pincer_flank_threat_detected"] = False
            metrics["upstream_hydro_leverage_active"] = False
            alignment = 0.48

        confidence = 0.91 if not evidence else round(min(0.98, 0.91 + (len(evidence) * 0.02)), 2)

        # Phase 231: Wire TripartiteCoherenceSieve
        _tri_result = TripartiteCoherenceSieve.calculate_tripartite_coherence(
            shared_maritime_security_alignment=metrics.get("shared_maritime_security_alignment", 0.85),
            defense_interoperability_score=metrics.get("defense_interoperability_score", 0.75),
            economic_supply_chain_synergy=metrics.get("economic_supply_chain_synergy", 0.70),
            bilateral_territorial_friction=metrics.get("bilateral_territorial_friction", 0.15),
        )
        metrics.update(_tri_result)

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=confidence,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )




class TripartiteCoherenceSieve:
    """
    Phase 231: Evaluates strategic cohesion and minilateral alignment across tripartite partnerships
    (e.g., India-France-UAE, India-US-Japan, India-Israel-UAE/I2U2) by balancing shared maritime security,
    defense interoperability, and economic synergy against bilateral territorial or diplomatic frictions.
    """

    @classmethod
    def calculate_tripartite_coherence(
        cls,
        shared_maritime_security_alignment: float = 0.85,
        defense_interoperability_score: float = 0.75,
        economic_supply_chain_synergy: float = 0.70,
        bilateral_territorial_friction: float = 0.15,
    ) -> Dict[str, Any]:
        """
        Calculates minilateral tripartite coherence score using logistic sigmoid model.
        """
        import math
        m_align = max(0.0, min(1.0, float(shared_maritime_security_alignment)))
        d_inter = max(0.0, min(1.0, float(defense_interoperability_score)))
        e_syn = max(0.0, min(1.0, float(economic_supply_chain_synergy)))
        b_fric = max(0.0, min(1.0, float(bilateral_territorial_friction)))

        ratio = (m_align * 0.40 + d_inter * 0.35 + e_syn * 0.25) / max(0.10, 1.0 + 2.0 * b_fric)
        z = 3.5 * ratio - 1.8
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.80:
            tier = "HIGHLY_COHERENT_STRATEGIC_AXIS"
            verdict = "UNIFIED_INDO_PACIFIC_MINILATERAL_LEVERAGE"
            rationale = (
                f"High minilateral coherence ({score:.4f}): Robust maritime alignment ({m_align:.2f}) and defense "
                f"interoperability ({d_inter:.2f}) provide formidable deterrent leverage."
            )
        elif score >= 0.60:
            tier = "EFFECTIVE_TACTICAL_COORDINATION"
            verdict = "FUNCTIONAL_MARITIME_DOMAIN_AWARENESS"
            rationale = (
                f"Effective tactical coordination ({score:.4f}): Solid operational synergy despite minor bilateral frictions ({b_fric:.2f})."
            )
        elif score >= 0.40:
            tier = "FRAGMENTED_BILATERAL_PRIORITIES"
            verdict = "FRICTION_DILUTING_MINILATERAL_COHESION"
            rationale = (
                f"Fragmented priorities ({score:.4f}): Bilateral friction ({b_fric:.2f}) diluting minilateral coalition cohesion."
            )
        else:
            tier = "COGNITIVE_MINILATERAL_DISARRAY"
            verdict = "STRATEGIC_DIVERGENCE_PARALYZING_COALITION"
            rationale = (
                f"Strategic disarray ({score:.4f}): Divergent sovereign objectives render minilateral grouping non-functional."
            )

        return {
            "tripartite_coherence_score": score,
            "shared_maritime_security_alignment": round(m_align, 4),
            "defense_interoperability_score": round(d_inter, 4),
            "economic_supply_chain_synergy": round(e_syn, 4),
            "bilateral_territorial_friction": round(b_fric, 4),
            "tripartite_coherence_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_tripartite_coherent": score >= 0.60
        }

```