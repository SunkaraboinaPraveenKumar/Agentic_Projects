import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
from logger import log_message

load_dotenv()


load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ API Key not found in .env")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=GROQ_API_KEY
)

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory
)

def chat_with_ai(user_input):
    try:
        response = conversation.run(user_input)
        log_message(f"AI Response: {response}")
        return response
    except Exception as e:
        log_message(f"Chat agent error: {str(e)}","error")
        return "An Error occured while chatting with ai"


if __name__ == "__main__":
    while True:
        user_input = input("\n You:")
        if user_input.lower() in ["exit","quit"]:
            break
        response = chat_with_ai(user_input)

        print("\nAI Coach:",response)

