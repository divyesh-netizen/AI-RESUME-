import os
import sys
import json
import time
from datetime import datetime
import streamlit as st
import pandas as pd

# Add backend directory to python path
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import database
import nlp_engine

# Initialize Database Schema
database.init_db()

# Configure Streamlit Page
st.set_page_config(
    page_title="ResumeIQ — Intelligent Resume Screening & Fit Analysis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Refined Human-Crafted SaaS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.01em;
    }

    /* Background and global typography */
    .stApp {
        background-color: #090d16;
        color: #e2e8f0;
    }

    /* Top Brand & Hero Header */
    .saas-header {
        padding: 1.75rem 0 2rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 2rem;
    }

    .saas-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.25);
        color: #a5b4fc;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin-bottom: 0.85rem;
    }

    .saas-title {
        font-size: 2.35rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.2;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .saas-subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
        max-width: 680px;
        line-height: 1.6;
        font-weight: 400;
    }

    /* Clean Card Surfaces */
    .saas-card {
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.25rem;
    }

    .score-banner-card {
        background: linear-gradient(145deg, #131c31 0%, #0d1527 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 1.25rem;
        padding: 1.75rem 2rem;
        box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 1.75rem;
    }

    /* Metric Sub-cards */
    .submetric-box {
        background: #131c31;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 0.85rem;
        padding: 1.15rem;
    }

    /* Refined Tag Pills */
    .pill-matched {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.65rem;
        border-radius: 0.4rem;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.25);
        margin: 0.2rem 0.25rem 0.2rem 0;
    }

    .pill-missing {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.65rem;
        border-radius: 0.4rem;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.25);
        margin: 0.2rem 0.25rem 0.2rem 0;
    }

    /* High-End Primary Button */
    .stButton > button {
        background: #4f46e5 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border-radius: 0.65rem !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        padding: 0.65rem 1.4rem !important;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover {
        background: #4338ca !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.45) !important;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Text areas */
    .stTextArea textarea {
        background: #0f172a !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 0.65rem !important;
        color: #f1f5f9 !important;
        font-size: 0.85rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    /* Tabs Clean Line */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 0.9rem;
        color: #94a3b8;
        padding: 0.5rem 0.25rem;
    }
    .stTabs [aria-selected="true"] {
        color: #6366f1 !important;
        border-bottom: 2px solid #6366f1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = ""
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": """Hello! I am your **ResumeIQ Career Advisor**.

I can evaluate your resume against any job description, pinpoint skill gaps, and provide actionable advice. 

Feel free to ask me:
- *"How can I improve my match score to 90% or higher?"*
- *"What high-priority keywords are missing from my resume?"*
- *"Rewrite my work experience bullet points using the X-Y-Z formula."*
- *"What qualifications or certifications would strengthen my application?"*"""
        }
    ]

# Refined Circular Radial Gauge
def render_circular_gauge(score, label):
    is_strong = score >= 80
    is_moderate = score >= 60 and score < 80
    
    stroke_color = "#10b981" if is_strong else ("#6366f1" if is_moderate else "#f43f5e")
    badge_bg = "rgba(16, 185, 129, 0.12)" if is_strong else ("rgba(99, 102, 241, 0.12)" if is_moderate else "rgba(244, 63, 94, 0.12)")
    badge_color = "#34d399" if is_strong else ("#a5b4fc" if is_moderate else "#fb7185")
    
    radius = 56
    circumference = 2 * 3.14159 * radius
    offset = circumference - (score / 100.0) * circumference

    svg_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
        <div style="position: relative; width: 160px; height: 160px;">
            <svg style="transform: rotate(-90deg); width: 100%; height: 100%;" viewBox="0 0 140 140">
                <circle cx="70" cy="70" r="{radius}" stroke="rgba(255,255,255,0.06)" stroke-width="10" fill="transparent" />
                <circle cx="70" cy="70" r="{radius}" stroke="{stroke_color}" stroke-width="10" stroke-linecap="round"
                        stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" fill="transparent"
                        style="transition: stroke-dashoffset 0.8s ease-in-out;" />
            </svg>
            <div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <span style="font-size: 2.25rem; font-weight: 800; color: #ffffff; letter-spacing: -0.03em; line-height: 1;">{score}%</span>
                <span style="font-size: 0.7rem; font-weight: 700; color: {badge_color}; text-transform: uppercase; margin-top: 4px; letter-spacing: 0.05em;">{label}</span>
            </div>
        </div>
        <span style="font-size: 0.75rem; color: #64748b; margin-top: 0.5rem; font-weight: 500;">Overall Match Index</span>
    </div>
    """
    return svg_html

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.65rem; margin-bottom: 1.25rem;">
        <div style="width: 32px; height: 32px; border-radius: 8px; background: #4f46e5; display: flex; align-items: center; justify-content: center; font-size: 1rem; color: white;">
            📄
        </div>
        <div>
            <div style="font-weight: 800; font-size: 1.05rem; color: #ffffff; letter-spacing: -0.02em;">ResumeIQ</div>
            <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 500;">Universal Screening Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.25rem;'>Universal Role Compatibility</p>", unsafe_allow_html=True)
    st.caption("Works for candidate profiles across **any industry or profession** (Healthcare, Business, Finance, Education, Legal, Creative, Operations, Engineering, and more).")

    if st.button("Clear Input Fields", use_container_width=True):
        st.session_state.resume_text = ""
        st.session_state.job_description = ""
        st.session_state.candidate_name = ""
        st.session_state.current_result = None
        st.rerun()

    st.markdown("---")
    st.markdown("<p style='font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.5rem;'>Pipeline Activity</p>", unsafe_allow_html=True)
    candidates_in_db = database.get_candidates()
    st.metric("Total Candidates Evaluated", len(candidates_in_db))
    strong_matches = len([c for c in candidates_in_db if c["overall_score"] >= 80])
    st.metric("High Match Candidates (80%+)", f"{strong_matches} of {len(candidates_in_db)}")

    st.markdown("---")
    st.caption("Grounded in TF-IDF semantic vectorization, functional keyword analysis, and ATS heuristic standards.")

# ==========================================
# MAIN HERO BANNER
# ==========================================
st.markdown("""
<div class="saas-header">
    <div class="saas-badge">Universal Resume Screening & Match Analysis</div>
    <div class="saas-title">Screen Resumes with Clarity & Precision</div>
    <div class="saas-subtitle">Evaluate candidate resumes against any job description, uncover skill gaps, and receive actionable suggestions to optimize for hiring requirements and ATS standards.</div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_screen, tab_recruiter, tab_compare, tab_coach = st.tabs([
    "Screen & Score",
    "Candidate Pipeline",
    "Compare Candidates",
    "Career Advisor"
])

# ==========================================
# TAB 1: SCREEN & SCORE
# ==========================================
with tab_screen:
    col_input_left, col_input_right = st.columns(2)

    with col_input_left:
        st.markdown("<p style='font-size: 0.95rem; font-weight: 700; color: #ffffff; margin-bottom: 0.25rem;'>1. Candidate Resume</p>", unsafe_allow_html=True)
        cand_name_input = st.text_input("Candidate Name", value=st.session_state.candidate_name, placeholder="e.g. Alex Morgan (optional)")
        
        upload_choice = st.radio("Input Method:", ["Upload File (PDF / DOCX / TXT)", "Paste Text"], horizontal=True)
        
        if upload_choice == "Upload File (PDF / DOCX / TXT)":
            uploaded_file = st.file_uploader("Upload resume file", type=["pdf", "docx", "doc", "txt"], label_visibility="collapsed")
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                extracted = nlp_engine.extract_text_from_file(file_bytes, uploaded_file.name)
                st.session_state.resume_text = extracted
                st.success(f"Extracted {len(extracted.split())} words from {uploaded_file.name}")
        else:
            resume_text_val = st.text_area(
                "Resume Content",
                value=st.session_state.resume_text,
                height=260,
                placeholder="Paste the candidate's resume content here (Summary, Work Experience, Skills, Education, Achievements)...",
                label_visibility="collapsed"
            )
            st.session_state.resume_text = resume_text_val

    with col_input_right:
        st.markdown("<p style='font-size: 0.95rem; font-weight: 700; color: #ffffff; margin-bottom: 0.25rem;'>2. Target Job Description</p>", unsafe_allow_html=True)
        st.caption("Paste the requirements, responsibilities, and qualifications:")
        jd_text_val = st.text_area(
            "Job Description",
            value=st.session_state.job_description,
            height=325,
            placeholder="Paste the target job description here (Role Overview, Key Responsibilities, Required Qualifications, Domain Competencies)...",
            label_visibility="collapsed"
        )
        st.session_state.job_description = jd_text_val

    # Screening Action Button
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        screen_clicked = st.button("Evaluate Candidate Fit", use_container_width=True)

    if screen_clicked:
        if not st.session_state.resume_text.strip():
            st.error("Please provide a resume by uploading a file or pasting text.")
        elif not st.session_state.job_description.strip():
            st.error("Please provide a target job description to evaluate against.")
        else:
            with st.spinner("Analyzing candidate alignment, extracting requirements, and evaluating ATS fit..."):
                time.sleep(0.4)
                analysis_res = nlp_engine.analyze_resume_vs_jd(
                    resume_text=st.session_state.resume_text,
                    jd_text=st.session_state.job_description,
                    candidate_name_override=cand_name_input
                )
                cand_id = database.save_candidate_screening(analysis_res)
                analysis_res["id"] = cand_id
                st.session_state.current_result = analysis_res

    # ==========================================
    # DISPLAY SCREENING RESULTS
    # ==========================================
    res = st.session_state.current_result
    if res:
        st.markdown("---")

        overall_sc = res["overall_score"]
        match_lvl = res["match_level"]
        cand_name = res["name"]
        t_role = res["target_role"]

        # 1. TOP SCORE SUMMARY CARD
        col_hero_left, col_hero_right = st.columns([3, 2])

        with col_hero_left:
            st.markdown(f"""
            <div class="score-banner-card">
                <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.65rem;">
                    <span style="background: rgba(99, 102, 241, 0.15); color: #c7d2fe; font-size: 0.75rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 4px;">
                        Screening Result
                    </span>
                    <span style="background: rgba(16, 185, 129, 0.15); color: #6ee7b7; font-size: 0.75rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 4px;">
                        {match_lvl}
                    </span>
                </div>
                <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin: 0 0 0.2rem 0; letter-spacing: -0.02em;">
                    {cand_name} <span style="color: #64748b; font-weight: 400;">•</span> <span style="color: #a5b4fc; font-size: 1.3rem;">{t_role}</span>
                </h2>
                <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 1.25rem;">
                    Evaluated across semantic context relevance, hard requirement coverage, and communication metrics.
                </p>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem;">
                    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 0.6rem; padding: 0.75rem;">
                        <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 500;">Matched Keywords</div>
                        <div style="font-size: 1.2rem; font-weight: 800; color: #34d399;">{len(res['matched_skills'])} <span style="font-size: 0.75rem; font-weight: 400; color: #94a3b8;">found</span></div>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 0.6rem; padding: 0.75rem;">
                        <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 500;">Missing Gaps</div>
                        <div style="font-size: 1.2rem; font-weight: 800; color: #fbbf24;">{len(res['missing_skills'])} <span style="font-size: 0.75rem; font-weight: 400; color: #94a3b8;">unmet</span></div>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 0.6rem; padding: 0.75rem;">
                        <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 500;">ATS Readability</div>
                        <div style="font-size: 1.05rem; font-weight: 800; color: #c084fc;">{'High' if overall_sc >= 80 else ('Moderate' if overall_sc >= 60 else 'Needs Revision')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_hero_right:
            st.markdown(f"""
            <div class="score-banner-card" style="display: flex; align-items: center; justify-content: center;">
                {render_circular_gauge(overall_sc, match_lvl)}
            </div>
            """, unsafe_allow_html=True)

        # 2. FOUR PILLARS SUB-SCORE BREAKDOWN
        st.markdown("<p style='font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 0.75rem;'>Evaluation Breakdown by Category</p>", unsafe_allow_html=True)
        
        def get_sub_status(sc):
            if sc >= 80: return "Strong Fit", "#34d399", "rgba(16, 185, 129, 0.15)"
            if sc >= 60: return "Moderate", "#818cf8", "rgba(99, 102, 241, 0.15)"
            return "Needs Growth", "#fb7185", "rgba(244, 63, 94, 0.15)"

        c_sc1, c_sc2, c_sc3, c_sc4 = st.columns(4)

        with c_sc1:
            lbl, col, bg = get_sub_status(res["job_fit_score"])
            st.markdown(f"""
            <div class="submetric-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">Role Scope Fit</span>
                    <span style="font-size: 0.65rem; font-weight: 700; color: {col}; background: {bg}; padding: 0.15rem 0.45rem; border-radius: 4px;">{lbl}</span>
                </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #ffffff; margin-bottom: 0.4rem;">{res["job_fit_score"]}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(res["job_fit_score"] / 100.0)
            st.caption("Alignment with core responsibilities")

        with c_sc2:
            lbl, col, bg = get_sub_status(res["technical_score"])
            st.markdown(f"""
            <div class="submetric-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">Qualifications</span>
                    <span style="font-size: 0.65rem; font-weight: 700; color: {col}; background: {bg}; padding: 0.15rem 0.45rem; border-radius: 4px;">{lbl}</span>
                </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #ffffff; margin-bottom: 0.4rem;">{res["technical_score"]}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(res["technical_score"] / 100.0)
            st.caption("Required domain skills & tools")

        with c_sc3:
            lbl, col, bg = get_sub_status(res["cultural_score"])
            st.markdown(f"""
            <div class="submetric-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">Workplace & Team</span>
                    <span style="font-size: 0.65rem; font-weight: 700; color: {col}; background: {bg}; padding: 0.15rem 0.45rem; border-radius: 4px;">{lbl}</span>
                </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #ffffff; margin-bottom: 0.4rem;">{res["cultural_score"]}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(res["cultural_score"] / 100.0)
            st.caption("Leadership, teamwork & initiative")

        with c_sc4:
            lbl, col, bg = get_sub_status(res["communication_score"])
            st.markdown(f"""
            <div class="submetric-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">Impact & Clarity</span>
                    <span style="font-size: 0.65rem; font-weight: 700; color: {col}; background: {bg}; padding: 0.15rem 0.45rem; border-radius: 4px;">{lbl}</span>
                </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #ffffff; margin-bottom: 0.4rem;">{res["communication_score"]}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(res["communication_score"] / 100.0)
            st.caption("Measurable achievements & action verbs")

        # 3. STRENGTHS & GROWTH AREAS (2 COLUMNS)
        st.markdown("<br>", unsafe_allow_html=True)
        col_str, col_grw = st.columns(2)

        with col_str:
            st.markdown("""
            <div class="saas-card">
                <p style="font-size: 0.95rem; font-weight: 700; color: #34d399; margin-bottom: 0.85rem;">
                    Key Strengths & Matched Qualifications
                </p>
            """, unsafe_allow_html=True)
            
            for s in res.get("strengths", []):
                st.markdown(f"• **{s['title']}:** {s['desc']}")
            
            if res.get("matched_skills"):
                st.markdown("<br><p style='font-size: 0.75rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.35rem;'>Matched Target Keywords:</p>", unsafe_allow_html=True)
                matched_html = "".join([f"<span class='pill-matched'>✓ {sk}</span>" for sk in res.get("matched_skills", [])[:12]])
                st.markdown(matched_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_grw:
            st.markdown("""
            <div class="saas-card">
                <p style="font-size: 0.95rem; font-weight: 700; color: #fbbf24; margin-bottom: 0.85rem;">
                    Missing Keywords & Growth Areas
                </p>
            """, unsafe_allow_html=True)
            
            for w in res.get("weaknesses", []):
                st.markdown(f"• **{w['title']}:** {w['desc']}")
            
            if res.get("missing_skills"):
                st.markdown("<br><p style='font-size: 0.75rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.35rem;'>Recommended Keywords to Add:</p>", unsafe_allow_html=True)
                missing_html = "".join([f"<span class='pill-missing'>+ {sk}</span>" for sk in res.get("missing_skills", [])[:12]])
                st.markdown(missing_html, unsafe_allow_html=True)
            else:
                st.success("Strong coverage! No critical skill gaps identified.")
            st.markdown("</div>", unsafe_allow_html=True)

        # 4. COLLAPSIBLE DETAILED AUDIT
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 0.5rem;'>Detailed ATS Audit & Optimization Advice</p>", unsafe_allow_html=True)

        with st.expander("1. Mathematical Calculation & Semantic Vector Analysis", expanded=True):
            det = res.get("detailed_analysis", {})
            st.info(det.get("score_explanation", ""))
            
            c_d1, c_d2, c_d3, c_d4 = st.columns(4)
            c_d1.metric("Contextual Relevance", f"{det.get('semantic_similarity_pct', 0)}%")
            c_d2.metric("Requirement Coverage", f"{det.get('skill_coverage_pct', 0)}%")
            c_d3.metric("Action Verbs Detected", f"{det.get('action_verb_count', 0)}")
            c_d4.metric("Quantifiable Metrics", f"{det.get('metrics_found_count', 0)}")

        with st.expander("2. ATS Compliance & Formatting Checklist"):
            for item in res.get("ats_recommendations", []):
                st.markdown(f"**[{item['impact']} Priority] {item['category']}:** {item['recommendation']}")

        with st.expander("3. Recommended Credentials & Project Roadmap"):
            det = res.get("detailed_analysis", {})
            st.markdown("#### Recommended Industry Certifications:")
            for c in det.get("recommended_certifications", []):
                st.markdown(f"- **{c}**")
            
            st.markdown("#### Recommended Project / Experience Highlights:")
            for p in det.get("recommended_projects", []):
                st.markdown(f"- {p}")

        with st.expander("4. High-Impact Bullet Point Rewriter (X-Y-Z Method)"):
            st.markdown("""
            **Example 1: Project & Operations**
            - *Standard wording:* Handled daily team tasks and coordinated with different departments.
            - **Optimized wording:** "Orchestrated cross-departmental operations across **15+ team members**, reducing project turnaround time by **28%**."

            **Example 2: Client & Quality Impact**
            - *Standard wording:* Responded to client inquiries and resolved issues.
            - **Optimized wording:** "Managed high-priority client relationships, boosting customer satisfaction ratings to **96%** with a **99% on-time resolution rate**."
            """)

        # Download Report Section
        st.markdown("<br>", unsafe_allow_html=True)
        report_text = f"""==================================================
RESUMEIQ SCREENING & ATS AUDIT REPORT
==================================================
Candidate: {res['name']}
Target Position: {res['target_role']}
Overall Match Score: {res['overall_score']}% ({res['match_level']})

EVALUATION BREAKDOWN:
- Role Scope Fit: {res['job_fit_score']}%
- Key Qualifications: {res['technical_score']}%
- Workplace & Team Alignment: {res['cultural_score']}%
- Impact & Presentation: {res['communication_score']}%

MATCHED REQUIREMENTS:
{', '.join(res['matched_skills'])}

MISSING KEYWORDS / GAPS:
{', '.join(res['missing_skills'])}

KEY STRENGTHS:
""" + "\n".join([f"- {s['title']}: {s['desc']}" for s in res.get('strengths', [])]) + """

AREAS FOR GROWTH:
""" + "\n".join([f"- {w['title']}: {w['desc']}" for w in res.get('weaknesses', [])]) + """

ATS RECOMMENDATIONS:
""" + "\n".join([f"- [{r['impact']}] {r['category']}: {r['recommendation']}" for r in res.get('ats_recommendations', [])])

        st.download_button(
            label="Download Full ATS Screening Report (.TXT)",
            data=report_text,
            file_name=f"resumeiq_report_{res['name'].replace(' ', '_').lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ==========================================
# TAB 2: RECRUITER PIPELINE BOARD
# ==========================================
with tab_recruiter:
    st.markdown("<p style='font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-bottom: 0.25rem;'>Candidate Pipeline Database</p>", unsafe_allow_html=True)
    st.caption("Review, filter, and export candidate evaluations stored in the persistent database.")

    candidates = database.get_candidates()

    if not candidates:
        st.info("No candidates evaluated yet. Run a screening to save records.")
    else:
        tot = len(candidates)
        strong = len([c for c in candidates if c["overall_score"] >= 80])
        avg = round(sum([c["overall_score"] for c in candidates]) / tot) if tot else 0

        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("Total Screened", tot)
        c_m2.metric("High Match (80%+)", strong)
        c_m3.metric("Average Score", f"{avg}%")

        st.markdown("---")

        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
        with f_col1:
            search_query = st.text_input("Search by Name or Role", "")
        with f_col2:
            min_score_sel = st.selectbox("Score Threshold", ["All Candidates", "80%+ (Strong Match)", "60%+ (Moderate Alignment)"])
        with f_col3:
            sort_sel = st.selectbox("Sort Order", ["Score: High to Low", "Date: Newest First"])

        filtered_candidates = candidates
        if search_query:
            filtered_candidates = [c for c in filtered_candidates if search_query.lower() in c["name"].lower() or search_query.lower() in c["target_role"].lower()]
        if min_score_sel == "80%+ (Strong Match)":
            filtered_candidates = [c for c in filtered_candidates if c["overall_score"] >= 80]
        elif min_score_sel == "60%+ (Moderate Alignment)":
            filtered_candidates = [c for c in filtered_candidates if c["overall_score"] >= 60]

        if sort_sel == "Score: High to Low":
            filtered_candidates.sort(key=lambda x: x["overall_score"], reverse=True)
        else:
            filtered_candidates.sort(key=lambda x: x["created_at"], reverse=True)

        table_data = []
        for c in filtered_candidates:
            table_data.append({
                "ID": c["id"],
                "Candidate Name": c["name"],
                "Target Role": c["target_role"],
                "Overall Match": f"{c['overall_score']}%",
                "Status": c["match_level"],
                "Scope Fit": f"{c['job_fit_score']}%",
                "Qualifications": f"{c['technical_score']}%",
                "Workplace Fit": f"{c['cultural_score']}%",
                "Clarity": f"{c['communication_score']}%",
                "Evaluation Date": c["created_at"][:10] if c.get("created_at") else "N/A"
            })

        df_candidates = pd.DataFrame(table_data)
        st.dataframe(df_candidates, use_container_width=True, hide_index=True)

        csv_data = df_candidates.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export Pipeline to CSV",
            data=csv_data,
            file_name=f"resumeiq_pipeline_{datetime.utcnow().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# ==========================================
# TAB 3: MULTI-CANDIDATE BENCHMARK
# ==========================================
with tab_compare:
    st.markdown("<p style='font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-bottom: 0.25rem;'>Candidate Comparison & Benchmarking</p>", unsafe_allow_html=True)
    st.caption("Evaluate 2 candidate resumes side-by-side against a single job description.")

    comp_jd = st.text_area("Target Job Description", height=120, placeholder="Paste the job description here...")

    col_cmp1, col_cmp2 = st.columns(2)
    with col_cmp1:
        st.markdown("<p style='font-size: 0.85rem; font-weight: 600; color: #cbd5e1;'>Candidate A</p>", unsafe_allow_html=True)
        c1_name = st.text_input("Name A", "Candidate A")
        c1_resume = st.text_area("Resume A Content", height=180, placeholder="Paste Candidate A resume text...")

    with col_cmp2:
        st.markdown("<p style='font-size: 0.85rem; font-weight: 600; color: #cbd5e1;'>Candidate B</p>", unsafe_allow_html=True)
        c2_name = st.text_input("Name B", "Candidate B")
        c2_resume = st.text_area("Resume B Content", height=180, placeholder="Paste Candidate B resume text...")

    if st.button("Run Side-by-Side Comparison", use_container_width=True):
        if not comp_jd.strip() or not c1_resume.strip() or not c2_resume.strip():
            st.error("Please provide the Job Description and both candidate resumes to compare.")
        else:
            r1 = nlp_engine.analyze_resume_vs_jd(c1_resume, comp_jd, candidate_name_override=c1_name)
            r2 = nlp_engine.analyze_resume_vs_jd(c2_resume, comp_jd, candidate_name_override=c2_name)

            winner = r1 if r1["overall_score"] >= r2["overall_score"] else r2

            st.markdown(f"""
            <div style="text-align: center; margin: 1.5rem 0; padding: 1rem; border-radius: 0.75rem; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.25);">
                <span style="font-weight: 800; font-size: 1.15rem; color: #34d399;">Top Alignment: {winner['name']} ({winner['overall_score']}%)</span>
            </div>
            """, unsafe_allow_html=True)

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.markdown(f"""
                <div class="saas-card">
                    <h3 style="margin: 0 0 0.25rem 0;">{r1['name']}</h3>
                    <p style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 0.75rem;">{r1['target_role']}</p>
                    <h1 style="color: #818cf8; font-size: 2.25rem; font-weight: 800; margin: 0 0 0.5rem 0;">{r1['overall_score']}%</h1>
                    <p style="font-size: 0.85rem;"><strong>Scope Fit:</strong> {r1['job_fit_score']}% | <strong>Qualifications:</strong> {r1['technical_score']}%</p>
                    <p style="font-size: 0.8rem; color: #94a3b8;"><strong>Matched Keywords:</strong> {', '.join(r1['matched_skills'][:6])}</p>
                </div>
                """, unsafe_allow_html=True)

            with col_r2:
                st.markdown(f"""
                <div class="saas-card">
                    <h3 style="margin: 0 0 0.25rem 0;">{r2['name']}</h3>
                    <p style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 0.75rem;">{r2['target_role']}</p>
                    <h1 style="color: #818cf8; font-size: 2.25rem; font-weight: 800; margin: 0 0 0.5rem 0;">{r2['overall_score']}%</h1>
                    <p style="font-size: 0.85rem;"><strong>Scope Fit:</strong> {r2['job_fit_score']}% | <strong>Qualifications:</strong> {r2['technical_score']}%</p>
                    <p style="font-size: 0.8rem; color: #94a3b8;"><strong>Matched Keywords:</strong> {', '.join(r2['matched_skills'][:6])}</p>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 4: AI CAREER COACH CHATBOT
# ==========================================
with tab_coach:
    st.markdown("<p style='font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-bottom: 0.25rem;'>Career Advisor & Optimization Coach</p>", unsafe_allow_html=True)
    st.caption("Personalized coaching tailored to candidate qualifications and target role expectations.")

    st.markdown("<p style='font-size: 0.8rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.35rem;'>Suggested Prompts:</p>", unsafe_allow_html=True)
    qp_cols = st.columns(4)
    if qp_cols[0].button("Improve match score to 90%+"):
        user_query = "How can I improve my match score to 90%+?"
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        reply = nlp_engine.generate_ai_chat_response(
            user_query,
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.current_result
        )
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})

    if qp_cols[1].button("Missing key requirements"):
        user_query = "What key skills or keywords should I add?"
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        reply = nlp_engine.generate_ai_chat_response(
            user_query,
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.current_result
        )
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})

    if qp_cols[2].button("Role fit assessment"):
        user_query = "Am I fit for this role?"
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        reply = nlp_engine.generate_ai_chat_response(
            user_query,
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.current_result
        )
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})

    if qp_cols[3].button("Bullet rewrites (X-Y-Z)"):
        user_query = "Rewrite bullet points with high-impact action verbs"
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        reply = nlp_engine.generate_ai_chat_response(
            user_query,
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.current_result
        )
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if chat_input := st.chat_input("Ask for resume wording, missing skills, or interview tips..."):
        st.session_state.chat_messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing candidate profile..."):
                reply = nlp_engine.generate_ai_chat_response(
                    chat_input,
                    st.session_state.resume_text,
                    st.session_state.job_description,
                    st.session_state.current_result
                )
                st.markdown(reply)
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
