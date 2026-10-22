"""
Lens 11: Digital Sovereignty, Compute & Telecommunications Stack Lens.
Evaluates technological independence, hardware supply chains, telecom infrastructure,
subsea cable ownership, satellite constellations, and AI compute bottlenecks.
"""

from typing import Any, Dict, List, Optional
from ..core.models import EpistemicTier, LensEvaluation, SummitEvent


class DigitalSovereigntyLens:
    """Digital sovereignty, semiconductor compute, and communications infrastructure evaluator."""

    LENS_NAME = "Digital Sovereignty & Compute Infrastructure"
    PRIMARY_TIER = EpistemicTier.TIER_1_PHYSICAL

    @classmethod
    def evaluate(
        cls,
        summit: Optional[SummitEvent] = None,
        claims: Optional[List[Any]] = None
    ) -> LensEvaluation:
        """
        Assesses tech architecture decoupling, hardware choke points, and sovereign telecom grids.
        Dynamically incorporates semiconductor, telecom, and compute infrastructure claims.
        """
        findings = [
            "Telecom Stack Bifurcation: India enforces absolute exclusion of Chinese telecom vendors (Huawei, ZTE) from its 5G/6G core national infrastructure, directly contrasting with China's Digital Silk Road rollout across Africa and Central Asia.",
            "Semiconductor Compute Chokepoint: No BRICS member currently possesses leading-edge sub-5nm lithography fabrication capacity (ASML monopoly). The entire bloc remains structurally reliant on Western/Taiwanese foundry architecture for advanced AI training compute.",
            "Sovereign Satellite Constellations: Member states maintain independent, competing sovereign positioning systems (India's NavIC, China's BeiDou, Russia's GLONASS), limiting deep military-grade satellite interoperability.",
            "Data Localization Mandates: Strict national data protection laws (India's DPDP Act, China's Data Security Law) preclude the creation of unified, open cross-border data or cloud sharing protocols."
        ]

        # Phase 181: Tech Sovereignty & Spectrum Allocation Sieve
        tech_sieve = TechSovereigntySieve.evaluate_tech_sovereignty(claims=claims)

        # Phase 186: Imperial Subversion Pipes Sieve (The Two Imperial Pipes)
        pipes_sieve = ImperialSubversionPipesSieve.evaluate_imperial_pipes(claims=claims)

        # Phase 188: Protocol Layer Sovereignty Sieve (DPI vs China's Clone Trap)
        protocol_sieve = ProtocolLayerSovereigntySieve.evaluate_protocol_sovereignty(claims=claims)

        # Phase 195: Corporate Astroturfing & Subsidized Agitation Sieve
        astroturf_sieve = CorporateAstroturfingSieve.evaluate_astroturfing(claims=claims)

        metrics = {
            "advanced_silicon_autonomy_pct": 12.0, # Bloc self-sufficiency in advanced compute
            "telecom_infrastructure_cleavage": "Absolute (India Trusted Telecom Portal blocks Chinese hardware)",
            "satellite_interoperability_index": 0.35, # Limited civilian cross-referencing only
            "data_border_walls": "Impenetrable sovereign firewalls",
            "tech_sovereignty_score": tech_sieve["tech_sovereignty_score"],
            "spectrum_auction_protection_ratio": tech_sieve["spectrum_auction_protection_ratio"],
            "domestic_capex_insulation_score": tech_sieve["domestic_capex_insulation_score"],
            "foreign_constellation_penetration_pct": tech_sieve["foreign_constellation_penetration_pct"],
            "tech_sovereignty_tier": tech_sieve["tech_sovereignty_tier"],
            "tech_operational_verdict": tech_sieve["operational_verdict"],
            "telecom_pipes_risk_score": pipes_sieve["pipes_risk_score"],
            "telecom_pipes_risk_tier": pipes_sieve["pipes_risk_tier"],
            "telecom_shield_factor": pipes_sieve["domestic_telecom_shield_factor"],
            "protocol_layer_sovereignty_score": protocol_sieve["protocol_sovereignty_score"],
            "protocol_sovereignty_tier": protocol_sieve["protocol_sovereignty_tier"],
            "isa_hardware_autonomy": protocol_sieve["isa_hardware_autonomy"],
            "os_hardening_score": protocol_sieve["os_hardening_score"],
            "transaction_rails_openness": protocol_sieve["transaction_rails_openness"],
            "astroturfing_probability": astroturf_sieve["astroturfing_probability"],
            "astroturfing_tier": astroturf_sieve["astroturfing_tier"],
            "fcra_trace_probability": astroturf_sieve["fcra_trace_probability"],
            "is_astroturfing_detected": astroturf_sieve["is_astroturfing_detected"]
        }

        alignment = 0.22 # Very low multilateral tech integration; high sovereign competition
        confidence = 0.95

        if claims:
            tech_keywords = [
                "semiconductor", "compute", "gpu", "asml", "huawei", "5g", "6g",
                "telecom", "tsmc", "ai chips", "cloud", "subsea cable", "cyber", "chip", "lithography"
            ]
            matched_tech = any(
                any(kw in (c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))).lower() for kw in tech_keywords)
                for c in claims
            )
            if matched_tech:
                findings.insert(0, "[GROUNDED TELEMETRY] Digital stack sovereignty / semiconductor supply chain evidence detected.")
                confidence = min(0.99, round(confidence + 0.02, 2))
                metrics["grounded_digital_claims_verified"] = True

            if tech_sieve["matched_keywords"]:
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Tech Sovereignty & Spectrum Allocation Sieve triggered: "
                    f"Tier [{tech_sieve['tech_sovereignty_tier']}] (Score: {tech_sieve['tech_sovereignty_score']:.2f}). "
                    f"Verdict: {tech_sieve['operational_verdict']}. {tech_sieve['tactical_rationale']}"
                ))

            if pipes_sieve["matched_switch_keywords"] or pipes_sieve["matched_capital_keywords"]:
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Imperial Subversion Pipes Sieve triggered: "
                    f"Tier [{pipes_sieve['pipes_risk_tier']}] (Pipes Risk: {pipes_sieve['pipes_risk_score']:.4f}). "
                    f"Verdict: {pipes_sieve['operational_verdict']}. {pipes_sieve['tactical_rationale']}"
                ))

            if protocol_sieve["matched_keywords"]:
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Protocol-Layer Digital Sovereignty Sieve triggered: "
                    f"Tier [{protocol_sieve['protocol_sovereignty_tier']}] (Score: {protocol_sieve['protocol_sovereignty_score']:.4f}). "
                    f"Verdict: {protocol_sieve['operational_verdict']}. {protocol_sieve['tactical_rationale']}"
                ))

            if astroturf_sieve["is_astroturfing_detected"] or astroturf_sieve["matched_keywords"]:
                findings.insert(0, (
                    f"[GROUNDED TELEMETRY] Corporate Astroturfing Sieve triggered: "
                    f"Tier [{astroturf_sieve['astroturfing_tier']}] (Probability: {astroturf_sieve['astroturfing_probability']:.4f}). "
                    f"Verdict: {astroturf_sieve['operational_verdict']}. {astroturf_sieve['tactical_rationale']}"
                ))

            metrics["claims_evaluated"] = len(claims)

        return LensEvaluation(
            lens_name=cls.LENS_NAME,
            alignment_score=alignment,
            confidence=confidence,
            primary_epistemic_tier=cls.PRIMARY_TIER,
            key_findings=findings,
            hard_metrics=metrics
        )


