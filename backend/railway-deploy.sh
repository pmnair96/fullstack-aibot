#!/bin/bash

# Railway Deployment Script for Backend
echo "🚀 Deploying Genie AI Backend to Railway..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create uploads directory
mkdir -p uploads

# Start the server
echo "🌟 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port $PORT
