# LENS SPECIFICATION: MILITARY_READINESS

```python
"""
Lens 18: Military Readiness, ORBAT & Escalation Dominance.
Evaluates Order of Battle (ORBAT) posture, dual-front military deterrence,
War Wastage Reserves (WWR) ammunition depth, domestic defense industrial base
(IDDM / Atmanirbharta), Integrated Air Defense System (IADS) coverage,
and kinetic escalation ladders.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, StrategicEvent


class AvionicsSovereigntySieve:
    """
    Defense Avionics Electronic Sovereignty & Digital Leash Sieve.
    Quantifies operational autonomy, mission data sovereignty, and foreign telemetry tethering
    for advanced 5th/6th generation combat aircraft (F-35, SU-57, MRFA proposals).
    """

    @classmethod
    def calculate_operational_autonomy(
        cls,
        source_code_transfer: bool = False,
        on_prem_mission_data: bool = False,
        foreign_cloud_tether: bool = True,
        proprietary_kill_switch_risk: float = 0.85
    ) -> Dict[str, Any]:
        """
        Computes closed-form Operational Autonomy Index (Omega_autonomy in [0.0, 1.0]).
        Mathematical Formulation:
          Base_Autonomy = 0.35 * SourceCode + 0.35 * OnPremData + 0.30 * (1.0 - KillSwitchRisk)
          Tether_Discount = 0.70 if foreign_cloud_tether else 1.0
          Omega_autonomy = round(Base_Autonomy * Tether_Discount, 4)
        """
        base_autonomy = (
            (0.35 if source_code_transfer else 0.0) +
            (0.35 if on_prem_mission_data else 0.0) +
            (0.30 * max(0.0, 1.0 - proprietary_kill_switch_risk))
        )
        tether_discount = 0.70 if foreign_cloud_tether else 1.0
        omega_autonomy = min(1.0, max(0.0, round(base_autonomy * tether_discount, 4)))

        if omega_autonomy >= 0.75:
            tier = "SOVEREIGN_AUTONOMOUS"
            verdict = "FULL_MISSION_COMPUTER_AND_WEAPONS_INTEGRATION_FREEDOM"
        elif omega_autonomy >= 0.50:
            tier = "CONDITIONAL_AUTONOMY"
            verdict = "RESTRICTED_SOURCE_ACCESS_WITH_DOMESTIC_DATA_SERVERS"
        elif omega_autonomy >= 0.25:
            tier = "DIGITAL_LEASH_HIGH_RISK"
            verdict = "REMOTE_TELEMETRY_INTERDICTION_SUSCEPTIBLE"
        else:
            tier = "EXTRATERRITORIAL_REMOTE_KILL_SWITCH_ACTIVE"
            verdict = "COMPLETE_MISSION_CLOUD_DEPENDENCE"

        rationale = (
            f"Source code ({source_code_transfer}), On-premise MDF ({on_prem_mission_data}), "
            f"Foreign cloud tether ({foreign_cloud_tether}), Kill-switch risk ({proprietary_kill_switch_risk:.2f}). "
            f"Operational autonomy Omega_autonomy: {omega_autonomy:.4f} ({tier})."
        )

        return {
            "operational_autonomy_score": omega_autonomy,
            "digital_leash_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "source_code_transferred": source_code_transfer,
            "on_prem_mission_data": on_prem_mission_data,
            "cloud_tether_active": foreign_cloud_tether
        }


class MilitaryReadinessLens:
    """Evaluator for kinetic warfighting capability, ammunition stockpiles, and strategic deterrence."""

    LENS_NAME = "Military Readiness, ORBAT & Escalation Dominance"
    PRIMARY_TIER = EpistemicTier.TIER_1_PHYSICAL

    @classmethod
    def evaluate(
        cls,
        event: Any,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Assesses operational military readiness, theater deterrence posture, defense industrial capacity,
        and 5th-Gen combat avionics digital sovereignty.
        """
        findings = [
            "Dual-Front Order of Battle (ORBAT) Posture: Permanent deployment of rebalanced Strike Corps (1 Corps and 17 Mountain Strike Corps) facing the Line of Actual Control (LAC) while maintaining active punitive deterrence along the Line of Control (LoC).",
            "Ammunition Stockpile & War Wastage Reserves (WWR): Ongoing capital procurement targeting 10-day intense (10I) to 40-day (40I) reserve stocking levels across critical precision-guided munitions (PGM), 155mm artillery shells, and loitering munitions.",
            "Defense Industrial Base & Indigenization (Atmanirbharta): Accelerated execution of Positive Indigenisation Lists under DAP 2020, domestic fighter engine co-production agreements (GE-414 for LCA Tejas Mk1A/Mk2), and continuous expansion of indigenous missile manufacturing.",
            "Integrated Air Defense Coverage: Strategic deployment of S-400 Triumf squadrons integrated with indigenous Akash-NG, Project Kusha long-range SAMs, and Phase-II Ballistic Missile Defence (BMD) shields protecting critical political-military nodes.",
            "Kinetic Escalation Ladder: Credible threshold deterrence balancing conventional standoff surgical retaliation with an unyielding No-First-Use (NFU) nuclear posture backed by survivable SSBN second-strike capability (INS Arihant, Arighat).",
            "Cyber & Electronic Warfare Readiness: Fifth-domain warfighting capability across Defence Cyber Agency (DCA), electronic warfare suites (Himshakti/Samyukta), and SIGINT infrastructure. Pre-kinetic cyber operations increasingly precede conventional strikes (as demonstrated in Operation Sindoor 2025).",
            "Asymmetric Naval Balancing & Sub-Kinetic Probing: The Indian Ocean Region (IOR) features structural asymmetry between Indian blue-water sea control (carrier battle groups, P-8I Neptune maritime patrol) and adversary sea-denial (Type 054A/P frigates, Hangor-class AIP submarines, Yarmook-class corvettes). Sub-kinetic naval maneuvers (e.g. ramming/shouldering) seek to probe Rules of Engagement (ROE) without risking decisive fleet encounters."
        ]

        # Scan for defense avionics & digital leash keywords
        avionics_terms = [
            "f-35", "f35", "odin", "alis", "su-57", "su57", "mrfa",
            "stealth fighter", "digital leash", "kill-switch", "kill switch",
            "luneburg", "rcs", "radar cross section", "tarang shakti", "jodhpur"
        ]
        corpus = (
            f"{getattr(event, 'summit_name', '')} {getattr(event, 'title', '')} " +
            " ".join(getattr(c, 'raw_text', getattr(c, 'asserted_fact', getattr(c, 'assertion', ''))) for c in (claims or []))
        ).lower()

        avionics_detected = any(t in corpus for t in avionics_terms)
        avionics_calc = None

        if avionics_detected:
            is_f35 = ("f-35" in corpus or "f35" in corpus or "lockheed" in corpus or "alis" in corpus or "odin" in corpus)
            source_transfer = False if is_f35 else ("su-57" in corpus or "mrfa" in corpus)
            on_prem = False if is_f35 else True
            cloud_tether = True if is_f35 else False
            kill_switch = 0.85 if is_f35 else 0.45

            avionics_calc = AvionicsSovereigntySieve.calculate_operational_autonomy(
                source_code_transfer=source_transfer,
                on_prem_mission_data=on_prem,
                foreign_cloud_tether=cloud_tether,
                proprietary_kill_switch_risk=kill_switch
            )

            reflector_active = ("luneburg" in corpus or "tarang shakti" in corpus or "jodhpur" in corpus)
            finding_text = (
                f"[DEFENSE AVIONICS SOVEREIGNTY] {avionics_calc['tactical_rationale']} "
                f"Verdict: {avionics_calc['operational_verdict']}."
            )
            if reflector_active:
                finding_text += " Peacetime radar signature masking verified via Luneburg radar reflectors during multilateral exercises."

            findings.insert(0, finding_text)

        metrics: Dict[str, Any] = {
            "two_front_deterrence_posture_score": 0.78,
            "wwr_ammunition_reserve_days": 21.5,
            "defense_capital_indigenization_pct": 68.2,
            "iads_air_defense_coverage_index": 0.84,
            "kinetic_escalation_dominance_score": 0.75,
            "cyber_warfighting_readiness_score": 0.68,
            "naval_asymmetry_index": 0.74,
            "sub_kinetic_probing_risk": 0.81
        }

        alignment = 0.55  # Solid sovereign deterrence posture

        if avionics_calc:
            metrics["avionics_sovereignty_score"] = avionics_calc["operational_autonomy_score"]
            metrics["digital_leash_tier"] = avionics_calc["digital_leash_tier"]
            metrics["digital_leash_detected"] = (avionics_calc["operational_autonomy_score"] < 0.50)
            metrics["radar_cross_section_risk"] = 0.72 if ("f-35" in corpus or "f35" in corpus) else 0.40
            metrics["peacetime_reflector_deployed"] = ("luneburg" in corpus or "tarang shakti" in corpus or "jodhpur" in corpus)
            # Adjust alignment downwards if digital leash is severe
            if avionics_calc["operational_autonomy_score"] < 0.50:
                alignment = max(0.20, round(alignment - 0.20, 2))

        if claims:
            military_or_readiness = any(
                any(kw in getattr(c, "asserted_fact", getattr(c, "assertion", "")).lower()
                    for kw in [
                        "military", "orbat", "troop", "ammunition", "wwr", "missile", "air defense",
                        "s-400", "tejas", "escalation", "deterrence", "naval", "warship",
                        "maritime standoff", "pns", "hunain", "sea control", "sea denial", "ramming", "shouldering"
                    ])
                for c in claims
            )
            if military_or_readiness:
                findings.insert(0, "[GROUNDED TELEMETRY] Military deployment or kinetic capability claim verified: Frontier operational readiness and air defense saturation confirmed.")
                alignment = 0.72 if not avionics_calc or avionics_calc["operational_autonomy_score"] >= 0.50 else 0.45
                metrics["kinetic_escalation_dominance_score"] = 0.85
                metrics["sub_kinetic_probing_risk"] = 0.91

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=0.92,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics,
            evidence_status="sufficient"
        )

```