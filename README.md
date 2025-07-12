# 🧞 Genie AI Assistant

A modern full-stack ChatGPT-like application built with **Angular frontend** and **Python FastAPI backend** that provides an interactive chat interface with real AI capabilities powered by OpenRouter.

## ✨ Features

- 🎯 Clean, modern ChatGPT-inspired UI
- 💬 Real-time chat interface with AI responses
- 📁 File upload support (Images, PDF, Excel, Word documents)
- 🤖 **Real OpenRouter integration** with multiple LLM options
- � AI-powered search functionality
- �📱 Responsive design for mobile and desktop
- ⚡ Fast loading with Angular standalone components
- 🎨 Beautiful animations and transitions
- 🔒 Secure backend with FastAPI and async processing
- 📊 Health monitoring and API documentation
- 🐳 Docker containerization ready
- 🚀 Multiple deployment options

## 🏗️ Tech Stack

**Frontend:**
- Angular 20+ (Standalone Components)
- TypeScript
- Modern CSS with animations
- Responsive design

**Backend:**
- Python FastAPI
- OpenRouter API integration
- Async file processing
- Pydantic data validation
- Auto-generated API docs

**Deployment:**
- Docker & Docker Compose
- Multiple cloud platform support
- CI/CD with GitHub Actions

## 📁 Project Structure

```
├── frontend/              # Angular application
│   ├── src/app/
│   │   ├── components/    # Chat components
│   │   ├── services/      # HTTP services
│   │   └── environments/  # Environment configs
│   ├── Dockerfile         # Frontend container
│   └── nginx.conf         # Production web server
├── backend/               # Python FastAPI application
│   ├── main.py           # FastAPI app with OpenRouter
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Backend container
│   └── uploads/          # File upload directory
├── docker-compose.yml    # Multi-container deployment
├── deploy.sh            # Quick deployment script
└── DEPLOYMENT.md        # Comprehensive deployment guide
```
- OpenRouter API account (optional for development)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your OpenRouter credentials:
   ```env
   OPENROUTER_API_KEY=your-openrouter-api-key
   OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
   OPENROUTER_SITE_URL=https://your-site.com
   OPENROUTER_APP_NAME=Genie-AI-Assistant
   ```

4. Start the backend server:
   ```bash
   npm start
   ```
   
   The backend will run on `http://localhost:3000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser and navigate to `http://localhost:4200`

### Development Mode

The application works in development mode without OpenRouter credentials. The backend will use mock responses for testing the chat functionality and file uploads.

## API Endpoints

### Backend API (http://localhost:3000)

- `GET /api/health` - Health check endpoint
- `POST /api/chat/message` - Send chat message (supports file uploads)
- `GET /api/chat/history/:sessionId` - Get conversation history
- `DELETE /api/chat/file/:filename` - Delete uploaded file

### File Upload Support

The application supports uploading the following file types:
- **Images**: JPEG, PNG, GIF, WebP
- **Documents**: PDF, Word (.doc, .docx)
- **Spreadsheets**: Excel (.xls, .xlsx, .xlsm)

Maximum file size: 10MB per file
Maximum files per message: 5 files

## Available Scripts

### Frontend Scripts
- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run unit tests
- `npm run watch` - Build in watch mode

### Backend Scripts
- `npm start` - Start production server
- `npm run dev` - Start development server with auto-reload
- `npm test` - Run tests

## Chat Interface Features

- **Message History**: All conversations are stored in the session
- **Typing Indicators**: Shows when the AI is "thinking"
- **File Upload**: Support for images, PDFs, Excel files, and Word documents
- **File Preview**: Image thumbnails and file information display
- **Responsive Design**: Works on all screen sizes
- **Keyboard Shortcuts**: 
  - `Enter` to send message
  - `Shift + Enter` for new line
- **OpenRouter Integration**: Real-time responses from various LLMs
- **Session Management**: Conversation context maintained across messages
- **Error Handling**: Graceful fallback and error messages

## Future Enhancements

- Integration with real AI services (OpenAI, Azure AI, etc.)
- Message persistence
- User authentication
- Chat export functionality
- Dark/light theme toggle
- Voice input support

## Technology Stack

- **Frontend**: Angular 20+ with standalone components
- **Backend**: Node.js with Express.js
- **AI Integration**: OpenRouter API for multiple LLM access
- **File Upload**: Multer middleware
- **Styling**: Pure CSS with modern design patterns
- **State Management**: Angular services with RxJS
- **Build Tools**: Angular CLI with esbuild
- **Security**: Helmet.js, CORS, rate limiting
- **Logging**: Winston with file logging
- **Validation**: Joi schema validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

---

**Created by Pranav** ✨

## 🚀 Quick Deployment

### Option 1: Docker (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/your-username/fullstack-aibot.git
cd fullstack-aibot

# 2. Configure environment
cp .env.production .env
# Edit .env with your OpenRouter API key

# 3. Deploy with Docker
./deploy.sh
```

**Access Points:**
- 🌐 Frontend: http://localhost
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

### Option 2: GitHub Pages + Railway (Free!)

**🌟 Completely Free Deployment:**
```bash
# 1. Deploy backend to Railway
./deploy-backend-railway.sh

# 2. Update frontend API URL with your Railway URL
# Edit frontend/src/environments/environment.prod.ts

# 3. Enable GitHub Pages in repository settings

# 4. Push to trigger deployment
git add .
git commit -m "Configure GitHub Pages deployment"
git push origin main
```

**Live URLs:**
- 🌐 Frontend: https://pmnair96.github.io/fullstack-aibot
- 🔧 Backend: https://your-app.railway.app
- 📚 Docs: https://your-app.railway.app/docs

📖 **See [GITHUB-PAGES.md](GITHUB-PAGES.md) for detailed GitHub Pages setup**

### Option 3: Cloud Platforms

**Quick Deploy Options:**
- 🟦 **Vercel + Railway**: Frontend on Vercel, Backend on Railway
- 🟪 **Heroku**: Both frontend and backend on Heroku
- 🟩 **DigitalOcean**: App Platform deployment
- 🟨 **Render**: Full-stack deployment

📖 **See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed platform-specific instructions**

## 🔧 Configuration

### Required Environment Variables
```bash
OPENROUTER_API_KEY=your_openrouter_api_key  # Get from https://openrouter.ai/keys
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
OPENROUTER_SITE_URL=https://your-domain.com
SECRET_KEY=your-strong-secret-key
```

### Development Setup