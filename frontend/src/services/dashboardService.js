import apiClient from './apiClient';
import { normalizeDashboardSummary } from './normalizers';
import { tripService } from './tripService';

export async function fetchDashboardSummary() {
  const [summaryResponse, tripsResponse] = await Promise.all([
    apiClient.get('/dashboard/summary'),
    tripService.list({ limit: 5 }),
  ]);

  const normalized = normalizeDashboardSummary(summaryResponse.data);
  normalized.recentTrips = (tripsResponse.items || []).slice(0, 5).map((trip) => ({
    id: trip.id,
    tripCode: trip.tripCode,
    source: trip.source,
    destination: trip.destination,
    vehicle: trip.vehicle,
    driver: trip.driver,
    status: trip.tripStatus,
  }));

  return normalized;
}