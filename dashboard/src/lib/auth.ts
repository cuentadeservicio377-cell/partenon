import { createHmac, timingSafeEqual } from 'node:crypto';
import { cookies } from 'next/headers';

const COOKIE_NAME = 'partenon_dashboard_session';
const SESSION_TTL_MS = 1000 * 60 * 60 * 12;

function getSecret() {
  const secret = process.env.DASHBOARD_AUTH_SECRET;
  if (!secret) {
    throw new Error('DASHBOARD_AUTH_SECRET is not set');
  }
  return secret;
}

function nowMs() {
  return Date.now();
}

function base64url(input: string) {
  return Buffer.from(input, 'utf8').toString('base64url');
}

function sign(value: string) {
  return createHmac('sha256', getSecret()).update(value).digest('base64url');
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

export function buildSessionToken(username: string) {
  const payload = JSON.stringify({
    sub: username,
    exp: nowMs() + SESSION_TTL_MS,
  });
  const encoded = base64url(payload);
  const signature = sign(encoded);
  return `${encoded}.${signature}`;
}

export function verifySessionToken(token: string | undefined | null): { ok: boolean; username?: string } {
  if (!token) return { ok: false };
  const [encoded, signature] = token.split('.');
  if (!encoded || !signature) return { ok: false };
  const expected = sign(encoded);
  const a = Buffer.from(signature);
  const b = Buffer.from(expected);
  if (a.length !== b.length || !timingSafeEqual(a, b)) return { ok: false };

  try {
    const json = JSON.parse(Buffer.from(encoded, 'base64url').toString('utf8')) as {
      sub?: string;
      exp?: number;
    };
    if (!json.sub || typeof json.exp !== 'number') return { ok: false };
    if (json.exp < nowMs()) return { ok: false };
    return { ok: true, username: json.sub };
  } catch {
    return { ok: false };
  }
}

export async function getServerSession() {
  const jar = await cookies();
  const token = jar.get(COOKIE_NAME)?.value;
  return verifySessionToken(token);
}

export async function setSessionCookie(username: string) {
  const jar = await cookies();
  jar.set(COOKIE_NAME, buildSessionToken(username), {
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
