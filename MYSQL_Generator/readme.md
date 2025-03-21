# 🚀 AI-Powered SQL Query Generator

An AI-driven tool that converts **natural language queries into optimized SQL queries** and executes them in a MySQL database.  
Built with **FastAPI**, **Streamlit**, and **GROQ MODELS**.

---

## 📌 Features
✅ Convert **natural language to SQL** using OpenAI (GPT-4)  
✅ **Execute SQL queries** in a MySQL database  
✅ **Query validation** & **indexing suggestions** for optimization  
✅ Interactive **web UI with Streamlit**  
✅ **FastAPI backend** with REST API support  

---

## 🛠️ Tech Stack
- **Backend:** FastAPI, SQLAlchemy, OpenAI API
- **Frontend:** Streamlit
- **Database:** MySQL
- **AI Model:** GROQ API
- **Deployment:** Uvicorn (for FastAPI), Streamlit Cloud (for UI)

---

## 🚀 Setup & Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/<your-github-username>/AI-Powered-SQL-Query-Generator.git
cd AI-Powered-SQL-Query-Generator


##  Create a Virtual Environment & Install Dependencie

python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
pip install -r requirements.txt

##  Set Up Environment Variables

Create a .env file in the project root and add:

# MySQL Database Config
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=my_password
MYSQL_DATABASE=test_db
MYSQL_PORT=3306

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key


🏗️ Running the Application
1️⃣ Start FastAPI Backend

uvicorn app:app --reload

2️⃣ Start Streamlit UI

streamlit run ui.py
