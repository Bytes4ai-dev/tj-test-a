// TJD-644 Timeline retrospectives: one order everywhere (the outline order on TJD-640, 2024 first).
import { getCollection } from 'astro:content';
import meta from '../data/retrospectives.json';

export const YEARS = ['2024', '2025', '2026'];
export const published = meta.published;
export const byline = meta.byline;
if (!/^2026-\d\d-\d\d$/.test(published)) throw new Error(`retrospectives.json: published must be a 2026 date, got ${published}`);

export async function getRetros() {
  const all = await getCollection('retrospectives');
  return all.sort((a, b) => a.data.order - b.data.order);
}

export const retroUrl = (r) => `/timeline/${r.id}/`;
export const visual = (r, name) => `/timeline/${r.id}/${name}.svg`;
export const readingMinutes = (r) => Math.max(1, Math.round((r.body || '').split(/\s+/).filter(Boolean).length / 200));
// Each service on the Home page; the "What to do about it" section links to exactly one of them.
export const serviceUrl = () => '/#services';
