import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "candidates.db")
JSON_BACKUP_PATH = os.path.join(DB_DIR, "candidates_store.json")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def _sync_to_json_backup():
    """Sync current database rows to JSON backup file for extreme resilience."""
    try:
        candidates = _raw_get_all_candidates()
        with open(JSON_BACKUP_PATH, "w", encoding="utf-8") as f:
            json.dump(candidates, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error syncing JSON backup: {e}")

def _sync_from_json_backup_if_needed():
    """Restore from JSON backup if SQLite is empty but backup has rows."""
    try:
        if not os.path.exists(JSON_BACKUP_PATH):
            return
        with open(JSON_BACKUP_PATH, "r", encoding="utf-8") as f:
            backup_data = json.load(f)
        if not backup_data:
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM candidates")
        count = cursor.fetchone()[0]

        if count == 0 and len(backup_data) > 0:
            for item in backup_data:
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
                    item.get("name", "Anonymous Candidate"),
                    item.get("email", ""),
                    item.get("phone", ""),
                    item.get("target_role", "Professional Role"),
                    item.get("overall_score", 0),
                    item.get("match_level", "Moderate Match"),
                    item.get("job_fit_score", 0),
                    item.get("technical_score", 0),
                    item.get("cultural_score", 0),
                    item.get("communication_score", 0),
                    json.dumps(item.get("matched_skills", [])),
                    json.dumps(item.get("missing_skills", [])),
                    json.dumps(item.get("all_candidate_skills", [])),
                    json.dumps(item.get("all_jd_skills", [])),
                    json.dumps(item.get("strengths", [])),
                    json.dumps(item.get("weaknesses", [])),
                    json.dumps(item.get("ats_recommendations", [])),
                    json.dumps(item.get("detailed_analysis", {})),
                    item.get("resume_text", ""),
                    item.get("job_description", ""),
                    item.get("filename", "resume.pdf"),
                    item.get("created_at", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
                ))
            conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error restoring from JSON backup: {e}")

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
    _sync_from_json_backup_if_needed()

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
        data.get("target_role", "Professional Role"),
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
    
    _sync_to_json_backup()
    return candidate_id

def _raw_get_all_candidates() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates ORDER BY id DESC")
    rows = cursor.fetchall()
    
    results = []
    for row in rows:
        item = dict(row)
        for field in ["matched_skills", "missing_skills", "all_candidate_skills", "all_jd_skills", "strengths", "weaknesses", "ats_recommendations", "detailed_analysis"]:
            if item.get(field):
                try:
                    item[field] = json.loads(item[field])
                except (json.JSONDecodeError, TypeError):
                    pass
        results.append(item)
    conn.close()
    return results

def get_candidates(
    search: Optional[str] = None,
    min_score: Optional[int] = None,
    skill_filter: Optional[str] = None,
    sort_by: str = "created_at",
    order: str = "desc"
) -> List[Dict[str, Any]]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM candidates WHERE 1=1"
        params = []
        
        if search:
            query += " AND (name LIKE ? OR target_role LIKE ? OR resume_text LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term])
            
        if min_score is not None:
            query += " AND overall_score >= ?"
            params.append(min_score)
            
        allowed_sort = {
            "created_at": "created_at",
            "overall_score": "overall_score",
            "name": "name",
            "job_fit_score": "job_fit_score",
            "technical_score": "technical_score"
        }
        sort_column = allowed_sort.get(sort_by, "id")
        sort_order = "DESC" if order.lower() == "desc" else "ASC"
        
        query += f" ORDER BY {sort_column} {sort_order}"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        candidates = []
        for row in rows:
            cand = dict(row)
            for field in ["matched_skills", "missing_skills", "all_candidate_skills", "all_jd_skills", "strengths", "weaknesses", "ats_recommendations", "detailed_analysis"]:
                if cand.get(field):
                    try:
                        cand[field] = json.loads(cand[field])
                    except (json.JSONDecodeError, TypeError):
                        pass
            if skill_filter and skill_filter.lower() not in [s.lower() for s in cand.get("matched_skills", [])]:
                continue
            candidates.append(cand)
            
        conn.close()
        return candidates
    except Exception as e:
        print(f"Error fetching candidates: {e}")
        if os.path.exists(JSON_BACKUP_PATH):
            try:
                with open(JSON_BACKUP_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

def get_candidate_by_id(candidate_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    cand = dict(row)
    for field in ["matched_skills", "missing_skills", "all_candidate_skills", "all_jd_skills", "strengths", "weaknesses", "ats_recommendations", "detailed_analysis"]:
        if cand.get(field):
            try:
                cand[field] = json.loads(cand[field])
            except (json.JSONDecodeError, TypeError):
                pass
    return cand

def get_database_stats() -> Dict[str, Any]:
    candidates = get_candidates()
    total = len(candidates)
    if total == 0:
        return {
            "total_screened": 0,
            "avg_overall_score": 0,
            "strong_matches": 0,
            "moderate_matches": 0,
            "weak_matches": 0
        }
    return {
        "total_screened": total,
        "avg_overall_score": round(sum(c["overall_score"] for c in candidates) / total),
        "strong_matches": len([c for c in candidates if c["overall_score"] >= 80]),
        "moderate_matches": len([c for c in candidates if 60 <= c["overall_score"] < 80]),
        "weak_matches": len([c for c in candidates if c["overall_score"] < 60])
    }
