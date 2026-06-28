import { cookies } from 'next/headers';
import * as jose from 'jose';

const COOKIE_NAME = 'partenon_dashboard_session';
const SESSION_TTL_MS = 1000 * 60 * 60 * 12;

function getSecret() {
  const secret = process.env.PARTENON_API_SECRET || process.env.DASHBOARD_AUTH_SECRET;
  if (!secret) {
    throw new Error('PARTENON_API_SECRET or DASHBOARD_AUTH_SECRET is not set');
  }
  return new TextEncoder().encode(secret);
}

function getApiUrl() {
  return process.env.PARTENON_API_URL || 'http://127.0.0.1:8000';
}

function getExpectedCreds() {
  const username = process.env.DASHBOARD_APP_USERNAME;
  const password = process.env.DASHBOARD_APP_PASSWORD;
  if (!username || !password) {
    throw new Error('DASHBOARD_APP_USERNAME and DASHBOARD_APP_PASSWORD must be set');
  }
  return { username, password };
}

export function verifyCredentials(username: string, password: string) {
  const expected = getExpectedCreds();
  return username === expected.username && password === expected.password;
}

export async function buildSessionToken(username: string, password: string) {
  const response = await fetch(`${getApiUrl()}/api/v1/auth/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!response.ok) {
    throw new Error('Invalid credentials');
  }
  const data = (await response.json()) as { access_token: string };
  return data.access_token;
}

export async function verifySessionToken(
  token: string | undefined | null
): Promise<{ ok: boolean; username?: string }> {
  if (!token) return { ok: false };
  try {
    const { payload } = await jose.jwtVerify(token, getSecret(), {
      algorithms: ['HS256'],
    });
    if (typeof payload.sub !== 'string') return { ok: false };
    if (typeof payload.exp === 'number' && payload.exp * 1000 < Date.now()) {
      return { ok: false };
    }
    return { ok: true, username: payload.sub };
  } catch {
    return { ok: false };
  }
}

export async function getServerSession() {
  const jar = await cookies();
  const token = jar.get(COOKIE_NAME)?.value;
  return verifySessionToken(token);
}

export async function setSessionCookie(username: string, password: string) {
  const token = await buildSessionToken(username, password);
  const jar = await cookies();
  jar.set(COOKIE_NAME, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
    maxAge: SESSION_TTL_MS / 1000,
  });
}

export async function clearSessionCookie() {
  const jar = await cookies();
  jar.delete(COOKIE_NAME);
}

export const AUTH_COOKIE_NAME = COOKIE_NAME;
