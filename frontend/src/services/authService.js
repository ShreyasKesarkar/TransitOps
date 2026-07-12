import apiClient from './apiClient';
import { mockAuthUser } from '../data/mockData';

export async function login(credentials) {
  try {
    const { data } = await apiClient.post('/auth/login', credentials);
    return data;
  } catch {
    return {
      token: 'mock-jwt-token',
      user: mockAuthUser,
    };
  }
}

export async function fetchCurrentUser() {
  try {
    const { data } = await apiClient.get('/auth/me');
    return data;
  } catch {
    return mockAuthUser;
  }
}

export async function logout() {
  try {
    await apiClient.post('/auth/logout');
  } catch {
    return true;
  }
  return true;
}

export async function requestPasswordReset(payload) {
  try {
    const { data } = await apiClient.post('/auth/forgot-password', payload);
    return data;
  } catch {
    return { message: 'Password reset link queued in mock mode.' };
  }
}

export async function changePassword(payload) {
  try {
    const { data } = await apiClient.post('/auth/change-password', payload);
    return data;
  } catch {
    return { message: 'Password changed in mock mode.' };
  }
}