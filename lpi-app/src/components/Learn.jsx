import { useRef, useCallback } from 'react';
import { useApp } from '../context/AppContext';
import { useTTS } from '../hooks/useTTS';
import TopicPills from './TopicPills';
import DATA from '../data/questions.json';
import { esc, formatLesson } from '../utils/helpers';

export default function Learn() {
  const { state, save } = useApp();

  if (state.currentSection) return <SectionLearn state={state} save={save} />;

  return (
    <>
      <TopicPills />
      <div className="grid">
        {Object.entries(DATA).filter(([, sec]) => !state.topicFilter || sec.topic_num === state.topicFilter).map(([id, sec]) => {
          const m = state.mastery[id] || { level: 0 };
          const colors = ['var(--card)', 'var(--amber-light)', 'var(--primary-light)', 'var(--green-light)'];
          return (
            <div key={id} className="sec-card" onClick={() => save(s => ({ ...s, currentSection: id }))}>
              <div className="icon" style={{ background: colors[m.level] }}>📖</div>
              <div className="info"><h3>{sec.title}</h3><div className="meta">Topic {sec.topic_num}: {sec.topic}</div></div>
            </div>
          );
        })}
      </div>
    </>
  );
}

function SectionLearn({ state, save }) {
  const sec = DATA[state.currentSection];
  const tab = state.sectionTab || 'lesson';
  const lessonRef = useRef(null);
  const tts = useTTS();

  const highlightChunk = useCallback((idx) => {
    const el = lessonRef.current;
    if (!el) return;
    el.querySelectorAll('[data-chunk]').forEach(s => s.classList.remove('tts-highlight'));
    const span = el.querySelector(`[data-chunk="${idx}"]`);
    if (span) { span.classList.add('tts-highlight'); span.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  }, []);

  const toggleTTS = useCallback(() => {
    if (tts.isPlaying) { tts.stop(); clearHighlights(); return; }
    const el = lessonRef.current;
    if (!el) return;
    const text = el.textContent.substring(0, 5000).trim();
    if (!text) return;
    tts.speak(text, highlightChunk);
  }, [tts, highlightChunk]);

  function clearHighlights() {
    const el = lessonRef.current;
    if (el) el.querySelectorAll('.tts-highlight').forEach(s => s.classList.remove('tts-highlight'));
  }

  return (
    <>
      <button className="back-btn" onClick={() => { tts.stop(); save(s => ({ ...s, currentSection: null })); }}>← Back</button>
      {tts.serverAvailable === false && (
        <div style={{ background: 'var(--amber-light)', border: '1px solid var(--amber)', borderRadius: '8px', padding: '0.5rem 0.8rem', marginBottom: '0.8rem', fontSize: '0.78rem', color: 'var(--amber)' }}>
          🔊 For best audio: <code style={{ fontSize: '0.72rem' }}>docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi</code>
        </div>
      )}
      <div className="panel">
        <h2>{state.currentSection} — {sec.title}</h2>
        <div className="tabs">
          {['lesson', 'concepts', 'commands'].map(t => (
            <button key={t} className={tab === t ? 'active' : ''} onClick={() => save(s => ({ ...s, sectionTab: t }))}>{t.charAt(0).toUpperCase() + t.slice(1)}</button>
          ))}
        </div>
        {tab === 'lesson' && (
          <>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
              <button className="btn btn-outline btn-sm" onClick={toggleTTS}>
                {tts.isPlaying ? '⏹️ Stop' : '🔊 Read Aloud'}
              </button>
              {tts.isPlaying && (
                <input type="range" min="0" max="100" value={Math.round(tts.progress * 100)} style={{ flex: 1, minWidth: '80px', accentColor: 'var(--primary)' }} onChange={e => tts.seek(parseInt(e.target.value) / 100)} />
              )}
              {tts.voices.length > 0 && (
                <select value={tts.voice} onChange={e => tts.setVoice(e.target.value)} style={{ fontSize: '0.75rem', padding: '0.3rem', borderRadius: '6px', border: '1px solid var(--border)', background: 'var(--surface)', color: 'var(--text)' }}>
                  {tts.voices.map(v => <option key={typeof v === 'string' ? v : v.id} value={typeof v === 'string' ? v : v.id}>{typeof v === 'string' ? v : v.name || v.id}</option>)}
                </select>
              )}
              <select value={tts.speed} onChange={e => tts.setSpeed(parseFloat(e.target.value))} style={{ fontSize: '0.75rem', padding: '0.3rem', borderRadius: '6px', border: '1px solid var(--border)', background: 'var(--surface)', color: 'var(--text)' }}>
                <option value="0.5">0.5×</option>
                <option value="0.75">0.75×</option>
                <option value="1">1×</option>
                <option value="1.25">1.25×</option>
                <option value="1.5">1.5×</option>
                <option value="2">2×</option>
              </select>
            </div>
            <div className="lesson-text" ref={lessonRef} dangerouslySetInnerHTML={{ __html: formatLesson(sec.full_lesson || sec.lesson_excerpt) }} />
          </>
        )}
        {tab === 'concepts' && (
          sec.concepts.filter(c => c.term.length > 3 && c.term.length < 35 && !/^(There|This|But|On|The|It|A |An )/i.test(c.term)).length === 0
            ? <p style={{ color: 'var(--muted)' }}>See lesson text for concepts.</p>
            : sec.concepts.filter(c => c.term.length > 3 && c.term.length < 35 && !/^(There|This|But|On|The|It|A |An )/i.test(c.term)).map((c, i) => (
              <div key={i} style={{ background: 'var(--card)', padding: '0.8rem 1rem', borderRadius: '8px', marginBottom: '0.5rem', borderLeft: '3px solid var(--primary)' }}>
                <strong style={{ color: 'var(--primary)' }}>{esc(c.term)}</strong>
                <p style={{ fontSize: '0.84rem', marginTop: '0.2rem', color: 'var(--muted)' }}>{esc(c.definition)}</p>
              </div>
            ))
        )}
        {tab === 'commands' && (
          !sec.commands.length
            ? <p style={{ color: 'var(--muted)' }}>No commands in this section.</p>
            : sec.commands.map((cmd, i) => (
              <div key={i} style={{ background: '#1e1e2e', padding: '0.6rem 1rem', borderRadius: '8px', marginBottom: '0.4rem', fontFamily: 'monospace' }}>
                <code style={{ color: '#a6e3a1' }}>$ {esc(cmd.command)}</code>
                <p style={{ fontSize: '0.78rem', color: '#a6adc8', marginTop: '0.2rem' }}>{esc(cmd.context)}</p>
              </div>
            ))
        )}
      </div>
    </>
  );
}
