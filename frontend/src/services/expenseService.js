import { createCrudService } from './createCrudService';
import { expenses } from '../data/mockData';

export const expenseService = createCrudService({
  basePath: '/expenses',
  fallbackData: expenses,
  idKey: 'id',
  codePrefix: 'EXP',
});