import re
import io
import math
from typing import Dict, List, Any, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# PDF and DOCX parsers
try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None

# Comprehensive Universal Skill Taxonomy spanning ALL Industries & Domains
UNIVERSAL_TAXONOMY = {
    "Business, Strategy & Management": [
        "strategic planning", "operations management", "budgeting", "financial modeling",
        "risk management", "stakeholder management", "project management", "p&l management",
        "vendor management", "supply chain", "logistics", "business analysis", "kpi tracking",
        "change management", "process optimization", "cost reduction", "lean six sigma",
        "procurement", "inventory management", "resource allocation", "cross-functional leadership"
    ],
    "Marketing, Sales & Growth": [
        "digital marketing", "seo", "sem", "content marketing", "social media marketing",
        "copywriting", "lead generation", "salesforce", "hubspot", "crm", "email marketing",
        "market research", "branding", "brand strategy", "b2b sales", "b2c sales", "cold calling",
        "account management", "client acquisition", "public relations", "conversion optimization",
        "google analytics", "campaign management", "product marketing", "growth marketing"
    ],
    "Finance, Accounting & Banking": [
        "financial analysis", "accounting", "quickbooks", "gaap", "ifrs", "auditing", "tax preparation",
        "forecasting", "portfolio management", "wealth management", "financial reporting", "compliance",
        "payroll", "accounts payable", "accounts receivable", "reconciliation", "excel modeling",
        "valuation", "treasury", "credit analysis", "risk assessment", "variance analysis"
    ],
    "Healthcare, Nursing & Life Sciences": [
        "patient care", "clinical research", "emr", "ehr", "hipaa", "triage", "pharmacology",
        "patient assessment", "vital signs", "medical terminology", "diagnostics", "healthcare administration",
        "phlebotomy", "bls", "acls", "cpr", "infection control", "patient advocacy", "treatment planning",
        "medical billing", "icu care", "nursing", "rehabilitation", "telehealth", "quality of care"
    ],
    "Education, Training & Research": [
        "curriculum development", "classroom management", "lesson planning", "instructional design",
        "educational technology", "student assessment", "academic advising", "mentorship",
        "e-learning", "qualitative research", "quantitative research", "data collection",
        "program evaluation", "student engagement", "pedagogy", "special education", "tutoring"
    ],
    "Design, Creative & Media": [
        "ui/ux design", "figma", "adobe creative suite", "photoshop", "illustrator", "indesign",
        "graphic design", "video editing", "premiere pro", "after effects", "typography", "wireframing",
        "prototyping", "user research", "usability testing", "brand identity", "storyboarding",
        "creative direction", "art direction", "photography", "visual design", "canva"
    ],
    "Human Resources & Legal": [
        "talent acquisition", "recruiting", "employee relations", "onboarding", "performance management",
        "labor laws", "contract negotiation", "legal research", "regulatory compliance",
        "benefits administration", "hris", "workday", "dispute resolution", "compensation planning",
        "policy development", "diversity & inclusion", "employee engagement", "contract drafting"
    ],
    "Customer Support & Client Services": [
        "customer service", "client relations", "conflict resolution", "zendesk", "intercom",
        "ticket management", "customer retention", "call center", "problem resolution",
        "customer satisfaction", "csat", "account management", "administrative support", "scheduling"
    ],
    "Technology, Data & Engineering": [
        "python", "sql", "data analysis", "machine learning", "excel", "power bi", "tableau",
        "software development", "javascript", "react", "cloud computing", "aws", "azure", "docker",
        "system design", "database management", "automation", "api integration", "quality assurance",
        "cad", "autocad", "solidworks", "technical writing", "it support", "cybersecurity"
    ],
    "Universal Core Competencies": [
        "leadership", "team leadership", "communication", "written communication", "verbal communication",
        "problem solving", "critical thinking", "collaboration", "teamwork", "time management",
        "organization", "adaptability", "multitasking", "decision making", "attention to detail",
        "negotiation", "presentation skills", "work ethic", "active listening", "customer focus"
    ]
}

