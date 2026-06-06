import { useTheme } from '../context/ThemeContext';
import { useApp } from '../context/AppContext';
import Mascot from './Mascot';

export default function Header({ onShowShortcuts }) {
  const { toggle } = useTheme();
  const { state } = useApp();

  const mascotMood = state.streak === 0 && state.lastStudyDate ? 'worried' : 'happy';
  const mascotMsg = state.streak === 0 && state.lastStudyDate ? 'Welcome back! Let\'s study!' :
    (state.streak === 7 || state.streak === 14 || state.streak === 30) ? `${state.streak} day streak! 🔥` : undefined;

  return (
    <div className="header">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
        <Mascot mood={mascotMood} size="sm" message={mascotMsg} />
        <h1>🐧 Linux Essentials</h1>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
        <button className="theme-toggle" onClick={onShowShortcuts} title="Keyboard shortcuts (?)">?</button>
        <button className="theme-toggle" onClick={toggle}>🌓</button>
        {state.streak > 0 && <div className="streak">🔥 {state.streak}</div>}
      </div>
    </div>
  );
}
