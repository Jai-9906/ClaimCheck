import React, { useState } from 'react';
import { Navbar } from './components/Navbar.jsx';
import { ClaimForm } from './components/ClaimForm.jsx';
import { CheckingProgress } from './components/CheckingProgress.jsx';
import { ResultCard } from './components/ResultCard.jsx';
import { HistoryList } from './components/HistoryList.jsx';

export default function App() {
  const [activeTab, setActiveTab] = useState('home'); // 'home' | 'history'
  const [verificationState, setVerificationState] = useState('idle'); // 'idle' | 'loading' | 'result'
  const [currentClaim, setCurrentClaim] = useState('');
  const [currentReport, setCurrentReport] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const handleVerifyClaim = async (claimText) => {
    setCurrentClaim(claimText);
    setVerificationState('loading');
    setErrorMsg(null);

    try {
      const response = await fetch('/api/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ claim: claimText }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.message || 'Verification failed. Please check server status.');
      }

      setCurrentReport(result.data);
      setVerificationState('result');
    } catch (err) {
      console.error('Verification error:', err);
      setErrorMsg(err.message || 'An unexpected error occurred during verification.');
      setVerificationState('idle');
    }
  };

  const handleReset = () => {
    setVerificationState('idle');
    setCurrentReport(null);
    setCurrentClaim('');
    setErrorMsg(null);
  };

  const handleViewHistory = () => {
    setActiveTab('history');
  };

  return (
    <div className="app-wrapper">
      <Navbar
        activeTab={activeTab}
        onTabChange={(tab) => {
          setActiveTab(tab);
          setErrorMsg(null);
        }}
      />

      <main className="main-content">
        {/* Error notification banner */}
        {errorMsg && (
          <div
            className="card"
            style={{
              borderColor: '#fca5a5',
              background: '#fef2f2',
              color: '#991b1b',
              marginBottom: '24px',
              padding: '16px 20px',
              display: 'flex',
              alignItems: 'flex-start',
              justifyContent: 'space-between',
              gap: '12px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <div>
                <strong>Verification Notice:</strong> {errorMsg}
              </div>
            </div>
            <button
              onClick={() => setErrorMsg(null)}
              style={{ background: 'transparent', color: '#991b1b', fontWeight: 'bold', fontSize: '1rem' }}
            >
              ✕
            </button>
          </div>
        )}

        {/* Tab 1: Home / Verify */}
        {activeTab === 'home' && (
          <>
            {verificationState === 'idle' && (
              <ClaimForm
                onSubmit={handleVerifyClaim}
                isLoading={false}
              />
            )}

            {verificationState === 'loading' && (
              <CheckingProgress
                claim={currentClaim}
              />
            )}

            {verificationState === 'result' && (
              <ResultCard
                report={currentReport}
                onReset={handleReset}
                onViewHistory={handleViewHistory}
              />
            )}
          </>
        )}

        {/* Tab 2: History */}
        {activeTab === 'history' && (
          <HistoryList
            onNavigateHome={() => {
              setActiveTab('home');
              setVerificationState('idle');
            }}
          />
        )}
      </main>

      <footer className="footer">
        <div style={{ maxWidth: '1080px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
          <div>
            <strong>ClaimCheck</strong> • Real-Time Fact-Checking Web Application (MERN Stack)
          </div>
          <div>
            Powered by <strong>MongoDB</strong>, <strong>Express</strong>, <strong>React</strong>, <strong>Node.js</strong>, <strong>Gemini API</strong>, and <strong>SerpApi</strong>
          </div>
        </div>
      </footer>
    </div>
  );
}
