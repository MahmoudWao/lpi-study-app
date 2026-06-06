import { useState, useMemo } from 'react';
import { useApp } from '../context/AppContext';
import { useKeyboard } from '../hooks/useKeyboard';
import { useSwipe } from '../hooks/useSwipe';
import Mascot from './Mascot';
import TopicPills from './TopicPills';
import { isDue } from '../utils/sm2';
import { esc } from '../utils/helpers';

export default function Flashcards() {
  const { state, save, grade, allCards, getDueCards } = useApp();
  const [highlight, setHighlight] = useState(-1);

  let filtered = allCards;
  if (state.topicFilter) filtered = filtered.filter(c => c.topic === state.topicFilter);
  if (state.fcFilter === 'due') filtered = filtered.filter(c => isDue(state.cards, c.id));
  else if (state.fcFilter === 'new') filtered = filtered.filter(c => !state.cards[c.id]);

  const card = filtered.length > 0 ? filtered[state.fcIdx % filtered.length] : null;

  const handleGrade = (cardId, gradeVal) => {
    grade(cardId, gradeVal);
    save(s => ({ ...s, fcIdx: s.fcIdx + 1, fcFlipped: false }));
  };

  useKeyboard(useMemo(() => ({
    ' ': () => save(s => ({ ...s, fcFlipped: !s.fcFlipped })),
    'ArrowLeft': () => save(s => ({ ...s, fcIdx: Math.max(0, s.fcIdx - 1), fcFlipped: false })),
    'ArrowRight': () => save(s => ({ ...s, fcIdx: s.fcIdx + 1, fcFlipped: false })),
    '1': () => { if (state.fcFlipped && card) { setHighlight(0); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 0); } },
    '2': () => { if (state.fcFlipped && card) { setHighlight(1); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 1); } },
    '3': () => { if (state.fcFlipped && card) { setHighlight(2); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 2); } },
    '4': () => { if (state.fcFlipped && card) { setHighlight(3); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 3); } },
  }), [state.fcFlipped, card, save]), true);

  const swipeHandlers = useSwipe({
    onLeft: () => save(s => ({ ...s, fcIdx: s.fcIdx + 1, fcFlipped: false })),
    onRight: () => save(s => ({ ...s, fcIdx: Math.max(0, s.fcIdx - 1), fcFlipped: false })),
  });

  return (
    <>
      <TopicPills />
      <div className="pills" style={{ marginTop: '0.5rem' }}>
        <button className={state.fcFilter === 'due' ? 'active' : ''} onClick={() => save(s => ({ ...s, fcFilter: 'due', fcIdx: 0, fcFlipped: false }))}>Due ({getDueCards().length})</button>
        <button className={state.fcFilter === 'all' ? 'active' : ''} onClick={() => save(s => ({ ...s, fcFilter: 'all', fcIdx: 0, fcFlipped: false }))}>All</button>
        <button className={state.fcFilter === 'new' ? 'active' : ''} onClick={() => save(s => ({ ...s, fcFilter: 'new', fcIdx: 0, fcFlipped: false }))}>New</button>
      </div>

      {!filtered.length ? (
        <div className="encourage"><Mascot mood="sleeping" size="lg" message="All done for now!" /><div className="big">🎉</div><h3>All caught up!</h3><p>No cards due right now.</p></div>
      ) : (() => {
        const idx = state.fcIdx % filtered.length;
        const card = filtered[idx];
        return (
          <>
            <div style={{ textAlign: 'center', marginBottom: '0.8rem' }}>
              <span style={{ fontSize: '0.72rem', color: 'var(--muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>{card.sectionTitle}</span>
            </div>
            <div className="fc-wrap" onClick={() => save(s => ({ ...s, fcFlipped: !s.fcFlipped }))} {...swipeHandlers}>
              <div className={`fc ${state.fcFlipped ? 'flipped' : ''}`}>
                <div className="fc-face fc-front"><h3>{esc(card.front)}</h3></div>
                <div className="fc-face fc-back"><p>{esc(card.back)}</p></div>
              </div>
            </div>
            <p className="fc-hint">Tap to flip · Arrow keys to navigate</p>
            <div className="fc-nav">
              <button onClick={() => save(s => ({ ...s, fcIdx: Math.max(0, s.fcIdx - 1), fcFlipped: false }))}>←</button>
              <span style={{ color: 'var(--muted)', fontSize: '0.8rem' }}>{idx + 1}/{filtered.length}</span>
              <button onClick={() => save(s => ({ ...s, fcIdx: s.fcIdx + 1, fcFlipped: false }))}>→</button>
              <button onClick={() => { allCards.sort(() => Math.random() - 0.5); save(s => ({ ...s, fcIdx: 0, fcFlipped: false })); }}>🔀 Reshuffle</button>
            </div>
            {state.fcFlipped && (
              <div className="grades" style={{ marginTop: '1rem' }}>
                {[{ g: 0, e: '😵', l: 'Missed' }, { g: 1, e: '😅', l: 'Hard' }, { g: 2, e: '👍', l: 'Good' }, { g: 3, e: '⚡', l: 'Easy' }].map(({ g, e, l }) => (
                  <div key={g} className={`grade grade-${g}${highlight === g ? ' picked' : ''}`} onClick={() => handleGrade(card.id, g)}>
                    <span className="emoji">{e}</span><span className="label">{l}</span>
                  </div>
                ))}
              </div>
            )}
          </>
        );
      })()}
    </>
  );
}
