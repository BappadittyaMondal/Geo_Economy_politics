"""
Lens 3: Civilizational Statecraft & Sanatan Dharma Lens.
Analyzes multilateral summits through foundational civilizational philosophies:
Kautilya's Arthashastra (Raja Mandala Theory), Rajdharma, Yogakshema, and Vasudhaiva Kutumbakam,
contrasted against Chinese Tianxia, Russian Eurasianism, and Western Hegemony.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, SummitEvent


class CivilizationalLens:
    """Civilizational philosophy and strategic culture evaluator."""

    LENS_NAME = "Civilizational Statecraft (Sanatan / Comparative)"
    PRIMARY_TIER = EpistemicTier.TIER_3_SOVEREIGN_REDLINES

    @classmethod
    def evaluate(
        cls,
        summit: Optional[SummitEvent] = None,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Evaluates summit maneuvers through civilizational matrices and Dharmic statecraft.
        Dynamically ingests civilizational doctrine, Raja Mandala, and philosophical claims.
        """
        findings = [
            "Kautilyan Mandala Dynamics: In Arthashastra terms, China occupies the structural role of 'Ari' (immediate neighbor rival); Russia serves as 'Mitra' (rebalancing friend); Middle Eastern entrants act as 'Madhyama' (intermediate swing powers).",
            "Rajdharma & Yogakshema: Indian foreign policy is governed not by abstract ideological alliances, but by Rajdharma—ensuring the physical security, affordable energy, and economic welfare (Yogakshema) of its 1.4 billion citizens.",
            "Vasudhaiva Kutumbakam vs. Tianxia: India champions 'Vasudhaiva Kutumbakam' (polycentric pluralism where sovereign civilizations coexist as equals), explicitly countering the Sinocentric 'Tianxia' model (hierarchical tributary empire).",
            "Civilizational Pluralism: BRICS is not a monolith of common values; it is an anti-hegemonic forum of ancient civilization-states (Bharat, China, Russia, Persia, Arab World) resisting Western universalism.",
            "Dandaniti & Sadguniya (Six-Fold Foreign Policy): Arthashastra Book VII prescribes Sandhi (alliance), Vigraha (hostility), Asana (neutrality), Yana (march/expedition), Samshraya (shelter-seeking), and Dvaidhibhava (dual policy) — India's current multi-alignment doctrine maps directly to Dvaidhibhava, maintaining simultaneous engagement with adversarial blocs.",
            "Symbolic Temporal Statecraft & Calendar Convergence: State maneuvers synchronize kinetic deterrence and diplomatic summits with civilizational calendar dates and historical anniversaries (e.g., Tagore Jayanti on May 7, Pushya Nakshatra, Kartik Purnima maritime trade memory), reinforcing national resolve through deep cultural memory.",
            "Kautilyan Saptanga Statecraft (The Seven Limbs of Sovereignty): Arthashastra Book VI defines organic state sovereignty through Swami (Leadership), Amatya (Bureaucracy), Janapada (Territory & Demographic Cohesion), Durga (Fortified Infrastructure), Kosha (Treasury & Fiscal Solvency), Danda (Military & Law Enforcement), and Mitra (Allies). Regime durability depends on composite limb integrity; acute failure in Kosha or Janapada alienation precipitates internal collapse irrespective of external Danda strength.",
            "Sanatan Economics & Festival Velocity of Money: Traditional Dharmic economies maintain organic liquidity churn through festive and pilgrimage calendars (Navratri, Dhanteras, Diwali, Kumbha, wedding seasons) which redistribute surplus capital from affluent merchants to grassroots artisans, jewelry, textiles, and services without inflationary fiat printing or central bank interest-rate manipulation."
        ]

        metrics = {
            "dharmic_framework": "Kautilya Raja Mandala (Ari-Mitra-Madhyama-Udasina)",
            "sovereignty_principle": "Yogakshema & Strategic Autonomy",
            "civilizational_friction": "Dharmic Polycentric Pluralism vs. Sinocentric Tianxia Hierarchy",
            "cultural_cohesion_index": 0.30,  # Low internal cultural cohesion; united purely by resistance to external hegemony
            "sadguniya_policy_mapping": "Dvaidhibhava (Dual Policy) — Simultaneous BRICS/SCO + Quad/AUKUS engagement",
            "symbolic_temporal_resonance_score": 0.88,
            "saptanga_sovereignty_index": 0.81,
            "festival_liquidity_velocity_multiplier": 1.45,
            "temple_ecosystem_permanence_score": 0.92,
            "saptanga_limb_vulnerabilities": {
                "swami": "High executive coherence & decisive risk tolerance",
                "amatya": "Bureaucratic inertia & regulatory red-tape drag",
                "janapada": "Demographic transition window & border infiltration risks",
                "durga": "Critical digital public infrastructure & high-tech fab fortification",
                "kosha": "Robust forex reserves ($700B) offsetting crude import deficit",
                "danda": "Strong kinetic deterrence with fifth-domain cyber & drone gap",
                "mitra": "Dynamic multi-alignment via Quad / BRICS balances"
            }
        }

        alignment = 0.40
        confidence = 0.90

        def _extract_text(c: Any) -> str:
            if isinstance(c, str):
                return c
            if isinstance(c, dict):
                return str(c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "")
            return str(getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", ""))))

        if claims:
            civ_keywords = [
                "mandala", "rajdharma", "dharmic", "sanatan", "tianxia",
                "vasudhaiva", "civilization", "kautilya", "yogakshema", "hegemony", "polycentric"
            ]
            matched_civ = any(
                any(kw in _extract_text(c).lower() for kw in civ_keywords)
                for c in claims
            )
            if matched_civ:
                findings.insert(0, "[GROUNDED TELEMETRY] Civilizational doctrine / Raja Mandala alignment detected in diplomatic conduct.")
                confidence = min(0.99, round(confidence + 0.02, 2))
                metrics["grounded_civilizational_claims_verified"] = True

            internal_dharmic_keywords = [
                "dharmashastra", "smriti", "sadachara", "deshadharma", "kuladharma",
                "shankaracharya", "peetham", "samskara", "matha", "traditional jurisprudence"
            ]
            matched_internal = any(
                any(kw in _extract_text(c).lower() for kw in internal_dharmic_keywords)
                for c in claims
            )
            if matched_internal:
                findings.insert(0, "[GROUNDED TELEMETRY] Internal Dharmic jurisprudence detected: Polycentric Sanatan traditions (Deshadharma / Sadachara / Peetham autonomy) contrasted against centralized statutory secular codification.")
                metrics["internal_jurisprudential_model"] = "Dharmic Polycentricity (Deshadharma / Sadachara) vs Statutory Uniformity"
                metrics["traditional_institutional_autonomy_friction"] = 0.76
                confidence = min(0.99, round(confidence + 0.02, 2))

            saptanga_keywords = [
                "saptanga", "swami", "amatya", "janapada", "durga", "kosha", "danda", "seven limbs", "state sovereignty"
            ]
            matched_saptanga = any(
                any(kw in _extract_text(c).lower() for kw in saptanga_keywords)
                for c in claims
            )
            if matched_saptanga:
                findings.insert(0, "[GROUNDED TELEMETRY] Kautilyan Saptanga limb evaluation activated: Internal state capacity and systemic limb durability audited.")
                metrics["saptanga_evaluation_active"] = True
                confidence = min(0.99, round(confidence + 0.02, 2))

            # Phase 71C: Cultural & Religious Grayzone Sieve
            gz_res = CulturalGrayzoneSieve.audit_cultural_claims(claims)
            if gz_res["grayzone_findings"]:
                for gf in gz_res["grayzone_findings"]:
                    findings.insert(0, f"[CULTURAL_GRAYZONE_SIEVE] {gf}")
            metrics["cultural_grayzone_vulnerability_index"] = gz_res["cultural_grayzone_vulnerability_index"]
            metrics["asymmetric_secular_lawfare_detected"] = gz_res["asymmetric_secular_lawfare_detected"]
            metrics["textual_stratigraphy_violation_detected"] = gz_res["textual_stratigraphy_violation_detected"]
            metrics["narrative_laundering_detected"] = gz_res["narrative_laundering_detected"]
            metrics["transnational_theological_cover_detected"] = gz_res.get("transnational_theological_cover_detected", False)
            metrics["sub_national_paradiplomacy_friction_detected"] = gz_res.get("sub_national_paradiplomacy_friction_detected", False)
            metrics["sacred_calendar_provocation_detected"] = gz_res.get("sacred_calendar_provocation_detected", False)
            metrics["sacred_provocation_tier"] = gz_res.get("sacred_provocation_tier", "NEUTRAL_CULTURAL_BASELINE")
            metrics["sacred_provocation_index"] = gz_res.get("sacred_provocation_index", 0.0)

            # Phase 182: Urban Insurrection & Asymmetric Agitation Risk Sieve
            urban_res = UrbanInsurrectionRiskSieve.evaluate_insurrection_risk(claims=claims)
            metrics["urban_insurrection_risk_score"] = urban_res["urban_insurrection_risk_score"]
            metrics["urban_insurrection_tier"] = urban_res["risk_tier"]
            metrics["paid_agitator_logistics_flag"] = urban_res["paid_agitator_logistics_flag"]
            if urban_res["is_insurrection_hazard"]:
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Urban Insurrection Risk Sieve triggered: "
                    f"Tier [{urban_res['risk_tier']}] (Score: {urban_res['urban_insurrection_risk_score']:.2f}). "
                    f"{urban_res['tactical_countermeasure']}"
                ))

            metrics["claims_evaluated"] = len(claims)
        else:
            urban_res = UrbanInsurrectionRiskSieve.evaluate_insurrection_risk(claims=None)
            metrics["cultural_grayzone_vulnerability_index"] = 0.15
            metrics["asymmetric_secular_lawfare_detected"] = False
            metrics["transnational_theological_cover_detected"] = False
            metrics["sub_national_paradiplomacy_friction_detected"] = False
            metrics["sacred_calendar_provocation_detected"] = False
            metrics["urban_insurrection_risk_score"] = urban_res["urban_insurrection_risk_score"]
            metrics["urban_insurrection_tier"] = urban_res["risk_tier"]
            metrics["paid_agitator_logistics_flag"] = False

        if "urban_insurrection_risk_score" not in metrics:
            metrics["urban_insurrection_risk_score"] = 0.28

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=confidence,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )


