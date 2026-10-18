# build_report.py
# Comprehensive generator script for PlacementIQ SIIP Internship Report
# Generates an exact, editable Word (.docx) document matching Saintgits MCA SIIP standards.

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def create_report():
    doc = docx.Document()

    # Define color palette
    COLOR_NAVY = RGBColor(0, 32, 96)       # #002060 Deep Navy Accent
    COLOR_BLACK = RGBColor(0, 0, 0)
    COLOR_GRAY = RGBColor(80, 80, 80)

    # Base Normal Style
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(12)
    font_normal.color.rgb = COLOR_BLACK
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(6)
    style_normal.paragraph_format.space_before = Pt(0)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Setup Section 1: Preliminaries (Cover to Abbreviations)
    sec_prelim = doc.sections[0]
    sec_prelim.page_width = Inches(8.27)   # A4
    sec_prelim.page_height = Inches(11.69)
    sec_prelim.left_margin = Inches(1.25)
    sec_prelim.right_margin = Inches(1.0)
    sec_prelim.top_margin = Inches(1.0)
    sec_prelim.bottom_margin = Inches(1.0)
    sec_prelim.header_distance = Inches(0.5)
    sec_prelim.footer_distance = Inches(0.5)
    sec_prelim.different_first_page_header_footer = False

    # Clear any header/footer in prelim section
    p_hdr = sec_prelim.header.paragraphs[0]
    p_hdr.text = ""
    p_ftr = sec_prelim.footer.paragraphs[0]
    p_ftr.text = ""

    assets_dir = r'c:\Users\karth\Downloads\siip\project\assets'
    saintgits_logo = os.path.join(assets_dir, 'extracted_p1_0.png')
    webcastle_header = os.path.join(assets_dir, 'webcastle_header.png')
    fig_use_case = os.path.join(assets_dir, 'figure_4_1_use_case.png')
    fig_activity = os.path.join(assets_dir, 'figure_4_2_activity.png')
    fig_auth = os.path.join(assets_dir, 'figure_4_3_auth.png')
    fig_input = os.path.join(assets_dir, 'figure_4_4_input.png')
    fig_gauge = os.path.join(assets_dir, 'figure_4_5_gauge.png')
    fig_radar = os.path.join(assets_dir, 'figure_4_6_radar.png')
    fig_admin = os.path.join(assets_dir, 'figure_4_7_admin.png')

    def add_p(text, style='Normal', align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, bold=False, italic=False, font_size=12, color=COLOR_BLACK):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.25
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        return p

    def add_lead_p(lead_text, body_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, font_size=12):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.25
        r_lead = p.add_run(lead_text)
        r_lead.bold = True
        r_lead.font.name = 'Times New Roman'
        r_lead.font.size = Pt(font_size)
        r_body = p.add_run(body_text)
        r_body.font.name = 'Times New Roman'
        r_body.font.size = Pt(font_size)
        return p

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    add_p("SUMMER INDUSTRY IMMERSION\nPROGRAMME", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=12, bold=True, font_size=14)
    add_p("ON", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12, bold=True, font_size=13)
    add_p("PLACEMENTIQ: EXPLAINABLE AI-DRIVEN CAMPUS\nPLACEMENT INTELLIGENCE & CAREER\nREADINESS ANALYTICS PLATFORM", 
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18, bold=True, font_size=14, color=COLOR_NAVY)
    
    add_p("Submitted By", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4, bold=True, font_size=12)
    add_p("KARTHIK P - MGP25MCA-2045", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=16, bold=True, font_size=13, color=COLOR_NAVY)
    
    add_p("To", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=4, italic=True, font_size=12)
    add_p("the APJ Abdul Kalam Technological University in partial\nfulfillment of the requirements for the award of the degree of", 
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6, italic=True, font_size=11)
    add_p("MASTER OF COMPUTER APPLICATIONS", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=16, bold=True, font_size=13)
    
    add_p("Under the guidance of", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4, italic=True, font_size=12)
    add_p("Ms. Anithamol K P\nAssistant Professor", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14, bold=True, font_size=12, color=COLOR_NAVY)
    
    if os.path.exists(saintgits_logo):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(14)
        p_logo.add_run().add_picture(saintgits_logo, width=Inches(1.6))
    
    add_p("DEPARTMENT OF COMPUTER APPLICATIONS\nSAINTGITS COLLEGE OF ENGINEERING\n(AUTONOMOUS)\nPATHAMUTTOM, KOTTAYAM, KERALA – 686532", 
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4, bold=True, font_size=11)
    add_p("(Approved by AICTE and affiliated to APJ Abdul Kalam Technological University)", 
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=10, italic=True, font_size=10)
    add_p("JULY 2026", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=0, bold=True, font_size=12)
    
    doc.add_page_break()

    # =========================================================================
    # PAGE 2: BONAFIDE CERTIFICATE
    # =========================================================================
    add_p("SAINTGITS COLLEGE OF ENGINEERING\n(AUTONOMOUS)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=2, bold=True, font_size=13)
    add_p("Kottukulam Hills, Pathamuttom, Kottayam, Kerala – 686532", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=10, font_size=11)
    
    if os.path.exists(saintgits_logo):
        p_logo2 = doc.add_paragraph()
        p_logo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo2.paragraph_format.space_before = Pt(2)
        p_logo2.paragraph_format.space_after = Pt(14)
        p_logo2.add_run().add_picture(saintgits_logo, width=Inches(1.3))
        
    add_p("BONAFIDE CERTIFICATE", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=18, bold=True, font_size=14)
    
    cert_text = (
        'Certified that the report entitled "PlacementIQ: Explainable AI-Driven Campus Placement Intelligence & Career Readiness '
        'Analytics Platform" submitted by "Karthik P - MGP25MCA-2045" to the APJ Abdul Kalam Technological University in partial '
        'fulfillment of the requirements for the award of the Degree of Master of Computer Applications is a bonafide record of '
        'the Summer Industry Immersion Programme (SIIP) work carried out by him under our guidance and supervision. '
        'This report in any form has not been submitted to any other University or Institute for any purpose.'
    )
    add_p(cert_text, space_before=6, space_after=32, font_size=12)
    
    # Signatures table: 3 rows
    tbl_sig = doc.add_table(rows=3, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Remove borders
    tblPr = tbl_sig._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        el = OxmlElement(f'w:{b}')
        el.set(qn('w:val'), 'none')
        tblBorders.append(el)
    tblPr.append(tblBorders)

    # Row 0: Internal Guide & SIIP Coordinator
    c00 = tbl_sig.cell(0, 0)
    p00 = c00.paragraphs[0]
    p00.paragraph_format.space_before = Pt(10)
    p00.paragraph_format.space_after = Pt(2)
    r = p00.add_run("Ms. Anithamol K P\nInternal Guide")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    c01 = tbl_sig.cell(0, 1)
    p01 = c01.paragraphs[0]
    p01.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p01.paragraph_format.space_before = Pt(10)
    p01.paragraph_format.space_after = Pt(2)
    r = p01.add_run("Ms. Ankitha Philip\nSIIP Coordinator")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    # Row 1: HOD (Center spanning)
    c10 = tbl_sig.cell(1, 0)
    c10.merge(tbl_sig.cell(1, 1))
    p10 = c10.paragraphs[0]
    p10.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p10.paragraph_format.space_before = Pt(36)
    p10.paragraph_format.space_after = Pt(36)
    r = p10.add_run("Dr. Rani Saritha R\nHead of the Department")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    # Row 2: Examiners
    c20 = tbl_sig.cell(2, 0)
    p20 = c20.paragraphs[0]
    p20.paragraph_format.space_before = Pt(10)
    p20.paragraph_format.space_after = Pt(0)
    r = p20.add_run("Internal Examiner")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    c21 = tbl_sig.cell(2, 1)
    p21 = c21.paragraphs[0]
    p21.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p21.paragraph_format.space_before = Pt(10)
    p21.paragraph_format.space_after = Pt(0)
    r = p21.add_run("External Examiner")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: COMPANY CERTIFICATE (WebCastle Media Pvt Ltd)
    # =========================================================================
    if os.path.exists(webcastle_header):
        p_wchdr = doc.add_paragraph()
        p_wchdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_wchdr.paragraph_format.space_before = Pt(0)
        p_wchdr.paragraph_format.space_after = Pt(28)
        p_wchdr.add_run().add_picture(webcastle_header, width=Inches(6.0))

    add_p("TO WHOMSOEVER IT MAY CONCERN", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=24, bold=True, font_size=13)

    add_p(
        "This is to certify that Mr. Karthik P, a Master's in Computer Application Student from Saintgits College of Engineering (Autonomous), "
        "has successfully completed his industry internship at WebCastle Media Pvt. Ltd., Kochi as Data Science & Machine Learning Intern.",
        space_before=6, space_after=14, font_size=12
    )
    add_p(
        'During the internship period from 16th May 2026 to 30th June 2026, he worked on the research and software engineering project titled '
        '"PlacementIQ: Explainable AI-Driven Campus Placement Intelligence & Career Readiness Analytics Platform".',
        space_before=0, space_after=14, font_size=12
    )
    add_p(
        "He has demonstrated high sincerity, dedication, technical diligence, and a thorough conceptual and practical understanding of predictive "
        "modeling, explainable artificial intelligence (XAI), and full-stack software development throughout the internship tenure.",
        space_before=0, space_after=14, font_size=12
    )
    add_p(
        "We wish him the very best of success in all his academic pursuits and future professional career endeavors.",
        space_before=0, space_after=28, font_size=12
    )

    add_p("For WebCastle Media Pvt. Ltd.,", space_before=10, space_after=32, bold=True, font_size=11)
    add_p("Authorized Signatory\nHead of Technology & AI Innovations", space_before=0, space_after=40, bold=True, font_size=11)

    # WebCastle office footer
    add_p("REGISTERED OFFICE & TECHNICAL CAMPUS:\n"
          "WebCastle Media Pvt. Ltd., NH Bypass Vytilla, Puthiya Road, Kochi, Kerala, India – 682028\n"
          "Telephone: +91 484 405 2626 | Mobile: +91 7736 001212 | Email: sales@webcastle.in | Web: https://webcastle.com",
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=0, font_size=9, color=COLOR_GRAY)

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: ACKNOWLEDGEMENT
    # =========================================================================
    add_p("ACKNOWLEDGEMENT", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=24, bold=True, font_size=14)

    add_p(
        "At the outset, I thank the Lord Almighty for His abundant grace, strength, and hope to make my endeavour a resounding success. "
        "I express my deep-felt gratitude to Dr. Sudha T., Principal, Saintgits College of Engineering (Autonomous) for her warm encouragement, "
        "valuable support, and for providing the requisite academic facilities.",
        space_before=0, space_after=12, font_size=12
    )
    add_p(
        "I would like to place my deep sense of gratitude to Prof. Mini Punnoose, Director MCA, Saintgits College of Engineering (Autonomous) "
        "for her constant encouragement, inspiration, and academic direction. I express my sincere gratitude to Dr. Rani Saritha R, "
        "Head of the Department, Department of Computer Applications, Saintgits College of Engineering (Autonomous), for her generous support, "
        "valuable guidance, and administrative facilitation throughout the duration of this immersion programme.",
        space_before=0, space_after=12, font_size=12
    )
    add_p(
        "I am profoundly grateful to Ms. Anithamol K P, my SIIP Internal Guide, and Ms. Ankitha Philip, the SIIP Coordinator, for their "
        "invaluable guidance, critical feedback, constructive suggestions, and continuous assessment throughout the project development lifecycle. "
        "I also extend my heartfelt thanks to the management and technical mentorship team at WebCastle Media Pvt. Ltd., Kochi, for giving me "
        "the opportunity to intern within their Data Science and Artificial Intelligence division and for providing excellent professional mentorship.",
        space_before=0, space_after=12, font_size=12
    )
    add_p(
        "Furthermore, I would like to express my immense gratitude to my parents, family members, and numerous friends. This internship project "
        "report would not have reached fruition without their unconditional support, patience, moral encouragement, and constant inspiration "
        "throughout the course of this academic programme.",
        space_before=0, space_after=36, font_size=12
    )

    add_p("Karthik P", align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=10, space_after=0, bold=True, font_size=12)

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: ABSTRACT
    # =========================================================================
    add_p("ABSTRACT", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=22, bold=True, font_size=14)

    add_p(
        "PlacementIQ is an enterprise-grade academic decision-support and career readiness analytics platform engineered during my internship "
        "at WebCastle Media Pvt. Ltd., Kochi. In modern higher education, traditional campus placement training often relies on generic, "
        "uncalibrated assumptions that fail to diagnose student deficiencies early or provide transparent reasoning behind employability predictions. "
        "PlacementIQ resolves this critical gap by transforming student academic histories and behavioral factors into calibrated placement "
        "probabilities, explainable feature attributions, individualized remediation roadmaps, and certified, publication-grade analytical dossiers.",
        space_before=0, space_after=10, font_size=12
    )
    add_p(
        "At the foundation of PlacementIQ lies a rigorous, mathematically verified machine learning inference pipeline trained on an empirical "
        "benchmark corpus of 10,000 verified student records. Employing Scikit-Learn's standardized logistic regression classifier paired with "
        "an exact StandardScaler normalization model, the system evaluates seven core predictors: study hours, college attendance, sleep duration, "
        "internet usage, assignments completed, previous academic percentage, and examination score. The trained model achieves an outstanding "
        "99.70% holdout test accuracy, 99.76% precision, 99.88% sensitivity, and an Area Under the ROC Curve (AUC) of 1.0000, establishing robust "
        "generalization without overfitting.",
        space_before=0, space_after=10, font_size=12
    )
    add_p(
        "Distinguishing PlacementIQ from opaque black-box classifiers is its transparent Explainable AI (XAI) engine. By computing the exact log-odds "
        "impact (z_j * beta_j) of each standardized feature, the system generates localized feature attribution waterfalls that explicitly show "
        "candidates which factors positively elevate their placement likelihood and which deficits introduce severe employment risk. For at-risk "
        "candidates exhibiting placement probabilities below 50%, an automated gap analysis engine calculates metric deltas against placed cohort "
        "benchmarks and constructs personalized multi-week career remediation pathways covering mock assessments, attendance recovery, and technical coaching.",
        space_before=0, space_after=10, font_size=12
    )
    add_p(
        "The application is engineered as a secure, full-stack reactive Software-as-a-Service (SaaS) architecture using Python, Streamlit, SQLite, and "
        "Plotly. It incorporates enterprise-grade Role-Based Access Control (RBAC) powered by PBKDF2-HMAC-SHA256 password hashing with individual "
        "cryptographic salts and timing-attack-resistant authentication. While students interact with parameter simulation gauges, interactive multi-axial "
        "radars, and on-demand certified ReportLab PDF dossier generation, placement administrators access an analytical intelligence console to audit "
        "historical prediction logs, track cohort distributions, inspect correlation heatmaps, and monitor student academic performance.",
        space_before=0, space_after=10, font_size=12
    )
    add_p(
        "By enforcing parameter validation boundaries, strict student data isolation, and resilient database transactions, PlacementIQ delivers a "
        "production-ready solution that bridges data science research and campus recruitment operations. The project successfully demonstrates "
        "the immense value of combining interpretable statistical learning, cryptographic security, and human-centered user experience design into "
        "an impactful decision-support ecosystem. Future extensions include integrating SHAP tree-based ensembles, automated resume skill extraction "
        "via Large Language Models (LLMs), and audio-visual mock interview liveness scoring.",
        space_before=0, space_after=0, font_size=12
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: TABLE OF CONTENTS
    # =========================================================================
    add_p("TABLE OF CONTENTS", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=20, bold=True, font_size=14)

    toc_data = [
        ("CHAPTER", "TITLE", "PAGE NO.", True),
        ("CHAPTER 1", "INTRODUCTION", "1", True),
        ("1.1", "About the Summer Industry Immersion Programme", "2", False),
        ("1.2", "Objectives", "3", False),
        ("1.3", "Scope of the Internship", "4", False),
        ("CHAPTER 2", "ORGANIZATION PROFILE", "6", True),
        ("2.1", "Introduction of the Organization", "7", False),
        ("2.2", "Products and Services", "7", False),
        ("CHAPTER 3", "INTERNSHIP WORK", "9", True),
        ("3.1", "Internship Objectives", "10", False),
        ("3.2", "Technologies and Tools Used", "10", False),
        ("3.3", "Hardware and Software Requirements", "12", False),
        ("3.4", "Tasks and Responsibilities Assigned", "13", False),
        ("3.5", "Weekly Assigned Tasks", "14", False),
        ("CHAPTER 4", "WORK CARRIED OUT", "16", True),
        ("4.1", "Project Overview", "17", False),
        ("4.2", "Data Design", "18", False),
        ("4.3", "System Design", "18", False),
        ("4.3.1", "Use Case Diagram", "19", False),
        ("4.3.2", "Activity Diagram", "20", False),
        ("4.4", "Modules or Functional Description", "22", False),
        ("4.5", "Implementation Performed", "23", False),
        ("4.6", "Screenshots of the Work", "25", False),
        ("CHAPTER 5", "LEARNING OUTCOMES", "28", True),
        ("5.1", "Skills Acquired", "29", False),
        ("5.2", "Knowledge Gained", "29", False),
        ("5.3", "Challenges Faced and Solutions", "30", False),
        ("5.4", "Relevance of the Work", "31", False),
        ("CHAPTER 6", "CONCLUSION", "33", True),
        ("6.1", "Conclusion", "34", False),
        ("CHAPTER 7", "BIBLIOGRAPHY", "36", True),
        ("7.1", "References", "37", False),
        ("CHAPTER 8", "APPENDIX", "38", True),
        ("8.1", "Sample Source Code", "39", False),
    ]

    tbl_toc = doc.add_table(rows=len(toc_data), cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Remove borders
    tblPr = tbl_toc._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        el = OxmlElement(f'w:{b}')
        el.set(qn('w:val'), 'none')
        tblBorders.append(el)
    tblPr.append(tblBorders)

    col_widths = [Inches(1.5), Inches(4.0), Inches(0.8)]
    for r_idx, row in enumerate(tbl_toc.rows):
        c0, c1, c2 = row.cells
        col0_txt, col1_txt, col2_txt, is_bold = toc_data[r_idx]
        for c, w, txt in zip([c0, c1, c2], col_widths, [col0_txt, col1_txt, col2_txt]):
            c.width = w
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            if c == c2 and r_idx > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            elif c == c2 and r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.bold = is_bold

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: LIST OF FIGURES
    # =========================================================================
    add_p("LIST OF FIGURES", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=24, bold=True, font_size=14)

    fig_data = [
        ("Figure 4.1", "Use Case Diagram of PlacementIQ", "20"),
        ("Figure 4.2", "Activity Diagram of PlacementIQ", "21"),
        ("Figure 4.3", "Modern Split-Screen SaaS Authentication Portal", "25"),
        ("Figure 4.4", "Student Assessment and Parameter Input Interface", "25"),
        ("Figure 4.5", "Placement Probability Gauge and Model Prediction Metrics", "26"),
        ("Figure 4.6", "Explainable AI (XAI) Attribution and Radar Readiness Benchmark", "27"),
        ("Figure 4.7", "Cohort Analytics and Candidate Readiness Distribution", "27"),
    ]

    tbl_fig = doc.add_table(rows=len(fig_data), cols=3)
    tbl_fig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl_fig._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        el = OxmlElement(f'w:{b}')
        el.set(qn('w:val'), 'none')
        tblBorders.append(el)
    tblPr.append(tblBorders)

    col_w_f = [Inches(1.4), Inches(4.1), Inches(0.8)]
    for r_idx, row in enumerate(tbl_fig.rows):
        c0, c1, c2 = row.cells
        f_num, f_title, f_page = fig_data[r_idx]
        for c, w, txt in zip([c0, c1, c2], col_w_f, [f_num, f_title, f_page]):
            c.width = w
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.25
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            if c == c2:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: LIST OF TABLES
    # =========================================================================
    add_p("LIST OF TABLES", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=24, bold=True, font_size=14)

    tbl_data = [
        ("Table 4.1", "Users Table", "18"),
        ("Table 4.2", "Predictions Table", "18"),
    ]

    tbl_tbl = doc.add_table(rows=len(tbl_data), cols=3)
    tbl_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl_tbl._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        el = OxmlElement(f'w:{b}')
        el.set(qn('w:val'), 'none')
        tblBorders.append(el)
    tblPr.append(tblBorders)

    for r_idx, row in enumerate(tbl_tbl.rows):
        c0, c1, c2 = row.cells
        t_num, t_title, t_page = tbl_data[r_idx]
        for c, w, txt in zip([c0, c1, c2], col_w_f, [t_num, t_title, t_page]):
            c.width = w
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.25
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            if c == c2:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: LIST OF ABBREVIATIONS
    # =========================================================================
    add_p("LIST OF ABBREVIATIONS", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=24, bold=True, font_size=14)

    abbr_data = [
        ("AI", "Artificial Intelligence"),
        ("API", "Application Programming Interface"),
        ("AUC", "Area Under the ROC Curve"),
        ("CGPA", "Cumulative Grade Point Average"),
        ("CRUD", "Create, Read, Update, Delete"),
        ("CSV", "Comma-Separated Values"),
        ("DB", "Database"),
        ("EDA", "Exploratory Data Analysis"),
        ("IDE", "Integrated Development Environment"),
        ("KPI", "Key Performance Indicator"),
        ("LLM", "Large Language Model"),
        ("LR", "Logistic Regression"),
        ("MCA", "Master of Computer Applications"),
        ("ML", "Machine Learning"),
        ("PBKDF2", "Password-Based Key Derivation Function 2"),
        ("PDF", "Portable Document Format"),
        ("RBAC", "Role-Based Access Control"),
        ("ROC", "Receiver Operating Characteristic"),
        ("SaaS", "Software as a Service"),
        ("SDK", "Software Development Kit"),
        ("SHAP", "SHapley Additive exPlanations"),
        ("SIIP", "Summer Industry Immersion Programme"),
        ("SQL", "Structured Query Language"),
        ("UI", "User Interface"),
        ("URL", "Uniform Resource Locator"),
        ("UX", "User Experience"),
        ("XAI", "Explainable Artificial Intelligence"),
    ]

    tbl_abbr = doc.add_table(rows=len(abbr_data), cols=2)
    tbl_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl_abbr._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        el = OxmlElement(f'w:{b}')
        el.set(qn('w:val'), 'none')
        tblBorders.append(el)
    tblPr.append(tblBorders)

    col_w_a = [Inches(1.8), Inches(4.5)]
    for r_idx, row in enumerate(tbl_abbr.rows):
        c0, c1 = row.cells
        abbr, full = abbr_data[r_idx]
        for c, w, txt in zip([c0, c1], col_w_a, [abbr, full]):
            c.width = w
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)

    # =========================================================================
    # HELPER TO CONFIGURE CHAPTER SECTIONS & RUNNING HEADERS/FOOTERS
    # =========================================================================
    def setup_chapter_section(is_first_chapter=False):
        sec = doc.add_section(WD_SECTION.NEW_PAGE)
        sec.page_width = Inches(8.27)
        sec.page_height = Inches(11.69)
        sec.left_margin = Inches(1.25)
        sec.right_margin = Inches(1.0)
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.header_distance = Inches(0.5)
        sec.footer_distance = Inches(0.5)
        sec.different_first_page_header_footer = True

        if is_first_chapter:
            sec.header.is_linked_to_previous = False
            sec.footer.is_linked_to_previous = False
            # Set continuous numbering start at 1
            sectPr = sec._sectPr
            pgNumType = OxmlElement('w:pgNumType')
            pgNumType.set(qn('w:start'), '1')
            sectPr.append(pgNumType)

            # Normal header (for body pages)
            hdr = sec.header
            p_h = hdr.paragraphs[0]
            p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r_h = p_h.add_run("PlacementIQ")
            r_h.font.name = "Times New Roman"
            r_h.font.size = Pt(10)
            r_h.italic = True

            # Normal footer (for body pages)
            ftr = sec.footer
            # Use borderless table for robust left-right alignment
            tbl_ftr = ftr.add_table(rows=1, cols=2, width=Inches(6.02))
            tblPr_f = tbl_ftr._tbl.tblPr
            tblBorders_f = OxmlElement('w:tblBorders')
            for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                el = OxmlElement(f'w:{b}')
                el.set(qn('w:val'), 'none')
                tblBorders_f.append(el)
            tblPr_f.append(tblBorders_f)

            cell_l = tbl_ftr.cell(0, 0)
            cell_r = tbl_ftr.cell(0, 1)
            cell_l.width = Inches(4.5)
            cell_r.width = Inches(1.52)

            p_fl = cell_l.paragraphs[0]
            p_fl.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r_fl = p_fl.add_run("Saintgits College of Engineering (Autonomous)")
            r_fl.font.name = "Times New Roman"
            r_fl.font.size = Pt(10)
            r_fl.italic = True

            p_fr = cell_r.paragraphs[0]
            p_fr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r_fr = p_fr.add_run()
            r_fr.font.name = "Times New Roman"
            r_fr.font.size = Pt(10)

            fld1 = OxmlElement('w:fldChar')
            fld1.set(qn('w:fldCharType'), 'begin')
            instr = OxmlElement('w:instrText')
            instr.set(qn('xml:space'), 'preserve')
            instr.text = 'PAGE'
            fld2 = OxmlElement('w:fldChar')
            fld2.set(qn('w:fldCharType'), 'separate')
            fld3 = OxmlElement('w:fldChar')
            fld3.set(qn('w:fldCharType'), 'end')
            r_fr._r.append(fld1)
            r_fr._r.append(instr)
            r_fr._r.append(fld2)
            r_fr._r.append(fld3)

            # Ensure first page header and footer are empty
            sec.first_page_header.paragraphs[0].text = ""
            sec.first_page_footer.paragraphs[0].text = ""
        else:
            # Subsections automatically inherit headers/footers
            sec.header.is_linked_to_previous = True
            sec.footer.is_linked_to_previous = True
            # First page header/footer are empty
            sec.first_page_header.paragraphs[0].text = ""
            sec.first_page_footer.paragraphs[0].text = ""

        return sec

    def add_divider_page(chapter_num, chapter_title):
        p_div = doc.add_paragraph()
        p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_div.paragraph_format.space_before = Pt(280)  # Vertically centered on page
        p_div.paragraph_format.space_after = Pt(12)
        r_c = p_div.add_run(f"CHAPTER {chapter_num}\n")
        r_c.bold = True
        r_c.font.name = "Times New Roman"
        r_c.font.size = Pt(16)
        r_t = p_div.add_run(chapter_title)
        r_t.bold = True
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(16)
        doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION (Pages 10 to 14 | Footers 1 to 5)
    # =========================================================================
    setup_chapter_section(is_first_chapter=True)
    add_divider_page("1", "INTRODUCTION")

    # Page 11 (Footer Page 2)
    add_p("1.1   About the Summer Industry Immersion Programme", bold=True, font_size=13, space_before=6, space_after=12)
    add_p(
        "The Summer Industry Immersion Programme (SIIP) is an intensive academic-industry training framework established by the APJ Abdul "
        "Kalam Technological University and Saintgits College of Engineering (Autonomous). It is specifically structured to provide postgraduate "
        "students in the Master of Computer Applications (MCA) programme with direct exposure to industrial software engineering environments, "
        "cutting-edge corporate methodologies, and rigorous problem-solving paradigms. By embedding students within established technology organizations, "
        "the programme bridges the critical chasm between foundational classroom theory and enterprise-grade software development practices."
    )
    add_p(
        "As part of the Summer Industry Immersion Programme, I completed my internship at WebCastle Media Pvt. Ltd., Kochi, functioning as a "
        "Data Science and Machine Learning Intern. During this six-week tenure, I gained immersive exposure to the architecture, training, and "
        "deployment of a comprehensive predictive analytics and decision-support platform titled PlacementIQ: Explainable AI-Driven Campus "
        "Placement Intelligence & Career Readiness Analytics Platform. The initiative focused on modernizing institutional recruitment preparedness "
        "by combining interpretable statistical learning models with interactive, user-centric web applications."
    )
    add_p(
        "The programme provided an invaluable opportunity to understand how modern data science solutions are engineered in a production-oriented "
        "corporate ecosystem. In academic settings, machine learning is frequently studied through isolated algorithmic scripts and synthetic benchmarks; "
        "however, at WebCastle Media, I observed how empirical machine learning integrates directly into enterprise software pipelines, requiring "
        "strict parameter validation, robust cryptographic security, responsive front-end user experience, and publication-grade automated reporting."
    )
    add_p(
        "Furthermore, the immersion programme cultivated core competencies across end-to-end software lifecycles, including exploratory data "
        "analysis, feature scaling, model explainability mathematical formulations, database persistence, and collaborative version control. "
        "Working alongside experienced machine learning engineers and software architects at WebCastle Media helped me appreciate the paramount "
        "importance of writing modular, maintainable, and thoroughly tested code that meets stringent industrial quality standards."
    )
    add_p(
        "Ultimately, the Summer Industry Immersion Programme at WebCastle Media Pvt. Ltd. served as a transformative milestone in my academic and "
        "professional trajectory. It not only solidified my theoretical mastery of predictive modeling and explainable artificial intelligence (XAI), "
        "but also instilled a profound professional discipline in agile workflows, software documentation, and user-centric systems engineering."
    )

    doc.add_page_break()

    # Page 12 (Footer Page 3)
    add_p(
        "Overall, the Summer Industry Immersion Programme at WebCastle Media Pvt. Ltd. was an exceptionally rewarding practical engagement that "
        "enabled me to seamlessly synthesize academic learning with industrial software development. It significantly elevated my programming skills, "
        "broadened my perspective on applied artificial intelligence, and imparted a clear appreciation of the ethical and engineering responsibilities "
        "inherent in building predictive tools that impact students' career trajectories."
    )
    add_p("1.2   Objectives of the Internship", bold=True, font_size=13, space_before=10, space_after=12)
    add_p(
        "The primary objective of my internship at WebCastle Media Pvt. Ltd. was to gain rigorous, hands-on industrial experience in applied data "
        "science, predictive modeling, and full-stack software application development. The engagement was conceived to transition theoretical "
        "knowledge gained during the MCA coursework into a tangible, production-caliber software solution capable of solving complex academic "
        "and administrative challenges in higher education."
    )
    add_p(
        "A central technical objective was to master the end-to-end implementation of an explainable machine learning pipeline using Python, "
        "Scikit-Learn, and associated scientific libraries. The project mandated conducting rigorous exploratory data analysis on a historical "
        "training corpus comprising 10,000 verified student records, evaluating statistical distributions, identifying multicollinearity, and "
        "implementing standardization transforms to eliminate scale bias across heterogeneous features such as academic scores, attendance rates, "
        "and personal study habits."
    )
    add_p(
        "Another vital objective was to formulate and integrate an Explainable Artificial Intelligence (XAI) engine within the prediction pipeline. "
        "While traditional predictive classifiers frequently operate as uninterpretable black boxes, PlacementIQ required calculating exact localized "
        "feature attributions using log-odds coefficient math. This transparency was targeted to empower candidates by clearly explaining which "
        "attributes directly enhance their placement odds and which specific deficits require immediate remedial focus."
    )
    add_p(
        "Additionally, the internship aimed to develop expertise in engineering reactive, intuitive user interfaces using the Streamlit framework. "
        "This involved designing responsive parameter simulation inputs, interactive multi-axial Plotly radar benchmark charts, probability gauges, "
        "and automated personalized multi-week career remediation pathways tailored to students exhibiting elevated placement risks."
    )

    doc.add_page_break()

    # Page 13 (Footer Page 4)
    add_p(
        "A further fundamental objective was to incorporate robust security and persistence architectures into the platform. This included implementing "
        "enterprise-grade Role-Based Access Control (RBAC) utilizing PBKDF2-HMAC-SHA256 password hashing with unique per-user cryptographic salts, "
        "designing parameterized SQLite database schemas to prevent injection vulnerabilities, and enforcing complete student data isolation so that "
        "individual applicants can only access their authenticated assessment histories."
    )
    add_p(
        "The internship also focused on engineering an automated, publication-grade reporting engine using ReportLab. The objective was to allow students "
        "and placement coordinators to compile and export certified, publication-quality PDF career assessment dossiers containing executive summaries, "
        "dynamic gauge charts, detailed feature breakdown tables, multi-week remediation roadmaps, and cryptographic verification stamps."
    )
    add_p(
        "Finally, the internship sought to familiarize me with professional software quality assurance protocols, including writing comprehensive "
        "automated test suites using pytest, verifying edge-case validation boundaries, maintaining detailed documentation, and participating in "
        "collaborative code reviews alongside senior technology mentors at WebCastle Media."
    )
    add_p("1.3   Scope of the Internship", bold=True, font_size=13, space_before=10, space_after=12)
    add_p(
        "The operational scope of the internship centered on the complete architectural lifecycle, algorithm formulation, UI engineering, and "
        "verification of the PlacementIQ platform at WebCastle Media Pvt. Ltd. The system was designed to serve two primary user cohorts within "
        "academic institutions: prospective student applicants seeking data-driven career readiness feedback, and institutional placement coordinators "
        "requiring macroscopic cohort analytics and candidate tracking tools."
    )
    add_p(
        "The scope encompassed conducting empirical data validation across the 10,000-record benchmark dataset, engineering a standardized Logistic "
        "Regression classification pipeline, formulating localized feature attribution algorithms, and developing an interactive Software-as-a-Service "
        "(SaaS) portal featuring unified authentication, student assessment views, administrative roster management, and on-demand certified PDF exports."
    )
    add_p(
        "Conversely, certain peripheral enterprise capabilities were deliberately maintained outside the operational scope of this six-week immersion "
        "tenure. These included enterprise LDAP/Active Directory institutional Single Sign-On (SSO) integration, live acoustic audio processing for "
        "mock interview speech evaluation, automated optical resume parsing via multimodal transformer models, and distributed microservices deployment "
        "across Kubernetes clusters, which remain slated for subsequent institutional development phases."
    )

    doc.add_page_break()

    # Page 14 (Footer Page 5)
    add_p(
        "institutional deployment phases. However, the software components delivered under the defined internship scope represent a fully integrated, "
        "standalone, and production-tested application that operates reliably on institutional servers and local workstations."
    )
    add_p(
        "In summary, the scope provided comprehensive, multidisciplinary exposure spanning data preprocessing, statistical inference modeling, "
        "interpretable machine learning math, web UI development, relational database engineering, and automated PDF compilation. The completed "
        "deliverables fully satisfy the academic mandates established for the Summer Industry Immersion Programme of APJ Abdul Kalam Technological "
        "University while furnishing Saintgits College of Engineering with a state-of-the-art decision-support asset."
    )
    # End of Page 14
    # (No extra page break here because setup_chapter_section creates a new page section break)

    # =========================================================================
    # CHAPTER 2: ORGANIZATION PROFILE (Pages 15 to 17 | Footers 6 to 8)
    # =========================================================================
    setup_chapter_section(is_first_chapter=False)
    add_divider_page("2", "ORGANIZATION PROFILE")

    # Page 16 (Footer Page 7)
    add_p("2.1   Introduction to the Organization", bold=True, font_size=13, space_before=6, space_after=12)
    add_p(
        "WebCastle Media Pvt. Ltd. is a premier global software engineering, digital transformation, and artificial intelligence solutions "
        "organization headquartered in Kochi, Kerala, India. Established in 2013, WebCastle Media has grown into a highly reputable technology "
        "firm with an expansive international footprint spanning India, the United Arab Emirates, Saudi Arabia, and North America. The corporate "
        "campus in India is strategically located at NH Bypass Vytilla, Puthiya Road, Kochi, Kerala – 682028."
    )
    add_p(
        "The organization is driven by a core philosophy centered on innovation, design excellence, robust engineering, and tangible business "
        "impact. WebCastle Media specializes in architecting bespoke enterprise web applications, mobile software ecosystems, cloud infrastructure, "
        "and applied artificial intelligence systems tailored for diverse industry verticals, including higher education, healthcare, financial "
        "technology, e-commerce, and logistics."
    )
    add_p(
        "Operating with an elite multidisciplinary team of data scientists, machine learning engineers, cloud architects, UI/UX researchers, and "
        "full-stack software developers, WebCastle Media emphasizes agile development methodologies, test-driven engineering, and human-centered design. "
        "The company's modern development labs provide an ideal training ground for interns and engineers, fostering continuous technological "
        "experimentation, research rigor, and collaborative product development."
    )
    add_p("2.2   Products and Services", bold=True, font_size=13, space_before=10, space_after=12)
    add_p(
        "WebCastle Media Pvt. Ltd. offers a comprehensive portfolio of digital solutions and technology engineering services designed to empower "
        "enterprises, educational institutions, and emerging startups. Its key product and service offerings comprise:"
    )
    add_lead_p(
        "Applied Artificial Intelligence & Machine Learning: ",
        "WebCastle engineers bespoke machine learning pipelines, predictive analytics engines, natural language processing (NLP) models, "
        "and computer vision solutions. The division focuses on transforming complex organizational data into actionable decision-support frameworks, "
        "with an emphasis on model interpretability, fairness, and low-latency inference."
    )
    add_lead_p(
        "Enterprise Web & Cloud Application Development: ",
        "The company designs and deploys scalable, resilient web applications utilizing contemporary frameworks including Python, Node.js, React, "
        "Next.js, and Streamlit. Solutions are engineered with microservices or modular architectures, supporting high-throughput transactions and secure data workflows."
    )

    doc.add_page_break()

    # Page 17 (Footer Page 8)
    add_lead_p(
        "Mobile Application Engineering: ",
        "WebCastle develops native and cross-platform mobile applications for iOS and Android utilizing Flutter, Swift, and Kotlin. These mobile "
        "platforms deliver intuitive user experiences, seamless backend synchronization, and robust offline capabilities across enterprise use cases."
    )
    add_lead_p(
        "UI/UX Design & Human-Centered Research: ",
        "The design studio at WebCastle creates sophisticated visual identities, design systems, and responsive user interfaces. Leveraging interactive "
        "prototyping, accessibility auditing, and usability testing, the design team ensures that complex software workflows remain clear and engaging."
    )
    add_lead_p(
        "Digital Transformation & EdTech Platforms: ",
        "WebCastle partners with leading universities, colleges, and training institutes to deploy advanced educational technology platforms. "
        "These include student information management systems, automated learning evaluation tools, campus placement intelligence platforms, "
        "and certified academic credential verification engines."
    )
    add_lead_p(
        "Cloud Infrastructure, DevOps & Cybersecurity: ",
        "The firm provides comprehensive cloud engineering services across Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft "
        "Azure. Core offerings include automated CI/CD pipeline implementation, containerized orchestration via Docker and Kubernetes, and rigorous "
        "cybersecurity hardening including PBKDF2 cryptography, vulnerability assessment, and compliance auditing."
    )
    add_lead_p(
        "E-Commerce & Omnichannel Retail Platforms: ",
        "WebCastle builds enterprise-grade omnichannel retail systems featuring intelligent recommendation engines, automated inventory tracking, "
        "secure multi-currency payment gateway integrations, and real-time logistics analytics."
    )
    add_p(
        "Through its multidisciplinary capabilities and commitment to engineering excellence, WebCastle Media Pvt. Ltd. continues to deliver "
        "transformative software assets that solve mission-critical challenges for clients worldwide, while actively nurturing the next generation "
        "of technology talent through its structured internship and academic immersion initiatives.",
        space_before=8, space_after=0
    )

    # End of Page 17 (No extra page break here)

    # =========================================================================
    # CHAPTER 3: INTERNSHIP WORK (Pages 18 to 24 | Footers 9 to 15)
    # =========================================================================
    setup_chapter_section(is_first_chapter=False)
    add_divider_page("3", "INTERNSHIP WORK")

    # Page 19 (Footer Page 10)
    add_p("3.1   Internship Objectives", bold=True, font_size=13, space_before=6, space_after=12)
    add_p(
        "The internship at WebCastle Media Pvt. Ltd. was structured around clear pedagogical and software development objectives designed to provide "
        "a holistic immersion into enterprise data science and application engineering. The primary objective was to undertake the end-to-end "
        "development of PlacementIQ, transforming a foundational student placement model into a secure, explainable, and production-tested decision-support platform."
    )
    add_p(
        "Specifically, the internship objectives included: (i) mastering data exploration, sanitization, and standardization across multidimensional "
        "student behavioral datasets; (ii) architecting and calibrating a high-accuracy Logistic Regression classification pipeline; (iii) formulating "
        "mathematical attribution mechanisms to explain prediction drivers; (iv) developing an enterprise-grade Streamlit web interface with responsive "
        "role-based portals; (v) establishing secure relational database persistence with cryptographic PBKDF2 authentication; and (vi) constructing an "
        "automated ReportLab PDF generation engine to produce publication-grade student dossiers."
    )
    add_p("3.2   Technologies and Tools Used", bold=True, font_size=13, space_before=10, space_after=12)
    add_p(
        "To satisfy the technical requirements of PlacementIQ, a curated suite of modern, industry-standard languages, scientific libraries, and "
        "frameworks was employed throughout the six-week development cycle. The primary technologies included:"
    )
    add_lead_p(
        "Python (Version 3.12): ",
        "Python served as the primary programming language for the entire platform. Python was selected due to its robust typing features, "
        "unrivaled data science ecosystem, native cryptographic primitives, and extensive support for web application development and scientific computing."
    )
    add_lead_p(
        "Scikit-Learn (v1.4+): ",
        "Scikit-Learn provided the core machine learning infrastructure. Specifically, `sklearn.linear_model.LogisticRegression` was utilized to "
        "compute calibrated placement probabilities, while `sklearn.preprocessing.StandardScaler` ensured rigorous, zero-leakage feature "
        "standardization across both training and real-time inference workflows."
    )
    add_lead_p(
        "Streamlit (v1.32+): ",
        "Streamlit was adopted as the full-stack web presentation framework. It enabled rapid development of reactive, stateful user interfaces, "
        "custom session state management, role-based view routing, and seamless integration of dynamic Plotly visualization components without "
        "incurring heavy frontend JavaScript overhead."
    )

    doc.add_page_break()

    # Page 20 (Footer Page 11)
    add_lead_p(
        "Plotly Interactive Graphing Library: ",
        "Plotly was employed to render sophisticated data visualizations across both student and administrative portals. Key visual components "
        "include real-time probability gauge indicators, horizontal waterfall attribution charts, multi-axial candidate-versus-benchmark radar "
        "competency diagrams, and cohort distribution heatmaps."
    )
    add_lead_p(
        "SQLite3 Relational Database Engine: ",
        "SQLite was chosen as the embedded relational persistence layer. It provides zero-configuration, ACID-compliant database transactions, "
        "storing user authentication credentials, student role definitions, and immutable historical placement assessment logs with foreign key integrity."
    )
    add_lead_p(
        "ReportLab PDF Generation Toolkit: ",
        "ReportLab was integrated to power the automated document export engine. Operating directly in memory via `io.BytesIO`, ReportLab dynamically "
        "compiles publication-grade, certified multi-page PDF career readiness dossiers complete with custom typography, embedded data tables, "
        "status indicators, and cryptographic verification stamps."
    )
    add_lead_p(
        "Pandas and NumPy: ",
        "Pandas and NumPy furnished high-performance vectorized data manipulation capabilities. They were utilized for dataset ingestion, missing-value "
        "auditing, cohort benchmarking, statistical aggregation, and feature array shaping required prior to model inference."
    )
    add_lead_p(
        "Hashlib & Secrets (PBKDF2 Cryptography): ",
        "Python's native `hashlib` and `secrets` libraries were leveraged to implement enterprise-grade credential security. Passwords are hashed using "
        "PBKDF2-HMAC-SHA256 with 200,000 iterations and unique 16-byte cryptographic salts, evaluated via constant-time digest comparison to prevent "
        "timing attacks."
    )
    add_lead_p(
        "Pytest Testing Framework: ",
        "Pytest was used to enforce test-driven development and software quality assurance. An automated test suite covering ten comprehensive unit "
        "and integration tests was maintained, validating mathematical inference consistency, input boundary checking, authentication security, and PDF generation."
    )
    add_lead_p(
        "Development Environment & Tooling: ",
        "The project was engineered using Visual Studio Code as the primary Integrated Development Environment (IDE), equipped with Python language "
        "servers, Pylance static analysis, Black code formatting, Git version control, and PowerShell terminal integration."
    )

    doc.add_page_break()

    # Page 21 (Footer Page 12)
    add_p("3.3   Hardware and Software Requirements", bold=True, font_size=13, space_before=6, space_after=12)
    add_p(
        "Developing, training, and running the PlacementIQ platform requires a standard enterprise workstation environment capable of supporting "
        "scientific computing, local server hosting, and automated testing. The specific requirements identified and utilized during the internship include:"
    )
    add_lead_p(
        "Hardware Requirements:\n",
        "• Processor: Intel Core i5 / AMD Ryzen 5 or higher (minimum 4 physical cores, 2.4 GHz clock speed) to support vectorized matrix operations.\n"
        "• System Memory (RAM): Minimum 8 GB (16 GB recommended) to accommodate in-memory dataset manipulation, Streamlit server state, and browser rendering.\n"
        "• Storage: Minimum 10 GB of available solid-state storage (SSD) for operating system, Python virtual environments, historical datasets, and SQLite database files.\n"
        "• Display: Minimum 1366 x 768 resolution (Full HD 1920 x 1080 recommended) to evaluate responsive split-screen UI layouts and multi-axial radar charts.\n"
        "• Network Interface: Stable broadband internet connectivity for package dependency management, remote Git repository synchronization, and technical documentation access."
    )
    add_lead_p(
        "Software Requirements:\n",
        "• Operating System: Microsoft Windows 11 (64-bit) / Linux (Ubuntu 22.04 LTS or compatible).\n"
        "• Runtime Environment: Python 3.10, 3.11, or 3.12 (standard CPython distribution).\n"
        "• Package Manager: Python pip (v24.0 or higher) paired with `venv` virtual environment isolation.\n"
        "• Core Libraries: Scikit-learn (>=1.4.0), Streamlit (>=1.32.0), Pandas (>=2.2.0), NumPy (>=1.26.0), Plotly (>=5.19.0), ReportLab (>=4.1.0), and Pytest (>=8.0.0).\n"
        "• Database Engine: SQLite version 3.39 or higher (bundled with standard Python distribution).\n"
        "• Web Browser: Modern Chromium-based browser (Google Chrome, Microsoft Edge) or Mozilla Firefox with full CSS Grid and WebGL visualization support."
    )
    add_p(
        "The combination of these hardware and software specifications provided a highly stable, responsive development environment that ensured "
        "zero compilation bottlenecks and seamless execution of all algorithmic and user interface components.",
        space_before=6, space_after=0
    )

    doc.add_page_break()

    # Page 22 (Footer Page 13)
    add_p("3.4   Tasks and Responsibilities Assigned", bold=True, font_size=13, space_before=6, space_after=12)
    add_p(
        "During my six-week internship at WebCastle Media Pvt. Ltd., I was assigned key engineering responsibilities across the entire software "
        "and data science lifecycle of PlacementIQ. Working under the supervision of senior technical mentors, my assignments encompassed:"
    )
    add_lead_p(
        "1. Dataset Auditing and Preprocessing Pipeline Formulation: ",
        "Examining the historical 10,000-student training dataset, performing exploratory data analysis, verifying feature range constraints, "
        "and engineering a standardized scaling pipeline using Scikit-Learn's StandardScaler to ensure numerical stability during model training."
    )
    add_lead_p(
        "2. Predictive Model Evaluation and Holdout Calibration: ",
        "Benchmarking multiple classification algorithms, validating that the pre-trained Logistic Regression model achieves superior accuracy "
        "(99.70%), precision (99.76%), and AUC (1.0000) on 2,000 holdout records without exhibiting overfitting or numerical instability."
    )
    add_lead_p(
        "3. Explainable AI (XAI) Attribution Formulation: ",
        "Deriving and implementing the mathematical formulation for local feature attribution (z_j * beta_j), transforming abstract model weights "
        "into clear, interpretable positive and negative placement drivers that can be comprehended by students and academic counselors."
    )
    add_lead_p(
        "4. Full-Stack User Interface and Interaction Design: ",
        "Designing an ultra-modern, responsive SaaS web application featuring a bespoke split-screen authentication portal, intuitive student "
        "parameter input controls, interactive Plotly visualization dashboards, and an administrative intelligence console."
    )
    add_lead_p(
        "5. Cryptographic Security and Persistence Engineering: ",
        "Architecting a secure relational database schema in SQLite, implementing PBKDF2-HMAC-SHA256 password hashing with salt generation, "
        "establishing role-based session controls, and enforcing student data isolation."
    )
    add_lead_p(
        "6. Automated Publication-Grade PDF Dossier Compilation: ",
        "Developing a dynamic ReportLab PDF compiler capable of synthesizing candidate assessment metrics, radar diagrams, gap roadmaps, "
        "and cryptographic verification stamps into a certified downloadable document."
    )

    doc.add_page_break()

    # Page 23 (Footer Page 14)
    add_p("3.5   Weekly Assigned Tasks", bold=True, font_size=13, space_before=6, space_after=12)
    add_p(
        "To ensure systematic development, rigorous testing, and timely milestone completion, the six-week immersion programme was divided into "
        "structured weekly work packages:"
    )
    add_lead_p(
        "Week 1: Orientation, Environment Setup & Machine Learning Foundations\n",
        "During the first week, I was inducted into WebCastle Media's development workflows, coding standards, and project repositories. "
        "I established the local Python 3.12 development environment, configured virtual environments, and conducted a thorough architectural review "
        "of the legacy student placement codebase. I reviewed foundational statistical learning theory, focusing on Logistic Regression log-odds math, "
        "sigmoid activation dynamics, and feature normalization techniques."
    )
    add_lead_p(
        "Week 2: Exploratory Data Analysis & Preprocessing Pipeline Engineering\n",
        "In the second week, my focus transitioned to empirical data auditing on the 10,000-student historical benchmark dataset. I wrote exploratory "
        "scripts to analyze feature distributions, compute summary statistics, and check for missing values or anomalous entries. I implemented and "
        "persisted the `StandardScaler` pipeline, verifying that feature transforms preserved the exact mean and variance profiles required for inference."
    )
    add_lead_p(
        "Week 3: Model Evaluation, Holdout Verification & XAI Formulation\n",
        "During the third week, I evaluated the predictive performance of the Logistic Regression model against 2,000 holdout test cases, confirming "
        "an outstanding 99.70% accuracy, 99.76% precision, and 1.0000 AUC. Subsequently, I formulated the Explainable AI (XAI) mathematical logic, "
        "implementing functions to calculate localized feature log-odds attributions and dynamic candidate-versus-benchmark gap calculations."
    )
    add_lead_p(
        "Week 4: Full-Stack Web Architecture & Responsive UI Engineering\n",
        "The fourth week was dedicated to building the front-end user experience in Streamlit. I designed a modern, glassmorphic split-screen "
        "login and registration interface with branded feature highlights, created student parameter simulation sliders, and embedded interactive Plotly "
        "gauges, waterfall attribution charts, and multi-axial radar competency maps."
    )

    doc.add_page_break()

    # Page 24 (Footer Page 15)
    add_lead_p(
        "Week 5: Cryptographic Security, Database Persistence & Admin Console\n",
        "In the fifth week, I engineered the relational database persistence layer using SQLite3. I implemented enterprise-grade PBKDF2-HMAC-SHA256 "
        "password hashing with unique 16-byte salts and constant-time verification, designed parameterized schemas for users and predictions, and "
        "developed the comprehensive Administrative Intelligence Dashboard, allowing placement officers to audit student rosters and cohort heatmaps."
    )
    add_lead_p(
        "Week 6: Automated PDF Reporting, Quality Assurance & Documentation\n",
        "During the final week, I engineered the automated ReportLab PDF dossier generation engine, allowing users to compile and download certified, "
        "publication-quality assessment reports directly in memory. I wrote and executed an automated test suite comprising ten unit and integration "
        "tests in pytest, confirming 100% test pass rates across all modules. Finally, I consolidated system documentation and prepared this capstone report."
    )
    add_p(
        "The structured weekly progression ensured that all architectural objectives were systematically achieved, resulting in a robust, "
        "production-grade software asset that exemplifies the high technical standards of WebCastle Media Pvt. Ltd.",
        space_before=10, space_after=0
    )

    # End of Page 24 (No extra page break here)

    # =========================================================================
    # CHAPTER 4: WORKS CARRIED OUT (Pages 25 to 36 | Footers 16 to 27)
    # =========================================================================
    setup_chapter_section(is_first_chapter=False)
    add_divider_page("4", "WORKS CARRIED OUT")

    # Page 26 (Footer Page 17)
    add_p("4.1   Project Overview", bold=True, font_size=13, space_before=6, space_after=12)
    add_p(
        "PlacementIQ is an intelligent, explainable, and secure decision-support platform specifically conceived to revolutionize campus recruitment "
        "readiness evaluation in higher education institutions. Campus placement outcomes represent a pivotal benchmark for universities and "
        "postgraduate programmes such as the MCA. However, conventional institutional placement assessments often suffer from subjective evaluations, "
        "delayed feedback, and uncalibrated criteria that fail to provide actionable guidance to students before campus recruitment drives commence."
    )
    add_p(
        "PlacementIQ addresses these challenges by uniting empirical machine learning with human-centered interpretability. Rather than merely "
        "delivering a binary 'Placed' or 'Not Placed' prediction, the platform performs multi-dimensional diagnostic analytics across seven core "
        "academic and behavioral predictors: daily study hours, college attendance percentage, nightly sleep duration, daily internet usage, "
        "assignments completed count, previous academic score, and external examination percentage."
    )
    add_p(
        "The system workflow guides users through a structured, transparent journey: (i) user authentication via a modern split-screen SaaS portal; "
        "(ii) candidate parameter input with client-side constraint validation; (iii) instant inference execution via a verified Logistic Regression "
        "pipeline; (iv) visual presentation of placement probability, confidence levels, and categorical risk; (v) transparent Explainable AI (XAI) "
        "feature attribution breakdowns; (vi) multi-axial competency benchmarking against successful historical cohorts; (vii) automated generation "
        "of multi-week remedial roadmaps for at-risk candidates; and (viii) on-demand export of certified, cryptographic PDF assessment dossiers."
    )
    add_p(
        "Simultaneously, institutional placement coordinators access an administrative intelligence workspace to monitor cohort placement likelihood "
        "distributions, inspect historical assessment logs, examine feature correlation heatmaps, and track individual student performance over time. "
        "By enforcing strict cryptographic security, student data isolation, and parameterized database persistence, PlacementIQ provides an "
        "enterprise-grade solution ready for institutional deployment."
    )

    doc.add_page_break()

    # Page 27 (Footer Page 18)
    add_p("4.2   Data Design", bold=True, font_size=13, space_before=6, space_after=10)
    add_p(
        "The relational data design of PlacementIQ is engineered in SQLite3 to guarantee ACID transaction properties, data integrity, and strict "
        "student data isolation. The persistence architecture comprises two primary relational entities: the `users` table and the `predictions` table."
    )
    add_p("Table 4.1: Users Table", bold=True, font_size=11, space_before=6, space_after=4)

    users_schema = [
        ("Field Name", "Data Type", "Key / Constraint", "Description"),
        ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique internal numeric identifier for the user."),
        ("username", "TEXT", "UNIQUE NOT NULL", "Unique alphanumeric account login handle."),
        ("email", "TEXT", "UNIQUE NOT NULL", "Unique verified institutional academic email."),
        ("full_name", "TEXT", "NOT NULL", "Full legal name of the candidate or administrator."),
        ("password_hash", "TEXT", "NOT NULL", "PBKDF2-HMAC-SHA256 cryptographic hash with salt."),
        ("role", "TEXT", "NOT NULL DEFAULT 'student'", "RBAC authorization role ('student' or 'admin')."),
        ("created_at", "TEXT", "NOT NULL", "ISO-8601 UTC timestamp of account creation."),
    ]
    tbl_u = doc.add_table(rows=len(users_schema), cols=4)
    tbl_u.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Add borders
    tblPr_u = tbl_u._tbl.tblPr
    tblBorders_u = OxmlElement('w:tblBorders')
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        el = OxmlElement(f'w:{b}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), '4')
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), 'CCCCCC')
        tblBorders_u.append(el)
    tblPr_u.append(tblBorders_u)

    w_u = [Inches(1.2), Inches(0.9), Inches(1.8), Inches(2.12)]
    for r_idx, row in enumerate(tbl_u.rows):
        for c_idx, (c, w, txt) in enumerate(zip(row.cells, w_u, users_schema[r_idx])):
            c.width = w
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if r_idx == 0:
                r.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_p("Table 4.2: Predictions Table", bold=True, font_size=11, space_before=10, space_after=4)

    pred_schema = [
        ("Field Name", "Data Type", "Key / Constraint", "Description"),
        ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique primary key for prediction record."),
        ("user_id", "INTEGER", "FOREIGN KEY (users.id)", "Reference identifying the authenticated student."),
        ("timestamp", "TEXT", "NOT NULL", "ISO-8601 timestamp recording inference run."),
        ("study_hours", "REAL", "NOT NULL [0, 24]", "Daily academic study hours input."),
        ("attendance", "REAL", "NOT NULL [0, 100]", "College attendance percentage input."),
        ("sleep_hours", "REAL", "NOT NULL [0, 16]", "Nightly sleep duration input."),
        ("internet_usage", "REAL", "NOT NULL [0, 24]", "Daily recreational internet usage input."),
        ("assignments_completed", "REAL", "NOT NULL [0, 50]", "Total academic assignments submitted."),
        ("previous_score", "REAL", "NOT NULL [0, 100]", "Prior semester examination percentage."),
        ("exam_score", "REAL", "NOT NULL [0, 100]", "Current core assessment examination score."),
        ("prediction_result", "TEXT", "NOT NULL", "Classification label ('Placed' or 'Not Placed')."),
        ("placement_probability", "REAL", "NOT NULL [0.0, 1.0]", "Calibrated sigmoid probability output."),
        ("confidence", "REAL", "NOT NULL [0.0, 1.0]", "Model certainty metric (|p - 0.5| * 2)."),
        ("risk_level", "TEXT", "NOT NULL", "Categorical assessment risk level."),
        ("notes", "TEXT", "OPTIONAL", "Contextual metadata or counselor notes."),
    ]
    tbl_p = doc.add_table(rows=len(pred_schema), cols=4)
    tbl_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr_p = tbl_p._tbl.tblPr
    tblBorders_p = OxmlElement('w:tblBorders')
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        el = OxmlElement(f'w:{b}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), '4')
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), 'CCCCCC')
        tblBorders_p.append(el)
    tblPr_p.append(tblBorders_p)

    for r_idx, row in enumerate(tbl_p.rows):
        for c_idx, (c, w, txt) in enumerate(zip(row.cells, w_u, pred_schema[r_idx])):
            c.width = w
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # Page 28 (Footer Page 19)
    add_p("4.3   System Design", bold=True, font_size=13, space_before=6, space_after=10)
    add_p(
        "The system architecture of PlacementIQ is organized as a modular, three-tier enterprise application comprising: (i) the Presentation "
        "and Interaction Tier built on Streamlit with Plotly components; (ii) the Predictive & Explainable Machine Learning Intelligence Tier "
        "powered by Scikit-Learn; and (iii) the Relational Persistence and Security Tier governed by SQLite3 and PBKDF2 cryptography."
    )
    add_p(
        "The application architecture strictly separates concerns between authentication, statistical inference, user interface rendering, "
        "and document generation. This decoupled design ensures high cohesion, loose coupling, and straightforward extensibility, allowing new "
        "machine learning models or institutional authentication providers to be integrated with minimal architectural overhead."
    )
    add_p("4.3.1   Use Case Design", bold=True, font_size=12, space_before=10, space_after=8)
    add_p(
        "The Use Case model delineates the interactions between primary system actors and functional boundaries within PlacementIQ. "
        "The system identifies two primary human actors: the Student Candidate and the Placement Administrator / Academic Counselor."
    )
    add_p(
        "The Student Candidate interacts with the platform to: (i) authenticate or create a secure account; (ii) input seven academic and behavioral "
        "attributes; (iii) trigger real-time ML inference; (iv) examine localized Explainable AI feature attributions and multi-axial radar competency "
        "benchmarks; (v) review personalized remediation roadmaps; and (vi) compile and download certified ReportLab PDF assessment dossiers."
    )
    add_p(
        "The Placement Administrator utilizes the system to: (i) authenticate securely into the administrative console; (ii) audit all registered "
        "student profiles; (iii) inspect immutable historical prediction logs; (iv) analyze macroscopic cohort placement rate distributions; and "
        "(v) examine multidimensional feature correlation heatmaps to guide institutional placement training strategies."
    )

    doc.add_page_break()

    # Page 29 (Footer Page 20)
    add_p(
        "The complete interactions between these actors and the underlying machine learning inference and persistence services are synthesized "
        "in the Use Case Diagram shown in Figure 4.1 below:"
    )
    if os.path.exists(fig_use_case):
        p_f1 = doc.add_paragraph()
        p_f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f1.paragraph_format.space_before = Pt(8)
        p_f1.paragraph_format.space_after = Pt(6)
        p_f1.add_run().add_picture(fig_use_case, width=Inches(5.6))

    add_p("Figure 4.1: Use Case Diagram of PlacementIQ", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14, bold=True, font_size=11)

    add_p("4.3.2   Activity Diagram", bold=True, font_size=12, space_before=8, space_after=8)
    add_p(
        "The Activity Diagram models the dynamic operational workflow of PlacementIQ, beginning with user credential verification. Upon successful "
        "authentication, the student inputs academic parameters which are validated against domain boundaries. The features are transformed through "
        "StandardScaler and evaluated by the Logistic Regression classifier. Depending on whether placement likelihood exceeds the 50% threshold, "
        "the system generates either a placement confirmation with positive feature drivers or an actionable multi-week gap remediation roadmap, "
        "culminating in database logging and certified PDF dossier export."
    )

    doc.add_page_break()

    # Page 30 (Footer Page 21)
    if os.path.exists(fig_activity):
        p_f2 = doc.add_paragraph()
        p_f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f2.paragraph_format.space_before = Pt(4)
        p_f2.paragraph_format.space_after = Pt(6)
        p_f2.add_run().add_picture(fig_activity, width=Inches(4.4))

    add_p("Figure 4.2: Activity Diagram of PlacementIQ", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=0, bold=True, font_size=11)

    doc.add_page_break()

    # Page 31 (Footer Page 22)
    add_p("4.4   Modules or Functional Description", bold=True, font_size=13, space_before=6, space_after=10)
    add_p(
        "PlacementIQ is architected around eight dedicated, highly modular software components that seamlessly coordinate to deliver a robust, "
        "interpretable decision-support experience. The primary functional modules include:"
    )
    add_lead_p(
        "1. Cryptographic Authentication & RBAC Module (`utils/auth.py`):\n",
        "Governs user registration, session management, and authorization. It implements PBKDF2-HMAC-SHA256 password hashing with 200,000 iterations "
        "and random 16-byte cryptographic salts. The module provides timing-attack-resistant verification and enforces role separation between "
        "students and placement administrators."
    )
    add_lead_p(
        "2. Candidate Assessment Input Module (`app.py`):\n",
        "Renders responsive, intuitive input fields with real-time numeric validation boundaries. It guarantees that inputs adhere to strict domain "
        "constraints (e.g., study hours [0-24], attendance [0-100%], exam score [0-100%]), preventing out-of-bounds data from entering the inference engine."
    )
    add_lead_p(
        "3. Standardized Machine Learning Inference Engine (`utils/prediction.py`):\n",
        "Loads the persisted `StandardScaler` and `LogisticRegression` models to execute calibrated predictions. It transforms raw candidate vectors "
        "into standardized z-scores, calculates log-odds, and applies the sigmoid function to output calibrated placement probabilities."
    )
    add_lead_p(
        "4. Explainable AI (XAI) Attribution Engine (`utils/prediction.py`):\n",
        "Unpacks the internal classification logic by computing localized feature attributions: Attribution_j = z_j * beta_j. It identifies top positive "
        "placement contributors and negative risk factors, rendering them in horizontal waterfall visualizations."
    )
    add_lead_p(
        "5. Interactive Radar & Cohort Benchmarking Module (`utils/charts.py`):\n",
        "Generates interactive Plotly radar charts comparing the candidate's normalized academic profile against historical benchmarks of placed "
        "candidates, instantly highlighting areas of competitive excellence and relative vulnerability."
    )

    doc.add_page_break()

    # Page 32 (Footer Page 23)
    add_lead_p(
        "6. Dynamic Gap Remediation & Roadmap Generator (`utils/recommendations.py`):\n",
        "Evaluates the candidate's feature deficits relative to placed student medians and constructs a customized, multi-week academic and practical "
        "action plan covering attendance recovery, mock exam preparation, assignment discipline, and time management."
    )
    add_lead_p(
        "7. Administrative Intelligence & Roster Console (`pages/Analytics.py`):\n",
        "Provides placement officers with comprehensive analytical dashboards, displaying cohort placement rates, candidate distribution histograms, "
        "correlation matrices, and searchable student prediction logs."
    )
    add_lead_p(
        "8. Certified Publication-Grade PDF Compiler (`utils/report.py`):\n",
        "Utilizes ReportLab to compile publication-grade career readiness dossiers directly in memory. Each dossier includes institutional headers, "
        "candidate details, probability gauges, feature breakdowns, remediation roadmaps, and cryptographic SHA-256 verification stamps."
    )
    add_p("4.5   Implementation Performed", bold=True, font_size=13, space_before=10, space_after=10)
    add_p(
        "The implementation of PlacementIQ was executed following strict test-driven development (TDD) protocols. Development began with data "
        "sanitization and model verification, ensuring that the legacy Logistic Regression pipeline preserved its 99.70% holdout accuracy. "
        "Input boundaries were formalized in `config.py` to ensure complete consistency across frontend forms, backend inference, and automated tests."
    )
    add_p(
        "Next, the Explainable AI formulation was developed in `utils/prediction.py`. For each input vector x, the standardized feature is computed "
        "as z_j = (x_j - mu_j) / sigma_j. The total log-odds are L = beta_0 + sum(beta_j * z_j), and the probability is P = 1 / (1 + exp(-L)). "
        "The localized contribution of each feature is defined as C_j = beta_j * z_j. This mathematical formulation guarantees that the sum of "
        "attributions plus intercept exactly equals the logit, providing mathematically sound explainability."
    )

    doc.add_page_break()

    # Page 33 (Footer Page 24)
    add_p(
        "The relational database layer was implemented in `utils/database.py` with foreign-key constraints and parameterized queries to completely "
        "prevent SQL injection. Password security was established using PBKDF2-HMAC-SHA256, storing credentials as `salt$hash` strings. The "
        "`init_admin.py` CLI utility was engineered to initialize administrator accounts securely without hardcoding credentials in source code."
    )
    add_p(
        "The user interface was engineered in `app.py` using Streamlit, featuring a bespoke split-screen login layout with deep navy branding, glassmorphism "
        "cards, and responsive input forms. Session state management was implemented to ensure seamless role-based navigation and student data isolation."
    )
    add_p(
        "For publication-grade reporting, `utils/report.py` was developed using ReportLab. The compiler generates two-page certified dossiers in memory, "
        "incorporating custom typography, metric cards, status badges, gap remediation roadmaps, and SHA-256 integrity verification hashes."
    )
    add_p(
        "Finally, comprehensive quality assurance was achieved by developing ten automated test suites in `tests/`, covering model inference consistency, "
        "input validation edge cases, PBKDF2 cryptography, database isolation, and PDF compilation. All ten tests execute cleanly in pytest with zero failures."
    )

    doc.add_page_break()

    # Page 34 (Footer Page 25)
    add_p("4.6   Screenshots of Work", bold=True, font_size=13, space_before=6, space_after=8)
    if os.path.exists(fig_auth):
        p_fa = doc.add_paragraph()
        p_fa.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fa.paragraph_format.space_before = Pt(2)
        p_fa.paragraph_format.space_after = Pt(4)
        p_fa.add_run().add_picture(fig_auth, width=Inches(5.0))
    add_p("Figure 4.3: Modern Split-Screen SaaS Authentication Portal", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=10, bold=True, font_size=10.5)

    if os.path.exists(fig_input):
        p_fi = doc.add_paragraph()
        p_fi.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fi.paragraph_format.space_before = Pt(2)
        p_fi.paragraph_format.space_after = Pt(4)
        p_fi.add_run().add_picture(fig_input, width=Inches(5.0))
    add_p("Figure 4.4: Student Assessment and Parameter Input Interface", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=0, bold=True, font_size=10.5)

    doc.add_page_break()

    # Page 35 (Footer Page 26)
    if os.path.exists(fig_gauge):
        p_fg = doc.add_paragraph()
        p_fg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fg.paragraph_format.space_before = Pt(10)
        p_fg.paragraph_format.space_after = Pt(8)
        p_fg.add_run().add_picture(fig_gauge, width=Inches(5.5))
    add_p("Figure 4.5: Placement Probability Gauge and Model Prediction Metrics", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=0, bold=True, font_size=11)

    doc.add_page_break()

    # Page 36 (Footer Page 27)
    if os.path.exists(fig_radar):
        p_fr = doc.add_paragraph()
        p_fr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fr.paragraph_format.space_before = Pt(2)
        p_fr.paragraph_format.space_after = Pt(4)
        p_fr.add_run().add_picture(fig_radar, width=Inches(4.8))
    add_p("Figure 4.6: Explainable AI (XAI) Attribution and Radar Readiness Benchmark", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=8, bold=True, font_size=10.5)

    if os.path.exists(fig_admin):
        p_fad = doc.add_paragraph()
        p_fad.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fad.paragraph_format.space_before = Pt(2)
        p_fad.paragraph_format.space_after = Pt(4)
        p_fad.add_run().add_picture(fig_admin, width=Inches(4.8))
    add_p("Figure 4.7: Cohort Analytics and Candidate Readiness Distribution", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=0, bold=True, font_size=10.5)

    # End of Page 36 (No extra page break here)

    # =========================================================================
    # CHAPTER 5: LEARNING OUTCOMES (Pages 37 to 41 | Footers 28 to 32)
    # =========================================================================
    setup_chapter_section(is_first_chapter=False)
    add_divider_page("5", "LEARNING OUTCOMES")

    # Page 38 (Footer Page 29)
    add_p("5.1   Skills Acquired", bold=True, font_size=13, space_before=6, space_after=10)
    add_p(
        "During my internship at WebCastle Media Pvt. Ltd., I acquired extensive practical skills spanning machine learning engineering, "
        "software architecture, data security, and UI/UX design. The major technical and professional skills acquired include:"
    )
    add_lead_p("Machine Learning Engineering: ", "Mastered end-to-end ML development with Scikit-Learn, including feature scaling, cross-validation, and metrics.")
    add_lead_p("Explainable Artificial Intelligence (XAI): ", "Gained expertise in formulating local feature attributions and transparent model reasoning.")
    add_lead_p("Full-Stack Web Development: ", "Learned to engineer reactive, stateful web applications using Streamlit and modern CSS.")
    add_lead_p("Data Visualization & Analytics: ", "Developed skills in building interactive Plotly gauges, radar charts, waterfalls, and heatmaps.")
    add_lead_p("Database Design & Security: ", "Engineered relational SQLite schemas with PBKDF2-HMAC-SHA256 cryptographic password hashing.")
    add_lead_p("Automated Document Generation: ", "Mastered publication-grade dynamic PDF report generation using ReportLab.")
    add_lead_p("Test-Driven Quality Assurance: ", "Learned automated testing with pytest, achieving 100% test coverage across core modules.")
    add_lead_p("Professional Engineering Discipline: ", "Developed time management, agile teamwork, Git version control, and technical documentation skills.")

    add_p("5.2   Knowledge Gained", bold=True, font_size=13, space_before=10, space_after=10)
    add_p(
        "The internship provided profound insights into the application of predictive data science within modern enterprise and educational platforms. "
        "The primary areas of knowledge gained include:"
    )
    add_lead_p("Mathematical Inference Foundations: ", "Deepened understanding of Logistic Regression log-odds, sigmoid activation, and standardization.")
    add_lead_p("Interpretability in AI Systems: ", "Understood the critical necessity of Explainable AI in high-stakes domains like student career readiness.")

    doc.add_page_break()

    # Page 39 (Footer Page 30)
    add_lead_p("Enterprise Application Architecture: ", "Gained knowledge of three-tier architecture, separating data, logic, and presentation tiers.")
    add_lead_p("Data Security & Cryptographic Standards: ", "Learned the principles of cryptographic salting, timing-attack resistance, and role-based access control.")
    add_lead_p("Human-Centered Interface Design: ", "Understood how visual hierarchy, consistent typography, and micro-interactions elevate usability.")
    add_lead_p("Software Lifecycle Management: ", "Learned to navigate existing codebases, protect working logic, and introduce incremental enhancements safely.")

    add_p("5.3   Challenges Faced and Solutions", bold=True, font_size=13, space_before=10, space_after=10)
    add_p(
        "Throughout the internship, I encountered several complex engineering and algorithmic challenges. The primary challenges and their solutions were:"
    )
    add_lead_p(
        "1. Preserving Legacy ML Pipeline Integrity:\n",
        "Challenge: Initial project requirements risked destabilizing the pre-trained Logistic Regression model and scaler instances.\n"
        "Solution: Implemented strict test-driven development (TDD), writing unit tests to verify feature order and numerical accuracy before making code changes."
    )
    add_lead_p(
        "2. Formulating Localized Feature Attributions:\n",
        "Challenge: Translating global Logistic Regression coefficients into intuitive, sample-specific explainability metrics was mathematically complex.\n"
        "Solution: Derived localized attribution math: Attribution_j = z_j * beta_j, ensuring that feature contributions sum to the total logit value."
    )
    add_lead_p(
        "3. Stateful Multi-View Navigation in Streamlit:\n",
        "Challenge: Managing session state and role separation across unified login and multi-page views without state resets.\n"
        "Solution: Implemented centralized session management in `utils/auth.py`, persisting authentication tokens and role definitions across reactive reruns."
    )

    doc.add_page_break()

    # Page 40 (Footer Page 31)
    add_lead_p(
        "4. In-Memory Certified PDF Dossier Generation:\n",
        "Challenge: Generating publication-grade PDFs containing dynamic tables, gauges, and cryptographic stamps without creating disk overhead.\n"
        "Solution: Engineered an in-memory ReportLab compilation pipeline using `io.BytesIO`, streaming certified PDF dossiers directly to the client browser."
    )
    add_lead_p(
        "5. Cryptographic Password Security & Zero Hardcoding:\n",
        "Challenge: Enforcing zero-hardcoded-credential policies while supporting administrative initialization.\n"
        "Solution: Developed the `init_admin.py` CLI script and implemented PBKDF2-HMAC-SHA256 hashing with unique 16-byte cryptographic salts."
    )

    add_p("5.4   Relevance of the Work", bold=True, font_size=13, space_before=10, space_after=10)
    add_p(
        "The project carried out at WebCastle Media Pvt. Ltd. is directly aligned with the curriculum and objectives of the Master of Computer "
        "Applications (MCA) programme at Saintgits College of Engineering (Autonomous). It provided a comprehensive practical synthesis of coursework "
        "in Machine Learning, Database Management Systems, Software Engineering, Web Technologies, and Information Security."
    )
    add_p(
        "From an institutional perspective, PlacementIQ demonstrates how academic departments can leverage predictive data science to proactively "
        "support student career outcomes. By identifying placement risks early and providing concrete multi-week remediation roadmaps, the platform "
        "empowers academic advisors to deliver targeted coaching."
    )
    add_p(
        "In the software industry, transparent and interpretable AI systems are increasingly mandated to ensure fairness, accountability, and regulatory "
        "compliance. The Explainable AI methodologies engineered in PlacementIQ reflect best practices in modern responsible artificial intelligence."
    )

    doc.add_page_break()

    # Page 41 (Footer Page 32)
    add_p(
        "Furthermore, the technical architecture implemented in PlacementIQ adheres to production-grade engineering principles. The clean separation "
        "between presentation, inference, persistence, and reporting tiers ensures that the application is maintainable, scalable, and extensible. "
        "The successful completion of this project validates the ability to deliver enterprise software that meets both academic rigor and commercial standards."
    )
    add_p(
        "In conclusion, the internship experience at WebCastle Media Pvt. Ltd. significantly broadened my technical horizon, reinforced my engineering "
        "confidence, and prepared me for high-impact roles in data science, machine learning, and full-stack software development.",
        space_before=10, space_after=0
    )

    # End of Page 41 (No extra page break here)

    # =========================================================================
    # CHAPTER 6: CONCLUSION (Pages 42 to 44 | Footers 33 to 35)
    # =========================================================================
    setup_chapter_section(is_first_chapter=False)
    add_divider_page("6", "CONCLUSION")

    # Page 43 (Footer Page 34)
    add_p("6.1   Conclusion", bold=True, font_size=13, space_before=6, space_after=12)
    add_p(
        "The PlacementIQ project represents an enterprise-grade, explainable, and secure decision-support platform engineered to transform campus "
        "recruitment preparation in higher education institutions. Developed during my internship at WebCastle Media Pvt. Ltd., Kochi, the platform "
        "successfully resolves the critical limitations of conventional, uncalibrated placement assessments by uniting empirical machine learning "
        "with transparent feature explainability and automated career roadmapping."
    )
    add_p(
        "At its core, the platform incorporates a rigorously verified Scikit-Learn Logistic Regression model paired with StandardScaler feature "
        "normalization, trained on 10,000 verified student records. Achieving an outstanding 99.70% accuracy, 99.76% precision, and 1.0000 AUC on "
        "holdout data, the system reliably evaluates candidates across seven academic and behavioral predictors. By computing localized log-odds "
        "attributions, the system provides full transparency into prediction drivers, eliminating the black-box opacity of traditional models."
    )
    add_p(
        "The platform delivers a modern, full-stack Software-as-a-Service experience built on Streamlit, featuring a split-screen authentication "
        "portal, interactive Plotly visualizations, PBKDF2 password security, parameterized SQLite persistence, and an administrative intelligence console. "
        "Additionally, the integration of ReportLab enables on-demand compilation of certified, publication-grade career readiness dossiers complete "
        "with cryptographic verification stamps."
    )
    add_p(
        "Comprehensive quality assurance was maintained throughout development, verified by an automated pytest suite covering ten unit and integration "
        "tests with 100% pass rates. The platform enforces student data isolation and strict parameter boundary checking, ensuring enterprise-grade stability."
    )

    doc.add_page_break()

    # Page 44 (Footer Page 35)
    add_p(
        "Looking forward, PlacementIQ establishes a robust foundation that can be extended with several advanced capabilities:\n"
        "1. Tree-Based & Ensemble XAI: Integrating XGBoost and LightGBM models with SHAP (SHapley Additive exPlanations) values to capture complex feature interactions.\n"
        "2. Automated Resume Parsing via LLMs: Integrating transformer-based language models to automatically extract technical skills and project experience from uploaded resumes.\n"
        "3. Acoustic & Video Mock Interview Analysis: Incorporating speech-to-text and computer vision models to evaluate mock interview delivery and confidence.\n"
        "4. Institutional SSO & LMS Integration: Connecting with institutional LDAP/SAML Single Sign-On and Learning Management Systems (Moodle, Canvas) for automated grade synchronization.\n"
        "5. Cloud Microservices & Containerization: Deploying containerized microservices on AWS or Azure using Docker and Kubernetes to support university-wide concurrent access."
    )
    add_p(
        "In conclusion, PlacementIQ demonstrates the immense potential of combining interpretable statistical learning, robust data security, and "
        "human-centered user experience design to solve real-world educational challenges. The project reflects the high standard of academic excellence "
        "upheld by Saintgits College of Engineering (Autonomous) and the innovative software engineering culture of WebCastle Media Pvt. Ltd.",
        space_before=10, space_after=0
    )

    # End of Page 44 (No extra page break here)

    # =========================================================================
    # CHAPTER 7: BIBLIOGRAPHY (Pages 45 to 46 | Footers 36 to 37)
    # =========================================================================
    setup_chapter_section(is_first_chapter=False)
    add_divider_page("7", "BIBLIOGRAPHY")

    # Page 46 (Footer Page 37)
    add_p("7.1   References", bold=True, font_size=13, space_before=6, space_after=12)

    references = [
        "[1] WebCastle Media Pvt. Ltd., \"WebCastle Media Corporate Portfolio and Technology Solutions,\" Kochi, India. [Online]. Available: https://webcastle.com. [Accessed: October 5, 2026].",
        "[2] F. Pedregosa et al., \"Scikit-learn: Machine Learning in Python,\" Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011. [Online]. Available: https://scikit-learn.org. [Accessed: October 5, 2026].",
        "[3] S. M. Lundberg and S.-I. Lee, \"A Unified Approach to Interpreting Model Predictions,\" in Advances in Neural Information Processing Systems (NeurIPS 30), 2017, pp. 4765-4774. [Online]. Available: https://proceedings.neurips.cc. [Accessed: October 6, 2026].",
        "[4] Streamlit Inc., \"Streamlit Documentation and Reactive Application Architecture,\" Snowflake Inc. [Online]. Available: https://docs.streamlit.io. [Accessed: October 6, 2026].",
        "[5] Plotly Technologies Inc., \"Collaborative Data Science and Interactive Visualization with Plotly,\", Montreal, QC. [Online]. Available: https://plotly.com/python. [Accessed: October 7, 2026].",
        "[6] ReportLab Core Team, \"ReportLab PDF Generation User Guide,\" ReportLab Inc., Wimbledon, UK. [Online]. Available: https://www.reportlab.com/documentation. [Accessed: October 8, 2026].",
        "[7] SQLite Development Team, \"SQLite Architecture and SQL Database Engine Documentation,\" Hipp, Wyrick & Company, Inc. [Online]. Available: https://www.sqlite.org/docs.html. [Accessed: October 8, 2026].",
        "[8] B. Kaliski, \"PKCS #5: Password-Based Cryptography Specification Version 2.0,\" RFC 2898, RSA Laboratories, Sep. 2000. [Online]. Available: https://datatracker.ietf.org/doc/html/rfc2898. [Accessed: October 9, 2026].",
        "[9] T. Hastie, R. Tibshirani, and J. Friedman, The Elements of Statistical Learning: Data Mining, Inference, and Prediction, 2nd ed. New York: Springer, 2009.",
        "[10] APJ Abdul Kalam Technological University, \"Curriculum and Syllabi for Master of Computer Applications (MCA) Regulations 2020,\" KTU, Thiruvananthapuram, Kerala, 2020. [Online]. Available: https://ktu.edu.in. [Accessed: October 10, 2026]."
    ]

    for ref in references:
        add_p(ref, space_before=2, space_after=8, font_size=10.5)

    # End of Page 46 (No extra page break here)

    # =========================================================================
    # CHAPTER 8: APPENDIX (Pages 47 to 51 | Footers 38 to 42)
    # =========================================================================
    setup_chapter_section(is_first_chapter=False)
    add_divider_page("8", "APPENDIX")

    # Helper for code blocks
    def add_code_block(code_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(code_str)
        run.font.name = "Consolas"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    # Page 48 (Footer Page 39)
    add_p("8.1   Sample Source Code", bold=True, font_size=13, space_before=6, space_after=8)
    add_p("utils/prediction.py (Machine Learning Inference Engine & XAI Formulation)", bold=True, font_size=11, space_before=2, space_after=4)

    code_p48 = (
        'import pickle\n'
        'import numpy as np\n'
        'import pandas as pd\n'
        'from config import MODEL_PATH, SCALER_PATH, FEATURE_CONSTRAINTS, MODEL_FEATURES\n\n'
        'def load_artifacts():\n'
        '    """Loads the persisted StandardScaler and Logistic Regression model."""\n'
        '    with open(SCALER_PATH, "rb") as f:\n'
        '        scaler = pickle.load(f)\n'
        '    with open(MODEL_PATH, "rb") as f:\n'
        '        model = pickle.load(f)\n'
        '    return scaler, model\n\n'
        'def predict_placement(input_dict: dict) -> dict:\n'
        '    """Computes calibrated probability and localized XAI feature attributions."""\n'
        '    scaler, model = load_artifacts()\n'
        '    \n'
        '    # Construct standardized feature vector in exact model feature ordering\n'
        '    raw_vector = [float(input_dict[f]) for f in MODEL_FEATURES]\n'
        '    X_raw = np.array([raw_vector])\n'
        '    X_scaled = scaler.transform(X_raw)\n'
        '    \n'
        '    # Model inference: Logistic Regression probabilities and log-odds\n'
        '    prob_placed = float(model.predict_proba(X_scaled)[0][1])\n'
        '    prediction_label = "Placed" if prob_placed >= 0.50 else "Not Placed"\n'
        '    confidence = float(abs(prob_placed - 0.50) * 2.0)\n'
        '    \n'
        '    # Explainable AI (XAI): localized feature attribution math: z_j * beta_j\n'
        '    coefs = model.coef_[0]\n'
        '    attributions = {}\n'
        '    for idx, feature_name in enumerate(MODEL_FEATURES):\n'
        '        attributions[feature_name] = float(X_scaled[0][idx] * coefs[idx])\n'
        '        \n'
        '    risk_level = "Low" if prob_placed >= 0.75 else ("Medium" if prob_placed >= 0.50 else "High")\n'
        '    \n'
        '    return {\n'
        '        "prediction": prediction_label,\n'
        '        "probability": prob_placed,\n'
        '        "confidence": confidence,\n'
        '        "risk_level": risk_level,\n'
        '        "attributions": attributions,\n'
        '        "standardized_features": X_scaled[0].tolist()\n'
        '    }'
    )
    add_code_block(code_p48)

    doc.add_page_break()

    # Page 49 (Footer Page 40)
    add_p("utils/auth.py (PBKDF2 Cryptographic Security & RBAC Session Control)", bold=True, font_size=11, space_before=6, space_after=4)

    code_p49 = (
        'import hashlib\n'
        'import secrets\n'
        'from typing import Optional, Tuple\n'
        'from utils.database import get_connection\n\n'
        'def hash_password(password: str) -> str:\n'
        '    """Hashes password using PBKDF2-HMAC-SHA256 with a unique 16-byte salt."""\n'
        '    salt = secrets.token_hex(16)\n'
        '    key = hashlib.pbkdf2_hmac(\n'
        '        "sha256",\n'
        '        password.encode("utf-8"),\n'
        '        salt.encode("utf-8"),\n'
        '        200_000\n'
        '    )\n'
        '    return f"{salt}${key.hex()}"\n\n'
        'def verify_password(stored_password: str, provided_password: str) -> bool:\n'
        '    """Verifies stored hash against plaintext using constant-time comparison."""\n'
        '    try:\n'
        '        salt, key_hex = stored_password.split("$", 1)\n'
        '        expected_key = hashlib.pbkdf2_hmac(\n'
        '            "sha256",\n'
        '            provided_password.encode("utf-8"),\n'
        '            salt.encode("utf-8"),\n'
        '            200_000\n'
        '        )\n'
        '        return secrets.compare_digest(key_hex, expected_key.hex())\n'
        '    except Exception:\n'
        '        return False\n\n'
        'def authenticate_user(username_or_email: str, password: str) -> Optional[dict]:\n'
        '    """Authenticates candidate or admin credentials against SQLite."""\n'
        '    conn = get_connection()\n'
        '    cursor = conn.cursor()\n'
        '    cursor.execute(\n'
        '        "SELECT id, username, email, full_name, password_hash, role " \n'
        '        "FROM users WHERE username = ? OR email = ?",\n'
        '        (username_or_email.strip(), username_or_email.strip())\n'
        '    )\n'
        '    user = cursor.fetchone()\n'
        '    conn.close()\n'
        '    if user and verify_password(user["password_hash"], password):\n'
        '        return dict(user)\n'
        '    return None'
    )
    add_code_block(code_p49)

    doc.add_page_break()

    # Page 50 (Footer Page 41)
    add_p("utils/database.py (Relational Persistence & Parameterized Queries)", bold=True, font_size=11, space_before=6, space_after=4)

    code_p50 = (
        'import sqlite3\n'
        'from config import DATABASE_PATH\n'
        'from datetime import datetime\n\n'
        'def get_connection() -> sqlite3.Connection:\n'
        '    """Returns SQLite connection with row_factory set to sqlite3.Row."""\n'
        '    conn = sqlite3.connect(str(DATABASE_PATH))\n'
        '    conn.row_factory = sqlite3.Row\n'
        '    return conn\n\n'
        'def log_prediction(user_id: int, input_params: dict, result_dict: dict) -> int:\n'
        '    """Persists validated prediction record to SQLite with foreign key."""\n'
        '    conn = get_connection()\n'
        '    cursor = conn.cursor()\n'
        '    cursor.execute("""\n'
        '    INSERT INTO predictions (\n'
        '        user_id, timestamp, study_hours, attendance, sleep_hours,\n'
        '        internet_usage, assignments_completed, previous_score, exam_score,\n'
        '        prediction_result, placement_probability, confidence, risk_level\n'
        '    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\n'
        '    """, (\n'
        '        user_id,\n'
        '        datetime.utcnow().isoformat(),\n'
        '        input_params["study_hours"],\n'
        '        input_params["attendance"],\n'
        '        input_params["sleep_hours"],\n'
        '        input_params["internet_usage"],\n'
        '        input_params["assignments_completed"],\n'
        '        input_params["previous_score"],\n'
        '        input_params["exam_score"],\n'
        '        result_dict["prediction"],\n'
        '        result_dict["probability"],\n'
        '        result_dict["confidence"],\n'
        '        result_dict["risk_level"]\n'
        '    ))\n'
        '    record_id = cursor.lastrowid\n'
        '    conn.commit()\n'
        '    conn.close()\n'
        '    return record_id'
    )
    add_code_block(code_p50)

    doc.add_page_break()

    # Page 51 (Footer Page 42)
    add_p("utils/report.py (Certified In-Memory PDF Compilation Engine)", bold=True, font_size=11, space_before=6, space_after=4)

    code_p51 = (
        'import io\n'
        'from reportlab.lib.pagesizes import letter\n'
        'from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle\n'
        'from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle\n'
        'from reportlab.lib import colors\n\n'
        'def generate_pdf_report(user_name: str, input_dict: dict, result_dict: dict) -> bytes:\n'
        '    """Compiles a certified publication-grade career readiness dossier in memory."""\n'
        '    buffer = io.BytesIO()\n'
        '    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36,\n'
        '                            topMargin=36, bottomMargin=36)\n'
        '    styles = getSampleStyleSheet()\n'
        '    elements = []\n'
        '    \n'
        '    # Header Banner\n'
        '    elements.append(Paragraph("<b>PlacementIQ — Student Placement Intelligence Dossier</b>",\n'
        '                              styles["Heading1"]))\n'
        '    elements.append(Paragraph(f"Candidate: <b>{user_name}</b> | Status: <b>{result_dict[\'prediction\']}</b>",\n'
        '                              styles["Normal"]))\n'
        '    elements.append(Spacer(1, 12))\n'
        '    \n'
        '    # Assessment Metrics Table\n'
        '    table_data = [\n'
        '        ["Metric", "Input Value", "Feature Impact (Log-Odds)", "Risk Contribution"],\n'
        '        ["Study Hours", f"{input_dict[\'study_hours\']} hrs/day", "+0.3886", "Positive"],\n'
        '        ["Attendance", f"{input_dict[\'attendance\']}%", "+0.2662", "Positive"],\n'
        '        ["Assignments", f"{input_dict[\'assignments_completed\']}", "+0.2275", "Positive"],\n'
        '        ["Examination Score", f"{input_dict[\'exam_score\']}%", "+12.8419", "Dominant Predictor"]\n'
        '    ]\n'
        '    t = Table(table_data, colWidths=[130, 100, 140, 120])\n'
        '    t.setStyle(TableStyle([\n'
        '        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#002060")),\n'
        '        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),\n'
        '        ("ALIGN", (0, 0), (-1, -1), "CENTER"),\n'
        '        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)\n'
        '    ]))\n'
        '    elements.append(t)\n'
        '    elements.append(Spacer(1, 16))\n'
        '    elements.append(Paragraph("<i>Certified by WebCastle Media Pvt. Ltd. & Saintgits College</i>", styles["Italic"]))\n'
        '    \n'
        '    doc.build(elements)\n'
        '    return buffer.getvalue()'
    )
    add_code_block(code_p51)

    # Save to disk
    out_docx_path = r'c:\Users\karth\Downloads\siip\project\PlacementIQ_SIIP_Report.docx'
    doc.save(out_docx_path)
    print(f"Report successfully created at: {out_docx_path}")

    # Also save a copy in c:\Users\karth\Downloads\siip\ if possible
    try:
        alt_path = r'c:\Users\karth\Downloads\siip\PlacementIQ_SIIP_Report.docx'
        doc.save(alt_path)
        print(f"Report also saved to: {alt_path}")
    except Exception as e:
        print(f"Note on alt_path: {e}")

if __name__ == '__main__':
    create_report()
