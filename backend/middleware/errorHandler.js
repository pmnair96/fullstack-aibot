// Global error handler middleware
const errorHandler = (err, req, res, next) => {
  console.error('Error:', err);

  // Multer errors
  if (err.code === 'LIMIT_FILE_SIZE') {
    return res.status(400).json({
      success: false,
      error: 'File too large',
      message: 'The uploaded file exceeds the maximum size limit of 10MB.'
    });
  }

  if (err.code === 'LIMIT_FILE_COUNT') {
    return res.status(400).json({
      success: false,
      error: 'Too many files',
      message: 'Maximum of 5 files can be uploaded at once.'
    });
  }

  if (err.code === 'LIMIT_UNEXPECTED_FILE') {
    return res.status(400).json({
      success: false,
      error: 'Unexpected file field',
      message: 'The file upload field is not recognized.'
    });
  }

  // File type errors
  if (err.message && err.message.includes('File type') && err.message.includes('not supported')) {
    return res.status(400).json({
      success: false,
      error: 'Unsupported file type',
      message: err.message
    });
  }

  // Validation errors
  if (err.isJoi) {
    return res.status(400).json({
      success: false,
      error: 'Validation error',
      message: err.details[0].message,
      details: err.details
    });
  }

  // MongoDB/Database errors (for future use)
  if (err.name === 'MongoError' || err.name === 'ValidationError') {
    return res.status(400).json({
      success: false,
      error: 'Database error',
      message: process.env.NODE_ENV === 'development' ? err.message : 'A database error occurred.'
    });
  }

  // JWT errors (for future authentication)
  if (err.name === 'JsonWebTokenError') {
    return res.status(401).json({
      success: false,
      error: 'Invalid token',
      message: 'The provided authentication token is invalid.'
    });
  }

  if (err.name === 'TokenExpiredError') {
    return res.status(401).json({
      success: false,
      error: 'Token expired',
      message: 'The authentication token has expired.'
    });
  }

  // Azure API errors
  if (err.code && err.code.toString().startsWith('4')) {
    return res.status(400).json({
      success: false,
      error: 'Azure API error',
      message: process.env.NODE_ENV === 'development' ? err.message : 'External service error.'
    });
  }

  // Default error response
  const statusCode = err.statusCode || err.status || 500;
  
  res.status(statusCode).json({
    success: false,
    error: statusCode === 500 ? 'Internal server error' : err.message || 'An error occurred',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong.',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

module.exports = errorHandler;
