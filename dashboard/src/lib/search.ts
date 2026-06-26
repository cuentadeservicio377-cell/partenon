export async function getProfileParam(searchParams: Promise<Record<string, string | string[] | undefined>>): Promise<string> {
  const params = await searchParams;
  const raw = params.profile;
  if (Array.isArray(raw)) return raw[0] || 'all';
  return raw || 'all';
}
