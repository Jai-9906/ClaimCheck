import mongoose from 'mongoose';
import { FactCheck } from '../models/FactCheck.js';
import { getDBStatus } from '../config/db.js';

/**
 * Controller to handle GET /api/history
 * Supports optional ?verdict=... and ?search=... query parameters.
 */
export const getHistory = async (req, res, next) => {
  try {
    const dbStatus = getDBStatus();
    if (!dbStatus.isConnected) {
      return res.status(503).json({
        success: false,
        error: 'Database Unavailable',
        message: 'Cannot retrieve history: MongoDB is not connected.',
      });
    }

    const { verdict, search, limit = 50 } = req.query;
    const filter = {};

    if (verdict && ['True', 'False', 'Misleading', 'Disputed', 'Unverified'].includes(verdict)) {
      filter.verdict = verdict;
    }

    if (search && typeof search === 'string' && search.trim()) {
      const searchRegex = new RegExp(search.trim(), 'i');
      filter.$or = [
        { claimText: searchRegex },
        { extractedClaim: searchRegex },
      ];
    }

    const records = await FactCheck.find(filter)
      .sort({ createdAt: -1 })
      .limit(Math.min(100, Math.max(1, parseInt(limit, 10) || 50)))
      .lean();

    return res.status(200).json({
      success: true,
      count: records.length,
      data: records.map((doc) => ({
        id: doc._id,
        claimText: doc.claimText,
        extractedClaim: doc.extractedClaim,
        entities: doc.entities,
        verdict: doc.verdict,
        confidence: doc.confidence,
        explanation: doc.explanation,
        supportingEvidence: doc.supportingEvidence,
        contradictingEvidence: doc.contradictingEvidence,
        sources: doc.sources,
        limitations: doc.limitations,
        createdAt: doc.createdAt,
      })),
    });
  } catch (err) {
    console.error('[Get History Error]:', err);
    return next(err);
  }
};

/**
 * Controller to handle GET /api/history/:id
 */
export const getReportById = async (req, res, next) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({
        success: false,
        error: 'Bad Request',
        message: `"${id}" is not a valid MongoDB ObjectId.`,
      });
    }

    const dbStatus = getDBStatus();
    if (!dbStatus.isConnected) {
      return res.status(503).json({
        success: false,
        error: 'Database Unavailable',
        message: 'Cannot retrieve report: MongoDB is not connected.',
      });
    }

    const doc = await FactCheck.findById(id).lean();

    if (!doc) {
      return res.status(404).json({
        success: false,
        error: 'Not Found',
        message: `Fact-check report with ID ${id} was not found.`,
      });
    }

    return res.status(200).json({
      success: true,
      data: {
        id: doc._id,
        claimText: doc.claimText,
        extractedClaim: doc.extractedClaim,
        entities: doc.entities,
        verdict: doc.verdict,
        confidence: doc.confidence,
        explanation: doc.explanation,
        supportingEvidence: doc.supportingEvidence,
        contradictingEvidence: doc.contradictingEvidence,
        sources: doc.sources,
        limitations: doc.limitations,
        createdAt: doc.createdAt,
      },
    });
  } catch (err) {
    console.error('[Get Report By ID Error]:', err);
    return next(err);
  }
};
