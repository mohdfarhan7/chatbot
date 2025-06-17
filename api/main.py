from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from typing import Optional, List, Dict, Any

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

# Rasa server URL from environment variable
RASA_API_URL = os.getenv("RASA_API_URL", "https://your-rasa-server-url.com")

class Message(BaseModel):
    sender_id: str
    message: str

class BotResponse(BaseModel):
    recipient_id: str
    text: str
    buttons: Optional[List[Dict[str, Any]]] = None

@app.post("/api/webhook", response_model=BotResponse)
async def webhook(message: Message):
    try:
        rasa_response = requests.post(
            f"{RASA_API_URL}/webhooks/rest/webhook",
            json={"sender": message.sender_id, "message": message.message},
            timeout=10
        )
        rasa_response.raise_for_status()
        
        rasa_data = rasa_response.json()
        if not rasa_data:
            return BotResponse(
                recipient_id=message.sender_id,
                text="I'm sorry, I couldn't process your request at the moment."
            )
        
        response = rasa_data[0]
        buttons = response.get("buttons")
        
        return BotResponse(
            recipient_id=message.sender_id,
            text=response.get("text", ""),
            buttons=buttons
        )
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Rasa: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/health")
async def health_check():
    try:
        response = requests.get(f"{RASA_API_URL}/status", timeout=5)
        response.raise_for_status()
        return {"status": "healthy", "rasa_status": "connected"}
    except:
        return {"status": "unhealthy", "rasa_status": "disconnected"}

@app.get("/")
async def root():
    return {"message": "Event Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 