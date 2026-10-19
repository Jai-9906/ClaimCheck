import { getDBStatus } from '../config/db.js';

export const getRootStatus = (req, res) => {
  return res.status(200).json({
    status: 'online',
    message: 'ClaimCheck: Real-Time Fact-Checking API is operational',
    version: '1.0.0',
    endpoints: {
      health: 'GET /api/health',
      verify: 'POST /api/verify',
      history: 'GET /api/history',
      report: 'GET /api/history/:id',
    },
  });
};

export const getHealthStatus = (req, res) => {
  const dbStatus = getDBStatus();
  const isHealthy = dbStatus.isConnected;

  return res.status(isHealthy ? 200 : 503).json({
    status: isHealthy ? 'ok' : 'degraded',
    timestamp: new Date().toISOString(),
    database: {
      state: dbStatus.state,
      name: dbStatus.database,
      connected: dbStatus.isConnected,
    },
  });
};
