import { createCrudService } from './createCrudService';
import { drivers } from '../data/mockData';

export const driverService = createCrudService({
  basePath: '/drivers',
  fallbackData: drivers,
  idKey: 'id',
  codePrefix: 'DRV',
});