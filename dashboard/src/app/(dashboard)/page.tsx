import { getMissions, getCronJobs } from '@/lib/data';
import { getProfileParam } from '@/lib/search';
import Link from 'next/link';

type PageProps = {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

export default async function HomePage({ searchParams }: PageProps) {
  const profile = await getProfileParam(searchParams);
  const missions = await getMissions();
  const cronJobs = await getCronJobs();

  const filteredMissions = profile && profile !== 'all' ? missions.filter((m) => m.profile === profile) : missions;
  const filteredCron = profile && profile !== 'all' ? cronJobs.filter((j) => j.profile === profile) : cronJobs;

  const done = filteredMissions.filter((m) => m.status === 'done').length;
  const total = filteredMissions.length;
  const activeCron = filteredCron.filter((j) => j.enabled).length;
  const highPriority = filteredMissions.filter((m) => m.priority === 'high' && m.status !== 'done').length;

  const q = profile && profile !== 'all' ? `?profile=${encodeURIComponent(profile)}` : '';

  return (
    <main className="grid gap-6">
      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard label="Missions" value={`${done}/${total}`} href={`/kanban${q}`} />
        <KpiCard label="Active cron jobs" value={String(activeCron)} href={`/cron${q}`} />
        <KpiCard label="High priority" value={String(highPriority)} href={`/kanban${q}`} />
        <KpiCard label="Profiles" value="6" href={`/kanban${q}`} />
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-partenon-border bg-partenon-card p-4 md:p-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-display text-lg font-medium text-partenon-text">Recent missions</h2>
            <Link href={`/kanban${q}`} className="text-sm text-partenon-cyan hover:underline">
              View kanban
            </Link>
          </div>
          <div className="grid gap-3">
            {filteredMissions.slice(0, 5).map((m) => (
              <div
                key={m.id}
                className="flex items-center justify-between rounded-lg border border-partenon-border bg-partenon-surface p-3"
              >
                <div>
                  <p className="text-sm font-medium text-partenon-text">{m.title}</p>
                  <p className="text-xs text-partenon-muted capitalize">{m.status.replace(/_/g, ' ')}</p>
                </div>
                <span
                  className={`text-xs font-medium uppercase ${
                    m.priority === 'high'
                      ? 'text-partenon-amber'
                      : m.priority === 'medium'
                        ? 'text-partenon-cyan'
                        : 'text-partenon-muted'
                  }`}
                >
                  {m.priority}
                </span>
              </div>
            ))}
            {filteredMissions.length === 0 && (
              <p className="text-sm text-partenon-muted">No missions for this profile.</p>
            )}
          </div>
        </div>

        <div className="rounded-xl border border-partenon-border bg-partenon-card p-4 md:p-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-display text-lg font-medium text-partenon-text">Cron jobs</h2>
            <Link href={`/cron${q}`} className="text-sm text-partenon-cyan hover:underline">
              Manage
            </Link>
          </div>
          <div className="grid gap-3">
            {filteredCron.slice(0, 5).map((j) => (
              <div
                key={j.id}
                className="flex items-center justify-between rounded-lg border border-partenon-border bg-partenon-surface p-3"
              >
                <div>
                  <code className="font-mono text-xs text-partenon-text">{j.command}</code>
                  <p className="font-mono text-xs text-partenon-muted">{j.schedule}</p>
                </div>
                <span
                  className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                    j.enabled
                      ? 'bg-partenon-cyan/10 text-partenon-cyan'
                      : 'bg-partenon-muted/10 text-partenon-muted'
                  }`}
                >
                  {j.enabled ? 'Active' : 'Paused'}
                </span>
              </div>
            ))}
            {filteredCron.length === 0 && (
              <p className="text-sm text-partenon-muted">No cron jobs for this profile.</p>
            )}
          </div>
        </div>
      </section>
    </main>
  );
}

function KpiCard({ label, value, href }: { label: string; value: string; href: string }) {
  return (
    <Link
      href={href}
      className="rounded-xl border border-partenon-border bg-partenon-card p-4 transition-colors hover:border-partenon-cyan/30 md:p-6"
    >
      <p className="text-sm text-partenon-muted">{label}</p>
      <p className="mt-2 font-display text-3xl font-medium text-partenon-text">{value}</p>
    </Link>
  );
}
