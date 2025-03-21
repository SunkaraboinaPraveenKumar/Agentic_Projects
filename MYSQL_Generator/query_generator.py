import os
from groq import Groq
import sqlparse
import re
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database import engine, get_schema

# Load environment variables
load_dotenv()

groq=Groq()

def clean_sql_output(response_text):
    """Removes markdown formatting and extracts the raw SQL query."""
    # Remove Markdown code block formatting (```sql ... ```)
    clean_query = re.sub(r"```sql\n(.*?)\n```", r"\1", response_text, flags=re.DOTALL)
    sql_match = re.search(r"SELECT .*?;", clean_query, re.DOTALL | re.IGNORECASE)
    return sql_match.group(0) if sql_match else clean_query.strip()

def validate_sql_query(sql_query):
    """Validates the SQL query syntax before execution."""
    try:
        parsed = sqlparse.parse(sql_query)
        if not parsed:
            return False, "Invalid SQL syntax."
        return True, None
    except Exception as e:
        return False, str(e)

def generate_sql_query(nl_query):
    """Converts a natural language query into an optimized MySQL query using Groq's model."""
    schema = get_schema()
    schema_text = "\n".join([f"{table}: {', '.join(columns)}" for table, columns in schema.items()])
    
    prompt = f"""
    You are an SQL expert. Convert the following natural language query into an optimized MySQL query.
    Ensure:
    - Proper use of INDEXING where applicable.
    - Use of efficient JOINS instead of nested queries.
    - Use GROUP BY when aggregations are needed.
    - Ensure SQL is valid and optimized for execution.
    
    Database Schema:
    {schema_text}
    
    User Request: {nl_query}
    
    SQL Query:
    """
    
    try:
        response = groq.chat.completions.create(
            model="qwen-2.5-32b",
            messages=[
                {"role": "system", "content": "You are a SQL optimization expert."},
                {"role": "user", "content": prompt}
            ]
        )
        raw_sql_query = response.choices[0].message.content.strip()
        clean_query = clean_sql_output(raw_sql_query)
        return clean_query

    except Exception as e:
        print(f"Error generating SQL query with Groq: {e}")
        return None

def suggest_index(sql_query):
    """Suggests indexes for the executed SQL query."""
    try:
        with engine.connect() as connection:
            explain_query = f"EXPLAIN {sql_query}"
            result = connection.execute(text(explain_query))
            execution_plan = result.fetchall()
        print("\nQuery Execution Plan:")
        for row in execution_plan:
            print(row)
        return "Consider adding an index on frequently used WHERE conditions."
    except Exception as e:
        return f"Could not generate execution plan: {e}"

def execute_query(sql_query):
    """Executes a validated and optimized SQL query."""
    is_valid, error_msg = validate_sql_query(sql_query)
    if not is_valid:
        print(f"SQL Validation Error: {error_msg}")
        return None

    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            fetched_results = result.fetchall()
        index_suggestion = suggest_index(sql_query)
        return {"results": fetched_results, "optimization_tips": index_suggestion}
    except SQLAlchemyError as e:
        print(f"Database Execution Error: {str(e)}")
        return None

if __name__ == "__main__":
    user_input = input("Enter your natural language query: ")
    sql_query = generate_sql_query(user_input)
    
    if sql_query:
        print(f"\nGenerated SQL Query:\n{sql_query}")
        execution_results = execute_query(sql_query)
        if execution_results:
            print("\nQuery Results:")
            for row in execution_results["results"]:
                print(row)
            print("\nOptimization Tips:", execution_results["optimization_tips"])
        else:
            print("No results found or error executing query.")
    else:
        print("Failed to generate a valid SQL query.")
