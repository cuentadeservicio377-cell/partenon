import { cookies } from 'next/headers';

const API_URL = process.env.PARTENON_API_URL || 'http://127.0.0.1:8000';
const COOKIE_NAME = 'partenon_dashboard_session';

export function getApiUrl(): string {
  return API_URL;
}

export async function apiFetch(path: string, init: RequestInit = {}) {
  const jar = await cookies();
  const token = jar.get(COOKIE_NAME)?.value;
  if (!token) {
    throw new Error('Not authenticated');
  }

  const url = `${API_URL}${path}`;
  const headers = new Headers(init.headers);
  headers.set('Authorization', `Bearer ${token}`);
  if (!headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(url, {
    ...init,
    headers,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error ${response.status}: ${text}`);
  }

  return response.json();
}
