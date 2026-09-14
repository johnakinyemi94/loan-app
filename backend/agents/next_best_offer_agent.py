from typing import Dict, List
from dataclasses import dataclass

@dataclass
class LoanOffer:
    loan_amount: float
    interest_rate: float
    term_months: int
    reason: str

class NextBestOfferAgent:
    """
    When applicant is DENIED, suggests alternative offers
    Based on their credit profile and GB model reasoning
    """
    
    async def generate_alternative_offers(
        self,
        applicant_data: Dict,
        gb_decision_data: Dict,
        requested_amount: float
    ) -> Dict:
        """
        Analyzes why they were denied and suggests next-best offers
        
        Returns: {
            "offers": [LoanOffer, ...],
            "reasoning": str,
            "recommendation": "INCLUDE_IN_EMAIL" | "SEPARATE_OFFER"
        }
        """
        

        weak_factors = self._identify_weak_factors(gb_decision_data)
        

        offers = []
        

        if applicant_data['income'] >= requested_amount * 0.3:
            smaller_offer = LoanOffer(
                loan_amount=requested_amount * 0.7,  
                interest_rate=7.5,  
                term_months=60,
                reason="Approved at 70% of requested amount"
            )
            offers.append(smaller_offer)
        
     
        if applicant_data['debt_to_income'] < 0.35:
            moderate_offer = LoanOffer(
                loan_amount=requested_amount * 0.5,
                interest_rate=5.5,
                term_months=48,
                reason="Approved at 50% with competitive rate"
            )
            offers.append(moderate_offer)
        

        offer_email = await self._generate_offer_email(
            applicant_data,
            offers,
            weak_factors
        )
        
        return {
            "offers": [offer.__dict__ for offer in offers],
            "offer_email": offer_email,
            "reasoning": f"Denied due to: {', '.join(weak_factors)}",
            "recommendation": "INCLUDE_IN_EMAIL" if offers else "NO_OFFER"
        }
    
    def _identify_weak_factors(self, gb_data: Dict) -> List[str]:
        factors = []
        if gb_data['credit_score_impact'] < -0.1:
            factors.append("Credit score")
        if gb_data['debt_ratio_impact'] < -0.1:
            factors.append("High existing debt")
        if gb_data['income_ratio_impact'] < -0.1:
            factors.append("Loan-to-income ratio")
        return factors
    
    async def _generate_offer_email(self, applicant_data, offers, factors) -> str:
  
        pass