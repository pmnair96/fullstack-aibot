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

app = FastAPI(title="Genie AI Assistant API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:4200")],
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
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"OpenRouter API error: {response.status_code} - {response.text}")
                return f"I apologize, but I'm having trouble connecting to the AI service right now. Error: {response.status_code}"
                
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
async def chat_endpoint(
    message: str = Form(...),
    files: List[UploadFile] = File(default=[])
):
    """Chat endpoint that handles messages and optional file uploads"""
    try:
        # Handle file uploads
        file_context = ""
        uploaded_files = []
        
        if files:
            for file in files:
                if file and file.filename:
                    # Generate unique filename
                    file_extension = os.path.splitext(file.filename)[1]
                    unique_filename = f"{uuid.uuid4()}{file_extension}"
                    file_path = os.path.join(UPLOAD_PATH, unique_filename)
                    
                    # Save file
                    async with aiofiles.open(file_path, 'wb') as f:
                        content = await file.read()
                        await f.write(content)
                    
                    uploaded_files.append({
                        "original_name": file.filename,
                        "saved_name": unique_filename,
                        "size": len(content),
                        "type": file.content_type
                    })
                    
                    # Read file content for context (text files only)
                    if file.content_type and file.content_type.startswith('text/'):
                        try:
                            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                                file_content = await f.read()
                                file_context += f"\n\nFile '{file.filename}' content:\n{file_content[:1000]}..."
                        except Exception as e:
                            file_context += f"\n\nFile '{file.filename}' uploaded but could not read content: {str(e)}"
                    else:
                        file_context += f"\n\nFile '{file.filename}' uploaded (binary file, {len(content)} bytes)"
        
        # Get AI response
        ai_response = await call_openrouter_api(message, file_context if file_context else None)
        
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
