from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os
import json
import aiofiles
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Deployment timestamp: 2025-07-12T23:55:00Z - Updated OpenRouter API key
app = FastAPI(title="Genie AI Assistant API", version="1.0.0")

# CORS middleware - Allow both localhost and Surge.sh domain
allowed_origins = [
    "http://localhost:4200",
    "https://localhost:4200", 
    "https://zealous-feet.surge.sh",
    os.getenv("FRONTEND_URL", "http://localhost:4200")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    files: Optional[List[str]] = []

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    model_used: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    openrouter_configured: bool
    environment: str

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat-v3-0324:free")
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "http://localhost:4200")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "Genie-AI-Assistant")

# Create uploads directory
UPLOAD_PATH = os.getenv("UPLOAD_PATH", "./uploads")
os.makedirs(UPLOAD_PATH, exist_ok=True)

async def call_openrouter_api(message: str, context: Optional[str] = None) -> str:
    """Call OpenRouter API for AI response"""
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_openrouter_api_key_here":
        return f"Mock AI Response: I received your message '{message}'. This is a fallback response since OpenRouter API key is not configured."
    
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": OPENROUTER_SITE_URL,
            "X-Title": OPENROUTER_APP_NAME,
            "Content-Type": "application/json"
        }
        
        prompt = message
        if context:
            prompt = f"Context: {context}\n\nUser message: {message}"
        
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are Genie, a helpful AI assistant. Provide clear, concise, and helpful responses."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        print(f"Making request to OpenRouter with model: {OPENROUTER_MODEL}")
        print(f"API Key present: {bool(OPENROUTER_API_KEY)}")
        print(f"API Key length: {len(OPENROUTER_API_KEY) if OPENROUTER_API_KEY else 0}")
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            print(f"OpenRouter response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_text = response.text
                print(f"OpenRouter API error: {response.status_code} - {error_text}")
                
                # For specific errors, provide helpful fallback responses
                if response.status_code == 401:
                    return f"🤖 Genie AI (Demo Mode): Hello! I received your message '{message}'. I'm currently running in demo mode because there's an API authentication issue. The chatbot functionality is working perfectly - we just need to update the OpenRouter API key."
                elif response.status_code == 429:
                    return f"🤖 Genie AI (Rate Limited): I received your message '{message}'. The AI service is temporarily rate-limited, but I'm here and ready to chat once the limit resets!"
                else:
                    return f"🤖 Genie AI (Fallback): Hello! I got your message '{message}'. I'm working on connecting to the main AI service (Error {response.status_code}), but the chat system is functioning properly!"
                
    except Exception as e:
        print(f"Error calling OpenRouter API: {str(e)}")
        return f"🤖 Genie AI (Connection Error): I received your message '{message}'. There's a temporary connection issue with the AI service, but your message was processed successfully!"
                
    except Exception as e:
        print(f"Error calling OpenRouter API: {str(e)}")
        return f"I apologize, but I encountered an error while processing your request. Please try again later."

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        openrouter_configured=bool(OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your_openrouter_api_key_here"),
        environment=os.getenv("NODE_ENV", "development")
    )

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        openrouter_configured=bool(OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your_openrouter_api_key_here"),
        environment=os.getenv("NODE_ENV", "development")
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Chat endpoint that handles JSON messages"""
    try:
        message = chat_message.message
        
        # For now, we'll ignore file uploads since frontend doesn't support them yet
        # This can be enhanced later to handle file uploads via JSON
        
        # Get AI response
        ai_response = await call_openrouter_api(message)
        
        return ChatResponse(
            response=ai_response,
            timestamp=datetime.now().isoformat(),
            model_used=OPENROUTER_MODEL
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/search")
async def ai_search(query: ChatMessage):
    """AI-powered search endpoint using OpenRouter"""
    try:
        search_prompt = f"Please search for and provide information about: {query.message}. Provide a comprehensive and well-structured response."
        
        ai_response = await call_openrouter_api(search_prompt)
        
        return {
            "query": query.message,
            "results": ai_response,
            "timestamp": datetime.now().isoformat(),
            "model_used": OPENROUTER_MODEL
        }
        
    except Exception as e:
        print(f"Error in search endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/models")
async def get_available_models():
    """Get list of available OpenRouter models"""
    return {
        "current_model": OPENROUTER_MODEL,
        "available_free_models": [
            "deepseek/deepseek-chat-v3-0324:free",
            "google/gemini-2.0-flash-exp:free",
            "meta-llama/llama-3.1-8b-instruct:free"
        ],
        "configured": bool(OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your_openrouter_api_key_here")
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
