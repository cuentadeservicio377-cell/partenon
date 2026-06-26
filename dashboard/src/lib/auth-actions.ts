'use server';

import { clearSessionCookie } from '@/lib/auth';

export async function logout() {
  await clearSessionCookie();
}
