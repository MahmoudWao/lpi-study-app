const STORAGE_KEY = 'lpi_brilliant_v2';

export function defaultState() {
  return {
    version: 2, mode: 'practice', topicFilter: null, currentSection: null,
    sectionTab: 'lesson', cards: {}, streak: 0, lastStudyDate: null,
    totalReviews: 0, mastery: {}, fcIdx: 0, fcFlipped: false, fcFilter: 'due'
  };
}

export function loadState() {
  try {
    const s = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (s && s.version === 2) return s;
  } catch (e) {}
  return defaultState();
}

export function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

export function loadTermProgress() {
  return JSON.parse(localStorage.getItem('lpi_term_progress') || '{}');
}

export function saveTermProgress(progress) {
  localStorage.setItem('lpi_term_progress', JSON.stringify(progress));
}
