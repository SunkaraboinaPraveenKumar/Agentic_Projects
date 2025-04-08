import os
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.5
)

class WaterIntakeAgent:
    def __init__(self):
        self.history = []
    
    def analyze_intake(self, intake_ml):
        prompt = f"""
        You are a hydration assistant.
        The user has consumed {intake_ml} ml of water today.
        Provide hydration status and suggest if they need to drink more water.
        """
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content

    def analyze_history(self, history):
        """
        Given a list of tuples (intake_ml, date), construct a prompt for historical intake analysis.
        This prompt may include trends or suggestions for improving hydration habits.
        """
        if not history:
            return "No intake history to analyze."
        
        # Optionally, you can create a summary of the history; for a simple example, join each record.
        history_lines = [f"On {date}, consumed {intake} ml." for intake, date in history]
        history_text = "\n".join(history_lines)
        
        prompt = f"""
        You are a hydration expert. Given the following water intake history:
        
        {history_text}
        
        Please analyze the hydration trends, provide insights on the user’s water consumption habits,
        and suggest ways they might improve their hydration if needed.
        """
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content

if __name__ == "__main__":
    agent = WaterIntakeAgent()
    intake = 1500
    feedback = agent.analyze_intake(intake_ml=intake)
    print(f"Hydration Analysis: {feedback}")
