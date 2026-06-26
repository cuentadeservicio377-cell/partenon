import { CronManager } from '@/components/CronManager';
import { getCronJobs } from '@/lib/data';
import { getProfileParam } from '@/lib/search';

type PageProps = {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

export default async function CronPage({ searchParams }: PageProps) {
  const profile = await getProfileParam(searchParams);
  const jobs = await getCronJobs();

  return (
    <main className="grid gap-6">
      <div className="flex items-center justify-between">
        <h2 className="font-display text-xl font-medium text-partenon-text">Cron manager</h2>
        <p className="text-sm text-partenon-muted">{jobs.length} jobs configured</p>
      </div>
      <CronManager jobs={jobs} selectedProfile={profile} />
    </main>
  );
}
