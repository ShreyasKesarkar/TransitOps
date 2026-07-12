import { createCrudService } from './createCrudService';
import { maintenanceRequests } from '../data/mockData';

export const maintenanceService = createCrudService({
  basePath: '/maintenance',
  fallbackData: maintenanceRequests,
  idKey: 'id',
  codePrefix: 'MNT',
});