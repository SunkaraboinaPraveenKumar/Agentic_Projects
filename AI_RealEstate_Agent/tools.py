from duckduckgo_search import DDGS  # Correct import

class DuckDuckGoSearchTool:
    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    def run(self, query: str) -> str:
        """
        Perform a DuckDuckGo search and return formatted results.
        """
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=self.max_results)]
            
            if results:
                formatted_results = "\n".join(
                    f"{idx + 1}. {result.get('title', 'No Title')}: {result.get('href', 'No URL')}"
                    for idx, result in enumerate(results)
                )
                return formatted_results
            return "No results found."
        except Exception as e:
            return f"An error occurred: {str(e)}"

google_search_tool = DuckDuckGoSearchTool()