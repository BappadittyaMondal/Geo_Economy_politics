"""scripts/generate_7_targets_audit_pdf.py
Compiles publication-grade PDF Intelligence Dossier for Section 195 (7 Targets Audited 2026-11-25 Night):
analysis_reports/2026-11-25_2245IST_MULTI_DOMAIN_INTELLIGENCE_AUDIT_7_TARGETS.pdf
Mirrors copy to active artifact directory.
"""
import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfgen import canvas

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(REPO_ROOT, "analysis_reports")
ARTIFACT_DIR = r"C:\Users\BAPPADITYA\.gemini\antigravity\brain\50a153d3-ad4a-410f-9d77-a0092c7f65d3"

PDF_FILENAME = "2026-11-25_2245IST_MULTI_DOMAIN_INTELLIGENCE_AUDIT_7_TARGETS.pdf"
PROJECT_PDF_PATH = os.path.join(REPORTS_DIR, PDF_FILENAME)
ARTIFACT_PDF_PATH = os.path.join(ARTIFACT_DIR, PDF_FILENAME)


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#7A1C1C"))
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "GEO-ENGINE INTELLIGENCE ARCHIVE | DOSSIER SEC-195")
            self.setFont("Helvetica-Oblique", 8)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(letter[0] - 54, letter[1] - 36, "7-TARGET AUDIT: METALLURGY, PGI GOLD, STOP SWITCH & QUANTITATIVE QUARANTINE")
            self.setStrokeColor(colors.HexColor("#B8860B"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(54, 36, "CONFIDENTIAL // STRATEGIC RECONNAISSANCE // BSKM EPISTEMIC MATRIX")
        self.drawRightString(letter[0] - 54, 36, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#B8860B"))
        self.setLineWidth(0.5)
        self.line(54, 46, letter[0] - 54, 46)
        self.restoreState()


def build_pdf():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    doc = SimpleDocTemplate(PROJECT_PDF_PATH, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('T', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=colors.HexColor('#7A1C1C'), spaceAfter=4)
    sub_style = ParagraphStyle('S', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=colors.HexColor('#B8860B'), spaceAfter=6)
    h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=colors.HexColor('#1A2B4C'), spaceBefore=7, spaceAfter=3, keepWithNext=True)
    body_style = ParagraphStyle('B', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10.5, textColor=colors.HexColor('#222222'), spaceAfter=3.5)
    bullet_style = ParagraphStyle('BL', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10.5, textColor=colors.HexColor('#222222'), leftIndent=12, firstLineIndent=-8, spaceAfter=2)
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=colors.white)
    tc_style = ParagraphStyle('TC', parent=styles['Normal'], fontName='Helvetica', fontSize=6.8, leading=8.8, textColor=colors.HexColor('#222222'))
    tcb_style = ParagraphStyle('TCB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.8, textColor=colors.HexColor('#1A2B4C'))
    meta_style = ParagraphStyle('M', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.3, leading=9.5, textColor=colors.HexColor('#333333'))

    story = []
    story.append(Paragraph("GEO-ENGINE INTELLIGENCE ARCHIVE | STRATEGIC DOSSIER SEC-195", sub_style))
    story.append(Paragraph("MULTI-DOMAIN DNA AUDIT OF 7 TARGETS: PROPULSION METALLURGY, PGI GOLD SETTLEMENT, BANKING STOP SWITCH, DIPLOMATIC LATITUDE & DIMENSIONAL FACT QUARANTINE", title_style))
    story.append(Paragraph("Paired Cross-Examination Contrasting Banking Alarmism vs RBI Safeguards, US Technical Outages vs Conspiracy Narratives, Aerospace Metallurgy vs Budget Spin, and 10x Unit Error Detection", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7A1C1C'), spaceAfter=6))

    meta_data = [
        [Paragraph("<b>Timestamp:</b> 2026-11-25 22:45 IST", meta_style), Paragraph("<b>Targets Audited:</b> 7 YouTube Discourses", meta_style), Paragraph("<b>DB Index:</b> Section 195 (195 Total)", meta_style)],
        [Paragraph("<b>Core Domains:</b> Aero Metallurgy, Bullion, Cyber, Bank", meta_style), Paragraph("<b>Verification:</b> RBI, WGC, 8th Cir, Hudson Inst", meta_style), Paragraph("<b>Upgrade Queue:</b> Phase 459 + 458 Add.", meta_style)]
    ]
    t_meta = Table(meta_data, colWidths=[170, 170, 164])
    t_meta.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')), ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D3D3')), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3), ('LEFTPADDING', (0, 0), (-1, -1), 4)]))
    story.append(t_meta)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Executive Synthesis & Cross-Video Interlocks", h1_style))
    story.append(Paragraph(
        "Cross-auditing all seven targets exposes critical hidden linkages alongside concrete quantitative errors. Pairing <code>-g3ceK_V1as</code> (Shamik Moitra) directly against <code>ZNVShd2Qy4Y</code> (Dr. Ankit Shah) clarifies that while statutory DICGC insurance caps household deposits at ₹5 lakh per bank and lockers at 100× annual rent, Indian bank balance sheets remain solvent (~1.6% GNPA), and the RBI's November 2026 draft 'Stop Switch' targets digital-arrest/phishing debit fraud rather than systemic bank collapse. Meanwhile, major verified breakthroughs—WGC/HSBC/JPMorgan/StoneX live London Pooled Gold Interests (PGIs), GeM procurement scoring weights excluding Indian MSMEs, and single-crystal turbine alloy bottlenecks—sit beside severe creator errors: two independent 10× unit/FX blunders (248k JPY claimed as ₹17L instead of ₹1.4L; 9,700 lbs claimed as 470 kg instead of 4,409 kg), labeling Lead Azide a 'dirty bomb,' and merging Microsoft's software scalability outage with CIA OSINT breaches into an apocalyptic plot.",
        body_style
    ))

    story.append(Paragraph("2. Deep Forensic Audit Across the 7 Targets", h1_style))
    story.append(Paragraph("• <b>Indian Banking & Nvidia Corporatocracy (<code>-g3ceK_V1as</code> &amp; <code>ZNVShd2Qy4Y</code>):</b> Both examine Nvidia's 11-day Jensen Huang reinstatement &amp; Trump's 'not too late' equity stake remark, confirming intensifying US corporate-state entanglement. Ankit Shah adds verifiable high-value signals: live London PGI digital gold transactions (HSBC, JPMorgan, StoneX), RBI's Nov 2026 'Stop Switch' &amp; Trusted Person draft rules, SC clarifying 11 writ petitioners enabling NFRA action on ~100 auditor notices, GeM's 30–45% legacy/ISO scoring hurdle excluding domestic startups, and Karthigai Deepam SC/TVK conflict. <i>Quarantined Overreach:</i> Converting Microsoft's Nov 12–14 Code Red scalability bug &amp; H.R. 1's 300k noncitizen Medicare rule into an intentional US elite airline/401(k) sabotage conspiracy.", bullet_style))
    story.append(Paragraph("• <b>Iowa Lead Azide Detonation &amp; Japan XR Hardware (<code>Iy-KO051RPY</code> &amp; <code>K-2gxaXJAKM</code>):</b> Verifies the Nov 25, 2026 9 AM CST Middletown IAAP controlled detonation of ~9,500–9,700 lbs recrystallized Lead Azide across 68 drums cleared Nov 23 by the Eighth Circuit Court of Appeals (toxic heavy-metal hazard, NOT a radiological dirty bomb) and Japan's 125g NTT QONOQ / Sharp MiRZA AR2 Gen 1 glasses (248,000 JPY). <i>10× Errors Caught:</i> Sattology miscalculated 9,700 lbs as 470 kg (~4,409 kg actual); Sochify mispriced 248,000 JPY as ₹17 Lakh (~₹1.4 Lakh actual).", bullet_style))
    story.append(Paragraph("• <b>Post-Sindoor Diplomatic Space &amp; Kaveri Metallurgy (<code>dab--v8_oW8</code> &amp; <code>TGVGjDixXZ0</code>):</b> Prashant Dhawan accurately analyzes Amb. Kenneth Juster's April 2026 Hudson warning on US–Pakistan mediation tempering future Indian kinetic responses unless backed by civilizational narrative diplomacy. Vigyan Recharge lucidly explains single-crystal turbine superalloys (Re/Hf/Ta/W/Co), TBCs, micro-cooling, FADEC &amp; missing altitude test tunnels—clarifying ₹382.21 Cr was only the 1989 sanction vs ₹2,035.56 Cr cumulative actual Kaveri expenditure.", bullet_style))
    story.append(Paragraph("• <b>Archival Catastrophe vs. Internet ARG Fiction (<code>yHqupzOBCFM</code>):</b> <i>The File</i> groups verified institutional disasters (1963 Vajont Dam warning failure killing ~1,900; 1944 WWII Ghost Army deception) alongside confirmed 1990s Ong's Hat internet ARG fiction and urban legends without taxonomy separation.", bullet_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("3. Comprehensive 7-Target Credibility Scorecard", h1_style))
    rows = [
        [Paragraph("Video ID / Source", th_style), Paragraph("Topic Focus", th_style), Paragraph("Agree", th_style), Paragraph("Rigor", th_style), Paragraph("Reality", th_style), Paragraph("Verdict", th_style)],
        [Paragraph("<b>dab--v8_oW8</b> (Prashant Dhawan)", tcb_style), Paragraph("Amb. Juster Warning &amp; Narrative Strategy", tc_style), Paragraph("<b>88%</b>", tcb_style), Paragraph("89%", tc_style), Paragraph("92%", tc_style), Paragraph("Clean Hudson Institute citation &amp; pragmatic realism", tc_style)],
        [Paragraph("<b>TGVGjDixXZ0</b> (Vigyan Recharge)", tcb_style), Paragraph("Kaveri Jet Metallurgy, FADEC &amp; R&amp;D", tc_style), Paragraph("<b>84%</b>", tcb_style), Paragraph("86%", tc_style), Paragraph("85%", tc_style), Paragraph("Accurate physics; ₹382 Cr omits ₹2,035 Cr cumulative", tc_style)],
        [Paragraph("<b>K-2gxaXJAKM</b> (Sochify)", tcb_style), Paragraph("NTT QONOQ/Sharp MiRZA XR 125g", tc_style), Paragraph("<b>76%</b>", tcb_style), Paragraph("78%", tc_style), Paragraph("75%", tc_style), Paragraph("Sound hardware summary marred by 10× JPY math error", tc_style)],
        [Paragraph("<b>-g3ceK_V1as</b> (Shamik Moitra)", tcb_style), Paragraph("Nvidia Circularity &amp; DICGC ₹5L Cap", tc_style), Paragraph("<b>75%</b>", tcb_style), Paragraph("78%", tc_style), Paragraph("76%", tc_style), Paragraph("Good corporate/DICGC math; inflated 25% VaR alarm", tc_style)],
        [Paragraph("<b>Iy-KO051RPY</b> (Sattology)", tcb_style), Paragraph("Iowa Nov 25 Lead Azide &amp; Breaches", tc_style), Paragraph("<b>64%</b>", tcb_style), Paragraph("58%", tc_style), Paragraph("68%", tc_style), Paragraph("Real 8th Cir / blast facts; 10× weight err &amp; 'dirty bomb'", tc_style)],
        [Paragraph("<b>ZNVShd2Qy4Y</b> (Dr. Ankit Shah)", tcb_style), Paragraph("RBI Stop Switch, PGI Gold, GeM Bias", tc_style), Paragraph("<b>56%</b>", tcb_style), Paragraph("54%", tc_style), Paragraph("62%", tc_style), Paragraph("Strong PGI/GeM/RBI clues; overreaches on blackout plot", tc_style)],
        [Paragraph("<b>yHqupzOBCFM</b> (The File EP 11)", tcb_style), Paragraph("Vajont, Ghost Army &amp; Ong's Hat Myth", tc_style), Paragraph("<b>50%</b>", tcb_style), Paragraph("55%", tc_style), Paragraph("50%", tc_style), Paragraph("Mixes real 1963/1944 history with 1990s ARG fiction", tc_style)],
    ]
    t_s = Table(rows, colWidths=[118, 128, 36, 36, 40, 146])
    t_s.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A2B4C')), ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')), ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E5E5')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2), ('LEFTPADDING', (0, 0), (-1, -1), 3)]))
    story.append(t_s)

    story.append(Paragraph("4. Council Titans Directives &amp; Queued Structural Upgrade (Phase 459)", h1_style))
    story.append(Paragraph("• <b>Dr. S. Jaishankar / NSA Doval:</b> Answer Amb. Juster's mediation caveat by scaling civilizational narrative diplomacy while fixing Kaveri single-crystal metallurgy and GeM startup exclusions internally.", bullet_style))
    story.append(Paragraph("• <b>Dr. Ankit Shah / PM Modi / Sanjeev Sanyal:</b> Track live London Pooled Gold Interests (PGIs) while using RBI's new Stop Switch and splitting deposits across solvent Tier-1 banks (respecting DICGC ₹5L limits).", bullet_style))
    story.append(Paragraph("• <b>J. Sai Deepak / Dr. Anand Ranganathan:</b> Enforce constitutional consistency on religious sites and audit tenders, while verifying every unit/claim (248k JPY ≈ ₹1.4L; Lead Azide ≠ dirty bomb; Code Red = Windows scaling bug).", bullet_style))
    story.append(Paragraph(
        "<b>Queued Real Upgrade (Preserves Phases 451–458; Zero Codebase Modification):</b> Refines Phase 458 with Automated Unit/Currency/Taxonomy Quarantine and stages <b>Phase 459: AeroMetallurgyProcurementBiasAndBullionSettlementTensor</b> in <code>UPGRADE_PLANING</code> (projecting <b>262 Resilience Channels / 272 Lens Symbols</b>).",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    shutil.copy2(PROJECT_PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"[OK] Generated {PROJECT_PDF_PATH} ({os.path.getsize(PROJECT_PDF_PATH)/1024:.1f} KB)")
    print(f"[OK] Mirrored to {ARTIFACT_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
