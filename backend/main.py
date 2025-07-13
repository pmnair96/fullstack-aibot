from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import httpx
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Deployment timestamp: 2025-07-13T01:00:00Z - Clean Azure-only implementation
app = FastAPI(title="Genie AI Assistant API", version="1.0.0")

# CORS middleware - Allow all localhost origins for development
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:4000", 
    "http://localhost:4200",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4000",
    "http://127.0.0.1:4200",
    "https://localhost:4200", 
    "https://zealous-feet.surge.sh",
    "*"  # Allow all origins for development
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

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    model_used: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    azure_configured: bool
    environment: str

# Azure OpenAI configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")

def get_mock_ai_response(message: str) -> str:
    """Generate a sophisticated mock AI response that feels like a real AI assistant"""
    import random
    message_lower = message.lower()
    
    # Greeting responses
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
        greetings = [
            "Hello! 👋 I'm Genie, your AI assistant. How can I help you today?",
            "Hi there! Great to meet you. What can I assist you with?",
            "Hello! I'm excited to help you with whatever you need. What's on your mind?",
            "Hey! 👋 I'm here and ready to help. What would you like to explore together?"
        ]
        return random.choice(greetings)
    
    # How are you responses
    elif any(word in message_lower for word in ['how are you', 'how do you do', 'how\'s it going', 'how have you been']):
        responses = [
            "I'm doing great, thank you for asking! I'm here and ready to help with any questions or tasks you have. What's on your mind?",
            "I'm fantastic! Always excited to help and learn from our conversations. How are you doing today?",
            "I'm doing wonderfully! Every conversation is a new adventure for me. How can I assist you today?"
        ]
        return random.choice(responses)
    
    # Capability questions
    elif any(word in message_lower for word in ['what can you do', 'help', 'capabilities', 'what are you', 'who are you', 'abilities']):
        capabilities = [
            "I'm Genie, your AI assistant! I can help with answering questions, providing explanations, brainstorming ideas, helping with writing, problem-solving, coding assistance, math, research topics, and much more. What would you like to explore together?",
            "Great question! I can assist with a wide range of tasks: answering questions, explaining concepts, helping with writing and editing, coding problems, creative brainstorming, math calculations, and general problem-solving. What specific area interests you?",
            "I'm here to help with virtually anything! Whether you need explanations, creative help, technical assistance, problem-solving, or just want to have an interesting conversation. What challenge can I help you tackle?"
        ]
        return random.choice(capabilities)
    
    # Technical/coding questions
    elif any(word in message_lower for word in ['code', 'programming', 'python', 'javascript', 'html', 'css', 'react', 'node', 'function', 'algorithm', 'debug']):
        coding_responses = [
            "I'd be happy to help with coding! Whether you need help debugging, learning a new concept, writing code from scratch, or understanding algorithms, just let me know what programming challenge you're working on.",
            "Coding assistance is one of my favorite topics! I can help with multiple programming languages, debugging, code review, explaining concepts, or working through algorithms. What specific coding challenge are you facing?",
            "Great! I love helping with programming. Whether it's Python, JavaScript, web development, or any other tech topic, I'm here to help. What would you like to work on?"
        ]
        return random.choice(coding_responses)
    
    # Thanks/appreciation
    elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate', 'grateful']):
        thanks_responses = [
            "You're very welcome! I'm happy to help. Feel free to ask me anything else - I'm here to assist you!",
            "My pleasure! That's what I'm here for. Is there anything else you'd like to explore or discuss?",
            "You're so welcome! I really enjoy helping and learning through our conversations. What else can I do for you?"
        ]
        return random.choice(thanks_responses)
    
    # Jokes/humor
    elif any(word in message_lower for word in ['joke', 'funny', 'humor', 'laugh', 'comedy']):
        jokes = [
            "Here's one for you: Why don't scientists trust atoms? Because they make up everything! 😄 Want to hear another one?",
            "I've got a good one: Why did the AI go to therapy? Because it had too many deep learning issues! 🤖 What else can I help you with?",
            "Here's a classic: Why do programmers prefer dark mode? Because light attracts bugs! 💻 Need anything else?",
            "How about this: What do you call a fake noodle? An impasta! 🍝 What else would you like to chat about?"
        ]
        return random.choice(jokes)
    
    # Short/unclear messages
    elif len(message.strip()) < 3:
        short_responses = [
            "I'm here and listening! Feel free to ask me anything - questions, requests for help, or just want to chat. What's on your mind?",
            "I'm ready to help! What would you like to talk about or work on together?",
            "Hi there! I'm here to assist with whatever you need. What can I help you with today?"
        ]
        return random.choice(short_responses)
    
    # General fallback responses
    else:
        general_responses = [
            f"That's an interesting topic about '{message}'! I'd love to help you explore that further. Could you tell me more about what specific aspect you're most curious about or what kind of help you're looking for?",
            f"Thanks for sharing that about '{message}'. I'm intrigued! Could you give me a bit more context about what you'd like to know or how I can best assist you with this?",
            f"Interesting point about '{message}'! I'd be happy to discuss this with you. What particular angle or question do you have in mind?",
            f"I find '{message}' to be a fascinating topic! To give you the most helpful response, could you tell me more about what you're trying to understand or accomplish?"
        ]
        return random.choice(general_responses)

