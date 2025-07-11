import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

export interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  isLoading?: boolean;
  attachments?: FileAttachment[];
}

export interface FileAttachment {
  id: string;
  name: string;
  size: number;
  type: string;
  url?: string;
  data?: string; // base64 encoded data for preview
}

export interface ChatRequest {
  message: string;
  attachments?: FileAttachment[];
  sessionId?: string;
}

export interface ChatResponse {
  success: boolean;
  response: string;
  sessionId?: string;
  attachments?: FileAttachment[];
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private readonly API_URL = 'http://localhost:3000/api';
  private sessionId: string | null = null;

  constructor(private http: HttpClient) {}

  sendMessage(message: string, attachments?: FileAttachment[]): Observable<ChatResponse> {
    const formData = new FormData();
    formData.append('message', message);
    
    if (this.sessionId) {
      formData.append('sessionId', this.sessionId);
    }

    // Add file attachments if any
    if (attachments && attachments.length > 0) {
      formData.append('attachments', JSON.stringify(attachments));
    }

    return this.http.post<ChatResponse>(`${this.API_URL}/chat/message`, formData)
      .pipe(
        catchError(error => {
          console.error('Chat service error:', error);
          return throwError(() => new Error('Failed to send message. Please try again.'));
        })
      );
  }

  // Method to send message with file uploads
  sendMessageWithFiles(message: string, files: File[], attachments?: FileAttachment[]): Observable<ChatResponse> {
    const formData = new FormData();
    formData.append('message', message || 'Please analyze the uploaded files');
    
    if (this.sessionId) {
      formData.append('sessionId', this.sessionId);
    }

    // Add client-side attachments (for display purposes)
    if (attachments && attachments.length > 0) {
      formData.append('attachments', JSON.stringify(attachments));
    }

    // Add actual files for upload
    files.forEach((file, index) => {
      formData.append('files', file);
    });

    return this.http.post<ChatResponse>(`${this.API_URL}/chat/message`, formData)
      .pipe(
        catchError(error => {
          console.error('Chat service error:', error);
          return throwError(() => new Error('Failed to send message with files. Please try again.'));
        })
      );
  }

  setSessionId(sessionId: string) {
    this.sessionId = sessionId;
  }

  getSessionId(): string | null {
    return this.sessionId;
  }

  // Health check method
  checkHealth(): Observable<any> {
    return this.http.get(`${this.API_URL}/health`);
  }
}
