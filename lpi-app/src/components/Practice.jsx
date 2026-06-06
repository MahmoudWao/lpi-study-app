import { useState, useCallback, useMemo } from 'react';
import { useApp } from '../context/AppContext';
import { useKeyboard } from '../hooks/useKeyboard';
import Mascot from './Mascot';
import TopicPills from './TopicPills';
import DATA from '../data/questions.json';
import { isDue, getWeakCards, isWeak } from '../utils/sm2';
import { esc, stripQuestion, ENCOURAGEMENTS } from '../utils/helpers';

export default function Practice() {
  const { state, save, grade, getDueCards, getCardsBySection, allCards } = useApp();
  const [encourage, setEncourage] = useState(null);
  const [weakMode, setWeakMode] = useState(false);
  const [weakIdx, setWeakIdx] = useState(0);

  const handleGrade = useCallback((cardId, gradeVal) => {
    grade(cardId, gradeVal);
    save(s => ({ ...s, fcFlipped: false }));
    if (gradeVal >= 2) {
      const e = ENCOURAGEMENTS[Math.floor(Math.random() * ENCOURAGEMENTS.length)];
      setEncourage(e);
      setTimeout(() => setEncourage(null), 1500);
    }
  }, [grade, save]);

  if (encourage) {
    return <div className="encourage"><Mascot mood="celebrating" size="lg" message={encourage.h} /><div className="big">{encourage.big}</div><h3>{encourage.h}</h3><p>{encourage.p}</p></div>;
  }

  if (weakMode) {
    const weakCards = getWeakCards(allCards, state.cards);
    if (weakIdx >= weakCards.length || weakCards.length === 0) {
      return (
        <>
          <button className="back-btn" onClick={() => { setWeakMode(false); setWeakIdx(0); }}>← Back</button>
          <div className="encourage"><div className="big">💪</div><h3>Weak areas reviewed!</h3><p>Great work tackling your toughest cards. Try a regular practice session next.</p></div>
        </>
      );
    }
    const card = weakCards[weakIdx];
    return <WeakReview card={card} idx={weakIdx} total={weakCards.length} state={state} save={save} handleGrade={(id, g) => { handleGrade(id, g); setWeakIdx(i => i + 1); }} onBack={() => { setWeakMode(false); setWeakIdx(0); }} />;
  }

  if (state.currentSection) return <SectionChallenge state={state} save={save} handleGrade={handleGrade} getCardsBySection={getCardsBySection} />;

  const due = getDueCards();
  const weakCards = getWeakCards(allCards, state.cards);
  return (
    <>
      <TopicPills />
      <div style={{ textAlign: 'center', marginBottom: '1.2rem', color: 'var(--muted)', fontSize: '0.85rem' }}>
        <strong style={{ color: 'var(--primary)' }}>{due.length}</strong> questions waiting for you
      </div>
      {weakCards.length > 0 && (
        <button className="btn btn-outline" style={{ width: '100%', marginBottom: '1rem', borderColor: 'var(--red)', color: 'var(--red)' }} onClick={() => { setWeakMode(true); setWeakIdx(0); }}>
          🎯 Focus on Weak Areas ({weakCards.length} cards)
        </button>
      )}
      <div className="grid">
        {Object.entries(DATA).filter(([, sec]) => !state.topicFilter || sec.topic_num === state.topicFilter).map(([id, sec]) => {
          const m = state.mastery[id] || { level: 0 };
          const sectionCards = getCardsBySection(id);
          const sectionDue = sectionCards.filter(c => isDue(state.cards, c.id)).length;
          const sectionWeak = sectionCards.filter(c => state.cards[c.id] && isWeak(state.cards[c.id])).length;
          const pct = sectionCards.length ? Math.round(((sectionCards.length - sectionDue) / sectionCards.length) * 100) : 0;
          const colors = ['var(--card)', 'var(--amber-light)', 'var(--primary-light)', 'var(--green-light)'];
          const icons = ['📘', '📙', '📕', '✅'];
          return (
            <div key={id} className="sec-card" onClick={() => save(s => ({ ...s, currentSection: id }))} style={sectionWeak > 0 ? { borderColor: sectionWeak >= 5 ? 'var(--red)' : 'var(--amber)' } : undefined}>
              <div className="icon" style={{ background: colors[m.level] }}>{icons[m.level]}</div>
              <div className="info"><h3>{sec.title}</h3><div className="meta">Topic {sec.topic_num} · {sectionDue} due{sectionWeak > 0 ? ` · ${sectionWeak} weak` : ''}</div></div>
              <div className={`ring ring-${m.level}`}>{pct}%</div>
            </div>
          );
        })}
      </div>
    </>
  );
}

