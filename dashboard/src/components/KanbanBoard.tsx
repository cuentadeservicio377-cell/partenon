"use client";

import { useState, useTransition } from 'react';
import { updateMissionStatus } from '@/lib/data';
import { STATUS_LABELS, type Status, type ProfileId, getProfile, STATUSES } from '@/lib/env';

type Mission = {
  id: string;
  profile: ProfileId;
  title: string;
  status: Status;
  priority: string;
  description: string;
};

type KanbanBoardProps = {
  missions: Mission[];
  selectedProfile: string;
};

const PRIORITY_ORDER: Record<string, number> = {
  high: 1,
  medium: 2,
  low: 3,
};

export function KanbanBoard({ missions, selectedProfile }: KanbanBoardProps) {
  const [items, setItems] = useState<Mission[]>(missions);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const visible =
    selectedProfile && selectedProfile !== 'all'
      ? items.filter((m) => m.profile === selectedProfile)
      : items;

  function move(id: string, next: Status) {
    setBusyId(id);
    startTransition(async () => {
      const updated = await updateMissionStatus(id, next);
      setItems(updated);
      setBusyId(null);
    });
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {STATUSES.map((status) => {
        const column = visible
          .filter((m) => m.status === status)
          .sort((a, b) => PRIORITY_ORDER[a.priority] - PRIORITY_ORDER[b.priority]);
        return (
          <section
            key={status}
            className="flex max-h-[70vh] flex-col rounded-xl border border-partenon-border bg-partenon-card"
          >
            <div className="flex items-center justify-between border-b border-partenon-border px-4 py-3">
              <h3 className="text-sm font-medium text-partenon-text">{STATUS_LABELS[status]}</h3>
              <span className="rounded-full bg-partenon-surface px-2 py-0.5 text-xs text-partenon-muted">
                {column.length}
              </span>
            </div>
            <div className="flex-1 overflow-y-auto p-3">
              <div className="grid gap-3">
                {column.map((mission) => (
                  <MissionCard
                    key={mission.id}
                    mission={mission}
                    busy={busyId === mission.id || isPending}
                    onMove={move}
                  />
                ))}
                {column.length === 0 && (
                  <p className="py-6 text-center text-xs text-partenon-muted">No missions</p>
                )}
              </div>
            </div>
          </section>
        );
      })}
    </div>
  );
}

function MissionCard({
  mission,
  busy,
  onMove,
}: {
  mission: Mission;
  busy: boolean;
  onMove: (id: string, status: Status) => void;
}) {
  const profile = getProfile(mission.profile);
  const currentIndex = STATUSES.indexOf(mission.status);

  return (
    <article className="rounded-lg border border-partenon-border bg-partenon-surface p-3 transition-colors hover:border-partenon-cyan/30">
      <div className="mb-2 flex items-start justify-between gap-2">
        <h4 className="text-sm font-medium leading-snug text-partenon-text">{mission.title}</h4>
        <PriorityBadge priority={mission.priority} />
      </div>
      <p className="mb-3 line-clamp-3 text-xs leading-relaxed text-partenon-muted">
        {mission.description}
      </p>
      <div className="mb-3 flex items-center gap-2">
        <span
          className="inline-block h-2 w-2 rounded-full"
          style={{ backgroundColor: profile.color }}
        />
        <span className="text-xs text-partenon-muted">{profile.name}</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {currentIndex > 0 && (
          <MoveButton
            label="<<"
            title={STATUS_LABELS[STATUSES[currentIndex - 1]]}
            disabled={busy}
            onClick={() => onMove(mission.id, STATUSES[currentIndex - 1])}
          />
        )}
        {currentIndex < STATUSES.length - 1 && (
          <MoveButton
            label=">>"
            title={STATUS_LABELS[STATUSES[currentIndex + 1]]}
            disabled={busy}
            onClick={() => onMove(mission.id, STATUSES[currentIndex + 1])}
          />
        )}
      </div>
    </article>
  );
}

function PriorityBadge({ priority }: { priority: string }) {
  const color =
    priority === 'high' ? 'text-partenon-amber' : priority === 'medium' ? 'text-partenon-cyan' : 'text-partenon-muted';
  return <span className={`text-xs font-medium uppercase ${color}`}>{priority}</span>;
}

function MoveButton({
  label,
  title,
  disabled,
  onClick,
}: {
  label: string;
  title: string;
  disabled: boolean;
  onClick: () => void;
}) {
  return (
    <button
      title={title}
      disabled={disabled}
      onClick={onClick}
      className="rounded-md border border-partenon-border bg-partenon-card px-2 py-1 text-xs font-medium text-partenon-text transition-colors hover:border-partenon-cyan hover:text-partenon-cyan disabled:cursor-not-allowed disabled:opacity-50"
    >
      {label}
    </button>
  );
}
