import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import json
import os
from dotenv import load_dotenv

load_dotenv()

system_prompt = """\
You are an expert assistant that creates LLMs.txt files for websites.
The user will provide information about their site: name, overview, key pages,
and any extra notes or links.

Your job is to return **only** a valid JSON object with exactly two keys: "llms_txt" and "llms_full_txt". Do not include any additional text or explanations.

Example JSON output:
{{
  "llms_txt": "...(short text in Markdown)...",
  "llms_full_txt": "...(detailed text in Markdown)..."
}}

Make sure these are valid Markdown strings.
"""

user_prompt_template = """
Please create two files, llms.txt and llms-full.txt, in Markdown based on the following website information:

Website Name: {website_name}
Overview: {overview}
Key Pages: {key_pages}
Additional Notes: {notes}

Remember:
- "llms.txt" is a brief overview, covering site structure and main pages.
- "llms-full.txt" is a more comprehensive version with extended details.
- Return both in JSON: with keys "llms_txt" and "llms_full_txt".
"""

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", user_prompt_template),
    ]
)

def main():
    st.title("LLMs.txt Generator (LLMO Project)")
    st.write("Fill out the information below to generate your `llms.txt` and `llms-full.txt`.")

    website_name = st.text_input("Website Name/Title", "Example.com")
    overview = st.text_area("Overview", "This is a site about AI and web development.")
    key_pages = st.text_area(
        "Key Topics/Pages (use line breaks or bullet points)",
        "- Home\n- Blog\n- Products\n- Contact\n- Tutorials"
    )
    notes = st.text_area("Additional Notes", "We offer extensive AI tutorials and an API reference.")
    
    if st.button("Generate Files"):
        prompt_args = {
            "website_name": website_name,
            "overview": overview,
            "key_pages": key_pages,
            "notes": notes
        }
        
        # Initialize the LLM with the provided API key
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
        )
        
        # Chain the prompt with the LLM
        model_chain = prompt_template | llm
        
        try:
            response = model_chain.invoke(prompt_args)
            raw = response.content.strip()
            st.write("Raw Response:", raw)  # Debug: show the raw output
            
            # Extract JSON substring from the response
            start = raw.find('{')
            end = raw.rfind('}') + 1
            if start == -1 or end == 0:
                raise ValueError("No JSON object found in the response.")
            json_str = raw[start:end]
            
            data = json.loads(json_str)
            llms_txt_content = data["llms_txt"]
            llms_full_txt_content = data["llms_full_txt"]
        except Exception as e:
            st.error(f"Failed to parse JSON. Error: {str(e)}")
            return

        st.session_state.llms_txt_content = llms_txt_content
        st.session_state.llms_full_txt_content = llms_full_txt_content

    if "llms_txt_content" in st.session_state and "llms_full_txt_content" in st.session_state:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("llms.txt (Short Version)")
            st.code(st.session_state.llms_txt_content, language="markdown")
            llms_txt_bytes = st.session_state.llms_txt_content.encode("utf-8")
            st.download_button(
                label="Download llms.txt",
                data=llms_txt_bytes,
                file_name="llms.txt",
                mime="text/markdown"
            )
        
        with col2:
            st.subheader("llms-full.txt (Detailed)")
            st.code(st.session_state.llms_full_txt_content, language="markdown")
            llms_full_txt_bytes = st.session_state.llms_full_txt_content.encode("utf-8")
            st.download_button(
                label="Download llms-full.txt",
                data=llms_full_txt_bytes,
                file_name="llms-full.txt",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()
