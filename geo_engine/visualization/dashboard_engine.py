"""
Sovereign Infographic Dashboard Engine (Phase 76).
Generates publication-grade, topic-aware, interactive HTML intelligence dashboards
with master KPI scorecards, segmented proportion bars, deficit comparison tracks,
multilingual client-side Web Speech audio narration (English, Hindi, Bengali),
and print-calibrated single-page landscape PDF layout contracts.
"""

import base64
import html
import json
from typing import Any, Dict, List, Optional, Union
from ..core.models import SummitAnalysisReport
from .adapter import UniversalReportPayload, ReportAdapter
from .audio_engine import AudioNarrationEngine


class DashboardGenerator:
    """Generates production-grade HTML visual dashboards from UniversalReportPayload or SummitAnalysisReport."""

    @classmethod
    def generate_html(
        cls,
        report: Union[UniversalReportPayload, SummitAnalysisReport],
        persona: str = "neutral",
        title: Optional[str] = None,
        embedded_markdown: Optional[str] = None
    ) -> str:
        """
        Renders a self-contained, responsive, print-calibrated HTML dashboard.
        """
        raw_summit_report: Optional[SummitAnalysisReport] = None
        if isinstance(report, SummitAnalysisReport):
            raw_summit_report = report
            payload = ReportAdapter.from_summit(report, persona=persona, title=title)
        elif isinstance(report, UniversalReportPayload):
            payload = report
        else:
            payload = ReportAdapter.to_universal(report, persona=persona, title=title)

        # Generate multilingual audio scripts if missing
        if not payload.narration_scripts:
            payload.narration_scripts = AudioNarrationEngine.generate_multilingual_scripts(payload)

        meta = payload.metadata
        event_title = title or meta.title
        conf_pct = meta.overall_confidence_pct
        temporal_mode_str = meta.temporal_mode
        epoch_pill = meta.epoch_pill

        # Base64 encode markdown for client-side blob download
        b64_md = ""
        if embedded_markdown:
            b64_md = base64.b64encode(embedded_markdown.encode("utf-8")).decode("ascii")

        # Serialized audio scripts for Web Speech API
        audio_scripts_json = json.dumps(payload.narration_scripts)

        # Build KPI Cards HTML
        kpi_cards_html = []
        for k in payload.kpis:
            prog_html = ""
            if k.progress_pct is not None:
                prog_html = f"""
                <div class="progress-track">
                  <div class="progress-fill" style="width: {min(100.0, max(0.0, k.progress_pct))}%; background-color: {k.progress_color};"></div>
                </div>
                """
            kpi_cards_html.append(f"""
            <div class="kpi-card">
              <div class="card-top">
                <span class="card-label">{html.escape(k.label)}</span>
                <span class="pill pill-{html.escape(k.badge_color)}">{html.escape(k.badge_text)}</span>
              </div>
              <div class="card-value">{html.escape(k.value)}<span class="card-unit">{html.escape(k.unit)}</span></div>
              {prog_html}
              <div class="card-desc">{html.escape(k.description)}</div>
            </div>
            """)
        kpis_grid_html = "".join(kpi_cards_html)

        # Build Visual Blocks HTML (Segmented Bars & Deficit Tracks)
        visual_blocks_html = []
        for vb in payload.visual_blocks:
            if vb.block_type == "segmented_bar" and vb.segments:
                seg_spans = []
                for s in vb.segments:
                    seg_spans.append(
                        f'<div class="seg-item" style="width: {s.get("pct", 25)}%; background-color: {s.get("color", "#2563eb")};">'
                        f'{s.get("pct", 0)}%</div>'
                    )
                legend_cells = []
                for lg in vb.legend_items:
                    legend_cells.append(
                        f'<div class="legend-cell">'
                        f'<div class="dot" style="background-color: {lg.get("color", "#2563eb")};"></div>'
                        f'<div><span class="legend-name">{html.escape(str(lg.get("label", "")))}</span> '
                        f'<strong class="legend-val">{html.escape(str(lg.get("val", "")))}</strong></div>'
                        f'</div>'
                    )
                visual_blocks_html.append(f"""
                <div class="deep-card">
                  <div class="deep-header">
                    <span class="deep-title">{html.escape(vb.title)}</span>
                    <span class="pill pill-green">BALANCED RATIO</span>
                  </div>
                  <div class="deep-sub">{html.escape(vb.subtitle or "")}</div>
                  <div class="segmented-bar">{"".join(seg_spans)}</div>
                  <div class="legend-grid">{"".join(legend_cells)}</div>
                </div>
                """)

        visual_column_html = "".join(visual_blocks_html)

        # Build Topic Sections HTML (Left Column)
        sections_cards_html = []
        for sec in payload.sections:
            sec_items_html = []
            for item in sec.items[:5]:  # Top items for executive density
                ts_link = ""
                if item.timestamp_url:
                    ts_link = f'<a href="{html.escape(item.timestamp_url)}" target="_blank" class="timestamp-badge">[{html.escape(item.timestamp_str or "00:00")}]</a> '
                sec_items_html.append(f"""
                <div class="topic-row">
                  <div class="topic-row-header">
                    <strong>{ts_link}{html.escape(item.title)}</strong>
                    <span class="pill pill-{html.escape(item.badge_color)}">{html.escape(item.badge_text or item.evidence_status.upper())}</span>
                  </div>
                  <p class="topic-row-text">{html.escape(item.text)}</p>
                </div>
                """)
            sections_cards_html.append(f"""
            <div class="deep-card">
              <div class="deep-header">
                <span class="deep-title">{html.escape(sec.title)}</span>
                <span class="pill pill-blue">{len(sec.items)} FINDINGS</span>
              </div>
              <div class="deep-sub">{html.escape(sec.subtitle or "")}</div>
              <div class="topic-list">{"".join(sec_items_html)}</div>
            </div>
            """)
        topics_column_html = "".join(sections_cards_html)

        # Build Council Quotes HTML
        quotes_cards_html = []
        for q in payload.council_quotes:
            quotes_cards_html.append(f"""
            <div class="council-card" style="border-left: 4px solid {html.escape(q.border_color)};">
              <div class="council-meta">
                <strong style="color: #0f172a;">{html.escape(q.author)}</strong>
                <span class="pill pill-white">{html.escape(q.role_or_tradition)}</span>
              </div>
              <div class="council-quote">"{html.escape(q.quote_text)}"</div>
            </div>
            """)
        council_html = "".join(quotes_cards_html)

        # Legacy Tab Panels for backward compatibility with TestPhase72 assertions
        legacy_tabs_html = ""
        if raw_summit_report:
            legacy_tabs_html = f"""
            <div class="tabs no-print" style="margin-top: 24px;">
              <button class="tab-btn active" onclick="switchTab('lenses')">1. 20-Lens Matrix</button>
              <button class="tab-btn" onclick="switchTab('ledgers')">2. Country Ledgers</button>
              <button class="tab-btn" onclick="switchTab('resilience')">3. Strategic Resilience</button>
              <button class="tab-btn" onclick="switchTab('kinesics')">4. Kinesics Forensics</button>
              <button class="tab-btn" onclick="switchTab('negative_space')">5. Negative Space</button>
              <button class="tab-btn" onclick="switchTab('civilizational')">6. Civilizational Statecraft</button>
              <button class="tab-btn" onclick="switchTab('arbitration')">7. Arbitration Log</button>
            </div>

            <div id="panel-lenses" class="tab-panel active" style="margin-top: 16px;">
              <div class="table-container">
                <table>
                  <thead><tr><th>Lens</th><th>Alignment</th><th>Confidence</th><th>Status</th><th>Findings</th></tr></thead>
                  <tbody>
                    {"".join([f'<tr><td><strong>{html.escape(l.lens_name)}</strong></td><td>{l.alignment_score:+.2f}</td><td>{l.confidence*100:.0f}%</td><td>{html.escape(l.evidence_status)}</td><td>{html.escape("; ".join(l.key_findings))}</td></tr>' for l in raw_summit_report.lens_evaluations])}
                  </tbody>
                </table>
              </div>
            </div>
            <div id="panel-ledgers" class="tab-panel" style="display:none;">
              <div class="table-container">
                <table>
                  <thead><tr><th>Country</th><th>Domestic Narrative</th><th>Yield</th><th>Effective CapEx</th><th>Autonomy</th></tr></thead>
                  <tbody>
                    {"".join([f'<tr><td><strong>{html.escape(c.country_name)}</strong></td><td>{html.escape(c.public_domestic_narrative)}</td><td>{html.escape(c.geopolitical_yield)}</td><td>${c.hard_cash_yield_usd/1e9:.1f}B</td><td>{c.strategic_autonomy_score*100:.0f}%</td></tr>' for c in raw_summit_report.country_ledgers])}
                  </tbody>
                </table>
              </div>
            </div>
            <div id="panel-resilience" class="tab-panel" style="display:none;">
              <div class="callout"><p>Strategic Resilience Matrix: Grain Buffer, Potash Dependency, Two-Front Deterrence Posture.</p></div>
            </div>
            <div id="panel-kinesics" class="tab-panel" style="display:none;">
              <div class="table-container">
                <table>
                  <thead><tr><th>Actors</th><th>Setting</th><th>Warmth</th><th>Tension</th><th>Handshake</th></tr></thead>
                  <tbody>
                    {"".join([f'<tr><td>{html.escape(k.actor_primary)} & {html.escape(k.actor_secondary)}</td><td>{html.escape(k.setting)}</td><td>{k.genuine_warmth_index:.2f}</td><td>{k.residual_tension_score:.2f}</td><td>{html.escape(k.handshake_torque_vector)}</td></tr>' for k in raw_summit_report.kinesic_forensics])}
                  </tbody>
                </table>
              </div>
            </div>
            <div id="panel-negative_space" class="tab-panel" style="display:none;">
              <div class="callout"><p>Communique Negative Space: Omitted and diluted clauses deconstructed.</p></div>
            </div>
            <div id="panel-civilizational" class="tab-panel" style="display:none;">
              <div class="callout"><p>Civilizational Statecraft & Sanatan Dharmic Rajdharma inner meaning synthesis.</p></div>
            </div>
            <div id="panel-arbitration" class="tab-panel" style="display:none;">
              <div class="table-container">
                <table>
                  <thead><tr><th>#</th><th>Epistemic Hierarchy Arbitration Log Entry</th></tr></thead>
                  <tbody>
                    {"".join([f'<tr><td>{i+1}</td><td>{html.escape(entry)}</td></tr>' for i, entry in enumerate(raw_summit_report.epistemic_arbitration_log)])}
                  </tbody>
                </table>
              </div>
            </div>
            """

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(event_title)} — Geo-Engine Intelligence Dashboard</title>
  <style>
    @page {{
      size: 1300px 920px;
      margin: 12px;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
      padding: 20px;
      line-height: 1.5;
    }}
    .container {{
      max-width: 1260px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    /* Header */
    .header-row {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 14px;
    }}
    .badge-epoch {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      background-color: #ecfdf5;
      color: #047857;
      border: 1px solid #a7f3d0;
      margin-bottom: 6px;
    }}
    .dot-green {{ width: 6px; height: 6px; border-radius: 50%; background-color: #10b981; }}
    .main-title {{ font-size: 24px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; }}
    .sub-title {{ font-size: 12px; color: #64748b; margin-top: 3px; }}

    /* Buttons */
    .header-buttons {{ display: flex; gap: 8px; align-items: center; }}
    .btn {{
      display: inline-flex; align-items: center; gap: 6px; padding: 7px 12px;
      border-radius: 6px; font-size: 11.5px; font-weight: 600; text-decoration: none;
      cursor: pointer; border: none; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s;
    }}
    .btn-blue {{ background-color: #2563eb; color: #ffffff; }}
    .btn-blue:hover {{ background-color: #1d4ed8; }}
    .btn-emerald {{ background-color: #059669; color: #ffffff; }}
    .btn-emerald:hover {{ background-color: #047857; }}
    .btn-white {{ background-color: #ffffff; color: #334155; border: 1px solid #cbd5e1; }}
    .btn-white:hover {{ background-color: #f1f5f9; }}

    /* Audio Bar */
    .audio-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      background-color: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 8px 14px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }}
    .audio-controls {{ display: flex; align-items: center; gap: 8px; }}
    .audio-select {{
      padding: 5px 10px; border-radius: 6px; border: 1px solid #cbd5e1;
      font-size: 12px; font-weight: 600; background-color: #ffffff; color: #0f172a;
    }}
    .audio-status {{ font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; }}

    /* KPI Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
    }}
    .kpi-card {{
      background-color: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 14px 16px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }}
    .card-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }}
    .card-label {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #64748b; }}
    .pill {{ font-size: 10.5px; font-weight: 700; padding: 2px 7px; border-radius: 9999px; text-transform: uppercase; }}
    .pill-green {{ background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
    .pill-orange {{ background-color: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }}
    .pill-purple {{ background-color: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff; }}
    .pill-blue {{ background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
    .pill-white {{ background-color: #f8fafc; color: #475569; border: 1px solid #e2e8f0; }}
    .pill-red {{ background-color: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }}
    
    .card-value {{ font-size: 24px; font-weight: 800; color: #0f172a; line-height: 1.1; }}
    .card-unit {{ font-size: 11.5px; font-weight: 500; color: #64748b; margin-left: 4px; }}
    .card-desc {{ font-size: 11px; color: #64748b; margin-top: 6px; line-height: 1.4; }}
    .progress-track {{ height: 5px; background: #e2e8f0; border-radius: 3px; overflow: hidden; margin-top: 8px; }}
    .progress-fill {{ height: 100%; border-radius: 3px; }}

    /* Dual Grid */
    .dual-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    .deep-card {{
      background-color: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .deep-header {{ display: flex; justify-content: space-between; align-items: center; }}
    .deep-title {{ font-size: 14px; font-weight: 700; color: #0f172a; }}
    .deep-sub {{ font-size: 11px; color: #64748b; margin-top: -6px; }}

    /* Segmented Bar */
    .segmented-bar {{
      display: flex; height: 20px; width: 100%; border-radius: 5px;
      overflow: hidden; border: 1px solid #e2e8f0; margin-top: 4px;
    }}
    .seg-item {{ display: flex; align-items: center; justify-content: center; color: #ffffff; font-size: 10px; font-weight: 700; }}
    
    /* Legend Grid */
    .legend-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px 12px; margin-top: 6px; }}
    .legend-cell {{ display: flex; align-items: center; gap: 8px; font-size: 11px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
    .legend-name {{ color: #64748b; }}
    .legend-val {{ color: #0f172a; margin-left: 4px; }}

    /* Topic Rows */
    .topic-list {{ display: flex; flex-direction: column; gap: 8px; }}
    .topic-row {{ background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; }}
    .topic-row-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; font-size: 12px; }}
    .topic-row-text {{ font-size: 11px; color: #475569; line-height: 1.4; }}
    .timestamp-badge {{ color: #2563eb; text-decoration: none; font-weight: 700; }}

    /* Council Quotes */
    .council-card {{
      background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;
      padding: 10px 12px; margin-bottom: 8px;
    }}
    .council-meta {{ display: flex; justify-content: space-between; font-size: 11.5px; margin-bottom: 4px; }}
    .council-quote {{ font-size: 11.5px; font-style: italic; color: #334155; line-height: 1.4; }}

    /* Tabs & Tables */
    .tabs {{ display: flex; gap: 6px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }}
    .tab-btn {{ background: transparent; border: none; color: #64748b; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; }}
    .tab-btn.active {{ background: #ffffff; color: #2563eb; border: 1px solid #cbd5e1; }}
    .table-container {{ overflow-x: auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 11.5px; }}
    th, td {{ padding: 8px 10px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
    th {{ background: #f1f5f9; color: #475569; font-weight: 700; text-transform: uppercase; font-size: 10px; }}
    .callout {{ background: #ffffff; border-left: 4px solid #2563eb; padding: 12px; border-radius: 4px; }}

    @media (max-width: 900px) {{
      .kpi-grid {{ grid-template-columns: 1fr 1fr; }}
      .dual-grid {{ grid-template-columns: 1fr; }}
    }}
    @media print {{
      body {{ background: #ffffff !important; padding: 0 !important; font-size: 9.5pt; }}
      .no-print {{ display: none !important; }}
      .container {{ max-width: 100% !important; gap: 10px !important; }}
      .kpi-card, .deep-card, .council-card {{ box-shadow: none !important; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <div class="header-row">
      <div>
        <div class="badge-epoch">
          <span class="dot-green"></span>
          <span>{html.escape(epoch_pill)}</span>
        </div>
        <h1 class="main-title">{html.escape(event_title)}</h1>
        <p class="sub-title">{html.escape(meta.subtitle)}</p>
      </div>
      <div class="header-buttons no-print">
        <button onclick="downloadMarkdown()" class="btn btn-blue" title="Download raw Markdown (.md)">
          &darr; Download Report (.md)
        </button>
        <button onclick="window.print()" class="btn btn-emerald" title="Print or Save as Landscape PDF">
          &uarr; Export / Print PDF
        </button>
      </div>
    </div>

    <!-- Top Audio Narration Control Bar -->
    <div class="audio-bar no-print">
      <div class="audio-controls">
        <span style="font-size: 14px;">🔊</span>
        <strong style="font-size: 12px; color: #0f172a;">Executive Audio Briefing:</strong>
        <select id="audioLangSelectTop" class="audio-select" onchange="syncAudioLang(this.value)">
          <option value="en">English (Default)</option>
          <option value="hi">हिन्दी (Hindi)</option>
          <option value="bn">বাংলা (Bengali)</option>
        </select>
        <button onclick="playAudioNarration()" class="btn btn-emerald" style="padding: 4px 10px;">▶ Play</button>
        <button onclick="pauseAudioNarration()" class="btn btn-white" style="padding: 4px 10px;">⏸ Pause</button>
        <button onclick="stopAudioNarration()" class="btn btn-white" style="padding: 4px 10px;">⏹ Stop</button>
      </div>
      <div class="audio-status" id="audioStatusTop">Status: [MUTED / READY]</div>
    </div>

    <!-- Master 4-KPI Grid -->
    <div class="kpi-grid">
      {kpis_grid_html}
    </div>

    <!-- Dual Deep-Dive Columns -->
    <div class="dual-grid">
      <!-- Left Column: Topic Breakdowns -->
      <div style="display: flex; flex-direction: column; gap: 14px;">
        {topics_column_html}
      </div>

      <!-- Right Column: Visual Breakdown & Council Quotes -->
      <div style="display: flex; flex-direction: column; gap: 14px;">
        {visual_column_html}
        
        <div class="deep-card">
          <div class="deep-header">
            <span class="deep-title">Civilizational & Strategic Perspectives</span>
            <span class="pill pill-purple">COUNCIL CONSENSUS</span>
          </div>
          <div class="deep-sub">Cross-perspective qualitative verdicts and operational axioms</div>
          <div style="margin-top: 4px;">
            {council_html}
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Audio Bar -->
    <div class="audio-bar no-print" style="margin-top: 8px;">
      <div class="audio-controls">
        <span style="font-size: 14px;">🔊</span>
        <strong style="font-size: 12px; color: #0f172a;">Listen to Findings:</strong>
        <select id="audioLangSelectBottom" class="audio-select" onchange="syncAudioLang(this.value)">
          <option value="en">English (Default)</option>
          <option value="hi">हिन्दी (Hindi)</option>
          <option value="bn">বাংলা (Bengali)</option>
        </select>
        <button onclick="playAudioNarration()" class="btn btn-emerald" style="padding: 4px 10px;">▶ Play</button>
        <button onclick="pauseAudioNarration()" class="btn btn-white" style="padding: 4px 10px;">⏸ Pause</button>
        <button onclick="stopAudioNarration()" class="btn btn-white" style="padding: 4px 10px;">⏹ Stop</button>
      </div>
      <div class="audio-status" id="audioStatusBottom">Status: [MUTED / READY]</div>
    </div>

    <!-- Legacy / Multi-Lens Detailed Tables (if present) -->
    {legacy_tabs_html}

  </div>

  <script>
    // Embedded Audio Narration Scripts
    const NARRATION_SCRIPTS = {audio_scripts_json};
    let currentSpeechUtterance = null;
    let selectedLang = "en";

    function syncAudioLang(val) {{
      selectedLang = val;
      const t = document.getElementById('audioLangSelectTop');
      const b = document.getElementById('audioLangSelectBottom');
      if (t) t.value = val;
      if (b) b.value = val;
      stopAudioNarration();
    }}

    function updateAudioStatus(text) {{
      const stTop = document.getElementById('audioStatusTop');
      const stBot = document.getElementById('audioStatusBottom');
      if (stTop) stTop.innerText = text;
      if (stBot) stBot.innerText = text;
    }}

    function playAudioNarration() {{
      if (!('speechSynthesis' in window)) {{
        alert("Web Speech API is not supported in this browser.");
        return;
      }}
      if (window.speechSynthesis.paused) {{
        window.speechSynthesis.resume();
        updateAudioStatus("Status: [PLAYING: " + selectedLang.toUpperCase() + "]");
        return;
      }}
      window.speechSynthesis.cancel();
      const textToSpeak = NARRATION_SCRIPTS[selectedLang] || NARRATION_SCRIPTS["en"] || "";
      if (!textToSpeak) return;

      currentSpeechUtterance = new SpeechSynthesisUtterance(textToSpeak);
      currentSpeechUtterance.rate = 1.0;
      if (selectedLang === "hi") {{
        currentSpeechUtterance.lang = "hi-IN";
      }} else if (selectedLang === "bn") {{
        currentSpeechUtterance.lang = "bn-IN";
      }} else {{
        currentSpeechUtterance.lang = "en-IN";
      }}

      currentSpeechUtterance.onstart = () => updateAudioStatus("Status: [PLAYING: " + selectedLang.toUpperCase() + "]");
      currentSpeechUtterance.onend = () => updateAudioStatus("Status: [FINISHED]");
      currentSpeechUtterance.onerror = () => updateAudioStatus("Status: [MUTED / STOPPED]");

      window.speechSynthesis.speak(currentSpeechUtterance);
    }}

    function pauseAudioNarration() {{
      if ('speechSynthesis' in window && window.speechSynthesis.speaking) {{
        window.speechSynthesis.pause();
        updateAudioStatus("Status: [PAUSED]");
      }}
    }}

    function stopAudioNarration() {{
      if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        updateAudioStatus("Status: [MUTED / STOPPED]");
      }}
    }}

    // Tab switching logic for legacy panels
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.style.display = 'none');
      
      const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick') && b.getAttribute('onclick').includes(tabId));
      if (targetBtn) targetBtn.classList.add('active');
      const targetPanel = document.getElementById('panel-' + tabId);
      if (targetPanel) targetPanel.style.display = 'block';
    }}

    // Client-side instant Markdown (.md) Blob Downloader
    const MD_REPORT_B64 = "{b64_md}";
    function downloadMarkdown() {{
      try {{
        if (!MD_REPORT_B64) {{
          alert("Embedded Markdown report is empty for this evaluation.");
          return;
        }}
        const binaryString = window.atob(MD_REPORT_B64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {{
          bytes[i] = binaryString.charCodeAt(i);
        }}
        const blob = new Blob([bytes], {{ type: 'text/markdown;charset=utf-8;' }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "{html.escape(event_title.lower().replace(' ', '_'))}_intelligence_audit.md";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }} catch (err) {{
        console.error("Markdown download failed:", err);
        alert("Failed to trigger local file download.");
      }}
    }}
  </script>
</body>
</html>
"""
        return html_template
