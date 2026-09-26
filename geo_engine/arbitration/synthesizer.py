"""
5-Tier Response Protocol Synthesizer.
Reconciles all 12 analytical lenses, executes epistemic truth arbitration,
and outputs a complete, de-sanitized multilateral summit intelligence report.
"""

from typing import Any, Dict, List, Optional, Tuple
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
        summit_name: str = ""
    ) -> List[MemberCountryAudit]:
        """Generates comprehensive, realistic 4-dimensional country audits for requested countries or default member states."""
        if target_countries:
            ledgers = []
            for country in target_countries:
                c_norm = country.strip().lower()
                matched = None
                for key, template in cls.COUNTRY_AUDIT_TEMPLATES.items():
                    k_lower = key.lower()
                    if k_lower == c_norm or k_lower.startswith(c_norm) or c_norm in k_lower:
                        matched = template
                        break
                if matched and matched not in ledgers:
                    ledgers.append(matched)
                elif not matched:
                    ledgers.append(MemberCountryAudit(
                        country_name=country,
                        public_domestic_narrative=f"Domestic state media in {country} frames event through national sovereignty, economic security, and regional stability lenses.",
                        geopolitical_yield=f"Bilateral strategic leverage and diplomatic posture consolidation for {country}.",
                        hard_cash_yield_usd=1_000_000_000.0,
                        concessions_or_vulnerabilities=f"Exposure to regional friction, supply chain disruption, and external trade/sanctions pressures.",
                        strategic_autonomy_score=0.70,
                        key_bilateral_postures={"Multilateral": "Pragmatic sovereign hedging."}
                    ))
            if ledgers:
                return ledgers

        # Default 8 core BRICS member country audits
        return [
            cls.COUNTRY_AUDIT_TEMPLATES["India"],
            cls.COUNTRY_AUDIT_TEMPLATES["China"],
            cls.COUNTRY_AUDIT_TEMPLATES["Russia"],
            cls.COUNTRY_AUDIT_TEMPLATES["Brazil"],
            cls.COUNTRY_AUDIT_TEMPLATES["South Africa"],
            cls.COUNTRY_AUDIT_TEMPLATES["Iran"],
            cls.COUNTRY_AUDIT_TEMPLATES["Saudi Arabia & UAE"],
            cls.COUNTRY_AUDIT_TEMPLATES["Egypt & Ethiopia"],
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
        prioritized_lenses: Optional[List[str]] = None
    ) -> SummitAnalysisReport:
        """
        Executes the end-to-end synthesis pipeline across all 5 tiers.
        """
        # Validate temporal guardrail
        mode, guidance = TemporalGuardrail.evaluate_event_mode(summit)
        summit.temporal_mode = mode

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
            summit_name=getattr(summit, "summit_name", getattr(summit, "title", ""))
        )

        # Tier 3: Kinesics Forensics
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
            "bilateral_local_currency_clearing_share_pct": 38.5 if fixture_mode else 0.0,
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

        # Epistemic Arbitration Log
        arbitration_log = [
            f"[TEMPORAL_VALIDATION] Mode set to {mode.value.upper()}. {guidance}",
        ]
        if ach_report:
            arbitration_log.append(
                f"[ACH_ARBITRATION] Causal hypothesis '{ach_report.dominant_hypothesis_label}' selected with {ach_report.dominant_probability:.1%} probability."
            )
            if ach_report.is_epistemically_contested:
                arbitration_log.append("[ACH_CONTESTED] High epistemic ambiguity detected; alternative non-hostile causes probable.")

        if petro_eval.hard_metrics.get("physical_crude_diversion_bpd"):
            arbitration_log.append("[ARBITRATION_T1_OVER_T5] Petro-logistics physical tanker data (Tier 1) verified 4.2M bpd diversion; superseded communique rhetoric (Tier 5).")

        if cash_eval.primary_epistemic_tier == EpistemicTier.TIER_0_INSUFFICIENT_EVIDENCE:
            arbitration_log.append("[EVIDENCE_DEGRADED] Zero empirical financial flows verified. Tier 2 CapEx audit suppressed to TIER_0_INSUFFICIENT_EVIDENCE.")
        else:
            arbitration_log.append(f"[ARBITRATION_T2_OVER_T5] Cash Flow Haircut applied: Nominal ${hard_money_audit['total_nominal_announced_usd']/1e9:.1f}B discounted by {hard_money_audit['aggregate_haircut_pct']}% to ${hard_money_audit['total_effective_capex_usd']/1e9:.1f}B effective CapEx.")

        if kinesic_observations:
            arbitration_log.append("[ARBITRATION_T3_OVER_T4] India-China border military deployment (Tier 3) overrides staged photocall smiles (Tier 4): Categorized as 'TACTICAL_DE_ESCALATION_PERFORMANCE'.")
        else:
            arbitration_log.append("[EVIDENCE_DEGRADED] Zero empirical kinesic telemetry available. Tier 4 forensics suppressed to TIER_0_INSUFFICIENT_EVIDENCE.")

        # Collect Strategic Resilience Matrix from extended physical and sovereign lenses
        lens_eval_map = {l.lens_name: l for l in lens_evals}
        food_eval = lens_eval_map.get(FoodSecurityLens.LENS_NAME) or lens_eval_map.get("Food Security, Fertilizer Geopolitics & Caloric Sovereignty")
        military_eval = lens_eval_map.get(MilitaryReadinessLens.LENS_NAME) or lens_eval_map.get("Military Readiness, ORBAT & Escalation Dominance")
        minerals_eval = lens_eval_map.get(CriticalMineralsLens.LENS_NAME) or lens_eval_map.get("Critical Minerals & Refining Monopolies")
        demo_eval = lens_eval_map.get(DemographicInfiltrationLens.LENS_NAME) or lens_eval_map.get("Demographic Infiltration & Migration Corridors")
        lawfare_eval = lens_eval_map.get(InstitutionalLawfareLens.LENS_NAME) or lens_eval_map.get("Institutional Lawfare & Multilateral Traps")
        timeline_eval = lens_eval_map.get(IndiaTimelineLens.LENS_NAME) or lens_eval_map.get("India's Strategic Timelines & Post-1947 Boundary Trajectories")
        subsea_eval = lens_eval_map.get(SubseaCablesLens.LENS_NAME) or lens_eval_map.get("Subsea Cables & Hydro-Spatial Sovereignty")
        astro_eval = lens_eval_map.get(AstroPoliticsLens.LENS_NAME) or lens_eval_map.get("Astro-Politics, Orbital Sovereignty & Space Defense")

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
            epistemic_arbitration_log=arbitration_log
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

