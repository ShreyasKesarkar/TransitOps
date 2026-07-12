import apiClient from './apiClient';
import { normalizeDriver, serializeDriver, serializeDriverUpdate } from './normalizers';
import { userService } from './userService';

async function getUsersById() {
  const response = await userService.list();
  const items = response.items || [];
  return Object.fromEntries(items.map((item) => [item.userId, item]));
}

export const driverService = {
  async list(params = {}) {
    const [driversResponse, usersById] = await Promise.all([
      apiClient.get('/drivers', { params }),
      getUsersById(),
    ]);
    const items = driversResponse.data.map((driver) => normalizeDriver(driver, usersById));
    return { items, total: items.length };
  },
  async get(id) {
    const [driverResponse, usersById] = await Promise.all([apiClient.get(`/drivers/${id}`), getUsersById()]);
    return normalizeDriver(driverResponse.data, usersById);
  },
  async create(payload) {
    const { data } = await apiClient.post('/drivers', serializeDriver(payload));
    const usersById = await getUsersById();
    return normalizeDriver(data, usersById);
  },
  async update(id, payload) {
    const { data } = await apiClient.patch(`/drivers/${id}`, serializeDriverUpdate(payload));
    const usersById = await getUsersById();
    return normalizeDriver(data, usersById);
  },
  async remove(id) {
    await apiClient.delete(`/drivers/${id}`);
    return true;
  },
};