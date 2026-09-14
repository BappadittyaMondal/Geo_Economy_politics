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
                "PetroLogisticsLens": 1.2
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
                "HybridCovertLens": 1.6,
                "BureaucraticInertiaLens": 1.3,
                "GeopoliticalLens": 1.3,
                "IndiaTimelineLens": 1.4
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
                "IndiaTimelineLens": 1.3
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
                "HistoryLens": 1.3
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
                "PetroLogisticsLens": 1.4
            },
            "conceptual_framing": (
                "A hard macro-monetary warfare framework: global geopolitics is governed by the structural unwind "
                "of the unbacked fiat US dollar debt spiral and the transition toward physical asset settlement "
                "(gold bullion, crude, critical minerals, sovereign energy grid clearing). Multilateral platforms must be "
                "judged strictly by their ability to protect sovereign balance sheets from SWIFT de-platforming."
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
            "lens_weights": profile["lens_weights"]
        }

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