# Action verbs across all professions indicating high impact
ACTION_VERBS = [
    "spearheaded", "orchestrated", "developed", "implemented", "managed", "designed",
    "built", "optimized", "increased", "reduced", "improved", "led", "directed", "supervised",
    "automated", "streamlined", "accelerated", "delivered", "executed", "collaborated",
    "mentored", "revamped", "transformed", "established", "launched", "negotiated",
    "administered", "achieved", "exceeded", "generated", "coordinated", "resolved", "trained"
]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract clean text from PDF using pypdf."""
    text = ""
    if pypdf:
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"pypdf extraction error: {e}")
    if not text:
        try:
            text = file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            text = ""
    return text.strip()

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract clean text from DOCX using python-docx."""
    text = []
    if docx:
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            for para in doc.paragraphs:
                if para.text:
                    text.append(para.text)
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text:
                            text.append(cell.text)
        except Exception as e:
            print(f"docx extraction error: {e}")
    return "\n".join(text).strip()

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract text based on file format."""
    ext = filename.lower().split(".")[-1]
    if ext == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext in ["docx", "doc"]:
        return extract_text_from_docx(file_bytes)
    else:
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1", errors="ignore")

def extract_candidate_info(text: str) -> Dict[str, str]:
    """Extract candidate name, email, and phone heuristics."""
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    email = email_match.group(0) if email_match else ""
    
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    phone = phone_match.group(0) if phone_match else ""
    
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    name = "Candidate"
    for line in lines[:5]:
        clean = re.sub(r'[^a-zA-Z\s]', '', line).strip()
        words = clean.split()
        if 2 <= len(words) <= 4 and not any(w.lower() in ["resume", "curriculum", "vitae", "cv", "experience", "education", "profile", "contact", "summary"] for w in words):
            name = " ".join([w.capitalize() for w in words])
            break
            
    return {"name": name, "email": email, "phone": phone}

def extract_domain_keywords_from_jd(jd_text: str, top_n: int = 25) -> List[str]:
    """
    Dynamically extract domain keywords & requirements from ANY Job Description
    using TF-IDF n-grams + regex noun phrase heuristics.
    Works for any industry (Healthcare, Legal, Marketing, Teaching, Culinary, Trades, Tech, etc.).
    """
    if not jd_text.strip():
        return []
    
    # 1. Match from Universal Taxonomy
    matched_from_tax = set()
    lower_jd = " " + jd_text.lower() + " "
    
    for cat, skills in UNIVERSAL_TAXONOMY.items():
        for skill in skills:
            pattern = rf'\b{re.escape(skill)}\b'
            if re.search(pattern, lower_jd):
                matched_from_tax.add(skill.title())
                
    # 2. Dynamic TF-IDF keyphrase extraction for niche domain words
    try:
        tfidf = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=50,
            token_pattern=r'(?u)\b[a-zA-Z][a-zA-Z0-9_\-\+]{2,}\b'
        )
        tfidf.fit([jd_text])
        feature_names = tfidf.get_feature_names_out()
        
        # Exclude common generic filler words
        blacklist = {"experience", "responsibilities", "requirements", "candidate", "role", "work", "job", "ability", "skills", "knowledge", "including", "must", "years", "environment", "team", "strong", "preferred", "duties", "qualifications", "working", "looking"}
        for f in feature_names:
            if f.lower() not in blacklist and len(f) > 3:
                matched_from_tax.add(f.title())
    except Exception:
        pass
        
    return sorted(list(matched_from_tax))[:top_n]

def extract_matched_and_missing_skills(resume_text: str, jd_text: str) -> Tuple[List[str], List[str]]:
    """
    Compare resume text against extracted JD keywords universally.
    """
    jd_keywords = extract_domain_keywords_from_jd(jd_text)
    lower_resume = " " + resume_text.lower() + " "
    
    matched = []
    missing = []
    
    for kw in jd_keywords:
        pattern = rf'\b{re.escape(kw.lower())}\b'
        if re.search(pattern, lower_resume):
            matched.append(kw)
        else:
            missing.append(kw)
            
    return matched, missing

def compute_tf_idf_similarity(resume_text: str, jd_text: str) -> float:
    """Compute cosine similarity score between Resume and JD using TF-IDF."""
    if not resume_text.strip() or not jd_text.strip():
        return 0.0
        
    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 3),
            sublinear_tf=True,
            max_features=5000
        )
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        similarity = float(sim_matrix[0][0])
        return min(max(similarity, 0.0), 1.0)
    except Exception as e:
        print(f"TF-IDF similarity calculation error: {e}")
        return 0.5

def detect_role_domain(jd_text: str) -> str:
    """Detect candidate's target domain / job title from any JD."""
    role_match = re.search(r'(?:role|position|job title|looking for a|title:)\s*([A-Za-z0-9\s\/\-\+]+)', jd_text, re.IGNORECASE)
    if role_match:
        extracted = role_match.group(1).strip().split("\n")[0][:40]
        if len(extracted) > 3:
            return extracted.title()
            
    # Universal fallback detection across industries
    lower = jd_text.lower()
    if any(k in lower for k in ["nurse", "nursing", "patient", "clinical", "hospital", "healthcare"]):
        return "Healthcare Professional"
    elif any(k in lower for k in ["marketing", "seo", "social media", "brand", "campaign"]):
        return "Marketing Specialist"
    elif any(k in lower for k in ["accounting", "financial", "audit", "tax", "banking"]):
        return "Finance & Accounting Role"
    elif any(k in lower for k in ["teacher", "education", "curriculum", "instructional", "student"]):
        return "Education & Training Role"
    elif any(k in lower for k in ["designer", "ui/ux", "graphic design", "creative", "video editor"]):
        return "Design & Creative Role"
    elif any(k in lower for k in ["sales", "account executive", "client acquisition", "b2b"]):
        return "Sales & Business Development"
    elif any(k in lower for k in ["human resources", "recruiter", "talent acquisition", "hr"]):
        return "Human Resources Professional"
    elif any(k in lower for k in ["software", "developer", "engineer", "data scientist", "frontend", "backend"]):
        return "Engineering / Technical Role"
    elif any(k in lower for k in ["customer service", "support specialist", "client services"]):
        return "Customer Operations Role"
    elif any(k in lower for k in ["legal", "paralegal", "attorney", "contract", "counsel"]):
        return "Legal & Compliance Role"
    return "Target Professional Role"

