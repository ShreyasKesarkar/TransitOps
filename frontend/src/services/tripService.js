import { createCrudService } from './createCrudService';
import { trips } from '../data/mockData';

export const tripService = createCrudService({
  basePath: '/trips',
  fallbackData: trips,
  idKey: 'id',
  codePrefix: 'TRP',
});