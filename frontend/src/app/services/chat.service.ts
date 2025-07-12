import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

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
  private readonly API_URL = environment.apiUrl;
  private sessionId: string | null = null;

  constructor(private http: HttpClient) {}

  sendMessage(message: string, attachments?: FileAttachment[]): Observable<ChatResponse> {
    // Always use FormData to match backend expectations
    const formData = new FormData();
    formData.append('message', message);
    
    if (this.sessionId) {
      formData.append('sessionId', this.sessionId);
    }

    // Add file attachments if any
    if (attachments && attachments.length > 0) {
      formData.append('attachments', JSON.stringify(attachments));
    }

    console.log('Sending message to:', `${this.API_URL}/chat`);
    console.log('Message:', message);

    return this.http.post<any>(`${this.API_URL}/chat`, formData)
      .pipe(
        map(response => {
          // Transform Python backend response to match frontend interface
          return {
            success: true,
            response: response.response || response.message || 'No response',
            sessionId: this.sessionId,
            usage: {
              promptTokens: 0,
              completionTokens: 0,
              totalTokens: 0
            }
          } as ChatResponse;
        }),
        catchError(error => {
          console.error('Chat service error:', error);
          console.error('Error status:', error.status);
          console.error('Error details:', error.error);
          
          let errorMessage = 'Failed to send message. Please try again.';
          if (error.status === 0) {
            errorMessage = 'Unable to connect to the server. Please check if the backend is running.';
          } else if (error.status >= 500) {
            errorMessage = 'Server error. Please try again later.';
          } else if (error.status === 404) {
            errorMessage = 'API endpoint not found. Please check the server configuration.';
          }
          
          return throwError(() => new Error(errorMessage));
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

    console.log('Sending message with files to:', `${this.API_URL}/chat`);
    console.log('Files:', files.map(f => f.name));

    return this.http.post<any>(`${this.API_URL}/chat`, formData)
      .pipe(
        map(response => {
          // Transform Python backend response to match frontend interface
          return {
            success: true,
            response: response.response || response.message || 'No response',
            sessionId: this.sessionId,
            usage: {
              promptTokens: 0,
              completionTokens: 0,
              totalTokens: 0
            }
          } as ChatResponse;
        }),
        catchError(error => {
          console.error('Chat service error:', error);
          console.error('Error status:', error.status);
          console.error('Error details:', error.error);
          
          let errorMessage = 'Failed to send message with files. Please try again.';
          if (error.status === 0) {
            errorMessage = 'Unable to connect to the server. Please check if the backend is running.';
          } else if (error.status >= 500) {
            errorMessage = 'Server error. Please try again later.';
          }
          
          return throwError(() => new Error(errorMessage));
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
    console.log('Checking health at:', `${this.API_URL}/health`);
    return this.http.get(`${this.API_URL}/health`).pipe(
      catchError(error => {
        console.error('Health check failed:', error);
        return throwError(() => error);
      })
    );
  }

  // Test connection method
  testConnection(): Observable<boolean> {
    return this.checkHealth().pipe(
      map(() => true),
      catchError(() => {
        return throwError(() => new Error('Backend connection failed'));
      })
    );
  }
}
