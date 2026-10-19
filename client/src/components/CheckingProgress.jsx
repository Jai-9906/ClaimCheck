import React, { useState, useEffect } from 'react';

const STAGES = [
  { id: 1, title: 'Identifying Main Claim', desc: 'Parsing entities and formulating focused queries...' },
  { id: 2, title: 'Searching Web Sources', desc: 'Retrieving organic search results via SerpApi...' },
  { id: 3, title: 'Analyzing Evidence', desc: 'Cross-referencing supporting vs contradicting evidence...' },
  { id: 4, title: 'Generating Verdict', desc: 'Evaluating confidence, limitations, and reasoning...' },
];

export const CheckingProgress = ({ claim }) => {
  const [currentStage, setCurrentStage] = useState(1);
  const [secondsElapsed, setSecondsElapsed] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsElapsed((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Update progress stages based on typical pipeline timeline while request is pending
  useEffect(() => {
    if (secondsElapsed < 3) {
      setCurrentStage(1);
    } else if (secondsElapsed < 7) {
      setCurrentStage(2);
    } else if (secondsElapsed < 12) {
      setCurrentStage(3);
    } else {
      setCurrentStage(4);
    }
  }, [secondsElapsed]);

  return (
    <div className="card checking-card">
      <div className="checking-spinner-box">
        <div className="spinner-outer"></div>
      </div>

      <h3 className="checking-title">Verifying Claim</h3>
      <p className="checking-claim-preview">"{claim}"</p>

      <div className="stages-list">
        {STAGES.map((st) => {
          const isDone = st.id < currentStage;
          const isActive = st.id === currentStage;

          return (
            <div
              key={st.id}
              className={`stage-item ${isActive ? 'active' : ''} ${isDone ? 'completed' : ''}`}
            >
              <div className="stage-icon">
                {isDone ? (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                ) : isActive ? (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="spinning-icon">
                    <circle cx="12" cy="12" r="10" strokeDasharray="30" strokeDashoffset="10"></circle>
                  </svg>
                ) : (
                  <span style={{ fontSize: '0.8rem', opacity: 0.6 }}>{st.id}</span>
                )}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>{st.title}</span>
                  {isActive && (
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--primary)' }}>
                      In progress...
                    </span>
                  )}
                  {isDone && (
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--verdict-true)' }}>
                      Done
                    </span>
                  )}
                </div>
                {isActive && (
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-subtle)', fontWeight: 400, marginTop: '2px' }}>
                    {st.desc}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div style={{ marginTop: '24px', fontSize: '0.82rem', color: 'var(--text-subtle)' }}>
        Elapsed: <strong>{secondsElapsed}s</strong> • Contacting Gemini & SerpApi live servers
      </div>
    </div>
  );
};
