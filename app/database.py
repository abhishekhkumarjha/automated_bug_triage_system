from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create SQLite database
DATABASE_URL = "sqlite:///./bug_triage.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class BugReport(Base):
    """
    Database model for storing bug reports and their predictions.
    """
    __tablename__ = "bug_reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    predicted_assigned_to = Column(String, nullable=False)
    assignment_confidence = Column(Float, nullable=False)
    predicted_priority = Column(String, nullable=False)
    priority_confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_duplicate = Column(Integer, default=0)  # 0: not duplicate, 1: potential duplicate
    duplicate_of = Column(Integer, nullable=True)  # ID of the original bug if duplicate

def get_db():
    """
    Dependency to get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")