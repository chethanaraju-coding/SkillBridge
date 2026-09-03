import { apiClient } from './client';

export const skillsApi = {
  getSkills: (params = {}) => {
    const query = new URLSearchParams();
    if (params.search || params.q) query.append('search', params.search || params.q);
    if (params.type) query.append('type', params.type);
    if (params.user_id) query.append('user_id', params.user_id);
    const queryString = query.toString();
    return apiClient(`/skills${queryString ? `?${queryString}` : ''}`, { method: 'GET' });
  },
  getSkill: (id) => apiClient(`/skills/${id}`, { method: 'GET' }),
  createSkill: (data) => apiClient('/skills', { body: data, method: 'POST' }),
  updateSkill: (id, data) => apiClient(`/skills/${id}`, { body: data, method: 'PUT' }),
  deleteSkill: (id) => apiClient(`/skills/${id}`, { method: 'DELETE' }),
};
