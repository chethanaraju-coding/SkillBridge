import { apiClient } from './client';

export const authApi = {
  register: (data) => apiClient('/auth/register', { body: data, method: 'POST' }),
  login: (data) => apiClient('/auth/login', { body: data, method: 'POST' }),
  getMe: () => apiClient('/auth/me', { method: 'GET' }),
};
