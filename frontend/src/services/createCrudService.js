import apiClient from './apiClient';

function cloneRows(rows) {
  return rows.map((row) => ({ ...row }));
}

function createId(prefix) {
  return `${prefix}-${Math.random().toString(36).slice(2, 8).toUpperCase()}`;
}

export function createCrudService({ basePath, fallbackData, idKey = 'id', codePrefix }) {
  let cache = cloneRows(fallbackData);

  const resolveList = () => ({ items: cloneRows(cache), total: cache.length });

  return {
    async list(params) {
      try {
        const { data } = await apiClient.get(basePath, { params });
        return data;
      } catch {
        return resolveList();
      }
    },
    async get(id) {
      try {
        const { data } = await apiClient.get(`${basePath}/${id}`);
        return data;
      } catch {
        return cache.find((row) => String(row[idKey]) === String(id)) || null;
      }
    },
    async create(payload) {
      try {
        const { data } = await apiClient.post(basePath, payload);
        return data;
      } catch {
        const record = {
          [idKey]: createId(codePrefix),
          ...payload,
        };
        cache = [record, ...cache];
        return record;
      }
    },
    async update(id, payload) {
      try {
        const { data } = await apiClient.patch(`${basePath}/${id}`, payload);
        return data;
      } catch {
        cache = cache.map((row) => (String(row[idKey]) === String(id) ? { ...row, ...payload } : row));
        return cache.find((row) => String(row[idKey]) === String(id)) || null;
      }
    },
    async remove(id) {
      try {
        await apiClient.delete(`${basePath}/${id}`);
      } catch {
        cache = cache.filter((row) => String(row[idKey]) !== String(id));
      }
      return true;
    },
  };
}