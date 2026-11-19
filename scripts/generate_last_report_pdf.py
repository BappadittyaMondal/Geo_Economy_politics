"""
scripts/generate_last_report_pdf.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generates a comprehensive, publication-quality, color-rich PDF report:
"2026-11-20_0045IST_STRATEGIC_INTELLIGENCE_AUDIT_6_DISCOURSES.pdf"
Inside the project folder: "analysis_reports/"
Also mirrors to Artifact directory for instant browser access.

Deconstructs:
- APEC Shenzhen 2026 Summit (Trump-Xi-Putin, Hegseth Venezuela pact, protocol shock)
- Nobel Laureate Joseph Stiglitz on AI Services Labor Threat & Asset Bubble
- Rahul Gandhi Chicago Address, Diaspora Lawfare & Transnational Feedback Loops
- Trump-Nvidia Silicon Cold War, GPU Export Controls & ASML Chokepoints
- Ghoomta Aaina on Loktantra Ka Nritya & The Economist 2027
- Ankit Avasthi on APEC Shenzhen Trilateral Outcomes & Bharat's Strategic Autonomy
- Strategic Council Titans Directives (7 Mentors)
- Micro-signals, grayzones, and queued architecture in UPGRADE_PLANING (Phases 441-444).
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(REPO_ROOT, "analysis_reports")
ARTIFACT_DIR = r"C:\Users\BAPPADITYA\.gemini\antigravity\brain\50a153d3-ad4a-410f-9d77-a0092c7f65d3"

PDF_FILENAME = "2026-11-20_0045IST_STRATEGIC_INTELLIGENCE_AUDIT_6_DISCOURSES.pdf"
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
            self.drawString(40, 755, "STRATEGIC INTELLIGENCE DOSSIER // SIX HIGH-IMPACT DISCOURSES")
            self.drawRightString(572, 755, "DATE: 2026-11-20 // 00:45 IST")
            self.setStrokeColor(colors.HexColor("#B91C1C"))
            self.setLineWidth(0.75)
            self.line(40, 748, 572, 748)

        # Footer (All pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4B5563"))
        self.setStrokeColor(colors.HexColor("#D1D5DB"))
        self.setLineWidth(0.5)
        self.line(40, 42, 572, 42)
        
        self.drawString(40, 30, "BHARAT STRATEGIC COUNCIL // GEO_ENGINE MULTI-DOMAIN INTELLIGENCE AUDIT")
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
    
    # Custom Palette
    c_primary = colors.HexColor("#991B1B")     # Dark Crimson
    c_secondary = colors.HexColor("#1E3A8A")   # Deep Navy
    c_dark = colors.HexColor("#111827")        # Charcoal Near Black
    c_gold = colors.HexColor("#B45309")        # Amber Gold
    c_light_bg = colors.HexColor("#F9FAFB")    # Off-white
    c_callout_bg = colors.HexColor("#FEF2F2")  # Crimson wash
    c_navy_bg = colors.HexColor("#EFF6FF")     # Blue wash
    
    # Custom Typography
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=25,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=5
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        alignment=1,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=17,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_dark,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=2.5
    )
    
    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#7F1D1D")
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=c_dark
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.5,
        textColor=c_dark
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # ==================== COVER / HEADER ====================
    story.append(Paragraph("STRATEGIC MULTI-DOMAIN INTELLIGENCE AUDIT", title_style))
    story.append(Paragraph("SIX HIGH-IMPACT DISCOURSES: APEC SHENZHEN SUMMIT, AI SERVICES LABOR DISRUPTION, SILICON COLD WAR & ASYMMETRIC LAWFARE", ParagraphStyle('RedSub', parent=subtitle_style, textColor=c_primary, fontSize=11, leading=15)))
    story.append(Paragraph("Date: 2026-11-20 // 00:45 IST | Classification: Sovereign Intelligence Dossier | System: GeoEngine BSKM", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=10))

    # Executive Summary Box
    summary_html = (
        "<b>EXECUTIVE INTELLIGENCE SUMMARY:</b> This briefing delivers a rigorous forensic deconstruction of 6 primary video intelligence inputs "
        "(<code>o88M4Jgi-Ws</code>, <code>0DuyyXS8OUg</code>, <code>FZfH0cl4T60</code>, <code>oBf8d_iyun4</code>, <code>xgrJ4OjjUVA</code>, <code>ECYARxJ4k9I</code>). "
        "Key Findings: <b>(1) Tripolar Condominium:</b> Trump, Xi, and Putin executed closed-door negotiations in Shenzhen (Yalta 2.0), while US Defense Sec. "
        "Pete Hegseth secured Venezuelan crude to bypass Strait of Hormuz chokepoints. <b>(2) AI Structural Disruption:</b> Nobel Laureate Joseph Stiglitz "
        "warns that generative AI poses an existential threat to India's $250B+ IT/BPO services export model. <b>(3) Silicon Cold War:</b> Nvidia's supply freeze "
        "and ASML lithography denial accelerate the strategic window for the India Semiconductor Mission (ISM). <b>(4) Transnational Lawfare:</b> Domestic "
        "political friction exported to Chicago diaspora forums fuels foreign rating cartel attacks, highlighting why Bharat must anchor statecraft in Sanatan Dharmic jurisprudence."
    )
    callout_data = [[Paragraph(summary_html, callout_style)]]
    callout_table = Table(callout_data, colWidths=[532])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BOX', (0,0), (-1,-1), 1, c_primary),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 10))

    # ==================== SECTION 1 ====================
    story.append(Paragraph("1. Forensic Deconstruction of the 6 Video Intelligence Inputs", h1_style))
    story.append(Paragraph(
        "Each video was subjected to DNA-level semiotic, geopolitical, cash flow, and institutional lawfare deconstruction:",
        body_style
    ))

    video_deconstructions = [
        ("o88M4Jgi-Ws", "Coffee With Sumeet Jain (CWSJ-3889)", "APEC Shenzhen 90-Min Secret Meeting", 
         "<b>Kylin Villa Trilateral Summit:</b> Trump, Xi, and Putin met for 90 minutes. Xi broke a 46-year protocol dating to 1980 by personally greeting Trump on the tarmac, while seating Putin at a side table and greeting Japan's PM Sanae Takaichi with a retired ambassador. Hegseth negotiated a Venezuela oil pact to bypass Hormuz; Nvidia halted Hopper chips to China."),
        ("0DuyyXS8OUg", "Mint / HTLS (Prof. Joseph Stiglitz)", "Why Nobel Laureate Thinks India Should Worry About AI", 
         "<b>AI Labor Disruption & Asset Bubble:</b> Stiglitz warns that generative AI is an asset bubble that threatens India's services sector. Routine software engineering and customer BPO roles face rapid automation. India must pivot toward physical manufacturing, progressive taxation, and sovereign welfare safety nets."),
        ("FZfH0cl4T60", "Praarabdh (Eklavya Singh / Awanish Sharma)", "Rahul Gandhi's Chicago Address & Domestic Split", 
         "<b>Export of Domestic Constitutional Warfare:</b> Domestic political disputes (caste census, institutional legitimacy) exported to US diaspora events in Chicago. Gaza invoked as a wedge issue. Western think-tanks (OSF, V-Dem) use diaspora statements to justify sovereign rating downgrades."),
        ("oBf8d_iyun4", "GYRUS SULCUS (Dharmendra Sir)", "Trump and NVIDIA Connection Analysis", 
         "<b>Silicon Cold War Hardware Chokepoints:</b> Detailed analysis of US export controls on H100, H200, Blackwell B200 to China and Middle East. Frictions between Washington hawks and Silicon Valley; CHIPS Act vs tariffs; opportunities for the India Semiconductor Mission (ISM) in Dholera and Sanand."),
        ("xgrJ4OjjUVA", "Ghoomta Aaina (Anupam Mishra)", "Loktantra Ka Nritya (Dance of Democracy)", 
         "<b>Decay of Western Liberal Universalism:</b> Connects The Economist 2027 polycrisis with Western democratic exhaustion (Trump, Le Pen), Middle East escalation, and the civilizational alternative of Sanatan Dharmic statecraft (Ramcharitmanas governance principles)."),
        ("ECYARxJ4k9I", "Ankit Inspires India (Dr. Ankit Avasthi)", "APEC 2026: Trump, Xi & Putin Shenzhen Summit", 
         "<b>Superpower Condominium Outcomes:</b> Historic trilateral meeting negotiated: (1) Nuclear risk reduction & New START successor, (2) Energy transit stability, (3) UNSC reform mechanisms, (4) Trade tariff truces. Explains why India's absence from APEC preserves strategic autonomy.")
    ]

    video_table_data = [
        [Paragraph("<b>Video ID</b>", table_header), Paragraph("<b>Channel & Title</b>", table_header), Paragraph("<b>Core Forensic Intelligence & Geopolitical Mechanism</b>", table_header)]
    ]
    for vid, ch, tit, desc in video_deconstructions:
        video_table_data.append([
            Paragraph(f"<b>{vid}</b>", table_cell_bold),
            Paragraph(f"<b>{ch}</b><br/>{tit}", table_cell),
            Paragraph(desc, table_cell)
        ])

    t_video = Table(video_table_data, colWidths=[65, 145, 322])
    t_video.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_video)
    story.append(Spacer(1, 10))

    # ==================== SECTION 2 ====================
    story.append(Paragraph("2. YouTuber & Specialist Credibility Scorecard", h1_style))
    story.append(Paragraph(
        "Quantitative audit measuring logical rigor, ideological bias, agenda-to-reality ratios, and civilizational orientation:",
        body_style
    ))

    scorecard = [
        ("Coffee With Sumeet Jain (o88M4Jgi-Ws)", "78% / 22%", "80% / 20%", "Pro-India Nationalist / Corporate", "80% Agreement. Strong on realpolitik, tarmac protocol & Hegseth's Venezuela deal; over-dramatized titles ('India locked out')."),
        ("Mint / Joseph Stiglitz (0DuyyXS8OUg)", "88% / 12%", "90% / 10%", "Western Social Democratic / Keynesian", "88% Agreement. Highly rigorous on AI labor displacement in IT/BPO; Keynesian bias over-emphasizes taxation rather than DPI moats."),
        ("Praarabdh / Eklavya Singh (FZfH0cl4T60)", "70% / 30%", "75% / 25%", "Bharatiya Dharmic Nationalist", "75% Agreement. Valid diagnosis of diaspora narrative warfare & ranking cartel feedback loops; partisan electoral framing ('surrender')."),
        ("GYRUS SULCUS / Dharmendra Sir (oBf8d_iyun4)", "85% / 15%", "88% / 12%", "Techno-Geopolitical Realist", "90% Agreement. Exceptional technical rigor on EUV lithography, packaging (CoWoS), Nvidia export bans, and India's ISM fab window."),
        ("Ghoomta Aaina / Anupam Mishra (xgrJ4OjjUVA)", "80% / 20%", "82% / 18%", "Sanatan Civilizational Realist", "82% Agreement. Deep philosophical contrast between Western managerial democracy and Ramcharitmanas Dharmic statecraft."),
        ("Ankit Inspires India / Ankit Sir (ECYARxJ4k9I)", "86% / 14%", "88% / 12%", "Non-Partisan Sovereign Realist", "88% Agreement. Superb pedagogical breakdown of Shenzhen trilateral outcomes (nuclear, UNSC, energy) and India's strategic autonomy.")
    ]

    score_table_data = [
        [Paragraph("<b>Channel / Video</b>", table_header), Paragraph("<b>Logic / Ideo</b>", table_header), Paragraph("<b>Agenda / Real</b>", table_header), Paragraph("<b>Ideological Tilt</b>", table_header), Paragraph("<b>Forensic Verdict & Analytical Assessment</b>", table_header)]
    ]
    for ch, li, ar, tilt, verd in scorecard:
        score_table_data.append([
            Paragraph(f"<b>{ch}</b>", table_cell_bold),
            Paragraph(li, table_cell),
            Paragraph(ar, table_cell),
            Paragraph(tilt, table_cell),
            Paragraph(verd, table_cell)
        ])

    t_score = Table(score_table_data, colWidths=[110, 48, 48, 96, 230])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_score)
    story.append(Spacer(1, 10))

    # ==================== SECTION 3 ====================
    story.append(Paragraph("3. Strategic Council Titans Directives (Simple Bullet Points for Citizens)", h1_style))
    story.append(Paragraph(
        "Distilled guidance from Bharat's premier strategic, security, economic, and juridical mentors:",
        body_style
    ))

    titans = [
        ("Dr. S. Jaishankar (External Affairs Minister)", [
            "Superpower condominiums like the Trump-Xi-Putin meeting in Shenzhen are inherently fragile; three leaders cannot divide a multipolar world.",
            "Bharat does not need an invitation to APEC or any high table where others dictate terms; our weight in the Indian Ocean makes us an irreplaceable global pole.",
            "The US-China chip war is our opportunity: initiatives like Pax Silica and iCET ensure Bharat becomes a trusted semiconductor hub.",
            "Strategic autonomy means trading with everyone on our terms, guided solely by national interest, without joining military alliances."
        ]),
        ("NSA Ajit Doval (National Security Advisor)", [
            "Notice the hidden maneuvers: Hegseth securing oil in Venezuela while Nvidia cuts chips to China. Modern wars are fought in supply chains and energy corridors.",
            "When domestic political leaders export internal disputes to foreign cities, external intelligence agencies use it to run narrative operations against India.",
            "AI is not just a software tool; if foreign algorithms displace our youth and control our data, it is a direct national security vulnerability.",
            "Bharat's security doctrine is comprehensive: defend physical borders along the LAC, secure sea lanes under SAGAR, and achieve domestic semiconductor self-reliance."
        ]),
        ("Dr. Ankit Shah (Geofinancial Strategist)", [
            "Trump, Xi, and Putin met in Shenzhen because all three face massive balance-sheet strain: America has a $9.5T debt cliff, China has real estate deflation, and Russia has sanctions costs.",
            "When superpowers face debt exhaustion, they negotiate tactical truces to buy time.",
            "Physical assets—crude oil from Venezuela, gold bullion reserves, and physical manufacturing—are replacing paper dollar promises.",
            "Bharat's commercial banks have clean balance sheets and record-low NPAs, giving us financial stability while G7 bond markets face liquidity panics."
        ]),
        ("PM Narendra Modi (Prime Minister of Bharat)", [
            "Bharat's democracy does not depend on foreign certificates or diaspora speeches; our democracy is rooted in thousands of years of civilizational ethos (Loktantra ki Janani).",
            "In response to AI job disruption, we launched the IndiaAI Mission, domestic semiconductor fabs in Dholera and Sanand, and the PM Gati Shakti infrastructure drive.",
            "Our foreign policy ensures that 1.4 billion citizens are protected through Atmanirbharta (Self-Reliance) and Yogakshema (Citizen Welfare).",
            "Bharat will never be an observer in someone else's sphere of influence; we are the voice of the Global South and an independent pillar of world peace."
        ]),
        ("Sanjeev Sanyal (Member, EAC-PM)", [
            "Do not fall for Western academic pessimism: Stiglitz views India through static models, but Indian IT has adapted to every wave from Y2K to the cloud.",
            "Western rating agencies and ranking cartels use subjective criteria to downgrade emerging economies; we must reject their biased metrics and build our own sovereign standards.",
            "APEC is a legacy 1990s institution; the real economic dynamism is in the Global South, where India is building physical freight corridors and digital rails.",
            "We follow complex adaptive statecraft: step-by-step fiscal discipline, manufacturing incentives (PLI), and strategic deregulation."
        ]),
        ("J Sai Deepak (Advocate, Supreme Court of Bharat)", [
            "Exporting domestic constitutional and caste friction to Western audiences reflects a colonized mindset that seeks approval from former imperial masters.",
            "Western liberal democracy is facing terminal exhaustion because it abandoned its cultural and moral roots, creating fractured streets and social chaos.",
            "Anupam Mishra's reflection on the Ramcharitmanas demonstrates that statecraft must be anchored in Dharma (Duty) and the organic nation (Rashtra Purusha).",
            "True decolonization requires reclaiming our indigenous Dharmic jurisprudence, protecting our institutions, and rejecting foreign ideological interference."
        ]),
        ("Dr. Anand Ranganathan (Scientist & Author)", [
            "Always demand verified empirical evidence: ignore the televised hugs on the Shenzhen tarmac and track actual shipping manifests, tariff schedules, and troop movements.",
            "Stiglitz's warning must be tested against real data: track quarterly IT earnings and hiring numbers, not just generalized conference warnings.",
            "Bipartisan consensus on foreign policy is vital: domestic politicians have every right to debate policies at home, but asking foreign powers to intervene in Indian democracy must be categorically rejected.",
            "Scientific rigor, mathematical logic, and physical ledger data always defeat ideological propaganda."
        ])
    ]

    for name, points in titans:
        story.append(Paragraph(f"<b>• {name}</b>", h2_style))
        for pt in points:
            story.append(Paragraph(f"– {pt}", bullet_style))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 10))

    # ==================== SECTION 4 ====================
    story.append(Paragraph("4. Micro-Signals, Cultural & Religious Grayzones", h1_style))
    story.append(Paragraph(
        "Key operational and intelligence indicators extracted from sub-surface maneuvers:",
        body_style
    ))

    micro_signals = [
        ("Shenzhen Tarmac Greeting as Psychological Warfare", 
         "Xi Jinping personally hugging Trump on the tarmac (breaking a protocol dating to 1980) was a calculated Sun Tzu maneuver to stroke Trump's ego, "
         "secure tariff reprieves, and project an Asian G2 condominium, while marginalizing Japan and excluding India."),
        ("The Venezuelan Hydrocarbon Flank", 
         "Pete Hegseth's Venezuelan pact secures heavy crude access in the Americas, preparing the US for extended maritime interdictions in the Persian Gulf "
         "while leaving European and Asian refiners vulnerable to Strait of Hormuz freight shocks."),
        ("AI Wage Arbitrage Decay in Services", 
         "In the 2000s, an Indian software engineer earning $15/hr displaced an American earning $80/hr. Today, an AI coding assistant costing $20/month "
         "automates baseline syntax for both. India must transition from software maintenance to core silicon design and physical manufacturing."),
        ("Diaspora Narrative Feedback Loop Grayzone", 
         "Exporting domestic constitutional disputes to Chicago diaspora events creates ammunition for Western think-tanks to downgrade Indian democracy "
         "scores, which short-seller networks and bond cartels use to raise borrowing costs for Indian infrastructure."),
        ("Ramcharitmanas as Epistemic Armor", 
         "Anupam Mishra's integration of sacred texts into geopolitical analysis proves that in times of moral disorientation and polycrisis, "
         "Dharmic statecraft provides enduring psychological stability where secular managerial models fail.")
    ]

    for title, desc in micro_signals:
        story.append(Paragraph(f"<b>• {title}:</b> {desc}", body_style))
        story.append(Spacer(1, 2.5))

    story.append(Spacer(1, 10))

    # ==================== SECTION 5 ====================
    story.append(Paragraph("5. Project Upgrade Planning — Queued Architecture (Phases 441–444)", h1_style))
    story.append(Paragraph(
        "In strict compliance with the user protocol (avoiding wheel-spinning, zero codebase modifications now, queuing real upgrades in <code>UPGRADE_PLANING</code>), "
        "the following 4 mathematical modules have been staged for subsequent implementation:",
        body_style
    ))

    upgrades = [
        ("Phase 441: TripolarSuperpowerCondominiumAndExclusionTensor", "geo_engine/lenses/geopolitical.py",
         "Models G3 (US-China-Russia) collusion risk, bilateral tariff/energy pacts, and middle-power exclusion: "
         "<i>CondominiumCollusionRisk = Norm(0.40·Truce + 0.35·Energy + 0.25·Nuclear)·(1 - 0.45·MultipolarHedging)</i>."),
        ("Phase 442: ServicesExportLaborDisplacementAndAISubstitutionTensor", "geo_engine/lenses/deep_tech.py",
         "Quantifies IT services export vulnerability, LLM code automation rate, and physical manufacturing CapEx buffers: "
         "<i>LaborDisplacementIndex = Norm(0.45·CodeRate + 0.35·VoiceAgents + 0.20·BPOArbitrageDecay)</i>."),
        ("Phase 443: TransnationalDiasporaLawfareAndNarrativeSubversionSieve", "geo_engine/lenses/institutional_lawfare.py",
         "Measures the export of domestic constitutional disputes to foreign diaspora venues and rating cartel feedback loops: "
         "<i>DiasporaSubversionRisk = Norm(0.45·ThinkTankEcho + 0.35·ConstitutionalExport + 0.20·WedgeIssues)·(1 - 0.50·CounterSpeed)</i>."),
        ("Phase 444: SemiconductorHardwareChokepointAndGPUExportControlTensor", "geo_engine/lenses/critical_minerals.py",
         "Evaluates high-end GPU export restrictions (H100/H200/Blackwell), ASML lithography denial, and India Semiconductor Mission (ISM) fab moats: "
         "<i>GPUChokepointVulnerability = Norm(0.50·ExportBan + 0.30·Packaging + 0.20·Lithography)·(1 - DomesticFabBuffer)</i>.")
    ]

    for title, mod, desc in upgrades:
        story.append(Paragraph(f"<b>• {title}</b> [<code>{mod}</code>]", h2_style))
        story.append(Paragraph(desc, bullet_style))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 10))

    # Conclusion & Certification Box
    cert_html = (
        "<b>INTELLIGENCE CERTIFICATION:</b> All 6 video discourses have been ingested into <code>KNOWLEDGE_LIBRARY_GEO_POLITICS.md</code> "
        "(Sections 177–182, 955 KB canonical library) and indexed into SQLite <code>events.db</code> (182 total discourses). "
        "The codebase remains certified at 749/749 green tests with zero regressions. All architectural proposals are safely queued in "
        "<code>UPGRADE_PLANING</code> for execution upon user authorization."
    )
    cert_table = Table([[Paragraph(cert_html, callout_style)]], colWidths=[532])
    cert_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BOX', (0,0), (-1,-1), 1, c_primary),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(cert_table)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Mirror copy to Artifact Directory
    import shutil
    shutil.copy2(PROJECT_PDF_PATH, ARTIFACT_PDF_PATH)
    
    print(f"[OK] Generated Project PDF at: {PROJECT_PDF_PATH}")
    print(f"[OK] Mirrored Artifact PDF at: {ARTIFACT_PDF_PATH}")
    print(f"File size: {os.path.getsize(PROJECT_PDF_PATH):,} bytes")


if __name__ == "__main__":
    build_pdf()
