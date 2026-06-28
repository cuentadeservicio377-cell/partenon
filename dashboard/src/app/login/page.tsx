import { redirect } from 'next/navigation';
import { verifyCredentials, setSessionCookie, getServerSession } from '@/lib/auth';

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const session = await getServerSession();
  if (session.ok) {
    const params = await searchParams;
    const next = Array.isArray(params.next) ? params.next[0] : params.next || '/';
    redirect(next);
  }

  async function login(formData: FormData) {
    'use server';
    const username = String(formData.get('username') || '');
    const password = String(formData.get('password') || '');
    const next = String(formData.get('next') || '/');

    if (!verifyCredentials(username, password)) {
      redirect('/login?error=1');
    }

    await setSessionCookie(username, password);
    redirect(next);
  }

  const params = await searchParams;
  const next = Array.isArray(params.next) ? params.next[0] : params.next || '/';
  const error = params.error === '1';

  return (
    <main className="flex min-h-[60vh] items-center justify-center px-4">
      <div className="w-full max-w-sm rounded-xl border border-partenon-border bg-partenon-card p-6">
        <h1 className="mb-1 font-display text-2xl font-medium text-partenon-text">Partenon</h1>
        <p className="mb-6 text-sm text-partenon-muted">Sign in to the operations panel.</p>
        <form action={login} className="grid gap-4">
          <input type="hidden" name="next" value={next} />
          <div className="grid gap-2">
            <label htmlFor="username" className="text-xs text-partenon-muted">
              Username
            </label>
            <input
              id="username"
              name="username"
              autoComplete="username"
              className="rounded-lg border border-partenon-border bg-partenon-surface px-3 py-2 text-sm text-partenon-text"
            />
          </div>
          <div className="grid gap-2">
            <label htmlFor="password" className="text-xs text-partenon-muted">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              className="rounded-lg border border-partenon-border bg-partenon-surface px-3 py-2 text-sm text-partenon-text"
            />
          </div>
          {error && <p className="text-sm text-partenon-amber">Incorrect credentials.</p>}
          <button
            type="submit"
            className="rounded-lg bg-partenon-cyan px-4 py-2 text-sm font-medium text-partenon-bg transition-opacity hover:opacity-90"
          >
            Sign in
          </button>
        </form>
      </div>
    </main>
  );
}
