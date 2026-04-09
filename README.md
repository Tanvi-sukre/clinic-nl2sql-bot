🏥 Clinic AI Assistant - NL2SQL API

This project is a high-performance FastAPI application that translates natural language questions into precise SQL queries to interact with a Clinic Management Database. It utilizes Vanna 2.0 and Google Gemini 1.5 Flash to provide a seamless "Chat with Data" experience.

🌟 Key Features

Natural Language to SQL: Query your database using plain English.

Vanna 2.0 Integration: Leveraging advanced Agent-based RAG for high-accuracy SQL generation.

Step 7 Security Validation: A custom security layer that intercepts and blocks dangerous SQL commands (DROP, DELETE, UPDATE, etc.) to ensure database integrity.

Automated Schema Training: Includes scripts to seed the AI with specific database context for reliable results.

🚀 Getting Started

1. Installation

Install the required dependencies using pip:

pip install fastapi uvicorn vanna python-dotenv google-genai pandas


2. Configuration

Create a .env file in the root directory and add your Google Gemini API Key:

GOOGLE_API_KEY=your_actual_api_key_here


3. Database & AI Initialization

Run the following scripts in order to build the database and train the AI:

python setup_database.py  # Creates clinic.db with 200+ records
python seed_memory.py      # Trains the AI agent on your schema


4. Running the API

Start the FastAPI server:

uvicorn main:app --reload


Interactive API docs are available at: http://127.0.0.1:8000/docs

🛡️ Security Protocol (Step 7)

Following the project requirements, all generated SQL is passed through a validation engine before execution:

Whitelisted: Only SELECT statements are permitted.

Blacklisted: Commands like DROP, DELETE, INSERT, ALTER, and TRUNCATE are strictly blocked.

Response: Any violation returns a 400 Bad Request security alert.

📂 File Structure

main.py: Core FastAPI application and security logic.

vanna_setup.py: Configuration for LLM, SQL Runner, and AI Agent.

setup_database.py: Mock data generation for the clinic system.

seed_memory.py: Logic for training the AI on domain-specific knowledge.

RESULTS.md: Full report of tested queries and results.
