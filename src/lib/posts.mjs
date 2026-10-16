// Shared post helpers (TJD-645): one sort order everywhere (publish date desc, then id) so archive, filters and RSS agree.
import { getCollection } from 'astro:content';

export const TAGS = ['Governance', 'Agents', 'Observability', 'Engineering', 'Data and people'];
export const PAGE_SIZE = 10;

export async function getPosts() {
  const all = await getCollection('posts');
  return all.sort((a, b) => b.data.date - a.data.date || a.id.localeCompare(b.id));
}

export const postUrl = (post) => `/posts/${post.id}/`;
export const isoDate = (d) => d.toISOString().slice(0, 10);
export const yearOf = (post) => post.data.date.getUTCFullYear();
export const readingMinutes = (post) => Math.max(1, Math.round((post.body || '').split(/\s+/).filter(Boolean).length / 200));