def analyze_resume_vs_jd(resume_text: str, jd_text: str, candidate_name_override: Optional[str] = None, filename: str = "resume.pdf") -> Dict[str, Any]:
    """
    Universal hybrid screening algorithm applicable to ANY job domain and ANY resume.
    """
    info = extract_candidate_info(resume_text)
    candidate_name = candidate_name_override if candidate_name_override and candidate_name_override.strip() else info["name"]
    target_role = detect_role_domain(jd_text)
    
    # 1. Extract Matched & Missing Skills / Domain Keywords
    matched_skills, missing_skills = extract_matched_and_missing_skills(resume_text, jd_text)
    total_keywords = len(matched_skills) + len(missing_skills)
    skill_coverage_ratio = (len(matched_skills) / total_keywords) if total_keywords > 0 else 0.70
    
    # 2. Compute TF-IDF Semantic Relevance
    tfidf_sim = compute_tf_idf_similarity(resume_text, jd_text)
    
    # 3. Analyze Action Verbs & Measurable Metrics
    lower_resume = resume_text.lower()
    action_verb_count = sum(1 for verb in ACTION_VERBS if re.search(rf'\b{verb}\b', lower_resume))
    action_verb_score = min(action_verb_count / 7.0, 1.0)
    
    metrics_count = len(re.findall(r'(\d+[\.,]?\d*[%kKmMBb$]|\$\d+|\b\d{2,}\b)', resume_text))
    metrics_score = min(metrics_count / 5.0, 1.0)
    
    # 4. Soft Skills & Collaboration indicators
    soft_indicators = ["leadership", "collaboration", "communication", "problem solving", "organization", "adaptability", "teamwork", "planning", "initiative"]
    soft_matches = sum(1 for s in soft_indicators if s in lower_resume)
    cultural_ratio = min(soft_matches / 4.0, 1.0)
    
    # 5. Calculate 4 Universal Sub-Scores (0 - 100)
    job_fit_score = int(np.clip((tfidf_sim * 0.50 + skill_coverage_ratio * 0.50) * 100 + 15, 25, 98))
    technical_score = int(np.clip((skill_coverage_ratio * 0.75 + tfidf_sim * 0.25) * 100 + 10, 25, 99))
    cultural_score = int(np.clip((cultural_ratio * 0.60 + tfidf_sim * 0.40) * 100 + 20, 30, 96))
    communication_score = int(np.clip((action_verb_score * 0.45 + metrics_score * 0.40 + 0.15) * 100, 30, 97))
    
    # Composite Overall Score
    raw_overall = (job_fit_score * 0.35 + technical_score * 0.35 + cultural_score * 0.15 + communication_score * 0.15)
    overall_score = int(np.clip(raw_overall, 20, 99))
    
    if overall_score >= 80:
        match_level = "Strong Match"
    elif overall_score >= 60:
        match_level = "Moderate Match"
    else:
        match_level = "Weak Match"
        
    def get_status(score: int) -> str:
        if score >= 80: return "Excellent"
        if score >= 60: return "Good"
        return "Needs Improvement"
        
    # 6. Universal Strengths
    strengths = []
    if matched_skills:
        top_skills = ", ".join(matched_skills[:4])
        strengths.append({
            "title": "Strong Core Qualification Alignment",
            "desc": f"Demonstrated background and proficiency in key target requirements: {top_skills}."
        })
    if metrics_count >= 3:
        strengths.append({
            "title": "Measurable Results & Data Points",
            "desc": f"Includes {metrics_count}+ quantifiable achievements illustrating concrete business/operational value."
        })
    if action_verb_count >= 4:
        strengths.append({
            "title": "Proactive Action Verbs",
            "desc": f"Utilizes {action_verb_count}+ active accomplishment verbs to showcase ownership and leadership."
        })
    if len(strengths) < 3:
        strengths.append({
            "title": "Clear Career Trajectory",
            "desc": "Logical progression of responsibilities aligned with standard industry qualifications."
        })
        
    # 7. Universal Areas for Growth
    weaknesses = []
    if missing_skills:
        top_missing = ", ".join(missing_skills[:4])
        weaknesses.append({
            "title": "Key Requirement Gaps",
            "desc": f"The job description emphasizes {top_missing}, which are not clearly highlighted in the resume."
        })
    if metrics_count < 3:
        weaknesses.append({
            "title": "Substantiate Achievements with Metrics",
            "desc": "Add more numerical metrics (e.g., % growth, revenue, volume handled, team size, cost savings) to quantify impact."
        })
    if action_verb_count < 4:
        weaknesses.append({
            "title": "Dynamic Wording Needed",
            "desc": "Replace passive phrases ('responsible for', 'worked on') with powerful impact verbs ('spearheaded', 'orchestrated', 'streamlined')."
        })
    if len(weaknesses) == 0:
        weaknesses.append({
            "title": "Continuous Professional Expansion",
            "desc": "Consider showcasing advanced domain credentials, leadership milestones, or specialized methodologies."
        })
        
    # 8. ATS Recommendations
    ats_recommendations = [
        {
            "category": "Keyword Optimization",
            "recommendation": f"Incorporate target job keywords ({', '.join(missing_skills[:3]) if missing_skills else 'core competencies'}) directly into your experience bullet points.",
            "impact": "High"
        },
        {
            "category": "Quantifiable Proof (X-Y-Z Formula)",
            "recommendation": "Structure bullet points as: 'Accomplished [X] as measured by [Y], by doing [Z]'.",
            "impact": "High"
        },
        {
            "category": "ATS Section Headers",
            "recommendation": "Use clean, standard headings like 'Professional Experience', 'Core Competencies / Skills', and 'Education'.",
            "impact": "Medium"
        },
        {
            "category": "Action Verbs",
            "recommendation": "Begin each work experience bullet point with an active verb showing direct initiative.",
            "impact": "Medium"
        }
    ]
    
    # 9. Detailed analysis
    detailed_analysis = {
        "score_explanation": f"The candidate achieved an overall match score of {overall_score}% ({match_level}). Functional qualification coverage is {int(skill_coverage_ratio * 100)}%, matching {len(matched_skills)} of {total_keywords} key job requirements. Semantic contextual relevance is {int(tfidf_sim * 100)}%.",
        "semantic_similarity_pct": int(tfidf_sim * 100),
        "skill_coverage_pct": int(skill_coverage_ratio * 100),
        "action_verb_count": action_verb_count,
        "metrics_found_count": metrics_count,
        "sub_score_ratings": {
            "job_fit": {"score": job_fit_score, "status": get_status(job_fit_score)},
            "technical": {"score": technical_score, "status": get_status(technical_score)},
            "cultural": {"score": cultural_score, "status": get_status(cultural_score)},
            "communication": {"score": communication_score, "status": get_status(communication_score)}
        },
        "recommended_certifications": [
            f"Industry-recognized Professional Certification in {target_role}",
            "Project Management / Agile Leadership Certification (e.g. PMP, Scrum, Lean)",
            "Advanced Domain Credential or Specialized Workshop"
        ],
        "recommended_projects": [
            f"Showcase a comprehensive end-to-end case study addressing {', '.join(missing_skills[:2]) if missing_skills else 'key industry challenges'}.",
            "Highlight a process improvement initiative resulting in measurable efficiency gains or cost reductions.",
            "Document a collaborative cross-functional project highlighting leadership and stakeholder management."
        ]
    }
    
    return {
        "name": candidate_name,
        "email": info["email"],
        "phone": info["phone"],
        "target_role": target_role,
        "overall_score": overall_score,
        "match_level": match_level,
        "job_fit_score": job_fit_score,
        "technical_score": technical_score,
        "cultural_score": cultural_score,
        "communication_score": communication_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "ats_recommendations": ats_recommendations,
        "detailed_analysis": detailed_analysis,
        "resume_text": resume_text,
        "job_description": jd_text,
        "filename": filename
    }

