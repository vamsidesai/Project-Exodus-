from duckduckgo_search import DDGS

class WebSearchModule:
    """
    Live web search skill using DuckDuckGo to answer current events 
    or real-time specific questions.
    """
    def __init__(self):
        self.ddgs = DDGS()

    def search_web(self, query: str, max_results: int = 3) -> str:
        try:
            results = self.ddgs.text(query, max_results=max_results)
            context = []
            for r in results:
                context.append(f"Title: {r.get('title')}\nSnippet: {r.get('body')}\nURL: {r.get('href')}")
            
            if not context:
                return "No recent search results found for this query."
                
            return "\n\n".join(context)
        except Exception as e:
            return f"Web Search Error: {str(e)}"
