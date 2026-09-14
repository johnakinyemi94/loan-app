from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Loan Approval API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoanApplicationRequest(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=18, le=120)
    income: float = Field(..., gt=0)
    credit_score: int = Field(..., ge=300, le=850)
    loan_amount: float = Field(..., gt=0)
    employment_years: int = Field(..., ge=0)
    existing_debt: float = Field(..., ge=0)

class LoanOffer(BaseModel):
    loan_amount: float
    interest_rate: float
    term_months: int
    reason: str

class LoanApplicationResponse(BaseModel):
    application_id: str
    status: str
    decision: str  
    confidence: float
    email: Optional[str] = None
    offers: Optional[List[LoanOffer]] = None
    next_steps: str

class AdminReviewAction(BaseModel):
    application_id: str
    decision: str
    notes: str

class EscalatedApplicationItem(BaseModel):
    id: str
    applicant_name: str
    applicant_email: str
    bias_score_l1: float
    bias_score_l2: Optional[float] = None
    generated_email: str
    reason_escalated: str
    created_at: str

class MetricsResponse(BaseModel):
    total_applications: int
    approved_count: int
    denied_count: int
    escalated_count: int
    approval_rate: float
    average_bias_score_l1: float
    average_bias_score_l2: Optional[float] = None
    escalation_rate: float


applications_db = {}
decisions_db = {}
escalation_queue = {}
audit_logs = []


@app.post("/api/applications/submit", response_model=LoanApplicationResponse)
async def submit_application(req: LoanApplicationRequest):
    """Submit a loan application"""
    try:
     
        app_id = str(uuid.uuid4())[:8]
        
      
        logger.info(f"New application submitted: {app_id} - {req.name}")
        
       
        applications_db[app_id] = {
            "id": app_id,
            "name": req.name,
            "age": req.age,
            "income": req.income,
            "credit_score": req.credit_score,
            "loan_amount": req.loan_amount,
            "employment_years": req.employment_years,
            "existing_debt": req.existing_debt,
            "created_at": datetime.now().isoformat()
        }

        
        income_to_loan = req.income / req.loan_amount
        debt_to_income = req.existing_debt / req.income
        score = 0.0
        score += 0.35 if req.credit_score >= 700 else 0.2 if req.credit_score >= 650 else 0.05
        score += 0.3 if income_to_loan >= 2 else 0.2 if income_to_loan >= 1.5 else 0.05
        score += 0.2 if debt_to_income <= 0.3 else 0.1 if debt_to_income <= 0.45 else 0.0
        score += 0.15 if req.employment_years >= 5 else 0.1 if req.employment_years >= 2 else 0.05

        approved = score >= 0.65
        decision = "APPROVED" if approved else "DENIED"
        confidence = round(min(0.98, max(0.55, 0.55 + abs(score - 0.5) * 0.8)), 2)
        status = "APPROVED" if approved else "DENIED"

        if approved:
            email = (
                f"Hi {req.name},\n\n"
                f"Good news: your loan application for £{req.loan_amount:,.0f} has been approved. "
                f"We will contact you with the final documents and funding details.\n\n"
                "Thank you,\nLendwise"
            )
            offers = []
            next_steps = "Review the final documents when they arrive and confirm your funding details."
        else:
            email = (
                f"Hi {req.name},\n\n"
                f"We are unable to approve your request for £{req.loan_amount:,.0f} at this time. "
                "Here are options that may better fit your current profile.\n\n"
                "Thank you,\nLendwise"
            )
            offers = [
                LoanOffer(
                    loan_amount=round(req.loan_amount * 0.7, 2),
                    interest_rate=9.99,
                    term_months=48,
                    reason="A smaller loan amount may reduce the payment-to-income burden.",
                ),
                LoanOffer(
                    loan_amount=round(req.loan_amount * 0.85, 2),
                    interest_rate=11.49,
                    term_months=60,
                    reason="A longer term can make monthly payments more manageable.",
                ),
            ]
            next_steps = "Review the alternative offers and consider reapplying after improving your credit or debt profile."

        response = LoanApplicationResponse(
            application_id=app_id,
            status=status,
            decision=decision,
            confidence=confidence,
            email=email,
            offers=offers,
            next_steps=next_steps,
        )
        decisions_db[app_id] = response.model_dump()
        return response
    
    except Exception as e:
        logger.error(f"Error processing application: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing application: {str(e)}")

