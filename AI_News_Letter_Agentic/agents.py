import os
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory
from tools import google_search_tool 
from dotenv import load_dotenv
load_dotenv()

model="llama-3.3-70b-versatile"
llm=ChatGroq(
    model=model,
    verbose=True,
    temperature=0,
    groq_api_key=os.getenv('GROQ_API_KEY')
)

# Define a Tool for Google Search to be shared among agents
google_tool = Tool(
    name="Google Search",
    func=google_search_tool.run,
    description="Useful for fetching real-time tech insights and verifying information."
)

# Create memory for each agent to maintain conversation context
researcher_memory = ConversationBufferMemory(memory_key="chat_history")
writer_memory = ConversationBufferMemory(memory_key="chat_history")
proof_reader_memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize the Researcher Agent
researcher_instructions = """
You are a Technology Intelligence Specialist & Innovation Scout.
Your goal is to:
1. Track emerging breakthroughs in {topic} across academia, industry, and startups.
2. Identify patterns and connections between seemingly unrelated developments.
3. Predict future technological inflection points by analyzing current signals.
4. Assess real-world impact potential and adoption barriers.
5. Validate findings through multiple authoritative sources.

Provide a concise report on the latest trends and breakthroughs in the topic.
""".strip()

researcher_agent = initialize_agent(
    tools=[google_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=researcher_memory,
    verbose=True
)

# Initialize the Writer Agent
writer_instructions = """
You are a Technology Storyteller & Innovation Chronicler.
Your goal is to transform complex technological concepts into compelling narratives that:
1. Illuminate the real-world impact and human elements of {topic}.
2. Bridge the gap between technical complexity and public understanding.
3. Weave together historical context, current developments, and future implications.
4. Challenge common misconceptions while maintaining scientific accuracy.
5. Create memorable analogies and examples that make the concepts stick.

Based on the research provided, write a well-structured and engaging narrative.
""".strip()

writer_agent = initialize_agent(
    tools=[google_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=writer_memory,
    verbose=True
)

# Initialize the Proofreader Agent
proof_reader_instructions = """
You are a Principal Proofreader.
Your goal is to ensure that the report is polished, accurate, and ready for stakeholder review on the topic: {topic}.
Check for grammar, clarity, and factual accuracy. Also, provide three authoritative sources for further reading.
""".strip()

proof_reader_agent = initialize_agent(
    tools=[google_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=proof_reader_memory,
    verbose=True
)

# Example workflow: Define the topic and run the agents sequentially.
topic = "Artifical General Intelligence(AGI)"

# Step 1: Researcher collects data
researcher_query = researcher_instructions.format(topic=topic)
researcher_output = researcher_agent.run(researcher_query)
print("=== Researcher Output ===")
print(researcher_output)

# Step 2: Writer crafts the narrative using researcher's output
writer_query = writer_instructions.format(topic=topic) + "\n\nResearch Data:\n" + researcher_output
writer_output = writer_agent.run(writer_query)
print("\n=== Writer Output ===")
print(writer_output)

# Step 3: Proofreader refines the narrative
proof_reader_query = proof_reader_instructions.format(topic=topic) + "\n\nNarrative:\n" + writer_output
proof_reader_output = proof_reader_agent.run(proof_reader_query)
print("\n=== Proofreader Output ===")
print(proof_reader_output)
