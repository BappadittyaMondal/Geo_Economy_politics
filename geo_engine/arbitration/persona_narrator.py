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

        else:
            takeaway = (
                f"Neutral arbitration confirms overall epistemic confidence at {report.overall_confidence_score * 100:.1f}%. "
                f"Physical and financial ground truth successfully supersedes ceremonial communiqué text."
            )
            recommendations = [
                "Prioritize Tier 1 physical data over Tier 5 public declarations.",
                "Track ongoing negative-space omissions across multilateral negotiation tracks."
            ]


        return {
            "archetype_key": key,
            "archetype_name": profile["name"],
            "doctrinal_axis": profile["doctrinal_axis"],
            "conceptual_framing": profile["conceptual_framing"],
            "executive_takeaway": takeaway,
            "strategic_recommendations": recommendations,
            "lens_weights": profile["lens_weights"],
            "disclaimer": "[Analytical modeling of doctrinal tradition — not a statement by or attributable to the named individual]"
        }

    @classmethod
    def apply_all_personas(cls, report: SummitAnalysisReport) -> Dict[str, Dict[str, Any]]:
        """
        Executes concurrent synthesis across the complete 7-archetype Strategic Heptarchy.
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


