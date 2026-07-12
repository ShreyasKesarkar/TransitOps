import { createCrudService } from './createCrudService';
import { vehicles } from '../data/mockData';

export const vehicleService = createCrudService({
  basePath: '/vehicles',
  fallbackData: vehicles,
  idKey: 'id',
  codePrefix: 'VEH',
});