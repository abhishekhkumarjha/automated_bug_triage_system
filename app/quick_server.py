"""Ultra-lightweight mock FastAPI server for immediate response."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from datetime import datetime


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


# In-memory storage for this session
reports_storage = []
report_id_counter = 1


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


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Bug Triage System is running"}


@app.post("/predict", response_model=BugReportResponse)
async def predict_bug_assignment(request: BugReportRequest):
    """Mock prediction endpoint - returns simulated predictions"""
    global report_id_counter
    
    try:
        # Mock prediction results
        prediction = {
            "assigned_to": "Backend Team",
            "assignment_confidence": 0.85,
            "priority": "Medium",
            "priority_confidence": 0.78,
            "is_duplicate": False,
            "duplicate_info": {},
        }

        # Store in memory
        reports_storage.append({
            "id": report_id_counter,
            "title": request.title,
            "description": request.description,
            "assigned_to": prediction["assigned_to"],
            "assignment_confidence": prediction["assignment_confidence"],
            "priority": prediction["priority"],
            "priority_confidence": prediction["priority_confidence"],
            "is_duplicate": prediction["is_duplicate"],
            "duplicate_of": None,
            "created_at": datetime.utcnow().isoformat(),
        })
        report_id_counter += 1

        return BugReportResponse(**prediction)
    except Exception as e:
        return BugReportResponse(
            assigned_to="Error",
            assignment_confidence=0.0,
            priority="Unknown",
            priority_confidence=0.0,
            is_duplicate=False,
            duplicate_info={"error": str(e)},
        )


@app.get("/reports", response_model=list[BugHistoryResponse])
async def get_bug_reports(skip: int = 0, limit: int = 50):
    """Get bug report history"""
    sorted_reports = sorted(reports_storage, key=lambda x: x["created_at"], reverse=True)
    return sorted_reports[skip : skip + limit]
