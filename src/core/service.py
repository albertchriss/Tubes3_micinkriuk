from core.database import get_db
from core.repository import *
from datetime import date
from core.algorithm import knuth_morris_pratt, boyer_moore, aho_corasick, fuzzy_match
from core.utils import extract_text_from_pdf
import time
import pickle
import json
import os
from pathlib import Path
from core.regex import process_cv

cv_data_text = {}
CACHE_FILE = Path("data/cache/cv_data_cache.pkl")

def save_cache():
    """Save cv_data_text to cache file"""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cv_data_text, f)

def load_cache():
    """Load cv_data_text from cache file"""
    global cv_data_text
    try:
        if CACHE_FILE.exists():
            with open(CACHE_FILE, 'rb') as f:
                cv_data_text = pickle.load(f)
                return True
    except (FileNotFoundError, pickle.PickleError, EOFError):
        cv_data_text = {}
    return False

def extract_all_cv_data(force_refresh=False):
    """
    Extract all CV data with caching support
    """
    global cv_data_text
    
    # Try to load from cache first (unless force refresh)
    if not force_refresh and load_cache():
        print(f"Loaded {len(cv_data_text)} CV records from cache")
        return cv_data_text
    
    print("Extracting CV data from PDFs...")
    from core.service import get_all_applications
    
    cv_data_text = {}  # Reset the dictionary
    applications = get_all_applications()

    for application in applications:
        if application.cv_path and application.applicant_id: # type: ignore
            cv_text = extract_text_from_pdf(application.cv_path)
            cv_text = cv_text.lower()
            if cv_text:
                cv_data_text[application.detail_id] = {
                    "applicant_id": application.applicant_id,
                    "cv_text": cv_text,
                    "cleaned_text": cv_text.replace('\n', ' ').strip()
                }
    
    # Save to cache
    save_cache()
    print(f"Extracted and cached {len(cv_data_text)} CV records")
    return cv_data_text

def clear_cache():
    """Clear the cache file"""
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
        print("Cache cleared")

# --- Service Functions for ApplicantProfile ---

def get_all_applicants():
    """
    Retrieve all applicants from the database.
    """
    db = next(get_db())
    try:
        return repo_get_all_applicants(db)
    finally:
        db.close()

def get_applicant_by_id(applicant_id: int):
    """
    Retrieve an applicant by their ID.
    """
    db = next(get_db())
    try:
        return repo_get_applicant_by_id(db, applicant_id)
    finally:
        db.close()

def insert_applicant(first_name: str, last_name: str, date_of_birth: date, address: str, phone_number: str):
    """
    Insert a new applicant into the database.
    """
    db = next(get_db())
    try:
        applicant = ApplicantProfile(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            address=address,
            phone_number=phone_number
        )
        return repo_insert_applicant(db, applicant)
    finally:
        db.close()


# --- Service Functions for ApplicationDetail ---

def get_all_applications():
    """
    Retrieve all applications from the database.
    """
    db = next(get_db())
    try:
        return repo_get_all_applications(db)
    finally:
        db.close()

def get_applications_by_applicant_id(applicant_id: int):
    """
    Retrieve all applications for a specific applicant.
    """
    db = next(get_db())
    try:
        return repo_get_applications_by_applicant_id(db, applicant_id)
    finally:
        db.close()

def insert_application(applicant_id: int, application_role: str, cv_path: str):
    """
    Insert a new application into the database.
    """
    db = next(get_db())

    try:
        applicant = repo_get_applicant_by_id(db, applicant_id)
        if not applicant:
            return None
    
        application = ApplicationDetail(
            applicant_id=applicant_id,
            application_role=application_role,
            cv_path=cv_path
        )
        return repo_insert_application(db, application)
    finally:
        db.close()


