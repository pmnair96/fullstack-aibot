# 🚀 Genie AI Assistant - Deployment Guide

This guide covers multiple deployment options for the Genie AI Assistant fullstack application.

## 📋 Prerequisites

1. **OpenRouter API Key**: Get your free API key from [OpenRouter](https://openrouter.ai/keys)
2. **Git Repository**: Push your code to GitHub/GitLab
3. **Domain** (optional): For custom domain deployment

## 🐳 Docker Deployment (Recommended)

### Quick Start
```bash
# 1. Clone and setup
git clone https://github.com/your-username/fullstack-aibot.git
cd fullstack-aibot

# 2. Configure environment
cp .env.production .env
# Edit .env with your OpenRouter API key and domain

# 3. Deploy with Docker
./deploy.sh
```

### Manual Docker Commands
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access Points:**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## ☁️ Cloud Platform Deployments

### 1. Vercel (Frontend) + Railway (Backend)

#### Frontend on Vercel:
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy frontend
cd frontend
vercel --prod

# 3. Update backend URL in vercel.json
```

#### Backend on Railway:
```bash
# 1. Connect GitHub repo to Railway
# 2. Set environment variables in Railway dashboard
# 3. Deploy from main branch
```

**Required Environment Variables:**
```
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
OPENROUTER_SITE_URL=https://your-frontend-url.vercel.app
FRONTEND_URL=https://your-frontend-url.vercel.app
SECRET_KEY=your-strong-secret-key
```

### 2. DigitalOcean App Platform

```bash
# 1. Push code to GitHub
git push origin main

# 2. Create app from GitHub in DO dashboard
# 3. Use the provided .do/app.yaml configuration
# 4. Set environment variables in DO dashboard
```

### 3. Heroku

#### Backend:
```bash
# 1. Install Heroku CLI
# 2. Create Heroku app
heroku create your-app-backend

# 3. Set environment variables
heroku config:set OPENROUTER_API_KEY=your_key -a your-app-backend
heroku config:set OPENROUTER_SITE_URL=https://your-frontend.herokuapp.com -a your-app-backend

# 4. Deploy
git subtree push --prefix backend heroku main
```

#### Frontend:
```bash
# Create frontend app
heroku create your-app-frontend

# Deploy
git subtree push --prefix frontend heroku main
```

### 4. Render

1. Connect GitHub repository
2. Create Web Service for backend (Python)
3. Create Static Site for frontend
4. Configure environment variables

---

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```bash
NODE_ENV=production
PORT=8000
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
OPENROUTER_SITE_URL=https://your-domain.com
OPENROUTER_APP_NAME=Genie-AI-Assistant
FRONTEND_URL=https://your-domain.com
MAX_FILE_SIZE=10485760
SECRET_KEY=your-strong-secret-key
```

**Frontend (environment.prod.ts):**
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://your-backend-url.com/api'
};
```

### Custom Domain Setup

1. **Configure DNS**: Point your domain to deployment platform
2. **Update Environment Variables**: Replace localhost URLs with your domain
3. **SSL Certificate**: Most platforms auto-configure HTTPS

---

## 📊 Monitoring & Maintenance

### Health Checks
- Backend: `GET /api/health`
- Frontend: Browser accessibility test

### Logs
```bash
# Docker
docker-compose logs -f

# Railway
railway logs

# Heroku
heroku logs --tail -a your-app-name
```

### Updates
```bash
# 1. Update code
git pull origin main

# 2. Rebuild (Docker)
docker-compose down
docker-compose build
docker-compose up -d

# 3. Platform auto-deploy (most cloud platforms)
git push origin main
```

---

## 🔒 Security Considerations

1. **API Keys**: Never commit real API keys to git
2. **Secret Key**: Generate strong secret for JWT tokens
3. **CORS**: Configure proper CORS origins
4. **HTTPS**: Always use HTTPS in production
5. **File Uploads**: Monitor upload sizes and types

---

## 🛠️ Troubleshooting

### Common Issues:

1. **CORS Errors**: Check FRONTEND_URL matches actual domain
2. **API Key Issues**: Verify OpenRouter API key is valid
3. **File Upload Fails**: Check MAX_FILE_SIZE and upload permissions
4. **502 Bad Gateway**: Backend service not running or misconfigured

### Debug Commands:
```bash
# Check backend health
curl https://your-backend-url.com/api/health

# Test API endpoint
curl -X POST "https://your-backend-url.com/api/chat" \
  -F "message=Hello"

# Check Docker logs
docker-compose logs backend
docker-compose logs frontend
```

---

## 💡 Performance Optimization

1. **CDN**: Use CDN for static assets
2. **Caching**: Configure proper cache headers
3. **Compression**: Enable gzip compression (included in nginx config)
4. **Database**: Add PostgreSQL for production data storage
5. **Load Balancing**: Use multiple instances for high traffic

---

## 📚 Additional Resources

- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Angular Deployment Guide](https://angular.io/guide/deployment)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [OpenRouter API Documentation](https://openrouter.ai/docs)

---

## 🆘 Support

For deployment issues:
1. Check the logs first
2. Verify environment variables
3. Test API endpoints manually
4. Review platform-specific documentation

**Need help?** Create an issue in the GitHub repository with:
- Deployment platform
- Error messages
- Environment configuration (without sensitive data)
