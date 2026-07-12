import api from './api';

export const getMaintenance = async () => {
  const response = await api.get('/maintenance');
  return response.data;
};
