import api from './api';

export const getVehicles = async () => {
  const response = await api.get('/vehicles');
  return response.data;
};
