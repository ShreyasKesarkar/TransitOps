import { createCrudService } from './createCrudService';
import { users } from '../data/mockData';

export const userService = createCrudService({
  basePath: '/users',
  fallbackData: users,
  idKey: 'id',
  codePrefix: 'USR',
});