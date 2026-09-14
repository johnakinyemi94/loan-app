from enum import Enum
from typing import Dict
from datetime import datetime

class DecisionStatus(Enum):
    PENDING = "PENDING"
    APPROVED_EMAIL_SENT = "APPROVED_EMAIL_SENT"
    DENIED_EMAIL_SENT = "DENIED_EMAIL_SENT"
    ESCALATED_TO_HUMAN = "ESCALATED_TO_HUMAN"
    OFFER_SENT = "OFFER_SENT"

class WorkflowEngine:
    """
    Orchestrates the entire loan approval workflow
    Coordinates between all agents
    """
    
    def __init__(self, db, gb_model, llm, bias_l1, bias_l2, offer_agent):
        self.db = db
        self.gb_model = gb_model
        self.llm = llm
        self.bias_detector_l1 = bias_l1
        self.bias_detector_l2 = bias_l2
        self.offer_agent = offer_agent
    
    async def process_application(self, application_data: Dict) -> Dict:
        """
        Main workflow:
        1. GB Decision
        2. LLM Email Generation
        3. Level 1 Bias Check
        4. Level 2 Bias Check (if needed)
        5. Send or Escalate
        6. Generate alternative offer (if denied)
        """
        
        application_id = application_data['id']
        self._log_event(application_id, "WORKFLOW_STARTED")
        
   
        gb_result = self.gb_model.predict(application_data['features'])
        self._log_event(application_id, f"GB_DECISION: {gb_result['decision']}")
        
    
        email = await self.llm.generate_email(
            applicant_name=application_data['name'],
            decision=gb_result['decision'],
            loan_amount=application_data['requested_amount'],
            confidence_score=gb_result['confidence'],
            denial_reason=gb_result.get('reason')
        )
        self._log_event(application_id, "EMAIL_GENERATED")
        
    
        bias_l1_result = await self.bias_detector_l1.analyze_email(email)
        self._log_event(
            application_id,
            f"BIAS_L1: score={bias_l1_result['bias_score']:.2f}"
        )
        
   
        if bias_l1_result['recommendation'] in ["ESCALATE", "REVIEW"]:
            bias_l2_result = await self.bias_detector_l2.analyze_email(email)
            self._log_event(
                application_id,
                f"BIAS_L2: score={bias_l2_result['bias_score']:.2f}"
            )
        else:
            bias_l2_result = {"recommendation": "APPROVED_TO_SEND"}
        
  
        final_status, action = await self._determine_action(
            application_id,
            gb_result,
            bias_l1_result,
            bias_l2_result,
            email,
            application_data
        )
        
   
        if gb_result['decision'] == "DENIED":
            offer_result = await self.offer_agent.generate_alternative_offers(
                application_data,
                gb_result,
                application_data['requested_amount']
            )
            self._log_event(application_id, f"OFFERS_GENERATED: {len(offer_result['offers'])}")
        else:
            offer_result = None
        

        result = {
            "application_id": application_id,
            "status": final_status.value,
            "action": action,
            "gb_decision": gb_result,
            "bias_scores": {
                "level_1": bias_l1_result['bias_score'],
                "level_2": bias_l2_result.get('bias_score', None)
            },
            "email": email if action in ["SEND", "SEND_WITH_OFFER"] else None,
            "offers": offer_result if offer_result else None,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.db.save_result(result)
        self._log_event(application_id, f"WORKFLOW_COMPLETED: {final_status.value}")
        
        return result
    
    async def _determine_action(
        self,
        app_id: str,
        gb_result: Dict,
        bias_l1: Dict,
        bias_l2: Dict,
        email: str,
        app_data: Dict
    ) -> tuple:
        """
        Logic tree for determining final action
        """
        
     
        if bias_l2.get('recommendation') == "ESCALATE_TO_HUMAN":
            self._log_event(app_id, "ESCALATED: Failed strict bias check (L2)")
            return DecisionStatus.ESCALATED_TO_HUMAN, "ESCALATE"
        
      
        if bias_l1.get('recommendation') == "ESCALATE":
            self._log_event(app_id, "ESCALATED: Failed soft bias check (L1)")
            return DecisionStatus.ESCALATED_TO_HUMAN, "ESCALATE"
        
      
        if gb_result['decision'] == "APPROVED":
            self._log_event(app_id, "APPROVED: Email will be sent")
            return DecisionStatus.APPROVED_EMAIL_SENT, "SEND"
        else:
            self._log_event(app_id, "DENIED: Will send denial + offers")
            return DecisionStatus.DENIED_EMAIL_SENT, "SEND_WITH_OFFER"
    
    def _log_event(self, application_id: str, event: str):
       
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] APP_{application_id}: {event}")
      