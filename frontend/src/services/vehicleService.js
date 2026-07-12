import apiClient from './apiClient';
import { normalizeVehicle, serializeVehicle, serializeVehicleUpdate } from './normalizers';

export const vehicleService = {
  async list(params = {}) {
    const { data } = await apiClient.get('/vehicles', { params });
    const items = data.map(normalizeVehicle);
    return { items, total: items.length };
  },
  async get(id) {
    const { data } = await apiClient.get(`/vehicles/${id}`);
    return normalizeVehicle(data);
  },
  async create(payload, context = {}) {
    const { data } = await apiClient.post('/vehicles', serializeVehicle(payload, context.organizationId));
    return normalizeVehicle(data);
  },
  async update(id, payload) {
    const { data } = await apiClient.patch(`/vehicles/${id}`, serializeVehicleUpdate(payload));
    return normalizeVehicle(data);
  },
  async remove(id) {
    await apiClient.delete(`/vehicles/${id}`);
    return true;
  },
};