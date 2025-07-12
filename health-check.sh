#!/bin/bash

# Deployment Health Check Script
echo "🏥 Checking Genie AI Assistant Deployment Health..."

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost}"

# Check backend health
echo "🔍 Checking backend at $BACKEND_URL..."
if curl -f -s "$BACKEND_URL/api/health" > /dev/null; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
    
    # Get backend info
    BACKEND_INFO=$(curl -s "$BACKEND_URL/api/health")
    echo "📊 Backend Status: $BACKEND_INFO"
else
    echo -e "${RED}❌ Backend is not responding${NC}"
    EXIT_CODE=1
fi

# Check frontend
echo "🔍 Checking frontend at $FRONTEND_URL..."
if curl -f -s "$FRONTEND_URL" > /dev/null; then
    echo -e "${GREEN}✅ Frontend is accessible${NC}"
else
    echo -e "${RED}❌ Frontend is not responding${NC}"
    EXIT_CODE=1
fi

# Check OpenRouter integration
echo "🤖 Testing OpenRouter integration..."
CHAT_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/chat" -F "message=Health check test")
if echo "$CHAT_RESPONSE" | grep -q "response"; then
    echo -e "${GREEN}✅ OpenRouter AI is working${NC}"
else
    echo -e "${YELLOW}⚠️ OpenRouter integration may have issues${NC}"
    echo "Response: $CHAT_RESPONSE"
fi

# Summary
echo ""
echo "🎯 Health Check Summary:"
if [ ${EXIT_CODE:-0} -eq 0 ]; then
    echo -e "${GREEN}✅ All systems operational${NC}"
    echo -e "${GREEN}🌐 Application: $FRONTEND_URL${NC}"
    echo -e "${GREEN}🔧 API: $BACKEND_URL/api${NC}"
    echo -e "${GREEN}📚 Docs: $BACKEND_URL/docs${NC}"
else
    echo -e "${RED}❌ Some services are down${NC}"
    exit 1
fi
