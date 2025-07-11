const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const Joi = require('joi');
const azureOpenAIService = require('../services/azureOpenAIService');
const { validateRequest } = require('../middleware/validation');

const router = express.Router();

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadPath = process.env.UPLOAD_PATH || './uploads';
    if (!fs.existsSync(uploadPath)) {
      fs.mkdirSync(uploadPath, { recursive: true });
    }
    cb(null, uploadPath);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const fileFilter = (req, file, cb) => {
  const allowedTypes = [
    'image/jpeg',
    'image/jpg', 
    'image/png',
    'image/gif',
    'image/webp',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel.sheet.macroEnabled.12'
  ];
  
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error(`File type ${file.mimetype} is not supported`), false);
  }
};

const upload = multer({
  storage: storage,
  fileFilter: fileFilter,
  limits: {
    fileSize: parseInt(process.env.MAX_FILE_SIZE) || 10 * 1024 * 1024, // 10MB
    files: 5 // Maximum 5 files
  }
});

// Validation schemas
const chatMessageSchema = Joi.object({
  message: Joi.string().min(1).max(5000).required(),
  sessionId: Joi.string().optional(),
  attachments: Joi.array().items(Joi.object({
    id: Joi.string().required(),
    name: Joi.string().required(),
    size: Joi.number().required(),
    type: Joi.string().required(),
    url: Joi.string().optional(),
    data: Joi.string().optional()
  })).optional()
});

// Chat endpoint
router.post('/message', upload.array('files', 5), validateRequest(chatMessageSchema), async (req, res) => {
  try {
    const { message, sessionId, attachments } = req.body;
    
    // Process uploaded files
    const processedFiles = [];
    if (req.files && req.files.length > 0) {
      for (const file of req.files) {
        processedFiles.push({
          id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
          name: file.originalname,
          size: file.size,
          type: file.mimetype,
          url: `/uploads/${file.filename}`,
          path: file.path
        });
      }
    }
    
    // Combine client-side attachments with uploaded files
    const allAttachments = [
      ...(attachments || []),
      ...processedFiles
    ];

    // Call Azure OpenAI service
    const aiResponse = await azureOpenAIService.getChatCompletion(message, allAttachments, sessionId);
    
    res.json({
      success: true,
      response: aiResponse.content,
      sessionId: aiResponse.sessionId,
      attachments: processedFiles.length > 0 ? processedFiles : undefined,
      usage: aiResponse.usage
    });
    
  } catch (error) {
    console.error('Chat message error:', error);
    
    // Clean up uploaded files on error
    if (req.files) {
      req.files.forEach(file => {
        if (fs.existsSync(file.path)) {
          fs.unlinkSync(file.path);
        }
      });
    }
    
    res.status(500).json({
      success: false,
      error: 'Failed to process chat message',
      message: process.env.NODE_ENV === 'development' ? error.message : 'Internal server error'
    });
  }
});

// Get chat history (if implementing session storage)
router.get('/history/:sessionId', async (req, res) => {
  try {
    const { sessionId } = req.params;
    
    // For now, return empty history as we're not storing sessions
    // This can be extended to use a database later
    res.json({
      success: true,
      sessionId,
      messages: []
    });
    
  } catch (error) {
    console.error('Get history error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve chat history'
    });
  }
});

// Delete uploaded file
router.delete('/file/:filename', (req, res) => {
  try {
    const { filename } = req.params;
    const filePath = path.join(process.env.UPLOAD_PATH || './uploads', filename);
    
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      res.json({
        success: true,
        message: 'File deleted successfully'
      });
    } else {
      res.status(404).json({
        success: false,
        error: 'File not found'
      });
    }
    
  } catch (error) {
    console.error('Delete file error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to delete file'
    });
  }
});

module.exports = router;