class TechSovereigntySieve:
    """
    Phase 181: Tech Sovereignty & Spectrum Allocation Sieve.
    Evaluates regulatory vulnerability to foreign mega-constellations (e.g. Starlink),
    the erosion of domestic terrestrial telecom capex ($30B+), administrative vs competitive
    auction dynamics under the Telecommunications Act 2023, and sovereign lawful interception mandates.

    Formula:
        S_tech_sovereignty = min(1.0, max(0.0, 0.40 * A_protection + 0.35 * C_insulation + 0.25 * (1.0 - P_penetration)))
    """

    SPECTRUM_TECH_KEYWORDS = [
        "spectrum auction", "administrative spectrum", "telecom act 2023", "starlink",
        "satellite broadband", "satellite spectrum", "mega-constellation", "telecom capex",
        "data localization", "lawful interception", "terrestrial capex", "jio", "airtel",
        "ku-band", "ka-band", "gmpcs", "first schedule"
    ]

    @classmethod
    def evaluate_tech_sovereignty(
        cls,
        spectrum_auction_protection_ratio: float = 0.85,
        domestic_capex_insulation_score: float = 0.80,
        foreign_constellation_penetration_pct: float = 15.0,
        claims: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        prot = max(0.0, min(1.0, float(spectrum_auction_protection_ratio)))
        insul = max(0.0, min(1.0, float(domestic_capex_insulation_score)))
        pen_pct = max(0.0, min(100.0, float(foreign_constellation_penetration_pct)))
        pen_norm = pen_pct / 100.0

        matched_kws = []
        if claims:
            for c in claims:
                txt = c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
                txt_l = txt.lower()
                for kw in cls.SPECTRUM_TECH_KEYWORDS:
                    if kw in txt_l and kw not in matched_kws:
                        matched_kws.append(kw)

            if any(k in matched_kws for k in ["administrative spectrum", "starlink", "mega-constellation"]):
                # Administrative allocation lowers domestic auction protection ratio unless heavily conditioned
                prot = max(0.20, prot - 0.25)
                pen_norm = min(1.0, pen_norm + 0.20)
                pen_pct = round(pen_norm * 100.0, 1)

        sovereignty_score = round(min(1.0, max(0.0, 0.40 * prot + 0.35 * insul + 0.25 * (1.0 - pen_norm))), 4)

        if sovereignty_score >= 0.75:
            tier = "SOVEREIGN_TECH_FORTRESS"
            verdict = "DOMESTIC_CAPEX_SECURED"
            rationale = (
                "Robust technological sovereignty: Domestic telecom capex ($30B+) insulated by strict security vetting, "
                "mandatory in-country gateway landing stations, local cryptographic key escrow, and protected spectrum governance."
            )
        elif sovereignty_score >= 0.50:
            tier = "MANAGED_TECH_COMPETITION"
            verdict = "CONDITIONAL_MARKET_ACCESS"
            rationale = (
                "Managed competition: Administrative satcom licensing granted subject to strict national security clearance, "
                "telecom security guidelines (Trusted Telecom Portal), and localized data processing."
            )
        elif sovereignty_score >= 0.25:
            tier = "ELEVATED_FOREIGN_LEVERAGE"
            verdict = "VULNERABLE_DIGITAL_STACK"
            rationale = (
                "High dependency risk: Foreign low-Earth orbit mega-constellation unchecked penetration undermines domestic "
                "telecom network economics and bypasses conventional lawful interception safeguards."
            )
        else:
            tier = "CRITICAL_DIGITAL_CAPITULATION"
            verdict = "INFRASTRUCTURE_SOVEREIGNTY_LOST"
            rationale = "Critical communication infrastructure surrendered to extraterritorial private monopolies."

        return {
            "tech_sovereignty_score": sovereignty_score,
            "spectrum_auction_protection_ratio": prot,
            "domestic_capex_insulation_score": insul,
            "foreign_constellation_penetration_pct": pen_pct,
            "tech_sovereignty_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "matched_keywords": matched_kws,
            "is_tech_sovereignty_resilient": sovereignty_score >= 0.50
        }


class ImperialSubversionPipesSieve:
    """
    Phase 186: Imperial Subversion Pipes Sieve (The Two Imperial Pipes).
    Evaluates physical telecommunications switchboard/gateway sovereignty (Pipe 1)
    coupled with foreign capital inflow conduits / FCRA hawala pipelines (Pipe 2),
    incorporating the 1974 ITT Chile/India destabilization precedent and the
    2013 Snowden telemetry interception baseline.

    Formula:
        F_telecom = foreign_satcom_subsea_exposure
        F_capital = fcra_inflow_velocity_score
        S_shield = 0.50 * domestic_5g_core_readiness + 0.50 * sbi_statutory_audit_compliance
        PipesRisk = min(1.0, max(0.0, 0.45 * F_telecom + 0.40 * F_capital - 0.35 * S_shield + 0.20))
    """

    TELECOM_SWITCH_KEYWORDS = [
        "subsea cable", "cable landing station", "cls", "5g core", "ran", "open ran",
        "telco switch", "crossbar switch", "lawful interception", "calea", "telecom act 2023",
        "starlink", "kuiper", "oneweb", "satcom gateway", "satellite spectrum", "itt",
        "telecom monopoly", "eavesdropping", "telemetry leak", "prisms", "snowden"
    ]

    CAPITAL_CONDUIT_KEYWORDS = [
        "fcra", "sbi ndmb", "foreign contribution", "hawala", "soros", "open society",
        "regime change fund", "foreign funding", "ngo conduit", "shell ngo", "crypto off-ramp",
        "civil society grant", "fiat pipeline", "10 billion"
    ]

    @classmethod
    def evaluate_imperial_pipes(
        cls,
        foreign_satcom_subsea_exposure: float = 0.50,
        fcra_inflow_velocity_score: float = 0.50,
        domestic_5g_core_readiness: float = 0.70,
        sbi_statutory_audit_compliance: float = 0.85,
        claims: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        telecom_exp = max(0.0, min(1.0, float(foreign_satcom_subsea_exposure)))
        capital_exp = max(0.0, min(1.0, float(fcra_inflow_velocity_score)))
        core_readiness = max(0.0, min(1.0, float(domestic_5g_core_readiness)))
        sbi_compliance = max(0.0, min(1.0, float(sbi_statutory_audit_compliance)))

        matched_switch = []
        matched_capital = []

        if claims:
            for c in claims:
                txt = c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
                txt_l = txt.lower()
                for kw in cls.TELECOM_SWITCH_KEYWORDS:
                    if kw in txt_l and kw not in matched_switch:
                        matched_switch.append(kw)
                for kw in cls.CAPITAL_CONDUIT_KEYWORDS:
                    if kw in txt_l and kw not in matched_capital:
                        matched_capital.append(kw)

            if matched_switch:
                telecom_exp = min(1.0, max(telecom_exp, 0.40 + 0.12 * len(matched_switch)))
            if matched_capital:
                capital_exp = min(1.0, max(capital_exp, 0.40 + 0.12 * len(matched_capital)))
            if any(k in matched_switch for k in ["starlink", "satcom gateway", "satellite spectrum"]):
                # Bypass of terrestrial gateways elevates telecom exposure
                telecom_exp = min(1.0, telecom_exp + 0.15)
            if any(k in matched_capital for k in ["soros", "regime change fund", "10 billion"]):
                capital_exp = min(1.0, capital_exp + 0.20)

        shield_factor = round(0.50 * core_readiness + 0.50 * sbi_compliance, 4)
        raw_risk = 0.45 * telecom_exp + 0.40 * capital_exp - 0.35 * shield_factor + 0.20
        pipes_risk_score = round(min(1.0, max(0.0, raw_risk)), 4)

        if pipes_risk_score >= 0.75:
            tier = "CRITICAL_IMPERIAL_PIPES_EXPOSURE"
            verdict = "HIGH_RISK_SUBVERSION_VECTOR"
            rationale = (
                "Critical vulnerability across imperial regime-change pipes: Foreign satcom/subsea gateway dependency "
                "coupled with high-velocity non-governmental capital inflows. Replicates 1974 ITT Chile/India destabilization vector."
            )
        elif pipes_risk_score >= 0.50:
            tier = "ELEVATED_DUAL_PIPE_VULNERABILITY"
            verdict = "COORDINATED_PRESSURE_SURGE"
            rationale = (
                "Elevated dual-pipe exposure: Moderate telecom switchboard vulnerability and active external capital conduits. "
                "Requires mandatory SBI New Delhi Main Branch FCRA forensic reconciliation and satcom gateway localization."
            )
        elif pipes_risk_score >= 0.25:
            tier = "MODERATE_MANAGED_FRICTION"
            verdict = "STANDBY_INTERCEPTION_POSTURE"
            rationale = (
                "Managed risk posture: Domestic telecom networks secured by indigenously designed 5G core stacks and strict "
                "banking gateway reporting under amended FCRA statutory norms."
            )
        else:
            tier = "SOVEREIGN_DUAL_SHIELD_SECURED"
            verdict = "INFRASTRUCTURE_INSULATED"
            rationale = "Full physical and financial insulation: Sovereign telecom routing, local cryptographic key escrow, and sterile capital conduits."

        return {
            "pipes_risk_score": pipes_risk_score,
            "foreign_satcom_subsea_exposure": round(telecom_exp, 4),
            "fcra_inflow_velocity_score": round(capital_exp, 4),
            "domestic_telecom_shield_factor": shield_factor,
            "pipes_risk_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "matched_switch_keywords": matched_switch,
            "matched_capital_keywords": matched_capital,
            "is_dual_pipe_threat_active": pipes_risk_score >= 0.50
        }


class ProtocolLayerSovereigntySieve:
    """
    Phase 188: Protocol-Layer Digital Sovereignty Sieve.
    Evaluates full-stack architectural independence versus the 'Chinese Clone Trap'.
    Quantifies sovereign insulation across 5 non-negotiable protocol layers:
    1. Hardware & Instruction Set Architecture (DIRV Shakti/Vega RISC-V vs x86/ARM)
    2. Hardened Operating System (BharOS vs Google/Apple kill-switch telemetry)
    3. Open Transactional & Commerce Rails (UPI & ONDC vs Visa/Mastercard/Amazon 30% monopolies)
    4. Linguistic & AI Independence (Bhashini & IndiaAI GPU infrastructure vs Western training bias)
    5. Global Export Architecture (MOSIP / Aadhaar international adoption across Global South)

    Formula:
        S_protocol = 0.25 * S_isa + 0.20 * S_os + 0.25 * S_rails + 0.15 * S_ai + 0.15 * S_export
    """

    PROTOCOL_KEYWORDS = [
        "risc-v", "shakti", "vega", "dirv", "bharos", "upi", "ondc", "bhashini", "mosip",
        "dholera", "tata-psmc", "morigaon", "indiaai", "open protocol", "clone trap",
        "proprietary monopoly", "kill-switch", "android kill-switch", "operating system sovereignty"
    ]

    @classmethod
    def evaluate_protocol_sovereignty(
        cls,
        isa_hardware_autonomy: float = 0.60,
        os_hardening_score: float = 0.55,
        transaction_rails_openness: float = 0.95,
        linguistic_ai_sovereignty: float = 0.70,
        dpi_export_adoption_score: float = 0.80,
        claims: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        s_isa = max(0.0, min(1.0, float(isa_hardware_autonomy)))
        s_os = max(0.0, min(1.0, float(os_hardening_score)))
        s_rails = max(0.0, min(1.0, float(transaction_rails_openness)))
        s_ai = max(0.0, min(1.0, float(linguistic_ai_sovereignty)))
        s_export = max(0.0, min(1.0, float(dpi_export_adoption_score)))

        matched_kws = []
        if claims:
            for c in claims:
                txt = c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
                txt_l = txt.lower()
                for kw in cls.PROTOCOL_KEYWORDS:
                    if kw in txt_l and kw not in matched_kws:
                        matched_kws.append(kw)

            if any(k in matched_kws for k in ["shakti", "vega", "risc-v", "dirv"]):
                s_isa = min(1.0, s_isa + 0.15)
            if any(k in matched_kws for k in ["bharos", "operating system sovereignty"]):
                s_os = min(1.0, s_os + 0.20)
            if any(k in matched_kws for k in ["upi", "ondc", "open protocol"]):
                s_rails = min(1.0, s_rails + 0.05)
            if any(k in matched_kws for k in ["bhashini", "indiaai"]):
                s_ai = min(1.0, s_ai + 0.15)
            if any(k in matched_kws for k in ["mosip"]):
                s_export = min(1.0, s_export + 0.15)

        raw_score = 0.25 * s_isa + 0.20 * s_os + 0.25 * s_rails + 0.15 * s_ai + 0.15 * s_export
        sovereignty_score = round(min(1.0, max(0.0, raw_score)), 4)

        if sovereignty_score >= 0.80:
            tier = "SOVEREIGN_PROTOCOL_SUPERPOWER"
            verdict = "FULL_STACK_ARCHITECTURAL_AUTONOMY"
            rationale = (
                "Unassailable digital architecture: Bypassed the Chinese Clone Trap by building open public protocol rails "
                "(RISC-V Shakti, BharOS, UPI, ONDC, MOSIP). Foreign Big Tech operates strictly as regulated tenants on sovereign digital land."
            )
        elif sovereignty_score >= 0.60:
            tier = "ADVANCED_PROTOCOL_AUTONOMY"
            verdict = "DPI_RAILS_SECURED"
            rationale = (
                "High protocol autonomy: Financial transaction and identity rails fully sovereign (UPI/MOSIP); trailing-edge silicon "
                "fabrication scaling up. OS hardening (BharOS) deployed across sensitive defense and administrative nodes."
            )
        elif sovereignty_score >= 0.40:
            tier = "TRANSITIONAL_HYBRID_STACK"
            verdict = "SELECTIVE_PROTOCOL_EXPOSURE"
            rationale = (
                "Transitional vulnerability: Sovereign payment rails operational, but consumer smartphone endpoints remain reliant "
                "on foreign proprietary OS (Android/iOS) subject to extraterritorial remote kill-switches."
            )
        else:
            tier = "PROPRIETARY_DEPENDENCY_RISK"
            verdict = "DIGITAL_COLONIAL_STACK"
            rationale = "Severe architectural vulnerability: Critical computing, operating systems, and payment rails run on foreign proprietary silos."

        return {
            "protocol_sovereignty_score": sovereignty_score,
            "isa_hardware_autonomy": round(s_isa, 4),
            "os_hardening_score": round(s_os, 4),
            "transaction_rails_openness": round(s_rails, 4),
            "linguistic_ai_sovereignty": round(s_ai, 4),
            "dpi_export_adoption_score": round(s_export, 4),
            "protocol_sovereignty_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "matched_keywords": matched_kws,
            "is_protocol_autonomous": sovereignty_score >= 0.60
        }


class CorporateAstroturfingSieve:
    """
    Phase 195: Corporate Astroturfing & Subsidized Agitation Sieve.
    Quantifies the discrepancy between ground participant socioeconomic baselines
    and the physical/digital capitalization of the protest infrastructure.
    Synthesizes:
    - Daily logistical expenditure (luxury tentage, automated catering, generator banks, Starlink/Wi-Fi).
    - Participant median daily income baseline.
    - Foreign non-governmental capital inflow (FCRA) and corporate middleman cartels.

    Formula:
        SpendPerCapita = DailyLogisticalSpend / max(100, AttendeesCount)
        CapRatio = SpendPerCapita / max(50.0, ParticipantMedianDailyWage)
        z = 2.5 * (CapRatio - 0.50) + 1.8 * FCRASponsorshipProb + 1.5 * CorporateSubsidyFactor
        AstroturfingFactor = 1 / (1 + exp(-z))
    """

    ASTROTURFING_KEYWORDS = [
        "astroturf", "corporate funding", "luxury rv", "air conditioned tents", "mass catering",
        "foot massager", "sponsored protest", "middleman cartel", "unaccounted cash", "fcra subsidy",
        "synthetic consensus", "pr agency", "automated roti maker", "commercial agitation"
    ]

    @classmethod
    def evaluate_astroturfing(
        cls,
        daily_logistical_spend_inr: float = 250_000.0,
        attendees_count: float = 5_000.0,
        median_participant_daily_wage_inr: float = 350.0,
        foreign_fcra_sponsorship_prob: float = 0.25,
        corporate_middleman_subsidy_factor: float = 0.30,
        claims: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        import math
        spend = max(0.0, float(daily_logistical_spend_inr))
        attendees = max(1.0, float(attendees_count))
        wage = max(50.0, float(median_participant_daily_wage_inr))
        fcra_prob = max(0.0, min(1.0, float(foreign_fcra_sponsorship_prob)))
        corp_factor = max(0.0, min(1.0, float(corporate_middleman_subsidy_factor)))

        matched_kws = []
        if claims:
            for c in claims:
                txt = c if isinstance(c, str) else (c.get("asserted_fact") or c.get("raw_text") or c.get("assertion") or "") if isinstance(c, dict) else getattr(c, "asserted_fact", getattr(c, "raw_text", getattr(c, "assertion", "")))
                txt_l = txt.lower()
                for kw in cls.ASTROTURFING_KEYWORDS:
                    if kw in txt_l and kw not in matched_kws:
                        matched_kws.append(kw)

            if matched_kws:
                spend = max(spend, 1_500_000.0 + 500_000.0 * len(matched_kws))
                fcra_prob = min(1.0, fcra_prob + 0.15 * len(matched_kws))
                corp_factor = min(1.0, corp_factor + 0.15 * len(matched_kws))
            if any(k in matched_kws for k in ["air conditioned tents", "luxury rv", "automated roti maker", "foot massager"]):
                spend = max(spend, 5_000_000.0)
                fcra_prob = max(fcra_prob, 0.70)
                corp_factor = max(corp_factor, 0.75)

        spend_per_capita = spend / max(100.0, attendees)
        cap_ratio = spend_per_capita / wage

        z = 2.5 * (cap_ratio - 0.50) + 1.8 * fcra_prob + 1.5 * corp_factor
        astroturfing_prob = round(1.0 / (1.0 + math.exp(-z)), 4)

        if astroturfing_prob >= 0.75:
            tier = "HEAVILY_SUBSIDIZED_ASTROTURFING"
            verdict = "COMMERCIAL_CARTEL_OPERATION"
            rationale = (
                f"Severe astroturfing detected: Daily logistical capitalization (₹{spend:,.0f}/day, ₹{spend_per_capita:.1f}/head) "
                f"exceeds claimed agrarian participant income (CapRatio: {cap_ratio:.2f}x wage). High FCRA foreign conduit "
                f"and corporate middleman cartel subsidy probability ({fcra_prob*100:.1f}%)."
            )
        elif astroturfing_prob >= 0.50:
            tier = "HYBRID_SPONSORED_MOBILIZATION"
            verdict = "ORGANIZED_LOGISTICAL_BACKING"
            rationale = (
                f"Substantial external capitalization: Logistical support (₹{spend_per_capita:.1f}/head) reflects coordinated "
                f"institutional or cartel sponsorship layered atop localized grievances."
            )
        elif astroturfing_prob >= 0.25:
            tier = "MODERATE_COMMUNITY_SUPPORT"
            verdict = "LOCALIZED_MUTUAL_AID"
            rationale = "Protest logistics largely funded by community langar/donations within reasonable baseline boundaries."
        else:
            tier = "ORGANIC_GRASSROOTS_MOVEMENT"
            verdict = "AUTHENTIC_CITIZEN_GRIEVANCE"
            rationale = "Logistical footprint matches genuine voluntary contribution; zero foreign or corporate subsidization detected."

        return {
            "astroturfing_probability": astroturfing_prob,
            "daily_logistical_spend_inr": round(spend, 2),
            "spend_per_capita_inr": round(spend_per_capita, 2),
            "capitalization_ratio": round(cap_ratio, 4),
            "fcra_trace_probability": round(fcra_prob, 4),
            "corporate_subsidy_factor": round(corp_factor, 4),
            "astroturfing_tier": tier,
            "operational_verdict": verdict,
            "tactical_rationale": rationale,
            "matched_keywords": matched_kws,
            "is_astroturfing_detected": astroturfing_prob >= 0.50
        }




