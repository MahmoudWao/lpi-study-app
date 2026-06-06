export function getCardState(cards, id) {
  if (!cards[id]) cards[id] = { interval: 0, ease: 2.5, due: 0, reps: 0, lapses: 0 };
  return cards[id];
}

export function gradeCard(card, grade) {
  const now = Date.now();
  if (grade === 0) {
    card.reps = 0;
    card.interval = 1;
    card.lapses++;
    card.ease = Math.max(1.3, card.ease - 0.2);
  } else {
    if (card.reps === 0) card.interval = 1;
    else if (card.reps === 1) card.interval = 3;
    else card.interval = Math.round(card.interval * card.ease);
    card.reps++;
    card.ease += grade === 3 ? 0.15 : grade === 1 ? -0.15 : 0;
    card.ease = Math.max(1.3, card.ease);
  }
  card.due = now + card.interval * 86400000;
  return card;
}

export function isDue(cards, id) {
  const c = cards[id];
  return !c || Date.now() >= c.due;
}


export function isWeak(cardState) {
  if (!cardState) return false;
  const now = Date.now();
  if (cardState.ease < 2.0) return true;
  if (cardState.lapses >= 3) return true;
  // Overdue by more than 2x interval
  if (cardState.due > 0 && cardState.interval > 0) {
    const overdue = now - cardState.due;
    if (overdue > cardState.interval * 86400000 * 2) return true;
  }
  return false;
}

export function getWeakCards(allCards, cardStates) {
  return allCards
    .filter(c => cardStates[c.id] && isWeak(cardStates[c.id]))
    .sort((a, b) => (cardStates[a.id].ease || 2.5) - (cardStates[b.id].ease || 2.5));
}

export function getRecoveredThisWeek(cardStates) {
  const weekAgo = Date.now() - 7 * 86400000;
  return Object.values(cardStates).filter(c => c.ease >= 2.0 && c.lapses > 0 && c.due > weekAgo).length;
}
