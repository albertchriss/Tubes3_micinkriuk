from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class ApplicantProfile(Base):
    __tablename__ = "applicantprofile" 

    applicant_id = Column(Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String(50), default=None, nullable=True)
    last_name = Column(String(50), default=None, nullable=True)
    date_of_birth = Column(Date, default=None, nullable=True)
    address = Column(String(255), default=None, nullable=True)
    phone_number = Column(String(50), default=None, nullable=True)

    # --- Relationships ---
    applications = relationship("ApplicationDetail", back_populates="applicant")

    # for debugging and logging purposes 
    def __repr__(self):
        return f"<ApplicantProfile(id={self.applicant_id}, name='{self.first_name} {self.last_name}')>"


class ApplicationDetail(Base):
    __tablename__ = "applicationdetail"

    detail_id = Column(Integer, primary_key=True, index=True, nullable=False)
    applicant_id = Column(Integer, ForeignKey("applicantprofile.applicant_id"), nullable=False)
    application_role = Column(String(100), default=None, nullable=True) # VARCHAR(100) DEFAULT NULL
    cv_path = Column(Text, default=None, nullable=True) # TEXT DEFAULT NULL (TEXT can store long strings)

    # --- Relationships ---
    applicant = relationship("ApplicantProfile", back_populates="applications")

    # for debugging and logging purposes 
    def __repr__(self):
        return f"<ApplicationDetail(id={self.detail_id}, role='{self.application_role}', applicant_id={self.applicant_id})>"