def generate_ai_chat_response(
    user_query: str,
    resume_text: str,
    jd_text: str,
    screening_data: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Generate conversational coaching response tailored to candidate's resume and target JD for ANY field.
    """
    query_lower = user_query.lower()
    
    if not screening_data and resume_text and jd_text:
        screening_data = analyze_resume_vs_jd(resume_text, jd_text)
        
    matched = screening_data.get("matched_skills", []) if screening_data else []
    missing = screening_data.get("missing_skills", []) if screening_data else []
    overall = screening_data.get("overall_score", 75) if screening_data else 75
    role = screening_data.get("target_role", "your target position") if screening_data else "the role"
    
    # 1. "How can I improve my resume / match score?"
    if any(k in query_lower for k in ["improve", "score", "higher", "better", "boost", "increase"]):
        missing_text = ", ".join(missing[:4]) if missing else "key role deliverables and specialized methodologies"
        return f"""### 🚀 Action Plan to Boost Your Match Score to 90%+

Here is your tailored strategy based on our gap analysis for **{role}**:

1. **Integrate High-Priority Missing Keywords:**
   - Incorporate direct experience or demonstrated competence with: **{missing_text}**.
   - Place these keywords in your *Core Competencies / Skills* section and naturally within your experience bullet points.

2. **Quantify Your Work with Measurable Impact:**
   - **Before:** "Responsible for managing projects and handling day-to-day operations."
   - **After:** "Spearheaded 8+ cross-functional initiatives, improving operational workflow efficiency by **32%** and saving **$45,000 annually**."

3. **Align Header & Role Terminology:**
   - Ensure your summary title directly reflects the target role (e.g., *'{role}'*).
   - Use standard ATS headings: *Professional Experience*, *Core Skills*, *Education*, *Certifications*.

4. **Highlight Leadership & Collaboration:**
   - Add bullet points on team mentoring, process optimization, and stakeholder communication."""

    # 2. "What skills should I add?"
    elif any(k in query_lower for k in ["skills", "missing", "technologies", "what should i learn", "keywords"]):
        if missing:
            items = "\n".join([f"- **{skill}**: High priority in the job description. Highlight relevant coursework, past experience, or projects." for skill in missing[:6]])
            return f"""### 🛠️ Key Skills & Keywords to Highlight for {role}

To maximize your alignment with this position, ensure the following keywords from the job description appear prominently in your resume:

{items}

> **Tip:** If you have applied these competencies in past roles, volunteer work, or freelance projects, include them under **'Core Competencies'** or within bullet points!"""
        else:
            return f"Great news! Your resume already covers the core requirements identified in the job description ({', '.join(matched[:5])}). To further distinguish yourself, emphasize leadership achievements, quantifiable business results, and advanced domain certifications."

    # 3. "Am I a fit for this role?"
    elif any(k in query_lower for k in ["am i fit", "good fit", "chance", "qualify", "qualified", "fit for this"]):
        level = screening_data.get("match_level", "Moderate Match") if screening_data else "Moderate Match"
        return f"""### 📊 Role Fit Assessment: **{level} ({overall}%)**

**Summary Analysis:**
- **Core Strengths:** You have strong alignment on primary qualifications including **{', '.join(matched[:3]) if matched else 'foundational competencies'}**.
- **Primary Gaps:** The hiring team will likely evaluate your depth in **{', '.join(missing[:3]) if missing else 'specialized role responsibilities'}**.
- **Next Steps:** You are well-positioned for an initial review. Tailor your top 3 work experience bullet points to mirror the exact outcomes requested in the job description to maximize your interview callback rate."""

    # 4. "Rewrite bullet points / resume wording"
    elif any(k in query_lower for k in ["rewrite", "bullet", "bullet point", "wording", "phrasing", "action verb"]):
        return f"""### ✍️ High-Impact Bullet Point Rewrites (Universal X-Y-Z Method)

Here is how you can transform standard resume bullets into high-impact, recruiter-ready statements:

#### Example 1: Management & Operations
- ❌ *Standard:* Handled daily team tasks and coordinated with different departments.
- ✅ **Optimized:** "Orchestrated daily cross-departmental operations across **15+ team members**, reducing project delivery turnaround time by **28%**."

#### Example 2: Client & Customer Impact
- ❌ *Standard:* Responded to client inquiries and resolved issues.
- ✅ **Optimized:** "Managed high-priority client relationships, boosting customer satisfaction rating from 82% to **96%** while maintaining a **99% on-time resolution rate**."

#### Example 3: Strategy & Process Improvement
- ❌ *Standard:* Helped improve workflow and reduced errors.
- ✅ **Optimized:** "Spearheaded comprehensive workflow standardization that decreased operational errors by **40%** and reduced administrative costs by **$25,000**." """

    # Generic contextual AI response
    else:
        return f"""### 💡 AI Coach Insights for {role}

Regarding your question: *"{user_query}"*

- **Your Current Match Rating:** Overall Score is **{overall}%** with **{len(matched)} matched core requirements** ({', '.join(matched[:3]) if matched else 'relevant skills'}).
- **Recruiter Perspective:** Recruiters scan resumes in under 10 seconds. Position your strongest achievements and target keywords in the top third of your resume.
- **Key Focus:** Ensure the terms **{', '.join(missing[:3]) if missing else 'highlighted in the JD'}** appear prominently, and quantify your deliverables with concrete numbers, percentages, or milestones.

*Feel free to ask for specific bullet rewrites, interview preparation tips, or salary negotiation advice!*"""
