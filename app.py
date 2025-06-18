from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import os
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
client = OpenAI(api_key=OPENAI_API_KEY)

# Database configuration
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", "3306"))
}

# Initialize FastAPI app
app = FastAPI(
    title="Event Chatbot API",
    description="API for interacting with the Event Chatbot",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Database connection error: {err}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Models
class Message(BaseModel):
    sender_id: str
    message: str

class BotResponse(BaseModel):
    recipient_id: str
    text: str
    buttons: Optional[List[Dict[str, Any]]] = None

# Utility functions
def fix_sql_year(sql: str) -> str:
    current_year = str(datetime.now().year)
    return sql.replace("2022", current_year)

def get_sql_from_gpt(user_query: str) -> str:
    prompt = f"""
You are an AI that converts natural language questions into MySQL SELECT queries.

The database has a table named `events` with these columns:
id, title, address, lat, long, date_time, about, category_id, rating, user_id, created_at, link, visible_date, recurring, end_date, weekdays, dates, all_time, selected_weeks.

Rules:
- `date_time` is a string like '20/06/2025,20 : 30'
- Use STR_TO_DATE(date_time, '%d/%m/%Y,%H : %i') for comparisons
- Use:
    STR_TO_DATE(date_time, '%d/%m/%Y,%H : %i') >= ...
    AND STR_TO_DATE(date_time, '%d/%m/%Y,%H : %i') < ...
- `category_id` mappings:
    • music → 6
    • sports → 3
    • art → 4
    • education → 5
    • tech → 2
    • food → 7

Return only a valid SELECT query. No markdown, no comments.
Always use LIMIT 10.

User query: "{user_query}"
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        sql = response.choices[0].message.content.strip().strip('`').replace("```sql", "").replace("```", "")
        return sql
    except Exception as e:
        logger.error(f"Error generating SQL: {e}")
        raise HTTPException(status_code=500, detail="Error generating SQL query")

def format_results_with_gpt(results: List[Dict]) -> str:
    if not results:
        return "No matching events found."

    prompt = f"""
You are an AI assistant that formats a list of event data into a user-friendly summary.
Include:
- Title 
- Date & Time 
- Location 
- Link  (if available)
- Rating 
- About  (max 300 chars)

Use line breaks, no JSON, no markdown.

Data:
{results}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error formatting results: {e}")
        return "Error formatting results. Please try again."

# Routes
@app.post("/api/webhook", response_model=BotResponse)
async def webhook(message: Message):
    try:
        # Handle greetings
        query_lower = message.message.lower()
        greetings = ["hi", "hello", "hey", "hola", "hii", "hiii", "greetings"]
        exits = ["ok", "bye", "goodbye", "thank you", "thanks", "see you"]

        if query_lower in greetings:
            return BotResponse(
                recipient_id=message.sender_id,
                text="👋 Hello! I'm your event assistant. Ask me things like 'Events in June', 'Concerts in Malta', or 'What's happening next weekend?'"
            )

        if query_lower in exits:
            return BotResponse(
                recipient_id=message.sender_id,
                text="👋 Thank you! Have a great day. I'm here if you need help with events later!"
            )

        # Generate SQL and fetch results
        sql = get_sql_from_gpt(message.message)
        if not sql.lower().startswith("select"):
            return BotResponse(
                recipient_id=message.sender_id,
                text="❓ Sorry, I couldn't understand your request. Try asking about events by date, location, or category."
            )

        sql = fix_sql_year(sql)
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return BotResponse(
                recipient_id=message.sender_id,
                text="❌ No matching event details found. Try using different keywords, dates, or categories."
            )

        formatted_output = format_results_with_gpt(results)
        return BotResponse(
            recipient_id=message.sender_id,
            text=formatted_output
        )

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return BotResponse(
            recipient_id=message.sender_id,
            text="⚠️ Something went wrong. Please try again or ask in a different way."
        )

@app.get("/api/health")
async def health_check():
    try:
        # Check database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/")
async def root():
    return {
        "message": "Event Chatbot API is running",
        "version": "1.0.0",
        "status": "operational"
    }

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port) 