@app.get("/api/applications/{app_id}", response_model=LoanApplicationResponse)
async def get_application_status(app_id: str):
    """Check application status"""
    try:
        if app_id not in applications_db:
            raise HTTPException(status_code=404, detail=f"Application {app_id} not found")
        
        app_data = applications_db[app_id]
        decision_data = decisions_db.get(app_id)
        
        if not decision_data:
            return LoanApplicationResponse(
                application_id=app_id,
                status="PROCESSING",
                decision="PENDING",
                confidence=0.0,
                next_steps="Your application is being reviewed."
            )
        
        return LoanApplicationResponse(
            application_id=app_id,
            status=decision_data.get("status", "COMPLETED"),
            decision=decision_data.get("decision", "PENDING"),
            confidence=decision_data.get("confidence", 0.0),
            email=decision_data.get("email"),
            offers=decision_data.get("offers"),
            next_steps=decision_data.get("next_steps", "Processing complete.")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching application status: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching application status")

@app.get("/api/admin/review-queue", response_model=List[EscalatedApplicationItem])
async def get_review_queue():
    """Get applications escalated for human review"""
    try:
        queue_items = []
        for app_id, escalated_app in escalation_queue.items():
            queue_items.append(EscalatedApplicationItem(
                id=app_id,
                applicant_name=escalated_app.get("applicant_name", "Unknown"),
                applicant_email=escalated_app.get("applicant_email", "unknown@example.com"),
                bias_score_l1=escalated_app.get("bias_score_l1", 0.0),
                bias_score_l2=escalated_app.get("bias_score_l2"),
                generated_email=escalated_app.get("generated_email", ""),
                reason_escalated=escalated_app.get("reason", "BIAS_DETECTED"),
                created_at=escalated_app.get("created_at", datetime.now().isoformat())
            ))
        
        return queue_items
    
    except Exception as e:
        logger.error(f"Error fetching review queue: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching review queue")

@app.post("/api/admin/review/{app_id}")
async def admin_review(app_id: str, action: AdminReviewAction):
    """Human admin approves/rejects escalated email"""
    try:
        if app_id not in escalation_queue:
            raise HTTPException(status_code=404, detail=f"Escalated application {app_id} not found")
        
        escalated_app = escalation_queue[app_id]
        
        if action.decision == "APPROVE":
      
            status = "APPROVED_EMAIL_SENT"
        elif action.decision == "REJECT":
         
            status = "REJECTED_NEEDS_MODIFICATION"
        else:
            raise HTTPException(status_code=400, detail="Invalid decision")
        
      
        if app_id in decisions_db:
            decisions_db[app_id]["status"] = status
            decisions_db[app_id]["admin_notes"] = action.notes
        
      
        del escalation_queue[app_id]
        
       
        audit_logs.append({
            "timestamp": datetime.now().isoformat(),
            "app_id": app_id,
            "action": f"ADMIN_REVIEW_{action.decision}",
            "notes": action.notes
        })
        
        logger.info(f"Admin reviewed application {app_id}: {action.decision}")
        
        return {"status": "success", "message": f"Application {action.decision.lower()}ed"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing admin review: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing admin review")

@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Return system metrics (approval rate, bias detection stats, etc.)"""
    try:
        total = len(applications_db)
        approved = sum(1 for d in decisions_db.values() if d.get("decision") == "APPROVED")
        denied = sum(1 for d in decisions_db.values() if d.get("decision") == "DENIED")
        escalated = len(escalation_queue)
        
        approval_rate = (approved / total * 100) if total > 0 else 0
        escalation_rate = (escalated / total * 100) if total > 0 else 0
        

        bias_l1_scores = [d.get("bias_score_l1", 0) for d in decisions_db.values()]
        avg_bias_l1 = sum(bias_l1_scores) / len(bias_l1_scores) if bias_l1_scores else 0
        
        bias_l2_scores = [d.get("bias_score_l2") for d in decisions_db.values() if d.get("bias_score_l2")]
        avg_bias_l2 = sum(bias_l2_scores) / len(bias_l2_scores) if bias_l2_scores else None
        
        return MetricsResponse(
            total_applications=total,
            approved_count=approved,
            denied_count=denied,
            escalated_count=escalated,
            approval_rate=approval_rate,
            average_bias_score_l1=avg_bias_l1,
            average_bias_score_l2=avg_bias_l2,
            escalation_rate=escalation_rate
        )
    
    except Exception as e:
        logger.error(f"Error calculating metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating metrics")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
