import React from 'react';
import { VerdictBadge } from './VerdictBadge.jsx';

export const ResultCard = ({ report, onReset, onViewHistory }) => {
  if (!report) return null;

  const {
    claimText,
    extractedClaim,
    verdict,
    confidence = 0,
    explanation,
    supportingEvidence = [],
    contradictingEvidence = [],
    sources = [],
    limitations = [],
    createdAt,
  } = report;

  const getConfidenceLevel = (score) => {
    if (score >= 80) return 'High Confidence';
    if (score >= 50) return 'Moderate Confidence';
    return 'Low Confidence / Inconclusive';
  };

  const formattedDate = createdAt
    ? new Date(createdAt).toLocaleString(undefined, {
        dateStyle: 'medium',
        timeStyle: 'short',
      })
    : 'Just now';

  return (
    <div className="result-container">
      {/* Header card with Claim, Verdict, Confidence */}
      <div className="card result-header-card">
        <div className="claim-quote-box">
          <div className="claim-tag">Submitted Claim</div>
          <div className="claim-text-display">"{claimText}"</div>

          {extractedClaim && extractedClaim !== claimText && (
            <div className="extracted-box">
              <strong>Core Assertion Analyzed:</strong> {extractedClaim}
            </div>
          )}

          <div style={{ marginTop: '10px', fontSize: '0.8rem', color: 'var(--text-subtle)' }}>
            Verified on {formattedDate}
          </div>
        </div>

        <div className="verdict-score-column">
          <VerdictBadge verdict={verdict} />

          <div className="confidence-meter">
            <div className="confidence-header">Assessment Confidence</div>
            <div className="confidence-value">{confidence}%</div>
            <div className="confidence-bar-bg">
              <div
                className="confidence-bar-fill"
                style={{ width: `${Math.min(100, Math.max(0, confidence))}%` }}
              ></div>
            </div>
            <div className="confidence-subtext">{getConfidenceLevel(confidence)}</div>
          </div>
        </div>
      </div>

      {/* Explanation */}
      <div className="card explanation-card">
        <h4 className="section-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
          Evidentiary Explanation
        </h4>
        <p className="explanation-text">{explanation}</p>
      </div>

      {/* Supporting & Contradicting Evidence */}
      <div className="evidence-grid">
        <div className="evidence-box supporting">
          <h4 className="section-title" style={{ color: 'var(--verdict-true)' }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            Supporting Evidence ({supportingEvidence.length})
          </h4>
          {supportingEvidence.length > 0 ? (
            <ul className="evidence-list">
              {supportingEvidence.map((item, idx) => (
                <li key={idx} className="evidence-item">
                  <span className="evidence-icon" style={{ color: 'var(--verdict-true)' }}>✓</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          ) : (
            <div className="evidence-empty-note">
              No corroborating statements found in retrieved sources.
            </div>
          )}
        </div>

        <div className="evidence-box contradicting">
          <h4 className="section-title" style={{ color: 'var(--verdict-false)' }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
            Contradicting Evidence ({contradictingEvidence.length})
          </h4>
          {contradictingEvidence.length > 0 ? (
            <ul className="evidence-list">
              {contradictingEvidence.map((item, idx) => (
                <li key={idx} className="evidence-item">
                  <span className="evidence-icon" style={{ color: 'var(--verdict-false)' }}>✕</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          ) : (
            <div className="evidence-empty-note">
              No direct counter-evidence or debunking statements retrieved.
            </div>
          )}
        </div>
      </div>

      {/* Retrieved Web Sources */}
      <div className="card sources-card">
        <h4 className="section-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
          </svg>
          Referenced Web Sources ({sources.length})
        </h4>

        {sources.length > 0 ? (
          <div className="sources-grid">
            {sources.map((src, idx) => (
              <div key={idx} className="source-item">
                <div>
                  <a
                    href={src.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="source-title"
                  >
                    <span>{src.title || 'Source Reference'}</span>
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                      <polyline points="15 3 21 3 21 9"></polyline>
                      <line x1="10" y1="14" x2="21" y2="3"></line>
                    </svg>
                  </a>
                  {src.snippet && <p className="source-snippet">{src.snippet}</p>}
                </div>

                <div className="source-meta">
                  <span className="source-date-badge">
                    {src.date && src.date !== 'Date not available' ? src.date : 'Date not available'}
                  </span>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-subtle)' }}>
                    {src.relevance || 'Search Evidence'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="evidence-empty-note" style={{ padding: '14px 0' }}>
            No external sources were retrieved for this claim.
          </div>
        )}
      </div>

      {/* Limitations Box */}
      {limitations.length > 0 && (
        <div className="limitations-box">
          <div className="limitations-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            Fact-Checking Scope & Limitations
          </div>
          <ul className="limitations-list">
            {limitations.map((lim, idx) => (
              <li key={idx}>{lim}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Footer navigation */}
      <div className="result-footer">
        <button className="secondary-btn" onClick={onViewHistory}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 8v4l3 3"></path>
            <circle cx="12" cy="12" r="9"></circle>
          </svg>
          View in Global History
        </button>

        <button className="primary-btn" onClick={onReset}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.85.83 6.72 2.24L21 8"></path>
            <polyline points="21 3 21 8 16 8"></polyline>
          </svg>
          Check Another Claim
        </button>
      </div>
    </div>
  );
};
