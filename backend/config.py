import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration"""
    
    API_TITLE: str = "Loan Approval API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://loan_app:password@localhost:5432/loan_approval"
    )
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "sk-test-key")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    
    BIAS_L1_ESCALATE_THRESHOLD: float = 0.6
    BIAS_L1_REVIEW_THRESHOLD: float = 0.3
    BIAS_L2_ESCALATE_THRESHOLD: float = 0.7
    BIAS_L2_REVIEW_THRESHOLD: float = 0.5
    
    GB_MODEL_PATH: str = os.getenv("GB_MODEL_PATH", "./ml/models/gb_model.pkl")
    GB_N_ESTIMATORS: int = int(os.getenv("GB_N_ESTIMATORS", "100"))
    GB_MAX_DEPTH: int = int(os.getenv("GB_MAX_DEPTH", "7"))
    GB_LEARNING_RATE: float = float(os.getenv("GB_LEARNING_RATE", "0.1"))
    
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "noreply@loanapproval.com")
    
    SCALER_PATH: str = os.getenv("SCALER_PATH", "./ml/models/scaler.pkl")
 
    FEATURE_NAMES: list = [
        "age",
        "income",
        "credit_score",
        "loan_amount",
        "employment_years",
        "existing_debt"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
