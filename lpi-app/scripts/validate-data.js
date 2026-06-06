import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA = JSON.parse(readFileSync(join(__dirname, '../src/data/questions.json'), 'utf8'));

let errors = 0;
const seenQ = new Set();

for (const [secId, sec] of Object.entries(DATA)) {
  if (!sec.title || !sec.topic_num) { console.error(`ERROR: ${secId} missing title or topic_num`); errors++; }

  sec.qa_pairs.forEach((qa, i) => {
    if (!qa.question || qa.question.trim().length < 5) { console.error(`ERROR: ${secId}::qa::${i} empty/short question`); errors++; }
    if (!qa.answer || qa.answer.trim().length === 0) { console.error(`ERROR: ${secId}::qa::${i} empty answer`); errors++; }

    const norm = qa.question.toLowerCase().replace(/\s+/g, ' ').trim();
    if (seenQ.has(norm)) { console.warn(`WARN: duplicate question in ${secId}::qa::${i}`); }
    seenQ.add(norm);
  });

  sec.concepts.forEach((c, i) => {
    if (!c.term || !c.definition) { console.error(`ERROR: ${secId}::concept::${i} missing term/definition`); errors++; }
  });
}

if (errors > 0) {
  console.error(`\nValidation FAILED: ${errors} error(s) found`);
  process.exit(1);
} else {
  console.log(`✓ Validation passed: ${Object.keys(DATA).length} sections, ${Object.values(DATA).reduce((s, sec) => s + sec.qa_pairs.length, 0)} Q&A pairs`);
}
