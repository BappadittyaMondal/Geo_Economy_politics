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
