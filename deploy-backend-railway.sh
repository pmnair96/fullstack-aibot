#!/bin/bash

echo "🚀 Deploying Backend to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway (if not already logged in)
echo "🔐 Please login to Railway..."
railway login

# Navigate to backend directory
cd backend

# Initialize Railway project (if not already done)
echo "🏗️ Setting up Railway project..."
railway project create

# Set environment variables
echo "🔧 Setting environment variables..."
echo "Please set these environment variables in Railway dashboard:"
echo "OPENROUTER_API_KEY=your_openrouter_api_key"
echo "OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free"
echo "OPENROUTER_SITE_URL=https://your-domain.com"
echo "SECRET_KEY=your-strong-secret-key"

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Backend deployed to Railway!"
echo "📝 Don't forget to:"
echo "1. Update your environment variables in Railway dashboard"
echo "2. Update the frontend environment.prod.ts with your Railway URL"
echo "3. Push changes to trigger GitHub Pages deployment"
