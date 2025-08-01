/**
 * API client for LintIQ backend communication
 * Handles authentication and API requests
 */

import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('lintiq_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('lintiq_token');
      localStorage.removeItem('lintiq_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const auth = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  demoLogin: () => api.post('/auth/demo'),
  verify: () => api.post('/auth/verify'),
  logout: () => api.post('/auth/logout'),
};

// Payment API
export const payments = {
  getPackages: () => api.get('/payments/packages'),
  createPayment: (packageId) => api.post('/payments/create-payment', { package_id: packageId }),
  verifyPayment: (token, packageId) => api.post('/payments/verify-payment', { token, package_id: packageId }),
  simulatePurchase: (packageId) => api.post('/payments/simulate-purchase', { package_id: packageId }),
  getHistory: () => api.get('/payments/history'),
};

// Analysis API
export const analysis = {
  getCapabilities: () => api.get('/analysis/capabilities'),
  analyzeFiles: (formData) => api.post('/analysis/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  getHistory: () => api.get('/analysis/history'),
  demoAnalysis: () => api.post('/analysis/demo'),
};

// User API
export const user = {
  getProfile: () => api.get('/user/profile'),
  updateProfile: (userData) => api.put('/user/profile', userData),
  getStats: () => api.get('/user/stats'),
};

// Utility functions
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('lintiq_token', token);
  } else {
    localStorage.removeItem('lintiq_token');
  }
};

export const getAuthToken = () => {
  return localStorage.getItem('lintiq_token');
};

export const setUser = (user) => {
  if (user) {
    localStorage.setItem('lintiq_user', JSON.stringify(user));
  } else {
    localStorage.removeItem('lintiq_user');
  }
};

export const getUser = () => {
  const user = localStorage.getItem('lintiq_user');
  return user ? JSON.parse(user) : null;
};

export const clearAuth = () => {
  localStorage.removeItem('lintiq_token');
  localStorage.removeItem('lintiq_user');
};

export default api;

