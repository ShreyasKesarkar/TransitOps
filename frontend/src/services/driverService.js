import api from './api';

export const getDrivers = async () => {
  const response = await api.get('/drivers');
  return response.data;
};
