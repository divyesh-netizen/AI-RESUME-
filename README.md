# ⚡ ResumeIQ — Modern AI Resume Screening & Match Scoring SaaS (Streamlit & React)

A production-ready, full-stack **AI-powered Resume Screening & Match Scoring SaaS Web App** built with Python, Streamlit, and FastAPI + React.

---

## 🌟 Key Features

### 1. 📊 Intelligent AI Match Scoring
- **Top Score Gauge**: Large animated circular SVG progress ring with dynamic match ratings (*Strong Match / Moderate / Weak Match*).
- **Sub-Score Breakdown**: 4 hiring pillars with animated progress bars & rating chips:
  - **Job Fit %** (Role scope, responsibilities & years of experience alignment)
  - **Technical Skills %** (Coverage against required tech stack & tools)
  - **Cultural Fit %** (Agile, teamwork, leadership & ownership indicators)
  - **Communication %** (Quantifiable metrics density & active action verbs)

### 2. 📋 Strengths & Areas for Growth (2-Column Grid)
- **✅ Strengths**: Highlights verified technical proficiencies, data-backed metrics, and action verbs.
- **⚠️ Areas for Growth**: Callouts of missing high-priority skills, passive language warnings, and ATS keyword gaps.

### 3. 📑 Comprehensive Collapsible ATS Audit
- **Mathematical Explanation**: TF-IDF cosine relevance & skill taxonomy coverage.
- **ATS Compliance Checklist**: Formatting recommendations and impact indicators.
- **Career Roadmap**: Suggested industry certifications (e.g. AWS, CKA, Scrum Master) & standout portfolio projects.
- **Interactive Bullet Point Rewriter**: Before vs. After X-Y-Z formula examples.

### 4. 🤖 Context-Aware AI Career Coach (Chatbot Mode)
- Real-time conversational assistant grounded in candidate resume and target job description.
- 1-Click Quick Prompts (*"How to reach 90%+?"*, *"What skills to add?"*, *"Am I fit for this role?"*, *"Rewrite my resume bullets"*).

### 5. 👥 Recruiter Pipeline Dashboard
- Persistent SQLite candidate database storing all past screenings.
- Search by candidate name or target role.
- Filter by minimum match score (80%+, 60%+, All) and skills.
- Sort by score (High to Low) or date (Newest first).
- 1-Click **Export to CSV**.

### 6. ⚖️ Multi-Candidate Benchmark & Comparison
- Side-by-side comparison of 2 applicants against the same job description with winner ranking.

### 7. 📄 ATS Screening Report Download (.TXT / Printable)
- Full ATS score report download with detailed breakdowns.

---

## 🚀 How to Run on Streamlit (Recommended)

### 1-Click Launch:
Double-click `run_streamlit.bat` in the project root, or execute:

```bash
python -m streamlit run app.py --server.port 8501
```

Open your browser at: **[http://localhost:8501](http://localhost:8501)**

---

## 🌐 How to Run the React + FastAPI Version

### 1-Click Launch:
Double-click `start.bat` in the project root:
- **Frontend (Vite React)**: `http://localhost:5173`
- **Backend (FastAPI)**: `http://127.0.0.1:8000` (Swagger UI at `/docs`)

---

## 🛠️ Architecture & Tech Stack

- **UI Framework**: Streamlit (Python) with custom SaaS dark theme, glassmorphic cards, and SVG gauges.
- **AI & NLP Engine**: Scikit-learn (TF-IDF Vectorizer + Cosine Similarity), 500+ Skill Taxonomy, `pypdf`, `python-docx`.
- **Database**: SQLite (`backend/candidates.db`).
