import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import List
from config import settings

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails to applicants"""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.sender_email = settings.SENDER_EMAIL
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
    
    async def send_loan_decision_email(
        self,
        recipient_email: str,
        recipient_name: str,
        email_body: str,
        decision: str,
        subject: str = None
    ) -> bool:
        """
        Send loan decision email to applicant
        
        Args:
            recipient_email: Applicant's email address
            recipient_name: Applicant's name
            email_body: Email body content
            decision: APPROVED or DENIED
            subject: Custom subject line
        
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            if not subject:
                subject = f"Loan Application {decision}" if decision else "Loan Application Decision"
            

            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            

            message.attach(MIMEText(email_body, "html"))
            
 
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)
            
            logger.info(f"Email sent successfully to {recipient_email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
            return False
    
    async def send_admin_notification(
        self,
        admin_emails: List[str],
        application_id: str,
        reason: str,
        application_data: dict
    ) -> bool:
        """
        Send notification to admin for escalated applications
        
        Args:
            admin_emails: List of admin email addresses
            application_id: Application ID
            reason: Reason for escalation
            application_data: Application details
        
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            subject = f"[ESCALATED] Loan Application {application_id} Requires Review"
            
            body = f"""
            <h2>Escalated Application Alert</h2>
            <p><strong>Application ID:</strong> {application_id}</p>
            <p><strong>Reason:</strong> {reason}</p>
            <hr>
            <h3>Applicant Details</h3>
            <p><strong>Name:</strong> {application_data.get('name', 'N/A')}</p>
            <p><strong>Email:</strong> {application_data.get('email', 'N/A')}</p>
            <p><strong>Credit Score:</strong> {application_data.get('credit_score', 'N/A')}</p>
            <p><strong>Requested Amount:</strong> £{application_data.get('loan_amount', 'N/A')}</p>
            <hr>
            <p>Please review this application in the admin dashboard.</p>
            """
            
            for admin_email in admin_emails:
                message = MIMEMultipart()
                message["From"] = self.sender_email
                message["To"] = admin_email
                message["Subject"] = subject
                message.attach(MIMEText(body, "html"))
                
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(message)
            
            logger.info(f"Admin notification sent for application {application_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send admin notification: {str(e)}")
            return False
