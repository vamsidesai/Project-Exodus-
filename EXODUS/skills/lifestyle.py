import random
from core.state import ModeState

class LifestyleAdvisor:
    """
    Health, Energy, and Side-Quest Engine.
    "Strict, honest advice."
    """
    
    def __init__(self):
        self.quests = [
            "Do 20 Pushups immediately.",
            "Drink 500ml water.",
            "Walk outside for 10 minutes.",
            "Read 5 pages of a physical book.",
            "Clean your desk."
        ]
        
    def generate_side_quest(self, energy_level="normal"):
        """Generates a daily side quest based on energy."""
        quest = random.choice(self.quests)
        return f"⚔️ **SIDE QUEST:** {quest} (Reward: +1 Clarity)"

    def check_health_query(self, query: str) -> str:
        """
        Filters health questions.
        Escalates if medical intervention is needed.
        """
        red_flags = ["chest pain", "bleeding", "faint", "numbness"]
        
        if any(flag in query.lower() for flag in red_flags):
            return "🚨 **MEDICAL EMERGENCY:** I am essentially a calculator. Call a doctor or emergency services. Do not ask me."
            
        return "I can offer lifestyle advice (sleep, diet, exercise), but I cannot diagnose. What's on your mind?"

    def advise_on_energy(self, state: ModeState, typing_speed="normal"):
        """
        Infers state from 'typing speed' (mocked) and suggests breaks.
        """
        if typing_speed == "sluggish":
            return "Detected fatigue. Suggest taking a 20min power nap or caffeine intake."
        return "Energy levels appear optimal. Continue grinding."
