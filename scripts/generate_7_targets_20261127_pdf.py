"""scripts/generate_7_targets_20261127_pdf.py
Compiles publication-grade PDF Intelligence Dossier for Section 198 (8 Links / 7 Unique Targets Audited 2026-11-27):
analysis_reports/2026-11-27_1630IST_MULTI_DOMAIN_INTELLIGENCE_AUDIT_7_TARGETS.pdf
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

PDF_FILENAME = "2026-11-27_1630IST_MULTI_DOMAIN_INTELLIGENCE_AUDIT_7_TARGETS.pdf"
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
        self.setFont("Helvetica-Bold", 7.2)
        self.setFillColor(colors.HexColor("#7A1C1C"))
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "GEO-ENGINE ARCHIVE | DOSSIER SEC-198")
            self.setFont("Helvetica-Oblique", 7.2)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(letter[0] - 54, letter[1] - 36, "SEC 301 TARIFF MATH, RBI FORWARD BOOK, PMLA/TBML, MI OPS & IBM MYTH")
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
    title_style = ParagraphStyle('T', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13.5, leading=16.5, textColor=colors.HexColor('#7A1C1C'), spaceAfter=4)
    sub_style = ParagraphStyle('S', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=colors.HexColor('#B8860B'), spaceAfter=6)
    h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.2, leading=13, textColor=colors.HexColor('#1A2B4C'), spaceBefore=7, spaceAfter=3, keepWithNext=True)
    body_style = ParagraphStyle('B', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10.5, textColor=colors.HexColor('#222222'), spaceAfter=3.5)
    bullet_style = ParagraphStyle('BL', parent=styles['Normal'], fontName='Helvetica', fontSize=7.8, leading=10.2, textColor=colors.HexColor('#222222'), leftIndent=12, firstLineIndent=-8, spaceAfter=2.2)
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.8, textColor=colors.white)
    tc_style = ParagraphStyle('TC', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#222222'))
    tcb_style = ParagraphStyle('TCB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#1A2B4C'))
    meta_style = ParagraphStyle('M', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.2, leading=9.2, textColor=colors.HexColor('#333333'))

    story = []
    story.append(Paragraph("GEO-ENGINE INTELLIGENCE ARCHIVE | STRATEGIC DOSSIER SEC-198", sub_style))
    story.append(Paragraph("MULTI-DOMAIN DNA AUDIT (8 LINKS / 7 UNIQUE TARGETS): SEC. 301 TARIFF MATH, RBI $239.2B FORWARD BOOK & FEMA 9-MONTH RULE, AI ROUT ($8.5T), PMLA/TBML & MI OPS", title_style))
    story.append(Paragraph("Cross-Examining Section 138 Re-Audit (qa31tANX0tU), Impossible Trinity Liquidity Strains, USTR 154 GW Solar Contradiction, Karnal Singh ED Forensics & IBM H-1B Fact-Check", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7A1C1C'), spaceAfter=6))

    meta_data = [
        [Paragraph("<b>Timestamp:</b> 2026-11-27 16:30 IST", meta_style), Paragraph("<b>Targets:</b> 8 Links (7 Unique; Slot 8 dup)", meta_style), Paragraph("<b>DB Index:</b> Section 198 (198 Total)", meta_style)],
        [Paragraph("<b>Domains:</b> Trade, RBI FEMA, PMLA, CI Ops", meta_style), Paragraph("<b>Verification:</b> RBI, USTR, BoB/CBI, IBM, FCC", meta_style), Paragraph("<b>Upgrade Queue:</b> Phase 462 (Proj. 260/271)", meta_style)]
    ]
    t_meta = Table(meta_data, colWidths=[168, 174, 162])
    t_meta.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')), ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D3D3')), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3), ('LEFTPADDING', (0, 0), (-1, -1), 4)]))
    story.append(t_meta)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Executive Synthesis & Structural Interlocks", h1_style))
    story.append(Paragraph(
        "Auditing 7 unique targets (noting Slot 8 identically duplicates Slot 1 <code>RuBSdqXCqiw</code>) connects four deep stress lines across economics and national security. First, while US tech shed <b>$8.5T since Oct 6</b> and pushed <b>+$13B FII flows</b> into Indian equities (lifting the Rupee from 97 toward 92), India's underlying external buffer shows strain: <b>-$4.9B Sept net FDI outflow</b>, <b>6.1% Oct CPI</b>, <b>+82% gold-loan distress</b>, and <b>$705.34B gross reserves encumbered by a $239.2B net short forward book</b>—forcing the RBI to cut export realization from <b>15 months to 9 months FX (12m INR)</b> while carving out small-ticket <b>Rs. 10L self-declaration relief</b>. Second, Dharmendra Sir proves India's 25% Section 301 levy is net-inclusive (+15%) vs China's stacked 40%, while warning how 154 GW solar capacity and 97% Chinese upstream inputs invited USTR targeting. Third, Ex-ED Chief Karnal Singh and Col Gandotra expose institutional &amp; tactical vulnerability to TBML, CBS bypasses, predictable CI habits, and cantonment shrine cultivation.",
        body_style
    ))

    story.append(Paragraph("2. Multi-Domain Findings & Quarantined Distortions", h1_style))
    story.append(Paragraph("• <b>IBM Consulting Shift &amp; Pseudo-History Myths (<code>RuBSdqXCqiw</code>):</b> IBM ended US H-1B/Green Card sponsorship in Consulting (~3-wk relocation/Dec 31 severance window to IBM India), <i>NOT</i> firing '1.5 lakh Indians overnight' (150,000+ is global Consulting headcount). Confirms Kochi teen Raul John Aju meeting Putin (*AI Journey 2026*), but quarantines Satsangi claims that Sun Tzu is a 'British Mahabharata hoax' (disproved by Han Yinqueshan bamboo slips) and Bitcoin is an XRP gov plot.", bullet_style))
    story.append(Paragraph("• <b>Macro Bubble, Sec. 301 &amp; Impossible Trinity (<code>9TjSNSdiPnA</code>, <code>dZt16wkcGXc</code>, <code>HyAkTlFHNtw</code>):</b> Verifies Oct 6 $8.5T US tech drop, SpaceX FCC 1M-satellite 'Starmind' permit, Riyadh PIF Tower hits (Brent &gt;$94), Tata Trusts vs Chandrasekaran Bombay HC suit, 11–12 Bangladeshi IPL registrants, Nov 13 $705.34B RBI reserves, $239.2B forward book, and Sept 22 FEMA 9m/Rs. 10L rule shift. <i>Quarantined:</i> Sumeet Jain's diversionary 'Pak/BD border war' prophecy and minor Feb 2026 bilateral timeline compression.", bullet_style))
    story.append(Paragraph("• <b>ED/PMLA Financial Forensics &amp; Unconventional MI Ops (<code>GnYmmUkO4qQ</code>, <code>qPpC9eNvUvI</code>, <code>qa31tANX0tU</code>):</b> Synthesizes PMLA predicate offences &amp; Sec. 45/8(8) restitution, domestic vs FEMA hawala, BoB Rs. 6,000 Cr Ashok Vihar Duty-Drawback TBML, PNB CBS-bypass LoUs, Hasan Ali Rs. 48,000 Cr fraud, and Batla House 1-sec CDR + dermal nitrate forensics; plus Kupwara stealth/bus takedowns, cantonment-perimeter shrine cultivation alerts, zero-pattern CI survival, and Annie Jacobsen's Libya-DPRK parable &amp; Devolution bunker disclosure.", bullet_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("3. Comprehensive 7-Target Credibility Scorecard", h1_style))
    rows = [
        [Paragraph("Video ID / Source", th_style), Paragraph("Topic Focus", th_style), Paragraph("Agree", th_style), Paragraph("Rigor", th_style), Paragraph("Reality", th_style), Paragraph("Analytical Verdict", th_style)],
        [Paragraph("<b>GnYmmUkO4qQ</b> (Karnal Singh IPS)", tcb_style), Paragraph("ED, PMLA/FEMA, TBML &amp; Batla", tc_style), Paragraph("<b>93%</b>", tcb_style), Paragraph("95%", tc_style), Paragraph("95%", tc_style), Paragraph("Primary statutory &amp; forensic goldmine on laundering/Batla House", tc_style)],
        [Paragraph("<b>qPpC9eNvUvI</b> (Col B. Gandotra)", tcb_style), Paragraph("Unconventional Ops &amp; MI CI", tc_style), Paragraph("<b>91%</b>", tcb_style), Paragraph("92%", tc_style), Paragraph("93%", tc_style), Paragraph("Verified Kupwara tactics &amp; anti-pattern cantt shrine CI doctrine", tc_style)],
        [Paragraph("<b>dZt16wkcGXc</b> (Gyrus / Dharmendra)", tcb_style), Paragraph("USTR 25% Net vs China 40%", tc_style), Paragraph("<b>89%</b>", tcb_style), Paragraph("91%", tc_style), Paragraph("90%", tc_style), Paragraph("Nails net-vs-stacked tariff math &amp; 154 GW / 97% China solar trap", tc_style)],
        [Paragraph("<b>9TjSNSdiPnA</b> (Palki / IGR LIVE)", tcb_style), Paragraph("$8.5T AI Rout, FDI &amp; Starmind", tc_style), Paragraph("<b>86%</b>", tcb_style), Paragraph("87%", tc_style), Paragraph("89%", tc_style), Paragraph("Accurate market rout, -$4.9B FDI, 6.1% CPI, Tata &amp; PIF Tower", tc_style)],
        [Paragraph("<b>qa31tANX0tU</b> (Jacobsen Re-Audit)", tcb_style), Paragraph("Nuclear 72m, Iran &amp; Devolution", tc_style), Paragraph("<b>84%</b>", tcb_style), Paragraph("86%", tc_style), Paragraph("87%", tc_style), Paragraph("Closed Sec 138 gap: Libya-DPRK parable &amp; Devolution bunkers", tc_style)],
        [Paragraph("<b>HyAkTlFHNtw</b> (Sumeet Jain)", tcb_style), Paragraph("$705B Reserves, $239B &amp; FEMA", tc_style), Paragraph("<b>74%</b>", tcb_style), Paragraph("76%", tc_style), Paragraph("79%", tc_style), Paragraph("Accurate $239.2B forward book &amp; FEMA 9m/Rs.10L; war-spin fault", tc_style)],
        [Paragraph("<b>RuBSdqXCqiw</b> (Alternate Media)", tcb_style), Paragraph("IBM H-1B Reset &amp; AI/Crypto", tc_style), Paragraph("<b>44%</b>", tcb_style), Paragraph("40%", tc_style), Paragraph("42%", tc_style), Paragraph("'1.5L fired overnight' clickbait + Sun Tzu &amp; Bitcoin-XRP myths", tc_style)],
    ]
    t_s = Table(rows, colWidths=[116, 118, 34, 34, 38, 164])
    t_s.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A2B4C')), ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')), ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E5E5')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2), ('LEFTPADDING', (0, 0), (-1, -1), 3)]))
    story.append(t_s)

    story.append(Paragraph("4. Council Titans Directives &amp; Queued Structural Upgrade (Phase 462)", h1_style))
    story.append(Paragraph("• <b>Dr. S. Jaishankar / NSA Doval:</b> Reject US coercion on 154 GW solar/PLI while slashing 97% Chinese wafer reliance, and enforce Col Gandotra's zero-pattern CI entropy and cantonment-perimeter shrine monitoring.", bullet_style))
    story.append(Paragraph("• <b>PM Modi / Dr. Ankit Shah / Sanjeev Sanyal:</b> Respect the Impossible Trinity ($239.2B forward book + 6.1% CPI + $8.5T US AI bleed)—prepay floating loans, don't fall for '1.5L IBM fired' panic, and convert H-1B resets into Indian deep-tech leadership.", bullet_style))
    story.append(Paragraph("• <b>J. Sai Deepak / Dr. Anand Ranganathan:</b> Distinguish Income Tax black money from PMLA Sec. 45 crime proceeds, test historical claims against Han bamboo slips before mocking Sun Tzu, and separate real data from war-diversion spin.", bullet_style))
    story.append(Paragraph(
        "<b>Queued Real Upgrade (Preserves Phase 461 against 258 SRM / 269 Symbols Baseline; Zero Codebase Edits):</b> Stages <b>Phase 462: ImpossibleTrinityForexBookTbmlAndCounterInfiltrationOpsecTensor</b> in <code>UPGRADE_PLANING</code> (projecting <b>260 Resilience Channels / 271 Lens Symbols</b>).",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    shutil.copy2(PROJECT_PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"[OK] Generated {PROJECT_PDF_PATH} ({os.path.getsize(PROJECT_PDF_PATH)/1024:.1f} KB)")
    print(f"[OK] Mirrored to {ARTIFACT_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
