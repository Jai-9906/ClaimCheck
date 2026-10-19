/**
 * Global Express Error Handling Middleware
 */
export const errorHandler = (err, req, res, next) => {
  console.error('[Error Caught]:', err.stack || err.message);

  let statusCode = res.statusCode !== 200 && res.statusCode !== 201 ? res.statusCode : 500;
  let message = err.message || 'An unexpected internal server error occurred.';

  // Handle Mongoose validation errors
  if (err.name === 'ValidationError') {
    statusCode = 400;
    message = Object.values(err.errors).map(val => val.message).join(', ');
  }

  // Handle Mongoose cast errors (invalid ObjectId)
  if (err.name === 'CastError') {
    statusCode = 400;
    message = `Resource not found with id of ${err.value}`;
  }

  // Missing API keys specific handling
  if (message.includes('GEMINI_API_KEY is missing') || message.includes('SERPAPI_KEY is missing')) {
    statusCode = 500;
  }

  return res.status(statusCode).json({
    success: false,
    error: err.name || 'ServerError',
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
};
