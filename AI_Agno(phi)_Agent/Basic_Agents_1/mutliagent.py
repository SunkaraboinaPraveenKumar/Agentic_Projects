from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
import os
from dotenv import load_dotenv
from agno.tools.yfinance import YFinanceTools

load_dotenv()

web_agent=Agent(
    name="Web Agent",
    role="Search the web for information..",
    model=Groq(id="qwen-2.5-32b"),
    description="You are assistant please reply based on the question",
    tools=[DuckDuckGoTools()],
    markdown=True,
    instructions="Always include the sources",
    show_tool_calls=True,
)

finance_agent=Agent(
    name="Finance Agent",
    role="Get the financial Data..",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_info=True, company_news=True)],
    markdown=True,
    instructions="Use Tables to display data",
    show_tool_calls=True,
)



agent_team=Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["Use Tables to display data","Always include the sources"],
    show_tool_calls=True,
    markdown=True
)

agent_team.print_response("Anlayze the company stock data like NVIDIA, Apple, Meta, Google and Tesla and give a comparision and suggestions.")



