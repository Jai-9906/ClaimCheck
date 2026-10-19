import React, { useState } from 'react';

const PRESET_EXAMPLES = [
  {
    label: 'Space News',
    claim: "NASA's James Webb Space Telescope detected atmospheric carbon dioxide and water vapor on exoplanet WASP-39b.",
  },
  {
    label: 'Health Rumor',
    claim: 'Drinking boiled garlic water every morning cures 100% of viral infections and influenza within 24 hours.',
  },
  {
    label: 'Science & Climate',
    claim: 'Global average sea levels have risen by more than 20 centimeters since the year 1880.',
  },
  {
    label: 'Viral Headline',
    claim: 'A secret 5,000-year-old subterranean pyramid was discovered beneath the ice sheets of Antarctica last month.',
  },
];

export const ClaimForm = ({ onSubmit, isLoading }) => {
  const [claim, setClaim] = useState('');
  const [validationError, setValidationError] = useState('');

  const MAX_CHARS = 1000;
  const MIN_CHARS = 5;

  const handleChange = (e) => {
    const val = e.target.value;
    setClaim(val);
    if (validationError) {
      setValidationError('');
    }
  };

  const handleSelectExample = (exampleText) => {
    setClaim(exampleText);
    setValidationError('');
  };

  const handleClear = () => {
    setClaim('');
    setValidationError('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = claim.trim();

    if (!trimmed) {
      setValidationError('Please enter a statement, headline, or forwarded message to check.');
      return;
    }

    if (trimmed.length < MIN_CHARS) {
      setValidationError(`Claim must be at least ${MIN_CHARS} characters long.`);
      return;
    }

    if (trimmed.length > MAX_CHARS) {
      setValidationError(`Claim exceeds maximum limit of ${MAX_CHARS} characters.`);
      return;
    }

    setValidationError('');
    onSubmit(trimmed);
  };

  const charCount = claim.length;
  const isNearLimit = charCount > MAX_CHARS * 0.85;
  const isOverLimit = charCount > MAX_CHARS;

  return (
    <div>
      <section className="hero-section">
        <div className="hero-pill">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
          Evidence-Based Real-Time Verification
        </div>
        <h2 className="hero-title">
          Verify Before <span className="gradient-text">You Share.</span>
        </h2>
        <p className="hero-desc">
          Evaluate news headlines, viral claims, and forwarded messages against live web evidence.
          ClaimCheck cross-references search engine sources and generates transparent, evidence-backed verdicts.
        </p>
      </section>

      <div className="card claim-form-card">
        <form onSubmit={handleSubmit}>
          <div className="form-label">
            <span>Enter Claim, Headline, or Forwarded Message</span>
            <span className={`char-counter ${isOverLimit ? 'limit-exceeded' : isNearLimit ? 'near-limit' : ''}`}>
              {charCount} / {MAX_CHARS}
            </span>
          </div>

          <div className="claim-textarea-wrapper">
            <textarea
              className="claim-textarea"
              placeholder="e.g. 'NASA discovered active liquid water geysers on Saturn's moon Enceladus...'"
              value={claim}
              onChange={handleChange}
              disabled={isLoading}
              rows={4}
            />
            {claim.length > 0 && !isLoading && (
              <button
                type="button"
                className="clear-btn"
                onClick={handleClear}
                title="Clear text"
              >
                ✕
              </button>
            )}
          </div>

          {validationError && (
            <div className="validation-msg" style={{ marginBottom: '14px' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <span>{validationError}</span>
            </div>
          )}

          <div className="form-actions">
            <span style={{ fontSize: '0.85rem', color: 'var(--text-subtle)' }}>
              Supports factual assertions, news statements, and viral social media texts.
            </span>

            <button
              type="submit"
              className="primary-btn"
              disabled={isLoading || isOverLimit || claim.trim().length === 0}
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              <span>{isLoading ? 'Checking Claim...' : 'Check Claim'}</span>
            </button>
          </div>
        </form>

        <div className="presets-section">
          <div className="presets-header">Or try an example claim:</div>
          <div className="presets-grid">
            {PRESET_EXAMPLES.map((ex, idx) => (
              <button
                key={idx}
                type="button"
                className="preset-chip"
                onClick={() => handleSelectExample(ex.claim)}
                disabled={isLoading}
              >
                <strong>{ex.label}:</strong> {ex.claim.slice(0, 50)}...
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
