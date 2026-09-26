"""
Visualization & Sovereign Dashboard Engine (Phase 72).
Provides multi-format report exports (interactive HTML dashboard, Markdown audit, publication-grade PDF).
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Union

from ..core.models import SummitAnalysisReport
from .dashboard_engine import DashboardGenerator
from .markdown_exporter import MarkdownExporter
from .pdf_compiler import PDFCompiler


def sanitize_filename(name: str) -> str:
    """Converts a title or summit name into a filesystem-safe slug."""
    clean = re.sub(r"[^\w\s-]", "", name).strip().lower()
    return re.sub(r"[-\s]+", "_", clean) or "intelligence_report"


def export_report(
    report: SummitAnalysisReport,
    formats: Optional[Union[str, List[str]]] = None,
    output_dir: str = "reports",
    base_filename: Optional[str] = None,
    persona: str = "neutral"
) -> Dict[str, str]:
    """
    Exports a SummitAnalysisReport into requested formats (html, md, pdf, or all).
    Returns a dictionary of format -> absolute file path.
    """
    if formats is None:
        formats = ["html", "md", "pdf"]
    elif isinstance(formats, str):
        if formats.lower() == "all":
            formats = ["html", "md", "pdf"]
        else:
            formats = [f.strip().lower() for f in formats.split(",")]

    out_folder = Path(output_dir).resolve()
    out_folder.mkdir(parents=True, exist_ok=True)

    event_title = getattr(report.event, "summit_name", "") or getattr(report.event, "title", "Strategic Event")
    event_year = getattr(report.event, "year", 2026)

    slug = base_filename or f"{sanitize_filename(event_title)}_{event_year}"
    results: Dict[str, str] = {}

    # 1. Generate Markdown text
    md_content = MarkdownExporter.generate_markdown(report, persona=persona)
    if "md" in formats or "all" in formats:
        md_path = out_folder / f"{slug}.md"
        md_path.write_text(md_content, encoding="utf-8")
        results["md"] = str(md_path)

    # 2. Generate HTML Dashboard (with embedded Markdown for client-side blob download)
    html_content = DashboardGenerator.generate_html(
        report,
        persona=persona,
        title=f"{event_title} ({event_year})",
        embedded_markdown=md_content
    )
    if "html" in formats or "all" in formats or "pdf" in formats:
        html_path = out_folder / f"{slug}.html"
        html_path.write_text(html_content, encoding="utf-8")
        results["html"] = str(html_path)

    # 3. Generate PDF via headless browser
    if "pdf" in formats or "all" in formats:
        pdf_path = out_folder / f"{slug}.pdf"
        success, res_info = PDFCompiler.compile_pdf(html_content, str(pdf_path))
        if success:
            results["pdf"] = str(pdf_path)
        else:
            results["pdf_error"] = res_info

    return results


__all__ = [
    "DashboardGenerator",
    "MarkdownExporter",
    "PDFCompiler",
    "export_report",
    "sanitize_filename",
]
