'use server';

import { apiFetch } from '@/lib/api';
import { type ProfileId, type Status } from '@/lib/env';

export type Mission = {
  id: string;
  profile: ProfileId;
  title: string;
  status: Status;
  priority: string;
  description: string;
};

export type CronJob = {
  id: string;
  profile: ProfileId;
  schedule: string;
  command: string;
  enabled: boolean;
  note?: string;
};

export async function getMissions(): Promise<Mission[]> {
  const data = (await apiFetch('/api/v1/missions')) as { missions: Mission[] };
  return data.missions;
}

export async function updateMissionStatus(id: string, status: Status): Promise<Mission[]> {
  await apiFetch(`/api/v1/missions/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });
  return getMissions();
}

export async function getCronJobs(): Promise<CronJob[]> {
  const data = (await apiFetch('/api/v1/cron')) as { cron: CronJob[] };
  return data.cron;
}

export async function createCronJob(job: Omit<CronJob, 'id'>): Promise<CronJob[]> {
  await apiFetch('/api/v1/cron', {
    method: 'POST',
    body: JSON.stringify(job),
  });
  return getCronJobs();
}

export async function updateCronJob(id: string, patch: Partial<Omit<CronJob, 'id'>>): Promise<CronJob[]> {
  await apiFetch(`/api/v1/cron/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(patch),
  });
  return getCronJobs();
}

export async function deleteCronJob(id: string): Promise<CronJob[]> {
  await apiFetch(`/api/v1/cron/${id}`, {
    method: 'DELETE',
  });
  return getCronJobs();
}
