from typing import Dict
import re

class BiasDetectorLevel1:
    """
    First-pass soft bias detection
    Uses rule-based + simple ML classifier
    """
    
    OFFENSIVE_PATTERNS = {
        "rude": r"\b(stupid|idiot|bad decision|reject|decline)\b",
        "discriminatory": r"\b(too old|too young|wrong neighborhood|unusual name)\b",
        "dismissive": r"\b(unfortunately|sadly|regrettably|cannot possibly)\b",
    }
    
    async def analyze_email(self, email_text: str) -> Dict:
        """
        Returns: {
            "bias_score": 0.0-1.0,  # 0 = no bias, 1 = highly biased
            "flags": ["pattern1", "pattern2"],
            "recommendation": "SEND" | "ESCALATE" | "REVIEW"
        }
        """
        
        score = 0.0
        flags = []
        
        for category, pattern in self.OFFENSIVE_PATTERNS.items():
            if re.search(pattern, email_text, re.IGNORECASE):
                score += 0.3
                flags.append(f"Contains {category} language")
        

        if self._contains_vague_language(email_text):
            score += 0.2
            flags.append("Vague reasoning")
        
        if self._has_inconsistent_tone(email_text):
            score += 0.15
            flags.append("Tone inconsistency detected")
        
        score = min(score, 1.0)

        
        if score > 0.6:
            recommendation = "ESCALATE"
        elif score > 0.3:
            recommendation = "REVIEW"
        else:
            recommendation = "SEND"
        
        return {
            "bias_score": score,
            "flags": flags,
            "recommendation": recommendation,
            "model_name": "BiasDetectorLevel1"
        }
    
    def _contains_vague_language(self, text: str) -> bool:
        vague_terms = ["maybe", "might", "could be", "possibly"]
        return any(term in text.lower() for term in vague_terms)
    
    def _has_inconsistent_tone(self, text: str) -> bool:

        pass