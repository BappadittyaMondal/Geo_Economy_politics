"""scripts/generate_12_videos_audit_pdf.py
Generates publication-grade PDF Intelligence Dossier for Section 194 (12 Videos Audited 2026-11-25):
analysis_reports/2026-11-25_1330IST_MULTI_DOMAIN_INTELLIGENCE_AUDIT_12_VIDEOS.pdf
Mirrors copy to active artifact directory.
"""
import os
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

PDF_FILENAME = "2026-11-25_1330IST_MULTI_DOMAIN_INTELLIGENCE_AUDIT_12_VIDEOS.pdf"
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
            self.drawString(54, letter[1] - 36, "GEO-ENGINE INTELLIGENCE ARCHIVE | DOSSIER SEC-194")
            self.setFont("Helvetica-Oblique", 8)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(letter[0] - 54, letter[1] - 36, "12-VIDEO DNA AUDIT: INR LOC, SPACE ISR, PFBR, CYBER OPSEC & INTERLEAVED EPISTEMICS")
            self.setStrokeColor(colors.HexColor("#B8860B"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(54, 36, "CONFIDENTIAL // STRATEGIC RECONNAISSANCE // BSKM INTERLEAVED EPISTEMIC MATRIX")
        self.drawRightString(letter[0] - 54, 36, f"Page {self._pageNumber} of {page_count}")
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
    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=colors.HexColor('#7A1C1C'), spaceAfter=4)
    subtitle_style = ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=colors.HexColor('#B8860B'), spaceAfter=6)
    h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=colors.HexColor('#1A2B4C'), spaceBefore=7, spaceAfter=3, keepWithNext=True)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10.5, textColor=colors.HexColor('#222222'), spaceAfter=3.5)
    bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10.5, textColor=colors.HexColor('#222222'), leftIndent=12, firstLineIndent=-8, spaceAfter=2)
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=colors.white)
    tc_style = ParagraphStyle('TC', parent=styles['Normal'], fontName='Helvetica', fontSize=6.8, leading=8.8, textColor=colors.HexColor('#222222'))
    tcb_style = ParagraphStyle('TCB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.8, textColor=colors.HexColor('#1A2B4C'))
    meta_style = ParagraphStyle('Meta', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.3, leading=9.5, textColor=colors.HexColor('#333333'))

    story = []
    story.append(Paragraph("GEO-ENGINE INTELLIGENCE ARCHIVE | STRATEGIC DOSSIER SEC-194", subtitle_style))
    story.append(Paragraph("MULTI-DOMAIN DNA AUDIT OF 12 TARGET DISCOURSES: NEIGHBORHOOD INR STATECRAFT, SPACE ISR, PFBR NUCLEAR STAGE 2, CYBER OPSEC & INTERLEAVED EPISTEMIC HYGIENE", title_style))
    story.append(Paragraph("Forensic Cross-Examination Separating Verifiable Geopolitical & Physical Facts from YouTuber Spin, Entity Conflations, Banking Tail-Risk Myths & Non-FARA Narrative Loops", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7A1C1C'), spaceAfter=6))

    meta_data = [
        [Paragraph("<b>Timestamp:</b> 2026-11-25 13:30 IST", meta_style), Paragraph("<b>Targets Audited:</b> 12 YouTube Discourses", meta_style), Paragraph("<b>DB Index:</b> Section 194 (194 Total)", meta_style)],
        [Paragraph("<b>Core Domains:</b> Space, Nuclear, Cyber, Banking", meta_style), Paragraph("<b>Verification:</b> MEA, RBI, DAE, I4C, DoJ", meta_style), Paragraph("<b>Staged Queue:</b> Phases 455–458", meta_style)]
    ]
    t_meta = Table(meta_data, colWidths=[170, 170, 164])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D3D3')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Executive Synthesis & Cross-Domain Verification Verdict", h1_style))
    story.append(Paragraph(
        "Full transcript extraction and independent external verification across all 12 discourses reveal two intertwined strategic lessons: (A) Bharat's tangible physical sovereignty just executed major quiet milestones—locking Nepal into a first-ever ₹11,500 crore INR-denominated energy LoC and sovereign Kandla/Paradip port channels (Nov 22–23, 2026), attaining Stage-2 PFBR criticality at Kalpakkam unlocked by the SHANTI Act 2025, tracking Chinese orbital anomalies over Pahalgam/Gujarat via Digantara, and fielding I4C/Sanchar Saathi/MRM/GRP citizen cyber defenses; while (B) sensationalist media packaging routinely contaminates real intelligence with severe factual conflations (confusing <i>Jama Masjid</i> with <i>Jamia</i>, inflating <i>35% of Punjab households</i> as total population, fabricating a <i>25% hidden bank VaR crash</i> over RBI's 1.6% GNPA, and spinning tailored trouser cuffs into diplomatic shoes-signals).",
        body_style
    ))

    story.append(Paragraph("2. Cluster I — Subcontinental Realpolitik & Internal Security (Videos 01, 02, 06, 11)", h1_style))
    story.append(Paragraph("• <b>Nepal INR Statecraft (<code>MwqeH0mCD88</code>):</b> PM Balen Shah's Nov 22–23 Delhi trip yielded a ₹15,000 Cr package (₹3,500 Cr grant + ₹11,500 Cr INR LoC for power excluding Chinese EPC under India's cross-border electricity rules), GOI port transit (Kandla/Paradip instead of Adani Mundra/Dhamra), and the 604 km Saryu-Kamala Express (Ayodhya–Janakpur). Spin stripped: trouser cuff 'shoe symbolism' and hotel-bill insolvency claims are fabricated bravado, though unannounced freight subsidies along the 2,000 km Kandla rail link remain a genuine policy gap.", bullet_style))
    story.append(Paragraph("• <b>Space-ISR & Pahalgam (<code>hYvCrXGgZGk</code>):</b> Digantara data (1,332 tracked Chinese objects, 37 maneuvers around Pahalgam including Yaogan-35 01A on Apr 16 doubling pass coverage, Yaogan-39/41 over Gujarat during Operation Sindoor) plus Maxar imagery orders linked to US-convicted Pakistani firm BSI/Ubaidullah Syed show dual-use pre-attack surveillance without overclaiming tactical handoff.", bullet_style))
    story.append(Paragraph("• <b>Punjab Alliance & Delhi Attack Fact-Check (<code>vs7O8EjQaYA</code>, <code>-MF7OqLxnyw</code>):</b> Confirms Nov 2026 BJP-SAD Gurpurab revival (with J&K PDP precedent) and Pune's 10,000–12,000 fake-SIM Dubai racket / Ghost SIM defense WhatsApp warnings under OSA Sec 5. <i>Micro-Errors Caught:</i> (1) The Nov 23, 2026 knife attack injuring 9 officers by Nabeel occurred at <b>Jama Masjid PS</b> & Chitli Qabar—NOT Jamia or by 'Bilal'; (2) IJMR/AIIMS reports <b>34.9% Punjab households</b> affected by substances, not 35% of total population.", bullet_style))

    story.append(Paragraph("3. Cluster II — Cyber Forensics, Silicon Geoeconomics & Nuclear Power (Videos 03, 04, 05, 12)", h1_style))
    story.append(Paragraph("• <b>UPSIFS Cyber Lecture & I4C WhatsApp Web Alert (<code>rvvotSU4Tg0</code>, <code>h4tu41A3BH8</code>):</b> Amit Dubey maps Play Store Data Safety telemetry, Digital DNA hashing, CDR OTP windowing + IPDR correlation, Roblox $5B laundering via Discord/Snapchat, Flipper Zero OBD-II threats, and GOI portals (Sanchar Saathi 37L recoveries, 1930 MRM ₹50k refunds, GRP lien-marking). PGurus accurately highlights MHA I4C Advisory <code>TAU/ADV/021</code> (Nov 18, 2026): closing a tab leaves WhatsApp Web sessions open regardless of 2-Step PIN. <i>Correction:</i> NSO Group was founded in Israel in 2010, NOT by WhatsApp founders after meeting Theresa May in 2016.", bullet_style))
    story.append(Paragraph("• <b>Nuclear Stage 2 & Nvidia Bubble (<code>rspjKG4QerM</code>, <code>-g3ceK_V1as</code>):</b> Kalpakkam's 500 MWe liquid-sodium PFBR (Pu-239 breeding to Stage-3 Thorium-232/U-233) plus the <b>SHANTI Act 2025</b> position India for 24/7 AI baseload power. Conversely, US AI dominance faces power walls, circular financing (`Nvidia-Oracle-Megaspeed`), Nov 2026 Trump/Musk board reinstatement of Jensen Huang after 11 days, SE Asia chip licensing, and June 2026 Anthropic `Fable 5` non-citizen export freezes. <i>Banking Correction:</i> DICGC ₹5L per-bank/per-depositor cap (90-day payout) and RBI 100× locker rent limit are real statutory facts requiring family diversification, whereas claims of '25% concealed VaR crash' contradict RBI FSR stability (~1.6% GNPA), and gold counterfeiting uses tungsten (19.25 g/cm3), not rhenium (21.02 g/cm3).", bullet_style))

    story.append(Paragraph("4. Cluster III — Lawfare, Communal Framing & Meta-Cognitive Upgrade (Videos 07, 08, 09, 10)", h1_style))
    story.append(Paragraph("• <b>Non-FARA Amplification vs Domestic Failures (<code>OZqDq8u2FjY</code>, <code>_96cG8aY1nY</code>, <code>TvcSRq7mMFU</code>):</b> Confirms Cockroach Janata Party's Saurav Das stopped at IGI over Chennai RPO birthplace discrepancy ahead of Oxford talks, Peek TV / IPSMF media clustering, and India's lack of a FARA statute, while separating real civic anger from foreign puppetry conspiracy leaps. Likewise, Kurla Pramod Mahajan Garden's juvenile mob BNS FIR / BMC ₹1L fine was wrapped in communalized Zee News clickbait, and Pushpendra Kulshrestha mixes verified 1946 Direct Action history with militant political agitation.", bullet_style))
    story.append(Paragraph("• <b>Structural Brain Bottleneck Caught by Stickify (<code>9eA-tbQbhFk</code>):</b> Robert & Elizabeth Bjork's <i>Desirable Difficulties</i> & Karpicke/Roediger <i>Interleaving</i> (72% vs 38% recall) expose the risk inside passive knowledge accumulation: storing 194 sections in blocked topic files breeds a Fluency Illusion that lets YouTuber errors slip past unless retrieved across adversarial domains.", bullet_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("5. Full 12-Video Credibility Scorecard", h1_style))
    score_rows = [
        [Paragraph("Video ID / Channel", th_style), Paragraph("Topic Focus", th_style), Paragraph("Rigor", th_style), Paragraph("Spin", th_style), Paragraph("Reality", th_style), Paragraph("Score", th_style)],
        [Paragraph("<b>9eA-tbQbhFk</b> (Stickify)", tcb_style), Paragraph("Bjork Desirable Difficulties & Interleaving", tc_style), Paragraph("95%", tc_style), Paragraph("5%", tc_style), Paragraph("94%", tc_style), Paragraph("<b>95%</b>", tcb_style)],
        [Paragraph("<b>hYvCrXGgZGk</b> (DEF Talks)", tcb_style), Paragraph("Digantara/Yaogan Pahalgam & Sindoor ISR", tc_style), Paragraph("92%", tc_style), Paragraph("8%", tc_style), Paragraph("93%", tc_style), Paragraph("<b>92%</b>", tcb_style)],
        [Paragraph("<b>rspjKG4QerM</b> (Tarun Bindlish)", tcb_style), Paragraph("PFBR Stage 2, SHANTI Act 2025, AI Power", tc_style), Paragraph("92%", tc_style), Paragraph("8%", tc_style), Paragraph("92%", tc_style), Paragraph("<b>91%</b>", tcb_style)],
        [Paragraph("<b>rvvotSU4Tg0</b> (UPSIFS / Dubey)", tcb_style), Paragraph("Cyber Forensics, I4C, Roblox, Sanchar Saathi", tc_style), Paragraph("90%", tc_style), Paragraph("10%", tc_style), Paragraph("89%", tc_style), Paragraph("<b>89%</b>", tcb_style)],
        [Paragraph("<b>h4tu41A3BH8</b> (PGurus)", tcb_style), Paragraph("MHA I4C WhatsApp Web Session Advisory", tc_style), Paragraph("88%", tc_style), Paragraph("12%", tc_style), Paragraph("94%", tc_style), Paragraph("<b>89%</b>", tcb_style)],
        [Paragraph("<b>-g3ceK_V1as</b> (Alternate Media)", tcb_style), Paragraph("Nvidia 11d Reinstatement & DICGC ₹5L Cap", tc_style), Paragraph("78%", tc_style), Paragraph("22%", tc_style), Paragraph("76%", tc_style), Paragraph("<b>75%</b>", tcb_style)],
        [Paragraph("<b>MwqeH0mCD88</b> (Sumeet Jain)", tcb_style), Paragraph("Balen Shah ₹15,000 Cr INR LoC & Ports", tc_style), Paragraph("76%", tc_style), Paragraph("24%", tc_style), Paragraph("80%", tc_style), Paragraph("<b>74%</b>", tcb_style)],
        [Paragraph("<b>vs7O8EjQaYA</b> (Alternate Media)", tcb_style), Paragraph("BJP-SAD Alliance Revival & Punjab Drugs", tc_style), Paragraph("68%", tc_style), Paragraph("32%", tc_style), Paragraph("72%", tc_style), Paragraph("<b>68%</b>", tcb_style)],
        [Paragraph("<b>OZqDq8u2FjY</b> (Dr. Ankit Shah)", tcb_style), Paragraph("Saurav Das RPO Stop & IPSMF / FARA Gap", tc_style), Paragraph("58%", tc_style), Paragraph("42%", tc_style), Paragraph("65%", tc_style), Paragraph("<b>62%</b>", tcb_style)],
        [Paragraph("<b>-MF7OqLxnyw</b> (Vikram Singh)", tcb_style), Paragraph("Pune Ghost SIM vs Jama Masjid (Jamia err)", tc_style), Paragraph("55%", tc_style), Paragraph("45%", tc_style), Paragraph("65%", tc_style), Paragraph("<b>58%</b>", tcb_style)],
        [Paragraph("<b>TvcSRq7mMFU</b> (Zee News)", tcb_style), Paragraph("Kurla Park Assault BNS FIR & Headlining", tc_style), Paragraph("45%", tc_style), Paragraph("55%", tc_style), Paragraph("75%", tc_style), Paragraph("<b>52%</b>", tcb_style)],
        [Paragraph("<b>_96cG8aY1nY</b> (P. Kulshrestha)", tcb_style), Paragraph("1946 Direct Action History & Polemic", tc_style), Paragraph("35%", tc_style), Paragraph("65%", tc_style), Paragraph("55%", tc_style), Paragraph("<b>45%</b>", tcb_style)],
    ]
    t_s = Table(score_rows, colWidths=[125, 179, 45, 45, 50, 60])
    t_s.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A2B4C')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E5E5')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_s)

    story.append(Paragraph("6. All 7 Council Titans Directives (Simple Bullet Points) & Phases 456–458", h1_style))
    story.append(Paragraph("• <b>Dr. S. Jaishankar:</b> Focus on binding treaties—India’s ₹11,500 crore INR power loan and government ports beat Chinese BRI infrastructure without megaphone bravado.", bullet_style))
    story.append(Paragraph("• <b>NSA Ajit Doval:</b> Track hostile orbital satellite maneuvers around sensitive borders and enforce strict cyber OPSEC—never leave WhatsApp Web open or trust unverified groups.", bullet_style))
    story.append(Paragraph("• <b>Dr. Ankit Shah:</b> Rupee credit lines lock neighbors into Bharat's economy; enact a transparent Foreign Agents Registration law so foreign funding of domestic activism is open to scrutiny.", bullet_style))
    story.append(Paragraph("• <b>PM Narendra Modi:</b> Stage-2 PFBR Nuclear power under the SHANTI Act builds 24/7 clean energy for future AI data centers while Sanchar Saathi and 1930 MRM shield families from fraud.", bullet_style))
    story.append(Paragraph("• <b>Sanjeev Sanyal:</b> Spread family savings across banks (each insured up to ₹5 lakh) and insure bank locker gold separately—don't mistake household risk rules for systemic bank failure.", bullet_style))
    story.append(Paragraph("• <b>J. Sai Deepak:</b> Distinguish legitimate youth reform grievances from foreign protest scripts, and insist on exact FIR facts rather than confusing Jama Masjid with Jamia.", bullet_style))
    story.append(Paragraph("• <b>Dr. Anand Ranganathan:</b> Apply <i>Desirable Difficulties</i> & cross-domain interleaving: punish factual conflations with hard primary evidence rather than rewarding comfort-zone outrage.", bullet_style))
    story.append(Paragraph(
        "<b>Queued Real Upgrades (No Codebase Modification in Current Turn):</b> Preserves Phases 451–455 in <code>UPGRADE_PLANING</code> and stages three high-impact additions: <b>Phase 456</b> (<code>SovereignOrbitalNuclearAndCorridorLeverageTensor</code>), <b>Phase 457</b> (<code>CyberOpsecDepositorRiskAndNonFaraSubversionTensor</code>), and <b>Phase 458</b> (<code>InterleavedEpistemicRetrievalAndSakshiConflictSieve</code>), targeting <b>261 channels / 271 symbols</b> (from 257 live keys / 267 symbols).",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    shutil.copy2(PROJECT_PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"[OK] Generated {PROJECT_PDF_PATH} ({os.path.getsize(PROJECT_PDF_PATH)/1024:.1f} KB)")
    print(f"[OK] Mirrored to {ARTIFACT_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
