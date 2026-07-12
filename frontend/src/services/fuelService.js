import api from './api';

export const getFuelLogs = async () => {
  const response = await api.get('/fuel');
  return response.data;
};
