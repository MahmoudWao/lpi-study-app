import { useEffect, useCallback } from 'react';

/**
 * useKeyboard - subscribe to keyboard shortcuts.
 * @param {Object} bindings - map of key to handler function
 * @param {boolean} active - whether shortcuts are active (false when typing in terminal)
 */
export function useKeyboard(bindings, active = true) {
  const handler = useCallback((e) => {
    if (!active) return;
    // Don't fire when typing in inputs/textareas
    const tag = e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA') return;

    const key = e.key;
    if (bindings[key]) {
      e.preventDefault();
      bindings[key](e);
    }
  }, [bindings, active]);

  useEffect(() => {
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [handler]);
}
