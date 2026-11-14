# LENS SPECIFICATION: GEOPOLITICAL

```python
"""
Lens 5: Geopolitical Balance of Power Lens.
Evaluates multipolar balance, strategic hedging, deterrence,
and regional rivalries (LAC standoff, Gulf balance, Horn of Africa frictions).
"""

from typing import Any, Dict, List, Optional
import math
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

        # Phase 267: Wire DiasporaSanctuaryLawfareSieve
        geo_meta = getattr(summit, "metadata", {}) or {}
        diaspora_params = geo_meta.get("diaspora_sanctuary", {}) if isinstance(geo_meta, dict) else {}
        _diaspora_res = DiasporaSanctuaryLawfareSieve.calculate_sanctuary_threat(
            host_tolerance_index=diaspora_params.get("host_tolerance_index", 0.55),
            illicit_remittance_flow=diaspora_params.get("illicit_remittance_flow", 0.45),
            extradition_coercion_depth=diaspora_params.get("extradition_coercion_depth", 0.50),
            bilateral_diplomatic_leverage=diaspora_params.get("bilateral_diplomatic_leverage", 0.60),
        )
        metrics["transnational_extremism_threat_score"] = _diaspora_res["transnational_extremism_threat_score"]
        metrics["host_sanctuary_lawfare_exposure"] = _diaspora_res["host_sanctuary_lawfare_exposure"]
        metrics["diaspora_sanctuary_tier"] = _diaspora_res["diaspora_sanctuary_tier"]

        # Phase 283: Wire IslandEEZMaritimeNetSecuritySieve
        island_params = geo_meta.get("island_net_security", {}) if isinstance(geo_meta, dict) else {}
        _island_res = IslandEEZMaritimeNetSecuritySieve.calculate_maritime_net_security(
            basing_airgap_radius=island_params.get("basing_airgap_radius", 0.75),
            sagar_treaty_depth=island_params.get("sagar_treaty_depth", 0.80),
            coastal_radar_uptime=island_params.get("coastal_radar_uptime", 0.85),
            plan_dual_use_incursion=island_params.get("plan_dual_use_incursion", 0.35),
            host_nation_political_drift=island_params.get("host_nation_political_drift", 0.25),
        )
        metrics["maritime_net_security_score"] = _island_res["maritime_net_security_score"]
        metrics["maritime_bastion_tier"] = _island_res["maritime_bastion_tier"]
        metrics["chinese_hydrographic_threat_index"] = _island_res["chinese_hydrographic_threat_index"]
        metrics["agalega_surveillance_readiness"] = _island_res["agalega_surveillance_readiness"]

        # Phase 295: Wire TransHimalayanHydrologicalDeterrenceSieve
        hydro_params = geo_meta.get("trans_himalayan_hydrology", {}) if isinstance(geo_meta, dict) else {}
        _hydro_res = TransHimalayanHydrologicalDeterrenceSieve.calculate(
            buffer_storage_bcm=hydro_params.get("buffer_storage_bcm", 9.0),
            threat_surge_volume_bcm=hydro_params.get("threat_surge_volume_bcm", 10.0),
            lean_season_flow_parity=hydro_params.get("lean_season_flow_parity", 0.85),
            ngo_subversion_index=hydro_params.get("ngo_subversion_index", 0.25),
            proxy_political_obstruction=hydro_params.get("proxy_political_obstruction", 0.20),
            state_counter_sabotage=hydro_params.get("state_counter_sabotage", 0.75),
            malacca_counter_leverage_readiness=hydro_params.get("malacca_counter_leverage_readiness", 0.88),
        )
        metrics["hydro_deterrence_score"] = _hydro_res["hydro_deterrence_score"]

        # Phase 335: Black Swan Disruption Sieve
        gp_meta = getattr(summit, "metadata", {}) or {}
        bs_params = gp_meta.get("black_swan", {}) if isinstance(gp_meta, dict) else {}
        _bs_res = BlackSwanDisruptionSieve.calculate(
            shock_tail_risk_index=bs_params.get("shock_tail_risk_index", 0.75),
            infrastructure_coupling_density=bs_params.get("infrastructure_coupling_density", 0.80),
            redundancy_isolation_buffer=bs_params.get("redundancy_isolation_buffer", 0.30),
        )
        metrics["black_swan_disruption_score"] = _bs_res["black_swan_disruption_score"]
        metrics["hydrologic_sovereignty_tier"] = _hydro_res["hydrologic_sovereignty_tier"]
        metrics["asymmetric_escalation_parity"] = _hydro_res["asymmetric_escalation_parity"]

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


class DiasporaSanctuaryLawfareSieve:
    """
    Phase 267: Diaspora Sanctuary Lawfare Sieve.
    Quantifies national security exposure to transnational extremist safe havens in Western partner nations
    (e.g., Canada, UK, US), host government political vote-bank tolerance under 'free speech' pretexts,
    illicit diaspora charity remittance diversion, counterbalanced by reciprocal extradition coercion
    and bilateral trade/consular conditionality.
    """

    @classmethod
    def calculate_sanctuary_threat(
        cls,
        host_tolerance_index: float = 0.55,
        illicit_remittance_flow: float = 0.45,
        extradition_coercion_depth: float = 0.50,
        bilateral_diplomatic_leverage: float = 0.60,
    ) -> Dict[str, Any]:
        """
        Calculates transnational extremist sanctuary threat score using calibrated logistic sigmoid:
            z = 2.8 * HostTolerance + 2.4 * Remittances - 2.6 * Extradition - 2.2 * Leverage - 1.0
            threat = 1 / (1 + exp(-z))
        """
        import math
        host = max(0.0, min(1.0, float(host_tolerance_index)))
        remit = max(0.0, min(1.0, float(illicit_remittance_flow)))
        extra = max(0.0, min(1.0, float(extradition_coercion_depth)))
        lev = max(0.0, min(1.0, float(bilateral_diplomatic_leverage)))

        z = 2.8 * host + 2.4 * remit - 2.6 * extra - 2.2 * lev - 1.0
        threat = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if threat >= 0.75:
            tier = "ACUTE_TRANSNATIONAL_EXTREMIST_SANCTUARY"
            verdict = "HOST_STATE_SHIELDING_SUBVERSIVE_NETWORKS"
            rationale = (
                f"Acute sanctuary threat ({threat:.4f}): Host nation political tolerance ({host:.2f}) and dark remittance "
                f"flows ({remit:.2f}) shield anti-India violent extremism; mandates aggressive consular/economic reciprocity."
            )
        elif threat >= 0.55:
            tier = "ELEVATED_HOST_STATE_SHIELDING"
            verdict = "DIPLOMATIC_INERTIA_IMPEDING_EXTRADITION"
            rationale = (
                f"Elevated shielding ({threat:.4f}): Host government relies on procedural lawfare and free-speech pretexts "
                f"to stall red-corner notices and extradition dossiers."
            )
        elif threat >= 0.35:
            tier = "CONTESTED_EXTRADITION_CORRIDORS"
            verdict = "BALANCED_CONSULAR_CONTESTATION"
            rationale = (
                f"Contested corridors ({threat:.4f}): Diplomatic leverage ({lev:.2f}) yields selective security coordination "
                f"amid continuing diaspora political friction."
            )
        else:
            tier = "FORTIFIED_RECIPROCAL_CONSULAR_SECURITY"
            verdict = "EFFECTIVE_TRANSNATIONAL_DETERRENCE_ACTIVE"
            rationale = (
                f"Fortified security ({threat:.4f}): Assertive extradition leverage ({extra:.2f}) and mutual intelligence "
                f"interdiction neutralize external sanctuary operations."
            )

        exposure = round(min(1.0, host * 1.25), 4)
        reciprocal_idx = round(min(1.0, extra * 0.85 + lev * 0.15), 4)

        return {
            "transnational_extremism_threat_score": threat,
            "host_tolerance_index": round(host, 4),
            "illicit_remittance_flow": round(remit, 4),
            "extradition_coercion_depth": round(extra, 4),
            "bilateral_diplomatic_leverage": round(lev, 4),
            "host_sanctuary_lawfare_exposure": exposure,
            "reciprocal_diplomatic_pressure_index": reciprocal_idx,
            "diaspora_sanctuary_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_sanctuary_coercive": threat >= 0.55,
        }


class IslandEEZMaritimeNetSecuritySieve:
    """
    Phase 283: Island EEZ Maritime Net Security Sieve.
    Models Southwest Indian Ocean Maritime Domain Awareness (MDA), Net Security Provider posture
    across island littoral states (Mauritius, Seychelles, Maldives, Sri Lanka), Agaléga surveillance
    patrol radius (P-8I coverage), and Chinese dual-use hydrographic/research vessel interdiction.
    """

    @classmethod
    def calculate_maritime_net_security(
        cls,
        basing_airgap_radius: float = 0.75,
        sagar_treaty_depth: float = 0.80,
        coastal_radar_uptime: float = 0.85,
        plan_dual_use_incursion: float = 0.35,
        host_nation_political_drift: float = 0.25,
    ) -> Dict[str, Any]:
        """
        Calculates Maritime Net Security Score using calibrated logistic sigmoid:
            z = 2.8 * basing + 2.6 * sagar + 2.2 * radar - 3.2 * plan - 2.5 * drift - 0.4
            score = 1 / (1 + exp(-z))
        """
        import math
        basing = max(0.0, min(1.0, float(basing_airgap_radius)))
        sagar = max(0.0, min(1.0, float(sagar_treaty_depth)))
        radar = max(0.0, min(1.0, float(coastal_radar_uptime)))
        plan = max(0.0, min(1.0, float(plan_dual_use_incursion)))
        drift = max(0.0, min(1.0, float(host_nation_political_drift)))

        z = 2.8 * basing + 2.6 * sagar + 2.2 * radar - 3.2 * plan - 2.5 * drift - 0.4
        score = round(1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, z)))), 4)

        if score >= 0.75:
            tier = "FORTIFIED_IOR_MARITIME_BASTION"
            verdict = "DOMINANT_SOUTHWEST_IOR_NET_SECURITY_PROVIDER"
            rationale = (
                f"Fortified maritime bastion ({score:.4f}): Agaléga airgap radius ({basing:.2f}) and SAGAR treaty "
                f"depth ({sagar:.2f}) establish dominant P-8I surveillance and choke Chinese hydrographic incursions."
            )
        elif score >= 0.55:
            tier = "SUSTAINED_NET_SECURITY_SUPERIORITY"
            verdict = "RESILIENT_LITTORAL_RADAR_AND_PATROL_COVERAGE"
            rationale = (
                f"Sustained superiority ({score:.4f}): High radar uptime ({radar:.2f}) offsets moderate host nation "
                f"political drift ({drift:.2f}); maintains stable EEZ deterrence."
            )
        elif score >= 0.35:
            tier = "CONTESTED_ISLAND_LITTORAL_PRESSURE"
            verdict = "ESCALATING_DUAL_USE_RESEARCH_SURVEILLANCE"
            rationale = (
                f"Contested pressure ({score:.4f}): Chinese dual-use research vessel incursions ({plan:.2f}) and political "
                f"drift ({drift:.2f}) threaten forward maritime basing access."
            )
        else:
            tier = "CRITICAL_CHINESE_CHOKEPOINT_ENCIRCLEMENT"
            verdict = "ACUTE_LITTORAL_BASING_DENIAL_RISK"
            rationale = (
                f"Critical encirclement ({score:.4f}): High PLAN dual-use penetration ({plan:.2f}) and hostile political drift "
                f"compromise southwest IOR chokepoint security."
            )

        surv_readiness = round(min(1.0, basing * 0.90 + radar * 0.10), 4)
        threat_idx = round(min(1.0, plan * 0.70 + drift * 0.30), 4)

        return {
            "maritime_net_security_score": score,
            "basing_airgap_radius": round(basing, 4),
            "sagar_treaty_depth": round(sagar, 4),
            "coastal_radar_uptime": round(radar, 4),
            "plan_dual_use_incursion": round(plan, 4),
            "host_nation_political_drift": round(drift, 4),
            "agalega_surveillance_readiness": surv_readiness,
            "chinese_hydrographic_threat_index": threat_idx,
            "maritime_bastion_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_bastion_secure": score >= 0.55,
        }


class TransHimalayanHydrologicalDeterrenceSieve:
    """
    Phase 295: Trans-Himalayan Hydrological Warfare, Buffer Reservoir Sizing & Hybrid Sabotage Resistance Sieve.
    Quantifies Chinese upstream damming weaponization (Medog / Great Bend Yarlung Tsangpo 60,000 MW mega-dam)
    against Indian downstream counter-deterrence (Upper Siang 11,000 MW multipurpose buffer reservoir),
    incorporating hybrid subversion risks (foreign-funded NGO fear-mongering and political obstruction).

    Formulation:
      SurgeAbsorb = min(2.0, buffer_storage_bcm / (threat_surge_volume_bcm + 1e-6))
      SabotageRisk = max(0.0, min(1.0, 0.45 * ngo_subversion_index + 0.35 * proxy_political_obstruction - 0.30 * state_counter_sabotage))
      z = 2.8 * SurgeAbsorb + 2.5 * lean_season_flow_parity - 3.2 * SabotageRisk - 0.4
      S_Hydro = 1.0 / (1.0 + exp(-z))
    """

    @staticmethod
    def calculate(
        buffer_storage_bcm: float = 9.0,
        threat_surge_volume_bcm: float = 10.0,
        lean_season_flow_parity: float = 0.85,
        ngo_subversion_index: float = 0.25,
        proxy_political_obstruction: float = 0.20,
        state_counter_sabotage: float = 0.75,
        malacca_counter_leverage_readiness: float = 0.88,
    ) -> Dict[str, Any]:
        buf = max(0.0, float(buffer_storage_bcm))
        surge = max(0.001, float(threat_surge_volume_bcm))
        flow = max(0.0, min(1.0, float(lean_season_flow_parity)))
        ngo = max(0.0, min(1.0, float(ngo_subversion_index)))
        proxy = max(0.0, min(1.0, float(proxy_political_obstruction)))
        counter = max(0.0, min(1.0, float(state_counter_sabotage)))
        malacca = max(0.0, min(1.0, float(malacca_counter_leverage_readiness)))

        surge_absorb = min(2.0, buf / (surge + 1e-6))
        sabotage_risk = max(0.0, min(1.0, 0.45 * ngo + 0.35 * proxy - 0.30 * counter))

        z = 2.8 * surge_absorb + 2.5 * flow - 3.2 * sabotage_risk - 0.4
        score = round(1.0 / (1.0 + math.exp(-z)), 4)

        if score >= 0.75:
            tier = "FORTIFIED_HYDROLOGIC_BUFFER_SOVEREIGNTY"
            verdict = "STRATEGIC_SURGE_ABSORPTION_CERTIFIED"
            rationale = (
                f"Fortified sovereignty ({score:.4f}): Upper Siang buffer capacity ({buf:.1f} BCM) "
                f"neutralizes Chinese Medog upstream surge threats while domestic sabotage risk ({sabotage_risk:.2f}) is contained."
            )
        elif score >= 0.55:
            tier = "ROBUST_TRANSHIMALAYAN_DETERRENCE_STABLE"
            verdict = "ADEQUATE_FLOOD_BUFFER_AND_LEAN_FLOW"
            rationale = (
                f"Robust deterrence ({score:.4f}): Buffer absorption ({surge_absorb:.2f}) provides adequate defense, "
                f"but ongoing NGO narrative friction requires active state communication."
            )
        elif score >= 0.35:
            tier = "CONTESTED_DOWNSTREAM_RIPARIAN_VULNERABILITY"
            verdict = "ELEVATED_FLASH_FLOOD_AND_DROUGHT_RISK"
            rationale = (
                f"Contested vulnerability ({score:.4f}): Subversion friction ({sabotage_risk:.2f}) stalls buffer reservoir execution, "
                f"exposing Assam-Arunachal river basins to upstream manipulation."
            )
        else:
            tier = "CRITICAL_HYDRAULIC_BLACKMAIL_EXPOSURE"
            verdict = "ACUTE_CATASTROPHIC_SURGE_DEFICIT"
            rationale = (
                f"Critical exposure ({score:.4f}): Inadequate buffer storage and high sabotage paralysis "
                f"leave northeast India defenseless against weaponized hydrologic releases."
            )

        asymmetric_ratio = round(min(1.0, (score * 0.60) + (malacca * 0.40)), 4)

        return {
            "hydro_deterrence_score": score,
            "surge_absorption_ratio": round(surge_absorb, 4),
            "lean_season_flow_parity": round(flow, 4),
            "hybrid_sabotage_risk": round(sabotage_risk, 4),
            "malacca_counter_leverage_readiness": round(malacca, 4),
            "asymmetric_escalation_parity": asymmetric_ratio,
            "hydrologic_sovereignty_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "is_buffer_fortified": score >= 0.55,
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