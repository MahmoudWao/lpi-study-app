import { useNavigate, useLocation } from 'react-router-dom';

const MODES = [
  { path: '/practice', label: '⚡ Practice', short: '⚡', name: 'Practice' },
  { path: '/learn', label: '📖 Learn', short: '📖', name: 'Learn' },
  { path: '/exercises', label: '✍️ Exercises', short: '✍️', name: 'Exercises' },
  { path: '/terminal', label: '💻 Terminal', short: '💻', name: 'Terminal' },
  { path: '/flashcards', label: '🃏 Cards', short: '🃏', name: 'Cards' },
  { path: '/exam', label: '🎯 Exam', short: '🎯', name: 'Exam' },
  { path: '/stats', label: '📊 Stats', short: '📊', name: 'Stats' },
];

const MOBILE_TABS = [
  { path: '/practice', icon: '⚡', name: 'Practice' },
  { path: '/learn', icon: '📖', name: 'Learn' },
  { path: '/terminal', icon: '💻', name: 'Terminal' },
  { path: '/flashcards', icon: '🃏', name: 'Cards' },
  { path: '/stats', icon: '📊', name: 'Stats' },
];

export default function Nav() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  return (
    <>
      {/* Desktop/tablet top nav */}
      <div className="nav nav-top">
        {MODES.map(m => (
          <button key={m.path} className={pathname === m.path ? 'active' : ''} onClick={() => navigate(m.path)}>
            {m.label}
          </button>
        ))}
      </div>
      {/* Mobile bottom tab bar */}
      <nav className="nav-bottom">
        {MOBILE_TABS.map(m => (
          <button key={m.path} className={pathname === m.path ? 'active' : ''} onClick={() => navigate(m.path)}>
            <span className="nav-bottom-icon">{m.icon}</span>
            <span className="nav-bottom-label">{m.name}</span>
          </button>
        ))}
      </nav>
    </>
  );
}
