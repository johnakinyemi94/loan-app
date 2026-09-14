import logging
from datetime import datetime
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

class AuditLogger:
    """
    Comprehensive audit logging for compliance and transparency
    Tracks all decisions, events, and modifications
    """
    
    def __init__(self, log_file: str = "audit.log"):
        self.log_file = log_file
        self.setup_logger()
    
    def setup_logger(self):
        """Configure audit logger"""
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    def log_application_submitted(self, app_id: str, applicant_name: str, loan_amount: float):
        """Log when application is submitted"""
        message = f"APPLICATION_SUBMITTED | ID: {app_id} | Name: {applicant_name} | Amount: £{loan_amount}"
        logger.info(message)
    
    def log_gb_decision(
        self,
        app_id: str,
        decision: str,
        confidence: float,
        feature_importance: Dict[str, float]
    ):
        """Log Gradient Boosting decision"""
        message = f"GB_DECISION | ID: {app_id} | Decision: {decision} | Confidence: {confidence:.2f} | Features: {json.dumps(feature_importance)}"
        logger.info(message)
    
    def log_email_generated(self, app_id: str, decision: str):
        """Log email generation"""
        message = f"EMAIL_GENERATED | ID: {app_id} | Decision: {decision}"
        logger.info(message)
    
    def log_bias_detection(
        self,
        app_id: str,
        detector_level: int,
        bias_score: float,
        recommendation: str,
        flags: list
    ):
        """Log bias detection analysis"""
        message = f"BIAS_DETECTION_L{detector_level} | ID: {app_id} | Score: {bias_score:.2f} | Recommendation: {recommendation} | Flags: {json.dumps(flags)}"
        logger.info(message)
    
    def log_escalation(self, app_id: str, reason: str, escalation_level: int):
        """Log escalation to next level"""
        message = f"ESCALATION_TO_LEVEL{escalation_level} | ID: {app_id} | Reason: {reason}"
        logger.info(message)
    
    def log_escalation_to_human(self, app_id: str, reason: str):
        """Log escalation to human review"""
        message = f"ESCALATION_TO_HUMAN | ID: {app_id} | Reason: {reason}"
        logger.info(message)
    
    def log_offers_generated(self, app_id: str, num_offers: int, reasons: list):
        """Log alternative offers generation"""
        message = f"OFFERS_GENERATED | ID: {app_id} | Count: {num_offers} | Reasons: {json.dumps(reasons)}"
        logger.info(message)
    
    def log_email_sent(self, app_id: str, recipient_email: str, email_type: str):
        """Log email sent successfully"""
        message = f"EMAIL_SENT | ID: {app_id} | Recipient: {recipient_email} | Type: {email_type}"
        logger.info(message)
    
    def log_admin_review(self, app_id: str, admin_email: str, decision: str, notes: str):
        """Log admin review action"""
        message = f"ADMIN_REVIEW | ID: {app_id} | Admin: {admin_email} | Decision: {decision} | Notes: {notes}"
        logger.info(message)
    
    def log_workflow_completed(
        self,
        app_id: str,
        final_status: str,
        processing_time_seconds: float
    ):
        """Log workflow completion"""
        message = f"WORKFLOW_COMPLETED | ID: {app_id} | Status: {final_status} | Time: {processing_time_seconds:.2f}s"
        logger.info(message)
    
    def log_error(self, app_id: str, error_type: str, error_message: str):
        """Log errors for debugging"""
        message = f"ERROR | ID: {app_id} | Type: {error_type} | Message: {error_message}"
        logger.error(message)
    
    def log_system_event(self, event_type: str, details: Dict[str, Any]):
        """Log general system events"""
        message = f"SYSTEM_EVENT | Type: {event_type} | Details: {json.dumps(details)}"
        logger.info(message)
