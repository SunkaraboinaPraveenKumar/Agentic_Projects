from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY=os.getenv('GROQ_API_KEY')

def generate_blog(topic):
    """"Generate a full blog post based on a given topic using Groq Model: qwen-2.5-32b"""
    template="""
    Write a detailed blog post on the topic: "{topic}".
    - Include an engaging introduction.
    - Provide 3 key points with explanations
    - Use SEO-friendly keywords
    - End with a conclusion and call to action

    Return blog in structured markdown format.
    """

    prompt=PromptTemplate(input_variables=['topic'],template=template)

    llm=ChatGroq(
        model="qwen-2.5-32b",
        api_key=GROQ_API_KEY   
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.run(topic=topic)
