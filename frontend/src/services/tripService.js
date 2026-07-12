import apiClient from './apiClient';
import { normalizeTrip, serializeTrip, serializeTripUpdate } from './normalizers';
import { driverService } from './driverService';
import { userService } from './userService';
import { vehicleService } from './vehicleService';

async function getSupportingMaps() {
  const [driversResponse, usersResponse, vehiclesResponse] = await Promise.all([
    driverService.list(),
    userService.list(),
    vehicleService.list(),
  ]);

  const driversById = Object.fromEntries((driversResponse.items || []).map((item) => [item.driverId, item]));
  const usersById = Object.fromEntries((usersResponse.items || []).map((item) => [item.userId, item]));
  const vehiclesById = Object.fromEntries((vehiclesResponse.items || []).map((item) => [item.vehicleId, item]));

  return { driversById, usersById, vehiclesById };
}

export const tripService = {
  async list(params = {}) {
    const [tripsResponse, maps] = await Promise.all([
      apiClient.get('/trips', { params }),
      getSupportingMaps(),
    ]);
    const items = tripsResponse.data.map((trip) => normalizeTrip(trip, maps.driversById, maps.vehiclesById, maps.usersById));
    return { items, total: items.length };
  },
  async get(id) {
    const [tripResponse, maps] = await Promise.all([apiClient.get(`/trips/${id}`), getSupportingMaps()]);
    return normalizeTrip(tripResponse.data, maps.driversById, maps.vehiclesById, maps.usersById);
  },
  async create(payload, context = {}) {
    const { data } = await apiClient.post('/trips', serializeTrip(payload, context.organizationId));
    const maps = await getSupportingMaps();
    return normalizeTrip(data, maps.driversById, maps.vehiclesById, maps.usersById);
  },
  async update(id, payload) {
    const { data } = await apiClient.patch(`/trips/${id}`, serializeTripUpdate(payload));
    const maps = await getSupportingMaps();
    return normalizeTrip(data, maps.driversById, maps.vehiclesById, maps.usersById);
  },
  async remove(id) {
    await apiClient.delete(`/trips/${id}`);
    return true;
  },
};