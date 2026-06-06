import { useApp } from '../context/AppContext';
import Mascot, { useMascotVisible } from './Mascot';
import DATA from '../data/questions.json';
import { isDue, isWeak, getWeakCards, getRecoveredThisWeek } from '../utils/sm2';
import { TOPICS } from '../utils/helpers';
import { saveState, defaultState } from '../utils/storage';

export default function Stats() {
  const { state, allCards, getCardsBySection, save } = useApp();
  const [mascotOn, toggleMascot] = useMascotVisible();
  const total = allCards.length;
  const reviewed = Object.keys(state.cards).length;
  const mastered = Object.values(state.cards).filter(c => c.reps >= 3).length;
  const due = allCards.filter(c => isDue(state.cards, c.id)).length;
  const weakCards = getWeakCards(allCards, state.cards);
  const recovered = getRecoveredThisWeek(state.cards);

  // Weakest topics
  const weakByTopic = {};
  weakCards.forEach(c => { weakByTopic[c.topic] = (weakByTopic[c.topic] || 0) + 1; });
  const sortedWeakTopics = Object.entries(weakByTopic).sort((a, b) => b[1] - a[1]);

  return (
    <>
      <div className="stats">
        <div className="stat"><div className="n">{state.totalReviews}</div><div className="l">Reviews</div></div>
        <div className="stat"><div className="n">{reviewed}/{total}</div><div className="l">Cards Seen</div></div>
        <div className="stat"><div className="n">{mastered}</div><div className="l">Mastered</div></div>
        <div className="stat"><div className="n">{due}</div><div className="l">Due</div></div>
        <div className="stat"><div className="n" style={{ color: weakCards.length > 0 ? 'var(--red)' : 'var(--green)' }}>{weakCards.length}</div><div className="l">Weak</div></div>
        <div className="stat"><div className="n" style={{ color: 'var(--green)' }}>{recovered}</div><div className="l">Recovered</div></div>
      </div>
      <div className="progress-bar" style={{ marginBottom: '1.5rem' }}>
        <div className="progress-fill pf-primary" style={{ width: `${(reviewed / total) * 100}%` }}></div>
      </div>
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <Mascot mood={weakCards.length > 0 ? 'studying' : 'celebrating'} size="md" message={weakCards.length > 0 ? "Let's focus on these!" : "You're crushing it!"} />
      </div>
      {sortedWeakTopics.length > 0 && (
        <div className="panel" style={{ marginBottom: '1.5rem', borderColor: 'var(--red)' }}>
          <h2 style={{ color: 'var(--red)' }}>🎯 Weakest Topics</h2>
          {sortedWeakTopics.map(([t, count]) => (
            <div key={t} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.3rem 0', fontSize: '0.85rem' }}>
              <span>Topic {t}: {TOPICS[t]}</span>
              <span style={{ color: 'var(--red)', fontWeight: 600 }}>{count} weak</span>
            </div>
          ))}
        </div>
      )}
      {Object.entries(TOPICS).map(([num, name]) => (
        <div key={num} style={{ marginBottom: '1rem' }}>
          <div style={{ fontWeight: 600, fontSize: '0.85rem', marginBottom: '0.4rem' }}>Topic {num}: {name}</div>
          {Object.entries(DATA).filter(([, s]) => s.topic_num === num).map(([id, sec]) => {
            const m = state.mastery[id] || { level: 0 };
            const cards = getCardsBySection(id);
            const pct = cards.length ? Math.round((cards.filter(c => !isDue(state.cards, c.id)).length / cards.length) * 100) : 0;
            return (
              <div key={id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.3rem 0', fontSize: '0.82rem' }}>
                <span>{['⬜', '🟨', '🟦', '🟩'][m.level]}</span><span style={{ flex: 1 }}>{sec.title}</span><span style={{ color: 'var(--muted)' }}>{pct}%</span>
              </div>
            );
          })}
        </div>
      ))}
      <button className="btn btn-outline btn-sm" onClick={toggleMascot} style={{ marginRight: '0.5rem' }}>{mascotOn ? '🐧 Hide Mascot' : '🐧 Show Mascot'}</button>
      <button className="btn btn-outline btn-sm" onClick={() => { if (window.confirm('Reset all progress?')) { const fresh = defaultState(); saveState(fresh); save(() => fresh); } }}>Reset Progress</button>
    </>
  );
}
