"""Patch: dark mode toggle, fix duplicate hint/question text in challenge mode."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. ADD DARK MODE CSS before </style>
dark_css = """
.dark{--bg:#0f0f1a;--surface:#1a1a2e;--card:#1e293b;--primary:#818cf8;--primary-light:#312e81;--primary-dark:#a5b4fc;--green:#34d399;--green-light:#064e3b;--amber:#fbbf24;--amber-light:#78350f;--red:#f87171;--red-light:#7f1d1d;--text:#e2e8f0;--muted:#94a3b8;--light:#64748b;--border:#334155;--shadow:0 1px 3px rgba(0,0,0,0.3)}
.dark .answer{background:var(--card)}
.dark .ex-input{background:var(--bg)}
.theme-toggle{background:none;border:1px solid var(--border);border-radius:8px;padding:0.3rem 0.6rem;cursor:pointer;font-size:0.9rem;color:var(--text)}
"""
content = content.replace('</style>', dark_css + '</style>')

# 2. Add toggle button - find the header div and add button
# The header has: <div class="header"><h1>... Linux Essentials</h1>
# Add toggle between h1 and streak
old_streak = '${S.streak>0?`<div class="streak">'
toggle_btn = '<button class="theme-toggle" onclick="document.body.classList.toggle(\'dark\');localStorage.setItem(\'lpi_dark\',document.body.classList.contains(\'dark\'))">\\u{1F313}</button>${S.streak>0?`<div class="streak">'
content = content.replace(old_streak, toggle_btn, 1)

# 3. Load dark mode on startup
content = content.replace(
    'updateStreak();render();',
    "if(localStorage.getItem('lpi_dark')==='true')document.body.classList.add('dark');\nupdateStreak();render();"
)

# 4. Fix getHint - don't return same text as the question
old_hint = """function getHint(card){
  const sec=DATA[card.section];
  if(sec.explanations&&sec.explanations.length>0)return esc(sec.explanations[0].substring(0,250)+'...');
  const summary=sec.summary||'';
  return esc(summary.substring(0,200)+'...');
}"""

new_hint = """function getHint(card){
  const sec=DATA[card.section];
  const qStart=card.front.substring(0,30);
  if(sec.explanations&&sec.explanations.length>0){
    const h=sec.explanations[0];
    if(!h.includes(qStart))return esc(h.substring(0,250));
  }
  const lines=(sec.summary||sec.lesson_excerpt||'').split('\\n').filter(l=>l.trim().length>20&&!l.includes(qStart));
  return lines.length?esc(lines[0].substring(0,200)):esc('Review the lesson material for this section.');
}"""
content = content.replace(old_hint, new_hint)

# 5. Fix challenge answer: strip repeated question from displayed answer
content = content.replace(
    '<div class="answer answer-hidden" id="answerBox">${esc(card.back)}</div>',
    '<div class="answer answer-hidden" id="answerBox">${esc(stripQuestion(card.back,card.front))}</div>'
)

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
checks = [
    ('Dark mode CSS', '.dark{' in content),
    ('Theme toggle', 'theme-toggle' in content),
    ('Dark persistence', 'lpi_dark' in content),
    ('Hint fix', 'Review the lesson material' in content),
    ('Answer strip', 'stripQuestion(card.back,card.front)' in content),
]
all_ok = True
for name, ok in checks:
    if not ok: all_ok = False
    print(f"  {'OK' if ok else 'FAIL'}: {name}")
print(f"\n{'All patches applied!' if all_ok else 'SOME FAILED'}")
