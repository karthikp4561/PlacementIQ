import streamlit as st
import pandas as pd
import numpy as np
import base64
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, roc_auc_score
)

def get_asset_base64(filename: str) -> str:
    p = Path("assets") / filename
    if p.exists():
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

import config
from utils.style import load_css, render_hero, render_kpi, render_footer
from utils.database import (
    init_db, authenticate_user, create_user, save_prediction,
    get_user_predictions, delete_prediction, clear_user_predictions,
    get_admin_system_metrics, list_all_users, update_user_role, delete_user,
    reset_user_password, get_all_predictions_detailed
)
from utils.auth import (
    init_session_state, get_current_user, is_authenticated,
    is_admin, login, logout
)
from utils.prediction import predict_placement, get_model_and_scaler
from utils.recommendations import generate_recommendations, compute_target_profile
from utils.report import generate_pdf_report
from utils.charts import (
    probability_gauge, feature_attribution_bar, radar_chart,
    feature_chart, confusion_matrix_heatmap, roc_curve_chart,
    gap_analysis_chart, improvement_trajectory_radar
)

# -------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title=f"{config.APP_TITLE} | Intelligent Placement Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize DB & Session State
init_db()
init_session_state()
load_css(is_logged_in=is_authenticated())

current_user = get_current_user()

# =============================================================
# SCENARIO A: GUEST USER -> CLEAN SKILLBOOST-INSPIRED LOGIN GATEWAY
# =============================================================
if not is_authenticated() or not current_user:
    # High-End SaaS Split-Screen Layout matching User Specification
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    isometric_b64 = get_asset_base64("isometric_student_ai.jpg")

    col_brand, col_space, col_auth = st.columns([1.0, 0.14, 1.08])

    # Left Panel (Branding - Glassmorphism Style)
    with col_brand:
        left_brand_html = f"""<div class="glass-brand-panel">
<div>
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 22px;">
<div style="background: linear-gradient(135deg, #f97316 0%, #ec4899 50%, #3b82f6 100%); width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 4px 14px rgba(249,115,22,0.4);">🎓</div>
<div style="font-size: 25px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff;">PlacementIQ</div>
</div>
<div style="font-size: 32px; font-weight: 800; line-height: 1.22; margin-bottom: 14px; letter-spacing: -0.6px; color: #ffffff;">
Unlock Your Placement Potential
</div>
<div style="font-size: 13.5px; line-height: 1.6; color: #cbd5e1; margin-bottom: 24px;">
Sign in to evaluate campus placement readiness, uncover feature sensitivities through Explainable AI, and track personalized improvement pathways.
</div>
<div style="display: flex; flex-direction: column; gap: 13px; margin-bottom: 20px;">
<div style="display: flex; align-items: center; gap: 12px; font-size: 13.5px; color: #f1f5f9; font-weight: 500;">
<span style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; border: 1px solid rgba(56, 189, 248, 0.45); flex-shrink: 0;">✓</span>
<span>99.70% Verified Holdout Model Accuracy</span>
</div>
<div style="display: flex; align-items: center; gap: 12px; font-size: 13.5px; color: #f1f5f9; font-weight: 500;">
<span style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; border: 1px solid rgba(56, 189, 248, 0.45); flex-shrink: 0;">✓</span>
<span>Multi-Axial Radar & Gap Remediation</span>
</div>
<div style="display: flex; align-items: center; gap: 12px; font-size: 13.5px; color: #f1f5f9; font-weight: 500;">
<span style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; border: 1px solid rgba(56, 189, 248, 0.45); flex-shrink: 0;">✓</span>
<span>Certified ReportLab Dossier Downloads</span>
</div>
</div>
</div>
<div style="display: flex; justify-content: flex-end; margin-top: 6px; margin-bottom: 14px;">
<img src="data:image/jpeg;base64,{isometric_b64}" style="width: 220px; max-height: 160px; object-fit: cover; border-radius: 16px; box-shadow: 0 16px 36px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2);" alt="PlacementIQ 3D Tech Analytics" />
</div>
<div style="display: flex; gap: 10px; align-items: center;">
<span style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16); border-radius: 20px; font-size: 11px; font-weight: 600; padding: 5px 14px; color: #cbd5e1; backdrop-filter: blur(4px);">MCA Academic Research</span>
<span style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16); border-radius: 20px; font-size: 11px; font-weight: 600; padding: 5px 14px; color: #cbd5e1; backdrop-filter: blur(4px);">Secure PBKDF2</span>
</div>
</div>"""
        st.markdown(left_brand_html, unsafe_allow_html=True)

    # Right Panel (Form - Clean Light Theme)
    with col_auth:
        with st.container(border=True):
            st.markdown("""<div style="margin-bottom: 16px;">
<div style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 4px; letter-spacing: -0.5px;">Welcome 👋</div>
<div style="color: #64748b; font-size: 13.5px;">Sign in to access your student or administrator workspace</div>
</div>""", unsafe_allow_html=True)

            # Top Actions: Segmented Toggle Switch + SSO Outline Buttons
            c_tog, c_sso = st.columns([1.1, 1.3], gap="small")
            with c_tog:
                auth_mode = st.segmented_control(
                    "Mode",
                    options=["Sign In", "Create Account"],
                    default="Create Account" if st.session_state.get("auth_mode") == "Create Account" else "Sign In",
                    label_visibility="collapsed",
                    key="auth_seg_control"
                )
                st.session_state["auth_mode"] = auth_mode

            with c_sso:
                s1, s2 = st.columns(2, gap="small")
                with s1:
                    if st.button("🌐 Continue with Google", use_container_width=True, key="sso_goog", type="secondary"):
                        st.info("Campus Federated SSO: Please use your university credentials below.")
                with s2:
                    if st.button("🪟 Continue with Microsoft", use_container_width=True, key="sso_msft", type="secondary"):
                        st.info("Campus Azure AD SSO: Please use your university credentials below.")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            if auth_mode == "Create Account":
                with st.form("clean_student_reg"):
                    r_name = st.text_input("Full Name", placeholder="👤  e.g. John Doe", key="reg_name")
                    r_user = st.text_input("Username", placeholder="👤  e.g. johndoe", key="reg_user")
                    r_email = st.text_input("Academic Email", placeholder="✉️  e.g. john@college.edu", key="reg_email")
                    r_pass = st.text_input("Password (min 6 characters)", type="password", placeholder="🔒  Create a strong password", key="reg_pass")
                    r_submit = st.form_submit_button("Create Student Account →", use_container_width=True, type="primary")

                    if r_submit:
                        ok, msg = create_user(r_user, r_email, r_name, r_pass, role="student")
                        if ok:
                            st.success("Account created successfully! Switching to Sign In...")
                            st.session_state["auth_mode"] = "Sign In"
                            st.rerun()
                        else:
                            st.error(msg)

                st.markdown('<div class="switch-auth-link">', unsafe_allow_html=True)
                if st.button("Already have an account? Sign In", key="btn_switch_to_signin", use_container_width=True, type="tertiary"):
                    st.session_state["auth_mode"] = "Sign In"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            else:
                with st.form("common_login_form"):
                    s_user = st.text_input("Username or Email", placeholder="👤  Enter your username or academic email", key="login_user")
                    s_pass = st.text_input("Password", type="password", placeholder="🔒  Enter your password", key="login_pass")
                    s_submit = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

                    if s_submit:
                        u = authenticate_user(s_user, s_pass)
                        if u:
                            login(u)
                            if u.get("role") == "admin":
                                st.session_state["admin_nav"] = "🛡️ Admin Command Center"
                            else:
                                st.session_state["student_nav"] = "🎯 Placement Assessment"
                            st.rerun()
                        else:
                            st.error("Invalid username or password. Please verify your credentials.")

                st.markdown('<div class="switch-auth-link">', unsafe_allow_html=True)
                if st.button("Don't have an account? Create Account", key="btn_switch_to_create", use_container_width=True, type="tertiary"):
                    st.session_state["auth_mode"] = "Create Account"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    render_footer()
    st.stop()


