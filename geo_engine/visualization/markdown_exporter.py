"""
Markdown Exporter (Phase 72).
Exports de-sanitized multilateral summit and strategic event reports
into GitHub-Flavored Markdown (GFM) documents with structured tables,
epistemic hierarchy tags, and strategic paradox scorecards.
"""

from typing import Optional
from ..core.models import SummitAnalysisReport


class MarkdownExporter:
    """Exports SummitAnalysisReport into clean GitHub Flavored Markdown."""

    @classmethod
    def generate_markdown(
        cls,
        report: SummitAnalysisReport,
        persona: str = "neutral",
        title: Optional[str] = None
    ) -> str:
        """Generates comprehensive markdown text from SummitAnalysisReport."""
        event_title = title or getattr(report.event, "summit_name", "") or getattr(report.event, "title", "Strategic Event")
        event_year = getattr(report.event, "year", 2026)
        event_region = getattr(report.event, "host_country", getattr(report.event, "primary_region", "Global"))
        temporal_mode = getattr(report.event, "temporal_mode", "PROSPECTIVE_SCENARIO")
        if hasattr(temporal_mode, "value"):
            temporal_mode_str = temporal_mode.value.upper()
        else:
            temporal_mode_str = str(temporal_mode).upper()

        confidence_pct = round(report.overall_confidence_score * 100, 1)

        hard_money = report.hard_money_audit or {}
        nominal_b = round(hard_money.get("total_nominal_announced_usd", 0.0) / 1e9, 1)
        effective_b = round(hard_money.get("total_effective_capex_usd", 0.0) / 1e9, 1)
        haircut_pct = round(hard_money.get("aggregate_haircut_pct", 0.0), 1)

        lines = [
            f"# 🏛️ Sovereign Intelligence Audit: {event_title} ({event_year})",
            "",
            f"**Geographic Horizon:** {event_region} | **Temporal Mode:** `{temporal_mode_str}` | **Epistemic Confidence:** `{confidence_pct}%` | **Persona Projection:** `{persona}`",
            "",
            "> **Analytical Standard:** Zero Hallucination | Zero PR Laundering | Deep-Tech Realism | Hard Balance-Sheet Accounting  ",
            "> **Operational Framework:** 20-Lens Sovereign Matrix & 5-Tier Truth Arbitration Protocol.",
            "",
            "---",
            "",
            "## 1. Executive Master Scorecard",
            "",
            "| Macro Indicator | Value | Analytical Significance |",
            "| :--- | :--- | :--- |",
            f"| **Epistemic Confidence** | `{confidence_pct}%` | Inter-lens cross-validation score |",
            f"| **Nominal CapEx Announced** | `${nominal_b}B USD` | Stated diplomatic announcements |",
            f"| **Effective CapEx (After Haircut)** | `${effective_b}B USD` | Hard financial reality after `{haircut_pct}%` haircut |",
            f"| **Active Lenses Evaluated** | `{len(report.lens_evaluations)}` | Multi-domain physical & sovereign matrix |",
            f"| **Member States Audited** | `{len(report.country_ledgers)}` | Balance-sheet ledger reconciliation |",
            "",
            "---",
            "",
            "## 2. 20-Lens Matrix Evaluation & Epistemic Hierarchy",
            "",
            "| Lens / Domain | Alignment (-1.0 to +1.0) | Confidence | Epistemic Tier | Evidence Status |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]

        for le in report.lens_evaluations:
            tier_val = le.primary_epistemic_tier.name if hasattr(le.primary_epistemic_tier, "name") else str(le.primary_epistemic_tier)
            align_str = f"{le.alignment_score:+.2f}"
            conf_str = f"{le.confidence*100:.0f}%"
            lines.append(f"| **{le.lens_name}** | `{align_str}` | `{conf_str}` | `{tier_val}` | `{le.evidence_status}` |")

        lines.extend([
            "",
            "### Granular Key Findings by Lens",
            ""
        ])

        for le in report.lens_evaluations:
            lines.append(f"#### {le.lens_name}")
            for f in le.key_findings:
                lines.append(f"- {f}")
            if le.hard_metrics:
                lines.append("- **Hard Metrics:** " + ", ".join([f"`{k}: {v}`" for k, v in le.hard_metrics.items()]))
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 3. Member State Sovereign Ledgers (Optics vs. Hard Yield)",
            "",
            "| Country | Domestic Optics Narrative | Hard Geopolitical Yield | Effective CapEx | Concessions / Vulnerabilities | Autonomy Score |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for c in report.country_ledgers:
            capex_val = f"${c.hard_cash_yield_usd/1e9:.1f}B"
            autonomy_val = f"{c.strategic_autonomy_score*100:.0f}%"
            lines.append(f"| **{c.country_name}** | {c.public_domestic_narrative} | {c.geopolitical_yield} | `{capex_val}` | {c.concessions_or_vulnerabilities} | `{autonomy_val}` |")

        lines.extend([
            "",
            "---",
            "",
            "## 4. Communique Negative Space (What Was Omitted or Diluted)",
            ""
        ])

        for item in report.negative_space_synopsis:
            if "[CRITICAL OMISSION]" in item:
                lines.append(f"- ❌ **Critical Omission:** {item.replace('[CRITICAL OMISSION]', '').strip()}")
            elif "[DILUTION DETECTED]" in item:
                lines.append(f"- ⚠️ **Dilution Detected:** {item.replace('[DILUTION DETECTED]', '').strip()}")
            else:
                lines.append(f"- ✅ **Retained:** {item}")

        lines.extend([
            "",
            "---",
            "",
            "## 5. Diplomatic Kinesics & Photocall Forensics",
            "",
            "| Actors | Setting | Residual Warmth | Tension Score | Handshake Vector | Forensic Observation |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for k in report.kinesic_forensics:
            actors_str = f"{k.actor_primary} <-> {k.actor_secondary}"
            warmth_val = f"{getattr(k, 'genuine_warmth_index', 0.5)*100:.0f}%"
            tension_val = f"{getattr(k, 'residual_tension_score', 0.0)*100:.0f}%"
            handshake_val = getattr(k, 'handshake_torque_vector', 'neutral_vertical')
            notes_val = getattr(k, 'notes', '') or ''
            lines.append(f"| **{actors_str}** | {k.setting} | `{warmth_val}` | `{tension_val}` | `{handshake_val}` | {notes_val} |")

        lines.extend([
            "",
            "---",
            "",
            "## 6. Strategic Resilience Matrix",
            ""
        ])

        for k, v in (report.strategic_resilience_matrix or {}).items():
            lines.append(f"- **{k.replace('_', ' ').title()}:** `{v}`")

        lines.extend([
            "",
            "---",
            "",
            "## 7. Civilizational Statecraft & Sanatan Inner Meaning",
            ""
        ])

        for k, v in (report.civilizational_synthesis or {}).items():
            lines.append(f"### {k.replace('_', ' ').title()}")
            lines.append(f"{v}")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 8. Epistemic Hierarchy Truth Arbitration Log",
            ""
        ])

        for entry in report.epistemic_arbitration_log:
            lines.append(f"- `{entry}`")

        lines.append("")
        return "\n".join(lines)
