from sqlalchemy.orm import Session
from models.model import ApplicantProfile, ApplicationDetail

# --- AplicantProfile Repository Functions ---

def repo_get_all_applicants(db: Session):
    """
    Retrieve all applicants from the database.
    """
    return db.query(ApplicantProfile).all()

def repo_get_applicant_by_id(db: Session, applicant_id: int):
    """
    Retrieve an applicant by their ID.
    """
    return db.query(ApplicantProfile).filter(ApplicantProfile.applicant_id == applicant_id).first()

def repo_insert_applicant(db: Session, applicant: ApplicantProfile):
    """
    Insert a new applicant into the database.
    """
    db.add(applicant)
    db.commit()
    db.refresh(applicant)
    return applicant

# kayanya gaboleh update/delete ga sih

# --- ApplicationDetail Repository Functions ---

def repo_get_all_applications(db: Session):
    """
    Retrieve all applications from the database.
    """
    return db.query(ApplicationDetail).all()

def repo_get_applications_by_applicant_id(db: Session, applicant_id: int):
    """
    Retrieve all applications for a specific applicant.
    """
    return db.query(ApplicationDetail).filter(ApplicationDetail.applicant_id == applicant_id).all()

def repo_insert_application(db: Session, application: ApplicationDetail):
    """
    Insert a new application into the database.
    """
    db.add(application)
    db.commit()
    db.refresh(application)
    return application