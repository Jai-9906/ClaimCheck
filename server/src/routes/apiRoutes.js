import { Router } from 'express';
import { getHealthStatus } from '../controllers/healthController.js';
import { verifyClaim } from '../controllers/verifyController.js';
import { getHistory, getReportById } from '../controllers/historyController.js';

const router = Router();

// Health check endpoint
router.get('/health', getHealthStatus);

// Verification endpoint
router.post('/verify', verifyClaim);

// History endpoints
router.get('/history', getHistory);
router.get('/history/:id', getReportById);

export default router;
