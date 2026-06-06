import { useState } from 'react';
import { useApp } from '../context/AppContext';
import TopicPills from './TopicPills';
import DATA from '../data/questions.json';
import { esc, stripQuestion } from '../utils/helpers';

export default function Exercises() {
  const { state, save } = useApp();

  if (state.currentSection) return <SectionExercises state={state} save={save} />;

  return (
    <>
      <TopicPills />
      <div style={{ textAlign: 'center', marginBottom: '1.2rem', color: 'var(--muted)', fontSize: '0.85rem' }}>Guided exercises — write your answers before checking</div>
      <div className="grid">
        {Object.entries(DATA).filter(([, sec]) => !state.topicFilter || sec.topic_num === state.topicFilter).map(([id, sec]) => (
          <div key={id} className="sec-card" onClick={() => save(s => ({ ...s, currentSection: id }))}>
            <div className="icon" style={{ background: 'var(--card)' }}>✍️</div>
            <div className="info"><h3>{sec.title}</h3><div className="meta">Topic {sec.topic_num} · {sec.qa_pairs.length} questions</div></div>
          </div>
        ))}
      </div>
    </>
  );
}

function SectionExercises({ state, save }) {
  const sec = DATA[state.currentSection];
  const [revealed, setRevealed] = useState({});

  return (
    <>
      <button className="back-btn" onClick={() => save(s => ({ ...s, currentSection: null }))}>← Back</button>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700 }}>{state.currentSection} — {sec.title}</h2>
        <p style={{ color: 'var(--muted)', fontSize: '0.83rem', marginTop: '0.3rem' }}>Write your answer, then check against the model answer.</p>
      </div>
      {sec.qa_pairs.map((qa, i) => (
        <div key={i} className="ex-card">
          <div className="ex-num">Question {i + 1}</div>
          <div className="ex-q">{esc(qa.question)}</div>
          <textarea className="ex-input" placeholder="Type your answer here..." />
          <div className="ex-actions">
            <button className="btn btn-primary btn-sm" onClick={() => setRevealed(r => ({ ...r, [i]: true }))}>Check Answer</button>
          </div>
          {revealed[i] && <div className="answer">{esc(stripQuestion(qa.answer, qa.question))}</div>}
        </div>
      ))}
    </>
  );
}
