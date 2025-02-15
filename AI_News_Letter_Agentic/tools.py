from duckduckgo_search import duckduckgo_search

class DuckDuckGoSearchTool:
    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    def run(self, query: str) -> str:
        """
        Perform a DuckDuckGo search and return formatted results.
        """
        results = duckduckgo_search(query, max_results=self.max_results)
        if results:
            formatted_results = "\n".join(
                f"{idx + 1}. {result.get('title', 'No Title')}: {result.get('href', 'No URL')}"
                for idx, result in enumerate(results)
            )
            return formatted_results
        return "No results found."

google_search_tool = DuckDuckGoSearchTool()
