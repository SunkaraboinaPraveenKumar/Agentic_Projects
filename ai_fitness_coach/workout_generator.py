import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from logger import log_message

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ API Key not found in .env")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=GROQ_API_KEY
)

workout_prompt = PromptTemplate(
    input_variables=["fitness_lavel","goal","duration","equipment"],
    template=(
        "Create a personalized workout plan for a {fitness_level} individual "
        "whose goal is {goal}. The workout should last {duration} minutes "
        "and use {equipment} equipment. Provide step-by-step excercises"
    )
)

def generate_workout(fitness_level,goal,duration,equipment):
    prompt = workout_prompt.format(
        fitness_level=fitness_level,
        goal=goal,
        duration=duration,
        equipment=equipment
    )

    try:
        response = llm.invoke(prompt)
        log_message("workout plan generated successfully")
        return response.content
    except Exception as e:
        log_message(f"Workout generation failed: {str(e)}","error")
        return f"Error: {str(e)}"
    

if __name__ == "__main__":
    test_workout = generate_workout("Beginner","Weight Loss","30","Bodyweight")
    print(test_workout)