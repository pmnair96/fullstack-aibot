# Genie AI Assistant

A ChatGPT-like UI built with Angular that provides an interactive chat interface for AI conversations.

## Features

- 🎯 Clean, modern ChatGPT-inspired UI
- 💬 Real-time chat interface with typing indicators
- 📱 Responsive design for mobile and desktop
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

### Installation

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

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run unit tests
- `npm run watch` - Build in watch mode

## Chat Interface Features

- **Message History**: All conversations are stored in the session
- **Typing Indicators**: Shows when the AI is "thinking"
- **Responsive Design**: Works on all screen sizes
- **Keyboard Shortcuts**: 
  - `Enter` to send message
  - `Shift + Enter` for new line
- **Mock AI Responses**: Currently uses simulated responses (ready for backend integration)

## Future Enhancements

- Integration with real AI services (OpenAI, Azure AI, etc.)
- Message persistence
- User authentication
- Chat export functionality
- Dark/light theme toggle
- Voice input support

## Technology Stack

- **Frontend**: Angular 20+ with standalone components
- **Styling**: Pure CSS with modern design patterns
- **State Management**: Angular services with RxJS
- **Build Tool**: Angular CLI with esbuild

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