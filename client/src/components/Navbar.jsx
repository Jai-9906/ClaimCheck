import React, { useState, useEffect } from 'react';

export const Navbar = ({ activeTab, onTabChange }) => {
  const [backendStatus, setBackendStatus] = useState('checking'); // 'online' | 'offline' | 'checking'

  const checkStatus = async () => {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        setBackendStatus(data.database?.connected ? 'online' : 'degraded');
      } else {
        setBackendStatus('offline');
      }
    } catch {
      setBackendStatus('offline');
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="brand" onClick={() => onTabChange('home')}>
          <div className="brand-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
              <path d="m9 12 2 2 4-4"></path>
            </svg>
          </div>
          <div className="brand-text">
            <h1>ClaimCheck</h1>
            <span>Real-Time Fact-Checker</span>
          </div>
        </div>

        <div className="nav-links">
          <button
            className={`nav-btn ${activeTab === 'home' ? 'active' : ''}`}
            onClick={() => onTabChange('home')}
          >
            Verify Claim
          </button>
          <button
            className={`nav-btn ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => onTabChange('history')}
          >
            History
          </button>

          <div className="system-status" title={`Backend & Database: ${backendStatus}`}>
            <span className={`status-dot ${backendStatus === 'online' ? 'online' : ''}`}></span>
            <span>{backendStatus === 'online' ? 'System Online' : backendStatus === 'degraded' ? 'DB Degraded' : 'Backend Offline'}</span>
          </div>
        </div>
      </div>
    </nav>
  );
};
