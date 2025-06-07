from core.database import get_db
from core.repository import *
from datetime import date

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