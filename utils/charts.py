import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Any

# Plotly theme colors tailored for clean modern SaaS theme (Fasto / Looker / Tableau)
THEME_BG = "#ffffff"
TEXT_COLOR = "#0f172a"
GRID_COLOR = "#f1f5f9"

def probability_gauge(probability: float) -> go.Figure:
    """Creates a modern circular gauge displaying placement probability."""
    prob = max(0.0, min(100.0, float(probability)))

    if prob >= 80:
        bar_color = "#10b981"  # Emerald
    elif prob >= 60:
        bar_color = "#2563eb"  # Royal Blue
    elif prob >= 40:
        bar_color = "#f59e0b"  # Amber
    else:
        bar_color = "#ef4444"  # Rose

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob,
        number={'suffix': "%", 'font': {'size': 38, 'color': TEXT_COLOR, 'family': 'Plus Jakarta Sans, sans-serif'}},
        title={'text': "<b>Placement Probability</b>", 'font': {'size': 16, 'color': "#475569"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
            'bar': {'color': bar_color, 'thickness': 0.28},
            'bgcolor': "#f8fafc",
            'borderwidth': 1,
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.12)"},
                {'range': [40, 60], 'color': "rgba(245, 158, 11, 0.12)"},
                {'range': [60, 80], 'color': "rgba(37, 99, 235, 0.12)"},
                {'range': [80, 100], 'color': "rgba(16, 185, 129, 0.15)"}
            ],
            'threshold': {
                'line': {'color': "#0f172a", 'width': 3},
                'thickness': 0.75,
                'value': prob
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font={'color': TEXT_COLOR},
        height=280,
        margin=dict(l=30, r=30, t=50, b=20)
    )
    return fig

def feature_attribution_bar(attributions: List[Dict[str, Any]]) -> go.Figure:
    """Creates a horizontal diverging bar chart representing explainable feature attributions."""
    labels = [a["label"] for a in attributions]
    contribs = [a["contribution"] for a in attributions]
    colors_list = ["#10b981" if c >= 0 else "#ef4444" for c in contribs]

    fig = go.Figure(go.Bar(
        x=contribs,
        y=labels,
        orientation='h',
        marker=dict(
            color=colors_list,
            line=dict(color="rgba(255,255,255,0.2)", width=1)
        ),
        text=[f"{c:+.2f}" for c in contribs],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=11)
    ))

    fig.update_layout(
        title="<b>Explainable Feature Contributions (Log-Odds Impact)</b>",
        title_font=dict(size=15, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=TEXT_COLOR),
        height=320,
        margin=dict(l=20, r=40, t=40, b=20),
        xaxis=dict(
            title="Log-Odds Shift &rarr;",
            gridcolor=GRID_COLOR,
            zerolinecolor="#94a3b8",
            zerolinewidth=2
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=11)
        )
    )
    return fig

def radar_chart(features: Dict[str, float]) -> go.Figure:
    """Creates an interactive radar plot displaying normalized student attributes."""
    categories = list(features.keys())
    values = list(features.values())

    # Benchmark typical means for MCA students
    benchmarks = {
        "Study Hours": 6.0,
        "Attendance": 70.0,
        "Sleep Hours": 6.5,
        "Internet Usage": 6.0,
        "Assignments": 10.0,
        "Previous Score": 65.0,
        "Exam Score": 85.0
    }

    # Normalize values to 0-100 scale for intuitive radar comparison
    norm_student = []
    norm_bench = []

    scales = {
        "Study Hours": 12.0,
        "Attendance": 100.0,
        "Sleep Hours": 10.0,
        "Internet Usage": 12.0,
        "Assignments": 20.0,
        "Previous Score": 100.0,
        "Exam Score": 100.0
    }

    for cat, val in zip(categories, values):
        max_s = scales.get(cat, 100.0)
        norm_student.append(min(100.0, (val / max_s) * 100.0))
        b_val = benchmarks.get(cat, val)
        norm_bench.append(min(100.0, (b_val / max_s) * 100.0))

    # Close loop
    plot_cats = categories + [categories[0]]
    plot_student = norm_student + [norm_student[0]]
    plot_bench = norm_bench + [norm_bench[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=plot_bench,
        theta=plot_cats,
        fill='toself',
        fillcolor='rgba(148, 163, 184, 0.15)',
        line=dict(color="#94a3b8", width=1.5, dash="dash"),
        name="Cohort Benchmark"
    ))

    fig.add_trace(go.Scatterpolar(
        r=plot_student,
        theta=plot_cats,
        fill='toself',
        fillcolor='rgba(6, 182, 212, 0.35)',
        line=dict(color="#06b6d4", width=2.5),
        name="Student Profile"
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(241, 245, 249, 0.7)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                linecolor=GRID_COLOR,
                gridcolor=GRID_COLOR
            ),
            angularaxis=dict(
                linecolor=GRID_COLOR,
                gridcolor=GRID_COLOR,
                tickfont=dict(color=TEXT_COLOR, size=11)
            )
        ),
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=TEXT_COLOR),
        height=360,
        margin=dict(l=40, r=40, t=30, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )
    return fig

def feature_chart(features: Dict[str, float]) -> go.Figure:
    """Legacy feature bar chart with upgraded dark theme aesthetics."""
    df = pd.DataFrame({
        "Feature": list(features.keys()),
        "Value": list(features.values())
    })

    fig = px.bar(
        df,
        x="Feature",
        y="Value",
        text="Value",
        color="Value",
        color_continuous_scale="Tealgrn"
    )

    fig.update_layout(
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=TEXT_COLOR),
        height=320,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
        xaxis=dict(gridcolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR)
    )
    return fig

