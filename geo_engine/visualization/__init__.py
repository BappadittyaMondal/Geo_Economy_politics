"""
Visualization & Sovereign Dashboard Engine (Phase 76).
Provides universal multi-format report exports (interactive HTML dashboard, Markdown audit, publication-grade PDF)
and multilingual client-side Web Speech audio narration (English, Hindi, Bengali).
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..core.models import SummitAnalysisReport
from ..video.synthesizer import VideoIntelligenceReport
from .adapter import UniversalReportPayload, ReportAdapter
from .audio_engine import AudioNarrationEngine
from .dashboard_engine import DashboardGenerator
from .markdown_exporter import MarkdownExporter
from .pdf_compiler import PDFCompiler


def sanitize_filename(name: str) -> str:
    """Converts a title or summit name into a filesystem-safe slug."""
    clean = re.sub(r"[^\w\s-]", "", name).strip().lower()
    return re.sub(r"[-\s]+", "_", clean) or "intelligence_report"


def export_report(
    report: Union[UniversalReportPayload, SummitAnalysisReport, VideoIntelligenceReport, Dict[str, Any], Any],
    formats: Optional[Union[str, List[str]]] = None,
    output_dir: str = "reports",
    base_filename: Optional[str] = None,
    persona: str = "neutral",
    title: Optional[str] = None
) -> Dict[str, str]:
    """
    Exports an intelligence report into requested formats (html, md, pdf, or all).
    Supports UniversalReportPayload, SummitAnalysisReport, VideoIntelligenceReport, and generic dicts.
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

    # Polymorphic conversion to UniversalReportPayload
    raw_source = report
    if isinstance(report, UniversalReportPayload):
        payload = report
    elif isinstance(report, SummitAnalysisReport):
        payload = ReportAdapter.from_summit(report, persona=persona, title=title)
    elif isinstance(report, VideoIntelligenceReport):
        payload = ReportAdapter.from_video(report, persona=persona)
    else:
        payload = ReportAdapter.to_universal(report, persona=persona, title=title)

    event_title = title or payload.metadata.title
    focal_date = payload.metadata.focal_date

    slug = base_filename or f"{sanitize_filename(event_title)}_{focal_date}"
    results: Dict[str, str] = {}

    # 1. Generate Markdown text
    # If raw source was SummitAnalysisReport, MarkdownExporter preserves full legacy multi-tier markdown
    md_content = MarkdownExporter.generate_markdown(raw_source if isinstance(raw_source, SummitAnalysisReport) else payload, persona=persona, title=event_title)
    if "md" in formats or "all" in formats:
        md_path = out_folder / f"{slug}.md"
        md_path.write_text(md_content, encoding="utf-8")
        results["md"] = str(md_path)

    # 2. Generate HTML Dashboard (with embedded Markdown for client-side blob download and audio scripts)
    html_content = DashboardGenerator.generate_html(
        raw_source if isinstance(raw_source, SummitAnalysisReport) else payload,
        persona=persona,
        title=event_title,
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
    "AudioNarrationEngine",
    "DashboardGenerator",
    "MarkdownExporter",
    "PDFCompiler",
    "ReportAdapter",
    "UniversalReportPayload",
    "export_report",
    "sanitize_filename",
]
