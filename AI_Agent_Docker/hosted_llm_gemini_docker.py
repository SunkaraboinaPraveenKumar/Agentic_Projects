import google.generativeai as genai
import os

os.environ['GOOGLE_API_KEY']=os.getenv('GEMINI_API_KEY')

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model=genai.GenerativeModel('gemini-2.0-flash')

PROMPT="""
Generate an ideal Dockerfile for {language} with best practices. Just Share the dockerfile without any explanation between two lines to make copying dockefile easy.
Include:
- Base image
- Installing dependencies
- Setting working directory
- Adding source code
- Running the application
"""

def generate_dockerfile(language):
    response = model.generate_content(PROMPT.format(language=language))
    return response.text


if __name__=="__main__":
    language=input("Enter the programming language:")
    dockerfile=generate_dockerfile(language)
    print("\nGenerated Dockerfile:\n")
    print(dockerfile)