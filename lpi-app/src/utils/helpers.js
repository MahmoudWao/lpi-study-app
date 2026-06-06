export function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

export function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export function stripQuestion(answer, question) {
  const qFirst50 = question.substring(0, 50).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const idx = answer.search(new RegExp(qFirst50.substring(0, 30)));
  if (idx >= 0) {
    const nlIdx = answer.indexOf('\n', idx + question.length - 10);
    if (nlIdx > 0) return answer.substring(nlIdx + 1).trim();
  }
  return answer;
}

export function formatLesson(raw) {
  let text = esc(raw);
  let paras = text.split(/\n{2,}/);
  let html = '';
  let chunkId = 0;
  paras.forEach(p => {
    p = p.trim();
    if (!p) return;
    if (/^(Introduction|Summary|Guided Exercises|Explorational Exercises)$/.test(p)) {
      html += `<h3 style="color:var(--primary);font-size:1rem;margin:1.5rem 0 0.5rem;font-family:-apple-system,sans-serif">${p}</h3>`;
      return;
    }
    if (/^\$ /.test(p)) {
      html += `<pre style="background:var(--card);padding:0.8rem 1rem;border-radius:8px;font-family:monospace;font-size:0.85rem;overflow-x:auto;margin:0.8rem 0;border:1px solid var(--border)">${p}</pre>`;
      return;
    }
    if (/^[\u2022\u25E6]/.test(p)) {
      const items = p.split(/\n/).map(l => l.replace(/^[\u2022\u25E6]\s*/, '').trim()).filter(Boolean);
      html += `<ul style="margin:0.8rem 0 0.8rem 1.2rem">${items.map(i => `<li style="margin-bottom:0.3rem">${i}</li>`).join('')}</ul>`;
      return;
    }
    const joined = p.replace(/\n/g, ' ').replace(/\s{2,}/g, ' ');
    const sentences = joined.match(/.{1,200}(?:[.!?]\s|$)|.{1,200}(?:\s|$)/g) || [joined];
    const spans = sentences.map(s => `<span data-chunk="${chunkId++}">${s}</span>`).join('');
    html += `<p style="margin-bottom:1rem">${spans}</p>`;
  });
  return html;
}

export const TOPICS = {
  '1': 'The Linux Community & Open Source',
  '2': 'Finding Your Way on Linux',
  '3': 'The Power of the Command Line',
  '4': 'The Linux Operating System',
  '5': 'Security & File Permissions'
};

export const ENCOURAGEMENTS = [
  { big: '🎯', h: 'Nailed it!', p: 'You\'re building real understanding.' },
  { big: '🧠', h: 'Great recall!', p: 'That knowledge is sticking.' },
  { big: '⚡', h: 'Quick thinking!', p: 'Your Linux skills are growing.' },
  { big: '🚀', h: 'On fire!', p: 'Keep this momentum going.' },
  { big: '💪', h: 'Solid work!', p: 'Every answer strengthens your knowledge.' },
];
