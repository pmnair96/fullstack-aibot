# Genie AI Backend

Node.js backend server for the Genie AI Assistant with Azure OpenAI integration.

## Features

- 🚀 Express.js REST API
- 🤖 Azure OpenAI integration
- 📁 File upload support (images, PDF, Excel, Word)
- 🔒 Security middleware (helmet, CORS, rate limiting)
- 📝 Request logging and error handling
- ✅ Input validation with Joi
- 🏥 Health check endpoints
- 🔄 Session management for conversations

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Azure OpenAI service account (optional for development)

## Setup

1. **Install dependencies:**
   ```bash
   cd backend
   npm install
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your configuration:
   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   
   # Other settings
   PORT=3000
   FRONTEND_URL=http://localhost:4200
   ```

3. **Start the server:**
   ```bash
   # Development mode with auto-reload
   npm run dev
   
   # Production mode
   npm start
   ```

## API Endpoints

### Health Check
- `GET /api/health` - Basic health status
- `GET /api/health/detailed` - Detailed system health

### Chat
- `POST /api/chat/message` - Send message to AI (supports file uploads)
- `GET /api/chat/history/:sessionId` - Get conversation history
- `DELETE /api/chat/file/:filename` - Delete uploaded file

### File Uploads
The API supports multipart form data with the following file types:
- Images: JPEG, PNG, GIF, WebP
- Documents: PDF, Word (.doc, .docx)
- Spreadsheets: Excel (.xls, .xlsx, .xlsm)

## Request/Response Examples

### Send Chat Message
```bash
curl -X POST http://localhost:3000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, can you help me analyze this data?",
    "sessionId": "optional-session-id"
  }'
```

### Send Message with File Upload
```bash
curl -X POST http://localhost:3000/api/chat/message \
  -F "message=Please analyze this document" \
  -F "files=@document.pdf" \
  -F "sessionId=optional-session-id"
```

### Response Format
```json
{
  "success": true,
  "response": "AI response text here...",
  "sessionId": "session-123",
  "attachments": [
    {
      "id": "file-123",
      "name": "document.pdf",
      "size": 1024,
      "type": "application/pdf",
      "url": "/uploads/file-123.pdf"
    }
  ],
  "usage": {
    "promptTokens": 100,
    "completionTokens": 150,
    "totalTokens": 250
  }
}
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NODE_ENV` | Environment mode | `development` |
| `PORT` | Server port | `3000` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Required |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Required |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Deployment model name | `gpt-35-turbo` |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:4200` |
| `MAX_FILE_SIZE` | Max upload size in bytes | `10485760` (10MB) |
| `RATE_LIMIT_WINDOW_MS` | Rate limit window | `900000` (15 min) |
| `RATE_LIMIT_MAX_REQUESTS` | Max requests per window | `100` |

### Azure OpenAI Setup

1. Create an Azure OpenAI resource in the Azure portal
2. Deploy a model (e.g., GPT-3.5 Turbo or GPT-4)
3. Get your endpoint URL and API key
4. Update the environment variables

## Development

### Mock Mode
If Azure OpenAI credentials are not configured, the server will automatically use mock responses for development.

### Logging
Logs are written to the `logs/` directory:
- `error.log` - Error logs only
- `combined.log` - All logs

### File Storage
Uploaded files are stored in the `uploads/` directory. In production, consider using cloud storage like Azure Blob Storage.

## Security Features

- **Helmet.js** - Security headers
- **CORS** - Cross-origin resource sharing
- **Rate limiting** - Prevent abuse
- **File validation** - Type and size restrictions
- **Input validation** - Joi schema validation
- **Error handling** - Comprehensive error responses

## Testing

```bash
# Run tests (when implemented)
npm test

# Health check
curl http://localhost:3000/api/health
```

## Production Deployment

1. Set `NODE_ENV=production`
2. Configure proper logging (consider external log services)
3. Use a process manager like PM2
4. Set up reverse proxy (nginx/Apache)
5. Configure SSL/TLS certificates
6. Use environment-specific configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
