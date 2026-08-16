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
import sample_data

# Initialize Database Schema
database.init_db()

# Configure Streamlit Page
st.set_page_config(
    page_title="ResumeIQ — AI Resume Screening & Match Scoring",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium SaaS Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main background */
    .stApp {
        background-color: #030712;
        color: #f8fafc;
    }

    /* Top banner glow */
    .hero-container {
        text-align: center;
        padding: 1.5rem 1rem 2rem 1rem;
        background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.18) 0%, rgba(3, 7, 18, 0) 70%);
        border-radius: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #a5b4fc;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.15;
        background: linear-gradient(135deg, #ffffff 30%, #c7d2fe 70%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
        max-width: 650px;
        margin: 0 auto;
        line-height: 1.5;
    }

    /* Glassmorphism Card Panels */
    .glass-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 1.25rem;
        padding: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        margin-bottom: 1rem;
    }

    .score-hero-card {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 1.5rem;
        padding: 2rem;
        box-shadow: 0 20px 40px -15px rgba(99, 102, 241, 0.2);
        margin-bottom: 1.5rem;
    }

    /* Metric progress sub-card */
    .metric-subcard {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 1rem;
        padding: 1.15rem;
        transition: all 0.2s ease;
    }
    .metric-subcard:hover {
        border-color: rgba(99, 102, 241, 0.3);
        transform: translateY(-2px);
    }

    /* Custom skill badges */
    .skill-badge-matched {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 0.5rem;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(16, 185, 129, 0.15);
        color: #6ee7b7;
        border: 1px solid rgba(16, 185, 129, 0.3);
        margin: 0.2rem;
    }

    .skill-badge-missing {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 0.5rem;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(245, 158, 11, 0.15);
        color: #fcd34d;
        border: 1px solid rgba(245, 158, 11, 0.3);
        margin: 0.2rem;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 0.75rem !important;
        border: none !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5) !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Input text areas */
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0.75rem !important;
        color: #f8fafc !important;
        font-size: 0.85rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = sample_data.SAMPLE_DATA["frontend_dev"]["resume"]
if "job_description" not in st.session_state:
    st.session_state.job_description = sample_data.SAMPLE_DATA["frontend_dev"]["job_description"]
if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = sample_data.SAMPLE_DATA["frontend_dev"]["candidate_name"]
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": """### 👋 Hi there! I'm your AI Resume & Career Coach.
I have evaluated your profile against the target job description. You can ask me:
- **"How can I boost my score to 90%+?"**
- **"What skills should I add?"**
- **"Am I a strong fit for this role?"**
- **"Rewrite my work experience bullet points"**
- **"What certifications or projects should I pursue?"**"""
        }
    ]

# Helper function to load sample profile
def load_sample_role(role_key):
    if role_key in sample_data.SAMPLE_DATA:
        sample = sample_data.SAMPLE_DATA[role_key]
        st.session_state.resume_text = sample["resume"]
        st.session_state.job_description = sample["job_description"]
        st.session_state.candidate_name = sample["candidate_name"]

# Helper to render SVG circular gauge
def render_circular_gauge(score, label):
    is_strong = score >= 80
    is_moderate = score >= 60 and score < 80
    stroke_color = "#10b981" if is_strong else ("#6366f1" if is_moderate else "#f43f5e")
    badge_bg = "rgba(16, 185, 129, 0.15)" if is_strong else ("rgba(99, 102, 241, 0.15)" if is_moderate else "rgba(244, 63, 94, 0.15)")
    badge_color = "#34d399" if is_strong else ("#818cf8" if is_moderate else "#fb7185")
    
    radius = 58
    circumference = 2 * 3.14159 * radius
    offset = circumference - (score / 100.0) * circumference

    svg_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
        <div style="position: relative; width: 170px; height: 170px;">
            <svg style="transform: rotate(-90deg); width: 100%; height: 100%;" viewBox="0 0 140 140">
                <circle cx="70" cy="70" r="{radius}" stroke="rgba(255,255,255,0.08)" stroke-width="12" fill="transparent" />
                <circle cx="70" cy="70" r="{radius}" stroke="{stroke_color}" stroke-width="12" stroke-linecap="round"
                        stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" fill="transparent"
                        style="transition: stroke-dashoffset 1s ease-in-out;" />
            </svg>
            <div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <span style="font-size: 2.25rem; font-weight: 800; color: #ffffff; line-height: 1;">{score}%</span>
                <span style="font-size: 0.75rem; font-weight: 700; color: {badge_color}; text-transform: uppercase; margin-top: 4px;">{label}</span>
            </div>
        </div>
        <span style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.5rem; font-weight: 500;">Hybrid AI Match Index</span>
    </div>
    """
    return svg_html

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
        <div style="width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #4f46e5, #7c3aed); display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">
            ⚡
        </div>
        <div>
            <div style="font-weight: 800; font-size: 1.1rem; color: #ffffff;">ResumeIQ</div>
            <div style="font-size: 0.7rem; color: #818cf8; font-weight: 600; text-transform: uppercase;">AI SaaS Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 1-Click Demo Profiles")
    st.caption("Instantly test with high-fidelity real-world resumes:")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("⚡ Frontend Dev", use_container_width=True):
            load_sample_role("frontend_dev")
            st.rerun()
    with col_s2:
        if st.button("💻 Full Stack", use_container_width=True):
            load_sample_role("fullstack_dev")
            st.rerun()

    if st.button("🧠 AI / ML Engineer", use_container_width=True):
        load_sample_role("ai_engineer")
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Pipeline Summary")
    candidates_in_db = database.get_candidates()
    st.metric("Total Screened Candidates", len(candidates_in_db))
    strong_matches = len([c for c in candidates_in_db if c["overall_score"] >= 80])
    st.metric("Strong Matches (80%+)", f"{strong_matches} / {len(candidates_in_db)}")

    st.markdown("---")
    st.caption("⚡ Powered by TF-IDF Semantic Embeddings & 500+ Skills Taxonomy Engine.")

