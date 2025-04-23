# agent_utils.py
import os
from pydantic_ai.agent import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from dotenv import load_dotenv

load_dotenv()

# Define and export the agent
agent = Agent(
    "groq:llama-3.1-8b-instant",
    tools=[duckduckgo_search_tool()],
    verbose=True,
    system_prompt = 'Search using DuckDuckGo for the given query and return the results and response accordingly.'
)

def get_search_results(query: str) -> str:
    result = agent.run_sync(query)
    return result.output