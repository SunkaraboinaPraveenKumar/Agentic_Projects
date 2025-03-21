from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
import os
from dotenv import load_dotenv

load_dotenv()

agent=Agent(
    model=Groq(id="qwen-2.5-32b"),
    description="You are assistant please reply based on the question",
    tools=[DuckDuckGoTools()],
    markdown=True
)

agent.print_response("What won India Vs New Zealand Champions Trophy 2025?")




