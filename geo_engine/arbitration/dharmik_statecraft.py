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
