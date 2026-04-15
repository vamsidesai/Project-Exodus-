from core.state import ModeState
from core.rules import RuleViolation

class FinancialBrain:
    """
    Financial Intelligence & Risk Governor.
    Requirement: Knowledge of Trading, Crypto, SaaS, etc.
    Constraint: NO SCAMS, NO RECKLESS STRATEGIES.
    """
    
    def __init__(self):
        self.risky_assets = ["shitcoin", "memecoin", "100x leverage", "ponzi"]
        self.safe_strategies = ["index_fund", "dividend", "value_investing", "saas_bootstrapping"]

    def analyze_opportunity(self, topic: str, state: ModeState) -> str:
        """
        Analyzes a financial opportunity.
        Enforces Policy: No 'Get Rich Quick' advice.
        """
        topic_lower = topic.lower()
        
        # 1. SCAM FILTER
        if any(bad in topic_lower for bad in self.risky_assets):
            return "⚠️ HIGH RISK ALERT: This looks speculative or dangerous. My protocols advise against this path."

        # 2. ANALYSIS LOGIC (Mocked for V1)
        if "crypto" in topic_lower:
            return ("Crypto Analysis: High Volatility. Recommend strict risk management (1-5% portfolio). "
                    "Focus on Blue chips (BTC/ETH). Avoid new launches without utility.")
        
        if "saas" in topic_lower:
            return ("SaaS Strategy: Focus on solving a specific B2B pain point. "
                    "Validate before building. Zero-to-One cost should be minimal.")
        
        return "I can analyze this, but I need more specific details. Is this for Trading, Investing, or Business?"

    def get_market_mood(self):
        # Todo: Integration with Yahoo Finance API
        return "Market API Disconnected. Assuming Neutral/Cautious."
