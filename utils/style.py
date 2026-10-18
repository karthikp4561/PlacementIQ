import streamlit as st

def load_css(is_logged_in: bool = False):
    """
    Injects high-end, modern SaaS CSS styling matching reference interfaces:
    - Login: Glassmorphism left card over tech navy gradient + crisp white right card
    - Admin: Fasto Dashboard with clean white KPI cards and colored indicator bars
    - Student: Royal blue hero welcome banner, circular probability gauge, and split gap charts
    """
    if is_logged_in:
        bg_style = """
            background-color: #f8fafc !important;
            color: #334155 !important;
        """
        sidebar_css = """
            section[data-testid="stSidebar"] {
                display: block !important;
                background-color: #111827 !important;
                border-right: 1px solid #1f2937 !important;
                width: 290px !important;
            }
            [data-testid="collapsedControl"] {
                display: block !important;
            }
            .main .block-container {
                max-width: 1320px !important;
                padding-top: 2rem !important;
                padding-bottom: 3rem !important;
                padding-left: 2rem !important;
                padding-right: 2rem !important;
            }
        """
    else:
        bg_style = """
            background: linear-gradient(108deg, #070e24 0%, #0c1a3e 33%, #162f64 47%, #eef2f8 56%, #f8fafc 100%) !important;
            background-attachment: fixed !important;
            color: #334155 !important;
        """
        sidebar_css = """
            section[data-testid="stSidebar"] {
                display: none !important;
                width: 0 !important;
                min-width: 0 !important;
            }
            [data-testid="collapsedControl"] {
                display: none !important;
            }
            .stApp::before {
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 50%;
                height: 100%;
                background-image: 
                    radial-gradient(circle at 80% 20%, rgba(56, 189, 248, 0.16) 0%, transparent 40%),
                    radial-gradient(circle at 20% 80%, rgba(37, 99, 235, 0.22) 0%, transparent 45%),
                    linear-gradient(to right, rgba(56, 189, 248, 0.05) 1px, transparent 1px),
                    linear-gradient(to bottom, rgba(56, 189, 248, 0.05) 1px, transparent 1px);
                background-size: 100% 100%, 100% 100%, 42px 42px, 42px 42px;
                pointer-events: none;
                z-index: 0;
            }
            .main .block-container {
                max-width: 1260px !important;
                padding-top: max(2rem, calc((100vh - 670px) / 2)) !important;
                padding-bottom: 2rem !important;
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
                margin: 0 auto !important;
                position: relative !important;
                z-index: 1 !important;
            }
        """

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    :root {{
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --primary-deep: #1e3a8a;
        --primary-light: #eff6ff;
        --bg-page: #f8fafc;
        --bg-card: #ffffff;
        --border-color: #e2e8f0;
        --border-focus: #3b82f6;
        --text-heading: #0f172a;
        --text-body: #334155;
        --text-muted: #64748b;
        --accent-emerald: #10b981;
        --accent-amber: #f59e0b;
        --accent-rose: #ef4444;
        --accent-purple: #7c3aed;
        --sidebar-bg: #111827;
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        --shadow-md: 0 4px 14px rgba(0,0,0,0.06);
        --shadow-lg: 0 10px 25px rgba(0,0,0,0.08);
    }}

    /* Overall Application Container */
    .stApp {{
        {bg_style}
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
    }}

    /* Remove Streamlit default header/footer clutter */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    [data-testid="stSidebarNav"] {{display: none !important;}}

    {sidebar_css}

    section[data-testid="stSidebar"] * {{
        color: #e5e7eb !important;
    }}

    section[data-testid="stSidebar"] div.stButton > button {{
        background: rgba(255, 255, 255, 0.08) !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        padding: 8px 16px !important;
        width: 100% !important;
    }}

    section[data-testid="stSidebar"] div.stButton > button:hover {{
        background: #ef4444 !important;
        border-color: #ef4444 !important;
        color: #ffffff !important;
        transform: translateY(-1px);
    }}

    /* Left Panel: Glassmorphism Branding Card */
    .glass-brand-panel {{
        background: rgba(13, 27, 62, 0.72) !important;
        backdrop-filter: blur(24px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(160%) !important;
        border: 1px solid rgba(255, 255, 255, 0.16) !important;
        border-radius: 28px !important;
        padding: 34px 34px 26px 34px !important;
        box-shadow: 0 25px 60px -15px rgba(2, 6, 23, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.25) !important;
        min-height: 590px !important;
        height: 590px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        color: #ffffff !important;
        position: relative !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
        margin-top: 0 !important;
    }}

    /* Right Panel: Clean White Container Card */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        height: 590px !important;
        margin-top: 0 !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        background: #ffffff !important;
        border-radius: 28px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.12), 0 0 1px 1px rgba(0, 0, 0, 0.04) !important;
        padding: 32px 34px !important;
        min-height: 590px !important;
        height: 590px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        box-sizing: border-box !important;
    }}

    /* Segmented Control Styling */
    div[data-testid="stSegmentedControl"] {{
        background-color: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 3px !important;
        width: 100% !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    }}

    div[data-testid="stSegmentedControl"] button {{
        border: none !important;
        border-radius: 9px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #64748b !important;
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        padding: 6px 10px !important;
        box-shadow: none !important;
        transition: all 0.15s ease !important;
        white-space: nowrap !important;
    }}

    div[data-testid="stSegmentedControl"] button * {{
        color: #64748b !important;
        background: transparent !important;
    }}

    div[data-testid="stSegmentedControl"] button[aria-checked="true"],
    div[data-testid="stSegmentedControl"] button[data-checked="true"],
    div[data-testid="stSegmentedControl"] button[aria-selected="true"],
    div[data-testid="stSegmentedControl"] button[data-selected="true"] {{
        background: #ffffff !important;
        background-color: #ffffff !important;
        background-image: none !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    }}

    div[data-testid="stSegmentedControl"] button[aria-checked="true"] *,
    div[data-testid="stSegmentedControl"] button[data-checked="true"] *,
    div[data-testid="stSegmentedControl"] button[aria-selected="true"] *,
    div[data-testid="stSegmentedControl"] button[data-selected="true"] * {{
        color: #0f172a !important;
    }}

    /* SSO Outline Buttons in Top Action Row */
    .sso-outline-btn button,
    .sso-outline-btn [data-testid="stButton"] button,
    .sso-outline-btn div.stButton > button {{
        background: #ffffff !important;
        background-color: #ffffff !important;
        background-image: none !important;
        color: #334155 !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 11px !important;
        line-height: 1.2 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        padding: 7px 6px !important;
        width: 100% !important;
        white-space: nowrap !important;
        transition: all 0.2s ease !important;
    }}

    .sso-outline-btn button *,
    .sso-outline-btn [data-testid="stButton"] button * {{
        color: #334155 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
    }}

    .sso-outline-btn button:hover,
    .sso-outline-btn [data-testid="stButton"] button:hover {{
        background: #f8fafc !important;
        background-color: #f8fafc !important;
        background-image: none !important;
        border-color: #94a3b8 !important;
        color: #0f172a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.06) !important;
    }}

    .sso-outline-btn button:hover * {{
        color: #0f172a !important;
    }}

    /* Stacked Input Fields (Light gray/blue fill with smooth rounded borders) */
    div[data-baseweb="input"] {{
        background-color: #f8fafc !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #0f172a !important;
        transition: all 0.2s ease !important;
        padding: 3px 8px !important;
    }}

    div[data-baseweb="input"]:focus-within {{
        border-color: #2563eb !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    }}

    div[data-baseweb="base-input"] input {{
        color: #0f172a !important;
        font-size: 13.5px !important;
    }}

    div[data-baseweb="base-input"] input::placeholder {{
        color: #94a3b8 !important;
    }}

    [data-testid="stWidgetLabel"] p {{
        font-weight: 600 !important;
        color: #334155 !important;
        font-size: 13px !important;
        margin-bottom: 2px !important;
    }}

    /* Primary Gradient Submit Button (Call to Action) */
    form button,
    [data-testid="stForm"] button,
    div.stFormSubmitButton button {{
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 14.5px !important;
        letter-spacing: 0.2px !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.2s ease !important;
        padding: 12px 24px !important;
        width: 100% !important;
        margin-top: 6px !important;
    }}

    form button *,
    [data-testid="stForm"] button *,
    div.stFormSubmitButton button * {{
        color: #ffffff !important;
    }}

    form button:hover,
    [data-testid="stForm"] button:hover,
    div.stFormSubmitButton button:hover {{
        background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
        transform: translateY(-1px) !important;
    }}

    /* Switch Auth Mode Button (Clean Centered Link Style) */
    .switch-auth-link {{
        text-align: center !important;
        margin-top: 8px !important;
    }}

    .switch-auth-link button,
    .switch-auth-link [data-testid="stButton"] button,
    .switch-auth-link div.stButton > button {{
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        color: #64748b !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 6px 12px !important;
        margin: 0 auto !important;
        text-align: center !important;
        transform: none !important;
        width: 100% !important;
    }}

    .switch-auth-link button *,
    .switch-auth-link [data-testid="stButton"] button * {{
        color: #64748b !important;
        background: transparent !important;
    }}

    .switch-auth-link button:hover,
    .switch-auth-link [data-testid="stButton"] button:hover {{
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        color: #2563eb !important;
        box-shadow: none !important;
        text-decoration: underline !important;
        transform: none !important;
    }}

    .switch-auth-link button:hover * {{
        color: #2563eb !important;
    }}

    [data-testid="stForm"] {{
        border: none !important;
        padding: 0 !important;
    }}

    /* Reference 3 & 4: Top Welcome Hero Banner */
    .student-welcome-banner {{
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 55%, #0284c7 100%);
        border-radius: 20px;
        padding: 30px 36px;
        color: #ffffff;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        overflow: hidden;
    }}

    .student-welcome-banner::before {{
        content: "";
        position: absolute;
        top: -50px;
        right: -50px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        pointer-events: none;
    }}

    .banner-title {{
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0 0 6px 0;
        color: #ffffff;
    }}

    .banner-subtitle {{
        color: #e0f2fe;
        font-size: 14px;
        margin: 0;
        line-height: 1.5;
        max-width: 650px;
    }}

    .banner-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        color: #ffffff;
        border-radius: 9999px;
        padding: 4px 14px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.3px;
        margin-bottom: 10px;
    }}

    /* Reference 3: Fasto KPI Metric Cards */
    .kpi-card-white {{
        background: #ffffff;
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: var(--shadow-sm);
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }}

    .kpi-card-white:hover {{
        transform: translateY(-3px);
        box-shadow: var(--shadow-md);
        border-color: #cbd5e1;
    }}

    .kpi-indicator-bar {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }}

    .kpi-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }}

    .kpi-label {{
        font-size: 13px;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .kpi-value-num {{
        font-size: 30px;
        font-weight: 800;
        color: var(--text-heading);
        letter-spacing: -0.5px;
        line-height: 1.1;
        margin-bottom: 4px;
    }}

    .kpi-subtext {{
        font-size: 12px;
        color: var(--text-muted);
    }}

    /* White Surface Card Container */
    .white-card {{
        background: #ffffff;
        border: 1px solid var(--border-color);
        border-radius: 18px;
        padding: 26px;
        box-shadow: var(--shadow-sm);
        margin-bottom: 22px;
    }}

    .white-card-title {{
        font-size: 17px;
        font-weight: 700;
        color: var(--text-heading);
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .white-card-desc {{
        color: var(--text-muted);
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 18px;
    }}

    /* Outcome Result Banners */
    .result-banner-placed-clean {{
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);
    }}

    .result-banner-notplaced-clean {{
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.08);
    }}

    /* Form Inputs Overrides (Crisp White Inputs) */
    div[data-baseweb="input"], div[data-baseweb="select"] {{
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        transition: all 0.2s ease !important;
    }}

    div[data-baseweb="input"]:focus-within {{
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    }}

    /* Form Labels */
    .stNumberInput label, .stTextInput label, .stSelectbox label {{
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }}

    /* Primary Action Buttons for Dashboard Operations */
    .white-card div.stButton > button,
    section[data-testid="stSidebar"] div.stButton > button {{
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.2s ease !important;
        padding: 10px 22px !important;
    }}

    .white-card div.stButton > button:hover,
    section[data-testid="stSidebar"] div.stButton > button:hover {{
        background: #1d4ed8 !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35) !important;
        transform: translateY(-1px);
    }}

    /* Download Button */
    div.stDownloadButton > button {{
        background: #059669 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25) !important;
        transition: all 0.2s ease !important;
    }}

    div.stDownloadButton > button:hover {{
        background: #047857 !important;
        box-shadow: 0 6px 18px rgba(5, 150, 105, 0.35) !important;
        transform: translateY(-1px);
    }}

    /* Clean Streamlit Tabs (Pill style) */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px !important;
        background-color: #f1f5f9 !important;
        padding: 4px !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #64748b !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        border: none !important;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: #ffffff !important;
        color: #2563eb !important;
        box-shadow: var(--shadow-sm) !important;
    }}

    /* Clean Footer */
    .app-footer-clean {{
        border-top: 1px solid #e2e8f0;
        margin-top: 40px;
        padding-top: 20px;
        padding-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #64748b;
        font-size: 13px;
    }}

    .badge-student-clean {{
        background: #eff6ff;
        color: #2563eb;
        border: 1px solid #bfdbfe;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }}

    .badge-admin-clean {{
        background: #faf5ff;
        color: #7c3aed;
        border: 1px solid #e9d5ff;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }}

    /* ========================================================= */
    /* GUEST LOGIN & AUTHENTICATION SPECIALIZED OVERRIDES        */
    /* ========================================================= */
    
    /* Segmented Control Pill Container & Items */
    div[data-testid="stSegmentedControl"] {{
        background-color: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 4px !important;
        width: 100% !important;
        display: flex !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    }}

    div[data-testid="stSegmentedControl"] button {{
        flex: 1 !important;
        border: none !important;
        border-radius: 9px !important;
        font-size: 12.5px !important;
        font-weight: 600 !important;
        color: #64748b !important;
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        padding: 6px 12px !important;
        box-shadow: none !important;
        transition: all 0.15s ease !important;
        white-space: nowrap !important;
    }}

    div[data-testid="stSegmentedControl"] button * {{
        color: #64748b !important;
        background: transparent !important;
    }}

    /* Selected Segment */
    div[data-testid="stSegmentedControl"] button[aria-checked="true"],
    div[data-testid="stSegmentedControl"] button[data-checked="true"],
    div[data-testid="stSegmentedControl"] button[aria-selected="true"],
    div[data-testid="stSegmentedControl"] button[data-selected="true"] {{
        background: #ffffff !important;
        background-color: #ffffff !important;
        background-image: none !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    }}

    div[data-testid="stSegmentedControl"] button[aria-checked="true"] *,
    div[data-testid="stSegmentedControl"] button[data-checked="true"] *,
    div[data-testid="stSegmentedControl"] button[aria-selected="true"] *,
    div[data-testid="stSegmentedControl"] button[data-selected="true"] * {{
        color: #0f172a !important;
    }}

    /* SSO Outline Buttons */
    [data-testid="stBaseButton-secondary"],
    [data-testid="baseButton-secondary"],
    button[kind="secondary"],
    button.e12tamyi2,
    .sso-outline-btn button,
    .sso-outline-btn [data-testid="stButton"] button,
    div.sso-outline-btn button,
    .sso-outline-btn + div.stButton button,
    .sso-outline-btn ~ div.stButton button,
    .sso-outline-btn + div button,
    .sso-outline-btn ~ div button {{
        background: #ffffff !important;
        background-color: #ffffff !important;
        background-image: none !important;
        color: #334155 !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 11px !important;
        line-height: 1.3 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        padding: 8px 10px !important;
        width: 100% !important;
        white-space: nowrap !important;
        transition: all 0.2s ease !important;
    }}

    [data-testid="stBaseButton-secondary"] *,
    [data-testid="baseButton-secondary"] *,
    button[kind="secondary"] *,
    button.e12tamyi2 *,
    .sso-outline-btn button *,
    .sso-outline-btn [data-testid="stButton"] button *,
    .sso-outline-btn + div.stButton button *,
    .sso-outline-btn ~ div.stButton button *,
    .sso-outline-btn + div button *,
    .sso-outline-btn ~ div button * {{
        color: #334155 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
    }}

    [data-testid="stBaseButton-secondary"]:hover,
    [data-testid="baseButton-secondary"]:hover,
    button[kind="secondary"]:hover,
    button.e12tamyi2:hover,
    .sso-outline-btn button:hover,
    .sso-outline-btn [data-testid="stButton"] button:hover,
    .sso-outline-btn + div.stButton button:hover,
    .sso-outline-btn ~ div.stButton button:hover,
    .sso-outline-btn + div button:hover,
    .sso-outline-btn ~ div button:hover {{
        background: #f8fafc !important;
        background-color: #f8fafc !important;
        background-image: none !important;
        border-color: #94a3b8 !important;
        color: #0f172a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.06) !important;
    }}

    [data-testid="stBaseButton-secondary"]:hover *,
    [data-testid="baseButton-secondary"]:hover *,
    button[kind="secondary"]:hover *,
    button.e12tamyi2:hover *,
    .sso-outline-btn button:hover *,
    .sso-outline-btn [data-testid="stButton"] button:hover *,
    .sso-outline-btn + div.stButton button:hover *,
    .sso-outline-btn ~ div.stButton button:hover *,
    .sso-outline-btn + div button:hover *,
    .sso-outline-btn ~ div button:hover * {{
        color: #0f172a !important;
    }}

    /* Form Submit CTA Button */
    div[data-testid="stForm"] div.stFormSubmitButton > button,
    div[data-testid="stForm"] button,
    [data-testid="stBaseButton-primary"],
    [data-testid="baseButton-primary"],
    button[kind="primary"],
    button.e12tamyi1,
    form button {{
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 0.2px !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.2s ease !important;
        padding: 13px 24px !important;
        width: 100% !important;
        margin-top: 6px !important;
    }}

    div[data-testid="stForm"] div.stFormSubmitButton > button *,
    div[data-testid="stForm"] button *,
    [data-testid="stBaseButton-primary"] *,
    [data-testid="baseButton-primary"] *,
    button[kind="primary"] *,
    button.e12tamyi1 *,
    form button * {{
        color: #ffffff !important;
    }}

    div[data-testid="stForm"] div.stFormSubmitButton > button:hover,
    div[data-testid="stForm"] button:hover,
    [data-testid="stBaseButton-primary"]:hover,
    [data-testid="baseButton-primary"]:hover,
    button[kind="primary"]:hover,
    button.e12tamyi1:hover,
    form button:hover {{
        background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
        transform: translateY(-1px) !important;
    }}

    /* Clean Centered Bottom Switch Link */
    [data-testid="stBaseButton-tertiary"],
    [data-testid="baseButton-tertiary"],
    button[kind="tertiary"],
    button.e12tamyi3,
    .switch-auth-link button,
    .switch-auth-link [data-testid="stButton"] button,
    div.switch-auth-link button,
    .switch-auth-link + div.stButton button,
    .switch-auth-link ~ div.stButton button,
    .switch-auth-link + div button,
    .switch-auth-link ~ div button {{
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        color: #64748b !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        padding: 6px 12px !important;
        margin: 4px auto 0 auto !important;
        text-align: center !important;
        transform: none !important;
        width: 100% !important;
    }}

    [data-testid="stBaseButton-tertiary"] *,
    [data-testid="baseButton-tertiary"] *,
    button[kind="tertiary"] *,
    button.e12tamyi3 *,
    .switch-auth-link button *,
    .switch-auth-link [data-testid="stButton"] button *,
    .switch-auth-link + div.stButton button *,
    .switch-auth-link ~ div.stButton button *,
    .switch-auth-link + div button *,
    .switch-auth-link ~ div button * {{
        color: #64748b !important;
        background: transparent !important;
    }}

    .switch-auth-link button:hover,
    .switch-auth-link [data-testid="stButton"] button:hover,
    .switch-auth-link + div.stButton button:hover,
    .switch-auth-link ~ div.stButton button:hover,
    .switch-auth-link + div button:hover,
    .switch-auth-link ~ div button:hover {{
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        color: #2563eb !important;
        box-shadow: none !important;
        text-decoration: underline !important;
        transform: none !important;
    }}

    .switch-auth-link button:hover *,
    .switch-auth-link [data-testid="stButton"] button:hover *,
    .switch-auth-link + div.stButton button:hover *,
    .switch-auth-link ~ div.stButton button:hover *,
    .switch-auth-link + div button:hover *,
    .switch-auth-link ~ div button:hover * {{
        color: #2563eb !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def render_hero(title: str, subtitle: str, badge: str = "PlacementIQ Platform"):
    """Renders the top welcome banner inspired by the Student Portal & Fasto reference UI."""
    st.markdown(f"""
    <div class="student-welcome-banner">
        <div>
            <div class="banner-badge">🎓 {badge}</div>
            <div class="banner-title">{title}</div>
            <div class="banner-subtitle">{subtitle}</div>
        </div>
        <div style='font-size: 48px; opacity: 0.9; margin-left: 20px;'>
            🎓
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi(col, title: str, value: str, desc: str, icon: str = "📊", accent_color: str = "#2563eb"):
    """Renders a Fasto-style clean white KPI metric card."""
    with col:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-indicator-bar" style="background: {accent_color};"></div>
            <div class="kpi-header">
                <div class="kpi-label">{title}</div>
                <div style="font-size: 18px;">{icon}</div>
            </div>
            <div class="kpi-value-num">{value}</div>
            <div class="kpi-subtext">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

def render_footer():
    """Renders the clean application footer."""
    st.markdown("""
    <div class="app-footer-clean">
        <div>
            <b>PlacementIQ</b> &copy; 2026 &bull; MCA Academic & Internship Research Platform &bull; Karthik P
        </div>
        <div>
            Powered by <b>Scikit-Learn</b> &bull; <b>Logistic Regression</b> &bull; <b>ReportLab</b>
        </div>
    </div>
    """, unsafe_allow_html=True)