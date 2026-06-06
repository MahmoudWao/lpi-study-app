import { useRef, useCallback } from 'react';

export function useSwipe({ onLeft, onRight, threshold = 50 }) {
  const startX = useRef(0);

  const onTouchStart = useCallback((e) => { startX.current = e.touches[0].clientX; }, []);
  const onTouchEnd = useCallback((e) => {
    const diff = e.changedTouches[0].clientX - startX.current;
    if (diff > threshold && onRight) onRight();
    else if (diff < -threshold && onLeft) onLeft();
  }, [onLeft, onRight, threshold]);

  return { onTouchStart, onTouchEnd };
}
