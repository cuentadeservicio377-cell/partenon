export const PROFILES = [
  { id: 'partenon-tesorero', name: 'Tesorero', color: '#00D4FF' },
  { id: 'partenon-mensajero', name: 'Mensajero', color: '#FFB800' },
  { id: 'partenon-cobrador', name: 'Cobrador', color: '#22C55E' },
  { id: 'partenon-guardian', name: 'Guardian', color: '#EF4444' },
  { id: 'partenon-estratega', name: 'Estratega', color: '#A855F7' },
  { id: 'partenon-diplomatico', name: 'Diplomatico', color: '#EC4899' },
] as const;

export type ProfileId = (typeof PROFILES)[number]['id'];

export const STATUSES = [
  'ideas',
  'backlog',
  'por_hacer',
  'en_progreso',
  'revision',
  'hecho',
] as const;

export type Status = (typeof STATUSES)[number];

export const STATUS_LABELS: Record<Status, string> = {
  ideas: 'Ideas',
  backlog: 'Backlog',
  por_hacer: 'Por hacer',
  en_progreso: 'En progreso',
  revision: 'Revision',
  hecho: 'Hecho',
};

export function getProfile(id: string) {
  return PROFILES.find((p) => p.id === id) || PROFILES[0];
}

export function isValidStatus(value: string): value is Status {
  return STATUSES.includes(value as Status);
}