function SectionChallenge({ state, save, handleGrade, getCardsBySection }) {
  const sec = DATA[state.currentSection];
  const allCards = getCardsBySection(state.currentSection);
  const cards = allCards.filter(c => isDue(state.cards, c.id));
  const done = allCards.length - cards.length;
  const pct = allCards.length ? Math.round((done / allCards.length) * 100) : 100;
  const card = cards.length > 0 ? cards[0] : null;
  const [highlight, setHighlight] = useState(-1);

  useKeyboard(useMemo(() => ({
    ' ': () => save(s => ({ ...s, fcFlipped: !s.fcFlipped })),
    '1': () => { if (state.fcFlipped && card) { setHighlight(0); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 0); } },
    '2': () => { if (state.fcFlipped && card) { setHighlight(1); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 1); } },
    '3': () => { if (state.fcFlipped && card) { setHighlight(2); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 2); } },
    '4': () => { if (state.fcFlipped && card) { setHighlight(3); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 3); } },
  }), [state.fcFlipped, card, handleGrade, save]), true);

  if (!card) {
    return (
      <>
        <button className="back-btn" onClick={() => save(s => ({ ...s, currentSection: null }))}>← Back</button>
        <div className="encourage"><div className="big">🎉</div><h3>Section complete!</h3><p>All {allCards.length} cards reviewed. Come back later for spaced review.</p></div>
      </>
    );
  }

  const isNew = !state.cards[card.id] || state.cards[card.id].reps === 0;
  const labelMap = { command: 'What does this command do?', reverse: 'What command does this?', concept: 'Define this term' };
  const label = labelMap[card.type] || 'Answer the question';

  return (
    <>
      <button className="back-btn" onClick={() => save(s => ({ ...s, currentSection: null }))}>← Back</button>
      <div className="focus">
        <div className="focus-progress"><div className="bar"><div className="fill" style={{ width: `${pct}%` }}></div></div><span>{done}/{allCards.length}</span></div>
        <div className="focus-label">{isNew ? '🆕 New' : '🔄 Review'} · {label}</div>
        <div className="fc-wrap" onClick={() => save(s => ({ ...s, fcFlipped: !s.fcFlipped }))}>
          <div className={`fc ${state.fcFlipped ? 'flipped' : ''}`}>
            <div className="fc-face fc-front"><h3>{esc(card.front)}</h3></div>
            <div className="fc-face fc-back"><p>{esc(stripQuestion(card.back, card.front))}</p></div>
          </div>
        </div>
        <p className="fc-hint">Tap card to flip</p>
        {state.fcFlipped && (
          <div className="grades">
            {[{ g: 0, e: '😵', l: 'Missed' }, { g: 1, e: '😅', l: 'Hard' }, { g: 2, e: '👍', l: 'Good' }, { g: 3, e: '⚡', l: 'Easy' }].map(({ g, e, l }) => (
              <div key={g} className={`grade grade-${g}${highlight === g ? ' picked' : ''}`} onClick={() => handleGrade(card.id, g)}>
                <span className="emoji">{e}</span><span className="label">{l}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}


function WeakReview({ card, idx, total, state, save, handleGrade, onBack }) {
  const [highlight, setHighlight] = useState(-1);
  const pct = Math.round(idx / total * 100);

  useKeyboard(useMemo(() => ({
    ' ': () => save(s => ({ ...s, fcFlipped: !s.fcFlipped })),
    '1': () => { if (state.fcFlipped) { setHighlight(0); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 0); } },
    '2': () => { if (state.fcFlipped) { setHighlight(1); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 1); } },
    '3': () => { if (state.fcFlipped) { setHighlight(2); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 2); } },
    '4': () => { if (state.fcFlipped) { setHighlight(3); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, 3); } },
  }), [state.fcFlipped, card, handleGrade, save]), true);

  const labelMap = { command: 'What does this command do?', reverse: 'What command does this?', concept: 'Define this term' };
  return (
    <>
      <button className="back-btn" onClick={onBack}>← Back</button>
      <div style={{ textAlign: 'center', marginBottom: '0.5rem', fontSize: '0.78rem', color: 'var(--red)', fontWeight: 600 }}>🎯 WEAK AREAS REVIEW</div>
      <div className="focus">
        <div className="focus-progress"><div className="bar"><div className="fill" style={{ width: `${pct}%`, background: 'var(--red)' }}></div></div><span>{idx}/{total}</span></div>
        <div className="focus-label">🔄 Review · {labelMap[card.type] || 'Answer the question'}</div>
        <div className="fc-wrap" onClick={() => save(s => ({ ...s, fcFlipped: !s.fcFlipped }))}>
          <div className={`fc ${state.fcFlipped ? 'flipped' : ''}`}>
            <div className="fc-face fc-front"><h3>{esc(card.front)}</h3></div>
            <div className="fc-face fc-back"><p>{esc(stripQuestion(card.back, card.front))}</p></div>
          </div>
        </div>
        <p className="fc-hint">Tap card to flip</p>
        {state.fcFlipped && (
          <div className="grades">
            {[{ g: 0, e: '😵', l: 'Missed' }, { g: 1, e: '😅', l: 'Hard' }, { g: 2, e: '👍', l: 'Good' }, { g: 3, e: '⚡', l: 'Easy' }].map(({ g, e, l }) => (
              <div key={g} className={`grade grade-${g}${highlight === g ? ' picked' : ''}`} onClick={() => { setHighlight(g); setTimeout(() => setHighlight(-1), 200); handleGrade(card.id, g); }}>
                <span className="emoji">{e}</span><span className="label">{l}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