# =============================================================
# SCENARIO B: AUTHENTICATED USER SESSIONS
# =============================================================

# Sidebar Profile Header
with st.sidebar:
    st.markdown(f"""
    <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 20px; padding: 10px 0;'>
        <div style='background: linear-gradient(135deg, #2563eb, #38bdf8); width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 4px 12px rgba(37,99,235,0.4);'>
            🎓
        </div>
        <div>
            <div style='font-size: 20px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;'>PlacementIQ</div>
            <div style='font-size: 11px; color: #94a3b8; font-weight: 500;'>v{config.VERSION} &bull; MCA Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    role_badge = "badge-admin-clean" if current_user.get("role") == "admin" else "badge-student-clean"
    st.markdown(f"""
    <div style='background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 16px; margin-bottom: 18px;'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;'>
            <div style='font-weight: 700; color: #ffffff; font-size: 14px;'>{current_user.get("full_name")}</div>
            <span class='{role_badge}'>{current_user.get("role")}</span>
        </div>
        <div style='color: #94a3b8; font-size: 11px;'>@{current_user.get("username")} &bull; {current_user.get("email")}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Sign Out", use_container_width=True, key="btn_logout_active"):
        logout()
        st.rerun()

    st.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 15px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='color: #94a3b8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>Navigation Menu</div>", unsafe_allow_html=True)


# =============================================================
# WORKSPACE 1: STUDENT (Inspired by Reference 4 - Student Portal)
# =============================================================
if current_user.get("role") == "student":
    student_nav_options = [
        "🎯 Placement Assessment",
        "📈 Gap Analysis & Roadmap",
        "📜 My History & Reports",
        "📊 Cohort Analytics"
    ]

    curr_student_nav = st.session_state.get("student_nav")
    student_index = student_nav_options.index(curr_student_nav) if curr_student_nav in student_nav_options else 0

    selected_student_nav = st.sidebar.radio(
        "Student Menu",
        student_nav_options,
        index=student_index,
        label_visibility="collapsed"
    )
    st.session_state["student_nav"] = selected_student_nav

    # --- STUDENT TAB 1: PLACEMENT ASSESSMENT ---
    if selected_student_nav == "🎯 Placement Assessment":
        # Reference 4 Style Welcome Banner
        render_hero(
            title=f"Welcome back, {current_user['full_name']}! 👋",
            subtitle="Always stay updated in your student placement portal. Enter your academic parameters below to evaluate placement probability and discover actionable pathways.",
            badge="Student Placement Console"
        )

        col_inputs, col_outcome = st.columns([1.1, 0.9])

        with col_inputs:
            with st.container(border=True):
                st.markdown("""
                <div style='font-size: 17px; font-weight: 700; color: #0f172a; margin-bottom: 4px;'>📝 Candidate Academic & Behavioral Parameters</div>
                <div style='color: #64748b; font-size: 13px; margin-bottom: 18px;'>Provide your current semester metrics. The model evaluates your profile against 10,000 historical placement records.</div>
                """, unsafe_allow_html=True)

                with st.form("form_student_predict"):
                    f1, f2 = st.columns(2)
                    with f1:
                        study_hours = st.number_input("📚 Daily Study Hours", 0, 24, 6, 1)
                        attendance = st.number_input("📅 College Attendance (%)", 0, 100, 75, 1)
                        sleep_hours = st.number_input("😴 Sleep Hours (per night)", 0, 16, 7, 1)
                        internet_usage = st.number_input("🌐 Internet Usage (hrs/day)", 0, 24, 5, 1)
                    with f2:
                        assignments_completed = st.number_input("📄 Assignments Completed", 0, 50, 10, 1)
                        previous_score = st.number_input("📈 Previous Academic Score (%)", 0, 100, 65, 1)
                        exam_score = st.number_input("🏆 Examination Score (%)", 0.0, 100.0, 75.0, 0.5)

                    btn_run = st.form_submit_button("🚀 Evaluate Placement Likelihood", use_container_width=True)

        if btn_run:
            student_inputs = {
                "study_hours": study_hours,
                "attendance": attendance,
                "sleep_hours": sleep_hours,
                "internet_usage": internet_usage,
                "assignments_completed": assignments_completed,
                "previous_score": previous_score,
                "exam_score": exam_score
            }

            try:
                res = predict_placement(student_inputs)
                recs = generate_recommendations(student_inputs, res["prediction_result"], res["placement_probability"])
                targets = compute_target_profile(student_inputs)

                st.session_state["cur_res"] = res
                st.session_state["cur_recs"] = recs
                st.session_state["cur_targets"] = targets

                save_prediction(
                    user_id=current_user["id"],
                    inputs=student_inputs,
                    prediction_result=res["prediction_result"],
                    placement_probability=res["placement_probability"],
                    confidence=res["confidence"],
                    risk_level=res["risk_level"]
                )
            except Exception as e:
                st.error(f"Inference error: {e}")

        cur_res = st.session_state.get("cur_res")
        cur_recs = st.session_state.get("cur_recs")
        cur_targets = st.session_state.get("cur_targets")

        with col_outcome:
            with st.container(border=True):
                if cur_res:
                    prob = cur_res["placement_probability"]
                    conf = cur_res["confidence"]
                    risk = cur_res["risk_level"]
                    is_placed = cur_res["is_placed"]

                    if is_placed:
                        st.markdown("""
                        <div class='result-banner-placed-clean'>
                            <div style='font-size: 24px; font-weight: 800; color: #16a34a; margin-bottom: 4px;'>✅ CANDIDATE IS LIKELY PLACED</div>
                            <div style='color: #475569; font-size: 13px;'>Your academic profile meets the benchmark for campus recruitment.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class='result-banner-notplaced-clean'>
                            <div style='font-size: 24px; font-weight: 800; color: #dc2626; margin-bottom: 4px;'>❌ NOT LIKELY TO BE PLACED</div>
                            <div style='color: #475569; font-size: 13px;'>Academic indicators identify placement risk. Review the split gap analysis below to achieve placement!</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Fasto Style KPI indicators
                    k1, k2, k3 = st.columns(3)
                    render_kpi(k1, "Probability", f"{prob:.1f}%", "Calculated by LogReg", "🎯", "#2563eb")
                    render_kpi(k2, "Confidence", f"{conf:.1f}%", "Model certainty", "🔍", "#0891b2")
                    render_kpi(k3, "Risk Level", risk, "Statistical tier", "⚖️", "#16a34a" if is_placed else "#dc2626")

                    st.plotly_chart(probability_gauge(prob), use_container_width=True)

                    try:
                        pdf_bytes = generate_pdf_report(current_user, cur_res, cur_recs)
                        st.download_button(
                            label="📥 Download Certified PDF Placement Report",
                            data=pdf_bytes,
                            file_name=f"PlacementIQ_Report_{current_user['username']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as err:
                        st.caption(f"PDF notice: {err}")
                else:
                    st.markdown("""
                    <div style='text-align: center; padding: 60px 20px;'>
                        <div style='font-size: 42px; margin-bottom: 12px;'>📊</div>
                        <div style='font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 6px;'>Awaiting Your Values</div>
                        <div style='color: #64748b; font-size: 13px; max-width: 320px; margin: 0 auto;'>
                            Fill out your academic parameters on the left and select 'Evaluate Placement Likelihood'.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # GAP ANALYSIS & HOW TO IMPROVE (SPLIT GRAPHICAL REPRESENTATION)
        if cur_res and cur_targets:
            st.markdown("<hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;'>", unsafe_allow_html=True)

            prob = cur_res["placement_probability"]

            if prob < 60.0:
                st.markdown("""
                <div style='background: #fffbeb; border: 1px solid #fde68a; border-radius: 16px; padding: 22px 26px; margin-bottom: 25px;'>
                    <div style='font-size: 18px; font-weight: 800; color: #b45309; margin-bottom: 6px;'>⚠️ Placement Remediation Roadmap</div>
                    <div style='color: #78350f; font-size: 13.5px; line-height: 1.6;'>
                        Your calculated probability (<b>{prob:.1f}%</b>) indicates high placement risk.
                        Below is a <b>full graphical split representation</b> comparing where you stand now versus the target parameters required to reach <b>>= 85% placement probability</b>.
                    </div>
                </div>
                """.format(prob=prob), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 16px; padding: 22px 26px; margin-bottom: 25px;'>
                    <div style='font-size: 18px; font-weight: 800; color: #15803d; margin-bottom: 6px;'>🌟 Performance Optimization Benchmarks</div>
                    <div style='color: #166534; font-size: 13.5px; line-height: 1.6;'>
                        Excellent performance (<b>{prob:.1f}%</b> probability). Review your split metrics below to sustain this standard.
                    </div>
                </div>
                """.format(prob=prob), unsafe_allow_html=True)

            # Two Clean White Cards for Charts
            col_radar_c, col_bar_c = st.columns(2)

            with col_radar_c:
                with st.container(border=True):
                    st.markdown("""
                    <div style='font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 4px;'>🕸️ Multi-Axial Perimeter (Current vs Target)</div>
                    <div style='color: #64748b; font-size: 13px; margin-bottom: 12px;'>Visualizing dimensional gaps across attendance, exam preparation, and study hours.</div>
                    """, unsafe_allow_html=True)
                    st.plotly_chart(
                        improvement_trajectory_radar(cur_res["inputs"], cur_targets["target_inputs"]),
                        use_container_width=True
                    )

            with col_bar_c:
                with st.container(border=True):
                    st.markdown("""
                    <div style='font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 4px;'>📊 Metric-by-Metric Current Standing vs Target</div>
                    <div style='color: #64748b; font-size: 13px; margin-bottom: 12px;'>Exact delta comparison showing required numerical increases for each academic dimension.</div>
                    """, unsafe_allow_html=True)
                    st.plotly_chart(
                        gap_analysis_chart(cur_targets["gaps"]),
                        use_container_width=True
                    )

            # Metric-by-Metric Shift Cards
            st.markdown("### 📋 Metric-by-Metric Actionable Breakdown")
            for gap in cur_targets["gaps"]:
                prio = gap["priority"]
                prio_bg = "#fef2f2" if prio == "Critical" else ("#fffbeb" if prio == "High" else "#f0fdf4")
                prio_border = "#fecaca" if prio == "Critical" else ("#fde68a" if prio == "High" else "#bbf7d0")
                prio_color = "#dc2626" if prio == "Critical" else ("#d97706" if prio == "High" else "#16a34a")
                delta_str = f"+{gap['delta']}" if gap['delta'] > 0 else (f"{gap['delta']}" if gap['delta'] < 0 else "0")

                st.markdown(f"""
                <div style='background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid {prio_color}; border-radius: 12px; padding: 16px 20px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='font-weight: 700; color: #0f172a; font-size: 15px;'>{gap["label"]}</div>
                        <span style='background: {prio_bg}; color: {prio_color}; border: 1px solid {prio_border}; padding: 2px 10px; border-radius: 20px; font-weight: 700; font-size: 11px;'>{prio.upper()}</span>
                    </div>
                    <div style='display: flex; gap: 24px; color: #64748b; font-size: 13px; margin: 8px 0;'>
                        <div>Current Standing: <b style='color: #0f172a;'>{gap['current']}{gap['unit']}</b></div>
                        <div>Placement Target: <b style='color: #16a34a;'>{gap['target']}{gap['unit']}</b></div>
                        <div>Required Shift: <b style='color: {prio_color};'>{delta_str}{gap['unit']}</b></div>
                    </div>
                    <div style='color: #334155; font-size: 13px;'>👉 <b>Action:</b> {gap["action"]}</div>
                </div>
                """, unsafe_allow_html=True)

            # Interactive Simulator
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("""
                <div style='font-size: 17px; font-weight: 700; color: #0f172a; margin-bottom: 4px;'>🎛️ Interactive 'What-If' Placement Improvement Simulator</div>
                <div style='color: #64748b; font-size: 13px; margin-bottom: 16px;'>Adjust the sliders below to simulate how closing performance gaps boosts your projected placement probability in real time.</div>
                """, unsafe_allow_html=True)

                sim_c1, sim_c2 = st.columns(2)
                with sim_c1:
                    sim_exam = st.slider("Target Exam Score (%)", 0.0, 100.0, float(cur_targets["target_inputs"]["exam_score"]), 0.5)
                    sim_att = st.slider("Target Attendance (%)", 0, 100, int(cur_targets["target_inputs"]["attendance"]), 1)
                with sim_c2:
                    sim_study = st.slider("Target Daily Study Hours", 0, 24, int(cur_targets["target_inputs"]["study_hours"]), 1)
                    sim_assign = st.slider("Target Assignments Completed", 0, 50, int(cur_targets["target_inputs"]["assignments_completed"]), 1)

                sim_in = {
                    "study_hours": sim_study, "attendance": sim_att,
                    "sleep_hours": cur_res["inputs"]["sleep_hours"],
                    "internet_usage": cur_res["inputs"]["internet_usage"],
                    "assignments_completed": sim_assign,
                    "previous_score": cur_res["inputs"]["previous_score"],
                    "exam_score": sim_exam
                }

                sim_pred = predict_placement(sim_in)
                sim_p = sim_pred["placement_probability"]
                sim_gain = sim_p - cur_res["placement_probability"]

                res1, res2, res3 = st.columns(3)
                with res1:
                    st.metric("Projected Probability", f"{sim_p:.1f}%", delta=f"{sim_gain:+.1f}%")
                with res2:
                    st.metric("Projected Outcome", sim_pred["prediction_result"])
                with res3:
                    st.metric("Projected Risk", sim_pred["risk_level"])

        render_footer()

    # --- STUDENT TAB 2: GAP ANALYSIS & ROADMAP ---
    elif selected_student_nav == "📈 Gap Analysis & Roadmap":
        render_hero(
            title="Placement Gap Analysis & Remediation",
            subtitle="Full graphical breakdown of your current academic standing contrasted against optimal placement benchmarks.",
            badge="Remediation Strategy"
        )

        cur_res = st.session_state.get("cur_res")
        cur_targets = st.session_state.get("cur_targets")

        if not cur_res or not cur_targets:
            st.info("💡 You have not executed a prediction yet. Please complete your assessment in '🎯 Placement Assessment' to generate your customized roadmap.")
        else:
            c_r, c_b = st.columns(2)
            with c_r:
                st.plotly_chart(
                    improvement_trajectory_radar(cur_res["inputs"], cur_targets["target_inputs"]),
                    use_container_width=True
                )
            with c_b:
                st.plotly_chart(
                    gap_analysis_chart(cur_targets["gaps"]),
                    use_container_width=True
                )

        render_footer()

    # --- STUDENT TAB 3: MY HISTORY & REPORTS ---
    elif selected_student_nav == "📜 My History & Reports":
        render_hero(
            title="My Historical Assessments & Reports",
            subtitle="Audit your semester-over-semester progress and re-download certified PDF dossiers.",
            badge="Audit History"
        )

        user_preds = get_user_predictions(current_user["id"])
        if not user_preds:
            st.info("No recorded predictions found. Run an evaluation to log your first assessment.")
        else:
            col_t, col_b = st.columns([3, 1])
            with col_t:
                st.write(f"Showing **{len(user_preds)}** logged assessment(s) for **{current_user['full_name']}**")
            with col_b:
                if st.button("🗑️ Clear My History"):
                    clear_user_predictions(current_user["id"])
                    st.success("History cleared.")
                    st.rerun()

            df_h = pd.DataFrame([{
                "ID": p["id"],
                "Date": p["timestamp"],
                "Outcome": p["prediction_result"],
                "Probability": f"{p['placement_probability']:.1f}%",
                "Confidence": f"{p['confidence']:.1f}%",
                "Risk": p["risk_level"],
                "Attendance": f"{p['attendance']:.0f}%",
                "Exam Score": f"{p['exam_score']:.1f}%"
            } for p in user_preds])

            st.dataframe(df_h, use_container_width=True, hide_index=True)

            selected_pid = st.selectbox("Select Record ID to Download PDF:", [p["id"] for p in user_preds])
            p_rec = next((p for p in user_preds if p["id"] == selected_pid), None)

            if p_rec:
                rec_inputs = {
                    "study_hours": p_rec["study_hours"],
                    "attendance": p_rec["attendance"],
                    "sleep_hours": p_rec["sleep_hours"],
                    "internet_usage": p_rec["internet_usage"],
                    "assignments_completed": p_rec["assignments_completed"],
                    "previous_score": p_rec["previous_score"],
                    "exam_score": p_rec["exam_score"]
                }
                try:
                    p_res = predict_placement(rec_inputs)
                    p_recs = generate_recommendations(rec_inputs, p_rec["prediction_result"], p_rec["placement_probability"])
                    pdf_bytes = generate_pdf_report(current_user, p_res, p_recs)
                    st.download_button(
                        label=f"📥 Download PDF Dossier for Record #{selected_pid}",
                        data=pdf_bytes,
                        file_name=f"PlacementIQ_Report_{current_user['username']}_rec{selected_pid}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Report generation error: {e}")

        render_footer()

    # --- STUDENT TAB 4: COHORT ANALYTICS ---
    elif selected_student_nav == "📊 Cohort Analytics":
        render_hero(
            title="Cohort Dataset Benchmarks",
            subtitle="Explore how your academic standing benchmarks against the 10,000-student historical training corpus.",
            badge="Benchmark Intelligence"
        )
        try:
            df_cohort = pd.read_csv(config.get_dataset_path())
            c1, c2 = st.columns(2)
            with c1:
                import plotly.express as px
                fig_exam = px.histogram(
                    df_cohort, x="exam_score", color="placement_status", barmode="overlay",
                    color_discrete_map={"Placed": "#10b981", "Not Placed": "#ef4444"},
                    title="<b>Exam Score Distribution</b>"
                )
                fig_exam.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", font=dict(color="#0f172a"))
                st.plotly_chart(fig_exam, use_container_width=True)
            with c2:
                fig_att = px.box(
                    df_cohort, x="placement_status", y="attendance", color="placement_status",
                    color_discrete_map={"Placed": "#10b981", "Not Placed": "#ef4444"},
                    title="<b>Attendance Percentage by Placement Outcome</b>"
                )
                fig_att.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", font=dict(color="#0f172a"), showlegend=False)
                st.plotly_chart(fig_att, use_container_width=True)
        except Exception as err:
            st.error(f"Cohort data error: {err}")
        render_footer()




# =============================================================
# WORKSPACE 2: ADMINISTRATOR (Inspired by Reference 3 - Fasto)
# =============================================================
elif current_user.get("role") == "admin":
    admin_nav_options = [
        "🛡️ Admin Command Center",
        "👥 User Account Management",
        "📜 Student Activity & Audit Inspector",
        "🧠 Model Diagnostics & Test Evaluation",
        "🎯 Prediction Test Simulator",
        "📊 Cohort Analytics",
        "ℹ️ System Specifications"
    ]

    curr_admin_nav = st.session_state.get("admin_nav")
    admin_index = admin_nav_options.index(curr_admin_nav) if curr_admin_nav in admin_nav_options else 0

    selected_admin_nav = st.sidebar.radio(
        "Admin Menu",
        admin_nav_options,
        index=admin_index,
        label_visibility="collapsed"
    )
    st.session_state["admin_nav"] = selected_admin_nav

    # --- ADMIN TAB 1: COMMAND CENTER ---
    if selected_admin_nav == "🛡️ Admin Command Center":
        # Fasto Style Header & KPI Cards
        render_hero(
            title="Administrator Command Center",
            subtitle="Fasto SaaS-style administrative control center &bull; Monitor institutional placement telemetry, manage student accounts, and inspect live assessment logs.",
            badge="Executive Oversight"
        )

        metrics = get_admin_system_metrics()

        # Fasto-style white KPI cards with colored top bars
        a1, a2, a3, a4 = st.columns(4)
        render_kpi(a1, "Total Users", f"{metrics['total_users']}", f"{metrics['total_students']} Students / {metrics['total_admins']} Admins", "👥", "#2563eb")
        render_kpi(a2, "Global Predictions", f"{metrics['total_predictions']}", f"{metrics['placed_predictions']} Placed outcomes", "📈", "#0891b2")
        render_kpi(a3, "Placement Rate", f"{metrics['placement_rate']:.1f}%", "Cohort average across logs", "🎯", "#16a34a")
        render_kpi(a4, "DB Engine", "SQLite3", "data/placementiq.db", "💾", "#7c3aed")

        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

        col_act, col_alert = st.columns([2, 1])

        with col_act:
            st.markdown("""
            <div class='white-card'>
                <div class='white-card-title'>🕒 Recent Student Assessment Submissions</div>
                <div class='white-card-desc'>Live activity feed of candidate submissions recorded across the platform.</div>
            """, unsafe_allow_html=True)
            recent = metrics.get("recent_activity", [])
            if recent:
                df_rec = pd.DataFrame([{
                    "Student": r["full_name"],
                    "Username": r["username"],
                    "Time": r["timestamp"],
                    "Outcome": r["prediction_result"],
                    "Probability": f"{r['placement_probability']:.1f}%",
                    "Risk": r["risk_level"]
                } for r in recent[:15]])
                st.dataframe(df_rec, use_container_width=True, hide_index=True)
            else:
                st.info("No prediction activity recorded yet.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_alert:
            st.markdown("""
            <div class='white-card'>
                <div class='white-card-title'>🚨 At-Risk Student Alert</div>
                <div class='white-card-desc'>Candidates whose placement probability is below 50.0% requiring immediate intervention.</div>
            """, unsafe_allow_html=True)
            at_risk = [r for r in recent if r.get("placement_probability", 100) < 50.0]
            if at_risk:
                st.markdown(f"""
                <div style='background: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; padding: 14px; margin-bottom: 12px;'>
                    <div style='color: #dc2626; font-weight: 700; font-size: 14px;'>⚠️ {len(at_risk)} Student(s) Below 50% Probability</div>
                    <div style='color: #7f1d1d; font-size: 12px; margin-top: 4px;'>Recommend scheduling remedial technical practice and counseling.</div>
                </div>
                """, unsafe_allow_html=True)
                for ar in at_risk[:5]:
                    st.caption(f"&bull; **{ar['full_name']}** (@{ar['username']}): Prob {ar['placement_probability']:.1f}% ({ar['risk_level']})")
            else:
                st.markdown("""
                <div style='background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 14px;'>
                    <div style='color: #16a34a; font-weight: 700; font-size: 13px;'>✅ No High-Risk Candidates in Recent Feed</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        render_footer()

    # --- ADMIN TAB 2: USER ACCOUNT MANAGEMENT ---
    elif selected_admin_nav == "👥 User Account Management":
        render_hero(
            title="User Account Management",
            subtitle="Provision new users, inspect profiles, update roles (promote/demote), reset passwords, and manage accounts.",
            badge="User Governance"
        )

        all_users = list_all_users()

        col_search, col_filter = st.columns([2, 1])
        with col_search:
            u_search = st.text_input("🔍 Search Users (Name, Username, Email):")
        with col_filter:
            role_filter = st.selectbox("Filter by Role:", ["All", "student", "admin"])

        filtered_users = all_users
        if u_search:
            s = u_search.strip().lower()
            filtered_users = [u for u in filtered_users if s in u["username"].lower() or s in u["full_name"].lower() or s in u["email"].lower()]
        if role_filter != "All":
            filtered_users = [u for u in filtered_users if u["role"] == role_filter]

        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(filtered_users), use_container_width=True, hide_index=True)
        st.write(f"Displaying **{len(filtered_users)}** of **{len(all_users)}** total user accounts.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        t_add, t_role, t_pw, t_del = st.tabs([
            "➕ Add New User",
            "🔄 Change Role",
            "🔑 Reset Password",
            "🗑️ Delete Account"
        ])

        with t_add:
            st.markdown("#### Create Account")
            with st.form("form_admin_add_user"):
                n_name = st.text_input("Full Name")
                n_user = st.text_input("Username")
                n_email = st.text_input("Email")
                n_pass = st.text_input("Password", type="password")
                n_role = st.selectbox("Role", ["student", "admin"])
                n_sub = st.form_submit_button("Create Account")

                if n_sub:
                    ok, msg = create_user(n_user, n_email, n_name, n_pass, role=n_role)
                    if ok:
                        st.success(f"User '{n_user}' created successfully.")
                        st.rerun()
                    else:
                        st.error(msg)

        with t_role:
            st.markdown("#### Modify User Role")
            target_uid = st.selectbox("Select User ID to Update:", [u["id"] for u in all_users], key="sel_role_uid")
            new_r = st.selectbox("Assign Role:", ["student", "admin"], key="sel_new_r")
            if st.button("Update Role", use_container_width=True):
                if target_uid == current_user["id"] and new_r != "admin":
                    st.error("Safety guard: You cannot demote your own active administrator account.")
                else:
                    update_user_role(target_uid, new_r)
                    st.success(f"User #{target_uid} updated to '{new_r}'.")
                    st.rerun()

        with t_pw:
            st.markdown("#### Reset User Password")
            pw_uid = st.selectbox("Select User ID to Reset:", [u["id"] for u in all_users], key="sel_pw_uid")
            new_pw = st.text_input("New Password (min 6 characters):", type="password", key="inp_new_pw")
            if st.button("Reset Password", use_container_width=True):
                ok, msg = reset_user_password(pw_uid, new_pw)
                if ok:
                    st.success(f"Password for User #{pw_uid} reset successfully.")
                else:
                    st.error(msg)

        with t_del:
            st.markdown("#### Delete User Account")
            del_uid = st.selectbox("Select User ID to Delete:", [u["id"] for u in all_users], key="sel_del_uid")
            st.warning("⚠️ Deleting a user will permanently remove the account and cascade all associated predictions.")
            if st.button("Confirm Account Deletion", use_container_width=True):
                if del_uid == current_user["id"]:
                    st.error("Safety guard: You cannot delete your own active administrator account.")
                else:
                    delete_user(del_uid)
                    st.success(f"User #{del_uid} deleted.")
                    st.rerun()

        render_footer()

    # --- ADMIN TAB 3: STUDENT ACTIVITY & AUDIT INSPECTOR ---
    elif selected_admin_nav == "📜 Student Activity & Audit Inspector":
        render_hero(
            title="Student Activity & Prediction Inspector",
            subtitle="Inspect all student submissions, filter by outcome or risk levels, identify at-risk students, and export audit trails to CSV.",
            badge="Audit Trail"
        )

        f1, f2, f3 = st.columns(3)
        with f1:
            sel_outcome = st.selectbox("Filter Outcome:", ["All", "Placed", "Not Placed"])
        with f2:
            sel_risk = st.selectbox("Filter Risk:", ["All", "High Risk", "Medium Risk", "Low Risk", "Very Low Risk"])
        with f3:
            search_txt = st.text_input("Search Student Name / Username:")

        detailed = get_all_predictions_detailed(outcome=sel_outcome, risk=sel_risk, search=search_txt)

        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        st.write(f"Displaying **{len(detailed)}** prediction audit records:")
        if detailed:
            df_det = pd.DataFrame(detailed)
            st.dataframe(df_det, use_container_width=True, hide_index=True)
            csv_data = df_det.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Filtered Audit Trail to CSV",
                data=csv_data,
                file_name=f"PlacementIQ_Audit_Trail_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No prediction records match the selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)

        render_footer()

    # --- ADMIN TAB 4: MODEL DIAGNOSTICS & EVALUATION ---
    elif selected_admin_nav == "🧠 Model Diagnostics & Test Evaluation":
        render_hero(
            title="Model Diagnostics & Statistical Verification",
            subtitle="Evaluation metrics calculated on a 20% holdout test partition (2,000 cases) from the verified 10,000-record dataset.",
            badge="Model Integrity"
        )

        try:
            model, scaler = get_model_and_scaler()
            df = pd.read_csv(config.get_dataset_path())

            X = df[config.FEATURE_NAMES]
            y = df["placement_status"]

            X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
            X_te_scaled = pd.DataFrame(scaler.transform(X_te), columns=config.FEATURE_NAMES)
            y_pred = model.predict(X_te_scaled)
            y_proba = model.predict_proba(X_te_scaled)[:, 1]

            acc = accuracy_score(y_te, y_pred)
            prec = precision_score(y_te, y_pred, pos_label="Placed")
            rec = recall_score(y_te, y_pred, pos_label="Placed")
            f1 = f1_score(y_te, y_pred, pos_label="Placed")
            cm = confusion_matrix(y_te, y_pred, labels=["Not Placed", "Placed"])
            y_bin = (y_te == "Placed").astype(int)
            fpr, tpr, _ = roc_curve(y_bin, y_proba)
            auc_val = roc_auc_score(y_bin, y_proba)

            e1, e2, e3, e4 = st.columns(4)
            render_kpi(e1, "Holdout Accuracy", f"{acc*100:.2f}%", "2,000 holdout cases", "🎯", "#2563eb")
            render_kpi(e2, "Precision", f"{prec*100:.2f}%", "True Positive / Predicted", "🔍", "#0891b2")
            render_kpi(e3, "Recall / Sensitivity", f"{rec*100:.2f}%", "Captured Placed Candidates", "⚡", "#16a34a")
            render_kpi(e4, "F1-Score", f"{f1*100:.2f}%", "Harmonic Mean", "⚖️", "#7c3aed")

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

            c_cm, c_roc = st.columns(2)
            with c_cm:
                st.markdown("<div class='white-card'>", unsafe_allow_html=True)
                st.plotly_chart(confusion_matrix_heatmap(cm, labels=["Not Placed", "Placed"]), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with c_roc:
                st.markdown("<div class='white-card'>", unsafe_allow_html=True)
                st.plotly_chart(roc_curve_chart(fpr, tpr, auc_val), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div class='white-card'>
                <div class='white-card-title'>📐 Feature Coefficients & Sensitivity Weights</div>
                <div class='white-card-desc'>Standardized logistic regression coefficients indicating directional influence on placement likelihood.</div>
            """, unsafe_allow_html=True)
            coef_df = pd.DataFrame([{
                "Feature": config.FEATURE_LABELS.get(f, f),
                "Coefficient (β)": f"{c:+.4f}",
                "Mean": f"{m:.2f}",
                "Scale (Std Dev)": f"{s:.2f}",
                "Impact Direction": "Dominant Driver" if c > 1.0 else ("Positive Contributor" if c > 0 else "Inverse Risk Factor")
            } for f, c, m, s in zip(config.FEATURE_NAMES, model.coef_[0], scaler.mean_, scaler.scale_)])
            st.dataframe(coef_df, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as err:
            st.error(f"Diagnostics error: {err}")

        render_footer()

    # --- ADMIN TAB 5: PREDICTION TEST SIMULATOR ---
    elif selected_admin_nav == "🎯 Prediction Test Simulator":
        render_hero(
            title="Administrator Test Simulator",
            subtitle="Simulate candidate profiles and test edge-case inputs against the machine learning inference engine.",
            badge="Test Bench"
        )

        col_t1, col_t2 = st.columns([1.1, 0.9])
        with col_t1:
            st.markdown("<div class='white-card'>", unsafe_allow_html=True)
            st.markdown("### Input Simulation Parameters")
            with st.form("admin_test_bench_form"):
                sc1, sc2 = st.columns(2)
                with sc1:
                    t_study = st.number_input("Study Hours", 0, 24, 6)
                    t_att = st.number_input("Attendance (%)", 0, 100, 75)
                    t_sleep = st.number_input("Sleep Hours", 0, 16, 7)
                    t_net = st.number_input("Internet Usage", 0, 24, 5)
                with sc2:
                    t_assign = st.number_input("Assignments", 0, 50, 10)
                    t_prev = st.number_input("Previous Score", 0, 100, 65)
                    t_exam = st.number_input("Exam Score", 0.0, 100.0, 75.0, 0.5)

                t_run = st.form_submit_button("Run Test Simulation", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_t2:
            if t_run:
                t_inputs = {
                    "study_hours": t_study, "attendance": t_att, "sleep_hours": t_sleep,
                    "internet_usage": t_net, "assignments_completed": t_assign,
                    "previous_score": t_prev, "exam_score": t_exam
                }
                t_res = predict_placement(t_inputs)
                st.markdown(f"### Simulation Result: **{t_res['prediction_result']}**")
                st.metric("Placement Probability", f"{t_res['placement_probability']:.1f}%")
                st.metric("Risk Level", t_res["risk_level"])
                st.plotly_chart(probability_gauge(t_res["placement_probability"]), use_container_width=True)

        render_footer()

    # --- ADMIN TAB 6: COHORT ANALYTICS ---
    elif selected_admin_nav == "📊 Cohort Analytics":
        render_hero(
            title="Cohort Dataset Analytics",
            subtitle="Exploration of the complete 10,000-student historical training corpus.",
            badge="Benchmark Data"
        )
        try:
            df_cohort = pd.read_csv(config.get_dataset_path())
            st.markdown("<div class='white-card'>", unsafe_allow_html=True)
            st.dataframe(df_cohort.head(50), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Dataset error: {e}")
        render_footer()

    # --- ADMIN TAB 7: SYSTEM SPECIFICATIONS ---
    elif selected_admin_nav == "ℹ️ System Specifications":
        render_hero(
            title="System Specifications & Architecture",
            subtitle="Platform architecture, persistent files, and environment telemetry.",
            badge="System Specs"
        )
        import sys
        health_info = [
            {"Component": "Machine Learning Model", "Path": str(config.MODEL_PATH), "Status": "Online"},
            {"Component": "StandardScaler", "Path": str(config.SCALER_PATH), "Status": "Online"},
            {"Component": "Database Engine", "Path": str(config.DATABASE_PATH), "Status": "SQLite3 Online"},
            {"Component": "Python Environment", "Path": sys.executable, "Status": f"Python {sys.version.split()[0]}"}
        ]
        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(health_info), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
        render_footer()