def confusion_matrix_heatmap(cm: np.ndarray, labels: List[str] = ["Not Placed", "Placed"]) -> go.Figure:
    """Plots a confusion matrix heatmap."""
    z_text = [[str(val) for val in row] for row in cm]

    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=[f"Pred: {l}" for l in labels],
        y=[f"Actual: {l}" for l in labels],
        text=z_text,
        texttemplate="%{text}",
        textfont={"size": 16, "color": "white"},
        colorscale="Blues",
        showscale=False
    ))

    fig.update_layout(
        title="<b>Evaluation Confusion Matrix (Holdout Test Set)</b>",
        title_font=dict(size=15, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=TEXT_COLOR),
        height=320,
        margin=dict(l=40, r=20, t=50, b=30)
    )
    return fig

def roc_curve_chart(fpr: np.ndarray, tpr: np.ndarray, auc_score: float) -> go.Figure:
    """Plots the ROC Curve."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=fpr,
        y=tpr,
        mode='lines',
        name=f"Logistic Regression (AUC = {auc_score:.4f})",
        line=dict(color="#10b981", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        name="Random Classifier (AUC = 0.50)",
        line=dict(color="#94a3b8", dash='dash')
    ))

    fig.update_layout(
        title="<b>Receiver Operating Characteristic (ROC Curve)</b>",
        title_font=dict(size=15, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
        xaxis=dict(title="False Positive Rate", gridcolor=GRID_COLOR),
        yaxis=dict(title="True Positive Rate", gridcolor=GRID_COLOR),
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=TEXT_COLOR),
        height=320,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(x=0.4, y=0.1)
    )
    return fig

def gap_analysis_chart(gaps: List[Dict[str, Any]]) -> go.Figure:
    """
    Creates a grouped bar chart displaying Current Value vs Optimal Target Value
    for student improvement gap analysis.
    """
    labels = [g["label"] for g in gaps if g["feature"] != "sleep_hours"]
    current_vals = [g["current"] for g in gaps if g["feature"] != "sleep_hours"]
    target_vals = [g["target"] for g in gaps if g["feature"] != "sleep_hours"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Current Standing",
        y=labels,
        x=current_vals,
        orientation='h',
        marker=dict(color="#f59e0b", line=dict(color="rgba(255,255,255,0.2)", width=1)),
        text=[f"{v:.1f}" for v in current_vals],
        textposition="inside",
        textfont=dict(color="#ffffff", size=11)
    ))

    fig.add_trace(go.Bar(
        name="Placement Target Benchmark",
        y=labels,
        x=target_vals,
        orientation='h',
        marker=dict(color="#10b981", line=dict(color="rgba(255,255,255,0.2)", width=1)),
        text=[f"{v:.1f}" for v in target_vals],
        textposition="inside",
        textfont=dict(color="#ffffff", size=11)
    ))

    fig.update_layout(
        barmode='group',
        title="<b>Metric-by-Metric Current Standing vs Required Target</b>",
        title_font=dict(size=15, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=TEXT_COLOR),
        height=320,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(title="Score / Hours / Count", gridcolor=GRID_COLOR),
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    return fig

def improvement_trajectory_radar(
    current_features: Dict[str, float],
    target_features: Dict[str, float]
) -> go.Figure:
    """
    Creates an overlay radar chart showing where the student's current profile is pinched
    and what the target perimeter looks like.
    """
    categories = ["Study Hours", "Attendance", "Assignments", "Exam Score", "Previous Score"]
    
    scales = {
        "Study Hours": 12.0,
        "Attendance": 100.0,
        "Assignments": 20.0,
        "Exam Score": 100.0,
        "Previous Score": 100.0
    }

    norm_current = []
    norm_target = []

    for cat in categories:
        max_s = scales[cat]
        c_val = current_features.get(cat.lower().replace(" ", "_"), 0.0)
        t_val = target_features.get(cat.lower().replace(" ", "_"), 0.0)
        norm_current.append(min(100.0, (c_val / max_s) * 100.0))
        norm_target.append(min(100.0, (t_val / max_s) * 100.0))

    # Close loop
    p_cats = categories + [categories[0]]
    p_curr = norm_current + [norm_current[0]]
    p_targ = norm_target + [norm_target[0]]

    fig = go.Figure()

    # Target polygon (Green)
    fig.add_trace(go.Scatterpolar(
        r=p_targ,
        theta=p_cats,
        fill='toself',
        fillcolor='rgba(16, 185, 129, 0.25)',
        line=dict(color="#10b981", width=2.5),
        name="Target Roadmap Profile"
    ))

    # Current polygon (Amber/Red)
    fig.add_trace(go.Scatterpolar(
        r=p_curr,
        theta=p_cats,
        fill='toself',
        fillcolor='rgba(239, 68, 68, 0.35)',
        line=dict(color="#ef4444", width=2.5),
        name="Current Standing (Now)"
    ))

    fig.update_layout(
        title="<b>Multi-Axial Gap Analysis (Current vs Target Perimeter)</b>",
        title_font=dict(size=15, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
        polar=dict(
            bgcolor="rgba(241, 245, 249, 0.7)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                linecolor=GRID_COLOR,
                gridcolor=GRID_COLOR
            ),
            angularaxis=dict(
                linecolor=GRID_COLOR,
                gridcolor=GRID_COLOR,
                tickfont=dict(color=TEXT_COLOR, size=11)
            )
        ),
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=TEXT_COLOR),
        height=360,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    return fig