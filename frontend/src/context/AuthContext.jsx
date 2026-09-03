import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '../api/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('skillbridge_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState(() => localStorage.getItem('skillbridge_token'));
  const [loading, setLoading] = useState(true);

  // Validate session on initial load
  useEffect(() => {
    async function verifyUser() {
      if (token) {
        try {
          const res = await authApi.getMe();
          if (res && res.user) {
            setUser(res.user);
            localStorage.setItem('skillbridge_user', JSON.stringify(res.user));
          }
        } catch (err) {
          // Token invalid or expired
          logout();
        }
      }
      setLoading(false);
    }

    verifyUser();

    // Listen for cross-tab or client logout triggers
    const handleAuthChange = () => {
      setToken(localStorage.getItem('skillbridge_token'));
      const savedUser = localStorage.getItem('skillbridge_user');
      setUser(savedUser ? JSON.parse(savedUser) : null);
    };

    window.addEventListener('skillbridge_auth_change', handleAuthChange);
    return () => window.removeEventListener('skillbridge_auth_change', handleAuthChange);
  }, [token]);

  const login = async (email, password) => {
    const res = await authApi.login({ email, password });
    if (res.token && res.user) {
      localStorage.setItem('skillbridge_token', res.token);
      localStorage.setItem('skillbridge_user', JSON.stringify(res.user));
      setToken(res.token);
      setUser(res.user);
    }
    return res;
  };

  const register = async (name, email, password) => {
    const res = await authApi.register({ name, email, password });
    if (res.token && res.user) {
      localStorage.setItem('skillbridge_token', res.token);
      localStorage.setItem('skillbridge_user', JSON.stringify(res.user));
      setToken(res.token);
      setUser(res.user);
    }
    return res;
  };

  const logout = () => {
    localStorage.removeItem('skillbridge_token');
    localStorage.removeItem('skillbridge_user');
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    loading,
    isAuthenticated: !!token && !!user,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
