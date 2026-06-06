import { useState, useEffect, useMemo, useRef } from 'react';
import { useKeyboard } from '../hooks/useKeyboard';
import { useApp } from '../context/AppContext';
import MCQ from '../data/mcq-questions.json';
import { TOPICS } from '../utils/helpers';

function shuffleSlice(arr, n) {
  const a = [...arr].sort(() => Math.random() - 0.5);
  return n ? a.slice(0, n) : a;
}

export default function Exam() {
  const { grade } = useApp();
  const [mode, setMode] = useState('menu'); // menu | config | active | review | results | quick
  const [config, setConfig] = useState({ count: 40, topic: '', timer: true });
  const [questions, setQuestions] = useState([]);
  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState({}); // idx -> selected option
  const [flagged, setFlagged] = useState(new Set());
  const [timeLeft, setTimeLeft] = useState(3600);
  const [submitted, setSubmitted] = useState(false);
  // Quick quiz state
  const [quickAnswered, setQuickAnswered] = useState(false);
  const [quickSelected, setQuickSelected] = useState(-1);
  const timerRef = useRef(null);

  // Timer
  useEffect(() => {
    if (mode === 'active' && config.timer && !submitted) {
      timerRef.current = setInterval(() => {
        setTimeLeft(t => {
          if (t <= 1) { clearInterval(timerRef.current); setSubmitted(true); return 0; }
          return t - 1;
        });
      }, 1000);
      return () => clearInterval(timerRef.current);
    }
  }, [mode, config.timer, submitted]);

  function startExam() {
    let pool = config.topic ? MCQ.filter(q => q.d === config.topic) : MCQ;
    const qs = shuffleSlice(pool, config.count);
    setQuestions(qs);
    setAnswers({});
    setFlagged(new Set());
    setIdx(0);
    setTimeLeft(3600);
    setSubmitted(false);
    setMode('active');
  }

  function startQuickQuiz() {
    const qs = shuffleSlice(MCQ, 10);
    setQuestions(qs);
    setIdx(0);
    setQuickAnswered(false);
    setQuickSelected(-1);
    setMode('quick');
  }

  function submitExam() {
    clearInterval(timerRef.current);
    setSubmitted(true);
    setMode('results');
    localStorage.setItem('lpi_last_exam', getScore().pct.toString());
  }

  function getScore() {
    let correct = 0;
    const byTopic = {};
    questions.forEach((q, i) => {
      if (!byTopic[q.d]) byTopic[q.d] = { correct: 0, total: 0 };
      byTopic[q.d].total++;
      if (answers[i] === q.a) { correct++; byTopic[q.d].correct++; }
    });
    return { correct, total: questions.length, pct: Math.round(correct / questions.length * 100), byTopic };
  }

  // Keyboard for exam
  useKeyboard(useMemo(() => {
    if (mode === 'active' && !submitted) return {
      'a': () => setAnswers(a => ({ ...a, [idx]: 0 })), 'A': () => setAnswers(a => ({ ...a, [idx]: 0 })),
      'b': () => setAnswers(a => ({ ...a, [idx]: 1 })), 'B': () => setAnswers(a => ({ ...a, [idx]: 1 })),
      'c': () => setAnswers(a => ({ ...a, [idx]: 2 })), 'C': () => setAnswers(a => ({ ...a, [idx]: 2 })),
      'd': () => setAnswers(a => ({ ...a, [idx]: 3 })), 'D': () => setAnswers(a => ({ ...a, [idx]: 3 })),
      'ArrowRight': () => setIdx(i => Math.min(i + 1, questions.length - 1)),
      'ArrowLeft': () => setIdx(i => Math.max(i - 1, 0)),
      'f': () => setFlagged(f => { const n = new Set(f); n.has(idx) ? n.delete(idx) : n.add(idx); return n; }),
    };
    if (mode === 'quick' && !quickAnswered) return {
      'a': () => answerQuick(0), 'A': () => answerQuick(0),
      'b': () => answerQuick(1), 'B': () => answerQuick(1),
      'c': () => answerQuick(2), 'C': () => answerQuick(2),
      'd': () => answerQuick(3), 'D': () => answerQuick(3),
    };
    if (mode === 'quick' && quickAnswered) return { 'Enter': () => nextQuick() };
    return {};
  }, [mode, idx, submitted, quickAnswered, questions.length]), true);

  function answerQuick(i) {
    if (quickAnswered) return;
    setQuickSelected(i);
    setQuickAnswered(true);
    // SM-2 integration: wrong answers get penalized
    const q = questions[idx];
    if (i !== q.a) {
      // Find a matching card ID and penalize it
      const cardId = `${q.d}.1::qa::0`; // approximate - grade as wrong
      grade(cardId, 0);
    }
  }

  function nextQuick() {
    if (idx + 1 >= questions.length) {
      setMode('results');
      return;
    }
    setIdx(idx + 1);
    setQuickAnswered(false);
    setQuickSelected(-1);
  }

  // --- MENU ---
  if (mode === 'menu') {
    const lastScore = localStorage.getItem('lpi_last_exam');
    return (
      <div className="panel" style={{ textAlign: 'center' }}>
        <h2>🎯 Practice Exam</h2>
        <p style={{ color: 'var(--muted)', marginBottom: '1.5rem' }}>Test yourself with {MCQ.length} multiple-choice questions</p>
        {lastScore && <p style={{ marginBottom: '1rem', fontSize: '0.85rem' }}>Last score: <strong style={{ color: 'var(--primary)' }}>{lastScore}%</strong></p>}
        <div className="grid" style={{ gap: '0.8rem', maxWidth: '400px', margin: '0 auto' }}>
          <button className="btn btn-primary" style={{ width: '100%' }} onClick={() => setMode('config')}>📝 Exam Simulation</button>
          <button className="btn btn-outline" style={{ width: '100%' }} onClick={startQuickQuiz}>⚡ Quick Quiz (10 Q, immediate feedback)</button>
        </div>
      </div>
    );
  }

  // --- CONFIG ---
  if (mode === 'config') {
    return (
      <div className="panel">
        <button className="back-btn" onClick={() => setMode('menu')}>← Back</button>
        <h2>Exam Settings</h2>
        <div style={{ display: 'grid', gap: '1rem', marginTop: '1rem' }}>
          <div>
            <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--muted)' }}>Questions</label>
            <div className="pills" style={{ marginTop: '0.4rem' }}>
              {[20, 40, 60].map(n => (
                <button key={n} className={config.count === n ? 'active' : ''} onClick={() => setConfig(c => ({ ...c, count: n }))}>{n}</button>
              ))}
            </div>
          </div>
          <div>
            <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--muted)' }}>Topic Filter</label>
            <div className="pills" style={{ marginTop: '0.4rem' }}>
              <button className={!config.topic ? 'active' : ''} onClick={() => setConfig(c => ({ ...c, topic: '' }))}>All</button>
              {Object.entries(TOPICS).map(([num]) => (
                <button key={num} className={config.topic === num ? 'active' : ''} onClick={() => setConfig(c => ({ ...c, topic: num }))}>T{num}</button>
              ))}
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input type="checkbox" id="timer" checked={config.timer} onChange={e => setConfig(c => ({ ...c, timer: e.target.checked }))} />
            <label htmlFor="timer" style={{ fontSize: '0.85rem' }}>60-minute timer</label>
          </div>
          <button className="btn btn-primary" onClick={startExam}>Start Exam</button>
        </div>
      </div>
    );
  }

  // --- RESULTS ---
  if (mode === 'results') {
    const isQuick = questions.length === 10;
    const score = isQuick ? (() => {
      let c = 0; questions.forEach((q, i) => { if ((answers[i] ?? quickSelected) === q.a) c++; }); // approximate
      return { correct: c, total: 10, pct: Math.round(c / 10 * 100), byTopic: {} };
    })() : getScore();
    const pass = score.pct >= 65;
    return (
      <>
        <div className="panel" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>{pass ? '🎉' : '📚'}</div>
          <h2 style={{ fontSize: '2rem', color: 'var(--primary)' }}>{score.pct}%</h2>
          <p style={{ color: 'var(--muted)' }}>{score.correct}/{score.total} correct</p>
          <p style={{ marginTop: '0.8rem', fontSize: '0.9rem' }}>{pass ? 'Passing score! Keep reviewing weak areas.' : 'Below 65% passing threshold. Focus on missed topics.'}</p>
        </div>
        {!isQuick && Object.keys(score.byTopic).length > 0 && (
          <div className="panel" style={{ marginTop: '1rem' }}>
            <h2>Topic Breakdown</h2>
            {Object.entries(score.byTopic).map(([t, s]) => (
              <div key={t} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.4rem 0', fontSize: '0.85rem' }}>
                <span>Topic {t}: {TOPICS[t]}</span>
                <span style={{ color: s.correct / s.total >= 0.65 ? 'var(--green)' : 'var(--red)' }}>{s.correct}/{s.total}</span>
              </div>
            ))}
          </div>
        )}
        {!isQuick && (
          <div style={{ textAlign: 'center', marginTop: '1rem' }}>
            <button className="btn btn-outline btn-sm" style={{ marginRight: '0.5rem' }} onClick={() => { setMode('review'); setIdx(0); }}>📋 Review Answers</button>
            <button className="btn btn-primary btn-sm" onClick={() => setMode('menu')}>← Back</button>
          </div>
        )}
        {isQuick && <div style={{ textAlign: 'center', marginTop: '1rem' }}><button className="btn btn-primary" onClick={() => setMode('menu')}>← Back</button></div>}
      </>
    );
  }

  // --- REVIEW (post-exam) ---
  if (mode === 'review') {
    const q = questions[idx];
    const userAns = answers[idx];
    return (
      <div className="panel">
        <button className="back-btn" onClick={() => setMode('results')}>← Back to Results</button>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--muted)', marginBottom: '0.8rem' }}>
          <span>Q {idx + 1}/{questions.length}</span><span>Topic {q.d}</span>
        </div>
        <p style={{ fontSize: '1rem', lineHeight: 1.7, marginBottom: '1rem' }}>{q.q}</p>
        <QuestionOptions q={q} selected={userAns} answered={true} onSelect={() => {}} />
        <div className="answer" style={{ marginTop: '1rem' }}>{q.e}</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem' }}>
          <button className="btn btn-outline btn-sm" disabled={idx === 0} onClick={() => setIdx(i => i - 1)}>← Prev</button>
          <button className="btn btn-outline btn-sm" disabled={idx === questions.length - 1} onClick={() => setIdx(i => i + 1)}>Next →</button>
        </div>
      </div>
    );
  }

  // --- QUICK QUIZ ---
  if (mode === 'quick') {
    const q = questions[idx];
    return (
      <div className="panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--muted)', marginBottom: '0.8rem' }}>
          <span>Q {idx + 1}/10</span><span>Topic {q.d}</span>
        </div>
        <div className="progress-bar" style={{ marginBottom: '1.2rem' }}><div className="progress-fill pf-primary" style={{ width: `${idx / 10 * 100}%` }}></div></div>
        <p style={{ fontSize: '1rem', lineHeight: 1.7, marginBottom: '1.2rem' }}>{q.q}</p>
        <QuestionOptions q={q} selected={quickSelected} answered={quickAnswered} onSelect={answerQuick} />
        {quickAnswered && (
          <>
            <div className="answer" style={{ marginTop: '1rem' }}>{q.e}</div>
            <div style={{ marginTop: '1rem', textAlign: 'right' }}>
              <button className="btn btn-primary btn-sm" onClick={nextQuick}>{idx < 9 ? 'Next →' : 'Finish'}</button>
            </div>
          </>
        )}
      </div>
    );
  }

  // --- ACTIVE EXAM ---
  const q = questions[idx];
  const answered = Object.keys(answers).length;
  const fmtTime = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;

  return (
    <div className="panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.8rem', fontSize: '0.8rem', color: 'var(--muted)' }}>
        <span>Q {idx + 1}/{questions.length}</span>
        <span>Topic {q.d}</span>
        {config.timer && <span style={{ color: timeLeft < 300 ? 'var(--red)' : 'inherit' }}>⏱ {fmtTime(timeLeft)}</span>}
        <span>{answered}/{questions.length} answered</span>
      </div>
      <div className="progress-bar" style={{ marginBottom: '1rem' }}><div className="progress-fill pf-primary" style={{ width: `${(idx + 1) / questions.length * 100}%` }}></div></div>
      <p style={{ fontSize: '1rem', lineHeight: 1.7, marginBottom: '1.2rem' }}>{q.q}</p>
      <QuestionOptions q={q} selected={answers[idx] ?? -1} answered={false} onSelect={(i) => setAnswers(a => ({ ...a, [idx]: i }))} />
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
        <div style={{ display: 'flex', gap: '0.3rem' }}>
          <button className="btn btn-outline btn-sm" disabled={idx === 0} onClick={() => setIdx(i => i - 1)}>←</button>
          <button className="btn btn-outline btn-sm" disabled={idx === questions.length - 1} onClick={() => setIdx(i => i + 1)}>→</button>
        </div>
        <button className={`btn btn-sm ${flagged.has(idx) ? 'btn-primary' : 'btn-outline'}`} onClick={() => setFlagged(f => { const n = new Set(f); n.has(idx) ? n.delete(idx) : n.add(idx); return n; })}>
          🚩 {flagged.has(idx) ? 'Flagged' : 'Flag'}
        </button>
        <button className="btn btn-primary btn-sm" onClick={submitExam}>Submit ({answered}/{questions.length})</button>
      </div>
      {/* Question navigator */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem', marginTop: '1rem' }}>
        {questions.map((_, i) => (
          <button key={i} onClick={() => setIdx(i)} style={{
            width: '24px', height: '24px', borderRadius: '4px', border: '1px solid var(--border)',
            fontSize: '0.65rem', cursor: 'pointer',
            background: i === idx ? 'var(--primary)' : answers[i] !== undefined ? 'var(--green-light)' : flagged.has(i) ? 'var(--amber-light)' : 'var(--surface)',
            color: i === idx ? '#fff' : 'var(--text)',
          }}>{i + 1}</button>
        ))}
      </div>
    </div>
  );
}

function QuestionOptions({ q, selected, answered, onSelect }) {
  const KEYS = ['A', 'B', 'C', 'D'];
  return (
    <div style={{ display: 'grid', gap: '0.5rem' }}>
      {q.opts.map((opt, i) => {
        let style = { cursor: 'pointer', padding: '0.8rem 1rem', textAlign: 'left' };
        if (answered) {
          if (i === q.a) style = { ...style, borderColor: 'var(--green)', background: 'var(--green-light)' };
          else if (i === selected) style = { ...style, borderColor: 'var(--red)', background: 'var(--red-light)' };
        } else if (i === selected) {
          style = { ...style, borderColor: 'var(--primary)', background: 'var(--primary-light)' };
        }
        return (
          <button key={i} className="sec-card" style={style} onClick={() => onSelect(i)}>
            <strong style={{ color: 'var(--primary)', marginRight: '0.5rem' }}>{KEYS[i]}.</strong>{opt}
          </button>
        );
      })}
    </div>
  );
}
