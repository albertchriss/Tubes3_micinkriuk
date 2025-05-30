from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# --- Database Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/ats_database")

# --- SQLAlchemy Engine Setup ---
engine = create_engine(
    DATABASE_URL, echo=False
)

# --- SQLAlchemy Session Setup ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Base for Declarative Models ---
Base = declarative_base()

def get_db():
    """
    Provides a database session.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Function to create all tables ---
def create_tables():
    Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")