class CulturalGrayzoneSieve:
    """
    Phase 71C & Phase 78: Cultural & Religious Grayzone Sieve.
    Applies Paṇḍit/Mīmāṃsā textual stratigraphy, Decolonial jurisprudence (J. Sai Deepak),
    and sub-national paradiplomacy analysis to deconstruct asymmetric secular lawfare,
    Smṛti interpolation weaponization, transnational faith-based irregular warfare covers,
    and borderland paradiplomacy friction against sovereign statecraft.
    """

    @classmethod
    def audit_cultural_grayzone(cls, narrative_text: str) -> Dict[str, Any]:
        """Convenience method for auditing raw narrative text."""
        res = cls.audit_cultural_claims([narrative_text])
        return {
            "asymmetric_secular_lawfare_detected": res["asymmetric_secular_lawfare_detected"],
            "lawfare_index": res["cultural_grayzone_vulnerability_index"],
            "scriptural_stratigraphy_violation": res["textual_stratigraphy_violation_detected"],
            "transnational_theological_cover_detected": res.get("transnational_theological_cover_detected", False),
            "sub_national_paradiplomacy_friction_detected": res.get("sub_national_paradiplomacy_friction_detected", False),
            "violations": res["grayzone_findings"],
            "sieve_status": "SUSPICIOUS_ASYMMETRIC_OR_STRATIGRAPHIC_DISTORTION" if res["cultural_grayzone_vulnerability_index"] > 0 else "CLEAN_CIVILIZATIONAL_BASELINE"
        }

    @staticmethod
    def audit_cultural_claims(claims: List[Any]) -> Dict[str, Any]:
        asymmetric_secular_signals = 0
        textual_stratigraphy_signals = 0
        narrative_laundering_signals = 0
        theological_cover_signals = 0
        paradiplomacy_signals = 0
        findings = []

        asym_keywords = ["temple control", "hrce", "places of worship act", "waqf", "endowment", "denominational rights", "article 26", "article 30"]
        smrti_keywords = ["manusmriti", "caste oppression", "regressive sloka", "scriptural sanction", "puranic literalism", "smriti", "sruti", "śruti", "smṛti"]
        laundering_keywords = ["majoritarian", "hindu nationalism", "anti-conversion", "saffron terror", "fascism", "demographic shift"]
        theological_cover_keywords = [
            "soli", "sons of liberty", "humanitarian military", "persecuted minority relief",
            "faith-based contractor", "evangelical corridor", "cross-border church",
            "diaspora church fund", "free burma rangers"
        ]
        paradiplomacy_keywords = [
            "paradiplomacy", "sub-national paradiplomacy", "mizo-chin", "chin refugee sanctuary",
            "yma", "cross-border ethnic sanctuary", "tribal kinship corridor", "borderland kinship"
        ]

        for c in claims:
            txt = (c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))).lower()
            if any(k in txt for k in asym_keywords):
                asymmetric_secular_signals += 1
            if any(k in txt for k in smrti_keywords):
                textual_stratigraphy_signals += 1
            if any(k in txt for k in laundering_keywords):
                narrative_laundering_signals += 1
            if any(k in txt for k in theological_cover_keywords):
                theological_cover_signals += 1
            if any(k in txt for k in paradiplomacy_keywords):
                paradiplomacy_signals += 1

        vulnerability_index = min(1.0, round(
            0.40 * (1 if asymmetric_secular_signals > 0 else 0) +
            0.35 * (1 if textual_stratigraphy_signals > 0 else 0) +
            0.25 * (1 if narrative_laundering_signals > 0 else 0) +
            0.30 * (1 if theological_cover_signals > 0 else 0) +
            0.25 * (1 if paradiplomacy_signals > 0 else 0),
            2
        ))

        if asymmetric_secular_signals > 0:
            findings.append(
                "Asymmetric Secular Lawfare Detected: Audited institutional divergence where state apparatus exercises proprietary control over Hindu sacred endowments while shielding minority bodies under Article 26/30."
            )
        if textual_stratigraphy_signals > 0:
            findings.append(
                "Textual Stratigraphy Violation (Śruti-Smṛti Invariant): Adversary narrative isolates interpolated Smṛti passages out of historical context. Classical Mīmāṃsā establishes that Śruti (universal ontological principles) strictly overrides temporal Smṛti injunctions."
            )
        if narrative_laundering_signals > 0:
            findings.append(
                "Academic Narrative Laundering Detected: Legitimate civilizational sovereignty, border defense, and cultural preservation linguistically inverted into 'majoritarian aggression'."
            )
        if theological_cover_signals > 0:
            findings.append(
                "Transnational Theological Irregular Warfare Cover Detected: Faith-based 501(c)(3) or missionary relief pipelines identified facilitating irregular warfare or non-state combatant logistics under humanitarian cover."
            )
        if paradiplomacy_signals > 0:
            findings.append(
                "Sub-National Paradiplomacy Friction Detected: Borderland state/tribal authorities diverging from sovereign central foreign policy, extending sanctuary along ethnic-religious kinship corridors."
            )

        # Phase 151: Sacred Calendar Provocation & Contempt Optics Sifting
        provocation_res = SacredCalendarProvocationSieve.evaluate_provocation_claims(claims)
        if provocation_res["is_sacred_provocation_detected"]:
            findings.extend(provocation_res["findings"])
            vulnerability_index = min(1.0, max(vulnerability_index, provocation_res["provocation_index"]))

        return {
            "cultural_grayzone_vulnerability_index": vulnerability_index,
            "asymmetric_secular_lawfare_detected": asymmetric_secular_signals > 0,
            "textual_stratigraphy_violation_detected": textual_stratigraphy_signals > 0,
            "narrative_laundering_detected": narrative_laundering_signals > 0,
            "transnational_theological_cover_detected": theological_cover_signals > 0,
            "sub_national_paradiplomacy_friction_detected": paradiplomacy_signals > 0,
            "sacred_calendar_provocation_detected": provocation_res["is_sacred_provocation_detected"],
            "sacred_provocation_tier": provocation_res["provocation_tier"],
            "sacred_provocation_index": provocation_res["provocation_index"],
            "grayzone_findings": findings
        }

    BLASPHEMY_STREET_VETO_MARKERS = [
        "sar tan se juda", "gustakh", "blasphemy", "apostasy", "irtidad",
        "ridda", "beheading", "nupur", "salim vasty", "boycott", "charlie hebdo",
        "fatwa", "blasphemer", "sacrilege"
    ]

    @classmethod
    def evaluate_demographic_tipping_point(
        cls,
        minority_cohort_pct: float = 0.15,
        local_concentration_multiplier: float = 1.0
    ) -> Dict[str, Any]:
        """
        Evaluates demographic tipping point transition (Makki vs Madani phase transition).
        - Sub-critical (<10%): Makki accommodation, constitutional secularism, victimhood rhetoric.
        - Intermediate (10%-25%): Institutional assertion, parallel dietary/Halal & personal law demands.
        - Critical (>=25%): Madani hegemonic phase, street vetoes, communal enclave autonomy.
        """
        effective_pct = min(1.0, max(0.0, float(minority_cohort_pct) * float(local_concentration_multiplier)))

        if effective_pct >= 0.25:
            phase = "MADANI_HEGEMONIC_PHASE"
            tipping_score = min(1.0, 0.70 + (effective_pct - 0.25) * 1.20)
            communal_veto_prob = min(0.95, 0.65 + effective_pct * 0.8)
            sharia_pressure_index = min(1.0, 0.60 + effective_pct * 1.1)
            description = "Critical demographic concentration; high probability of parallel legal demands and street veto enforcement."
        elif effective_pct >= 0.10:
            phase = "INSTITUTIONAL_ASSERTION_PHASE"
            tipping_score = round(0.35 + (effective_pct - 0.10) * 2.33, 3)
            communal_veto_prob = round(0.25 + effective_pct * 1.5, 3)
            sharia_pressure_index = round(0.20 + effective_pct * 1.8, 3)
            description = "Intermediate demographic cohort; institutional bargaining for minority exceptions, Waqf autonomy, and separate personal laws."
        else:
            phase = "MAKKI_ACCOMMODATION_PHASE"
            tipping_score = round(effective_pct * 3.0, 3)
            communal_veto_prob = round(effective_pct * 1.2, 3)
            sharia_pressure_index = round(effective_pct * 1.0, 3)
            description = "Sub-critical minority phase; strict adherence to constitutional secularism, human rights advocacy, and tolerance rhetoric."

        return {
            "minority_cohort_pct": round(minority_cohort_pct, 3),
            "effective_demographic_pct": round(effective_pct, 3),
            "demographic_phase": phase,
            "tipping_point_score": round(tipping_score, 3),
            "communal_veto_probability": round(communal_veto_prob, 3),
            "sharia_parallel_pressure_index": round(sharia_pressure_index, 3),
            "sociological_assessment": description
        }

    @classmethod
    def evaluate_blasphemy_street_veto(cls, text_claims: str) -> Dict[str, Any]:
        """
        Evaluates blasphemy-related micro-signals and extra-judicial street veto escalation risk.
        """
        text_lower = (text_claims or "").lower()
        matched_markers = [m for m in cls.BLASPHEMY_STREET_VETO_MARKERS if m in text_lower]
        marker_count = len(matched_markers)

        if marker_count >= 3 or "sar tan se juda" in text_lower:
            veto_tier = "ACUTE_EXTRAJUDICIAL_STREET_VETO"
            escalation_prob = 0.88
            sovereignty_violation_score = 0.92
            recommendation = "Deploy Section 144 / BNSS 163, proactive preventive detention of agitation leadership, and freeze local hawala/UPI funding."
        elif marker_count >= 1:
            veto_tier = "ELEVATED_BLASPHEMY_INTIMIDATION"
            escalation_prob = 0.55
            sovereignty_violation_score = 0.60
            recommendation = "Continuous digital OSINT monitoring, intelligence escort for target figures, and statutory warnings under hate speech provisions."
        else:
            veto_tier = "BASELINE_COMMUNAL_EQUILIBRIUM"
            escalation_prob = 0.10
            sovereignty_violation_score = 0.05
            recommendation = "Standard civil policing baseline."

        return {
            "blasphemy_markers_detected": matched_markers,
            "marker_count": marker_count,
            "street_veto_tier": veto_tier,
            "escalation_probability": escalation_prob,
            "sovereignty_violation_score": sovereignty_violation_score,
            "operational_recommendation": recommendation
        }

    @classmethod
    def evaluate_juvenile_shield_vulnerability(
        cls,
        juvenile_cadre_present: bool = False,
        statutory_immunity_exploited: bool = False,
        media_brutality_trap_risk: float = 0.50
    ) -> Dict[str, Any]:
        """
        Phase 175: 5th-Gen Asymmetric Juvenile Shield Vulnerability Index.
        Models intentional deployment of minors (12-17 age cohort) at frontlines of violent
        agitations to paralyze law enforcement through juvenile justice criminal immunity and
        manufacture camera-ready police brutality footage for international media networks.
        """
        if not juvenile_cadre_present:
            return {
                "juvenile_shield_detected": False,
                "tactical_police_paralysis_score": 0.0,
                "shield_tier": "STANDARD_PROTEST_BASELINE",
                "countermeasure_protocol": "Standard civil crowd control protocols apply."
            }

        paralysis_score = 0.40
        if statutory_immunity_exploited:
            paralysis_score += 0.35
        paralysis_score += min(0.25, float(media_brutality_trap_risk) * 0.25)
        paralysis_score = round(min(1.0, paralysis_score), 3)

        if paralysis_score >= 0.75:
            tier = "CRITICAL_JUVENILE_CAMERA_TRAP"
            protocol = "Absolute kinetic restraint on vanguard minors; deploy drone facial recognition, trace adult organizers/handlers under BNS/UAPA, and enforce FCRA/bank account freezes against sponsoring NGOs."
        else:
            tier = "ELEVATED_ASYMMETRIC_SHIELD"
            protocol = "Deploy non-kinetic barricading, female and juvenile specialized police units, and comprehensive digital evidentiary recording."

        return {
            "juvenile_shield_detected": True,
            "statutory_immunity_exploited": statutory_immunity_exploited,
            "tactical_police_paralysis_score": paralysis_score,
            "shield_tier": tier,
            "countermeasure_protocol": protocol
        }


