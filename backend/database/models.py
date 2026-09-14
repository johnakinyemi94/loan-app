from sqlalchemy import Column, String, Float, Int, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    
    id = Column(String, primary_key=True)
    applicant_name = Column(String)
    applicant_email = Column(String)
    age = Column(Int)
    income = Column(Float)
    credit_score = Column(Int)
    requested_loan_amount = Column(Float)
    employment_years = Column(Int)
    existing_debt = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

class ApplicationDecision(Base):
    __tablename__ = "application_decisions"
    
    id = Column(String, primary_key=True)
    application_id = Column(String, ForeignKey("loan_applications.id"))
    gb_decision = Column(String) 
    gb_confidence = Column(Float)
    gb_reasoning = Column(JSON)  #
    bias_score_level1 = Column(Float)
    bias_score_level2 = Column(Float)
    bias_flags = Column(JSON)
    final_status = Column(String)  
    generated_email = Column(String)
    alternative_offers = Column(JSON)
    human_review_notes = Column(String)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

class AdminReviewQueue(Base):
    __tablename__ = "admin_review_queue"
    
    id = Column(String, primary_key=True)
    application_id = Column(String, ForeignKey("loan_applications.id"))
    reason_escalated = Column(String)  
    status = Column(String)  
    assigned_to = Column(String)  
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True)
    application_id = Column(String)
    event = Column(String)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)