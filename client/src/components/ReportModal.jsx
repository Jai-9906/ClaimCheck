import React from 'react';
import { ResultCard } from './ResultCard.jsx';

export const ReportModal = ({ report, onClose }) => {
  if (!report) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose} title="Close report">
          ✕
        </button>

        <div style={{ marginBottom: '16px' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-main)' }}>
            Historical Fact-Check Report
          </h3>
          <span style={{ fontSize: '0.82rem', color: 'var(--text-subtle)' }}>
            Record ID: {report.id}
          </span>
        </div>

        <ResultCard
          report={report}
          onReset={onClose}
          onViewHistory={onClose}
        />
      </div>
    </div>
  );
};
