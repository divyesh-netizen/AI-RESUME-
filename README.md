# 📄 ResumeIQ — Universal Resume Screening & Match Analysis

An intelligent, domain-agnostic resume screening and job fit evaluation tool. Evaluates candidate resumes against any target job description, highlights missing keywords, and provides actionable recommendations to optimize for ATS systems and hiring requirements.

🌐 **Live Web App:** [https://ln7dbyh8zbcvenqpt6jyvj.streamlit.app/](https://ln7dbyh8zbcvenqpt6jyvj.streamlit.app/)

---

## 🌟 Key Features

- **Universal Role Compatibility:** Works across all fields and professions — Healthcare, Business, Finance, Marketing, Education, Legal, Creative, Engineering, Operations, and Trades.
- **Match Score & Evaluation Breakdown:** Overall match index plus 4 categorical pillars:
  - *Role Scope Fit* (Responsibility alignment)
  - *Key Qualifications* (Hard & functional skills coverage)
  - *Workplace & Team Alignment* (Leadership, teamwork & initiative)
  - *Impact & Presentation* (Measurable metrics & active action verbs)
- **Keyword Gap Analysis:** Highlights matched requirements alongside missing keywords to add.
- **Actionable ATS Optimization:** Action verb analysis, quantifiable impact guidance, and concrete Before vs. After bullet point rewrites (X-Y-Z method).
- **Interactive Career Advisor:** Built-in AI coaching assistant tailored to your specific application.
- **Candidate Pipeline Database:** Saves screening history with sorting, filtering, and 1-click CSV export.
- **Multi-Candidate Benchmark:** Compare 2 candidate resumes side-by-side against a single job description.

## 🛠️ Architecture & Tech Stack

- **UI Framework**: Streamlit (Python) with custom SaaS dark theme, glassmorphic cards, and SVG gauges.
- **AI & NLP Engine**: Scikit-learn (TF-IDF Vectorizer + Cosine Similarity), 500+ Skill Taxonomy, `pypdf`, `python-docx`.
- **Database**: SQLite (`backend/candidates.db`).
