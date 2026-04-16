"""Mock FastAPI server for development - responds immediately without needing to load ML models."""

import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import only database dependencies (no ML models)
from app.database import BugReport, create_tables, get_db


class BugReportRequest(BaseModel):
    title: str
    description: str


class BugReportResponse(BaseModel):
    assigned_to: str
    assignment_confidence: float
    priority: str
    priority_confidence: float
    is_duplicate: bool = False
    duplicate_info: dict = {}


class BugHistoryResponse(BaseModel):
    id: int
    title: str
    description: str
    assigned_to: str
    assignment_confidence: float
    priority: str
    priority_confidence: float
    confidence: float
    is_duplicate: bool
    duplicate_of: int | None = None
    created_at: str


app = FastAPI(
    title="Automated Bug Triage System (Mock)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    create_tables()
    logger.info("Database initialized")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Bug Triage System is running"}


@app.post("/predict", response_model=BugReportResponse)
async def predict_bug_assignment(
    request: BugReportRequest,
    db: Session = Depends(get_db),
):
    """Mock prediction endpoint - returns simulated predictions"""
    try:
        # Mock prediction results
        prediction = {
            "assigned_to": "Backend Team",
            "assignment_confidence": 0.85,
            "priority": "Medium",
            "priority_confidence": 0.78,
        }

        # Save to database
        db_report = BugReport(
            title=request.title,
            description=request.description,
            predicted_assigned_to=prediction["assigned_to"],
            assignment_confidence=prediction["assignment_confidence"],
            predicted_priority=prediction["priority"],
            priority_confidence=prediction["priority_confidence"],
            is_duplicate=0,
            duplicate_of=None,
        )
        db.add(db_report)
        db.commit()

        return BugReportResponse(
            assigned_to=prediction["assigned_to"],
            assignment_confidence=prediction["assignment_confidence"],
            priority=prediction["priority"],
            priority_confidence=prediction["priority_confidence"],
            is_duplicate=False,
            duplicate_info={},
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return BugReportResponse(
            assigned_to="Error",
            assignment_confidence=0.0,
            priority="Unknown",
            priority_confidence=0.0,
            is_duplicate=False,
            duplicate_info={"error": str(e)},
        )


@app.get("/reports", response_model=list[BugHistoryResponse])
async def get_bug_reports(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Get bug report history"""
    reports = db.query(BugReport).order_by(BugReport.created_at.desc()).offset(skip).limit(limit).all()
    return [
        {
            "id": report.id,
            "title": report.title,
            "description": report.description,
            "assigned_to": report.predicted_assigned_to,
            "assignment_confidence": report.assignment_confidence,
            "priority": report.predicted_priority,
            "priority_confidence": report.priority_confidence,
            "confidence": report.assignment_confidence,
            "created_at": report.created_at.isoformat() if report.created_at else "",
            "is_duplicate": bool(report.is_duplicate),
            "duplicate_of": report.duplicate_of,
        }
        for report in reports
    ]
