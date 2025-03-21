import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.google import GeminiEmbedder
from agno.tools.yfinance import YFinanceTools
import os
from dotenv import load_dotenv
import io
import re
from contextlib import redirect_stdout

# Load environment variables
load_dotenv()

# ---------------------------
# Define the Agents
# ---------------------------

# 1. Thai Recipes Agent (Thai cuisine expert with a PDF knowledge base)
thai_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    description="You are a Thai cuisine expert!",
    instructions=[
        "Search Your Knowledge base for Thai recipes",
        "If the question is better suited for the web search to fill in gaps.",
        "Prefer the information in your knowledge base over web based results."
    ],
    knowledge=PDFUrlKnowledgeBase(
        urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="recipes",
            search_type=SearchType.hybrid,
            embedder=GeminiEmbedder()
        ),
    ),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True
)

# 2. Web Agent (for simple web searches)
web_agent = Agent(
    name="Web Agent",
    role="Search the web for information..",
    model=Groq(id="qwen-2.5-32b"),
    description="You are assistant please reply based on the question",
    tools=[DuckDuckGoTools()],
    markdown=True,
    instructions="Always include the sources",
    show_tool_calls=True,
)

# 3. Finance Agent (to retrieve financial data)
finance_agent = Agent(
    name="Finance Agent",
    role="Get the financial Data..",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(
        stock_price=True,
        analyst_recommendations=True,
        stock_fundamentals=True,
        company_info=True,
        company_news=True
    )],
    markdown=True,
    instructions="Use Tables to display data",
    show_tool_calls=True,
)

# 4. Combined Team Agent for Finance and Web searches
team_agent = Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["Use Tables to display data", "Always include the sources"],
    show_tool_calls=True,
    markdown=True
)

# 5. Simple Web Search Agent (the one used for quick queries)
simple_web_agent = Agent(
    model=Groq(id="qwen-2.5-32b"),
    description="You are assistant please reply based on the question",
    tools=[DuckDuckGoTools()],
    markdown=True
)

# ---------------------------
# Build the Streamlit UI
# ---------------------------

# Set page configuration for a wide, professional layout
st.set_page_config(page_title="Advanced AGNO Agent Chat", layout="wide")

# Custom CSS styling for a modern look
st.markdown(
    """
    <style>
    /* Background colors and font styling */
    .reportview-container {
        background: #f0f2f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2e7bcf, #2e7bcf);
        color: white;
    }
    h1, h2, h3 {
        color: #2e7bcf;
    }
    .stButton>button {
        background-color: #2e7bcf;
        color: white;
        border: none;
        padding: 0.5em 1em;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True
)

# App Title and description
st.title("Advanced AGNO Agent Chat App")
st.markdown("### Select an Agent and Chat with It")

# Sidebar for agent selection
agent_choice = st.sidebar.radio(
    "Choose an Agent:",
    ("Thai Recipes Agent", "Finance & Web Team Agent", "Simple Web Search Agent")
)

# Chat interface: Input field for user's query
user_query = st.text_input("Enter your query:")

# Button to submit the query
if st.button("Send"):
    if user_query.strip() == "":
        st.warning("Please enter a valid query.")
    else:
        try:
            # Capture the printed output from print_response
            f = io.StringIO()
            with redirect_stdout(f):
                if agent_choice == "Thai Recipes Agent":
                    thai_agent.print_response(user_query)
                elif agent_choice == "Finance & Web Team Agent":
                    team_agent.print_response(user_query)
                elif agent_choice == "Simple Web Search Agent":
                    simple_web_agent.print_response(user_query)
                else:
                    print("No agent selected.")
            # Retrieve the output as a string
            response = f.getvalue()

            # Remove ANSI escape codes so the output renders cleanly in Streamlit
            clean_response = re.sub(r'\x1b\[[0-9;]*m', '', response)

            # Display the response. Assumes response is a markdown-formatted string.
            st.markdown("#### Agent Response:")
            st.markdown(clean_response)
        except Exception as e:
            st.error(f"An error occurred while processing your query: {e}")

# Optional: Display instructions or chat history here if needed.
st.markdown("---")
st.info("This app integrates multiple agents to handle different types of queries. Use the sidebar to select the appropriate agent for your query. Each agent uses advanced models and tools to deliver expert-level answers along with proper citations and data tables where applicable.")
