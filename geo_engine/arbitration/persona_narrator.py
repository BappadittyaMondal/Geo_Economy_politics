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
                }
            }
            guidance = [
                "Ground all foreign policy in Kautilya's Ṣaḍguṇya and multi-vector strategic autonomy.",
                "Prioritize domestic physical self-reliance (energy, critical minerals, chips) over paper treaties.",
                "Maintain Abhaya: resist extraterritorial coercive sanctions through bilateral currency clearing.",
                "Execute relentlessly: translate civilizational confidence into industrial turnaround velocity."
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
                }
            }
            guidance = [
                "Do not succumb to fear-driven millenarianism; anchor yourself in primary canon (Surya Siddhanta, Mahabharata).",
                "Separate authentic Bhakti spiritual literature from post-1970s commercial chapbook interpolations.",
                "Recognize the algorithmic business model: apocalyptic titles monetize human anxiety for viral retention.",
                "Practice Purushartha and Karma Yoga: focus on education, character, and strategic deterrence over fatalistic doom."
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


