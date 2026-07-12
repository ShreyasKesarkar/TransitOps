import apiClient from './apiClient';
import { decodeJwtPayload, normalizeAuthUser } from './normalizers';

export async function login(credentials) {
  const { data } = await apiClient.post('/auth/login', credentials);
  return {
    token: data.access_token,
    tokenType: data.token_type,
    expiresIn: data.expires_in,
  };
}

export async function fetchCurrentUser(token) {
  let storedToken = null;
  if (!token) {
    try {
      const stored = localStorage.getItem('transitops.auth');
      storedToken = stored ? JSON.parse(stored).token : null;
    } catch {
      storedToken = null;
    }
  }
  const authToken = token ?? storedToken;

  try {
    const { data } = await apiClient.get('/auth/me', {
      headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
    });
    return normalizeAuthUser(data, authToken);
  } catch {
    const payload = decodeJwtPayload(authToken);
    return normalizeAuthUser(
      {
        user_id: payload?.sub ? Number(payload.sub) : null,
        organization_id: payload?.organization_id ?? null,
        role_id: payload?.role_id ?? null,
        full_name: payload?.full_name ?? null,
        email: payload?.email ?? '',
        must_change_password: false,
      },
      authToken,
    );
  }
}

export async function logout() {
  try {
    await apiClient.post('/auth/logout');
  } catch {
    return true;
  }
  return true;
}

export async function requestPasswordReset(payload) {
  try {
    const { data } = await apiClient.post('/auth/forgot-password', payload);
    return data;
  } catch {
    return { message: 'Password reset is not available in the current backend yet.' };
  }
}

export async function changePassword(payload) {
  try {
    const { data } = await apiClient.post('/auth/change-password', payload);
    return data;
  } catch {
    return { message: 'Password change is not available in the current backend yet.' };
  }
}