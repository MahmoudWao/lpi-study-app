import { readFileSync, writeFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const reportPath = join(__dirname, '../qa-audit-report.json');

if (!existsSync(reportPath)) {
  console.error('Run audit-qa.js first to generate qa-audit-report.json');
  process.exit(1);
}

const report = JSON.parse(readFileSync(reportPath, 'utf8'));
const DATA = JSON.parse(readFileSync(join(__dirname, '../src/data/questions.json'), 'utf8'));

function esc(s) { return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

let html = `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QA Audit Review</title>
<style>
body{font-family:system-ui;max-width:900px;margin:0 auto;padding:2rem;background:#f8fafc;color:#1e293b}
h1{color:#6366f1}
.summary{display:flex;gap:1rem;margin:1rem 0}
.badge{padding:0.5rem 1rem;border-radius:8px;font-weight:600;font-size:0.85rem}
.high{background:#fee2e2;color:#dc2626}
.medium{background:#fef3c7;color:#d97706}
.low{background:#e0e7ff;color:#4f46e5}
.issue{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.2rem;margin:0.8rem 0}
.issue-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem}
.type{font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;color:#64748b}
.question{font-weight:500;margin:0.5rem 0}
.answer{background:#f1f5f9;padding:0.8rem;border-radius:8px;font-size:0.85rem;white-space:pre-wrap;max-height:200px;overflow-y:auto}
.actions{display:flex;gap:0.5rem;margin-top:0.8rem}
.actions button{padding:0.4rem 0.8rem;border-radius:6px;border:1px solid #e2e8f0;cursor:pointer;font-size:0.8rem}
.actions .fix{background:#d1fae5;border-color:#10b981}
.actions .edit{background:#fef3c7;border-color:#f59e0b}
.actions .del{background:#fee2e2;border-color:#ef4444}
.done{opacity:0.4}
</style></head><body>
<h1>📋 QA Audit Review</h1>
<p>Generated: ${report.generated} · ${report.totalIssues} issues in ${report.totalQuestions} questions</p>
<div class="summary">
<span class="badge high">${report.bySeverity.high} High</span>
<span class="badge medium">${report.bySeverity.medium} Medium</span>
<span class="badge low">${report.bySeverity.low} Low</span>
</div>`;

report.issues.forEach((issue, i) => {
  const secData = DATA[issue.section];
  const qaIdx = parseInt(issue.id.split('::')[2]);
  const qa = secData?.qa_pairs[qaIdx];
  html += `<div class="issue" id="issue-${i}">
<div class="issue-header"><span class="badge ${issue.severity}">${issue.severity}</span><span class="type">${issue.type}</span></div>
<div style="font-size:0.75rem;color:#64748b">Section: ${issue.section} · ${issue.id}</div>
<p class="question">${esc(issue.question || qa?.question?.substring(0, 150))}</p>
${qa ? `<div class="answer">${esc(qa.answer.substring(0, 500))}</div>` : ''}
<div class="actions">
<button class="fix" onclick="mark(${i},'fixed')">✓ Fixed</button>
<button class="edit" onclick="mark(${i},'needs_edit')">✏️ Needs Edit</button>
<button class="del" onclick="mark(${i},'delete')">🗑️ Delete</button>
</div></div>`;
});

html += `<script>
const decisions={};
function mark(i,action){decisions[i]=action;document.getElementById('issue-'+i).classList.add('done');
document.getElementById('issue-'+i).querySelector('.actions').innerHTML='<em>'+action+'</em>';
console.log('Decisions:',JSON.stringify(decisions));}
</script></body></html>`;

writeFileSync(join(__dirname, '../qa-review.html'), html);
console.log(`Review page written to qa-review.html (${report.issues.length} issues)`);
