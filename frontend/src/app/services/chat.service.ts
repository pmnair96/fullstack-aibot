import { Injectable } from '@angular/core';
import { Observable, of, delay } from 'rxjs';

export interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  isLoading?: boolean;
}

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  response: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private mockResponses = [
    "I'm a mock AI assistant. I understand you asked: '{message}'. How can I help you further?",
    "That's an interesting question about '{message}'. Let me think about that...",
    "Based on your message '{message}', I can provide some insights. What specific aspect would you like to explore?",
    "I see you mentioned '{message}'. Here's what I think about that topic...",
    "Thank you for sharing '{message}' with me. I'd be happy to discuss this further.",
    "Your question about '{message}' is quite thoughtful. Let me provide a detailed response...",
    "I notice you're asking about '{message}'. This is definitely something worth exploring in depth.",
    "Great question regarding '{message}'! I have several thoughts on this matter."
  ];

  constructor() {}

  sendMessage(message: string): Observable<ChatResponse> {
    // Simulate network delay
    const randomDelay = Math.random() * 2000 + 1000; // 1-3 seconds
    
    // Get a random response and replace the placeholder with the actual message
    const randomResponse = this.mockResponses[Math.floor(Math.random() * this.mockResponses.length)];
    const response = randomResponse.replace('{message}', message);
    
    return of({ response }).pipe(delay(randomDelay));
  }
}
