// Shared post helpers (TJD-645): one sort order everywhere (publish date desc, then id) so archive, filters and RSS agree.
import { getCollection } from 'astro:content';

export const TAGS = ['Governance', 'Agents', 'Observability', 'Engineering', 'Data and people'];
export const PAGE_SIZE = 10;

export async function getPosts() {
  const all = await getCollection('posts', ({ data }) => !data.draft);
  return all.sort((a, b) => b.data.date - a.data.date || a.id.localeCompare(b.id));
}

export const postUrl = (post) => `/posts/${post.id}/`;
export const isoDate = (d) => d.toISOString().slice(0, 10);
export const yearOf = (post) => post.data.date.getUTCFullYear();
export const readingMinutes = (post) => Math.max(1, Math.round((post.body || '').split(/\s+/).filter(Boolean).length / 200));

// TJD-643: the migrated donor posts keep their own finer tags in the post files (never edited). Each one maps to at
// most one of the five Insights tags here; ai/opinion/critical do not map. The five tag names map to themselves
// (the TJD-645 fixtures use them directly). Dev choice, listed in PRELAUNCH-CHECKLIST.md for RP to confirm.
const TAG_MAP = {
  governance: 'Governance', safety: 'Governance', containment: 'Governance', security: 'Governance',
  agents: 'Agents',
  observability: 'Observability', evals: 'Observability',
  engineering: 'Engineering', infrastructure: 'Engineering', reliability: 'Engineering',
  data: 'Data and people', privacy: 'Data and people', 'data and people': 'Data and people',
};

export function siteTags(post) {
  const out = [];
  for (const t of post.data.tags) {
    const s = TAG_MAP[t.toLowerCase()];
    if (s && !out.includes(s)) out.push(s);
  }
  return out;
}

// Markdown source -> plain words for the in-page search index. Display never uses this.
export function plainText(md) {
  return (md || '')
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/<[^>]+>/g, ' ')
    .replace(/[#>*_`~|]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}
