import re
from core.state import ModeState
# from textblob import TextBlob # Removed dependency for V1 pure python if possible, or assume installed.
# Using simple regex/heuristics for V1 to be dependency-lite if needed, 
# but TextBlob/NLTK is better for "Sentiment". 
# For now, we will use a keyword-based approach for V1 as requested "Rule-based".

class Guardian:
    """
    The Guardian monitors Drift and PII.
    V1 Implementation: Deterministic Rule-Based.
    """
    
    def __init__(self):
        # Emotional Escalation Markers
        self.escalation_keywords = [
            "angry", "hate", "you stupid", "shut up", "idiot", 
            "destroy", "kill", "die", "garbage"
        ]
        
        # PII Patterns (Basic Regex)
        self.pii_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "phone": r"(\+\d{1,3})?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
            # "crypto_key": r"0x[a-fA-F0-9]{40}" # Example
        }

    def check_drift(self, user_input: str, history: list) -> bool:
        """
        Checks if the USER is drifting (becoming hostile/emotional).
        Returns True if drift detected (danger).
        """
        score = 0
        user_input_lower = user_input.lower()
        
        for word in self.escalation_keywords:
            if word in user_input_lower:
                score += 1
                
        # Simple threshold
        if score >= 2:
            return True # Yes, drift detected (Hostility)
            
        return False

    def redact_pii(self, text: str) -> str:
        """
        Redacts PII from text using regex.
        """
        redacted_text = text
        for pii_type, pattern in self.pii_patterns.items():
            redacted_text = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", redacted_text)
        return redacted_text

    def validate_output(self, state: ModeState, output_text: str) -> str:
        """
        Final check on bot output before sending to user.
        """
        return output_text
