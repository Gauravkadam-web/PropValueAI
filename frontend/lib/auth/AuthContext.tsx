'use client';

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { LoginRequest, RegisterRequest, UserProfile } from '@/types/api';
import { api, ApiError } from '@/lib/api/client';

interface AuthContextType {
  user: UserProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
}

const TOKEN_STORAGE_KEY = 'propvalueai_token';
const USER_STORAGE_KEY = 'propvalueai_user';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Initialize from storage and verify with backend
  useEffect(() => {
    async function initAuth() {
      if (typeof window === 'undefined') {
        setIsLoading(false);
        return;
      }

      const storedToken = localStorage.getItem(TOKEN_STORAGE_KEY);
      const storedUser = localStorage.getItem(USER_STORAGE_KEY);

      if (!storedToken) {
        setIsLoading(false);
        return;
      }

      setToken(storedToken);

      if (storedUser) {
        try {
          setUser(JSON.parse(storedUser));
        } catch {
          // ignore corrupted json
        }
      }

      // Verify token with backend /api/v1/auth/me
      try {
        const freshUser = await api.auth.me(storedToken);
        setUser(freshUser);
        localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(freshUser));
      } catch (err) {
        if (err instanceof ApiError && (err.status === 401 || err.status === 403)) {
          // Token expired or invalid
          localStorage.removeItem(TOKEN_STORAGE_KEY);
          localStorage.removeItem(USER_STORAGE_KEY);
          setToken(null);
          setUser(null);
        }
      } finally {
        setIsLoading(false);
      }
    }

    initAuth();
  }, []);

  const login = useCallback(async (credentials: LoginRequest) => {
    const response = await api.auth.login(credentials);
    const receivedToken = response.token;
    const receivedUser = response.user;

    setToken(receivedToken);
    setUser(receivedUser);

    if (typeof window !== 'undefined') {
      localStorage.setItem(TOKEN_STORAGE_KEY, receivedToken);
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(receivedUser));
    }
  }, []);

  const register = useCallback(async (data: RegisterRequest) => {
    await api.auth.register(data);
    // Automatically log in after registration
    await login({ email: data.email, password: data.password });
  }, [login]);

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    if (typeof window !== 'undefined') {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      localStorage.removeItem(USER_STORAGE_KEY);
    }
  }, []);

  const isAuthenticated = !!token && !!user;
  const isAdmin = user?.role === 'ROLE_ADMIN';

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated,
        isAdmin,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
