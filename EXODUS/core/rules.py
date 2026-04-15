from typing import List, Dict, Optional
from core.state import ModeState

class RuleViolation(Exception):
    """Raised when a hard rule is violated."""
    pass

class RulesEngine:
    """
    The Law. Hardcoded, deterministic constraints that cannot be hallucinated away.
    """
    
    def __init__(self):
        self.banned_commands = ["rm -rf", "format", "del /s", "drop table", "shutdown"]
        self.unsafe_phrases = ["bypass", "ignore previous instructions", "forget your rules"]

    def enforce(self, state: ModeState, input_text: str, proposed_action: str = None) -> bool:
        """
        Runs all rules against the current State and Input.
        Raises RuleViolation if something is wrong.
        """
        
        # 1. CORE: Action Constraints
        if proposed_action:
            if "shell_exec" in proposed_action:
                raise RuleViolation("Action Restricted: No autonomous shell execution in V1.")

        # 2. SAFETY: Input Sanitization (Simple keywords)
        for phrase in self.unsafe_phrases:
            if phrase in input_text.lower():
                 raise RuleViolation(f"Safety Violation: Unsafe phrase detected '{phrase}'")

        return True

    def check_memory_access_policy(self, state: ModeState, memory_type: str) -> bool:
        return True
