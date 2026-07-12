import apiClient from './apiClient';
import { dashboardSummary } from '../data/mockData';

export async function fetchDashboardSummary() {
  try {
    const { data } = await apiClient.get('/dashboard/summary');
    return data;
  } catch {
    return dashboardSummary;
  }
}