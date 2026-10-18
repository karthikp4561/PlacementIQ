import io
from datetime import datetime
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from config import APP_TITLE, APP_SUBTITLE, VERSION

def generate_pdf_report(
    user_info: Dict[str, Any],
    prediction_data: Dict[str, Any],
    recommendations: List[Dict[str, Any]]
) -> bytes:
    """
    Generates a publication-grade academic PDF report in memory using ReportLab.
    Returns the PDF bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0f172a")    # Deep Slate
    accent_blue = colors.HexColor("#2563eb")      # Royal Blue
    teal_color = colors.HexColor("#0891b2")       # Cyan/Teal
    text_dark = colors.HexColor("#1e293b")        # Dark Slate Text
    text_muted = colors.HexColor("#64748b")       # Muted Gray

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=teal_color,
        alignment=0
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=text_muted
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=text_dark
    )

    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10.5,
        textColor=text_muted
    )

    story = []

    # Header section
    story.append(Paragraph(f"<b>{APP_TITLE}</b> — Placement Intelligence Report", title_style))
    story.append(Paragraph(f"{APP_SUBTITLE} | Version {VERSION}", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_blue, spaceBefore=0, spaceAfter=12))

    # Student & Metadata block
    timestamp_str = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    student_name = user_info.get("full_name", "Student")
    student_email = user_info.get("email", "N/A")
    student_username = user_info.get("username", "N/A")

    meta_table_data = [
        [
            Paragraph("<b>Candidate Name:</b>", meta_label), Paragraph(student_name, meta_val),
            Paragraph("<b>Report Generated:</b>", meta_label), Paragraph(timestamp_str, meta_val)
        ],
        [
            Paragraph("<b>Email / Account:</b>", meta_label), Paragraph(f"{student_email} (@{student_username})", meta_val),
            Paragraph("<b>Model Architecture:</b>", meta_label), Paragraph("StandardScaler + Logistic Regression", meta_val)
        ]
    ]

    meta_table = Table(meta_table_data, colWidths=[1.3*inch, 2.3*inch, 1.4*inch, 2.3*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Executive Summary Card
    pred_res = prediction_data.get("prediction_result", "N/A")
    is_placed = (pred_res == "Placed")
    status_color = colors.HexColor("#059669") if is_placed else colors.HexColor("#dc2626")
    status_bg = colors.HexColor("#ecfdf5") if is_placed else colors.HexColor("#fef2f2")

    prob_str = f"{prediction_data.get('placement_probability', 0.0):.1f}%"
    conf_str = f"{prediction_data.get('confidence', 0.0):.1f}%"
    risk_str = prediction_data.get("risk_level", "N/A")
    score_str = f"{prediction_data.get('overall_score', 0.0):.1f}"

    kpi_data = [
        [
            Paragraph("<b>PREDICTION OUTCOME</b>", meta_label),
            Paragraph("<b>PLACEMENT PROBABILITY</b>", meta_label),
            Paragraph("<b>MODEL CONFIDENCE</b>", meta_label),
            Paragraph("<b>RISK ASSESSMENT</b>", meta_label)
        ],
        [
            Paragraph(f"<font size=14 color='{status_color.hexval()}'><b>{pred_res.upper()}</b></font>", body_style),
            Paragraph(f"<font size=14 color='#2563eb'><b>{prob_str}</b></font>", body_style),
            Paragraph(f"<font size=14 color='#0f172a'><b>{conf_str}</b></font>", body_style),
            Paragraph(f"<font size=14 color='{status_color.hexval()}'><b>{risk_str}</b></font>", body_style),
        ]
    ]

    kpi_table = Table(kpi_data, colWidths=[1.8*inch, 1.8*inch, 1.8*inch, 1.8*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BACKGROUND', (0,1), (-1,1), status_bg),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 14))

    # Input Metrics Breakdown
    story.append(Paragraph("<b>Academic & Behavioral Profile Metrics</b>", section_heading))
    inputs = prediction_data.get("inputs", {})

    input_table_data = [
        [
            Paragraph("<b>Attribute</b>", meta_label),
            Paragraph("<b>Observed Value</b>", meta_label),
            Paragraph("<b>Training Baseline (Mean)</b>", meta_label),
            Paragraph("<b>Standard Deviation</b>", meta_label)
        ],
        [Paragraph("Study Hours", body_style), Paragraph(f"{inputs.get('study_hours', 0):.1f} hrs/day", body_style), Paragraph("5.99 hrs", body_style), Paragraph("±3.17", body_style)],
        [Paragraph("Attendance", body_style), Paragraph(f"{inputs.get('attendance', 0):.1f}%", body_style), Paragraph("69.88%", body_style), Paragraph("±17.59", body_style)],
        [Paragraph("Sleep Hours", body_style), Paragraph(f"{inputs.get('sleep_hours', 0):.1f} hrs/day", body_style), Paragraph("6.51 hrs", body_style), Paragraph("±1.70", body_style)],
        [Paragraph("Internet Usage", body_style), Paragraph(f"{inputs.get('internet_usage', 0):.1f} hrs/day", body_style), Paragraph("6.07 hrs", body_style), Paragraph("±3.15", body_style)],
        [Paragraph("Assignments Completed", body_style), Paragraph(f"{inputs.get('assignments_completed', 0):.0f}", body_style), Paragraph("9.97 count", body_style), Paragraph("±6.05", body_style)],
        [Paragraph("Previous Score", body_style), Paragraph(f"{inputs.get('previous_score', 0):.1f}%", body_style), Paragraph("64.82%", body_style), Paragraph("±17.42", body_style)],
        [Paragraph("Examination Score", body_style), Paragraph(f"{inputs.get('exam_score', 0):.1f}%", body_style), Paragraph("86.76%", body_style), Paragraph("±15.03", body_style)],
    ]

    input_table = Table(input_table_data, colWidths=[2.3*inch, 1.8*inch, 1.8*inch, 1.3*inch])
    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(input_table)
    story.append(Spacer(1, 14))

    # Feature Importance Explanation
    story.append(Paragraph("<b>Explainable Model Insights & Impact Drivers</b>", section_heading))
    attributions = prediction_data.get("attributions", [])[:4]

    xai_rows = [
        [
            Paragraph("<b>Feature</b>", meta_label),
            Paragraph("<b>Statistical Direction</b>", meta_label),
            Paragraph("<b>Relative Impact Weight</b>", meta_label),
            Paragraph("<b>Analysis</b>", meta_label)
        ]
    ]

    for attr in attributions:
        dir_color = "#059669" if attr['direction'] == 'Positive Driver' else ("#dc2626" if attr['direction'] == 'Negative Driver' else "#64748b")
        xai_rows.append([
            Paragraph(f"<b>{attr['label']}</b>", body_style),
            Paragraph(f"<font color='{dir_color}'><b>{attr['direction']}</b></font>", body_style),
            Paragraph(f"{attr['relative_percentage']}%", body_style),
            Paragraph(f"Z-Score: {attr['z_score']:.2f} (Model weight: {attr['coefficient']:+.2f})", body_style)
        ])

    xai_table = Table(xai_rows, colWidths=[2.2*inch, 1.5*inch, 1.5*inch, 2.0*inch])
    xai_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(xai_table)
    story.append(Spacer(1, 14))

    # Personalized Improvement Plan
    story.append(Paragraph("<b>Actionable Academic & Career Development Plan</b>", section_heading))
    rec_rows = [
        [
            Paragraph("<b>Category</b>", meta_label),
            Paragraph("<b>Priority</b>", meta_label),
            Paragraph("<b>Current / Target</b>", meta_label),
            Paragraph("<b>Actionable Guidance</b>", meta_label)
        ]
    ]

    for rec in recommendations[:4]:
        prio_color = "#dc2626" if rec['priority'] == 'High' else ("#d97706" if rec['priority'] == 'Medium' else "#2563eb")
        rec_rows.append([
            Paragraph(f"<b>{rec['category']}</b>", body_style),
            Paragraph(f"<font color='{prio_color}'><b>{rec['priority']}</b></font>", body_style),
            Paragraph(f"{rec.get('current', '')} &rarr; <b>{rec.get('target', '')}</b>", body_style),
            Paragraph(rec['advice'], body_style)
        ])

    rec_table = Table(rec_rows, colWidths=[1.5*inch, 0.9*inch, 1.6*inch, 3.2*inch])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 14))

    # Disclaimer
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=6, spaceAfter=6))
    disclaimer_text = (
        "<b>ACADEMIC & ETHICAL AI DISCLAIMER:</b> This report is generated by the PlacementIQ machine learning decision "
        "support system for academic and self-assessment purposes. The placement probability reflects statistical associations "
        "identified by a supervised logistic regression model trained on a 10,000-record academic benchmark dataset. "
        "Actual placement depends on dynamic corporate interview processes, technical coding rounds, and non-quantified competencies. "
        "This evaluation does not constitute a legal, institutional, or contractual employment guarantee."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
