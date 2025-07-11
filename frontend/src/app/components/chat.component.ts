import { Component, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService, ChatMessage } from '../services/chat.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="chat-container">
      <div class="chat-header">
        <h1>Genie AI Assistant</h1>
        <p>Ask me anything!</p>
      </div>
      
      <div class="chat-messages" #messagesContainer>
        <div *ngFor="let message of messages" 
             class="message" 
             [ngClass]="{'user-message': message.isUser, 'ai-message': !message.isUser}">
          <div class="message-avatar">
            <span *ngIf="message.isUser">👤</span>
            <span *ngIf="!message.isUser">🤖</span>
          </div>
          <div class="message-content">
            <div class="message-text" [innerHTML]="formatMessage(message.content)"></div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
          <div *ngIf="message.isLoading" class="loading-indicator">
            <div class="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="chat-input-container">
        <div class="chat-input">
          <textarea 
            [(ngModel)]="currentMessage" 
            (keydown)="onKeyDown($event)"
            [disabled]="isLoading"
            placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
            rows="1"
            #messageInput></textarea>
          <button 
            (click)="sendMessage()" 
            [disabled]="!currentMessage.trim() || isLoading"
            class="send-button">
            <span *ngIf="!isLoading">Send</span>
            <span *ngIf="isLoading" class="spinner"></span>
          </button>
        </div>
      </div>
      
      <div class="chat-footer">
        <p>Created by Pranav ✨</p>
      </div>
    </div>
  `,
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements AfterViewChecked {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;
  @ViewChild('messageInput') private messageInput!: ElementRef;

  messages: ChatMessage[] = [
    {
      id: '1',
      content: 'Hello! I\'m your Genie AI assistant. How can I help you today?',
      isUser: false,
      timestamp: new Date()
    }
  ];
  
  currentMessage = '';
  isLoading = false;

  constructor(private chatService: ChatService) {}

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  sendMessage() {
    if (!this.currentMessage.trim() || this.isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: this.currentMessage,
      isUser: true,
      timestamp: new Date()
    };

    this.messages.push(userMessage);
    const messageText = this.currentMessage;
    this.currentMessage = '';
    this.isLoading = true;

    // Add loading message
    const loadingMessage: ChatMessage = {
      id: (Date.now() + 1).toString(),
      content: '',
      isUser: false,
      timestamp: new Date(),
      isLoading: true
    };
    this.messages.push(loadingMessage);

    this.chatService.sendMessage(messageText).subscribe({
      next: (response) => {
        // Remove loading message
        this.messages = this.messages.filter(m => !m.isLoading);
        
        // Add AI response
        const aiMessage: ChatMessage = {
          id: (Date.now() + 2).toString(),
          content: response.response,
          isUser: false,
          timestamp: new Date()
        };
        this.messages.push(aiMessage);
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error sending message:', error);
        // Remove loading message
        this.messages = this.messages.filter(m => !m.isLoading);
        
        // Add error message
        const errorMessage: ChatMessage = {
          id: (Date.now() + 3).toString(),
          content: 'Sorry, I\'m having trouble connecting to the server. Please try again later.',
          isUser: false,
          timestamp: new Date()
        };
        this.messages.push(errorMessage);
        this.isLoading = false;
      }
    });
  }

  formatMessage(content: string): string {
    // Basic formatting - you can enhance this with markdown support
    return content.replace(/\n/g, '<br>');
  }

  formatTime(timestamp: Date): string {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  private scrollToBottom(): void {
    try {
      this.messagesContainer.nativeElement.scrollTop = 
        this.messagesContainer.nativeElement.scrollHeight;
    } catch (err) {}
  }
}
