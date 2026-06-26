"use client";

import Link from 'next/link';
import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import { useState, useTransition } from 'react';
import { logout } from '@/lib/auth-actions';

type ProfileView = {
  id: string;
  name: string;
};

type TopNavProps = {
  profiles: ProfileView[];
};

const NAV_ITEMS = [
  ['/', 'Home'],
  ['/kanban', 'Kanban'],
  ['/cron', 'Cron'],
] as const;

export function TopNav({ profiles }: TopNavProps) {
  const pathname = usePathname();
  const router = useRouter();
  const params = useSearchParams();
  const profile = params.get('profile') || 'all';
  const [isPending, startTransition] = useTransition();

  function hrefWithContext(path: string) {
    const q = new URLSearchParams(params.toString());
    if (profile && profile !== 'all') q.set('profile', profile);
    return `${path}?${q.toString()}`;
  }

  function updateProfile(next: string) {
    const q = new URLSearchParams(params.toString());
    if (next === 'all') {
      q.delete('profile');
    } else {
      q.set('profile', next);
    }
    startTransition(() => {
      router.push(`${pathname}?${q.toString()}`);
    });
  }

  async function handleLogout() {
    await logout();
    router.push('/login');
  }

  return (
    <div className="mb-6 rounded-xl border border-partenon-border bg-partenon-card p-4">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <label htmlFor="profile-select" className="text-sm text-partenon-muted">
            Perfil
          </label>
          <select
            id="profile-select"
            value={profile}
            onChange={(e) => updateProfile(e.target.value)}
            disabled={isPending}
            className="rounded-lg border border-partenon-border bg-partenon-surface px-3 py-2 text-sm text-partenon-text"
          >
            <option value="all">Todos</option>
            {profiles.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </div>

        <nav className="flex flex-wrap gap-2">
          {NAV_ITEMS.map(([path, label]) => {
            const active = pathname === path;
            return (
              <Link
                key={path}
                href={hrefWithContext(path)}
                className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
                  active
                    ? 'bg-partenon-cyan/10 text-partenon-cyan'
                    : 'text-partenon-muted hover:bg-partenon-surface hover:text-partenon-text'
                }`}
              >
                {label}
              </Link>
            );
          })}
          <button
            onClick={handleLogout}
            className="rounded-lg px-4 py-2 text-sm font-medium text-partenon-muted transition-colors hover:bg-partenon-surface hover:text-partenon-text"
          >
            Salir
          </button>
        </nav>
      </div>
    </div>
  );
}
