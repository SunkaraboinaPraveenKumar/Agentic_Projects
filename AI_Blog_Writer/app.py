import streamlit as st
import requests

st.title("📝AI-Powered Blog Writer")

topic = st.text_input("Enter the Blog Topic:")

if st.button("Generate Blog"):
    with st.spinner("Generating Blog...."):
        response = requests.post("https://agentic-projects-blog-writer-backend.onrender.com/generate",json={"topic":topic})
        if response.status_code==200:
            result = response.json()
            st.subheader("Generated Blog")
            st.markdown(result["blog"])
        
        else:
            st.error("Error generating blog..")

    
