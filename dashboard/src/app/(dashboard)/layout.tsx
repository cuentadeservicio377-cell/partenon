import { Suspense } from 'react';
import { TopNav } from '@/components/TopNav';
import { PROFILES } from '@/lib/env';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="mx-auto max-w-7xl px-4 py-6 md:px-6 md:py-8">
      <header className="mb-8">
        <h1 className="font-display text-3xl font-medium tracking-tight text-partenon-text md:text-4xl">
          Partenon Mission Control
        </h1>
        <p className="mt-1 text-sm text-partenon-muted">
          Panel de operaciones para los seis perfiles de Hermes.
        </p>
      </header>
      <Suspense fallback={<div className="mb-6 rounded-xl border border-partenon-border bg-partenon-card p-4 text-sm text-partenon-muted">Cargando navegacion...</div>}>
        <TopNav profiles={PROFILES.map((p) => ({ id: p.id, name: p.name }))} />
      </Suspense>
      {children}
    </div>
  );
}
