import { apiClient } from './client';

export const sessionsApi = {
  getSessions: (params = {}) => {
    const query = new URLSearchParams();
    if (params.status) query.append('status', params.status);
    if (params.role) query.append('role', params.role);
    const queryString = query.toString();
    return apiClient(`/sessions${queryString ? `?${queryString}` : ''}`, { method: 'GET' });
  },
  getSession: (id) => apiClient(`/sessions/${id}`, { method: 'GET' }),
  createSession: (data) => apiClient('/sessions', { body: data, method: 'POST' }),
  updateSession: (id, data) => apiClient(`/sessions/${id}`, { body: data, method: 'PUT' }),
};
