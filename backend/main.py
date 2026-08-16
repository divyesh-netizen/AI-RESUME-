import os
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import database
import nlp_engine
import sample_data

# Initialize database schema
database.init_db()

app = FastAPI(
    title="ResumeIQ / ScreenAI API",
    description="Modern AI-Powered Resume Screening & Match Scoring Engine",
    version="1.0.0"
)

# Enable CORS for frontend local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Request Models
class TextScreenRequest(BaseModel):
    resume_text: str
    job_description: str
    candidate_name: Optional[str] = None
    save_to_db: bool = True

class ChatRequest(BaseModel):
    message: str
    resume_text: Optional[str] = ""
    job_description: Optional[str] = ""
    screening_data: Optional[dict] = None
    api_key: Optional[str] = None

class CompareRequest(BaseModel):
    job_description: str
    candidates: List[dict] # List of { "name": str, "resume_text": str }

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "ResumeIQ / ScreenAI Backend",
        "version": "1.0.0"
    }

@app.get("/api/sample-data")
def get_sample_data():
    """Retrieve preloaded sample resumes and job descriptions."""
    return sample_data.SAMPLE_DATA

@app.post("/api/seed-samples")
def seed_sample_candidates():
    """Seed initial sample candidates into the database for immediate recruiter pipeline view."""
    created_ids = []
    for key, item in sample_data.SAMPLE_DATA.items():
        analysis = nlp_engine.analyze_resume_vs_jd(
            resume_text=item["resume"],
            jd_text=item["job_description"],
            candidate_name_override=item["candidate_name"],
            filename=f"{item['candidate_name'].replace(' ', '_').lower()}_resume.pdf"
        )
        c_id = database.save_candidate_screening(analysis)
        created_ids.append(c_id)
    return {"message": f"Successfully seeded {len(created_ids)} candidates", "candidate_ids": created_ids}

@app.post("/api/screen")
async def screen_resume(
    resume_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None),
    job_description: str = Form(...),
    candidate_name: Optional[str] = Form(None),
    save_to_db: bool = Form(True)
):
    """
    Main screening endpoint. Accepts file upload (PDF/DOCX/TXT) or raw resume text,
    matches against the provided job description, calculates hybrid scores, and returns analysis.
    """
    extracted_text = ""
    filename = "resume.txt"
    
    if resume_file:
        filename = resume_file.filename or "uploaded_resume.pdf"
        contents = await resume_file.read()
        extracted_text = nlp_engine.extract_text_from_file(contents, filename)
    elif resume_text:
        extracted_text = resume_text.strip()
        filename = "pasted_resume.txt"
    else:
        raise HTTPException(status_code=400, detail="Please provide either a resume file or pasted resume text.")
        
    if not extracted_text:
        raise HTTPException(status_code=400, detail="Could not extract readable text from the provided resume.")
        
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
        
    # Analyze Resume vs JD
    result = nlp_engine.analyze_resume_vs_jd(
        resume_text=extracted_text,
        jd_text=job_description.strip(),
        candidate_name_override=candidate_name,
        filename=filename
    )
    
    # Save to SQLite Database if enabled
    candidate_id = None
    if save_to_db:
        candidate_id = database.save_candidate_screening(result)
        result["id"] = candidate_id
        
    return {
        "success": True,
        "candidate_id": candidate_id,
        "data": result
    }

@app.post("/api/screen-text")
def screen_resume_text(payload: TextScreenRequest):
    """Screen raw text payload (useful for JSON-only API requests)."""
    if not payload.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required.")
    if not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")
        
    result = nlp_engine.analyze_resume_vs_jd(
        resume_text=payload.resume_text.strip(),
        jd_text=payload.job_description.strip(),
        candidate_name_override=payload.candidate_name,
        filename="resume.txt"
    )
    
    candidate_id = None
    if payload.save_to_db:
        candidate_id = database.save_candidate_screening(result)
        result["id"] = candidate_id
        
    return {
        "success": True,
        "candidate_id": candidate_id,
        "data": result
    }

@app.post("/api/chat")
def chat_with_ai(payload: ChatRequest):
    """
    AI Career & Resume Coach endpoint. Answers user questions grounded in the parsed resume and JD.
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
        
    reply = nlp_engine.generate_ai_chat_response(
        user_query=payload.message,
        resume_text=payload.resume_text or "",
        jd_text=payload.job_description or "",
        screening_data=payload.screening_data,
        api_key=payload.api_key
    )
    
    return {
        "success": True,
        "reply": reply
    }

@app.get("/api/candidates")
def list_candidates(
    search: Optional[str] = Query(None),
    min_score: Optional[int] = Query(None),
    skill: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    order: str = Query("desc")
):
    """Retrieve screened candidates list for recruiter pipeline."""
    candidates = database.get_candidates(
        search=search,
        min_score=min_score,
        skill_filter=skill,
        sort_by=sort_by,
        order=order
    )
    return {
        "total": len(candidates),
        "candidates": candidates
    }

@app.get("/api/candidates/{candidate_id}")
def get_candidate(candidate_id: int):
    """Retrieve full screening report for a specific candidate."""
    candidate = database.get_candidate_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate screening record not found.")
    return candidate

@app.delete("/api/candidates/{candidate_id}")
def remove_candidate(candidate_id: int):
    """Delete a candidate screening record."""
    success = database.delete_candidate(candidate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Candidate not found or already removed.")
    return {"success": True, "message": f"Candidate {candidate_id} deleted successfully."}

@app.post("/api/compare")
def compare_candidates(payload: CompareRequest):
    """
    Compare multiple candidate resumes against a single job description side-by-side.
    """
    if not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")
    if not payload.candidates or len(payload.candidates) < 2:
        raise HTTPException(status_code=400, detail="Please provide at least 2 candidates to compare.")
        
    comparisons = []
    for cand in payload.candidates:
        name = cand.get("name", "Applicant")
        resume = cand.get("resume_text", "")
        analysis = nlp_engine.analyze_resume_vs_jd(
            resume_text=resume,
            jd_text=payload.job_description,
            candidate_name_override=name
        )
        comparisons.append(analysis)
        
    # Sort candidates by overall score descending
    comparisons.sort(key=lambda x: x["overall_score"], reverse=True)
    
    return {
        "success": True,
        "job_description_snippet": payload.job_description[:200] + "...",
        "comparisons": comparisons
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
