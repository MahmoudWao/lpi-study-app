import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA = JSON.parse(readFileSync(join(__dirname, '../src/data/questions.json'), 'utf8'));

const issues = [];
const seenQuestions = new Map(); // question text -> section

for (const [secId, sec] of Object.entries(DATA)) {
  sec.qa_pairs.forEach((qa, i) => {
    const id = `${secId}::qa::${i}`;
    const q = qa.question.trim();
    const a = qa.answer.trim();

    // Empty or single-word answer
    if (!a || a.split(/\s+/).length <= 1) {
      issues.push({ id, section: secId, type: 'empty_answer', severity: 'high', question: q.substring(0, 100), answer: a });
    }

    // Extremely long answer
    if (a.length > 500) {
      issues.push({ id, section: secId, type: 'long_answer', severity: 'low', question: q.substring(0, 100), answerLength: a.length });
    }

    // Answer starts by repeating the question (common data issue)
    if (a.startsWith(q.substring(0, 30))) {
      issues.push({ id, section: secId, type: 'answer_repeats_question', severity: 'medium', question: q.substring(0, 100) });
    }

    // Duplicate questions
    const qNorm = q.toLowerCase().replace(/\s+/g, ' ');
    if (seenQuestions.has(qNorm)) {
      issues.push({ id, section: secId, type: 'duplicate', severity: 'medium', question: q.substring(0, 100), duplicateOf: seenQuestions.get(qNorm) });
    } else {
      seenQuestions.set(qNorm, id);
    }

    // Answer is truncated
    if (a.endsWith('...') || a.endsWith('…')) {
      issues.push({ id, section: secId, type: 'truncated_answer', severity: 'medium', question: q.substring(0, 100) });
    }

    // Command question without a command in answer
    if (/what (command|is the command)/i.test(q) && !/[a-z]/.test(a.split('\n')[0]) === false && a.length < 5) {
      issues.push({ id, section: secId, type: 'missing_command', severity: 'high', question: q.substring(0, 100), answer: a.substring(0, 50) });
    }

    // Question too short to be meaningful
    if (q.length < 10) {
      issues.push({ id, section: secId, type: 'short_question', severity: 'medium', question: q });
    }
  });
}

const report = {
  generated: new Date().toISOString(),
  totalQuestions: Object.values(DATA).reduce((s, sec) => s + sec.qa_pairs.length, 0),
  totalIssues: issues.length,
  bySeverity: {
    high: issues.filter(i => i.severity === 'high').length,
    medium: issues.filter(i => i.severity === 'medium').length,
    low: issues.filter(i => i.severity === 'low').length,
  },
  byType: issues.reduce((a, i) => { a[i.type] = (a[i.type] || 0) + 1; return a; }, {}),
  issues,
};

writeFileSync(join(__dirname, '../qa-audit-report.json'), JSON.stringify(report, null, 2));
console.log(`Audit complete: ${report.totalIssues} issues found in ${report.totalQuestions} questions`);
console.log('By severity:', JSON.stringify(report.bySeverity));
console.log('By type:', JSON.stringify(report.byType));
console.log('Report written to qa-audit-report.json');
