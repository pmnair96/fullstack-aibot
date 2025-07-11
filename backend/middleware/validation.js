const Joi = require('joi');

// Middleware to validate request body against a Joi schema
const validateRequest = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      allowUnknown: true,
      stripUnknown: true
    });

    if (error) {
      const errorDetails = error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message,
        value: detail.context.value
      }));

      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        message: 'The request data is invalid.',
        details: errorDetails
      });
    }

    // Replace req.body with the validated and sanitized value
    req.body = value;
    next();
  };
};

// Middleware to validate request parameters
const validateParams = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.params, {
      abortEarly: false,
      allowUnknown: false,
      stripUnknown: true
    });

    if (error) {
      const errorDetails = error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message,
        value: detail.context.value
      }));

      return res.status(400).json({
        success: false,
        error: 'Parameter validation failed',
        message: 'The request parameters are invalid.',
        details: errorDetails
      });
    }

    req.params = value;
    next();
  };
};

// Middleware to validate query parameters
const validateQuery = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.query, {
      abortEarly: false,
      allowUnknown: true,
      stripUnknown: true
    });

    if (error) {
      const errorDetails = error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message,
        value: detail.context.value
      }));

      return res.status(400).json({
        success: false,
        error: 'Query validation failed',
        message: 'The query parameters are invalid.',
        details: errorDetails
      });
    }

    req.query = value;
    next();
  };
};

module.exports = {
  validateRequest,
  validateParams,
  validateQuery
};
