import { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [dark, setDark] = useState(() => {
    const stored = localStorage.getItem('lpi_dark');
    if (stored !== null) return stored === 'true';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });
  const [oled, setOled] = useState(() => localStorage.getItem('lpi_oled') === 'true');

  useEffect(() => {
    document.body.classList.toggle('dark', dark);
    document.body.classList.toggle('oled', dark && oled);
    localStorage.setItem('lpi_dark', dark);
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', dark ? '#0f0f1a' : '#6366f1');
  }, [dark, oled]);

  useEffect(() => { localStorage.setItem('lpi_oled', oled); }, [oled]);

  // Listen for system preference changes
  useEffect(() => {
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = (e) => { if (localStorage.getItem('lpi_dark') === null) setDark(e.matches); };
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);

  return (
    <ThemeContext.Provider value={{ dark, toggle: () => setDark(d => !d), oled, toggleOled: () => setOled(o => !o) }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() { return useContext(ThemeContext); }
