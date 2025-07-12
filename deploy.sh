#!/bin/bash

# Genie AI Assistant - Docker Deployment Script
echo "🚀 Deploying Genie AI Assistant with Docker..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️ No .env file found. Creating from template...${NC}"
    cp .env.production .env
    echo -e "${YELLOW}📝 Please edit .env file with your configuration before proceeding.${NC}"
    echo -e "${YELLOW}   Especially set your OPENROUTER_API_KEY and update domain URLs.${NC}"
    read -p "Press Enter to continue after editing .env file..."
fi

# Build and start the containers
echo -e "${GREEN}🔨 Building Docker images...${NC}"
docker-compose build

echo -e "${GREEN}🌟 Starting containers...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo -e "${GREEN}🌐 Frontend: http://localhost${NC}"
    echo -e "${GREEN}🔧 Backend API: http://localhost:8000${NC}"
    echo -e "${GREEN}📚 API Docs: http://localhost:8000/docs${NC}"
    echo -e ""
    echo -e "${YELLOW}📋 To view logs: docker-compose logs -f${NC}"
    echo -e "${YELLOW}🛑 To stop: docker-compose down${NC}"
else
    echo -e "${RED}❌ Deployment failed. Check logs with: docker-compose logs${NC}"
    exit 1
fi
