from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import json
from datetime import datetime

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "openrouter_configured": bool(os.getenv("OPENROUTER_API_KEY")),
        "environment": "production"
    }

@app.post("/api/chat/message")
async def chat_message(message: dict):
    try:
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        openrouter_model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat-v3-0324:free")
        
        if not openrouter_api_key:
            return {"response": "Hello! This is a demo response. Configure OPENROUTER_API_KEY for real AI responses."}
        
        # Call OpenRouter API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": openrouter_model,
                    "messages": [{"role": "user", "content": message.get("message", "")}],
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return {"response": result["choices"][0]["message"]["content"]}
            else:
                return {"response": "Sorry, I'm having trouble connecting to AI services right now."}
                
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

# For Vercel serverless functions
from mangum import Mangum
handler = Mangum(app)
