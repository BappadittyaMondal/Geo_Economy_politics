"""
scripts/generate_daily_dispatch_pdf.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generates the publication-grade daily intelligence PDF:
"2026-11-20_0900IST_DAILY_GLOBAL_INTELLIGENCE_DISPATCH.pdf"
Inside "analysis_reports/" and mirrored to the Artifact directory.
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

PDF_FILENAME = "2026-11-20_0900IST_DAILY_GLOBAL_INTELLIGENCE_DISPATCH.pdf"
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
            self.drawString(40, 755, "DAILY STRATEGIC INTELLIGENCE DISPATCH // FIVE PILLARS")
            self.drawRightString(572, 755, "DATE: 2026-11-20 // 09:00 IST")
            self.setStrokeColor(colors.HexColor("#B91C1C"))
            self.setLineWidth(0.75)
            self.line(40, 748, 572, 748)

        # Footer (All pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4B5563"))
        self.setStrokeColor(colors.HexColor("#D1D5DB"))
        self.setLineWidth(0.5)
        self.line(40, 42, 572, 42)
        
        self.drawString(40, 30, "BHARAT STRATEGIC COUNCIL // GEO_ENGINE DAILY DISPATCH")
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
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, leading=24,
        textColor=c_primary, alignment=1, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=14,
        textColor=c_secondary, alignment=1, spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=15,
        textColor=c_primary, spaceBefore=10, spaceAfter=4, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=c_secondary, spaceBefore=6, spaceAfter=3, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11,
        textColor=c_dark, spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=10.5,
        textColor=c_dark, leftIndent=12, firstLineIndent=-8, spaceAfter=2
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
    story.append(Paragraph("DAILY STRATEGIC INTELLIGENCE DISPATCH", title_style))
    story.append(Paragraph("GEOPOLITICAL, GEOECONOMIC, TECHNOLOGICAL, HISTORICAL & CIVILIZATIONAL MULTI-OPTICS", ParagraphStyle('SubSub', parent=subtitle_style, textColor=c_primary, fontSize=10.5, leading=14)))
    story.append(Paragraph("Date: 2026-11-20 // 09:00 IST | Classification: Sovereign Strategic Briefing | Scope: Five Core Pillars", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=1, spaceAfter=8))

    # Executive Summary Box
    summary_html = (
        "<b>EXECUTIVE DISPATCH OVERVIEW:</b> On November 20, 2026, global power dynamics transformed across five interconnected pillars:<br/>"
        "• <b>Geopolitics:</b> G3 Shenzhen trilateral talks (Yalta 2.0) contrast sharply with the Tokyo 2+2 India-Japan pact, granting Japanese Self-Defence Forces historic live-fire missile rights in India.<br/>"
        "• <b>Geoeconomics:</b> IEA World Energy Outlook declares an unprecedented supply shock via Strait of Hormuz chokepoints, as US Sec. Hegseth locks Venezuelan crude to hedge Gulf volatility.<br/>"
        "• <b>Deep-Tech:</b> AI hardware constraints pivot from algorithms to electrical power grids and baseload energy, compounded by Nvidia governance shockwaves.<br/>"
        "• <b>Historical:</b> Japan's live-fire deployment shatters post-1945 pacifist norms; Xi's tarmac hug breaks a 46-year Chinese diplomatic protocol.<br/>"
        "• <b>Civilizational:</b> PM Modi inaugurates the First SCO Civilisational Dialogue Forum at Purana Qila, New Delhi, asserting Eurasian civilizational roots."
    )
    t_box = Table([[Paragraph(summary_html, body_style)]], colWidths=[532])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BOX', (0,0), (-1,-1), 1, c_primary),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 8))

    # Five Pillars Table
    story.append(Paragraph("1. The Five Strategic Pillars of the Day", h1_style))
    pillars = [
        ("1. Geopolitics", "Shenzhen Yalta 2.0 vs. Tokyo 2+2 Live-Fire Pact", 
         "While Trump, Xi, and Putin carve spheres of influence in Shenzhen, India and Japan sign a landmark Letter of Intent (LoI) allowing Japanese Self-Defence Forces to conduct surface-to-ship missile drills in India, cementing 'Design with Japan, Make in India' naval deterrence."),
        ("2. Geoeconomics", "IEA Hormuz Energy Shock & WTO Tariff Spikes", 
         "IEA World Energy Outlook warns of chronic supply chain paralysis through Strait of Hormuz. WTO alerts of surging protectionist tariffs. US Sec. Hegseth concludes Venezuelan oil agreement to dilute Gulf choke exposure."),
        ("3. Deep-Tech", "AI Power Grid Wall & Nvidia Governance Shock", 
         "AI infrastructure bottleneck shifts from compute chips to 50-100 GW electrical power grid capacity. Nvidia key-man risk fallout following Jensen Huang's exit accelerates the India Semiconductor Mission (ISM) in Dholera/Sanand."),
        ("4. Historical", "1945 Yalta Echoes & Post-WWII Pacifist Rupture", 
         "Japan firing live missiles on foreign soil marks the most significant break from post-WWII pacifism since 1945. Xi's tarmac greeting breaks a 46-year Chinese diplomatic convention dating back to 1980."),
        ("5. Civilizational", "SCO Conclave at Purana Qila & Eurasian Dharma", 
         "PM Modi inaugurates the 1st SCO Civilisational Dialogue Forum at Indraprastha (Purana Qila), asserting that Eurasian integration must be grounded in civilizational statehood rather than Western universalist dogma.")
    ]

    p_data = [[Paragraph("<b>Pillar</b>", table_header), Paragraph("<b>Key Strategic Event</b>", table_header), Paragraph("<b>Forensic Deconstruction & Cashflow/Power Optics</b>", table_header)]]
    for pil, ev, desc in pillars:
        p_data.append([
            Paragraph(f"<b>{pil}</b>", table_cell_bold),
            Paragraph(ev, table_cell_bold),
            Paragraph(desc, table_cell)
        ])
    t_pillars = Table(p_data, colWidths=[65, 145, 322])
    t_pillars.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_pillars)
    story.append(Spacer(1, 8))

    # Strategic Council Directives
    story.append(Paragraph("2. Strategic Council Titans Directives for General Citizens", h1_style))
    titans = [
        ("Dr. S. Jaishankar", "The weaponization of trade and tech proves globalization is dead. Our 2+2 missile agreement with Japan gives Bharat hard deterrence without joining military blocs."),
        ("NSA Ajit Doval", "Japanese missile crews training in India sends an unmistakable kinetic signal to Beijing. Security cannot be outsourced to foreign summits; indigenous defense is non-negotiable."),
        ("Dr. Ankit Shah", "The IEA Hormuz alert and US reliance on Venezuelan crude confirm that the petrodollar is cracking. Real wealth lies in physical energy reserves and domestic manufacturing."),
        ("PM Narendra Modi", "At Purana Qila, we remind the world that Eurasia's true foundation is ancient civilizational harmony, backed by the self-reliant industrial power of Atmanirbhar Bharat."),
        ("Sanjeev Sanyal", "The WTO tariff surge shows protectionism is the new global baseline. Indian banks with record-low NPAs and domestic PLI manufacturing are built to thrive in this volatility."),
        ("J Sai Deepak", "The SCO forum at Indraprastha marks a historic decolonial milestone. Bharat's statecraft must be derived from Sanatan Dharmic jurisprudence, not European legal templates."),
        ("Dr. Anand Ranganathan", "Track the physical metrics: how many missile batteries are deployed? How many barrels of crude bypass Hormuz? Hard data exposes diplomatic spin every time.")
    ]
    for name, text in titans:
        story.append(Paragraph(f"<b>• {name}:</b> {text}", bullet_style))

    story.append(Spacer(1, 8))

    # Micro-Signals Box
    story.append(Paragraph("3. Micro-Signals & Sub-Surface Grayzones", h1_style))
    signals = [
        ("Live-Fire Missile Trajectory", "Permitting Japanese forces to test surface-to-ship missiles on Indian ranges operationalizes Quad interoperability into actual kinetic deterrence."),
        ("The AI Power Grid Chokepoint", "AI scaling now faces an energy wall: transformer shortages, copper supply constraints, and grid interconnection queues have overtaken GPU shortages.")
    ]
    for tit, dsc in signals:
        story.append(Paragraph(f"<b>• {tit}:</b> {dsc}", body_style))

    # Build
    doc.build(story, canvasmaker=NumberedCanvas)
    shutil.copy2(PROJECT_PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"[OK] Daily Dispatch PDF generated at: {PROJECT_PDF_PATH}")
    print(f"[OK] Mirrored at: {ARTIFACT_PDF_PATH}")
    print(f"Size: {os.path.getsize(PROJECT_PDF_PATH):,} bytes")


if __name__ == "__main__":
    build_pdf()
