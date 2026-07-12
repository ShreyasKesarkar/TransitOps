import apiClient from './apiClient';
import { normalizeUser, serializeUser, serializeUserUpdate } from './normalizers';

export const userService = {
  async list(params = {}) {
    const { data } = await apiClient.get('/users', { params });
    return { items: data.map(normalizeUser), total: data.length };
  },
  async get(id) {
    const { data } = await apiClient.get(`/users/${id}`);
    return normalizeUser(data);
  },
  async create(payload, context = {}) {
    const { data } = await apiClient.post('/users', serializeUser(payload, context.organizationId));
    return normalizeUser(data);
  },
  async update(id, payload) {
    const { data } = await apiClient.patch(`/users/${id}`, serializeUserUpdate(payload));
    return normalizeUser(data);
  },
  async remove(id) {
    await apiClient.delete(`/users/${id}`);
    return true;
  },
};