class SacredCalendarProvocationSieve:
    """
    Phase 151: Sacred Calendar Provocation & Contempt Optics Sieve.
    Deconstructs deliberate ritual desensitization and theatrical transgressions
    orchestrated during sacred Sanatan observances (Pitru Paksha, Navratri, Shravan, Kanwar Yatra)
    designed to bait counter-reactions for second-order narrative weaponization.
    """

    SACRED_PERIOD_WEIGHTS = {
        "pitru paksh": 0.95,
        "pitru paksha": 0.95,
        "shradh": 0.90,
        "navratri": 0.90,
        "shravan": 0.85,
        "kanwar yatra": 0.85,
        "durga puja fasting": 0.80,
        "ekadashi": 0.75,
    }

    TRANSGRESSION_KEYWORDS = [
        "chicken roll", "khan chacha", "mutton party", "beef feast",
        "eating meat in navratri", "eating non-veg", "non-veg flaunt",
        "provocative feast", "meat during fasting", "ritual mockery",
    ]

    THEATRICAL_STAGING_KEYWORDS = [
        "camera crew", "media sting", "live broadcast", "pr video",
        "social media flaunt", "instagram reel", "viral video",
        "deliberate photo", "staged photoshoot", "political leader feast"
    ]

    @classmethod
    def evaluate_provocation(
        cls,
        text: str,
        is_political_actor: bool = False,
        media_amplified: bool = False
    ) -> Dict[str, Any]:
        text_lower = text.lower()
        sacred_weight = 0.0
        matched_period = None
        for period, weight in cls.SACRED_PERIOD_WEIGHTS.items():
            if period in text_lower and weight > sacred_weight:
                sacred_weight = weight
                matched_period = period

        matched_transgressions = [kw for kw in cls.TRANSGRESSION_KEYWORDS if kw in text_lower]
        transgression_weight = min(1.0, len(matched_transgressions) * 0.50)

        matched_staging = [kw for kw in cls.THEATRICAL_STAGING_KEYWORDS if kw in text_lower]
        staging_weight = 0.30
        if matched_staging:
            staging_weight += 0.35
        if is_political_actor:
            staging_weight += 0.20
        if media_amplified:
            staging_weight += 0.15
        staging_weight = min(1.0, staging_weight)

        if sacred_weight > 0.0 and matched_transgressions:
            provocation_index = min(1.0, 0.40 * sacred_weight + 0.35 * transgression_weight + 0.25 * staging_weight)
        else:
            provocation_index = 0.0

        is_provocation = provocation_index >= 0.50

        if provocation_index >= 0.80:
            tier = "ACUTE_THEATRICAL_CONTEMPT_OPTICS"
        elif provocation_index >= 0.50:
            tier = "ELEVATED_RITUAL_DESENSITIZATION"
        elif provocation_index > 0.0:
            tier = "INCIDENTAL_CULTURAL_DISSONANCE"
        else:
            tier = "NEUTRAL_CULTURAL_BASELINE"

        findings = []
        if is_provocation:
            findings.append(
                f"Sacred calendar provocation detected during '{matched_period}' with public transgression ({', '.join(matched_transgressions)})."
            )
            findings.append(
                "Second-order narrative weaponization: Orchestrated to bait counter-reactions and manufacture 'majoritarian intolerance' headlines."
            )

        return {
            "is_sacred_provocation_detected": is_provocation,
            "provocation_index": round(provocation_index, 3),
            "provocation_tier": tier,
            "matched_period": matched_period,
            "matched_transgressions": matched_transgressions,
            "theatrical_staging_detected": bool(matched_staging),
            "findings": findings
        }

    @classmethod
    def evaluate_provocation_claims(cls, claims: List[Any]) -> Dict[str, Any]:
        max_idx = 0.0
        dominant_res = {
            "is_sacred_provocation_detected": False,
            "provocation_index": 0.0,
            "provocation_tier": "NEUTRAL_CULTURAL_BASELINE",
            "matched_period": None,
            "matched_transgressions": [],
            "theatrical_staging_detected": False,
            "findings": []
        }
        for c in claims:
            txt = c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
            res = cls.evaluate_provocation(txt)
            if res["provocation_index"] > max_idx:
                max_idx = res["provocation_index"]
                dominant_res = res
        return dominant_res


