'use server';

import fs from 'node:fs/promises';
import path from 'node:path';
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
};

const PROJECT_ROOT = path.resolve(process.cwd(), '..');
const TASKS_PATH = path.join(PROJECT_ROOT, 'data', 'tasks.json');
const CRON_PATH = path.join(PROJECT_ROOT, 'data', 'cron.json');

async function readJson<T>(filePath: string): Promise<T> {
  try {
    const raw = await fs.readFile(filePath, 'utf8');
    return JSON.parse(raw) as T;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      return [] as unknown as T;
    }
    throw error;
  }
}

async function writeJson<T>(filePath: string, data: T) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

export async function getMissions(): Promise<Mission[]> {
  return readJson<Mission[]>(TASKS_PATH);
}

export async function updateMissionStatus(id: string, status: Status): Promise<Mission[]> {
  const missions = await getMissions();
  const updated = missions.map((m) => (m.id === id ? { ...m, status } : m));
  await writeJson(TASKS_PATH, updated);
  return updated;
}

export async function getCronJobs(): Promise<CronJob[]> {
  return readJson<CronJob[]>(CRON_PATH);
}

export async function createCronJob(job: Omit<CronJob, 'id'>): Promise<CronJob[]> {
  const jobs = await getCronJobs();
  const id = `cron-${Date.now()}`;
  const created = [...jobs, { ...job, id }];
  await writeJson(CRON_PATH, created);
  return created;
}

export async function updateCronJob(id: string, patch: Partial<Omit<CronJob, 'id'>>): Promise<CronJob[]> {
  const jobs = await getCronJobs();
  const updated = jobs.map((j) => (j.id === id ? { ...j, ...patch } : j));
  await writeJson(CRON_PATH, updated);
  return updated;
}

export async function deleteCronJob(id: string): Promise<CronJob[]> {
  const jobs = await getCronJobs();
  const updated = jobs.filter((j) => j.id !== id);
  await writeJson(CRON_PATH, updated);
  return updated;
}
