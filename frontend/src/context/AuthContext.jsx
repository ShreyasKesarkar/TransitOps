import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { fetchCurrentUser, login as loginRequest, logout as logoutRequest } from '../services/authService';
import { decodeJwtPayload, normalizeAuthUser } from '../services/normalizers';

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
        if (parsed.user) {
          setUser(parsed.user);
        } else if (parsed.token) {
          const payload = decodeJwtPayload(parsed.token);
          setUser(normalizeAuthUser(
            {
              user_id: payload?.sub ? Number(payload.sub) : null,
              organization_id: payload?.organization_id ?? null,
              role_id: payload?.role_id ?? null,
              full_name: payload?.full_name ?? null,
              email: payload?.email ?? '',
              must_change_password: false,
            },
            parsed.token,
          ));
        }

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
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ token: response.token }));
    const currentUser = await fetchCurrentUser(response.token);
    persistSession(response.token, currentUser);
    return currentUser;
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