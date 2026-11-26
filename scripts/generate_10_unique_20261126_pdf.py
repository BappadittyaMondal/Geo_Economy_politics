"""scripts/generate_10_unique_20261126_pdf.py
Compiles publication-grade PDF Intelligence Dossier for Section 196 (11 Links / 10 Unique Targets Audited 2026-11-26 Morning):
analysis_reports/2026-11-26_1000IST_MULTI_DOMAIN_INTELLIGENCE_AUDIT_10_TARGETS.pdf
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

PDF_FILENAME = "2026-11-26_1000IST_MULTI_DOMAIN_INTELLIGENCE_AUDIT_10_TARGETS.pdf"
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
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#7A1C1C"))
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "GEO-ENGINE ARCHIVE | DOSSIER SEC-196")
            self.setFont("Helvetica-Oblique", 7.5)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(letter[0] - 54, letter[1] - 36, "SEC. 301 TARIFFS, RBI TWIN BRAKES, DPDP 2027 & STRATIGRAPHY")
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
    story.append(Paragraph("GEO-ENGINE INTELLIGENCE ARCHIVE | STRATEGIC DOSSIER SEC-196", sub_style))
    story.append(Paragraph("MULTI-DOMAIN DNA AUDIT (11 LINKS / 10 UNIQUE TARGETS): USTR SECTION 301 TARIFFS, RBI TWIN BANKING BRAKES, AI BUBBLE & DPDP MAY 2027, DPRK/EOS-05 & RAMAYANA STRATIGRAPHY", title_style))
    story.append(Paragraph("Cross-Examining Section 195 Claims (ZNVShd2Qy4Y), Banking Safeguards vs Blackout Myths, 2024 Spaced Forecast Decay, and Primary-Text vs Puranic Folk Quarantines", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7A1C1C'), spaceAfter=6))

    meta_data = [
        [Paragraph("<b>Timestamp:</b> 2026-11-26 10:00 IST", meta_style), Paragraph("<b>Targets:</b> 11 Links (10 Unique; Slot 7 dup)", meta_style), Paragraph("<b>DB Index:</b> Section 196 (196 Total)", meta_style)],
        [Paragraph("<b>Domains:</b> Trade 301, RBI NBFC, AI/DPDP, Space, Epics", meta_style), Paragraph("<b>Verification:</b> USTR, RBI, SCOTUS, ISRO, MEA", meta_style), Paragraph("<b>Upgrade Queue:</b> Phase 460 Staged", meta_style)]
    ]
    t_meta = Table(meta_data, colWidths=[168, 174, 162])
    t_meta.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')), ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D3D3')), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3), ('LEFTPADDING', (0, 0), (-1, -1), 4)]))
    story.append(t_meta)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Executive Synthesis & Cross-Batch Interlocks", h1_style))
    story.append(Paragraph(
        "Auditing all 10 unique targets (noting Slot 7 identically duplicates Slot 1 <code>uatz1dTTPQ0</code>) and re-checking Slot 6 (<code>ZNVShd2Qy4Y&amp;t=135s</code>) exposes four critical structural patterns. First, pairing <code>uatz1dTTPQ0</code> against <code>ZNVShd2Qy4Y</code> proves India's November 23, 2026 RBI dual actions—the draft <b>Stop Switch / 1-hour Trusted Person</b> banking framework (which excludes everyday UPI P2P/merchant sweeps) and final <b>Rs. 1 Crore demat-only NBFC securitisation floor</b> effective April 1, 2027—combat domestic cyber-fraud and shadow retail loan slicing rather than preparing for Western 2029–30 blackouts. Second, Washington's November 25, 2026 proposed <b>Section 301 tariffs (25% India, 17% conditional deal)</b> directly target Atmanirbhar Bharat &amp; PLI after SCOTUS struck down IEEPA tariffs on Feb 20, 2026. Third, <b>DPDP Act May 13, 2027</b> enforcement (up to Rs. 250 Cr fines) drives domestic AI workflow localization even as local GPU hardware risks 3-year depreciation and WSJ's AI-bubble warning mounts. Fourth, juxtaposing <code>qwOL9dWveEM</code> against <code>xrBNBZEnRJY</code> proves why Critical Edition primary texts must be separated from later Puranic/Adhyatma Ramayana folklore ('Dacoit Ratnakar').",
        body_style
    ))

    story.append(Paragraph("2. Multi-Domain Findings & Quarantined Distortions", h1_style))
    story.append(Paragraph("• <b>Twin RBI Safeguards &amp; Communal Slur Catch (<code>uatz1dTTPQ0</code> + <code>ZNVShd2Qy4Y</code>):</b> Verifies Nov 23 Draft EBT Directions (Default-Off channels, daily/night limits, Stop Switch freezing outward debits, Dec 14 consultation) + Final NBFC Securitisation Directions (demat PTCs, Rs. 1 Cr initial/secondary floor from Apr 1, 2027, save amortising paydowns). Quarantines Sumeet Jain's communal labeling of scam hubs as 'Jihadi' and Ankit Shah's 2029–30 digital prison blackout leap, while preserving verified London PGI gold and GeM MSME exclusion signals.", bullet_style))
    story.append(Paragraph("• <b>US Cyber/AI Bubble vs Software Bug Conflation (<code>aQv0stk8QY8</code>):</b> Verifies WSJ AI-bubble analysis (25% CapEx growth dependence, 35% equity net worth risk, Anthropic's Nov 19 Nasdaq IPO at $1.5T valuation, Project Stargate $500B), Oct 29 $6.3–6.4B Binance DPRK Lazarus heist, FinCEN &amp; CIA/ODNI OSINT intrusions, and Nov 19 Trump–Xi–Putin Shenzhen summit. <i>Quarantined:</i> Claiming Madhu Gottumukkala was fired 5 days prior (DHS reassigned him Feb 2026) and merging Microsoft Nov 12–14 exchange scaling bugs, FAA Nov 13 L3Harris router ~3,500 flight groundings (not 8,000+), and JPMorgan Nov 16 on-prem bugs into covert cyberwar.", bullet_style))
    story.append(Paragraph("• <b>Section 301 Trade War &amp; DPDP May 2027 AI Sovereignty (<code>q5N0EZ8fEJI</code> &amp; <code>Kf-trFQRZLI</code>):</b> USTR's Nov 25 proposal sets net top-up targets (India 25%/17% deal, Vietnam 35%/20%, China 20%/40% fallback, Japan/EU 15%) for Jan 5–25, 2027 review—leaving a prime Dec 14–15 Miami G20 negotiating lever. Meanwhile, May 13, 2027 DPDP enforcement catalyzes Indian B2B AI compliance workflows, though Tier-3 'petrol pump' GPU hardware rental faces brutal 3-year Nvidia obsolescence unlike high-margin B2B SaaS.", bullet_style))
    story.append(Paragraph("• <b>Space ISR, Pyongyang Envoy &amp; 2024 Spaced Decay (<code>VkLz1OXfV0Y</code>, <code>e_M8Tgin-uI</code>, <code>WD1lizsfRC8</code>):</b> Verifies Sep 4, 2026 ISRO GSLV-F17 / EOS-05 (GISAT-1A, 2,367 kg) 30-min/5-min GEO imaging &amp; cloud limits; Nov 22 Kim Jong Un receiving Amb. Sanjeev Jain among 10 envoys (de-spinning 'India-exclusive' clickbait); and Maj Gen Narayanan's Sept 2024 interview—validating HS 'Nuclear Reactor' bolts/gauges trap &amp; BharOS while correcting his dismissal of Bombay HC's formal FCU Rule 3 strike-down.", bullet_style))
    story.append(Paragraph("• <b>Ramayana Stratigraphy Contrast (<code>qwOL9dWveEM</code> vs <code>xrBNBZEnRJY</code>):</b> <i>Beyond Conscious</i> rigorously separates Nilesh Oak's 12,209 BCE Vega precession math, Critical Edition omission of Bala Kanda 5114 BCE horoscopes, ~800k-yr Asian Gomphotheres extinction, and CSIR-NIO ~8,500-yr Palk Strait data from belief. Conversely, <i>PK Pramas</i> packages later Puranic 'Dacoit Ratnakar' legend and anachronistic royal munim accounting (absent from Valmiki CE, where Valmiki is sage Pracetas's 10th son) as empirical history.", bullet_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("3. Comprehensive 10-Target Credibility Scorecard", h1_style))
    rows = [
        [Paragraph("Video ID / Source", th_style), Paragraph("Topic Focus", th_style), Paragraph("Agree", th_style), Paragraph("Rigor", th_style), Paragraph("Reality", th_style), Paragraph("Analytical Verdict", th_style)],
        [Paragraph("<b>qwOL9dWveEM</b> (Beyond Conscious)", tcb_style), Paragraph("Ramayana Stars, CE &amp; Ram Setu", tc_style), Paragraph("<b>90%</b>", tcb_style), Paragraph("92%", tc_style), Paragraph("91%", tc_style), Paragraph("Elite separation of CE text, fossils, oceanography &amp; faith", tc_style)],
        [Paragraph("<b>q5N0EZ8fEJI</b> (Palki / IGR)", tcb_style), Paragraph("USTR Nov 25 Sec. 301 Tariffs", tc_style), Paragraph("<b>87%</b>", tcb_style), Paragraph("88%", tc_style), Paragraph("89%", tc_style), Paragraph("Exact 25%/17% spread &amp; PLI target; softens Jan 2027 draft window", tc_style)],
        [Paragraph("<b>VkLz1OXfV0Y</b> (Prashant Dhawan)", tcb_style), Paragraph("ISRO GSLV-F17 / EOS-05 GEO", tc_style), Paragraph("<b>86%</b>", tcb_style), Paragraph("88%", tc_style), Paragraph("90%", tc_style), Paragraph("Verified Sep 4 GEO stare, Yaogan-41 parity &amp; cloud limits", tc_style)],
        [Paragraph("<b>uatz1dTTPQ0</b> (Sumeet Jain)", tcb_style), Paragraph("RBI Stop Switch &amp; Rs.1Cr NBFC PTC", tc_style), Paragraph("<b>79%</b>", tcb_style), Paragraph("84%", tc_style), Paragraph("83%", tc_style), Paragraph("Nails UPI exclusion &amp; Rs.1Cr floor; tainted by 'Jihadi' slur", tc_style)],
        [Paragraph("<b>e_M8Tgin-uI</b> (India.com)", tcb_style), Paragraph("Kim Jong Un &amp; Amb. Sanjeev Jain", tc_style), Paragraph("<b>78%</b>", tcb_style), Paragraph("76%", tc_style), Paragraph("84%", tc_style), Paragraph("True Nov 22 protocol shift; hides 9 other concurrent envoys", tc_style)],
        [Paragraph("<b>Kf-trFQRZLI</b> (Rishabh Bidhuri)", tcb_style), Paragraph("DPDP May 2027 &amp; Local AI Hubs", tc_style), Paragraph("<b>76%</b>", tcb_style), Paragraph("75%", tc_style), Paragraph("78%", tc_style), Paragraph("Real May 2027 Rs.250 Cr cliff; overhypes GPU 'petrol pump' ROI", tc_style)],
        [Paragraph("<b>aQv0stk8QY8</b> (Ankit Avasthi)", tcb_style), Paragraph("WSJ AI Crash &amp; US Breaches", tc_style), Paragraph("<b>70%</b>", tcb_style), Paragraph("66%", tc_style), Paragraph("72%", tc_style), Paragraph("Good WSJ/IPO/Binance data; stale CISA Feb firing &amp; bug conflation", tc_style)],
        [Paragraph("<b>WD1lizsfRC8</b> (Gen. Narayanan)", tcb_style), Paragraph("2024 Pre-Quad Geopolitics", tc_style), Paragraph("<b>68%</b>", tcb_style), Paragraph("72%", tc_style), Paragraph("70%", tc_style), Paragraph("Sound HS bolt trap &amp; impulse discipline; dated 2024/FCU ruling miss", tc_style)],
        [Paragraph("<b>ZNVShd2Qy4Y</b> (Dr. Ankit Shah)", tcb_style), Paragraph("Non-Debit Feature &amp; Nvidia Play", tc_style), Paragraph("<b>55%</b>", tcb_style), Paragraph("53%", tc_style), Paragraph("61%", tc_style), Paragraph("Valid PGI gold &amp; GeM 30-45% gate; false blackout causality", tc_style)],
        [Paragraph("<b>xrBNBZEnRJY</b> (PK Pramas)", tcb_style), Paragraph("Ratnakar &amp; Ramayana 'Code'", tc_style), Paragraph("<b>54%</b>", tcb_style), Paragraph("48%", tc_style), Paragraph("42%", tc_style), Paragraph("Strong maryada/tyag ethic inside non-CE Puranic 'reporting' fiction", tc_style)],
    ]
    t_s = Table(rows, colWidths=[116, 118, 34, 34, 38, 164])
    t_s.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A2B4C')), ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')), ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E5E5')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2), ('LEFTPADDING', (0, 0), (-1, -1), 3)]))
    story.append(t_s)

    story.append(Paragraph("4. Council Titans Directives &amp; Queued Structural Upgrade (Phase 460)", h1_style))
    story.append(Paragraph("• <b>Dr. S. Jaishankar / NSA Doval:</b> Leverage Dec 2026 Miami G20 talks against USTR's 25%/17% PLI-targeting proposal while pairing EOS-05 GEO orbital stare and Pyongyang human listening with hardened cyber-hygiene.", bullet_style))
    story.append(Paragraph("• <b>PM Modi / Dr. Ankit Shah / Sanjeev Sanyal:</b> Segregate daily-UPI spending accounts from bulk savings (due to UPI Trusted-Person exclusion), build DPDP-compliant Indian B2B AI workflows ahead of May 2027 instead of fragile GPU hardware bets, and read granular customs lines past 'Nuclear Reactor' labels.", bullet_style))
    story.append(Paragraph("• <b>J. Sai Deepak / Dr. Anand Ranganathan:</b> Reject trade hypocrisy and communal fraud slurs equally, separate Valmiki Critical Edition primary texts from later Puranic Ratnakar folklore, and check dates/bug reports before calling software crashes covert war.", bullet_style))
    story.append(Paragraph(
        "<b>Queued Real Upgrade (Preserves Phases 451–459; Zero Codebase Modification):</b> Rejects single-headline wheel-spinning and stages <b>Phase 460: TariffCapPliSovereigntyDpdpComputeAndTextualStratigraphySieve</b> in <code>UPGRADE_PLANING</code> (projecting <b>263 Resilience Channels / 273 Lens Symbols</b>).",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    shutil.copy2(PROJECT_PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"[OK] Generated {PROJECT_PDF_PATH} ({os.path.getsize(PROJECT_PDF_PATH)/1024:.1f} KB)")
    print(f"[OK] Mirrored to {ARTIFACT_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
