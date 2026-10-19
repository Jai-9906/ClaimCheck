import express from 'express';
import cors from 'cors';
import { config } from './config/env.js';
import apiRoutes from './routes/apiRoutes.js';
import { getRootStatus } from './controllers/healthController.js';
import { errorHandler } from './middleware/errorHandler.js';

const app = express();

// Enable CORS for frontend origin (allowing localhost:5173 and configurable origins)
app.use(cors({
  origin: (origin, callback) => {
    // Allow requests with no origin (like mobile apps, curl, postman) or matching origin
    if (!origin || origin === config.clientOrigin || origin.startsWith('http://localhost:')) {
      return callback(null, true);
    }
    return callback(null, true); // Permissive in dev mode
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));

// Body parsing
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true, limit: '1mb' }));

// Root status check
app.get('/', getRootStatus);

// API routes
app.use('/api', apiRoutes);

// 404 catch-all
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'NotFound',
    message: `Cannot ${req.method} ${req.originalUrl}`,
  });
});

// Centralized error handler
app.use(errorHandler);

export default app;
