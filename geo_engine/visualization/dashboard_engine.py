"""
Sovereign Dashboard Engine (Phase 72).
Generates standalone, theme-adaptive, interactive HTML intelligence dashboards
with embedded multi-lens navigation, KPI scorecards, and zero-dependency
client-side blob download capabilities.
"""

import base64
import html
import json
from typing import Any, Dict, List, Optional
from ..core.models import SummitAnalysisReport, EpistemicTier


class DashboardGenerator:
    """Generates production-grade HTML visual dashboards from SummitAnalysisReport."""

    @classmethod
    def generate_html(
        cls,
        report: SummitAnalysisReport,
        persona: str = "neutral",
        title: Optional[str] = None,
        embedded_markdown: Optional[str] = None
    ) -> str:
        """
        Renders a fully self-contained HTML dashboard with:
        1. Master KPI scorecards (autonomy, CapEx, physical flows, epistemic confidence)
        2. Interactive multi-tab layout (12-Lens Matrix, Ledgers, Kinesics, Negative Space, Civilizational, Arbitration)
        3. Client-side instant Markdown (.md) and PDF download engines
        4. Print-optimized CSS for clean headless or desktop PDF printing
        """
        event_title = title or getattr(report.event, "summit_name", "") or getattr(report.event, "title", "Strategic Event")
        event_year = getattr(report.event, "year", 2026)
        event_region = getattr(report.event, "host_country", getattr(report.event, "primary_region", "Global"))
        temporal_mode = getattr(report.event, "temporal_mode", "PROSPECTIVE_SCENARIO")
        if hasattr(temporal_mode, "value"):
            temporal_mode_str = temporal_mode.value.upper()
        else:
            temporal_mode_str = str(temporal_mode).upper()

        confidence_pct = round(report.overall_confidence_score * 100, 1)

        # Macro Financials
        hard_money = report.hard_money_audit or {}
        nominal_b = round(hard_money.get("total_nominal_announced_usd", 0.0) / 1e9, 1)
        effective_b = round(hard_money.get("total_effective_capex_usd", 0.0) / 1e9, 1)
        haircut_pct = round(hard_money.get("aggregate_haircut_pct", 0.0), 1)

        # Base64 encode markdown for client-side blob download if provided
        b64_md = ""
        if embedded_markdown:
            b64_md = base64.b64encode(embedded_markdown.encode("utf-8")).decode("ascii")

        # Serialized JSON data for interactive tab engine
        lens_data = [
            {
                "name": str(le.lens_name),
                "alignment": round(le.alignment_score, 2),
                "confidence": round(le.confidence * 100, 0),
                "tier": le.primary_epistemic_tier.name if hasattr(le.primary_epistemic_tier, "name") else str(le.primary_epistemic_tier),
                "status": str(le.evidence_status),
                "findings": le.key_findings,
                "metrics": le.hard_metrics
            }
            for le in report.lens_evaluations
        ]

        ledgers_data = [
            {
                "country": c.country_name,
                "narrative": c.public_domestic_narrative,
                "yield": c.geopolitical_yield,
                "capex_b": round(c.hard_cash_yield_usd / 1e9, 1),
                "vulnerabilities": c.concessions_or_vulnerabilities,
                "autonomy_pct": round(c.strategic_autonomy_score * 100, 0),
                "bilateral": c.key_bilateral_postures
            }
            for c in report.country_ledgers
        ]

        kinesics_data = [
            {
                "actors": f"{k.actor_primary} <-> {k.actor_secondary}",
                "setting": k.setting,
                "warmth": round(getattr(k, "genuine_warmth_index", 0.5) * 100, 0),
                "tension": round(getattr(k, "residual_tension_score", 0.0) * 100, 0),
                "handshake": getattr(k, "handshake_torque_vector", "neutral_vertical"),
                "notes": getattr(k, "notes", "") or ""
            }
            for k in report.kinesic_forensics
        ]

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(event_title)} ({event_year}) - Geo-Engine Intelligence Dashboard</title>
  <style>
    :root {{
      --bg: #0b0f19;
      --surface: #111827;
      --card: #1f2937;
      --border: #374151;
      --text: #f9fafb;
      --text-muted: #9ca3af;
      --primary: #38bdf8;
      --accent: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    body {{ background: var(--bg); color: var(--text); padding: 24px; font-size: 14px; line-height: 1.5; }}
    .container {{ max-width: 1400px; margin: 0 auto; }}
    
    /* Header & Action Bar */
    .header {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }}
    .badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; }}
    .badge-primary {{ background: rgba(56, 189, 248, 0.15); color: var(--primary); border: 1px solid var(--primary); }}
    .badge-success {{ background: rgba(16, 185, 129, 0.15); color: var(--accent); border: 1px solid var(--accent); }}
    .badge-warning {{ background: rgba(245, 158, 11, 0.15); color: var(--warning); border: 1px solid var(--warning); }}
    .badge-danger {{ background: rgba(239, 68, 68, 0.15); color: var(--danger); border: 1px solid var(--danger); }}
    
    .btn-group {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .btn {{ display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; text-decoration: none; border: 1px solid transparent; transition: all 0.2s; }}
    .btn-blue {{ background: #0284c7; color: #fff; }}
    .btn-blue:hover {{ background: #0369a1; }}
    .btn-emerald {{ background: #059669; color: #fff; }}
    .btn-emerald:hover {{ background: #047857; }}
    .btn-outline {{ background: var(--card); color: var(--text); border-color: var(--border); }}
    .btn-outline:hover {{ background: #374151; }}

    /* KPI Grid */
    .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 24px; }}
    .kpi-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 18px; }}
    .kpi-label {{ font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 700; }}
    .kpi-value {{ font-size: 24px; font-weight: 800; margin: 6px 0 2px 0; color: var(--text); }}
    .kpi-sub {{ font-size: 11px; color: var(--text-muted); }}

    /* Tab Navigation */
    .tabs {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
    .tab-btn {{ background: transparent; border: none; color: var(--text-muted); padding: 8px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.15s; }}
    .tab-btn.active {{ background: var(--card); color: var(--primary); border: 1px solid var(--border); }}
    .tab-btn:hover:not(.active) {{ color: var(--text); background: rgba(255,255,255,0.05); }}

    /* Content Panels */
    .tab-panel {{ display: none; }}
    .tab-panel.active {{ display: block; }}
    .table-container {{ overflow-x: auto; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; margin-bottom: 24px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    th, td {{ padding: 12px 14px; text-align: left; border-bottom: 1px solid var(--border); }}
    th {{ background: #1f2937; color: var(--text-muted); font-weight: 700; text-transform: uppercase; font-size: 10px; letter-spacing: 0.5px; }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover td {{ background: rgba(255,255,255,0.02); }}

    /* Lens Cards Grid */
    .lens-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }}
    .lens-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 16px; }}
    .lens-title {{ font-size: 14px; font-weight: 700; color: var(--primary); margin-bottom: 8px; }}
    .progress-bar {{ height: 6px; background: #374151; border-radius: 3px; overflow: hidden; margin: 8px 0; }}
    .progress-fill {{ height: 100%; border-radius: 3px; }}

    /* Callout & Blockquotes */
    .callout {{ background: var(--card); border-left: 4px solid var(--primary); padding: 14px; border-radius: 4px; margin-bottom: 16px; }}
    .list-item {{ padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }}
    .list-item:last-child {{ border-bottom: none; }}

    @media print {{
      body {{ background: #ffffff !important; color: #000000 !important; font-size: 10pt; }}
      .no-print {{ display: none !important; }}
      .tab-panel {{ display: block !important; margin-bottom: 30px; page-break-after: always; }}
      .kpi-card, .table-container, .lens-card, .callout {{ background: #ffffff !important; border-color: #cbd5e1 !important; color: #000000 !important; }}
      th {{ background: #f1f5f9 !important; color: #0f172a !important; }}
      td {{ color: #1e293b !important; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <div class="header">
      <div>
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
          <span class="badge badge-primary">{html.escape(temporal_mode_str)}</span>
          <span class="badge badge-success">Confidence: {confidence_pct}%</span>
          <span style="font-size: 11px; color: var(--text-muted);">{html.escape(event_region)} ({event_year})</span>
        </div>
        <h1 style="font-size: 24px; font-weight: 800;">{html.escape(event_title)}</h1>
        <p style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">
          Operationalized across the 20-Lens Sovereign Matrix, Epistemic Truth Hierarchy & 5-Tier Response Protocol
        </p>
      </div>
      <div class="btn-group no-print">
        <button onclick="downloadMarkdown()" class="btn btn-blue" title="Download raw Markdown (.md)">
          &darr; Download Report (.md)
        </button>
        <button onclick="window.print()" class="btn btn-emerald" title="Print or Save as PDF">
          &uarr; Export / Print PDF
        </button>
      </div>
    </div>

    <!-- Master KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Epistemic Truth Confidence</div>
        <div class="kpi-value" style="color: var(--accent);">{confidence_pct}%</div>
        <div class="kpi-sub">Cross-Lens Coherence & Verification</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Nominal vs Effective CapEx</div>
        <div class="kpi-value" style="color: var(--primary);">${effective_b}B</div>
        <div class="kpi-sub">Nominal ${nominal_b}B ({haircut_pct}% Haircut applied)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Lenses Evaluated</div>
        <div class="kpi-value">{len(report.lens_evaluations)}</div>
        <div class="kpi-sub">Active Physical, Economic & Sovereign Lenses</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Member Country Ledgers</div>
        <div class="kpi-value">{len(report.country_ledgers)}</div>
        <div class="kpi-sub">Domestic Optics vs Hard Strategic Yield</div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs no-print">
      <button class="tab-btn active" onclick="switchTab('lenses')">1. 20-Lens Matrix</button>
      <button class="tab-btn" onclick="switchTab('ledgers')">2. Country Ledgers</button>
      <button class="tab-btn" onclick="switchTab('resilience')">3. Strategic Resilience</button>
      <button class="tab-btn" onclick="switchTab('kinesics')">4. Kinesics Forensics</button>
      <button class="tab-btn" onclick="switchTab('negative_space')">5. Negative Space</button>
      <button class="tab-btn" onclick="switchTab('civilizational')">6. Civilizational Statecraft</button>
      <button class="tab-btn" onclick="switchTab('arbitration')">7. Arbitration Log</button>
    </div>

    <!-- Tab 1: 20-Lens Matrix -->
    <div id="panel-lenses" class="tab-panel active">
      <div class="lens-grid">
        {"".join([f'''
        <div class="lens-card">
          <div class="lens-title">{html.escape(l['name'])}</div>
          <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;">
            <span>Alignment: <strong style="color: {'var(--accent)' if l['alignment'] > 0.2 else ('var(--warning)' if l['alignment'] >= -0.2 else 'var(--danger)')};">{l['alignment']:+.2f}</strong></span>
            <span>Confidence: {l['confidence']:.0f}%</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" style="width: {int((l['alignment'] + 1) * 50)}%; background: {'var(--accent)' if l['alignment'] > 0.2 else ('var(--warning)' if l['alignment'] >= -0.2 else 'var(--danger)')};"></div>
          </div>
          <div style="margin-top: 8px; font-size: 11px;">
            <span class="badge badge-primary">{html.escape(l['tier'])}</span>
            <span class="badge badge-{'success' if l['status'] == 'sufficient' else 'warning'}">{html.escape(l['status'])}</span>
          </div>
          <div style="margin-top: 10px; font-size: 12px; color: var(--text-muted);">
            {"".join([f'<div class="list-item">&bull; {html.escape(f)}</div>' for f in l['findings'][:3]])}
          </div>
        </div>
        ''' for l in lens_data])}
      </div>
    </div>

    <!-- Tab 2: Country Ledgers -->
    <div id="panel-ledgers" class="tab-panel">
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Country</th>
              <th>Domestic Optics Narrative</th>
              <th>Hard Geopolitical Yield</th>
              <th>Effective CapEx</th>
              <th>Strategic Vulnerabilities</th>
              <th>Autonomy</th>
            </tr>
          </thead>
          <tbody>
            {"".join([f'''
            <tr>
              <td><strong>{html.escape(c['country'])}</strong></td>
              <td>{html.escape(c['narrative'])}</td>
              <td>{html.escape(c['yield'])}</td>
              <td><strong style="color: var(--accent);">${c['capex_b']}B</strong></td>
              <td style="color: var(--danger);">{html.escape(c['vulnerabilities'])}</td>
              <td><span class="badge badge-success">{c['autonomy_pct']:.0f}%</span></td>
            </tr>
            ''' for c in ledgers_data])}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 3: Strategic Resilience Matrix -->
    <div id="panel-resilience" class="tab-panel">
      <div class="kpi-grid">
        {"".join([f'''
        <div class="kpi-card">
          <div class="kpi-label">{html.escape(k.replace('_', ' '))}</div>
          <div class="kpi-value" style="font-size: 20px; color: var(--primary);">{v}</div>
        </div>
        ''' for k, v in (report.strategic_resilience_matrix or {{}}).items()])}
      </div>
    </div>

    <!-- Tab 4: Kinesics Forensics -->
    <div id="panel-kinesics" class="tab-panel">
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Leaders</th>
              <th>Setting</th>
              <th>Residual Warmth</th>
              <th>Tension Score</th>
              <th>Handshake Vector</th>
              <th>Forensic Findings</th>
            </tr>
          </thead>
          <tbody>
            {"".join([f'''
            <tr>
              <td><strong>{html.escape(k['actors'])}</strong></td>
              <td>{html.escape(k['setting'])}</td>
              <td><span class="badge badge-{'success' if k['warmth'] > 50 else 'warning'}">{k['warmth']:.0f}%</span></td>
              <td><span class="badge badge-{'danger' if k['tension'] > 50 else 'success'}">{k['tension']:.0f}%</span></td>
              <td>{html.escape(k['handshake'])}</td>
              <td>{html.escape(k['notes'])}</td>
            </tr>
            ''' for k in kinesics_data])}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 5: Negative Space -->
    <div id="panel-negative_space" class="tab-panel">
      <div class="callout">
        <h3 style="color: var(--primary); margin-bottom: 8px;">Deconstructed Communique Negative Space (Omissions & Dilutions)</h3>
        <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">
          Reveals what participating delegations deliberately excluded, watered down into passive phrasing, or failed to agree upon.
        </p>
        {"".join([f'<div class="list-item" style="color: {"var(--danger)" if "[CRITICAL OMISSION]" in item else ("var(--warning)" if "[DILUTION DETECTED]" in item else "var(--text)")}; font-weight: 500;">{html.escape(item)}</div>' for item in report.negative_space_synopsis])}
      </div>
    </div>

    <!-- Tab 6: Civilizational Statecraft -->
    <div id="panel-civilizational" class="tab-panel">
      {"".join([f'''
      <div class="callout" style="margin-bottom: 16px;">
        <h3 style="text-transform: uppercase; font-size: 12px; color: var(--primary); margin-bottom: 6px;">{html.escape(k.replace('_', ' '))}</h3>
        <p style="font-size: 13px; line-height: 1.6;">{html.escape(v)}</p>
      </div>
      ''' for k, v in (report.civilizational_synthesis or {{}}).items()])}
    </div>

    <!-- Tab 7: Arbitration Log -->
    <div id="panel-arbitration" class="tab-panel">
      <div class="table-container">
        <table>
          <thead>
            <tr><th>#</th><th>Epistemic Hierarchy Arbitration Log Entry</th></tr>
          </thead>
          <tbody>
            {"".join([f'''
            <tr>
              <td style="width: 40px; color: var(--text-muted);">{i+1}</td>
              <td style="font-family: monospace; font-size: 11px;">{html.escape(entry)}</td>
            </tr>
            ''' for i, entry in enumerate(report.epistemic_arbitration_log)])}
          </tbody>
        </table>
      </div>
    </div>

  </div>

  <script>
    // Tab switching logic
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      
      const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
      if (targetBtn) targetBtn.classList.add('active');
      const targetPanel = document.getElementById('panel-' + tabId);
      if (targetPanel) targetPanel.classList.add('active');
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
