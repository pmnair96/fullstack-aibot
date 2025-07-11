const https = require('https');

class AzureOpenAIService {
  constructor() {
    this.endpoint = process.env.AZURE_OPENAI_ENDPOINT;
    this.apiKey = process.env.AZURE_OPENAI_API_KEY;
    this.deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || 'gpt-35-turbo';
    this.apiVersion = process.env.AZURE_OPENAI_API_VERSION || '2024-02-15-preview';
    
    if (!this.endpoint || !this.apiKey) {
      console.warn('⚠️ Azure OpenAI credentials not configured. Using mock responses.');
      this.useMockResponse = true;
    } else {
      console.log('✅ Azure OpenAI configured');
      this.useMockResponse = false;
    }
    
    // Store conversation history (in production, use a proper database)
    this.conversationHistory = new Map();
  }

  async makeAzureOpenAIRequest(messages) {
    return new Promise((resolve, reject) => {
      const url = `${this.endpoint}/openai/deployments/${this.deploymentName}/chat/completions?api-version=${this.apiVersion}`;
      const urlObj = new URL(url);
      
      const requestBody = JSON.stringify({
        messages: messages,
        max_tokens: 1000,
        temperature: 0.7,
        top_p: 0.9,
        frequency_penalty: 0.1,
        presence_penalty: 0.1
      });

      const options = {
        hostname: urlObj.hostname,
        path: urlObj.pathname + urlObj.search,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'api-key': this.apiKey,
          'Content-Length': Buffer.byteLength(requestBody)
        }
      };

      const req = https.request(options, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
          data += chunk;
        });
        
        res.on('end', () => {
          try {
            const response = JSON.parse(data);
            if (res.statusCode === 200) {
              resolve(response);
            } else {
              reject(new Error(`Azure OpenAI API error: ${response.error?.message || 'Unknown error'}`));
            }
          } catch (error) {
            reject(new Error(`Failed to parse Azure OpenAI response: ${error.message}`));
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`Request error: ${error.message}`));
      });

      req.write(requestBody);
      req.end();
    });
  }

  async getChatCompletion(message, attachments = [], sessionId = null) {
    try {
      if (this.useMockResponse) {
        return this.getMockResponse(message, attachments, sessionId);
      }

      // Get or create conversation history
      const currentSessionId = sessionId || this.generateSessionId();
      let history = this.conversationHistory.get(currentSessionId) || [];

      // Prepare the system message
      const systemMessage = {
        role: 'system',
        content: `You are Genie, a helpful AI assistant. You can help users with various tasks including analyzing documents, images, and answering questions. 
        
        When users upload files, acknowledge them and provide relevant analysis based on the file type:
        - For images: Describe what you see and offer to help with image-related tasks
        - For PDFs: Offer to help analyze or summarize the document content
        - For Excel files: Offer to help with data analysis or explain spreadsheet contents
        - For Word documents: Offer to help review, summarize, or analyze the document
        
        Be conversational, helpful, and engaging. Always maintain context from the conversation history.`
      };

      // Prepare the user message
      let userContent = message;
      if (attachments && attachments.length > 0) {
        const fileList = attachments.map(att => `${att.name} (${att.type})`).join(', ');
        userContent += `\n\n[User has uploaded ${attachments.length} file(s): ${fileList}]`;
      }

      const userMessage = {
        role: 'user',
        content: userContent
      };

      // Build messages array with history
      const messages = [systemMessage];
      
      // Add conversation history (limit to last 10 exchanges to manage token usage)
      if (history.length > 0) {
        messages.push(...history.slice(-20)); // Last 20 messages (10 exchanges)
      }
      
      messages.push(userMessage);

      // Call Azure OpenAI
      const response = await this.makeAzureOpenAIRequest(messages);
      
      const aiResponse = response.choices[0]?.message?.content || 'I apologize, but I could not generate a response. Please try again.';

      // Update conversation history
      history.push(userMessage);
      history.push({ role: 'assistant', content: aiResponse });
      this.conversationHistory.set(currentSessionId, history);

      return {
        content: aiResponse,
        sessionId: currentSessionId,
        usage: {
          promptTokens: response.usage?.prompt_tokens || 0,
          completionTokens: response.usage?.completion_tokens || 0,
          totalTokens: response.usage?.total_tokens || 0
        }
      };

    } catch (error) {
      console.error('Azure OpenAI API error:', error);
      
      // Fallback to mock response on API errors
      return this.getMockResponse(message, attachments, sessionId, true);
    }
  }

  getMockResponse(message, attachments = [], sessionId = null, isError = false) {
    const currentSessionId = sessionId || this.generateSessionId();
    
    let response = '';
    
    if (isError) {
      response = "I'm experiencing some technical difficulties connecting to Azure AI services, but I'm still here to help! ";
    }
    
    if (attachments && attachments.length > 0) {
      const fileTypes = attachments.map(att => {
        if (att.type.startsWith('image/')) return 'image';
        if (att.type.includes('pdf')) return 'PDF document';
        if (att.type.includes('excel') || att.type.includes('spreadsheet')) return 'Excel file';
        if (att.type.includes('word') || att.type.includes('document')) return 'Word document';
        return 'file';
      });
      
      response += `I can see you've shared ${attachments.length} file(s) with me: ${fileTypes.join(', ')}. `;
      
      if (fileTypes.includes('image')) {
        response += "I'd be happy to help analyze any images you've uploaded. ";
      }
      if (fileTypes.includes('PDF document')) {
        response += "I can help you understand and analyze the PDF content. ";
      }
      if (fileTypes.includes('Excel file')) {
        response += "I can assist with data analysis and spreadsheet questions. ";
      }
      if (fileTypes.includes('Word document')) {
        response += "I can help review and analyze your document. ";
      }
    }
    
    // Generate contextual response based on message content
    const mockResponses = [
      `Regarding your message "${message}", I understand you're looking for assistance. ${response}How can I help you further?`,
      `That's an interesting question about "${message}". ${response}Let me provide some insights on this topic.`,
      `I see you mentioned "${message}". ${response}This is definitely something I can help you explore in more detail.`,
      `Thank you for sharing "${message}" with me. ${response}I'd be happy to discuss this further and provide guidance.`,
      `Your question about "${message}" is quite thoughtful. ${response}Let me help you with a comprehensive response.`
    ];
    
    const selectedResponse = mockResponses[Math.floor(Math.random() * mockResponses.length)];
    
    return {
      content: selectedResponse,
      sessionId: currentSessionId,
      usage: {
        promptTokens: 0,
        completionTokens: 0,
        totalTokens: 0
      }
    };
  }

  generateSessionId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
  }

  // Clear conversation history for a session
  clearHistory(sessionId) {
    this.conversationHistory.delete(sessionId);
  }

  // Get conversation history for a session
  getHistory(sessionId) {
    return this.conversationHistory.get(sessionId) || [];
  }
}

module.exports = new AzureOpenAIService();
