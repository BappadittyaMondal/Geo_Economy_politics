"""scripts/generate_6_targets_20261126_night_pdf.py
Compiles publication-grade PDF Intelligence Dossier for Section 197 (6 Targets Audited 2026-11-26 Night):
analysis_reports/2026-11-26_2145IST_MULTI_DOMAIN_INTELLIGENCE_AUDIT_6_TARGETS.pdf
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

PDF_FILENAME = "2026-11-26_2145IST_MULTI_DOMAIN_INTELLIGENCE_AUDIT_6_TARGETS.pdf"
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
            self.drawString(54, letter[1] - 36, "GEO-ENGINE ARCHIVE | DOSSIER SEC-197")
            self.setFont("Helvetica-Oblique", 7.2)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(letter[0] - 54, letter[1] - 36, "60T GOLD REPATRIATION, LONDON PGI/LLOYD'S, COGNITIVE SPOOFING & PROVENANCE")
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
    story.append(Paragraph("GEO-ENGINE INTELLIGENCE ARCHIVE | STRATEGIC DOSSIER SEC-197", sub_style))
    story.append(Paragraph("MULTI-DOMAIN DNA AUDIT (6 TARGETS): RBI 60-TONNE GOLD REPATRIATION VS. LONDON PGIs & LLOYD'S WAR-RISK, DIASPORA BRAND-HIJACK SPOOFING & MONUMENT PROVENANCE", title_style))
    story.append(Paragraph("Cross-Examining ZNVShd2Qy4Y & WD1lizsfRC8 Anchors Against Nov 25 RBI Reserve Filings, Prothom Alo/PTI/Factly Verification, Hormuz Marine Premia & Stone/Timeline Precision", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7A1C1C'), spaceAfter=6))

    meta_data = [
        [Paragraph("<b>Timestamp:</b> 2026-11-26 21:45 IST", meta_style), Paragraph("<b>Targets:</b> 6 Links (4 New + 2 Anchors)", meta_style), Paragraph("<b>DB Index:</b> Section 197 (197 Total)", meta_style)],
        [Paragraph("<b>Domains:</b> Gold, Marine P&amp;I, InfoWar, Culture", meta_style), Paragraph("<b>Verification:</b> RBI Nov 25, PIB, PTI, Prothom Alo", meta_style), Paragraph("<b>Upgrade Queue:</b> Phase 461 Staged", meta_style)]
    ]
    t_meta = Table(meta_data, colWidths=[168, 174, 162])
    t_meta.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')), ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D3D3')), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3), ('LEFTPADDING', (0, 0), (-1, -1), 4)]))
    story.append(t_meta)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Executive Synthesis & The London Custody Paradox", h1_style))
    story.append(Paragraph(
        "Cross-auditing <code>xYlarfz0KZI</code> (DEF Talks) directly against anchor <code>ZNVShd2Qy4Y</code> (Dr. Ankit Shah) and <code>ozCwyuUIdaE</code> (Sattology) exposes the core November 2026 sovereign bullion paradox. According to the <b>RBI Half-Yearly Foreign Exchange Reserves Report (Nov 25, 2026)</b>, India shifted another <b>60.08 metric tonnes</b> of gold home between March and September 2026, boosting domestic vaulting from <b>680t (77%)</b> to <b>740.13t (84%)</b> of its <b>880.52t</b> reserves (up from 301t / 38% in March 2023), leaving ~140.39t (~16%) offshore. Precisely as central banks pull physical bars out of London custody following Russia's EUR 210–260B freeze and Venezuela's $2B Bank of England dispute, City of London bullion clearers (WGC/HSBC/JPMorgan/StoneX) launched digital <b>Pooled Gold Interests (PGIs)</b> to sustain synthetic liquidity while London still leverages ~38% global FX turnover and ~36% specialty marine insurance. Meanwhile, <code>ZiyS8bivvIU</code> confirms multi-node anti-India spoofing, while <code>vZEY0HdnjA0</code> and <code>ozCwyuUIdaE</code> yield concrete geographic, legislative, and numerical errors requiring quarantine.",
        body_style
    ))

    story.append(Paragraph("2. Multi-Domain Findings & Verified Discrepancy Quarantines", h1_style))
    story.append(Paragraph("• <b>Sovereign Gold Repatriation &amp; London PGI/Marine Rent (<code>xYlarfz0KZI</code> + <code>ZNVShd2Qy4Y</code> + <code>ozCwyuUIdaE</code>):</b> Verifies RBI's 60.08t home shift (740.13t / 84% in India; 140.39t abroad for liquidity), City of London's 1.12 sq mi status, Bank of England (1694), Lloyd's ~36% specialty insurance, ~38% FX turnover, offshore RMB clearing, and Sullivan-Hickel's 100–165M colonial mortality literature. <i>Quarantined inside ozCwyuUIdaE:</i> Inflating Hormuz war-risk premia to '$65M per ship' (verified 2026 conflict peaks hit 3.5%–10% of H&amp;M hull value = ~$3.5M–$12.5M+ per VLCC/LNG transit), alleging British-bank rebate collusion with Iran, framing the 1992 NCM Act (1993 notification + 2014 Jains) as an Orsini splinter plot, and declaring 'Putin's victory over London'.", bullet_style))
    story.append(Paragraph("• <b>Anti-India Cognitive Spoofing &amp; Diaspora Brand Hijacking (<code>ZiyS8bivvIU</code> + <code>WD1lizsfRC8</code>):</b> Verifies <i>Prothom Alo</i>'s Nov 6, 2026 expose of ~150 Chinese streamers in Uttara/Dhaka filming drains as 'New Delhi / Maa Ganga', July 2026 Delhi Police blocking ~480 Pakistani AI/deepfake handles, PTI Fact Check (Japan 'Pramod Rathore' = Pakistani Afzal Muhammad), Greek Kos June 2023 case (Polish victim Anastazja Rubinska 27, Bangladeshi perpetrator Salahuddin S.), Factly-verified Korean creator Sumin Dhaka/Varanasi splice, Toronto operator Sadiq Ali's paid Telegram amplification, and Pakistani/Bangladeshi restaurants using 'Indian Restaurant / Sydney Lal Qila' GI signage—plus Gen. Narayanan's anti-impulsive 'Ranting Wing' warning.", bullet_style))
    story.append(Paragraph("• <b>Civilizational Monument Provenance &amp; Timeline Quarantine (<code>vZEY0HdnjA0</code>):</b> Pushpendra Kulshrestha accurately highlights P.V. Narasimha Rao's Bharat Ratna and Netaji Bose canopy reclamation, <i>BUT</i> commits two factual errors: (1) claims the 28-foot granite came from <b>Chhattisgarh</b> (PIB confirms 280-MT black granite came from <b>Khammam, Telangana</b>); and (2) implies Modi removed King George V directly in 2022 (George V's statue was relocated to Coronation Park in <b>1968</b>, leaving an empty canopy for 54 years).", bullet_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("3. Comprehensive 6-Target Credibility Scorecard", h1_style))
    rows = [
        [Paragraph("Video ID / Source", th_style), Paragraph("Topic Focus", th_style), Paragraph("Agree", th_style), Paragraph("Rigor", th_style), Paragraph("Reality", th_style), Paragraph("Analytical Verdict", th_style)],
        [Paragraph("<b>xYlarfz0KZI</b> (DEF Talks / Aadi)", tcb_style), Paragraph("RBI 60t Gold Return &amp; 84% Vaulting", tc_style), Paragraph("<b>91%</b>", tcb_style), Paragraph("91%", tc_style), Paragraph("94%", tc_style), Paragraph("Exact Nov 25 RBI 60.08t / 740.13t / 880.52t reserves &amp; custody logic", tc_style)],
        [Paragraph("<b>ZiyS8bivvIU</b> (The Pamphlet Ep.6)", tcb_style), Paragraph("Dhaka/Pak InfoWar &amp; Brand Hijack", tc_style), Paragraph("<b>87%</b>", tcb_style), Paragraph("86%", tc_style), Paragraph("89%", tc_style), Paragraph("High-rigor Prothom Alo, Delhi Police 480, PTI/Factly &amp; GI verification", tc_style)],
        [Paragraph("<b>vZEY0HdnjA0</b> (Pushpendra / Prakhar)", tcb_style), Paragraph("Rao Bharat Ratna &amp; Bose Canopy", tc_style), Paragraph("<b>68%</b>", tcb_style), Paragraph("64%", tc_style), Paragraph("66%", tc_style), Paragraph("Sound symbolic argument marred by Chhattisgarh &amp; 1968 errors", tc_style)],
        [Paragraph("<b>WD1lizsfRC8</b> (Gen. Narayanan)", tcb_style), Paragraph("2024 Quad &amp; Cognitive Discipline", tc_style), Paragraph("<b>68%</b>", tcb_style), Paragraph("72%", tc_style), Paragraph("70%", tc_style), Paragraph("Strong Ranting-Wing &amp; HS-bolt discipline; dated 2024/FCU error", tc_style)],
        [Paragraph("<b>ZNVShd2Qy4Y</b> (Dr. Ankit Shah)", tcb_style), Paragraph("Stop Switch &amp; London PGI Gold", tc_style), Paragraph("<b>55%</b>", tcb_style), Paragraph("53%", tc_style), Paragraph("61%", tc_style), Paragraph("Valid PGI gold &amp; GeM 30-45% gate; wrong RBI blackout causality", tc_style)],
        [Paragraph("<b>ozCwyuUIdaE</b> (Sattology)", tcb_style), Paragraph("City of London, Lloyd's &amp; Reset", tc_style), Paragraph("<b>48%</b>", tcb_style), Paragraph("45%", tc_style), Paragraph("50%", tc_style), Paragraph("Real 1.12 sq mi / FX / Hickel base drowned in $65M/ship &amp; Orsini plots", tc_style)],
    ]
    t_s = Table(rows, colWidths=[116, 118, 34, 34, 38, 164])
    t_s.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A2B4C')), ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')), ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E5E5')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2), ('LEFTPADDING', (0, 0), (-1, -1), 3)]))
    story.append(t_s)

    story.append(Paragraph("4. Council Titans Directives &amp; Queued Structural Upgrade (Phase 461)", h1_style))
    story.append(Paragraph("• <b>Dr. S. Jaishankar / NSA Doval:</b> Defend overseas Brand India against hostile restaurant identity hijacking via chamber GI certification, counter Dhaka/Toronto bot campaigns with primary proof rather than racial counter-slurs, and pair physical gold vaulting (84%) with cyber-hygiene.", bullet_style))
    story.append(Paragraph("• <b>PM Modi / Dr. Ankit Shah / Sanjeev Sanyal:</b> Track both sides of London bullion—Britain scaling paper PGIs as Bharat repatriates 60t home—while checking marine war-risk math (3.5–10% = $3.5M–$12.5M, not $65M/ship) and building Indian maritime P&amp;I underwriting autonomy.", bullet_style))
    story.append(Paragraph("• <b>J. Sai Deepak / Dr. Anand Ranganathan:</b> Cite the 1992 NCM Act (5 groups + 2014 Jains) accurately without Orsini conspiracy leaps, and check monument dates/stone origins (Khammam Telangana granite; King George V moved in 1968) before speaking.", bullet_style))
    story.append(Paragraph(
        "<b>Queued Real Upgrade (Baseline 258 SRM / 269 Symbols Intact; Zero Codebase Modification):</b> Rejects duplicate Dhaka-spoof &amp; anchor wheel-spinning and stages <b>Phase 461: PhysicalBullionRepatriationMarineInsuranceAndBrandIdentitySovereigntyTensor</b> in <code>UPGRADE_PLANING</code> (projecting <b>259 Resilience Channels / 270 Lens Symbols</b>).",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    shutil.copy2(PROJECT_PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"[OK] Generated {PROJECT_PDF_PATH} ({os.path.getsize(PROJECT_PDF_PATH)/1024:.1f} KB)")
    print(f"[OK] Mirrored to {ARTIFACT_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
