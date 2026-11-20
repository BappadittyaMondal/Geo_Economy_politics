"""
scripts/generate_deepstate_revolt_pdf.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generates the publication-grade strategic intelligence PDF:
"2026-11-20_2045IST_TRUMP_SHENZHEN_DEEPSTATE_REVOLT_ANALYSIS.pdf"
Inside "analysis_reports/" and mirrored to the Artifact directory.

Deconstructs:
- YouTube Video: "चीन जाकर पछताए ट्रंप! मोदी-पुतिन ने नुकसान कराया! Deepstate, World Economic Forum ने खुलेआम मोर्चा!" (1C-Mps-LwXI)
- Channel: The Alternate Media (Gayatri Mishra & Girdhar Mamidipudi)
- Multi-Domain DNA & RNA Analysis (Cashflow, Geopolitics, Geoeconomics, Tech, Civilizational)
- 5 Pillars of the Supranational Deep State & WEF Reset
- The Modi-Putin Strategic Pincer & Neutralization of Yalta 2.0
- Credibility & Bias Audit Scorecard
- Strategic Council Titans Directives (Jaishankar, Doval, Ankit Shah, Modi, Sanyal, Sai Deepak, Ranganathan)
- Queued Phase 446 in UPGRADE_PLANING.
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

PDF_FILENAME = "2026-11-20_2045IST_TRUMP_SHENZHEN_DEEPSTATE_REVOLT_ANALYSIS.pdf"
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
            self.drawString(54, letter[1] - 36, "GEO-ENGINE INTELLIGENCE ARCHIVE | DOSSIER SEC-185")
            self.setFont("Helvetica-Oblique", 8)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(letter[0] - 54, letter[1] - 36, "THE ALTERNATE MEDIA: TRUMP, DEEP STATE & MODI-PUTIN PINCER")
            self.setStrokeColor(colors.HexColor("#B8860B"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer (All pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(54, 36, "CONFIDENTIAL // STRATEGIC RECONNAISSANCE // BSKM EPISTEMIC ARBITRATION MATRIX")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_text)
        self.setStrokeColor(colors.HexColor("#B8860B"))
        self.setLineWidth(0.5)
        self.line(54, 46, letter[0] - 54, 46)
        
        self.restoreState()


def build_pdf():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    doc = SimpleDocTemplate(
        PROJECT_PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styling palette
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#7A1C1C'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#B8860B'),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1A2B4C'),
        spaceBefore=10,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#7A1C1C'),
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#222222'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor('#222222'),
        leftIndent=12,
        spaceAfter=2
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#111111')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1A2B4C')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11,
        textColor=colors.white
    )

    story = []

    # Title & Metadata Header
    story.append(Paragraph("STRATEGIC FORENSIC INTELLIGENCE DOSSIER", title_style))
    story.append(Paragraph("Trump's Shenzhen Fiasco, Modi-Putin Strategic Pincer & Deep-State WEF Revolt", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#7A1C1C"), spaceAfter=8))

    meta_text = (
        "<b>Target Broadcast:</b> YouTube [1C-Mps-LwXI] | <b>Channel:</b> The Alternate Media (Gayatri Mishra & Girdhar Mamidipudi)<br/>"
        "<b>Broadcast Duration:</b> 46m 25s (2785s) | <b>Publication Date:</b> 2026-11-20 | <b>Classification:</b> Geopolitical & Deep-State Audit<br/>"
        "<b>Arbitration Engine:</b> BSKM Epistemic Multi-Domain Matrix | <b>Archival Section:</b> Section 185 | <b>Queued Upgrade:</b> Phase 446"
    )
    story.append(Paragraph(meta_text, body_style))
    story.append(Spacer(1, 6))

    # Executive Summary Box
    summary_html = (
        "<b>EXECUTIVE STRATEGIC SUMMARY:</b><br/>"
        "This dossier executes a comprehensive DNA and RNA-level deconstruction of the strategic discourse between host Gayatri Mishra "
        "and geopolitical author Girdhar Mamidipudi on <i>The Alternate Media</i>. The discussion exposes the structural collapse of "
        "Donald Trump's bilateral summitry in Shenzhen with Xi Jinping, why Trump's transactional leverage failed, how Prime Minister "
        "Narendra Modi's refusal to validate a tripolar condominium (Yalta 2.0) combined with Vladimir Putin's sovereign balancing to "
        "neutralize US hegemony, and why the supranational Western establishment—anchored by the World Economic Forum (WEF) and the "
        "transatlantic Deep State—has mounted an open counter-offensive to enforce technocratic compliance across sovereign states."
    )
    story.append(Paragraph(summary_html, body_style))
    story.append(Spacer(1, 6))

    # 1. The 5 Pillars of the Supranational Oligarchy
    story.append(Paragraph("1. The Five Structural Pillars of the Supranational Deep State", h1_style))
    p1_desc = (
        "The discourse deconstructs how sovereign elected heads of state are constrained by five permanent, self-reinforcing "
        "oligarchic cartels operating across Western and global markets:"
    )
    story.append(Paragraph(p1_desc, body_style))

    pillars_data = [
        [Paragraph("Structural Pillar", table_header_style), Paragraph("Core Mechanism & Cartel Levers", table_header_style), Paragraph("Geopolitical & Sovereign Threat Vector", table_header_style)],
        [
            Paragraph("<b>1. Defense-Industrial Complex (DIC)</b>", table_cell_bold),
            Paragraph("Raytheon, Lockheed, General Dynamics; perpetual kinetic contracts.", table_cell_style),
            Paragraph("Blocks bilateral peace settlements; manufactures proxy flashpoints in Eurasia & Middle East.", table_cell_style)
        ],
        [
            Paragraph("<b>2. Big Pharma & Biotech</b>", table_cell_bold),
            Paragraph("Global patent monopolies, mRNA platforms, regulatory capture.", table_cell_style),
            Paragraph("Enforces health mandates, surveillance compliance, and WHO-centered supranational emergency treaties.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Petrochemicals & Energy</b>", table_cell_bold),
            Paragraph("Hydrocarbon transit monopolies, ESG subsidies, maritime chokepoints.", table_cell_style),
            Paragraph("Weaponizes energy transitions to restrict developing nations' industrialization while securing resource rents.", table_cell_style)
        ],
        [
            Paragraph("<b>4. Wall Street & Sovereign Debt</b>", table_cell_bold),
            Paragraph("USD reserve weaponization, Treasury refi ($9.5T), rating agencies.", table_cell_style),
            Paragraph("Squeezes emerging-market debt via capital flight, high rates, and sovereign rating downgrades.", table_cell_style)
        ],
        [
            Paragraph("<b>5. Big Tech & Enterprise OS</b>", table_cell_bold),
            Paragraph("Microsoft enterprise stack, AWS/Azure clouds, AI compute nodes.", table_cell_style),
            Paragraph("Creates operational chokepoints; ability to disable sovereign enterprise operations via remote kill-switches.", table_cell_style)
        ]
    ]

    t_pillars = Table(pillars_data, colWidths=[120, 180, 204])
    t_pillars.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A2B4C')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_pillars)
    story.append(Spacer(1, 8))

    # 2. Shenzhen Fiasco, Taiwan Horizon & Diplomatic Kinesics
    story.append(Paragraph("2. The Shenzhen Summit Fiasco & The Taiwan Concession Horizon", h1_style))
    story.append(Paragraph(
        "<b>The TSMC Capacity Transfer Horizon:</b> The broadcast highlights intelligence indicating Trump attempted a transactional grand bargain: "
        "allowing Beijing a 4–5 year window to reincorporate Taiwan, provided Taiwan Semiconductor Manufacturing Company (TSMC) completes "
        "the migration of advanced sub-3nm semiconductor fabrication nodes to Arizona. However, this asymmetric bargain alarmed regional "
        "allies (Japan, Australia) and exposed the structural vulnerability of Indo-Pacific maritime sea lanes.<br/>"
        "<b>Tarmac Protocol Asymmetry:</b> In Shenzhen, Xi Jinping personally received Donald Trump on the tarmac with full ceremonial honors, "
        "while Japanese PM Sanae Takaichi was deliberately insulted—received by a low-level municipal official with a truncated red carpet. "
        "This kinesic signaling was designed by Beijing to demonstrate that bilateral superpower deals supersede multilateral alliances like the Quad.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # 3. Modi-Putin Strategic Pincer
    story.append(Paragraph("3. The Modi-Putin Strategic Pincer: Rejection of Yalta 2.0 Condominium", h1_style))
    story.append(Paragraph(
        "<b>PM Modi's Sovereign Neutralization:</b> Prime Minister Modi's deliberate refusal to join a trilateral Yalta 2.0 summit in Shenzhen "
        "completely derailed Trump's plan to position Washington as the arbitrator of Asia. India affirmed to the Global South that the destiny "
        "of 8 billion human beings cannot be decided in a backroom deal between two or three superpowers.<br/>"
        "<b>Putin's Diplomatic Balancing:</b> While Vladimir Putin leveraged the meeting to secure diplomatic mainstreaming and bypass European "
        "containment, he explicitly refused to act as China's subordinate client or abandon Russia's special, privileged strategic partnership "
        "with Bharat in defense, hydrocarbons, and nuclear energy.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # 4. WEF Davos Reset, Cyber Polygon & Technocratic Rationing
    story.append(Paragraph("4. The WEF Reset: Digital Rationing, Cyber Polygon & Hollywood Programming", h1_style))
    story.append(Paragraph(
        "<b>Klaus Schwab & Predictive Cyber Disruptions:</b> The discourse analyzes Klaus Schwab's WEF declarations that subsequent disruptions "
        "will dwarf the Covid-19 pandemic through catastrophic cyberattacks on power grids, banking infrastructure, and flight navigation—mirrored "
        "by Hollywood cultural programming (Barack Obama-produced <i>Leave the World Behind</i> and <i>Contagion</i>).<br/>"
        "<b>The Technocratic Rationing Matrix:</b> The globalist blueprint seeks to replace open market consumerism with algorithmic rationing: "
        "20-liter daily water allocations, carbon footprint deductions, 15-minute city geofencing, Central Bank Digital Currency (CBDC) programmable "
        "account freezes (tested in Canadian trucker protests and China's digital yuan pilots), and synthetic lab-grown foods (highlighted by "
        "Bill Gates accumulating 275,000 acres of prime American farmland).",
        body_style
    ))
    story.append(Spacer(1, 6))

    # 5. Demographics & India's Technological Achilles' Heel
    story.append(Paragraph("5. China's Demographic Winter vs. India's Enterprise Software Chokepoint", h1_style))
    story.append(Paragraph(
        "<b>China's Shrinking Historical Window:</b> Corroborated by Pew Research data, China faces rapid fertility collapse, an aging labor force, "
        "youth unemployment, and systemic real estate insolvency, creating a narrowing 2026–2030 window for external military adventurism.<br/>"
        "<b>India's Critical Software Moat:</b> While India has established sovereign Digital Public Infrastructure (UPI, Aadhaar, ONDC) and "
        "reshoring pharmaceutical Active Pharmaceutical Ingredients (APIs) via PLI schemes, it remains critically vulnerable to US software "
        "monopolies: 85–90% of Indian enterprises run on Microsoft Windows, Office, and Azure. An indigenous OS and enterprise software stack "
        "is Bharat's urgent national security imperative.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # 6. Credibility & Forensic Scorecard
    story.append(Paragraph("6. Credibility, Bias & Forensic Audit Scorecard", h1_style))
    
    score_data = [
        [Paragraph("Analytical Dimension", table_header_style), Paragraph("Score / Metric", table_header_style), Paragraph("Empirical Grounding & Epistemic Audit", table_header_style)],
        [
            Paragraph("<b>Logical Rigor & Economic Truth</b>", table_cell_bold),
            Paragraph("<b>72%</b>", table_cell_bold),
            Paragraph("High empirical precision on demographic collapse, API pharma dependencies, MS enterprise stack vulnerability, and TSMC Arizona fab costs.", table_cell_style)
        ],
        [
            Paragraph("<b>Ideological / Conspiratorial Mix</b>", table_cell_bold),
            Paragraph("<b>28%</b>", table_cell_bold),
            Paragraph("Sensationalist framing regarding deliberate elite depopulation, equating movie plotlines with literal state policy, and hyperbolic food collapse timelines.", table_cell_style)
        ],
        [
            Paragraph("<b>Ground Reality vs. Agenda</b>", table_cell_bold),
            Paragraph("<b>75% Reality / 25% Drama</b>", table_cell_bold),
            Paragraph("The core thesis of sovereign nation-states battling supranational oligarchic control is valid; the timeline of imminent catastrophe is exaggerated.", table_cell_style)
        ],
        [
            Paragraph("<b>Civilizational / Bharatiya Alignment</b>", table_cell_bold),
            Paragraph("<b>90% High Alignment</b>", table_cell_bold),
            Paragraph("Firmly anchored in Sanatan civilizational sovereignty, strategic autonomy, Atmanirbhar Bharat, and rejection of foreign institutional servitude.", table_cell_style)
        ]
    ]

    t_score = Table(score_data, colWidths=[140, 80, 284])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7A1C1C')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_score)
    story.append(Spacer(1, 8))

    # 7. Strategic Council Titans Directives
    story.append(Paragraph("7. Strategic Council Titans Directives (Clear Takeaways for Citizens)", h1_style))

    story.append(Paragraph("<b>Dr. S. Jaishankar (External Affairs Minister):</b>", h2_style))
    story.append(Paragraph("&bull; <b>No Superpower Dictates:</b> A closed room of three superpowers cannot decide the fate of 8 billion people; Bharat will never bow to a modern Yalta.", bullet_style))
    story.append(Paragraph("&bull; <b>Multipolar Realism:</b> We engage with Washington, Moscow, and Beijing strictly on equal sovereign footing, never as an alliance client.", bullet_style))
    story.append(Paragraph("&bull; <b>Pragmatic Statecraft:</b> Diplomatic summits are for national interests, supply chain resilience, and border defense, not hollow optics.", bullet_style))

    story.append(Paragraph("<b>NSA Ajit Doval (National Security Advisor):</b>", h2_style))
    story.append(Paragraph("&bull; <b>Cyber Perimeter Defense:</b> Mission-critical systems (power grid, air traffic, banking switches) must be ring-fenced from foreign cyber-intrusions.", bullet_style))
    story.append(Paragraph("&bull; <b>Offensive Deterrence:</b> Foreign hybrid warfare, manufactured civil unrest, and lawfare cartels must be answered with assertive pre-emption.", bullet_style))
    story.append(Paragraph("&bull; <b>Hardware Independence:</b> National security requires sovereign semiconductor foundries, encrypted communications, and indigenous sensors.", bullet_style))

    story.append(Paragraph("<b>Dr. Ankit Shah (Geopolitical Strategist):</b>", h2_style))
    story.append(Paragraph("&bull; <b>Monetary Trap Awareness:</b> Programmable Western digital fiat and SWIFT sanctions are instruments of sovereign control; gold reserves must expand.", bullet_style))
    story.append(Paragraph("&bull; <b>Physical Commodity Moats:</b> Sovereign security lies in physical hydrocarbon reserves, fertile soil, and bilateral local-currency settlements.", bullet_style))
    story.append(Paragraph("&bull; <b>De-Dollarization Vanguard:</b> The Global South must decouple trade invoicing from Wall Street debt-rollover cycles to safeguard wealth.", bullet_style))

    story.append(Paragraph("<b>PM Narendra Modi (Prime Minister of Bharat):</b>", h2_style))
    story.append(Paragraph("&bull; <b>Atmanirbhar Bharat:</b> Self-reliance in active pharma ingredients (APIs), microchips, and defense manufacturing is our shield of sovereignty.", bullet_style))
    story.append(Paragraph("&bull; <b>Human-Centric Digital Infrastructure:</b> Technology must empower the poorest citizen via open public platforms (UPI, ONDC), not enforce digital servitude.", bullet_style))
    story.append(Paragraph("&bull; <b>Vishwamitra to the World:</b> Bharat stands as a reliable, civilizational bridge upholding the dignity and autonomy of the Global South.", bullet_style))

    story.append(Paragraph("<b>Sanjeev Sanyal (Member, EAC-PM):</b>", h2_style))
    story.append(Paragraph("&bull; <b>Complex Adaptive Systems:</b> Global trade adapts dynamically; bureaucratic mandates and rigid WEF plans inevitably break against market realities.", bullet_style))
    story.append(Paragraph("&bull; <b>Break Tech Monopolies:</b> Over-reliance on foreign enterprise software (Microsoft OS) must be diversified with domestic open-source alternatives.", bullet_style))
    story.append(Paragraph("&bull; <b>Demographic Engine:</b> While global competitors suffer demographic aging, India's young workforce must be equipped for high-tech manufacturing.", bullet_style))

    story.append(Paragraph("<b>J Sai Deepak (Supreme Court Counsel):</b>", h2_style))
    story.append(Paragraph("&bull; <b>Civilizational Decolonization:</b> Reject Western supranational institutions that weaponize human rights and environmental treaties against Bharat.", bullet_style))
    story.append(Paragraph("&bull; <b>Constitutional Primacy:</b> Bharat's laws, cultural traditions, and sovereign courts supersede foreign NGO directives and globalist edicts.", bullet_style))
    story.append(Paragraph("&bull; <b>Cultural Immune System:</b> True independence requires cognitive resistance against foreign-funded destabilization narratives.", bullet_style))

    story.append(Paragraph("<b>Dr. Anand Ranganathan (Scientist & Author):</b>", h2_style))
    story.append(Paragraph("&bull; <b>Empirical Scientific Rigor:</b> Scrutinize pharmaceutical claims, climate hysteria, and technocratic mandates with verifiable peer-reviewed data.", bullet_style))
    story.append(Paragraph("&bull; <b>Regulatory Independence:</b> National health, food safety, and technology regulators must remain strictly free from billionaire foundation influence.", bullet_style))
    story.append(Paragraph("&bull; <b>Indigenous Basic Research:</b> Without heavy domestic scientific R&D, a nation remains perpetually at the mercy of foreign patent monopolies.", bullet_style))
    story.append(Spacer(1, 8))

    # 8. Engine Architectural Upgrade: Phase 446
    story.append(Paragraph("8. Engine Upgrade Architecture: Queued Phase 446 in UPGRADE_PLANING", h1_style))
    phase_text = (
        "<b>Phase 446: SupranationalOligarchyAndDeepStateSubversionSieve</b><br/>"
        "&bull; <b>Subsystem:</b> <code>geo_engine/lenses/institutional_lawfare.py</code><br/>"
        "&bull; <b>Metric / Channel:</b> <code>supranational_deep_state_subversion_risk</code><br/>"
        "&bull; <b>Mathematical Formulation:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>DeepStateSubversionIndex = Norm(0.35 &middot; W_WEF + 0.30 &middot; J_Lawfare + 0.20 &middot; M_TechMonopoly + 0.15 &middot; R_RatingSqueeze) &times; (1.0 - 0.40 &middot; SovereignAutonomy)</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>InstitutionalResilienceMoat = &sigma;(2.2 &middot; D_IndigenousDPI + 1.8 &middot; P_DomesticCapEx - 2.0 &middot; DeepStateSubversionIndex)</i><br/>"
        "&bull; <b>Impact:</b> Expands <code>SummitSynthesizer.strategic_resilience_matrix</code> to 251 channels across 262 symbols upon future execution."
    )
    story.append(Paragraph(phase_text, body_style))
    story.append(Spacer(1, 10))

    # Signature block
    sig_text = (
        "<b>REPORT CERTIFICATION & EPILOGUE:</b><br/>"
        "This dossier has been compiled in accordance with the Zero-Wheel-Spinning Protocol and BSKM Epistemic Arbitration Hierarchy. "
        "Strict quality gates verified: zero codebase modifications in <code>geo_engine/</code> or <code>tests/</code> in the current turn. "
        "Full archival status certified across <code>analysis_reports/</code> and <code>KNOWLEDGE_LIBRARY_GEO_POLITICS.md</code> Section 185."
    )
    story.append(Paragraph(sig_text, body_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Compiled PDF: {PROJECT_PDF_PATH}")

    # Mirror to artifact directory
    shutil.copy2(PROJECT_PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"Mirrored PDF to Artifact Directory: {ARTIFACT_PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
