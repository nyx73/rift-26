import { useState, useRef, useEffect, useMemo } from 'react';

const severityLabel = (score) => {
  if (score >= 80) return { label: 'Critical', cls: 'bg-red-100 text-red-700' };
  if (score >= 60) return { label: 'High', cls: 'bg-orange-100 text-orange-700' };
  if (score >= 40) return { label: 'Medium', cls: 'bg-yellow-100 text-yellow-700' };
  return { label: 'Low', cls: 'bg-green-100 text-green-700' };
};

const Notification = ({ data, onHighlight }) => {
  const [open, setOpen] = useState(false);
  const [popup, setPopup] = useState(null); // account object for metrics popup
  const dropdownRef = useRef(null);

  const suspiciousAccounts = data?.suspicious_accounts || [];
  const count = suspiciousAccounts.length;

  // Top 5 highest risk accounts (memoized to avoid re-sorting on every render)
  const top5 = useMemo(() => (
    [...suspiciousAccounts]
      .sort((a, b) => b.suspicion_score - a.suspicion_score)
      .slice(0, 5)
  ), [suspiciousAccounts]);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false);
        setPopup(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleEntryClick = (acc) => {
    if (onHighlight) onHighlight([acc.account_id]);
    setPopup(acc);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Notification button */}
      <button
        onClick={() => { setOpen((o) => !o); setPopup(null); }}
        className="w-8 h-8 rounded-lg bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-600 transition-colors relative"
        title={count > 0 ? `${count} suspicious accounts flagged` : 'No suspicious accounts'}
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        {count > 0 && (
          <span className="absolute -top-1 -right-1 min-w-[18px] h-[18px] bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center px-0.5">
            {count > 99 ? '99+' : count}
          </span>
        )}
      </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute right-0 top-10 w-80 bg-white border border-gray-200 rounded-xl shadow-xl z-50 overflow-hidden">
          <div className="px-4 py-3 bg-slate-800 text-white flex items-center justify-between">
            <span className="text-sm font-semibold">Suspicious Accounts</span>
            <span className="text-xs bg-red-500 px-2 py-0.5 rounded-full font-bold">{count} flagged</span>
          </div>

          {count === 0 ? (
            <div className="px-4 py-6 text-center text-gray-400 text-sm">
              No suspicious accounts detected yet.
            </div>
          ) : (
            <ul className="divide-y divide-gray-100 max-h-72 overflow-y-auto">
              {top5.map((acc) => {
                const { label, cls } = severityLabel(acc.suspicion_score);
                return (
                  <li key={acc.account_id}>
                    <button
                      onClick={() => handleEntryClick(acc)}
                      className="w-full text-left px-4 py-3 hover:bg-slate-50 transition-colors"
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-mono text-sm font-semibold text-gray-800">{acc.account_id}</span>
                        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${cls}`}>{label}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-gray-200 rounded-full h-1.5">
                          <div
                            className="h-1.5 rounded-full bg-gradient-to-r from-yellow-400 to-red-500"
                            style={{ width: `${acc.suspicion_score}%` }}
                          />
                        </div>
                        <span className="text-xs font-semibold text-gray-600">{acc.suspicion_score}/100</span>
                      </div>
                    </button>
                  </li>
                );
              })}
            </ul>
          )}

          {count > 5 && (
            <div className="px-4 py-2 border-t border-gray-100 text-xs text-gray-400 text-center">
              +{count - 5} more — see Suspicious Accounts tab
            </div>
          )}
        </div>
      )}

      {/* Account metrics popup */}
      {popup && (
        <div className="absolute right-0 top-10 w-72 bg-white border border-gray-200 rounded-xl shadow-xl z-[60] overflow-hidden">
          <div className="px-4 py-3 bg-indigo-700 text-white flex items-center justify-between">
            <span className="font-mono text-sm font-bold">{popup.account_id}</span>
            <button onClick={() => setPopup(null)} className="text-indigo-200 hover:text-white">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="p-4 space-y-3 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-gray-500">Suspicion Score</span>
              <span className="font-bold text-gray-800">{popup.suspicion_score}/100</span>
            </div>
            <div>
              <span className="text-gray-500 block mb-1">Detected Patterns</span>
              <div className="flex flex-wrap gap-1">
                {popup.detected_patterns.map((p) => (
                  <span key={p} className="px-2 py-0.5 rounded-full text-xs bg-indigo-100 text-indigo-700 font-medium">{p}</span>
                ))}
              </div>
            </div>
            {popup.ring_id && (
              <div className="flex items-center justify-between">
                <span className="text-gray-500">Fraud Ring</span>
                <span className="font-mono text-purple-700 font-semibold">{popup.ring_id}</span>
              </div>
            )}
            <button
              onClick={() => { if (onHighlight) onHighlight([popup.account_id]); }}
              className="w-full mt-1 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold transition-colors"
            >
              Highlight in Graph
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Notification;