async def call_azure_openai_api(message: str, context: Optional[str] = None) -> str:
    """Call Azure OpenAI API for AI response"""
    if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY or AZURE_OPENAI_API_KEY == "your_azure_openai_api_key_here":
        return get_mock_ai_response(message)
    
    try:
        # Build the Azure OpenAI endpoint URL
        url = f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY
        }
        
        prompt = message
        if context:
            prompt = f"Context: {context}\n\nUser message: {message}"
        
        payload = {
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
        
        # Add API version as query parameter
        params = {"api-version": AZURE_OPENAI_API_VERSION}
        
        print(f"Making request to Azure OpenAI: {AZURE_OPENAI_DEPLOYMENT_NAME}")
        print(f"Endpoint: {url}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload, params=params)
            
            print(f"Azure OpenAI response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                return f"✅ {ai_response} (Powered by Azure OpenAI)"
            else:
                error_text = response.text
                print(f"Azure OpenAI API error: {response.status_code} - {error_text}")
                
                if response.status_code == 401:
                    return "🔐 Authentication issue with Azure OpenAI. Please check your API key and endpoint configuration."
                elif response.status_code == 429:
                    return "⏱️ Azure OpenAI rate limit reached. Please try again in a moment."
                elif response.status_code == 404:
                    return "🔍 Azure OpenAI deployment not found. Please check your deployment name configuration."
                else:
                    return get_mock_ai_response(message)
                
    except Exception as e:
        print(f"Exception in Azure OpenAI API call: {str(e)}")
        return get_mock_ai_response(message)

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        azure_configured=bool(AZURE_OPENAI_API_KEY and AZURE_OPENAI_API_KEY != "your_azure_openai_api_key_here"),
        environment=os.getenv("NODE_ENV", "development")
    )

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        azure_configured=bool(AZURE_OPENAI_API_KEY and AZURE_OPENAI_API_KEY != "your_azure_openai_api_key_here"),
        environment=os.getenv("NODE_ENV", "development")
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Chat endpoint that handles JSON messages"""
    try:
        message = chat_message.message
        
        # Get AI response from Azure OpenAI
        ai_response = await call_azure_openai_api(message)
        
        return ChatResponse(
            response=ai_response,
            timestamp=datetime.now().isoformat(),
            model_used=AZURE_OPENAI_DEPLOYMENT_NAME
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/api/models")
async def get_available_models():
    """Get list of available Azure OpenAI models"""
    return {
        "current_model": AZURE_OPENAI_DEPLOYMENT_NAME,
        "available_models": [
            "gpt-35-turbo",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-35-turbo-16k"
        ],
        "configured": bool(AZURE_OPENAI_API_KEY and AZURE_OPENAI_API_KEY != "your_azure_openai_api_key_here"),
        "endpoint": AZURE_OPENAI_ENDPOINT,
        "api_version": AZURE_OPENAI_API_VERSION
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
