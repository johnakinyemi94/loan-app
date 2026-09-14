from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class LoanApplicationRequest(BaseModel):
    name: str
    age: int
    income: float
    credit_score: int
    loan_amount: float
    employment_years: int
    existing_debt: float

class LoanApplicationResponse(BaseModel):
    application_id: str
    status: str
    decision: str
    confidence: float
    email: Optional[str] = None
    offers: Optional[list] = None
    next_steps: str

@app.post("/api/applications/submit")
async def submit_application(req: LoanApplicationRequest):
    """Submit a loan application"""

    pass

@app.get("/api/applications/{app_id}")
async def get_application_status(app_id: str):
    """Check application status"""
    pass

@app.get("/api/admin/review-queue")
async def get_review_queue():
    """Get applications escalated for human review"""
    pass

@app.post("/api/admin/review/{app_id}")
async def admin_review(app_id: str, decision: str, notes: str):
    """Human admin approves/rejects escalated email"""
    pass

@app.get("/api/metrics")
async def get_metrics():
    """Return system metrics (approval rate, bias detection stats, etc.)"""
    pass