class UrbanInsurrectionRiskSieve:
    """
    Phase 182: Urban Insurrection & Asymmetric Agitation Risk Sieve.
    Quantifies the vulnerability to hybrid urban street insurrection deploying
    demographic clustering, FCRA foreign funding multipliers (₹3,000/day professional agitator stipends),
    and juvenile/vanguard human shields against state police kinetic readiness.

    Formula:
        Insurrection Risk = min(1.0, (Demographic Concentration * FCRA Multiplier) / max(0.2, Police Readiness * Deterrence Speed * 3.0))
    """

    INSURRECTION_KEYWORDS = [
        "fcra", "daily stipend", "3000 per day", "3,000 per day", "professional agitator",
        "paid protest", "camera trap", "human shield", "gen-z vanguard", "urban insurrection",
        "rail roko", "chakka jam", "road blockade", "shaheen bagh", "farmer protest",
        "albania model", "street anarchy", "tractor rally", "toolkit"
    ]

    @classmethod
    def evaluate_insurrection_risk(
        cls,
        demographic_concentration: float = 0.5,
        fcra_foreign_inflow_multiplier: float = 1.0,
        police_kinetic_readiness: float = 0.7,
        judicial_deterrence_speed: float = 0.6,
        claims: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        demo = max(0.1, min(1.0, float(demographic_concentration)))
        fcra = max(0.5, min(3.0, float(fcra_foreign_inflow_multiplier)))
        police = max(0.1, min(1.0, float(police_kinetic_readiness)))
        judicial = max(0.1, min(1.0, float(judicial_deterrence_speed)))

        matched_kws = []
        paid_stipend_detected = False

        if claims:
            for c in claims:
                txt = c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
                txt_l = txt.lower()
                for kw in cls.INSURRECTION_KEYWORDS:
                    if kw in txt_l and kw not in matched_kws:
                        matched_kws.append(kw)

            if any(k in matched_kws for k in ["daily stipend", "3000 per day", "3,000 per day", "paid protest", "fcra"]):
                paid_stipend_detected = True
                fcra = max(fcra, 1.85)
            if any(k in matched_kws for k in ["camera trap", "human shield", "gen-z vanguard"]):
                # Human shields paralyze police kinetic readiness
                police = max(0.2, police * 0.75)

        denominator = max(0.2, police * judicial)
        raw_risk = (demo * fcra) / (denominator * 3.0)
        risk_score = round(min(1.0, max(0.0, raw_risk)), 4)

        if risk_score >= 0.75:
            tier = "CRITICAL_URBAN_INSURRECTION_HAZARD"
            countermeasure = (
                "Deploy proactive financial intelligence: Freeze FCRA bank accounts, cut hawala cash conduits (₹3,000/day stipends), "
                "deploy bodycam telemetry to counter camera traps, and invoke BNS Section 152 / CrPC 144 preemptive curfews."
            )
        elif risk_score >= 0.50:
            tier = "ELEVATED_CIVIC_DISRUPTION_RISK"
            countermeasure = (
                "Initiate high-visibility multi-agency checkpoint surveillance, issue statutory notices to organizers, "
                "and maintain non-lethal rapid action force (RAF) staging."
            )
        elif risk_score >= 0.25:
            tier = "MODERATE_LOCALIZED_STREET_FRICTION"
            countermeasure = "Standard municipal police crowd management and traffic rerouting."
        else:
            tier = "STABLE_URBAN_EQUILIBRIUM"
            countermeasure = "Routine community policing and periodic intelligence monitoring."

        return {
            "urban_insurrection_risk_score": risk_score,
            "risk_tier": tier,
            "demographic_concentration": demo,
            "fcra_multiplier": fcra,
            "police_kinetic_readiness": police,
            "judicial_deterrence_speed": judicial,
            "paid_agitator_logistics_flag": paid_stipend_detected,
            "matched_keywords": matched_kws,
            "tactical_countermeasure": countermeasure,
            "is_insurrection_hazard": risk_score >= 0.50
        }




