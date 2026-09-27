"""
Markdown Exporter (Phase 76).
Exports de-sanitized multilateral summit, media intelligence, and strategic event reports
into GitHub-Flavored Markdown (GFM) documents with structured tables,
epistemic hierarchy tags, and strategic paradox scorecards.
"""

from typing import Optional, Union
from ..core.models import SummitAnalysisReport
from .adapter import UniversalReportPayload, ReportAdapter


class MarkdownExporter:
    """Exports UniversalReportPayload or SummitAnalysisReport into clean GitHub Flavored Markdown."""

    @classmethod
    def generate_markdown(
        cls,
        report: Union[UniversalReportPayload, SummitAnalysisReport],
        persona: str = "neutral",
        title: Optional[str] = None
    ) -> str:
        """Generates comprehensive markdown text from UniversalReportPayload or SummitAnalysisReport."""
        if isinstance(report, SummitAnalysisReport):
            return cls._generate_summit_markdown(report, persona=persona, title=title)
        
        if not isinstance(report, UniversalReportPayload):
            report = ReportAdapter.to_universal(report, persona=persona, title=title)

        meta = report.metadata
        event_title = title or meta.title
        conf_pct = meta.overall_confidence_pct

        lines = [
            f"# 🏛️ Sovereign Intelligence Audit: {event_title}",
            "",
            f"**Geographic Horizon:** {meta.primary_region} | **Temporal Mode:** `{meta.temporal_mode}` | **Epistemic Confidence:** `{conf_pct}%` | **Persona Projection:** `{persona}`",
            "",
            "> **Analytical Standard:** Zero Hallucination | Zero PR Laundering | Deep-Tech Realism | Hard Balance-Sheet Accounting  ",
            "> **Operational Framework:** 20-Lens Sovereign Matrix & 5-Tier Truth Arbitration Protocol.",
            "",
            "---",
            "",
            "## 1. Executive Master Scorecard",
            "",
            "| Macro Indicator | Value | Unit | Analytical Significance |",
            "| :--- | :--- | :--- | :--- |"
        ]

        for k in report.kpis:
            lines.append(f"| **{k.label}** | `{k.value}` | {k.unit or '-'} | {k.description} |")

        for sec in report.sections:
            lines.extend([
                "",
                "---",
                "",
                f"## {sec.title}",
                ""
            ])
            if sec.subtitle:
                lines.append(f"> *{sec.subtitle}*")
                lines.append("")
            for it in sec.items:
                ts_info = f" `[{it.timestamp_str}]`" if it.timestamp_str else ""
                lines.append(f"### {it.title}{ts_info}")
                if it.subtitle:
                    lines.append(f"**Status:** `{it.evidence_status.upper()}` | **Telemetry:** {it.subtitle}")
                lines.append(it.text)
                if it.metrics:
                    lines.append("- **Metrics:** " + ", ".join([f"`{k}: {v}`" for k, v in it.metrics.items()]))
                lines.append("")

        if report.council_quotes:
            lines.extend([
                "---",
                "",
                "## Civilizational & Strategic Perspectives",
                ""
            ])
            for q in report.council_quotes:
                lines.append(f"### {q.author} ({q.role_or_tradition})")
                lines.append(f"> \"{q.quote_text}\"")
                lines.append("")

        if report.audit_log:
            lines.extend([
                "---",
                "",
                "## Epistemic Truth Arbitration Audit Log",
                ""
            ])
            for entry in report.audit_log:
                lines.append(f"- `{entry}`")
            lines.append("")

        return "\n".join(lines)

    @classmethod
    def _generate_summit_markdown(
        cls,
        report: SummitAnalysisReport,
        persona: str = "neutral",
        title: Optional[str] = None
    ) -> str:
        """Legacy SummitAnalysisReport Markdown generator preserving Phase 72 contract."""
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
        for ns in report.negative_space_synopsis:
            lines.append(f"- {ns}")

        lines.extend([
            "",
            "---",
            "",
            "## 5. Diplomatic Kinesics & Photocall Forensics",
            "",
            "| Primary <-> Secondary | Setting | Warmth | Tension | Handshake Torque | Notes |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for k in report.kinesic_forensics:
            lines.append(f"| {k.actor_primary} <-> {k.actor_secondary} | {k.setting} | `{k.genuine_warmth_index:.2f}` | `{k.residual_tension_score:.2f}` | `{k.handshake_torque_vector}` | {k.notes or ''} |")

        if report.strategic_resilience_matrix:
            lines.extend([
                "",
                "---",
                "",
                "## 6. Strategic Resilience Matrix",
                ""
            ])
            for rk, rv in report.strategic_resilience_matrix.items():
                lines.append(f"- **{rk.replace('_', ' ').title()}:** `{rv}`")

        if report.civilizational_synthesis:
            lines.extend([
                "",
                "---",
                "",
                "## 7. Civilizational Statecraft & Sanatan Inner Meaning",
                ""
            ])
            for ck, cv in report.civilizational_synthesis.items():
                lines.append(f"### {ck.replace('_', ' ').title()}")
                lines.append(cv)
                lines.append("")

        if report.epistemic_arbitration_log:
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


__all__ = ["MarkdownExporter"]
