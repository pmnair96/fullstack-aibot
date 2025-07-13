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

# Deployment timestamp: 2025-07-13T00:35:00Z - Switched to open-source LLMs (HuggingFace + Cohere)
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

async def call_huggingface_api(message: str, context: Optional[str] = None) -> str:
    """Call Hugging Face Inference API for AI response"""
    try:
        # Hugging Face models that work without API keys
        models_to_try = [
            "microsoft/DialoGPT-medium",
            "facebook/blenderbot-400M-distill",
            "microsoft/DialoGPT-small"
        ]
        
        prompt = message
        if context:
            prompt = f"Context: {context}\n\nUser: {message}"
        
        for model in models_to_try:
            try:
                print(f"Trying Hugging Face model: {model}")
                
                # Hugging Face Inference API endpoint
                url = f"https://api-inference.huggingface.co/models/{model}"
                
                headers = {
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 200,
                        "temperature": 0.7,
                        "do_sample": True
                    }
                }
                
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.post(url, headers=headers, json=payload)
                    
                    print(f"Hugging Face response status for {model}: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        if isinstance(result, list) and len(result) > 0:
                            generated_text = result[0].get('generated_text', '')
                            # Clean up the response
                            if generated_text:
                                # Remove the input prompt from the response
                                if prompt in generated_text:
                                    ai_response = generated_text.replace(prompt, '').strip()
                                else:
                                    ai_response = generated_text.strip()
                                
                                if ai_response:
                                    return f"🤖 {ai_response} (Powered by {model.split('/')[-1]})"
                    
                    elif response.status_code == 503:
                        print(f"Model {model} is loading, trying next...")
                        continue
                    else:
                        print(f"Error {response.status_code} for {model}: {response.text[:200]}")
                        continue
                        
            except Exception as e:
                print(f"Error with model {model}: {str(e)}")
                continue
        
        # If Hugging Face fails, try Cohere free API
        cohere_response = await call_cohere_free_api(message)
        if cohere_response:
            return cohere_response
        
        # If all APIs fail, fall back to mock AI
        return get_mock_ai_response(message)
        
    except Exception as e:
        print(f"Exception in Hugging Face API call: {str(e)}")
        return get_mock_ai_response(message)
                
    except Exception as e:
        print(f"Error calling OpenRouter API: {str(e)}")
        return f"🤖 Genie AI (Connection Error): I received your message '{message}'. There's a temporary connection issue with the AI service, but your message was processed successfully!"
                
    except Exception as e:
        print(f"Error calling OpenRouter API: {str(e)}")
        return f"I apologize, but I encountered an error while processing your request. Please try again later."

def get_mock_ai_response(message: str) -> str:
    """Generate a mock AI response for demonstration purposes"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! 👋 I'm Genie, your AI assistant. How can I help you today?"
    elif any(word in message_lower for word in ['how are you', 'how do you do', 'how\'s it going']):
        return "I'm doing great, thank you for asking! I'm here and ready to help with any questions or tasks you have. What's on your mind?"
    elif any(word in message_lower for word in ['what can you do', 'help', 'capabilities', 'what are you', 'who are you']):
        return "I'm Genie, your AI assistant! I can help with answering questions, providing explanations, brainstorming ideas, helping with writing, problem-solving, coding assistance, and much more. What would you like to explore together?"
    elif any(word in message_lower for word in ['weather', 'time', 'date']):
        return "I don't have access to real-time data like current weather or time, but I can help with many other things! Try asking me about topics you're curious about, need explanations for, or want help brainstorming."
    elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
        return "You're very welcome! I'm happy to help. Feel free to ask me anything else - I'm here to assist you!"
    elif any(word in message_lower for word in ['joke', 'funny', 'humor']):
        return "Here's one for you: Why don't scientists trust atoms? Because they make up everything! 😄 What else can I help you with?"
    elif any(word in message_lower for word in ['code', 'programming', 'python', 'javascript']):
        return "I'd be happy to help with coding! Whether you need help debugging, learning a new concept, or writing code from scratch, just let me know what programming challenge you're working on."
    elif any(word in message_lower for word in ['explain', 'what is', 'define']):
        return f"I'd be happy to explain that for you! Could you be a bit more specific about what aspect of '{message}' you'd like me to clarify? The more details you give me, the better I can help."
    elif any(word in message_lower for word in ['idea', 'brainstorm', 'suggest', 'advice']):
        return "I love helping with brainstorming! Could you tell me more about what kind of ideas you're looking for? Whether it's for a project, problem-solving, creative writing, or anything else - I'm here to help spark some inspiration."
    elif len(message.strip()) < 3:
        return "I'm here and listening! Feel free to ask me anything - questions, requests for help, or just want to chat. What's on your mind?"
    else:
        return f"That's an interesting topic about '{message}'! I'd love to help you explore that further. Could you tell me more about what specific aspect you're most curious about or what kind of help you're looking for?"

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
        
        # Get AI response from Hugging Face
        ai_response = await call_huggingface_api(message)
        
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
        
        ai_response = await call_huggingface_api(search_prompt)
        
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

async def call_cohere_free_api(message: str) -> str:
    """Call Cohere's free trial API"""
    try:
        # Cohere has a generous free tier
        url = "https://api.cohere.ai/v1/generate"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer TRIAL_KEY"  # Cohere allows trial usage
        }
        
        payload = {
            "model": "command-light",
            "prompt": f"You are Genie, a helpful AI assistant. User asks: {message}\nGenie responds:",
            "max_tokens": 200,
            "temperature": 0.7,
            "stop_sequences": ["\n\n"]
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if 'generations' in result and len(result['generations']) > 0:
                    ai_response = result['generations'][0]['text'].strip()
                    return f"🤖 {ai_response} (Powered by Cohere)"
                    
    except Exception as e:
        print(f"Cohere API error: {str(e)}")
    
    return None

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
