import { createCrudService } from './createCrudService';
import { fuelLogs } from '../data/mockData';

export const fuelService = createCrudService({
  basePath: '/fuel-logs',
  fallbackData: fuelLogs,
  idKey: 'id',
  codePrefix: 'FUEL',
});