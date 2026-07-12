import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { fetchCurrentUser, login as loginRequest, logout as logoutRequest } from '../services/authService';

const AuthContext = createContext(null);

const STORAGE_KEY = 'transitops.auth';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const bootstrap = async () => {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (!stored) {
        setLoading(false);
        return;
      }

      try {
        const parsed = JSON.parse(stored);
        setToken(parsed.token || null);
        setUser(parsed.user || null);

        if (!parsed.user) {
          const currentUser = await fetchCurrentUser();
          setUser(currentUser);
          localStorage.setItem(STORAGE_KEY, JSON.stringify({ token: parsed.token, user: currentUser }));
        }
      } catch {
        localStorage.removeItem(STORAGE_KEY);
      } finally {
        setLoading(false);
      }
    };

    bootstrap();
  }, []);

  const persistSession = (nextToken, nextUser) => {
    setToken(nextToken);
    setUser(nextUser);
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ token: nextToken, user: nextUser }));
  };

  const login = async (credentials) => {
    const response = await loginRequest(credentials);
    persistSession(response.token, response.user);
    return response.user;
  };

  const logout = async () => {
    await logoutRequest();
    setToken(null);
    setUser(null);
    localStorage.removeItem(STORAGE_KEY);
  };

  const value = useMemo(() => ({
    user,
    token,
    loading,
    isAuthenticated: Boolean(token && user),
    login,
    logout,
    setUser: (nextUser) => {
      if (!token) {
        setUser(nextUser);
        return;
      }
      persistSession(token, nextUser);
    },
  }), [loading, token, user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}