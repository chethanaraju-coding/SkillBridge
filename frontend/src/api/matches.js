import { apiClient } from './client';

export const matchesApi = {
  getMatches: () => apiClient('/matches', { method: 'GET' }),
};
