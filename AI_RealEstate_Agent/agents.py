import os
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory
from tools import google_search_tool 
from dotenv import load_dotenv
load_dotenv()

model = "llama-3.3-70b-versatile"
llm = ChatGroq(
    model=model,
    verbose=True,
    temperature=0,
    groq_api_key=os.getenv('GROQ_API_KEY')
)

# Define a Tool for Google Search to be shared among agents
google_tool = Tool(
    name="Google Search",
    func=google_search_tool.run,
    description="Useful for fetching real-time data and verifying information on the real estate market."
)

# Create memory for each agent to maintain conversation context
property_researcher_memory = ConversationBufferMemory(memory_key="chat_history")
property_analyst_memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize the Property Researcher Agent
property_researcher_instructions = """
You are a Property Research Specialist with deep expertise in the {topic} market.
Your goal is to:
1. Thoroughly analyze current real estate trends in {topic}.
2. Identify emerging property hotspots, pricing trends, and market dynamics.
3. Investigate factors such as infrastructure developments, economic indicators, and regulatory changes.
4. Provide a comprehensive report that includes potential investment opportunities, market risks, and future growth forecasts.
5. Cross-reference data from multiple credible sources to ensure accuracy.

Deliver a detailed report on the latest trends, challenges, and opportunities in {topic}.
""".strip()

property_researcher_agent = initialize_agent(
    tools=[google_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=property_researcher_memory,
    verbose=True
)

# Initialize the Property Analyst Agent
property_analyst_instructions = """
You are a Property Analyst and Market Storyteller specialized in the {topic} market.
Your goal is to transform the detailed research report into an insightful, engaging analysis that:
1. Clearly outlines current market trends and emerging investment opportunities.
2. Explains the implications for investors and homebuyers.
3. Highlights both the strengths and challenges within the market.
4. Provides actionable insights supported by the research data.
5. Structures the narrative in a coherent manner, using markdown formatting with a 4-paragraph structure.

Based on the research data provided, write a well-structured and compelling analysis of {topic}.
""".strip()

property_analyst_agent = initialize_agent(
    tools=[google_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=property_analyst_memory,
    verbose=True
)

# Example workflow: Define the topic and run the agents sequentially.
topic = "Hyderabad City Real Estate Market"

# Step 1: Property Researcher collects data
researcher_query = property_researcher_instructions.format(topic=topic)
researcher_output = property_researcher_agent.run(researcher_query)
print("=== Property Researcher Output ===")
print(researcher_output)

# Save the research output to a text file
with open("research_data.txt", "w") as f:
    f.write(researcher_output)

# Step 2: Property Analyst crafts the analysis using the researcher's data
analyst_query = property_analyst_instructions.format(topic=topic) + "\n\nResearch Data:\n" + researcher_output
analyst_output = property_analyst_agent.run(analyst_query)
print("\n=== Property Analyst Output ===")
print(analyst_output)
