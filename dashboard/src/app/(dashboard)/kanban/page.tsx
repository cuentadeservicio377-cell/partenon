import { KanbanBoard } from '@/components/KanbanBoard';
import { getMissions } from '@/lib/data';
import { getProfileParam } from '@/lib/search';

type PageProps = {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

export default async function KanbanPage({ searchParams }: PageProps) {
  const profile = await getProfileParam(searchParams);
  const missions = await getMissions();

  return (
    <main className="grid gap-6">
      <div className="flex items-center justify-between">
        <h2 className="font-display text-xl font-medium text-partenon-text">Kanban de misiones</h2>
        <p className="text-sm text-partenon-muted">
          {missions.length} misiones en total
        </p>
      </div>
      <KanbanBoard missions={missions} selectedProfile={profile} />
    </main>
  );
}
