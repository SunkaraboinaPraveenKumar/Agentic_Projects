import streamlit as st
import requests
import pandas as pd

# Set page title
st.title("🔍 AI-Powered SQL Query Generator")

query_input = st.text_input("Enter your natural language query...")

if st.button("Generate SQL"):
    response = requests.post("http://127.0.0.1:8000/generate_sql/", json={"query": query_input})
    sql_query = response.json().get("sql_query", "Error generating query")
    st.code(sql_query, language="sql")
    st.session_state["generated_sql"] = sql_query

if "generated_sql" in st.session_state:
    if st.button("Execute SQL"):
        response = requests.post("http://127.0.0.1:8000/execute_sql/", json={"query": st.session_state["generated_sql"]})
        response_json = response.json()
        results = response_json.get("results", [])
        optimization_tips = response_json.get("optimization_tips", "No optimization tips available.")
        
        st.subheader("Query Results:")
        if results:
            # Convert results (list of dicts) to a DataFrame and display as a table
            df = pd.DataFrame(results)
            st.table(df)
        else:
            st.write("No results found.")
        
        st.subheader("Optimization Tips:")
        st.write(optimization_tips)
