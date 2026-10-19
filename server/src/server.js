import app from './app.js';
import { config } from './config/env.js';
import { connectDB } from './config/db.js';

const startServer = async () => {
  console.log('==============================================');
  console.log('   ClaimCheck Fact-Checking Server Starting   ');
  console.log('==============================================');
  console.log(`Node Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`Configured Port: ${config.port}`);
  console.log(`Allowed Client Origin: ${config.clientOrigin}`);
  console.log(`Configured Gemini Model: ${config.geminiModel}`);

  // Connect to local MongoDB Community Server
  await connectDB();

  const server = app.listen(config.port, () => {
    console.log(`[ClaimCheck Server] Running at: http://localhost:${config.port}`);
    console.log(`[ClaimCheck Server] Health Check: http://localhost:${config.port}/api/health`);
    console.log('==============================================\n');
  });

  // Handle graceful shutdowns
  const handleExit = (signal) => {
    console.log(`\nReceived ${signal}. Shutting down ClaimCheck gracefully...`);
    server.close(() => {
      console.log('HTTP server closed.');
      process.exit(0);
    });
  };

  process.on('SIGINT', () => handleExit('SIGINT'));
  process.on('SIGTERM', () => handleExit('SIGTERM'));
};

startServer().catch((err) => {
  console.error('Fatal server boot error:', err);
  process.exit(1);
});
