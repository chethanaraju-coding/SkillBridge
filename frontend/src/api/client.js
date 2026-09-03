/**
 * Centralized API client for SkillBridge.
 * Handles baseURL, JWT authorization header injection, and consistent error extraction.
 */

const BASE_URL = import.meta.env.VITE_API_URL || '/api';

export async function apiClient(endpoint, { body, ...customConfig } = {}) {
  const token = localStorage.getItem('skillbridge_token');

  const headers = {
    'Content-Type': 'application/json',
    ...(customConfig.headers || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    method: body ? 'POST' : 'GET',
    ...customConfig,
    headers,
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  // Construct URL cleanly
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const url = `${BASE_URL}${cleanEndpoint}`;

  try {
    const response = await fetch(url, config);
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      // Auto-logout on token expiration / unauthorized
      if (response.status === 401) {
        // If expired, clear stored token
        if (token && (data.error?.includes('expired') || data.error?.includes('Invalid authentication token'))) {
          localStorage.removeItem('skillbridge_token');
          localStorage.removeItem('skillbridge_user');
          window.dispatchEvent(new Event('skillbridge_auth_change'));
        }
      }

      const errorMsg = data.error || data.message || `Request failed with status ${response.status}`;
      const err = new Error(errorMsg);
      err.status = response.status;
      err.data = data;
      throw err;
    }

    return data;
  } catch (error) {
    if (error.status) throw error;
    // Network error / connection refused
    throw new Error('Unable to connect to SkillBridge server. Please ensure the backend is running.');
  }
}
