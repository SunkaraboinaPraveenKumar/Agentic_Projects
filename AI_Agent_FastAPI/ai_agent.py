from dotenv import load_dotenv
load_dotenv()

import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

from langchain_groq import ChatGroq

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
# Initialize Groq LLMs (if needed globally)
primary_groq_llm = ChatGroq(model="llama-3.3-70b-versatile")
alternate_groq_llm = ChatGroq(model="llama-3.2-11b-vision-preview")

# Initialize DuckDuckGo Search Tool with default max_results=5
search_tool = DuckDuckGoSearchTool()

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt = "Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    # Rename the local variable to avoid any naming conflicts.
    if provider == "Groq":
        agent_llm = ChatGroq(model=llm_id)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    # Use our custom search tool's run method if web search is allowed
    tools = [search_tool.run] if allow_search else []
    
    agent = create_react_agent(
        model=agent_llm,
        tools=tools,
        state_modifier=system_prompt
    )

    state = {"messages": query}
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]
