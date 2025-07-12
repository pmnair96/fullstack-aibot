#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Genie AI Assistant Backend Setup${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}🔧 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo -e "${GREEN}✅ Dependencies installed successfully!${NC}"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}📝 Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please update the .env file with your OpenRouter API key and other configurations.${NC}"
fi

# Create uploads directory
mkdir -p uploads

echo -e "${GREEN}🎉 Setup complete!${NC}"
echo -e "${YELLOW}📋 Next steps:${NC}"
echo -e "1. Update your .env file with your OpenRouter API key"
echo -e "2. Run: ${GREEN}source venv/bin/activate${NC}"
echo -e "3. Run: ${GREEN}python main.py${NC} or ${GREEN}uvicorn main:app --reload --port 8000${NC}"
echo -e ""
echo -e "${GREEN}🌐 Your API will be available at: http://localhost:8000${NC}"
echo -e "${GREEN}📚 API Documentation: http://localhost:8000/docs${NC}"
