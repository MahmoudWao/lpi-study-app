import { useState, useMemo, useEffect, lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AppProvider } from './context/AppContext';
import { useKeyboard } from './hooks/useKeyboard';
import Header from './components/Header';
import Nav from './components/Nav';
import KeyboardOverlay from './components/KeyboardOverlay';
import Practice from './components/Practice';
import './styles/theme.css';

const Learn = lazy(() => import('./components/Learn'));
const Exercises = lazy(() => import('./components/Exercises'));
const Terminal = lazy(() => import('./components/Terminal'));
const Flashcards = lazy(() => import('./components/Flashcards'));
const Exam = lazy(() => import('./components/Exam'));
const Stats = lazy(() => import('./components/Stats'));

function AppShell() {
  const [showShortcuts, setShowShortcuts] = useState(false);
  const [installPrompt, setInstallPrompt] = useState(null);
  const [showInstall, setShowInstall] = useState(() => !localStorage.getItem('lpi_install_dismissed'));
  const [offline, setOffline] = useState(!navigator.onLine);
  const { pathname } = useLocation();
  const isTerminal = pathname === '/terminal';

  useEffect(() => {
    const handleInstall = (e) => { e.preventDefault(); setInstallPrompt(e); };
    const goOffline = () => setOffline(true);
    const goOnline = () => setOffline(false);
    window.addEventListener('beforeinstallprompt', handleInstall);
    window.addEventListener('offline', goOffline);
    window.addEventListener('online', goOnline);
    return () => { window.removeEventListener('beforeinstallprompt', handleInstall); window.removeEventListener('offline', goOffline); window.removeEventListener('online', goOnline); };
  }, []);

  const doInstall = async () => {
    if (!installPrompt) return;
    installPrompt.prompt();
    await installPrompt.userChoice;
    setInstallPrompt(null);
    setShowInstall(false);
  };

  const dismissInstall = () => { setShowInstall(false); localStorage.setItem('lpi_install_dismissed', '1'); };

  useKeyboard(useMemo(() => ({ '?': () => setShowShortcuts(s => !s) }), []), !isTerminal);

  return (
    <div className="app">
      {offline && <div className="offline-badge">📡 Offline</div>}
      {showInstall && installPrompt && (
        <div className="install-banner">
          <span>📱 Install this app for offline access</span>
          <button className="btn btn-primary btn-sm" onClick={doInstall}>Install</button>
          <button className="btn btn-sm" onClick={dismissInstall} style={{ background: 'none', border: 'none', color: 'var(--muted)' }}>✕</button>
        </div>
      )}
      <Header onShowShortcuts={() => setShowShortcuts(s => !s)} />
      <Nav />
      <Routes>
        <Route path="/practice" element={<Practice />} />
        <Route path="/learn" element={<Suspense fallback={<div style={{textAlign:'center',padding:'2rem',color:'var(--muted)'}}>Loading...</div>}><Learn /></Suspense>} />
        <Route path="/exercises" element={<Suspense fallback={null}><Exercises /></Suspense>} />
        <Route path="/terminal" element={<Suspense fallback={null}><Terminal /></Suspense>} />
        <Route path="/flashcards" element={<Suspense fallback={null}><Flashcards /></Suspense>} />
        <Route path="/exam" element={<Suspense fallback={null}><Exam /></Suspense>} />
        <Route path="/stats" element={<Suspense fallback={null}><Stats /></Suspense>} />
        <Route path="*" element={<Navigate to="/practice" replace />} />
      </Routes>
      {showShortcuts && <KeyboardOverlay onClose={() => setShowShortcuts(false)} />}
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AppProvider>
        <BrowserRouter>
          <AppShell />
        </BrowserRouter>
      </AppProvider>
    </ThemeProvider>
  );
}
