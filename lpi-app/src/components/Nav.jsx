import { useNavigate, useLocation } from 'react-router-dom';

const MODES = [
  { path: '/practice', label: '⚡ Practice' },
  { path: '/learn', label: '📖 Learn' },
  { path: '/exercises', label: '✍️ Exercises' },
  { path: '/terminal', label: '💻 Terminal' },
  { path: '/flashcards', label: '🃏 Cards' },
  { path: '/exam', label: '🎯 Exam' },
  { path: '/stats', label: '📊 Stats' },
];

export default function Nav() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  return (
    <div className="nav">
      {MODES.map(m => (
        <button key={m.path} className={pathname === m.path ? 'active' : ''} onClick={() => navigate(m.path)}>
          {m.label}
        </button>
      ))}
    </div>
  );
}
