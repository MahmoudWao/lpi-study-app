import { shuffleArray } from './helpers';
import DATA from '../data/questions.json';

export function buildAllCards() {
  const cards = [];
  for (const [secId, sec] of Object.entries(DATA)) {
    sec.qa_pairs.forEach((qa, i) => {
      const q = qa.question, a = qa.answer;
      if (q.length > 200 || a.length < 10 || a.endsWith('...')) return;
      if (/name (two|three|four|five|\d+)/i.test(q)) return;
      if (/list (two|three|four|five|\d+)/i.test(q)) return;
      if ((q.match(/\?/g) || []).length > 1) return;
      if (/\n.*\d+\./m.test(q)) return;
      cards.push({ id: `${secId}::qa::${i}`, type: 'question', section: secId, topic: sec.topic_num, difficulty: qa.difficulty, front: q.substring(0, 200), back: a.substring(0, 300), sectionTitle: sec.title });
    });
    sec.commands.forEach((cmd, i) => {
      if (cmd.command.length > 3 && cmd.command.length < 60 && cmd.context.length > 8 && cmd.context.length < 120) {
        let ctx = cmd.context.trim().replace(/^[\(\)\[\]:;,.\s]+|[\(\):;,\s]+$/g, '').trim();
        ctx = ctx.charAt(0).toUpperCase() + ctx.slice(1);
        if (!ctx.endsWith('.')) ctx += '.';
        if (/^(Is |Are |Was |Were |Has |Have |Had |Can |Will |Does |Did |Creates? |Contains? )/.test(ctx)) return;
        if (ctx.length < 15) return;
        cards.push({ id: `${secId}::cmd::${i}`, type: 'command', section: secId, topic: sec.topic_num, difficulty: 'intermediate', front: `$ ${cmd.command}`, back: ctx, sectionTitle: sec.title });
        cards.push({ id: `${secId}::cmdR::${i}`, type: 'reverse', section: secId, topic: sec.topic_num, difficulty: 'intermediate', front: ctx, back: `$ ${cmd.command}`, sectionTitle: sec.title });
      }
    });
    sec.concepts.forEach((c, i) => {
      if (c.term.length > 3 && c.term.length < 60 && !/^(There|This|But|On|The|It|A |An )/i.test(c.term)) {
        if (c.definition.length < 10) return;
        cards.push({ id: `${secId}::concept::${i}`, type: 'concept', section: secId, topic: sec.topic_num, difficulty: 'basic', front: c.term, back: c.definition, sectionTitle: sec.title });
        cards.push({ id: `${secId}::conceptR::${i}`, type: 'reverse', section: secId, topic: sec.topic_num, difficulty: 'basic', front: c.definition.substring(0, 150), back: c.term, sectionTitle: sec.title });
      }
    });
  }
  return shuffleArray(cards);
}
