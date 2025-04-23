import streamlit as st
from agent_utils import get_search_results
from weather_utils import get_weather_response

st.set_page_config(page_title="🔎 GenAI Search & Weather Agent", page_icon="🤖")

st.title("🔍 Ask Web Search or Weather Agent...")

# Web Search Section
st.header("🌐 Web Search")
query = st.text_input("Enter your query:", placeholder="e.g. What are the latest trends in Generative AI?")
if st.button("Search"):
    if query.strip():
        with st.spinner("Searching..."):
            response = get_search_results(query)
        st.success("✅ Here's What I found:")
        st.write(response)
    else:
        st.warning("⚠️ Please enter a query before searching.")

# Weather Section
st.header("⛅ Weather Forecast")
weather_query = st.text_input("Enter a city for weather forecast:", placeholder="e.g. New York")
if st.button("Get Weather"):
    if weather_query.strip():
        with st.spinner("Fetching weather..."):
            weather_response = get_weather_response(weather_query)
        st.success("✅ Here's the weather forecast:")
        st.write(weather_response)
    else:
        st.warning("⚠️ Please enter a city name before fetching the weather.")