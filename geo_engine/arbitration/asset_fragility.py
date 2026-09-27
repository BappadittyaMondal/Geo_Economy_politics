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
