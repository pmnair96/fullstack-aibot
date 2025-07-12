# Geni- 🎯 Clean, modern ChatGPT-inspired UI
- 💬 Real-time chat interface with typing indicators
- 📁 File upload support (Images, PDF, Excel, Word documents)
- 🤖 OpenRouter integration for intelligent responses with multiple LLM options
- 📱 Responsive design for mobile and desktop
- ⚡ Fast loading with Angular standalone components
- 🎨 Beautiful animations and transitions
- 🔒 Secure backend with rate limiting and validation
- 📊 Health monitoring and loggingsistant

A full-stack ChatGPT-like application built with Angular frontend and Node.js backend that provides an interactive chat interface for AI conversations with OpenRouter integration.

## Features

- 🎯 Clean, modern ChatGPT-inspired UI
- 💬 Real-time chat interface with typing indicators
- � File upload support for images, PDF, Excel, and Word documents
- 🖼️ Image preview functionality
- �📱 Responsive design for mobile and desktop
- ⚡ Fast loading with Angular standalone components
- 🎨 Beautiful animations and transitions

## Project Structure

```
frontend/  
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── chat.component.ts    # Main chat interface
│   │   │   └── chat.component.css   # Chat styling
│   │   ├── services/
│   │   │   └── chat.service.ts      # Mock chat service
│   │   ├── app.config.ts           # App configuration
│   │   ├── app.routes.ts           # Routing configuration
│   │   ├── app.ts                  # Root component
│   │   └── app.html                # Root template
│   ├── main.ts                     # Application bootstrap
│   ├── index.html                  # Main HTML file
│   └── styles.css                  # Global styles
├── package.json                    # Dependencies
└── angular.json                    # Angular configuration
```

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
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