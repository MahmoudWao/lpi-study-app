import { useKeyboard } from '../hooks/useKeyboard';

const SHORTCUTS = [
  { key: 'Space', ctx: 'Practice / Flashcards', action: 'Flip card / Show answer' },
  { key: '1', ctx: 'After answer shown', action: 'Grade: Missed' },
  { key: '2', ctx: 'After answer shown', action: 'Grade: Hard' },
  { key: '3', ctx: 'After answer shown', action: 'Grade: Good' },
  { key: '4', ctx: 'After answer shown', action: 'Grade: Easy' },
  { key: '← / →', ctx: 'Flashcards', action: 'Previous / Next card' },
  { key: 'A / B / C / D', ctx: 'Exam mode', action: 'Select answer' },
  { key: 'Enter', ctx: 'Exam (after answer)', action: 'Next question' },
  { key: '?', ctx: 'Global', action: 'Toggle this overlay' },
  { key: 'Esc', ctx: 'Any overlay', action: 'Close' },
];

export default function KeyboardOverlay({ onClose }) {
  useKeyboard({ Escape: onClose }, true);

  return (
    <div className="kb-overlay" onClick={onClose}>
      <div className="kb-modal" onClick={e => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 style={{ fontSize: '1rem', fontWeight: 700 }}>⌨️ Keyboard Shortcuts</h2>
          <button className="back-btn" onClick={onClose}>✕</button>
        </div>
        <div className="kb-list">
          {SHORTCUTS.map((s, i) => (
            <div key={i} className="kb-row">
              <kbd className="kb-key">{s.key}</kbd>
              <span className="kb-action">{s.action}</span>
              <span className="kb-ctx">{s.ctx}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
