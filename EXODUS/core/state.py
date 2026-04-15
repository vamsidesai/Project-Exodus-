from dataclasses import dataclass

@dataclass
class ModeState:
    """
    Simplified state for the public chatbot mode.
    """
    mode: str = "PUBLIC"
    
    def to_dict(self):
        return {
            "mode": self.mode
        }

    def reset(self):
        pass
