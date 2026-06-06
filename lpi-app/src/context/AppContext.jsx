import { createContext, useContext } from 'react';
import { useAppState } from '../hooks/useAppState';

const AppContext = createContext();

export function AppProvider({ children }) {
  const appState = useAppState();
  return <AppContext.Provider value={appState}>{children}</AppContext.Provider>;
}

export function useApp() { return useContext(AppContext); }
