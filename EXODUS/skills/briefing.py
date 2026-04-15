from datetime import datetime
from skills.search import WebSearchModule
from memory.vector_store import VectorMemory

class BriefingSkill:
    """
    Skill for generating a daily briefing by combining real-time news 
    and personal context from memory.
    """
    def __init__(self, search: WebSearchModule, memory: VectorMemory):
        self.search = search
        self.memory = memory

    def generate_briefing(self) -> str:
        """
        Creates a structured daily briefing.
        """
        now = datetime.now()
        date_str = now.strftime("%A, %d %B %Y")
        time_str = now.strftime("%H:%M")
        
        # 1. Fetch top news
        news = self.search.search_web("top global news today", max_results=2)
        
        # 2. Recall personal context / reminders
        personal = self.memory.recall("important reminders and personal goals", n_results=3)
        personal_context = "\n".join(personal) if personal else "No specific reminders found in memory."
        
        briefing = f"""
### ⬡ EXODUS DAILY BRIEFING
**DATE:** {date_str}
**TIME:** {time_str}

**🌍 GLOBAL SITUATION:**
{news}

**🧠 PERSONAL CONTEXT:**
{personal_context}

**---**
*How shall we proceed today?*
"""
        return briefing.strip()