def get_cv_data_by_applicant_id(applicant_id: int):
    """
    Retrieve the CV data for a specific applicant.
    """
    db = next(get_db())
    try:
        applications = repo_get_applications_by_applicant_id(db, applicant_id)
        if not applications:
            return None
        applicant = repo_get_applicant_by_id(db, applicant_id)
        if not applicant:
            return None
        
        regex_res = process_cv(cv_data_text.get(applications[0].detail_id, {}).get("cv_text", ""))

        cv_data = {
            "name": f"{applicant.first_name} {applicant.last_name}",
            "birthdate": applicant.date_of_birth.isoformat() if applicant.date_of_birth else None, # type: ignore
            "address": applicant.address,
            "phone_number": applicant.phone_number,
            "skills": regex_res.get("skills", []),
            "education": regex_res.get("education", []),
            "job_history": regex_res.get("job_history", []),
        }

        return cv_data

    finally:
        db.close()


def search_matching_data(keywords: list[str], algo: str, top_match: int) -> dict:
    applicants = get_all_applicants()

    applicant_match_count = 0
    applicants_results = []
    chosen_applications = set()

    curr_time = time.time()

    for applicant in applicants:
        if (applicant_match_count >= top_match) and (top_match > 0):
                break
        applications = get_applications_by_applicant_id(applicant.applicant_id) # type: ignore
        for application in applications:
            results = []
            cv_text = cv_data_text.get(application.detail_id, {}).get("cleaned_text", "")
            if not cv_text:
                continue
            if algo == "Knuth-Morris-Pratt":
                results = knuth_morris_pratt(cv_text, keywords)
            elif algo == "Boyer-Moore":
                results = boyer_moore(cv_text, keywords)
            elif algo == "Aho-Corasick":
                results = aho_corasick(cv_text, keywords)
            else:
                raise ValueError(f"Unknown algorithm: {algo}")
            
            if not results:
                continue

            applicant_match_count += 1
            applicants_results.append({
                "applicant_id": applicant.applicant_id,
                "name": f"{applicant.first_name} {applicant.last_name}",
                "matched_keywords": len(results),
                "keywords_data": results,
                "cv_path": application.cv_path,
                "bgcolor": "#E3F2FD"  # Example background color
            })
            chosen_applications.add(application.detail_id)

            if (applicant_match_count >= top_match) and (top_match > 0):
                break

    exact_match_stats = {
        "count": applicant_match_count,
        "time_ms": int((time.time() - curr_time) * 1000)  # Convert to milliseconds
    }

    # Fuzzy matching
    fuzzy_match_count = 0
    curr_time = time.time()
    for applicant in applicants:
        if (applicant_match_count >= top_match) and (top_match > 0):
            break
        applications = get_applications_by_applicant_id(applicant.applicant_id) # type: ignore
        for application in applications:
            cv_text = cv_data_text.get(application.detail_id, {}).get("cleaned_text", "")
            if not cv_text:
                continue

            if not application.detail_id or application.detail_id in chosen_applications: # type: ignore
                continue
            
            results = fuzzy_match(cv_text, keywords)

            if not results:
                continue
            fuzzy_match_count += 1
            applicants_results.append({
                "applicant_id": applicant.applicant_id,
                "name": f"{applicant.first_name} {applicant.last_name}",
                "matched_keywords": len(results),
                "keywords_data": results,
                "cv_path": application.cv_path,
                "bgcolor": "#E3F2FD"  # Example background color
            })

            if (applicant_match_count >= top_match) and (top_match > 0):
                break
    
    fuzzy_match_stats = {
        "count": fuzzy_match_count,
        "time_ms": int((time.time() - curr_time) * 1000)  # Convert to milliseconds
    }

    results_data = {
        "exact_match_stats": exact_match_stats,
        "fuzzy_match_stats": fuzzy_match_stats,
        "applicants": applicants_results
    }

    return results_data

            
    # results_data = {
    #     "exact_match_stats": {"count": 0, "time_ms": 0},
    #     "fuzzy_match_stats": {"count": 0, "time_ms": 0},
    #     "applicants": []
    # }