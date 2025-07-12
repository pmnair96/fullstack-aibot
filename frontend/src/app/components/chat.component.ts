import { Component, ViewChild, ElementRef, AfterViewChecked, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService, ChatMessage, FileAttachment } from '../services/chat.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="chat-container">
      <div class="chat-header">
        <h1>Genie AI Assistant</h1>
        <p>Ask me anything! You can also upload images, Excel, PDF, and Word files.</p>
        <div class="connection-status" [ngClass]="'status-' + connectionStatus">
          <span *ngIf="connectionStatus === 'checking'">🔄 Checking connection...</span>
          <span *ngIf="connectionStatus === 'connected'">✅ Connected to server</span>
          <span *ngIf="connectionStatus === 'disconnected'">❌ Server unavailable</span>
        </div>
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
            <!-- File attachments -->
            <div *ngIf="message.attachments && message.attachments.length > 0" class="message-attachments">
              <div *ngFor="let attachment of message.attachments" class="attachment-item">
                <div class="attachment-icon">
                  <span *ngIf="attachment.type.startsWith('image/')">🖼️</span>
                  <span *ngIf="attachment.type.includes('excel') || attachment.type.includes('spreadsheet')">📊</span>
                  <span *ngIf="attachment.type.includes('pdf')">📄</span>
                  <span *ngIf="attachment.type.includes('word') || attachment.type.includes('document')">📝</span>
                  <span *ngIf="!attachment.type.startsWith('image/') && !attachment.type.includes('excel') && !attachment.type.includes('spreadsheet') && !attachment.type.includes('pdf') && !attachment.type.includes('word') && !attachment.type.includes('document')">📎</span>
                </div>
                <div class="attachment-info">
                  <div class="attachment-name">{{ attachment.name }}</div>
                  <div class="attachment-size">{{ formatFileSize(attachment.size) }}</div>
                </div>
                <img *ngIf="attachment.type.startsWith('image/') && attachment.data" 
                     [src]="attachment.data" 
                     class="attachment-preview" 
                     [alt]="attachment.name">
              </div>
            </div>
            
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
        <!-- File upload preview -->
        <div *ngIf="selectedFiles.length > 0" class="file-preview-container">
          <div class="file-preview-header">
            <span>{{ selectedFiles.length }} file(s) selected</span>
            <button (click)="clearFiles()" class="clear-files-btn">✕</button>
          </div>
          <div class="file-preview-list">
            <div *ngFor="let file of selectedFiles; trackBy: trackByFileId" class="file-preview-item">
              <div class="file-icon">
                <span *ngIf="file.type.startsWith('image/')">🖼️</span>
                <span *ngIf="file.type.includes('excel') || file.type.includes('spreadsheet')">📊</span>
                <span *ngIf="file.type.includes('pdf')">📄</span>
                <span *ngIf="file.type.includes('word') || file.type.includes('document')">📝</span>
                <span *ngIf="!file.type.startsWith('image/') && !file.type.includes('excel') && !file.type.includes('spreadsheet') && !file.type.includes('pdf') && !file.type.includes('word') && !file.type.includes('document')">📎</span>
              </div>
              <div class="file-info">
                <div class="file-name">{{ file.name }}</div>
                <div class="file-size">{{ formatFileSize(file.size) }}</div>
              </div>
              <button (click)="removeFile(file.id)" class="remove-file-btn">✕</button>
            </div>
          </div>
        </div>

        <div class="chat-input">
          <div class="input-actions">
            <input 
              type="file" 
              #fileInput 
              (change)="onFileSelected($event)"
              multiple
              accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.xlsm"
              style="display: none;">
            <button 
              (click)="fileInput.click()" 
              class="file-upload-btn"
              [disabled]="isLoading"
              title="Upload files (Images, PDF, Excel, Word)">
              📎
            </button>
          </div>
          <textarea 
            [(ngModel)]="currentMessage" 
            (keydown)="onKeyDown($event)"
            [disabled]="isLoading"
            placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
            rows="1"
            #messageInput></textarea>
          <button 
            (click)="sendMessage()" 
            [disabled]="(!currentMessage.trim() && selectedFiles.length === 0) || isLoading"
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
export class ChatComponent implements AfterViewChecked, OnInit {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;
  @ViewChild('messageInput') private messageInput!: ElementRef;