# ==========================================
# MAIN HERO HEADER
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⚡ Hybrid TF-IDF + 500+ Skills Taxonomy Engine</div>
    <div class="hero-title">Screen Resumes in Seconds with AI Precision</div>
    <div class="hero-subtitle">Upload any resume (PDF, DOCX, TXT) and job description to get instant match scores, skills gap breakdown, ATS optimization suggestions, and personalized AI coaching.</div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_screen, tab_recruiter, tab_compare, tab_coach = st.tabs([
    "⚡ Screen & Score",
    "👥 Recruiter Pipeline",
    "⚖️ Compare Candidates",
    "🤖 AI Career Coach"
])

# ==========================================
# TAB 1: SCREEN & SCORE
# ==========================================
with tab_screen:
    col_input_left, col_input_right = st.columns(2)

    with col_input_left:
        st.markdown("#### 1. Candidate Resume")
        cand_name_input = st.text_input("Candidate Name (Optional)", value=st.session_state.candidate_name, placeholder="e.g. Alex Morgan")
        
        upload_choice = st.radio("Input Format:", ["Paste Text", "Upload File (.PDF / .DOCX / .TXT)"], horizontal=True)
        
        if upload_choice == "Upload File (.PDF / .DOCX / .TXT)":
            uploaded_file = st.file_uploader("Drop resume file here", type=["pdf", "docx", "doc", "txt"])
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                extracted = nlp_engine.extract_text_from_file(file_bytes, uploaded_file.name)
                st.session_state.resume_text = extracted
                st.success(f"✅ Extracted {len(extracted.split())} words from {uploaded_file.name}")
        else:
            resume_text_val = st.text_area(
                "Resume Content",
                value=st.session_state.resume_text,
                height=260,
                placeholder="Paste full resume text here..."
            )
            st.session_state.resume_text = resume_text_val

    with col_input_right:
        st.markdown("#### 2. Target Job Description")
        st.caption("Paste the requirements, responsibilities & required tech stack:")
        jd_text_val = st.text_area(
            "Job Description",
            value=st.session_state.job_description,
            height=325,
            placeholder="Paste target job description here..."
        )
        st.session_state.job_description = jd_text_val

    # Screening Action Button
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        screen_clicked = st.button("🚀 Screen Resume with AI", use_container_width=True)

    if screen_clicked:
        if not st.session_state.resume_text.strip():
            st.error("Please provide resume text or upload a resume file.")
        elif not st.session_state.job_description.strip():
            st.error("Please provide a job description to screen against.")
        else:
            with st.spinner("Analyzing semantics, extracting keywords & computing ATS score..."):
                time.sleep(0.5)
                analysis_res = nlp_engine.analyze_resume_vs_jd(
                    resume_text=st.session_state.resume_text,
                    jd_text=st.session_state.job_description,
                    candidate_name_override=cand_name_input
                )
                cand_id = database.save_candidate_screening(analysis_res)
                analysis_res["id"] = cand_id
                st.session_state.current_result = analysis_res

                if analysis_res["overall_score"] >= 80:
                    st.balloons()

    # ==========================================
    # DISPLAY SCREENING RESULTS
    # ==========================================
    res = st.session_state.current_result
    if res:
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)

        # 1. TOP SCORE HERO CARD
        overall_sc = res["overall_score"]
        match_lvl = res["match_level"]
        cand_name = res["name"]
        t_role = res["target_role"]

        col_hero_left, col_hero_right = st.columns([3, 2])

        with col_hero_left:
            st.markdown(f"""
            <div class="score-hero-card">
                <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.75rem;">
                    <span style="background: rgba(99, 102, 241, 0.2); color: #c7d2fe; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.65rem; border-radius: 9999px; text-transform: uppercase;">
                        AI Match Result
                    </span>
                    <span style="background: rgba(16, 185, 129, 0.2); color: #6ee7b7; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.65rem; border-radius: 9999px;">
                        {match_lvl}
                    </span>
                </div>
                <h2 style="font-size: 1.85rem; font-weight: 800; color: #ffffff; margin: 0 0 0.25rem 0;">
                    {cand_name} <span style="color: #64748b; font-weight: 400;">•</span> <span style="color: #a5b4fc; font-size: 1.4rem;">{t_role}</span>
                </h2>
                <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 1.25rem;">
                    Evaluated with TF-IDF cosine similarity, n-gram vectorization, and 500+ skill taxonomy coverage.
                </p>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem;">
                    <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 0.75rem; padding: 0.75rem;">
                        <div style="font-size: 0.7rem; color: #94a3b8;">Matched Skills</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #34d399;">{len(res['matched_skills'])} <span style="font-size: 0.75rem; font-weight: 400; color: #94a3b8;">skills</span></div>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 0.75rem; padding: 0.75rem;">
                        <div style="font-size: 0.7rem; color: #94a3b8;">Missing Gaps</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #fbbf24;">{len(res['missing_skills'])} <span style="font-size: 0.75rem; font-weight: 400; color: #94a3b8;">gaps</span></div>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 0.75rem; padding: 0.75rem;">
                        <div style="font-size: 0.7rem; color: #94a3b8;">ATS Readiness</div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: #c084fc;">{'High' if overall_sc >= 80 else ('Medium' if overall_sc >= 60 else 'Needs Work')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_hero_right:
            st.markdown(f"""
            <div class="score-hero-card" style="display: flex; align-items: center; justify-content: center;">
                {render_circular_gauge(overall_sc, match_lvl)}
            </div>
            """, unsafe_allow_html=True)

        # 2. FOUR SUB-SCORE BREAKDOWN CARDS
        st.markdown("### 📊 Four Pillars Performance Breakdown")
        
        def get_sub_status(sc):
            if sc >= 80: return "Excellent", "#34d399", "rgba(16, 185, 129, 0.2)"
            if sc >= 60: return "Good", "#818cf8", "rgba(99, 102, 241, 0.2)"
            return "Needs Improvement", "#fb7185", "rgba(244, 63, 94, 0.2)"

        c_sc1, c_sc2, c_sc3, c_sc4 = st.columns(4)

        with c_sc1:
            lbl, col, bg = get_sub_status(res["job_fit_score"])
            st.markdown(f"""
            <div class="metric-subcard">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">Job Fit</span>
                    <span style="font-size: 0.7rem; font-weight: 700; color: {col}; background: {bg}; padding: 0.15rem 0.5rem; border-radius: 9999px;">{lbl}</span>
                </div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 0.5rem;">{res["job_fit_score"]}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(res["job_fit_score"] / 100.0)
            st.caption("Role scope & responsibilities alignment")

        with c_sc2:
            lbl, col, bg = get_sub_status(res["technical_score"])
            st.markdown(f"""
            <div class="metric-subcard">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">Technical Skills</span>
                    <span style="font-size: 0.7rem; font-weight: 700; color: {col}; background: {bg}; padding: 0.15rem 0.5rem; border-radius: 9999px;">{lbl}</span>
                </div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 0.5rem;">{res["technical_score"]}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(res["technical_score"] / 100.0)
            st.caption("Required tech stack coverage")

        with c_sc3:
            lbl, col, bg = get_sub_status(res["cultural_score"])
            st.markdown(f"""
            <div class="metric-subcard">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">Cultural Fit</span>
                    <span style="font-size: 0.7rem; font-weight: 700; color: {col}; background: {bg}; padding: 0.15rem 0.5rem; border-radius: 9999px;">{lbl}</span>
                </div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 0.5rem;">{res["cultural_score"]}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(res["cultural_score"] / 100.0)
            st.caption("Agile, teamwork & leadership cues")

        with c_sc4:
            lbl, col, bg = get_sub_status(res["communication_score"])
            st.markdown(f"""
            <div class="metric-subcard">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">Communication</span>
                    <span style="font-size: 0.7rem; font-weight: 700; color: {col}; background: {bg}; padding: 0.15rem 0.5rem; border-radius: 9999px;">{lbl}</span>
                </div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 0.5rem;">{res["communication_score"]}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(res["communication_score"] / 100.0)
            st.caption("Action verbs & quantifiable metrics")

        # 3. STRENGTHS & AREAS FOR GROWTH (2-COLUMN GRID)
        st.markdown("<br>", unsafe_allow_html=True)
        col_str, col_grw = st.columns(2)

        with col_str:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #34d399; font-weight: 800; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                    ✅ Key Strengths & Highlights
                </h4>
            """, unsafe_allow_html=True)
            
            for s in res.get("strengths", []):
                st.markdown(f"• **{s['title']}:** {s['desc']}")
            
            st.markdown("<br><strong style='font-size: 0.8rem; color: #94a3b8;'>Verified Tech Skills:</strong><br>", unsafe_allow_html=True)
            matched_html = "".join([f"<span class='skill-badge-matched'>✓ {sk}</span>" for sk in res.get("matched_skills", [])[:10]])
            st.markdown(matched_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_grw:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #fbbf24; font-weight: 800; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                    ⚠️ Areas for Growth & Missing Skills
                </h4>
            """, unsafe_allow_html=True)
            
            for w in res.get("weaknesses", []):
                st.markdown(f"• **{w['title']}:** {w['desc']}")
            
            if res.get("missing_skills"):
                st.markdown("<br><strong style='font-size: 0.8rem; color: #94a3b8;'>Recommended Keywords to Add:</strong><br>", unsafe_allow_html=True)
                missing_html = "".join([f"<span class='skill-badge-missing'>+ {sk}</span>" for sk in res.get("missing_skills", [])[:10]])
                st.markdown(missing_html, unsafe_allow_html=True)
            else:
                st.success("🎉 No major technical keyword gaps detected!")
            st.markdown("</div>", unsafe_allow_html=True)

        # 4. COLLAPSIBLE DETAILED ANALYSIS
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📑 Detailed ATS Compliance & Career Roadmap")

        with st.expander("🔍 1. Mathematical Score Calculation & Semantic Vector Analysis", expanded=True):
            det = res.get("detailed_analysis", {})
            st.info(det.get("score_explanation", ""))
            
            c_d1, c_d2, c_d3, c_d4 = st.columns(4)
            c_d1.metric("TF-IDF Vector Relevance", f"{det.get('semantic_similarity_pct', 0)}%")
            c_d2.metric("Skill Coverage Ratio", f"{det.get('skill_coverage_pct', 0)}%")
            c_d3.metric("Action Verbs Used", f"{det.get('action_verb_count', 0)} verbs")
            c_d4.metric("Quantifiable Metrics", f"{det.get('metrics_found_count', 0)} data points")

        with st.expander("📋 2. Priority ATS Optimization Checklist"):
            for item in res.get("ats_recommendations", []):
                st.markdown(f"**[{item['impact']} Impact] {item['category']}:** {item['recommendation']}")

        with st.expander("🏆 3. Recommended Certifications & Projects Roadmap"):
            det = res.get("detailed_analysis", {})
            st.markdown("#### Recommended Industry Certifications:")
            for c in det.get("recommended_certifications", []):
                st.markdown(f"- 🎖️ **{c}**")
            
            st.markdown("#### Standout Portfolio Projects to Build:")
            for p in det.get("recommended_projects", []):
                st.markdown(f"- 🚀 {p}")

        with st.expander("✍️ 4. High-Impact Bullet Point Rewriter (X-Y-Z Method)"):
            st.markdown("""
            **Example 1: Frontend & Performance**
            - ❌ *Standard:* Worked on the frontend UI and fixed performance issues.
            - ✅ **Optimized:** "Spearheaded frontend re-architecture using **React** and **Tailwind CSS**, reducing initial page load time by **42%** and boosting Lighthouse performance score to 98."

            **Example 2: Backend & Database**
            - ❌ *Standard:* Built APIs and managed databases.
            - ✅ **Optimized:** "Engineered scalable **FastAPI** REST endpoints integrated with **PostgreSQL**, cutting database query response times by **35%** for 50k+ active users."
            """)

        # Download Report Section
        st.markdown("<br>", unsafe_allow_html=True)
        report_text = f"""==================================================
RESUMEIQ AI SCREENING REPORT
==================================================
Candidate: {res['name']}
Target Role: {res['target_role']}
Overall Match Score: {res['overall_score']}% ({res['match_level']})

FOUR PILLARS BREAKDOWN:
- Job Fit: {res['job_fit_score']}%
- Technical Skills: {res['technical_score']}%
- Cultural Fit: {res['cultural_score']}%
- Communication: {res['communication_score']}%

MATCHED SKILLS:
{', '.join(res['matched_skills'])}

MISSING SKILLS / KEYWORD GAPS:
{', '.join(res['missing_skills'])}

KEY STRENGTHS:
""" + "\n".join([f"- {s['title']}: {s['desc']}" for s in res.get('strengths', [])]) + """

AREAS FOR GROWTH:
""" + "\n".join([f"- {w['title']}: {w['desc']}" for w in res.get('weaknesses', [])]) + """

ATS RECOMMENDATIONS:
""" + "\n".join([f"- [{r['impact']}] {r['category']}: {r['recommendation']}" for r in res.get('ats_recommendations', [])])

        st.download_button(
            label="📥 Download Full ATS Screening Report (.TXT)",
            data=report_text,
            file_name=f"resumeiq_report_{res['name'].replace(' ', '_').lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ==========================================
# TAB 2: RECRUITER PIPELINE BOARD
# ==========================================
with tab_recruiter:
    st.markdown("### 👥 Recruiter Pipeline Database")
    st.caption("Browse, filter, sort, and export candidate screening records stored in SQLite.")

    candidates = database.get_candidates()

    if not candidates:
        st.info("No candidates in the database yet. Run a screening to save candidate records.")
    else:
        # Top Stats
        tot = len(candidates)
        strong = len([c for c in candidates if c["overall_score"] >= 80])
        avg = round(sum([c["overall_score"] for c in candidates]) / tot) if tot else 0

        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("Total Screened", tot)
        c_m2.metric("Strong Candidates (80%+)", strong)
        c_m3.metric("Average Score", f"{avg}%")

        st.markdown("---")

        # Filters
        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
        with f_col1:
            search_query = st.text_input("🔍 Search Name or Role", "")
        with f_col2:
            min_score_sel = st.selectbox("Filter by Score", ["All", "80%+ (Strong)", "60%+ (Moderate)"])
        with f_col3:
            sort_sel = st.selectbox("Sort By", ["Score (High to Low)", "Date (Newest First)"])

        # Filter logic
        filtered_candidates = candidates
        if search_query:
            filtered_candidates = [c for c in filtered_candidates if search_query.lower() in c["name"].lower() or search_query.lower() in c["target_role"].lower()]
        if min_score_sel == "80%+ (Strong)":
            filtered_candidates = [c for c in filtered_candidates if c["overall_score"] >= 80]
        elif min_score_sel == "60%+ (Moderate)":
            filtered_candidates = [c for c in filtered_candidates if c["overall_score"] >= 60]

        if sort_sel == "Score (High to Low)":
            filtered_candidates.sort(key=lambda x: x["overall_score"], reverse=True)
        else:
            filtered_candidates.sort(key=lambda x: x["created_at"], reverse=True)

        # Render Table as DataFrame
        table_data = []
        for c in filtered_candidates:
            table_data.append({
                "ID": c["id"],
                "Candidate Name": c["name"],
                "Target Role": c["target_role"],
                "Overall Score": f"{c['overall_score']}%",
                "Match Level": c["match_level"],
                "Job Fit": f"{c['job_fit_score']}%",
                "Tech Fit": f"{c['technical_score']}%",
                "Cultural": f"{c['cultural_score']}%",
                "Comm": f"{c['communication_score']}%",
                "Date": c["created_at"][:10] if c.get("created_at") else "N/A"
            })

        df_candidates = pd.DataFrame(table_data)
        st.dataframe(df_candidates, use_container_width=True, hide_index=True)

        # CSV Export Button
        csv_data = df_candidates.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Export Candidates to CSV",
            data=csv_data,
            file_name=f"resumeiq_pipeline_{datetime.utcnow().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# ==========================================
# TAB 3: MULTI-CANDIDATE BENCHMARK
# ==========================================
with tab_compare:
    st.markdown("### ⚖️ Multi-Candidate Benchmark & Comparison")
    st.caption("Compare 2 applicants side-by-side against the same job description.")

    col_cmp1, col_cmp2 = st.columns(2)
    with col_cmp1:
        c1_key = st.selectbox("Select Candidate 1", list(sample_data.SAMPLE_DATA.keys()), index=0)
    with col_cmp2:
        c2_key = st.selectbox("Select Candidate 2", list(sample_data.SAMPLE_DATA.keys()), index=1)

    if st.button("🔥 Run Side-by-Side Comparison", use_container_width=True):
        c1 = sample_data.SAMPLE_DATA[c1_key]
        c2 = sample_data.SAMPLE_DATA[c2_key]
        target_jd = c1["job_description"]

        r1 = nlp_engine.analyze_resume_vs_jd(c1["resume"], target_jd, candidate_name_override=c1["candidate_name"])
        r2 = nlp_engine.analyze_resume_vs_jd(c2["resume"], target_jd, candidate_name_override=c2["candidate_name"])

        winner = r1 if r1["overall_score"] >= r2["overall_score"] else r2

        st.markdown(f"""
        <div style="text-align: center; margin: 1.5rem 0; padding: 1rem; border-radius: 1rem; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3);">
            <span style="font-size: 1.5rem;">🏆</span>
            <span style="font-weight: 800; font-size: 1.2rem; color: #34d399; margin-left: 0.5rem;">Top Match: {winner['name']} ({winner['overall_score']}%)</span>
        </div>
        """, unsafe_allow_html=True)

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown(f"""
            <div class="glass-card">
                <h3>{r1['name']}</h3>
                <p style="color: #94a3b8; font-size: 0.85rem;">{r1['target_role']}</p>
                <h1 style="color: #818cf8; font-size: 2.5rem; font-weight: 800;">{r1['overall_score']}%</h1>
                <p><strong>Job Fit:</strong> {r1['job_fit_score']}% | <strong>Tech:</strong> {r1['technical_score']}%</p>
                <p><strong>Matched Skills:</strong> {', '.join(r1['matched_skills'][:5])}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_r2:
            st.markdown(f"""
            <div class="glass-card">
                <h3>{r2['name']}</h3>
                <p style="color: #94a3b8; font-size: 0.85rem;">{r2['target_role']}</p>
                <h1 style="color: #818cf8; font-size: 2.5rem; font-weight: 800;">{r2['overall_score']}%</h1>
                <p><strong>Job Fit:</strong> {r2['job_fit_score']}% | <strong>Tech:</strong> {r2['technical_score']}%</p>
                <p><strong>Matched Skills:</strong> {', '.join(r2['matched_skills'][:5])}</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 4: AI CAREER COACH CHATBOT
# ==========================================
with tab_coach:
    st.markdown("### 🤖 AI Career & Resume Coach")
    st.caption("Interactive advice tailored directly to the candidate's resume and target job requirements.")

    # Quick prompt buttons
    st.markdown("**Quick Prompts:**")
    qp_cols = st.columns(4)
    if qp_cols[0].button("🚀 How to get 90%+?"):
        user_query = "How can I improve my match score to 90%+?"
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        reply = nlp_engine.generate_ai_chat_response(
            user_query,
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.current_result
        )
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})

    if qp_cols[1].button("🛠️ What skills to add?"):
        user_query = "What skills should I add?"
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        reply = nlp_engine.generate_ai_chat_response(
            user_query,
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.current_result
        )
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})

    if qp_cols[2].button("📊 Am I a fit?"):
        user_query = "Am I fit for this role?"
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        reply = nlp_engine.generate_ai_chat_response(
            user_query,
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.current_result
        )
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})

    if qp_cols[3].button("✍️ Bullet point rewrites"):
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
    if chat_input := st.chat_input("Ask AI Coach for resume wording, missing skills, or interview tips..."):
        st.session_state.chat_messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)

        with st.chat_message("assistant"):
            with st.spinner("AI Coach is analyzing..."):
                reply = nlp_engine.generate_ai_chat_response(
                    chat_input,
                    st.session_state.resume_text,
                    st.session_state.job_description,
                    st.session_state.current_result
                )
                st.markdown(reply)
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
