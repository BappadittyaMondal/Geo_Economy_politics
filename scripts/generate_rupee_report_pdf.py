"""
scripts/generate_rupee_report_pdf.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generates the publication-grade intelligence PDF:
"2026-11-20_2015IST_SOVEREIGN_RUPEE_PARADOX_CEA_ANALYSIS.pdf"
Inside "analysis_reports/" and mirrored to the Artifact directory.

Deconstructs:
- Moneycontrol: The Rupee may have fallen too far & stock market impacts
- Economic Times: CEA V. Anantha Nageswaran on why India must fear a stronger rupee
- ET BFSI: Rupee defies global risk aversion as $12B FII flows rotate into Indian assets
- The Hindu: Rupee settles at 92.67 (strongest in 7 months) on FII inflows
- Strategic Council Titans Directives (7 Mentors)
- Queued Phase 445 in UPGRADE_PLANING.
"""

import os
import sys
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(REPO_ROOT, "analysis_reports")
ARTIFACT_DIR = r"C:\Users\BAPPADITYA\.gemini\antigravity\brain\50a153d3-ad4a-410f-9d77-a0092c7f65d3"

PDF_FILENAME = "2026-11-20_2015IST_SOVEREIGN_RUPEE_PARADOX_CEA_ANALYSIS.pdf"
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
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(40, 755, "STRATEGIC INTELLIGENCE DOSSIER // THE SOVEREIGN RUPEE PARADOX")
            self.drawRightString(572, 755, "DATE: 2026-11-20 // 20:15 IST")
            self.setStrokeColor(colors.HexColor("#B91C1C"))
            self.setLineWidth(0.75)
            self.line(40, 748, 572, 748)

        # Footer (All pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4B5563"))
        self.setStrokeColor(colors.HexColor("#D1D5DB"))
        self.setLineWidth(0.5)
        self.line(40, 42, 572, 42)
        
        self.drawString(40, 30, "BHARAT STRATEGIC COUNCIL // GEO_ENGINE GEOFACIAL AUDIT")
        self.drawRightString(572, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    
    doc = SimpleDocTemplate(
        PROJECT_PDF_PATH,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor("#991B1B")     # Dark Crimson
    c_secondary = colors.HexColor("#1E3A8A")   # Deep Navy
    c_dark = colors.HexColor("#111827")        # Charcoal Near Black
    c_light_bg = colors.HexColor("#F9FAFB")    # Off-white
    c_callout_bg = colors.HexColor("#FEF2F2")  # Crimson wash
    c_navy_bg = colors.HexColor("#EFF6FF")     # Blue wash
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, leading=24,
        textColor=c_primary, alignment=1, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=c_secondary, alignment=1, spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12.5, leading=16,
        textColor=c_primary, spaceBefore=10, spaceAfter=5, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=c_secondary, spaceBefore=6, spaceAfter=3, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11.5,
        textColor=c_dark, spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=11,
        textColor=c_dark, leftIndent=12, firstLineIndent=-8, spaceAfter=2.5
    )
    table_cell = ParagraphStyle(
        'Cell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7, leading=9.5, textColor=c_dark
    )
    table_cell_bold = ParagraphStyle(
        'CellBold', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7, leading=9.5, textColor=c_dark
    )
    table_header = ParagraphStyle(
        'Header', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=colors.white, alignment=1
    )

    story = []

    # Title & Header
    story.append(Paragraph("THE SOVEREIGN RUPEE PARADOX & THE $12B FII ROTATION", title_style))
    story.append(Paragraph("CEA V. ANANTHA NAGESWARAN'S WARNING, GLOBAL ASSET ROTATION & THE GEOFACIAL MOATS OF FX VALUATION", ParagraphStyle('SubSub', parent=subtitle_style, textColor=c_primary, fontSize=11, leading=14.5)))
    story.append(Paragraph("Date: 2026-11-20 // 20:15 IST | Classification: Sovereign Geofinancial Intelligence | Focus: INR Valuation Dynamics", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=1, spaceAfter=8))

    # Executive Summary Box
    summary_html = (
        "<b>EXECUTIVE INTELLIGENCE SUMMARY:</b> In late November 2026, the Indian Rupee staged an aggressive recovery, strengthening past the 93 threshold "
        "to settle at <b>92.67</b> (a 7-month high), lifting the INR by 1.75% this month as Asia's top-performing currency. This surge was propelled by "
        "<b>over $12 Billion in net FII inflows</b>, as global capital actively de-risked from overstretched Silicon Valley AI tech equities and rotated into "
        "Indian manufacturing and infrastructure assets. Amid this euphoria, Chief Economic Advisor (CEA) Dr. V. Anantha Nageswaran delivered a crucial strategic "
        "warning at FICCI's AGM: <b>India's core macroeconomic challenge in FY28 will not be currency depreciation, but managing the structural damage of an "
        "overly strong rupee on labor-intensive MSME exporters and the $250B+ IT services sector</b>. The RBI now faces an intricate macro-prudential sterilization "
        "task: absorbing surplus dollars into its $680B+ reserves without allowing unchecked currency appreciation to undermine Atmanirbhar Bharat."
    )
    t_box = Table([[Paragraph(summary_html, body_style)]], colWidths=[532])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BOX', (0,0), (-1,-1), 1, c_primary),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 8))

    # Section 1: The Four Intelligence Sources Deconstruction
    story.append(Paragraph("1. Micro-Forensic Deconstruction of the 4 Source Intelligence Inputs", h1_style))
    sources_data = [
        ("Moneycontrol Opinion", "The Rupee May Have Fallen Too Far", 
         "<b>Currency Overshoot & Equity Inflection:</b> When the INR slipped past 94 earlier in 2026, it overshot underlying economic fundamentals, becoming deeply undervalued on a REER basis. A currency that has 'fallen too far' triggers an asymmetric inflection: as currency risk evaporates, foreign institutional investors re-enter equities, driving technical multiple expansion."),
        ("Economic Times (CEA Speech)", "Should India Wish for a Stronger Rupee? - CEA Nageswaran", 
         "<b>The Strong Rupee Paradox:</b> Speaking at FICCI, CEA Dr. V. Anantha Nageswaran warned that FY28's challenge will be managing currency strength. While cheaper Brent crude (<$80/bbl) and strong capital inflows boost the rupee, rapid appreciation threatens export competitiveness, squeezing margins for IT services and labour-intensive manufacturers (textiles, gems, leather)."),
        ("ET BFSI (Nimesh Vora)", "Global Risk Jitters Bolster Rupee as Investors Turn to India", 
         "<b>The Great Asset Rotation:</b> Foreign investors poured over $800M in a single day, pushing monthly FII purchases past $12 Billion. Despite global risk aversion and a strong US Dollar Index, the Rupee emerged as Asia's top performer (+1.75%), driven by capital rotating out of the overvalued US AI tech trade into Indian domestic equities."),
        ("The Hindu Business", "Rupee Settles Above 93 Level After 7 Months on FII Inflows", 
         "<b>Sovereign FX Settlement Milestone:</b> The Rupee strengthened past 93, closing at 92.67 provisionally—its highest close since April 10. Supported by Sensex/Nifty rallies, falling crude oil import bills, and a softening Dollar Index, completing a multi-session winning streak.")
    ]

    t_src_data = [[Paragraph("<b>Source / Outlet</b>", table_header), Paragraph("<b>Headline & Focus</b>", table_header), Paragraph("<b>Forensic Cashflow & Macroeconomic Mechanism</b>", table_header)]]
    for s, h, d in sources_data:
        t_src_data.append([
            Paragraph(f"<b>{s}</b>", table_cell_bold),
            Paragraph(h, table_cell_bold),
            Paragraph(d, table_cell)
        ])
    t_src = Table(t_src_data, colWidths=[105, 125, 302])
    t_src.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_src)
    story.append(Spacer(1, 8))

    # Section 2: Mathematical Trade-off Table
    story.append(Paragraph("2. The Dual-Edged Sword: Macroeconomic Impact Matrix of Rupee Appreciation", h1_style))
    matrix_data = [
        ("Crude Oil & Energy Imports", "Positive (+)", "Every $1/bbl drop in Brent crude saves India ~$1.5B annually; an appreciating rupee compounds import bill reductions and eases headline CPI inflation."),
        ("External Debt Servicing", "Positive (+)", "Slashes rupee funding requirements for corporate external commercial borrowings (ECBs) and sovereign external debt obligations."),
        ("Equity Inflows (FII)", "Positive (+)", "Eliminates FX hedging drag; foreign asset allocators gain currency appreciation on top of equity index returns."),
        ("Labor-Intensive MSME Exports", "Hazard (-)", "Textiles, apparel, leather, and gems operate on 4-6% margins; rupee appreciation causes immediate market share loss to Vietnam, Bangladesh, and Indonesia."),
        ("IT / ITeS Services Exports", "Hazard (-)", "Revenues billed in USD while operating employee costs are in INR; a 1% rupee appreciation compresses operating EBITDA margins by 25-35 basis points."),
        ("RBI Sterilization Burden", "Operational Risk", "Absorbing $12B+ in foreign inflows injects massive domestic rupee liquidity, requiring aggressive Market Stabilization Scheme (MSS) bond sales.")
    ]
    t_mat_data = [[Paragraph("<b>Economic Domain</b>", table_header), Paragraph("<b>Directional Impact</b>", table_header), Paragraph("<b>Balance Sheet & Cash Flow Reality</b>", table_header)]]
    for dom, imp, dsc in matrix_data:
        t_mat_data.append([
            Paragraph(f"<b>{dom}</b>", table_cell_bold),
            Paragraph(f"<b>{imp}</b>", table_cell_bold),
            Paragraph(dsc, table_cell)
        ])
    t_mat = Table(t_mat_data, colWidths=[115, 75, 342])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_mat)
    story.append(Spacer(1, 8))

    # Section 3: Strategic Council Titans Directives
    story.append(Paragraph("3. Strategic Council Titans Directives for General Citizens", h1_style))
    titans = [
        ("Dr. S. Jaishankar (External Affairs Minister)", [
            "Currency valuation is not a trophy of national pride; it is an instrument of sovereign trade statecraft.",
            "Bharat must avoid the colonial mindset of measuring national dignity against the dollar exchange rate.",
            "We calibrate our currency to protect domestic MSME producers while expanding Rupee-settled bilateral trade corridors."
        ]),
        ("NSA Ajit Doval (National Security Advisor)", [
            "Volatile currency swings are an active vector for foreign speculative attacks and short-seller manipulation.",
            "A sudden flood of $12B in hot money can create asset bubbles that burst if geopolitical tensions spike.",
            "The RBI's $680B+ reserves are our national security fortress against external economic extortion."
        ]),
        ("Dr. Ankit Shah (Geofinancial Strategist)", [
            "Smart global money is fleeing the US $9.5T debt cliff and overinflated AI stocks, rotating into real Indian assets.",
            "CEA Nageswaran is 100% correct: a runaway strong rupee kills our exports and causes domestic deindustrialization.",
            "The RBI must aggressively buy incoming dollars, convert them into physical gold bullion, and keep the rupee competitively priced."
        ]),
        ("PM Narendra Modi (Prime Minister of Bharat)", [
            "The strength of Bharat's economy comes from our 1.4 billion citizens, our farmers, and our MSME entrepreneurs.",
            "Lower crude prices and foreign investments must translate into cheaper logistics and manufacturing jobs for our youth.",
            "We will never allow currency volatility to harm our textile weavers, leather artisans, or small manufacturers (Yogakshema)."
        ]),
        ("Sanjeev Sanyal (Member, EAC-PM)", [
            "Classic economics mistakenly celebrates a strong currency; East Asian giants grew by keeping currencies deliberately competitive.",
            "Nageswaran's warning is vital: we must prevent Dutch Disease where hot capital flows deindustrialize our manufacturing base.",
            "Our complex adaptive strategy balances import inflation relief with export competitiveness through dynamic RBI sterilization."
        ]),
        ("J Sai Deepak (Advocate, Supreme Court of Bharat)", [
            "Colonized post-independence economists viewed the rupee with an inferiority complex, worshipping the pound and dollar.",
            "Decolonial thinking understands Artha through domestic productive capacity and community welfare, not foreign FX rates.",
            "Sovereign currency autonomy means building local-currency trade ecosystems grounded in Sanatan Arthashastra principles."
        ]),
        ("Dr. Anand Ranganathan (Scientist & Author)", [
            "Empirical evidence proves there is no free lunch in economics: what benefits oil refiners hurts IT and textile exporters.",
            "When the rupee gains 2%, test the corporate EBITDA margins: TCS and Infosys take a direct hit while airlines rejoice.",
            "Demand hard mathematical data on REER and export elasticity rather than emotional television applause."
        ])
    ]

    for name, points in titans:
        story.append(Paragraph(f"<b>• {name}</b>", h2_style))
        for pt in points:
            story.append(Paragraph(f"– {pt}", bullet_style))
        story.append(Spacer(1, 1.5))

    story.append(Spacer(1, 8))

    # Section 4: Micro-Signals & Cultural Grayzones
    story.append(Paragraph("4. Micro-Signals, Cultural Grayzones & Queued Upgrade (Phase 445)", h1_style))
    signals = [
        ("The 'Prestige Currency' Cultural Trap", 
         "In post-colonial societies, currency appreciation is emotionally celebrated as national strength, while depreciation is mourned. "
         "CEA Nageswaran's public intervention is a vital cognitive correction: mercantilist powers dominate through competitive currencies."),
        ("The Silicon-to-Bharat Capital Rotation", 
         "The $12B FII surge reflects institutional fatigue with unmonetized Silicon Valley AI hype, redirecting liquidity into Bharat's physical infrastructure."),
        ("Phase 445 Queued in UPGRADE_PLANING", 
         "<i>CurrencyAppreciationExportFrictionAndREERTensor:</i> Formulates appreciation export friction: "
         "<code>AppreciationExportFriction = Norm(0.45·ITMarginCompression + 0.35·MSMECompetitivenessLoss + 0.20·(REER-100)+)</code>.")
    ]
    for tit, dsc in signals:
        story.append(Paragraph(f"<b>• {tit}:</b> {dsc}", body_style))

    # Build
    doc.build(story, canvasmaker=NumberedCanvas)
    shutil.copy2(PROJECT_PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"[OK] Rupee Report PDF generated at: {PROJECT_PDF_PATH}")
    print(f"[OK] Mirrored at: {ARTIFACT_PDF_PATH}")
    print(f"Size: {os.path.getsize(PROJECT_PDF_PATH):,} bytes")


if __name__ == "__main__":
    build_pdf()
