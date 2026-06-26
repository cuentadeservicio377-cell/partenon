export const PROFILES = [
  { id: 'partenon-tesorero', name: 'Treasurer', color: '#00D4FF' },
  { id: 'partenon-mensajero', name: 'Messenger', color: '#FFB800' },
  { id: 'partenon-cobrador', name: 'Collector', color: '#22C55E' },
  { id: 'partenon-guardian', name: 'Guardian', color: '#EF4444' },
  { id: 'partenon-estratega', name: 'Strategist', color: '#A855F7' },
  { id: 'partenon-diplomatico', name: 'Diplomat', color: '#EC4899' },
] as const;

export type ProfileId = (typeof PROFILES)[number]['id'];

export const STATUSES = [
  'ideas',
  'backlog',
  'to_do',
  'in_progress',
  'review',
  'done',
] as const;

export type Status = (typeof STATUSES)[number];

export const STATUS_LABELS: Record<Status, string> = {
  ideas: 'Ideas',
  backlog: 'Backlog',
  to_do: 'To do',
  in_progress: 'In progress',
  review: 'Review',
  done: 'Done',
};

export function getProfile(id: string) {
  return PROFILES.find((p) => p.id === id) || PROFILES[0];
}

export function isValidStatus(value: string): value is Status {
  return STATUSES.includes(value as Status);
}
