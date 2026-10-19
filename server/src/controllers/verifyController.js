import { FactCheck } from '../models/FactCheck.js';
import { getDBStatus } from '../config/db.js';
import { extractClaimAndQueries, analyzeEvidenceAndDetermineVerdict } from '../services/geminiService.js';
import { fetchEvidenceForQueries } from '../services/serpApiService.js';

/**
 * Controller to handle POST /api/verify
 */
export const verifyClaim = async (req, res, next) => {
  try {
    const { claim } = req.body;

    // 1. Validation
    if (!claim || typeof claim !== 'string') {
      return res.status(400).json({
        success: false,
        error: 'Validation Error',
        message: 'A valid claim text string is required.',
      });
    }

    const trimmedClaim = claim.trim();

    if (trimmedClaim.length < 5) {
      return res.status(400).json({
        success: false,
        error: 'Validation Error',
        message: 'Claim is too short. Please provide a statement of at least 5 characters.',
      });
    }

    if (trimmedClaim.length > 1000) {
      return res.status(400).json({
        success: false,
        error: 'Validation Error',
        message: 'Claim exceeds maximum length of 1000 characters.',
      });
    }

    // Check database connection before running expensive AI calls
    const dbStatus = getDBStatus();
    if (!dbStatus.isConnected) {
      return res.status(503).json({
        success: false,
        error: 'Database Unavailable',
        message: 'Local MongoDB is not connected. Please ensure MongoDB Community Server is running.',
      });
    }

    console.log(`\n==========================================`);
    console.log(`[ClaimCheck] Starting verification for: "${trimmedClaim.slice(0, 80)}..."`);

    // 2. Task 1: Gemini Claim Extraction & Query Formulation
    console.log(`[Stage 1/4] Extracting core claim and generating search queries with Gemini...`);
    const extractionResult = await extractClaimAndQueries(trimmedClaim);
    console.log(`[Stage 1/4] Extracted Claim: "${extractionResult.extractedClaim}"`);
    console.log(`[Stage 1/4] Search Queries:`, extractionResult.searchQueries);

    // 3. SerpApi: Retrieve live web evidence
    console.log(`[Stage 2/4] Retrieving web evidence via SerpApi...`);
    let searchResult;
    try {
      searchResult = await fetchEvidenceForQueries(extractionResult.searchQueries, 8);
      console.log(`[Stage 2/4] Evidence collected: ${searchResult.evidence.length} sources found.`);
    } catch (serpErr) {
      console.warn(`[SerpApi Warning]: ${serpErr.message}`);
      // If SerpApi fails or has no key, gracefully proceed with empty evidence so Gemini can evaluate lack of evidence
      searchResult = {
        evidence: [],
        totalFound: 0,
        queriesUsed: extractionResult.searchQueries,
      };
    }

    // 4. Task 2: Gemini Evidence Analysis & Verdict Generation
    console.log(`[Stage 3/4] Analyzing evidence and formulating verdict with Gemini...`);
    const analysisResult = await analyzeEvidenceAndDetermineVerdict(
      trimmedClaim,
      extractionResult.extractedClaim,
      searchResult.evidence
    );
    console.log(`[Stage 3/4] Verdict: [${analysisResult.verdict}] (Confidence: ${analysisResult.confidence}%)`);

    // Append limitation if search had issues
    const limitations = [...(analysisResult.limitations || [])];
    if (searchResult.evidence.length === 0) {
      limitations.unshift('Web search retrieved no live results or SerpApi was unavailable; assessment is based on lack of verifiable evidence.');
    }

    // 5. Save report to MongoDB
    console.log(`[Stage 4/4] Persisting fact-check report to MongoDB...`);
    const newReport = new FactCheck({
      claimText: trimmedClaim,
      extractedClaim: extractionResult.extractedClaim,
      entities: extractionResult.entities || [],
      verdict: analysisResult.verdict,
      confidence: analysisResult.confidence,
      explanation: analysisResult.explanation,
      supportingEvidence: analysisResult.supportingEvidence || [],
      contradictingEvidence: analysisResult.contradictingEvidence || [],
      sources: analysisResult.sources || [],
      limitations: limitations,
    });

    const savedDoc = await newReport.save();
    console.log(`[Stage 4/4] Report saved successfully with ID: ${savedDoc._id}`);
    console.log(`==========================================\n`);

    // 6. Return response
    return res.status(201).json({
      success: true,
      data: {
        id: savedDoc._id,
        claimText: savedDoc.claimText,
        extractedClaim: savedDoc.extractedClaim,
        entities: savedDoc.entities,
        verdict: savedDoc.verdict,
        confidence: savedDoc.confidence,
        explanation: savedDoc.explanation,
        supportingEvidence: savedDoc.supportingEvidence,
        contradictingEvidence: savedDoc.contradictingEvidence,
        sources: savedDoc.sources,
        limitations: savedDoc.limitations,
        createdAt: savedDoc.createdAt,
      },
    });
  } catch (err) {
    console.error('[Verify Claim Controller Error]:', err);
    return next(err);
  }
};
