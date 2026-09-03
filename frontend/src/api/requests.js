import { apiClient } from './client';

export const requestsApi = {
  getRequests: (params = {}) => {
    const query = new URLSearchParams();
    if (params.type) query.append('type', params.type);
    if (params.status) query.append('status', params.status);
    const queryString = query.toString();
    return apiClient(`/requests${queryString ? `?${queryString}` : ''}`, { method: 'GET' });
  },
  createRequest: (data) => apiClient('/requests', { body: data, method: 'POST' }),
  updateRequestStatus: (id, status) => apiClient(`/requests/${id}`, { body: { status }, method: 'PUT' }),
};
