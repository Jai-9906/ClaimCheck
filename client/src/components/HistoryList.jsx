import React, { useState, useEffect } from 'react';
import { VerdictBadge } from './VerdictBadge.jsx';
import { ReportModal } from './ReportModal.jsx';

export const HistoryList = ({ onNavigateHome }) => {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [verdictFilter, setVerdictFilter] = useState('ALL');
  const [selectedReport, setSelectedReport] = useState(null);

  const fetchHistory = async () => {
    setIsLoading(true);
    setError(null);
    try {
      let url = '/api/history';
      const params = new URLSearchParams();
      if (verdictFilter !== 'ALL') {
        params.append('verdict', verdictFilter);
      }
      if (searchQuery.trim()) {
        params.append('search', searchQuery.trim());
      }
      if (params.toString()) {
        url += `?${params.toString()}`;
      }

      const res = await fetch(url);
      const json = await res.json();

      if (!res.ok) {
        throw new Error(json.message || 'Failed to fetch verification history.');
      }

      setHistory(json.data || []);
    } catch (err) {
      console.error('History fetch error:', err);
      setError(err.message || 'Could not connect to MongoDB server.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [verdictFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchHistory();
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-main)', marginBottom: '6px' }}>
          Verification History
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.98rem' }}>
          Explore all verified claims saved in ClaimCheck's public repository. No sign-in required.
        </p>
      </div>

      {/* Search and Filters */}
      <form onSubmit={handleSearchSubmit} className="history-controls">
        <input
          type="text"
          className="search-input"
          placeholder="Search claims by keyword (e.g., NASA, health, ice)..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />

        <select
          className="filter-select"
          value={verdictFilter}
          onChange={(e) => setVerdictFilter(e.target.value)}
        >
          <option value="ALL">All Verdicts</option>
          <option value="True">True</option>
          <option value="False">False</option>
          <option value="Misleading">Misleading</option>
          <option value="Disputed">Disputed</option>
          <option value="Unverified">Unverified</option>
        </select>

        <button type="submit" className="primary-btn" style={{ padding: '10px 20px', fontSize: '0.92rem' }}>
          Search
        </button>
      </form>

      {/* Loading State */}
      {isLoading && (
        <div className="card" style={{ textAlign: 'center', padding: '50px 20px' }}>
          <div className="spinner-outer" style={{ width: '40px', height: '40px', margin: '0 auto 16px' }}></div>
          <p style={{ color: 'var(--text-muted)', fontWeight: 600 }}>Loading saved reports from MongoDB...</p>
        </div>
      )}

      {/* Error State */}
      {!isLoading && error && (
        <div className="card" style={{ borderColor: '#fca5a5', background: '#fef2f2', padding: '30px', textAlign: 'center' }}>
          <h4 style={{ color: '#dc2626', fontWeight: 700, marginBottom: '8px' }}>Failed to Load History</h4>
          <p style={{ color: '#991b1b', marginBottom: '16px' }}>{error}</p>
          <button className="secondary-btn" onClick={fetchHistory}>
            Retry Connection
          </button>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !error && history.length === 0 && (
        <div className="empty-state">
          <div className="empty-state-icon">📋</div>
          <h3>No Fact-Check Reports Found</h3>
          <p>
            {searchQuery || verdictFilter !== 'ALL'
              ? 'No reports match your current search filters. Try clearing the search or choosing another verdict.'
              : 'No claims have been verified yet. Check your first claim to see it recorded here!'}
          </p>
          <button className="primary-btn" onClick={onNavigateHome}>
            Verify a Claim Now
          </button>
        </div>
      )}

      {/* Results Grid */}
      {!isLoading && !error && history.length > 0 && (
        <div className="history-grid">
          {history.map((item) => {
            const formattedDate = new Date(item.createdAt).toLocaleString(undefined, {
              dateStyle: 'medium',
              timeStyle: 'short',
            });

            return (
              <div key={item.id} className="history-card">
                <div className="history-card-body">
                  <div className="history-card-claim">"{item.claimText}"</div>
                  <div className="history-card-meta">
                    <span>🕒 {formattedDate}</span>
                    <span>•</span>
                    <span>Confidence: <strong>{item.confidence}%</strong></span>
                    {item.sources && (
                      <>
                        <span>•</span>
                        <span>{item.sources.length} sources analyzed</span>
                      </>
                    )}
                  </div>
                </div>

                <div className="history-card-actions">
                  <VerdictBadge verdict={item.verdict} />

                  <button
                    className="secondary-btn"
                    onClick={() => setSelectedReport(item)}
                    style={{ whiteSpace: 'nowrap' }}
                  >
                    View Report
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Full Report Inspector Modal */}
      {selectedReport && (
        <ReportModal
          report={selectedReport}
          onClose={() => setSelectedReport(null)}
        />
      )}
    </div>
  );
};
