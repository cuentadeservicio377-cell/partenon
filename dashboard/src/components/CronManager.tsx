"use client";

import { useState, useTransition } from 'react';
import { createCronJob, updateCronJob, deleteCronJob } from '@/lib/data';
import { PROFILES, type ProfileId } from '@/lib/env';

type CronJob = {
  id: string;
  profile: ProfileId;
  schedule: string;
  command: string;
  enabled: boolean;
};

type CronManagerProps = {
  jobs: CronJob[];
  selectedProfile: string;
};

export function CronManager({ jobs, selectedProfile }: CronManagerProps) {
  const [items, setItems] = useState<CronJob[]>(jobs);
  const [profile, setProfile] = useState<ProfileId>(PROFILES[0].id);
  const [schedule, setSchedule] = useState('0 9 * * *');
  const [command, setCommand] = useState('');
  const [enabled, setEnabled] = useState(true);
  const [status, setStatus] = useState('');
  const [busyId, setBusyId] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const visible =
    selectedProfile && selectedProfile !== 'all'
      ? items.filter((j) => j.profile === selectedProfile)
      : items;

  function resetForm() {
    setSchedule('0 9 * * *');
    setCommand('');
    setEnabled(true);
    setProfile(PROFILES[0].id);
  }

  function create() {
    if (!command.trim()) {
      setStatus('El comando es obligatorio.');
      return;
    }
    setStatus('');
    setBusyId('create');
    startTransition(async () => {
      await createCronJob({ profile, schedule, command, enabled });
      resetForm();
      setBusyId(null);
      setStatus('Job creado.');
      window.location.reload();
    });
  }

  function toggle(id: string, next: boolean) {
    setBusyId(id);
    startTransition(async () => {
      const updated = await updateCronJob(id, { enabled: next });
      setItems(updated);
      setBusyId(null);
    });
  }

  function remove(id: string) {
    if (!confirm('Eliminar este cron job?')) return;
    setBusyId(id);
    startTransition(async () => {
      const updated = await deleteCronJob(id);
      setItems(updated);
      setBusyId(null);
    });
  }

  return (
    <div className="grid gap-6">
      <section className="rounded-xl border border-partenon-border bg-partenon-card p-4 md:p-6">
        <h2 className="mb-4 font-display text-lg font-medium text-partenon-text">Nuevo cron job</h2>
        <div className="grid gap-4 md:grid-cols-2">
          <div className="grid gap-2">
            <label className="text-xs text-partenon-muted">Perfil</label>
            <select
              value={profile}
              onChange={(e) => setProfile(e.target.value as ProfileId)}
              className="rounded-lg border border-partenon-border bg-partenon-surface px-3 py-2 text-sm text-partenon-text"
            >
              {PROFILES.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          </div>
          <div className="grid gap-2">
            <label className="text-xs text-partenon-muted">Schedule</label>
            <input
              value={schedule}
              onChange={(e) => setSchedule(e.target.value)}
              placeholder="0 9 * * *"
              className="rounded-lg border border-partenon-border bg-partenon-surface px-3 py-2 text-sm text-partenon-text"
            />
          </div>
          <div className="grid gap-2 md:col-span-2">
            <label className="text-xs text-partenon-muted">Comando</label>
            <input
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              placeholder="python -m partenon.tesorero weekly_report"
              className="rounded-lg border border-partenon-border bg-partenon-surface px-3 py-2 text-sm text-partenon-text"
            />
          </div>
          <div className="flex items-center gap-2 md:col-span-2">
            <input
              id="enabled"
              type="checkbox"
              checked={enabled}
              onChange={(e) => setEnabled(e.target.checked)}
              className="h-4 w-4 accent-partenon-cyan"
            />
            <label htmlFor="enabled" className="text-sm text-partenon-text">
              Activado
            </label>
          </div>
        </div>
        <div className="mt-4 flex items-center gap-4">
          <button
            onClick={create}
            disabled={busyId === 'create' || isPending}
            className="rounded-lg bg-partenon-cyan px-4 py-2 text-sm font-medium text-partenon-bg transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Crear job
          </button>
          {status ? <p className="text-sm text-partenon-muted">{status}</p> : null}
        </div>
      </section>

      <section className="rounded-xl border border-partenon-border bg-partenon-card p-4 md:p-6">
        <h2 className="mb-4 font-display text-lg font-medium text-partenon-text">Jobs existentes</h2>
        {visible.length === 0 ? (
          <p className="text-sm text-partenon-muted">No hay cron jobs.</p>
        ) : (
          <div className="grid gap-3">
            {visible.map((job) => (
              <article
                key={job.id}
                className="flex flex-col gap-3 rounded-lg border border-partenon-border bg-partenon-surface p-3 md:flex-row md:items-center md:justify-between"
              >
                <div className="grid gap-1">
                  <div className="flex items-center gap-2">
                    <span
                      className="inline-block h-2 w-2 rounded-full"
                      style={{ backgroundColor: PROFILES.find((p) => p.id === job.profile)?.color }}
                    />
                    <span className="text-xs text-partenon-muted">
                      {PROFILES.find((p) => p.id === job.profile)?.name}
                    </span>
                    <span
                      className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                        job.enabled
                          ? 'bg-partenon-cyan/10 text-partenon-cyan'
                          : 'bg-partenon-muted/10 text-partenon-muted'
                      }`}
                    >
                      {job.enabled ? 'Activo' : 'Pausado'}
                    </span>
                  </div>
                  <code className="font-mono text-xs text-partenon-text">{job.command}</code>
                  <p className="font-mono text-xs text-partenon-muted">{job.schedule}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => toggle(job.id, !job.enabled)}
                    disabled={busyId === job.id || isPending}
                    className="rounded-md border border-partenon-border bg-partenon-card px-3 py-1.5 text-xs font-medium text-partenon-text transition-colors hover:border-partenon-cyan hover:text-partenon-cyan disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {job.enabled ? 'Pausar' : 'Activar'}
                  </button>
                  <button
                    onClick={() => remove(job.id)}
                    disabled={busyId === job.id || isPending}
                    className="rounded-md border border-partenon-border bg-partenon-card px-3 py-1.5 text-xs font-medium text-partenon-text transition-colors hover:border-partenon-amber hover:text-partenon-amber disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    Eliminar
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