  messages: ChatMessage[] = [
    {
      id: '1',
      content: 'Hello! I\'m your Genie AI assistant. How can I help you today? You can also upload files like images, PDFs, Excel sheets, and Word documents.',
      isUser: false,
      timestamp: new Date()
    }
  ];
  
  currentMessage = '';
  isLoading = false;
  selectedFiles: FileAttachment[] = [];
  selectedFileObjects: File[] = []; // Store actual File objects for upload
  
  // Supported file types
  readonly supportedTypes = {
    'image/jpeg': true,
    'image/jpg': true,
    'image/png': true,
    'image/gif': true,
    'image/webp': true,
    'application/pdf': true,
    'application/msword': true,
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': true,
    'application/vnd.ms-excel': true,
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': true,
    'application/vnd.ms-excel.sheet.macroEnabled.12': true
  };

  // Connection status
  connectionStatus: 'checking' | 'connected' | 'disconnected' = 'connected';

  constructor(private chatService: ChatService) {
    // Welcome message is already in the messages array above
  }

  ngOnInit() {
    // Test backend connection on startup
    this.testBackendConnection();
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  private testBackendConnection() {
    console.log('Testing backend connection...');
    this.connectionStatus = 'checking';
    
    this.chatService.checkHealth().subscribe({
      next: (response) => {
        console.log('Backend connection successful:', response);
        this.connectionStatus = 'connected';
      },
      error: (error) => {
        console.error('Backend connection failed:', error);
        this.connectionStatus = 'disconnected';
      }
    });
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  sendMessage() {
    if ((!this.currentMessage.trim() && this.selectedFiles.length === 0) || this.isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: this.currentMessage || (this.selectedFiles.length > 0 ? 'Shared files' : ''),
      isUser: true,
      timestamp: new Date(),
      attachments: this.selectedFiles.length > 0 ? [...this.selectedFiles] : undefined
    };

    this.messages.push(userMessage);
    const messageText = this.currentMessage || 'Please analyze the uploaded files';
    const attachments = this.selectedFiles.length > 0 ? [...this.selectedFiles] : undefined;
    
    // Use the stored File objects for upload
    const filesToUpload: File[] = [...this.selectedFileObjects];
    
    this.currentMessage = '';
    this.selectedFiles = [];
    this.selectedFileObjects = []; // Clear file objects too
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

    // Choose the appropriate service method
    const serviceCall = filesToUpload.length > 0 
      ? this.chatService.sendMessageWithFiles(messageText, filesToUpload, attachments)
      : this.chatService.sendMessage(messageText, attachments);

    serviceCall.subscribe({
      next: (response) => {
        // Remove loading message
        this.messages = this.messages.filter(m => !m.isLoading);
        
        // Update session ID if provided
        if (response.sessionId) {
          this.chatService.setSessionId(response.sessionId);
        }
        
        // Add AI response
        const aiMessage: ChatMessage = {
          id: (Date.now() + 2).toString(),
          content: response.response,
          isUser: false,
          timestamp: new Date(),
          attachments: response.attachments
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

  onFileSelected(event: any) {
    const files: FileList = event.target.files;
    if (!files || files.length === 0) return;

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      
      // Check file type
      if (!this.supportedTypes[file.type as keyof typeof this.supportedTypes]) {
        alert(`File type ${file.type} is not supported. Please upload images, PDF, Excel, or Word files.`);
        continue;
      }

      // Check file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        alert(`File ${file.name} is too large. Please upload files smaller than 10MB.`);
        continue;
      }

      const fileAttachment: FileAttachment = {
        id: Date.now().toString() + i,
        name: file.name,
        size: file.size,
        type: file.type
      };

      // Store the actual File object for upload
      this.selectedFileObjects.push(file);

      // For images, create a preview
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          fileAttachment.data = e.target?.result as string;
        };
        reader.readAsDataURL(file);
      }

      this.selectedFiles.push(fileAttachment);
    }

    // Clear the input
    event.target.value = '';
  }

  removeFile(fileId: string) {
    const index = this.selectedFiles.findIndex(f => f.id === fileId);
    if (index !== -1) {
      this.selectedFiles.splice(index, 1);
      this.selectedFileObjects.splice(index, 1);
    }
  }

  clearFiles() {
    this.selectedFiles = [];
    this.selectedFileObjects = [];
  }

  trackByFileId(index: number, file: FileAttachment): string {
    return file.id;
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
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
