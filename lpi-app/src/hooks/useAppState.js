import { useState, useCallback, useRef, useMemo } from 'react';
import { loadState, saveState } from '../utils/storage';
import { gradeCard, getCardState, isDue } from '../utils/sm2';
import { buildAllCards } from '../utils/cards';

export function useAppState() {
  const [state, setState] = useState(loadState);
  const allCards = useMemo(() => buildAllCards(), []);
  const save = useCallback((updater) => {
    setState(prev => {
      const next = typeof updater === 'function' ? updater(prev) : { ...prev, ...updater };
      saveState(next);
      return next;
    });
  }, []);

  const updateStreak = useCallback(() => {
    setState(prev => {
      const today = new Date().toDateString();
      if (prev.lastStudyDate === today) return prev;
      const yesterday = new Date(Date.now() - 86400000).toDateString();
      const streak = (prev.lastStudyDate === yesterday) ? prev.streak + 1 : 1;
      const next = { ...prev, streak, lastStudyDate: today };
      saveState(next);
      return next;
    });
  }, []);

  const grade = useCallback((cardId, gradeVal) => {
    setState(prev => {
      const cards = { ...prev.cards };
      const c = getCardState(cards, cardId);
      gradeCard(c, gradeVal);
      cards[cardId] = c;
      const secId = cardId.split('::')[0];
      const mastery = { ...prev.mastery };
      if (!mastery[secId]) mastery[secId] = { seen: 0, correct: 0, total: 0, level: 0 };
      mastery[secId] = { ...mastery[secId], seen: mastery[secId].seen + 1, total: mastery[secId].total + 1 };
      if (gradeVal >= 2) mastery[secId].correct = mastery[secId].correct + 1;
      mastery[secId].level = Math.min(3, Math.floor((mastery[secId].correct / Math.max(1, mastery[secId].total)) * 4));
      const next = { ...prev, cards, mastery, totalReviews: prev.totalReviews + 1 };
      saveState(next);
      return next;
    });
    updateStreak();
  }, [updateStreak]);

  const getDueCards = useCallback(() => allCards.filter(c => isDue(state.cards, c.id)), [allCards, state.cards]);
  const getCardsBySection = useCallback((secId) => allCards.filter(c => c.section === secId), [allCards]);

  return { state, save, grade, allCards, getDueCards, getCardsBySection, updateStreak };
}
