import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 15000,
  withCredentials: true,
});

apiClient.interceptors.request.use((config) => {
  const session = localStorage.getItem('transitops.auth');
  if (session) {
    const parsed = JSON.parse(session);
    if (parsed?.token) {
      config.headers.Authorization = `Bearer ${parsed.token}`;
    }
  }
  return config;
});

export default apiClient;