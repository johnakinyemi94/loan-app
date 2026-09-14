from typing import Optional
import httpx
from functools import lru_cache

class LLMWrapper:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1"
    
    async def generate_email(
        self,
        applicant_name: str,
        decision: str, 
        loan_amount: float,
        confidence_score: float,
        denial_reason: Optional[str] = None,
        approved_amount: Optional[float] = None
    ) -> str:
        """
        Generates professional email based on loan decision
        Uses few-shot prompting to ensure consistency
        """
        
        if decision == "APPROVED":
            prompt = f"""
            Generate a professional, warm email to {applicant_name} 
            notifying them of loan approval.
            
            Details:
            - Approved Amount: £{approved_amount}
            - Confidence in decision: {confidence_score*100:.1f}%
            
            Keep tone:
            - Professional but friendly
            - Clear and concise
            - Include next steps
            
            Constraints:
            - Max 200 words
            - No jargon
            - One call-to-action
            
            Email body (start with greeting):
            """
        else:
            prompt = f"""
            Generate a professional, empathetic email to {applicant_name}
            notifying them of loan denial.
            
            Details:
            - Primary Reason: {denial_reason}
            - Decision Confidence: {confidence_score*100:.1f}%
            
            Keep tone:
            - Respectful and professional
            - Empathetic (they were denied)
            - Constructive (point toward improvement)
            
            Constraints:
            - Max 200 words
            - Avoid blame language
            - Include how they can reapply
            
            Email body (start with greeting):
            """
        
        response = await self._call_llm(prompt)
        return response
    
    async def _call_llm(self, prompt: str) -> str:
     
        pass