const express = require('express');
const router = express.Router();

// Health check endpoint
router.get('/', (req, res) => {
  const healthData = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'Genie AI Backend',
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    uptime: process.uptime(),
    memory: {
      used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024) + ' MB',
      total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024) + ' MB'
    },
    openrouter: {
      configured: !!process.env.OPENROUTER_API_KEY,
      model: process.env.OPENROUTER_MODEL || 'Not configured'
    }
  };

  res.json(healthData);
});

// Detailed health check
router.get('/detailed', async (req, res) => {
  try {
    const checks = {
      timestamp: new Date().toISOString(),
      service: 'healthy',
      database: 'not_configured', // For future database integration
      openrouter: 'unknown',
      file_system: 'healthy'
    };

    // Check file system
    const fs = require('fs');
    const path = require('path');
    const uploadsDir = path.join(__dirname, '../uploads');
    
    try {
      if (!fs.existsSync(uploadsDir)) {
        fs.mkdirSync(uploadsDir, { recursive: true });
      }
      fs.accessSync(uploadsDir, fs.constants.W_OK);
      checks.file_system = 'healthy';
    } catch (error) {
      checks.file_system = 'error';
    }

    // Check OpenRouter configuration
    if (process.env.OPENROUTER_API_KEY) {
      try {
        // Simple configuration check - not making actual API call for health check
        checks.openrouter = 'configured';
      } catch (error) {
        checks.openrouter = 'error';
      }
    } else {
      checks.openrouter = 'not_configured';
    }

    const overallHealth = Object.values(checks).every(status => 
      status === 'healthy' || status === 'configured' || status === 'not_configured'
    ) ? 'healthy' : 'degraded';

    res.json({
      status: overallHealth,
      checks,
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      version: '1.0.0'
    });

  } catch (error) {
    res.status(500).json({
      status: 'error',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

module.exports = router;
