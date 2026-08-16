import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "candidates.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            target_role TEXT,
            overall_score INTEGER NOT NULL,
            match_level TEXT NOT NULL,
            job_fit_score INTEGER NOT NULL,
            technical_score INTEGER NOT NULL,
            cultural_score INTEGER NOT NULL,
            communication_score INTEGER NOT NULL,
            matched_skills TEXT NOT NULL,
            missing_skills TEXT NOT NULL,
            all_candidate_skills TEXT NOT NULL,
            all_jd_skills TEXT NOT NULL,
            strengths TEXT NOT NULL,
            weaknesses TEXT NOT NULL,
            ats_recommendations TEXT NOT NULL,
            detailed_analysis TEXT NOT NULL,
            resume_text TEXT NOT NULL,
            job_description TEXT NOT NULL,
            filename TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_candidate_screening(data: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO candidates (
            name, email, phone, target_role,
            overall_score, match_level,
            job_fit_score, technical_score, cultural_score, communication_score,
            matched_skills, missing_skills, all_candidate_skills, all_jd_skills,
            strengths, weaknesses, ats_recommendations, detailed_analysis,
            resume_text, job_description, filename, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("name", "Anonymous Candidate"),
        data.get("email", ""),
        data.get("phone", ""),
        data.get("target_role", "Software Role"),
        data.get("overall_score", 0),
        data.get("match_level", "Moderate Match"),
        data.get("job_fit_score", 0),
        data.get("technical_score", 0),
        data.get("cultural_score", 0),
        data.get("communication_score", 0),
        json.dumps(data.get("matched_skills", [])),
        json.dumps(data.get("missing_skills", [])),
        json.dumps(data.get("all_candidate_skills", [])),
        json.dumps(data.get("all_jd_skills", [])),
        json.dumps(data.get("strengths", [])),
        json.dumps(data.get("weaknesses", [])),
        json.dumps(data.get("ats_recommendations", [])),
        json.dumps(data.get("detailed_analysis", {})),
        data.get("resume_text", ""),
        data.get("job_description", ""),
        data.get("filename", "resume.pdf"),
        created_at
    ))
    candidate_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return candidate_id

def get_candidates(
    search: Optional[str] = None,
    min_score: Optional[int] = None,
    skill_filter: Optional[str] = None,
    sort_by: str = "created_at",
    order: str = "desc"
) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM candidates WHERE 1=1"
    params = []
    
    if search:
        query += " AND (name LIKE ? OR target_role LIKE ? OR matched_skills LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])
        
    if min_score is not None:
        query += " AND overall_score >= ?"
        params.append(min_score)
        
    if skill_filter:
        query += " AND matched_skills LIKE ?"
        params.append(f"%{skill_filter}%")
        
    # Ordering
    sort_column = "overall_score" if sort_by == "score" else "created_at"
    sort_direction = "ASC" if order.lower() == "asc" else "DESC"
    query += f" ORDER BY {sort_column} {sort_direction}"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "phone": row["phone"],
            "target_role": row["target_role"],
            "overall_score": row["overall_score"],
            "match_level": row["match_level"],
            "job_fit_score": row["job_fit_score"],
            "technical_score": row["technical_score"],
            "cultural_score": row["cultural_score"],
            "communication_score": row["communication_score"],
            "matched_skills": json.loads(row["matched_skills"]),
            "missing_skills": json.loads(row["missing_skills"]),
            "strengths": json.loads(row["strengths"]),
            "weaknesses": json.loads(row["weaknesses"]),
            "ats_recommendations": json.loads(row["ats_recommendations"]),
            "detailed_analysis": json.loads(row["detailed_analysis"]),
            "filename": row["filename"],
            "created_at": row["created_at"]
        })
    
    conn.close()
    return results

def get_candidate_by_id(candidate_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "phone": row["phone"],
        "target_role": row["target_role"],
        "overall_score": row["overall_score"],
        "match_level": row["match_level"],
        "job_fit_score": row["job_fit_score"],
        "technical_score": row["technical_score"],
        "cultural_score": row["cultural_score"],
        "communication_score": row["communication_score"],
        "matched_skills": json.loads(row["matched_skills"]),
        "missing_skills": json.loads(row["missing_skills"]),
        "all_candidate_skills": json.loads(row["all_candidate_skills"]),
        "all_jd_skills": json.loads(row["all_jd_skills"]),
        "strengths": json.loads(row["strengths"]),
        "weaknesses": json.loads(row["weaknesses"]),
        "ats_recommendations": json.loads(row["ats_recommendations"]),
        "detailed_analysis": json.loads(row["detailed_analysis"]),
        "resume_text": row["resume_text"],
        "job_description": row["job_description"],
        "filename": row["filename"],
        "created_at": row["created_at"]
    }

def delete_candidate(candidate_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
