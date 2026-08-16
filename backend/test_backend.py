import database
import nlp_engine
import sample_data

def test():
    database.init_db()
    print("[1] Database initialized.")
    
    sample = sample_data.SAMPLE_DATA["frontend_dev"]
    res = nlp_engine.analyze_resume_vs_jd(
        resume_text=sample["resume"],
        jd_text=sample["job_description"],
        candidate_name_override=sample["candidate_name"]
    )
    print(f"[2] Screening Completed! Candidate: {res['name']}")
    print(f"    Overall Score: {res['overall_score']}% ({res['match_level']})")
    print(f"    Sub-scores: Job Fit={res['job_fit_score']}%, Tech={res['technical_score']}%, Cultural={res['cultural_score']}%, Comm={res['communication_score']}%")
    print(f"    Matched Skills ({len(res['matched_skills'])}): {res['matched_skills'][:5]}")
    print(f"    Missing Skills ({len(res['missing_skills'])}): {res['missing_skills'][:5]}")
    
    candidate_id = database.save_candidate_screening(res)
    print(f"[3] Saved to DB with ID: {candidate_id}")
    
    all_cands = database.get_candidates()
    print(f"[4] Total Candidates in DB: {len(all_cands)}")
    
    chat_reply = nlp_engine.generate_ai_chat_response(
        user_query="How can I improve my score?",
        resume_text=sample["resume"],
        jd_text=sample["job_description"],
        screening_data=res
    )
    print("[5] AI Chat Response generated successfully.")
    print("ALL TESTS PASSED!")

if __name__ == "__main__":
    test()
