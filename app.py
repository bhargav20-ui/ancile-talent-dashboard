# -*- coding: utf-8 -*-
"""
Ancile Talent Intelligence Dashboard v5
7 Pages: Overview | Analytics | AI Skill Matcher | Dataset Explorer |
         Resume Upload | Manage Candidates | About

FIXES APPLIED
  FIX 1: keyboard_double_arrow text hidden via CSS targeting
          [data-testid="stSidebarCollapsedControl"] and button[kind="header"]
  FIX 2: Dataset Explorer — Sort controls moved to their own row above the
          table so the 3-dot column popup has space to open without covering
          the first few data rows.
"""
import os
import sys
import streamlit as st
import pandas as pd

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from modules.data_loader import load_data, get_kpis
from modules.analytics import (
    chart_top_skills,
    chart_domain_distribution,
    chart_placement_by_role,
    chart_experience_distribution,
    chart_monthly_trend,
    chart_location_map,
    chart_match_score_box,
    chart_status_funnel,
    chart_client_placements,
)
from modules.ai_matcher import match_skills, extract_text_from_pdf, extract_skills_from_resume

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ancile Talent Intelligence Dashboard",
    page_icon="assets/ancile_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────

st.markdown("""

<style>
            
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body {
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1rem !important; padding-bottom: 2rem; }

/* ────────────────────────────────────────────────────────────────────────────
   FIX 1 — Hide the sidebar collapse/expand toggle button that renders the
   "keyboard_double_arrow" Material icon name as plain visible text.
   We target every known selector Streamlit uses across versions.

──────────────────────────────────────────────────────────────────────────── */

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1F44 0%, #0D2860 100%);
    border-right: 1px solid #1E3A6E;
}
[data-testid="stSidebar"] * { color: #FFFFFF !important; }
[data-testid="stSidebarNav"] { display: none; }

/* ── Page header ── */
.ancile-header {
    background: linear-gradient(135deg, #0A1F44 0%, #0D2860 50%, #102880 100%);
    border: 1px solid #1E3A6E;
    border-radius: 16px;
    padding: 1.4rem 2rem;
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.ancile-header h1 {
    color: #FFFFFF !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
    line-height: 1.2 !important;
}
.ancile-header p {
    color: #8892A4 !important;
    font-size: 0.82rem !important;
    margin: 0.2rem 0 0 0 !important;
}
.ancile-badge {
    background: linear-gradient(135deg, #F76C1B, #FF8C42);
    color: white !important;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    font-size: 0.70rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    white-space: nowrap;
}
header[data-testid="stHeader"]{
    background: transparent !important;
}


/* ── KPI cards ── */
.kpi-card {
    background: linear-gradient(135deg, #0A1F44, #112666);
    border: 1px solid #1E3A6E;
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
    margin-bottom: 6px;
}
.kpi-card:hover { transform: translateY(-3px); border-color: #F76C1B; }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #F76C1B, #FF8C42);
}
.kpi-icon  { font-size: 1.4rem; margin-bottom: 0.3rem; }
.kpi-value { color: #F76C1B !important; font-size: 1.75rem !important; font-weight: 700 !important; line-height: 1; margin: 0.15rem 0; }
.kpi-label { color: #8892A4 !important; font-size: 0.72rem !important; font-weight: 500 !important; letter-spacing: 0.5px; text-transform: uppercase; margin-top: 0.25rem; }
.kpi-sub   { color: #4A90D9 !important; font-size: 0.68rem !important; margin-top: 0.15rem; }

/* ── Section title ── */
.section-title {
    color: #FFFFFF !important;
    font-size: 1.0rem !important;
    font-weight: 600 !important;
    margin: 1.2rem 0 0.8rem 0 !important;
    padding-left: 0.75rem;
    border-left: 3px solid #F76C1B;
}

/* ── AI Matcher result cards ── */
.match-card {
    background: linear-gradient(135deg, #0A2A0A, #0D3A0D);
    border: 1px solid #1A5C1A;
    border-radius: 14px;
    padding: 1.4rem;
    margin: 0.8rem 0;
}
.match-role  { color: #34D399 !important; font-size: 1.45rem !important; font-weight: 700 !important; }
.match-score { color: #F76C1B !important; font-size: 2.1rem !important; font-weight: 800 !important; }

/* ── Skill pills ── */
.skill-pill {
    display: inline-block;
    background: rgba(247,108,27,0.14);
    border: 1px solid rgba(247,108,27,0.4);
    color: #F76C1B !important;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 500;
    margin: 0.18rem;
}
.skill-pill.missing {
    background: rgba(239,68,68,0.14);
    border-color: rgba(239,68,68,0.4);
    color: #EF4444 !important;
}
.skill-pill.matched {
    background: rgba(52,211,153,0.14);
    border-color: rgba(52,211,153,0.4);
    color: #34D399 !important;
}
.skill-pill.alt {
    background: rgba(96,165,250,0.14);
    border-color: rgba(96,165,250,0.4);
    color: #60A5FA !important;
}

/* ── Progress bar ── */
.prog-wrap { background: #1A2744; border-radius: 8px; height: 10px; overflow: hidden; margin: 0.4rem 0; }
.prog-fill  { height: 100%; border-radius: 8px; background: linear-gradient(90deg, #F76C1B, #FF8C42); }

/* ── About / info cards ── */
.about-card {
    background: linear-gradient(135deg, #0A1F44, #112666);
    border: 1px solid #1E3A6E;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
}
.about-card h4 { color: #F76C1B !important; margin: 0 0 0.5rem 0 !important; font-size: 0.95rem !important; }
.about-card p, .about-card li { color: #8892A4 !important; font-size: 0.82rem !important; line-height: 1.5; }

/* ── Filter label ── */
.filter-label {
    color: #8892A4 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.2rem;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background: #1A2744 !important;
    border-color: #2A3A5C !important;
    color: white !important;
}

/* ── Tip box ── */
.tip-box {
    background: #0A2035;
    border-left: 3px solid #F76C1B;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin-top: 10px;
}
.tip-box span { color: #8892A4; font-size: 0.80rem; }

/* ── Sidebar nav radio buttons ── */
div[role="radiogroup"] label {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: white !important;
}
div[role="radiogroup"] label:hover { color: #F76C1B !important; }
div[role="radiogroup"] > label[data-baseweb="radio"] {
    padding: 6px;
    border-radius: 10px;
}
div[role="radiogroup"] label[data-baseweb="radio"] {
    padding: 8px !important;
    border-radius: 10px !important;
}
div[role="radiogroup"] label[data-baseweb="radio"]:hover {
    background: rgba(247,108,27,0.15) !important;
}

/* ────────────────────────────────────────────────────────────────────────────
   FIX 2 — Dataset Explorer dataframe styling.
   The 3-dot column menu popup is rendered by the browser at z-index ~9999
   and floats above the page. Adding a top spacer (via the HTML div below in
   Python) and explicit overflow:visible on the wrapper lets the popup render
   in free space rather than clipping behind the canvas rows.
──────────────────────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
}
[data-testid="stDataFrame"] table {
    font-size: 14px !important;
}
/* Allow the popup to escape the container boundary */
[data-testid="stDataFrame"] > div,
[data-testid="stDataFrame"] > div > div {
    overflow: visible !important;
}
/* Placeholder text styling */

input::placeholder,
textarea::placeholder {
    color: rgba(255,255,255,0.35) !important;
    opacity: 1 !important;
}

[data-baseweb="input"] input::placeholder {
    color: rgba(255,255,255,0.35) !important;
}

[data-baseweb="textarea"] textarea::placeholder {
    color: rgba(255,255,255,0.35) !important;
}

</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
df_full = load_data()
# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("assets/ancile_logo.png", width=90)

    st.markdown(
        """
        <div style="text-align:center; margin-top:-18px;">
            <h2 style="color:white; margin-bottom:0; font-size:1.2rem;">Ancile Inc.</h2>
            <p style="color:#8892A4; margin-top:0; font-size:0.78rem;">Talent Intelligence Platform</p>
        </div>
        <hr style="border-color:#1E3A6E; margin:0.8rem 0 1rem 0;">
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "🏠 Overview",
            "📊 Analytics",
            "🤖 AI Skill Matcher",
            "🗂 Dataset Explorer",
            "📄 Resume Upload",
            "👥 Manage Candidates",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#1E3A6E; margin:0.9rem 0;'>", unsafe_allow_html=True)

    # Filters (shown only on relevant pages)
    if page in ["🏠 Overview", "📊 Analytics", "🗂 Dataset Explorer"]:
        st.markdown('<div class="filter-label">Filters</div>', unsafe_allow_html=True)
        sel_domain = st.selectbox("Domain", ["All"] + sorted(df_full["Domain"].unique()), key="fd")
        sel_status = st.selectbox("Status", ["All", "Placed", "Pending", "Rejected"], key="fs")
        emin = float(df_full["Experience_Years"].min())
        emax = float(df_full["Experience_Years"].max())
        sel_exp = st.slider("Experience (yrs)", emin, emax, (emin, emax), step=0.5, key="fe")
        df = df_full.copy()
        if sel_domain != "All":
            df = df[df["Domain"] == sel_domain]
        if sel_status != "All":
            df = df[df["Status"] == sel_status]
        df = df[(df["Experience_Years"] >= sel_exp[0]) & (df["Experience_Years"] <= sel_exp[1])]
    else:
        df = df_full.copy()


# ── Header helper ─────────────────────────────────────────────────────────────
def header(subtitle: str):
    st.markdown(
        f"""
    <div class="ancile-header">
        <div style="flex:1;">
            <h1>Ancile Talent Intelligence Dashboard</h1>
            <p>{subtitle}</p>
        </div>
        <span class="ancile-badge">LIVE &middot; {len(df_full)} Candidates</span>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ── KPI helper ────────────────────────────────────────────────────────────────
def kpi_card(icon, value, label, sub=""):
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-label">{label}</div>'
        + (f'<div class="kpi-sub">{sub}</div>' if sub else "")
        + "</div>"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    header("Recruitment Analytics & Talent Insights · Ancile Inc. 2026")
    kpis = get_kpis(df)

    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    cards = [
        (c1, "👥", kpis["total_candidates"],        "Total Candidates", "In pipeline"),
        (c2, "✅", kpis["placed"],                  "Placed",           "Successful"),
        (c3, "🕐", kpis["pending"],                 "Pending",          "In review"),
        (c4, "📈", f"{kpis['placement_rate']}%",    "Placement Rate",   "Success ratio"),
        (c5, "⭐", f"{kpis['avg_match_score']}%",   "Avg AI Score",     "Match accuracy"),
        (c6, "🏆", kpis["top_domain"],              "Top Domain",       "Highest demand"),
        (c7, "📄", len(df_full["Role"].unique()),    "Active Roles",     "Open positions"),
    ]
    for col, icon, val, label, sub in cards:
        with col:
            st.markdown(kpi_card(icon, val, label, sub), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown('<div class="section-title">In-Demand Skills</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_top_skills(df, 8), use_container_width=True)
    with r1c2:
        st.markdown('<div class="section-title">Domain Distribution</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_domain_distribution(df), use_container_width=True)

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown('<div class="section-title">Monthly Joining Trend</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_monthly_trend(df), use_container_width=True)
    with r2c2:
        st.markdown('<div class="section-title">Recruitment Funnel</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_status_funnel(df), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Analytics":
    header("Deep-Dive Analytics · Filtered & Interactive")

    if len(df) == 0:
        st.warning("No data matches your current filters. Adjust the sidebar filters.")
    else:
        kpis = get_kpis(df)
        c1, c2, c3, c4 = st.columns(4)
        mini = [
            (c1, kpis["total_candidates"],        "Filtered Candidates"),
            (c2, kpis["placed"],                  "Placed"),
            (c3, f"{kpis['placement_rate']}%",    "Placement Rate"),
            (c4, f"{kpis['avg_experience']} yrs", "Avg Experience"),
        ]
        for col, val, label in mini:
            with col:
                st.markdown(
                    f'<div class="kpi-card"><div class="kpi-value">{val}</div>'
                    f'<div class="kpi-label">{label}</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        r1, r2 = st.columns(2)
        with r1:
            st.markdown('<div class="section-title">Top In-Demand Skills</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_top_skills(df, 12), use_container_width=True)
        with r2:
            st.markdown('<div class="section-title">Domain Distribution</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_domain_distribution(df), use_container_width=True)

        r3, r4 = st.columns(2)
        with r3:
            st.markdown('<div class="section-title">Placement Status by Role</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_placement_by_role(df), use_container_width=True)
        with r4:
            st.markdown('<div class="section-title">Experience Distribution</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_experience_distribution(df), use_container_width=True)

        r5, r6 = st.columns(2)
        with r5:
            st.markdown('<div class="section-title">Candidates by Location</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_location_map(df), use_container_width=True)
        with r6:
            st.markdown('<div class="section-title">Match Score by Domain</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_match_score_box(df), use_container_width=True)

        st.markdown('<div class="section-title">Top Clients by Placements</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_client_placements(df), use_container_width=True)

        st.markdown('<div class="section-title">Monthly Joining Trend</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_monthly_trend(df), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — AI SKILL MATCHER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 AI Skill Matcher":
    header("AI-Powered Role Recommendation · TF-IDF + Cosine Similarity")

    st.markdown("""
    <div class="about-card" style="margin-bottom:1.2rem;">
        <h4>How the AI Works</h4>
        <p>
        This matcher uses <b style="color:#FFFFFF;">TF-IDF vectorization</b> and
        <b style="color:#FFFFFF;">Cosine Similarity</b> to compare your skills against
        18 curated role profiles. It returns your best role match, match score, missing
        skills, and career-specific tips — just like a real ATS system.
        </p>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio("Input Mode", ["Type Skills Manually", "Upload Resume PDF"], horizontal=True)
    user_skills_text = ""

    if mode == "Type Skills Manually":
        st.markdown('<div class="section-title">Enter Your Skills</div>', unsafe_allow_html=True)

        ex_cols = st.columns(4)
        EXAMPLES = {
            "Data Analyst":   "Python, SQL, Excel, Power BI, Pandas, Tableau",
            "ML Engineer":    "Python, TensorFlow, Scikit-learn, NLP, Statistics, PyTorch",
            "Full Stack Dev": "React, Node.js, MongoDB, JavaScript, CSS, REST API",
            "Cloud Engineer": "AWS, Docker, Kubernetes, Terraform, Linux, CI/CD",
        }
        chosen = ""
        for col, (label, skills) in zip(ex_cols, EXAMPLES.items()):
            with col:
                if st.button(label, use_container_width=True, key=f"ex_{label}"):
                    chosen = skills

        user_skills_text = st.text_area(
            "Skills (comma-separated)",
            value=chosen,
            placeholder="e.g., Python, SQL, Pandas, Power BI, Excel",
            height=100,
            label_visibility="collapsed",
        )

    else:
        st.markdown('<div class="section-title">Upload Your Resume (PDF)</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload PDF Resume", type=["pdf"], label_visibility="collapsed")
        if uploaded:
            with st.spinner("Extracting skills from resume..."):
                raw = extract_text_from_pdf(uploaded)
                user_skills_text = extract_skills_from_resume(raw)
            if user_skills_text:
                st.success("Skills extracted successfully!")
                with st.expander("Extracted Skills Preview"):
                    st.code(user_skills_text)
            else:
                st.error("Could not extract text. Please use a text-based PDF, not a scanned image.")

    top_n = st.slider("Roles to show", 1, 5, 3)
    run_btn = st.button("Analyze & Match Role", type="primary", use_container_width=True)

    if run_btn:
        if not user_skills_text.strip():
            st.warning("Please enter at least one skill.")
        else:
            with st.spinner("Running AI analysis..."):
                result = match_skills(user_skills_text, top_n=top_n)

            if not result:
                st.warning("Could not generate results. Please check your input.")
            else:
                st.markdown("---")
                st.markdown('<div class="section-title">Your Results</div>', unsafe_allow_html=True)

                score = result["top_score"]
                score_color = "#34D399" if score >= 72 else "#F76C1B" if score >= 52 else "#EF4444"
                verdict = "Excellent Match!" if score >= 72 else "Good Potential" if score >= 52 else "Needs Improvement"
                level_emoji = {"Excellent": "🎉", "Good": "💪", "Average": "📚"}.get(result["match_level"], "")

                r1, r2 = st.columns([3, 2])

                with r1:
                    st.markdown(f"""
                    <div class="match-card">
                        <div style="color:#8892A4;font-size:0.75rem;font-weight:600;
                                    text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">
                            Recommended Role
                        </div>
                        <div class="match-role">{result["top_role"]}</div>
                        <div style="margin:1rem 0 0.4rem 0;">
                            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                                <span style="color:#8892A4;font-size:0.78rem;">Match Score</span>
                                <span style="color:{score_color};font-weight:700;">{score}% · {result["match_level"]}</span>
                            </div>
                            <div class="prog-wrap">
                                <div class="prog-fill" style="width:{score}%;
                                     background:linear-gradient(90deg,{score_color},{score_color}bb);"></div>
                            </div>
                        </div>
                        <div style="color:{score_color};font-weight:600;font-size:0.9rem;">
                            {level_emoji} {verdict}
                        </div>
                        <div class="tip-box">
                            <span style="color:#F76C1B;font-size:0.70rem;text-transform:uppercase;
                                  letter-spacing:1px;font-weight:600;">Career Tip</span><br>
                            <span>{result["career_tip"]}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with r2:
                    st.markdown('<div class="about-card"><h4>Alternative Roles</h4>', unsafe_allow_html=True)
                    for alt in result["alternatives"]:
                        as_ = alt["score"]
                        st.markdown(f"""
                        <div style="margin-bottom:0.7rem;">
                            <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                                <span style="color:#FFFFFF;font-size:0.83rem;">{alt["role"]}</span>
                                <span style="color:#60A5FA;font-weight:600;">{as_}%</span>
                            </div>
                            <div class="prog-wrap" style="height:7px;">
                                <div class="prog-fill"
                                     style="width:{as_}%;background:linear-gradient(90deg,#1E5FCC,#60A5FA);">
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                s1, s2 = st.columns(2)
                with s1:
                    st.markdown('<div class="section-title">Matched Skills</div>', unsafe_allow_html=True)
                    if result["matched_skills"]:
                        pills = " ".join(
                            f'<span class="skill-pill matched">{s}</span>'
                            for s in result["matched_skills"]
                        )
                        st.markdown(f'<div style="line-height:2.2;">{pills}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(
                            '<div style="color:#8892A4;font-size:0.83rem;">'
                            "No direct keyword matches. Try expanding your skill list.</div>",
                            unsafe_allow_html=True,
                        )

                with s2:
                    st.markdown('<div class="section-title">Skills to Add</div>', unsafe_allow_html=True)
                    if result["missing_skills"]:
                        pills = " ".join(
                            f'<span class="skill-pill missing">{s}</span>'
                            for s in result["missing_skills"]
                        )
                        st.markdown(f'<div style="line-height:2.2;">{pills}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(
                            '<div style="color:#34D399;font-size:0.83rem;">'
                            "Great — you cover the key skills for this role!</div>",
                            unsafe_allow_html=True,
                        )

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-title">Action Plan</div>', unsafe_allow_html=True)
                m_str = ", ".join(result["missing_skills"][:3]) or "keep building current stack"
                alt0 = result["alternatives"][0]["role"] if result["alternatives"] else "similar roles"
                st.info(f"""
**Your recommended next steps:**
1. **Apply for:** {result["top_role"]} positions at consulting and IT firms
2. **Upskill in:** {m_str}
3. **Also consider:** {alt0} as a strong alternative
4. **Target score:** Aim for 80%+ by adding 2–3 missing skills
                """)

                report = "\n".join(
                    [
                        "Ancile AI Skill Matcher Report",
                        f"Input Skills: {user_skills_text}",
                        "",
                        f"Top Role: {result['top_role']}  Score: {result['top_score']}%  [{result['match_level']}]",
                        f"Career Tip: {result['career_tip']}",
                        "",
                        "Missing Skills: " + ", ".join(result["missing_skills"]),
                        "Matched Skills: " + ", ".join(result["matched_skills"]),
                        "",
                        "Alternatives:",
                    ]
                    + [f"  {a['role']} — {a['score']}%" for a in result["alternatives"]]
                )
                st.download_button(
                    "Download Match Report",
                    data=report.encode("utf-8"),
                    file_name="skill_match_report.txt",
                    mime="text/plain",
                )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — DATASET EXPLORER
# FIX 2: Sort controls moved to their own dedicated row (sc1, sc2 columns)
# above the dataframe so the 3-dot column popup can open freely without
# overlapping the data rows underneath.
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🗂 Dataset Explorer":
    header("Raw Data Explorer · Search, Filter & Export")

    if len(df) == 0:
        st.warning("No data matches your current filters.")
    else:
        # Row 1 — search (full width)
        search = st.text_input(
            "Search by name, skill, role, or location",
            placeholder="e.g. Python, Bangalore, Data Analyst...",
        )

        # Row 2 — sort controls on their own row, not squashed beside search
        sort_col = st.selectbox(
            "Sort by",
            ["Candidate_ID", "Match_Score", "Experience_Years", "Name", "Domain", "Status"],
        )

        sort_ascending = True
        # Apply search & sort
        df_view = df.copy()
        if search.strip():
            q = search.strip().lower()
            mask = (
                df_view["Name"].str.lower().str.contains(q, na=False)
                | df_view["Skills"].str.lower().str.contains(q, na=False)
                | df_view["Role"].str.lower().str.contains(q, na=False)
                | df_view["Location"].str.lower().str.contains(q, na=False)
                | df_view["Domain"].str.lower().str.contains(q, na=False)
            )
            df_view = df_view[mask]

        if sort_col == "Candidate_ID":
            df_view["_sort_id"] = (
                df_view["Candidate_ID"].str.replace("ANC", "", regex=False).astype(int)
            )
            df_view = df_view.sort_values("_sort_id", ascending=sort_ascending).drop(
                columns="_sort_id"
            )
        else:
            df_view = df_view.sort_values(by=sort_col, ascending=sort_ascending)

        st.markdown(
            f'<div class="section-title">Showing {len(df_view)} of {len(df)} records</div>',
            unsafe_allow_html=True,
        )

        # Small spacer — gives the column header popup room to open above row 1
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        st.data_editor(
            df_view.reset_index(drop=True),
            use_container_width=True,
            height=560,
            hide_index=True,
            column_config={
                "Candidate_ID":     st.column_config.TextColumn("ID",         width=90),
                "Name":             st.column_config.TextColumn("Name",       width=130),
                "Domain":           st.column_config.TextColumn("Domain",     width=130),
                "Role":             st.column_config.TextColumn("Role",       width=150),
                "Skills":           st.column_config.TextColumn("Skills",     width=260),
                "Experience_Years": st.column_config.NumberColumn(
                                        "Exp (yrs)", width=80, format="%.1f"
                                    ),
                "Location":         st.column_config.TextColumn("Location",   width=100),
                "Status":           st.column_config.TextColumn("Status",     width=80),
                "Client_Company":   st.column_config.TextColumn("Client",     width=120),
                "Match_Score":      st.column_config.ProgressColumn(
                                        "Match %", min_value=0, max_value=100, width=110
                                    ),
                "Joined_Month":     st.column_config.TextColumn("Joined",     width=110),
            },
        )

        csv_bytes = df_view.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Filtered Dataset (CSV)",
            data=csv_bytes,
            file_name="ancile_candidates_export.csv",
            mime="text/csv",
            type="primary",
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — RESUME UPLOAD
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📄 Resume Upload":
    header("Resume Upload Portal")

    st.markdown("""
    <div class="about-card">
        <h4>Upload Candidate Resume</h4>
        <p>Recruiters can upload resumes for future processing and evaluation.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])
    if uploaded_file:
        size_kb = round(uploaded_file.size / 1024, 2)
        st.success("Resume uploaded successfully and ready for future processing.")
        st.info(f"Filename: {uploaded_file.name}\n\nFile Size: {size_kb} KB")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — MANAGE CANDIDATES
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "👥 Manage Candidates":
    header("Candidate Management Portal")

    st.markdown("""
    <div class="about-card">
        <h4>Manage Candidates</h4>
        <p>Add new candidates or remove existing candidates from the recruitment pipeline.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── ADD ───────────────────────────────────────────────────────────────────
    st.subheader("➕ Add Candidate")

    with st.form("candidate_form"):
        name       = st.text_input("Candidate Name")
        skills     = st.text_area("Skills", placeholder="Python, SQL, Power BI")
        experience = st.number_input(
            "Experience (Years)", min_value=0.0, max_value=30.0, value=1.0, step=0.5
        )
        domain = st.selectbox("Domain", sorted(df_full["Domain"].unique()))
        status = st.selectbox("Status", ["Pending", "Placed", "Rejected"])
        submit = st.form_submit_button("Add Candidate", type="primary")

    if submit:
        csv_path  = os.path.join(ROOT, "data", "candidates.csv")
        latest_df = pd.read_csv(csv_path)
        new_id    = f"ANC{int(latest_df['Candidate_ID'].str.replace('ANC', '', regex=False).astype(int).max()) + 1}"
        new_row   = {
            "Candidate_ID":    new_id,
            "Name":            name,
            "Domain":          domain,
            "Role":            "Not Assigned",
            "Skills":          skills,
            "Experience_Years": experience,
            "Location":        "N/A",
            "Status":          status,
            "Client_Company":  "N/A",
            "Match_Score":     0,
            "Joined_Month":    pd.Timestamp.today().strftime("%B %Y"),
        }
        latest_df = pd.concat([latest_df, pd.DataFrame([new_row])], ignore_index=True)
        latest_df.to_csv(csv_path, index=False)
        st.success(f"{name} added successfully!")
        st.balloons()
        st.cache_data.clear()
        st.rerun()

    st.divider()

    # ── DELETE ────────────────────────────────────────────────────────────────
    st.subheader("🗑 Delete Candidate")

    delete_options = ["Select a candidate..."] + [
        f"{row['Candidate_ID']} - {row['Name']}"
        for _, row in df_full.iterrows()
    ]

    candidate_to_delete = st.selectbox(
        "Select Candidate",
        delete_options
    )
    confirm_delete      = st.checkbox("I confirm deletion")

    if confirm_delete and st.button("Delete Candidate", type="secondary"):
        candidate_id = candidate_to_delete.split(" - ")[0]
        csv_path     = os.path.join(ROOT, "data", "candidates.csv")
        latest_df    = pd.read_csv(csv_path)
        latest_df    = latest_df[latest_df["Candidate_ID"] != candidate_id]
        latest_df.to_csv(csv_path, index=False)
        st.success(f"{candidate_to_delete} deleted successfully!")
        st.cache_data.clear()
        st.rerun()

    st.divider()

    # ── PREVIEW ───────────────────────────────────────────────────────────────
    st.subheader("📋 Candidate Preview")
    st.dataframe(
        df_full[["Candidate_ID", "Name", "Domain", "Status"]].sort_values("Candidate_ID"),
        use_container_width=True,
        hide_index=True,
        height=350,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "ℹ️ About":
    header("Project Overview, Technology Stack & Architecture")

    st.markdown("""
    <div class="about-card">
        <h4>Project Objective</h4>
        <p>
        The <b style="color:white;">Ancile Talent Intelligence Dashboard</b>
        helps Ancile's recruiting and consulting teams visualize skill demand trends,
        track placement success rates, and intelligently match candidates to roles.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="about-card">
            <h4>Tech Stack</h4>
            <ul>
                <li><b style="color:white;">Dashboard:</b> Streamlit + Plotly</li>
                <li><b style="color:white;">Data Processing:</b> Python + Pandas</li>
                <li><b style="color:white;">AI Module:</b> TF-IDF + Cosine Similarity</li>
                <li><b style="color:white;">PDF Parsing:</b> PyMuPDF</li>
                <li><b style="color:white;">Version Control:</b> GitHub</li>
                <li><b style="color:white;">Dataset:</b> {len(df_full)} Candidate Profiles</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="about-card">
            <h4>Key Features</h4>
            <ul>
                <li>Interactive Recruitment Analytics Dashboard</li>
                <li>AI-Powered Skill Matching System</li>
                <li>Resume PDF Skill Extraction</li>
                <li>Advanced Candidate Filtering</li>
                <li>Dataset Search &amp; Export Functionality</li>
                <li>Real-time KPI Monitoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card">
        <h4>Architecture</h4>
        <p>
        Candidate Dataset (CSV)
        <span style="color:#F76C1B;"> → </span>
        Data Processing (Pandas)
        <span style="color:#F76C1B;"> → </span>
        Analytics Engine (Plotly)
        <span style="color:#F76C1B;"> → </span>
        Streamlit Dashboard
        <span style="color:#F76C1B;"> → </span>
        AI Skill Matcher (TF-IDF + Cosine Similarity)
        <span style="color:#F76C1B;"> → </span>
        Role Recommendation
        </p>
    </div>
    """, unsafe_allow_html=True)
