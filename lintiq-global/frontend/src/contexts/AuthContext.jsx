/**
 * Authentication Context for LintIQ
 * Manages user authentication state and operations
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import { auth, setAuthToken, setUser, getUser, clearAuth } from '../lib/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUserState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Initialize auth state on mount
  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = async () => {
    try {
      const storedUser = getUser();
      if (storedUser) {
        // Verify token is still valid
        const response = await auth.verify();
        if (response.data.success) {
          setUserState(response.data.user);
          setIsAuthenticated(true);
        } else {
          clearAuth();
        }
      }
    } catch (error) {
      console.error('Auth initialization failed:', error);
      clearAuth();
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    try {
      setLoading(true);
      const response = await auth.login(credentials);
      
      if (response.data.success) {
        const { user: userData, token } = response.data;
        
        setAuthToken(token);
        setUser(userData);
        setUserState(userData);
        setIsAuthenticated(true);
        
        return { success: true, user: userData };
      } else {
        return { success: false, error: response.data.error };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Login failed';
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      const response = await auth.register(userData);
      
      if (response.data.success) {
        const { user: newUser, token } = response.data;
        
        setAuthToken(token);
        setUser(newUser);
        setUserState(newUser);
        setIsAuthenticated(true);
        
        return { success: true, user: newUser };
      } else {
        return { success: false, error: response.data.error };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Registration failed';
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const demoLogin = async () => {
    try {
      setLoading(true);
      const response = await auth.demoLogin();
      
      if (response.data.success) {
        const { user: demoUser, token } = response.data;
        
        setAuthToken(token);
        setUser(demoUser);
        setUserState(demoUser);
        setIsAuthenticated(true);
        
        return { success: true, user: demoUser };
      } else {
        return { success: false, error: response.data.error };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Demo login failed';
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await auth.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      clearAuth();
      setUserState(null);
      setIsAuthenticated(false);
    }
  };

  const updateUser = (updatedUser) => {
    setUser(updatedUser);
    setUserState(updatedUser);
  };

  const refreshUser = async () => {
    try {
      const response = await auth.verify();
      if (response.data.success) {
        const updatedUser = response.data.user;
        setUser(updatedUser);
        setUserState(updatedUser);
        return updatedUser;
      }
    } catch (error) {
      console.error('Failed to refresh user:', error);
    }
    return user;
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    demoLogin,
    logout,
    updateUser,
    refreshUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

