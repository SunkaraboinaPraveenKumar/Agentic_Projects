import streamlit as st
from agent_utils import get_search_results

st.set_page_config(page_title="🔎 GenAI Search Agent", page_icon="🤖")

st.title("🔍 Ask Web Search Agent...")
query = st.text_input("Enter your query:", placeholder="e.g. What are the latest trends in Generative AI?")

if st.button("Search"):
    if query.strip():
        with st.spinner("Searching..."):
            response = get_search_results(query)
        st.success("✅ Here's What I found:")
        st.write(response)
    else:
        st.warning("⚠️ Please enter a query before searching.")