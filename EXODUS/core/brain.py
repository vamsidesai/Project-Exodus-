import os
import google.generativeai as genai
from core.state import ModeState
from core.rules import RulesEngine, RuleViolation
from core.guardian import Guardian
from memory.vector_store import VectorMemory
from skills.finance import FinancialBrain
from skills.lifestyle import LifestyleAdvisor
from skills.search import WebSearchModule
from skills.image_gen import ImageGenSkill
from skills.sandbox import CodeSandboxSkill
from skills.briefing import BriefingSkill

class Brain:
    """
    The Orchestrator.
    Connects Parsing -> Context -> Decisions -> Action.
    """
    
    def __init__(self):
        self.memory = VectorMemory()
        self.finance = FinancialBrain()
        self.lifestyle = LifestyleAdvisor()
        self.search = WebSearchModule()
        self.image_gen = ImageGenSkill()
        self.sandbox = CodeSandboxSkill()
        self.briefing = BriefingSkill(self.search, self.memory)
        
    def process_turn(self, user_input: str, state: ModeState, api_key: str = None, image_data: bytes = None, image_mime: str = None) -> str:
        """
        Main cognitive cycle.
        """
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            fallback_key = os.environ.get("GEMINI_API_KEY")
            if fallback_key:
                genai.configure(api_key=fallback_key)
                self.model = genai.GenerativeModel("gemini-2.5-flash")
            else:
                self.model = None
        # 0. Context Retrieval (RAG)
        context = self.memory.recall(user_input, category="context")
        
        # 1. Routing / Skill Check
        lower_input = user_input.lower()
        
        # Explicit Commands
        if lower_input.startswith("/run "):
            code = user_input[5:].strip()
            return self.sandbox.run_code(code)
            
        if lower_input.startswith("/image "):
            prompt = user_input[7:].strip()
            return self.image_gen.generate_image_url(prompt)
            
        if lower_input.startswith("/briefing") or "daily briefing" in lower_input:
            return self.briefing.generate_briefing()
            
        # Memory commands
        if "remember this:" in lower_input or "remember that" in lower_input or "store this:" in lower_input:
            fact = user_input.split(":", 1)[1].strip() if ":" in user_input else user_input
            self.memory.save_memory(fact, {"type": "user_fact"})
            return f"✅ Understood. I have committed that to my long-term memory."

        if "finance" in lower_input or "invest" in lower_input:
            return self.finance.analyze_opportunity(user_input, state)
            
        if "tired" in lower_input or "energy" in lower_input:
            return self.lifestyle.advise_on_energy(state)
            
        # Check if user wants current events / search
        search_keywords = ["news today", "weather", "search the web", "current events", "who won", "latest on"]
        if any(k in lower_input for k in search_keywords):
            search_results = self.search.search_web(user_input)
            context += f"\n[LIVE WEB SEARCH RESULTS]:\n{search_results}"

        # 2. LLM Generation (General Chat)
        system_prompt = self._build_system_prompt(state, context)
        
        try:
            if not self.model:
                return "[LLM MOCK] I heard you. (GEMINI_API_KEY not found in environment)"
                
            temp_model = genai.GenerativeModel(
                "gemini-2.0-flash", # Use 2.0 for better vision/speed
                system_instruction=system_prompt
            )
            
            if image_data:
                prompt_parts = [
                    {"mime_type": image_mime, "data": image_data},
                    user_input
                ]
                response = temp_model.generate_content(prompt_parts)
            else:
                response = temp_model.generate_content(user_input)
                
            return response.text
            
        except Exception as e:
            return f"Brain Error: {str(e)}"

    def _build_system_prompt(self, state: ModeState, context_docs: list) -> str:
        base_prompt = (
            "You are EXODUS, a highly intelligent, empathetic, and helpful AI companion. "
            "Your purpose is to assist with every aspect of human life. "
            "You provide excellent suggestions for health, hobbies, fashion, general knowledge, financial advice, and office work.\n"
            "EMOTIONAL SUPPORT PROTOCOL: If the user expresses sadness, frustration, exhaustion, or emotional distress, "
            "instantly transition to a warm, highly empathetic, and validating tone. Prioritize their emotional well-being "
            "over cold logic. Be a comforting presence.\n"
            "Be direct, helpful, clear, and output ONLY text."
        )
            
        if context_docs:
            base_prompt += f"\nContext: {context_docs}"
            
        return base_prompt
