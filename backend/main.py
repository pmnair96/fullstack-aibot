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

# Deployment timestamp: 2025-07-13T00:25:00Z - Enhanced with multiple models and smart fallback
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

# OpenRouter configuration - Check multiple sources for API key
OPENROUTER_API_KEY = (
    os.getenv("OPENROUTER_API_KEY") or 
    "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"  # Fallback to new key
)
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat-v3-0324:free")
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "http://localhost:4200")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "Genie-AI-Assistant")

# Create uploads directory
UPLOAD_PATH = os.getenv("UPLOAD_PATH", "./uploads")
os.makedirs(UPLOAD_PATH, exist_ok=True)

async def call_openrouter_api(message: str, context: Optional[str] = None) -> str:
    """Call OpenRouter API for AI response"""
    # Force use of new API key
    current_api_key = "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"
    
    if not current_api_key or current_api_key == "your_openrouter_api_key_here":
        return f"Mock AI Response: I received your message '{message}'. This is a fallback response since OpenRouter API key is not configured."
    
    try:
        headers = {
            "Authorization": f"Bearer {current_api_key}",
            "HTTP-Referer": "https://zealous-feet.surge.sh",
            "X-Title": "Genie-AI-Assistant",
            "Content-Type": "application/json"
        }
        
        prompt = message
        if context:
            prompt = f"Context: {context}\n\nUser message: {message}"
        
        # Try multiple models in case one doesn't work
        models_to_try = [
            "meta-llama/llama-3.1-8b-instruct:free",
            "google/gemini-2.0-flash-exp:free", 
            "deepseek/deepseek-chat-v3-0324:free"
        ]
        
        for model in models_to_try:
            payload = {
                "model": model,
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
            
            print(f"Trying model: {model}")
            print(f"API Key (first 20 chars): {current_api_key[:20]}...")
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                print(f"Response status for {model}: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    return f"✅ {result['choices'][0]['message']['content']} (Model: {model})"
                elif response.status_code == 401:
                    print(f"Auth failed for {model}: {response.text[:200]}")
                    continue
                else:
                    print(f"Error {response.status_code} for {model}: {response.text[:200]}")
                    continue
        
        # If all models fail, try mock response
        mock_response = get_mock_ai_response(message)
        return f"🤖 Genie AI (Demo): {mock_response} \n\n(Note: Currently using demo mode while working on API connectivity)"
                
    except Exception as e:
        print(f"Exception in API call: {str(e)}")
        mock_response = get_mock_ai_response(message)
        return f"🤖 Genie AI (Demo): {mock_response} \n\n(Note: Currently using demo mode while working on API connectivity)"
                
    except Exception as e:
        print(f"Error calling OpenRouter API: {str(e)}")
        return f"🤖 Genie AI (Connection Error): I received your message '{message}'. There's a temporary connection issue with the AI service, but your message was processed successfully!"
                
    except Exception as e:
        print(f"Error calling OpenRouter API: {str(e)}")
        return f"I apologize, but I encountered an error while processing your request. Please try again later."

def get_mock_ai_response(message: str) -> str:
    """Generate a mock AI response for demonstration purposes"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! 👋 I'm Genie, your AI assistant. How can I help you today?"
    elif any(word in message_lower for word in ['how are you', 'how do you do']):
        return "I'm doing great, thank you for asking! I'm here and ready to help with any questions or tasks you have."
    elif any(word in message_lower for word in ['what can you do', 'help', 'capabilities']):
        return "I can help with a wide variety of tasks including answering questions, providing explanations, helping with writing, coding assistance, problem-solving, and much more. What would you like to explore?"
    elif any(word in message_lower for word in ['weather', 'time']):
        return "I don't have access to real-time data like weather or current time, but I can help with many other things! What else can I assist you with?"
    elif any(word in message_lower for word in ['thank', 'thanks']):
        return "You're very welcome! I'm happy to help. Is there anything else you'd like to know or discuss?"
    else:
        return f"That's an interesting point about '{message}'. I'd love to help you explore that topic further. Could you tell me more about what specific aspect you're most curious about?"

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
