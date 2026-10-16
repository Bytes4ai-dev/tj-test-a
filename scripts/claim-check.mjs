#!/usr/bin/env node
// TJD-644 AC2 claim check (hard gate, PL 57018 (b)). Reads the BUILT retrospective pages (dist/timeline/<id>/index.html)
// and lists every paragraph that contains a number or names a study/survey/report. A flagged paragraph passes only if
// it has an <a href> link or a [n] Sources reference; otherwise the script exits 1 and names it.
// Scope: the post body and the chart caption of each retrospective (from class="post-body" up to the Sources list).
// "A number" = any digit, except a bare year (1900-2099) on its own; "[n]" Sources markers are not counted as numbers.
// Usage: node scripts/claim-check.mjs [distDir]   (default dist; run npm run build first). No dependencies.
import fs from 'node:fs';
import path from 'node:path';

const dist = process.argv[2] || 'dist';
const root = path.join(dist, 'timeline');
if (!fs.existsSync(root)) {
  console.error(`claim-check: no ${root} (run npm run build first)`);
  process.exit(2);
}

const STUDY = /\b(study|studies|survey|surveys|report|reports|index|forecast|paper|trial|benchmark|benchmarks|poll|research|analysis)\b/i;
const BLOCK = /<(p|li|figcaption|blockquote|td|th)\b[^>]*>([\s\S]*?)<\/\1>/g;
const plain = (h) => h.replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/&#39;|&#x27;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim();

const pages = fs.readdirSync(root).filter((d) => fs.existsSync(path.join(root, d, 'index.html'))).sort();
let flagged = 0;
let unsourced = 0;
const rows = [];
for (const id of pages) {
  const html = fs.readFileSync(path.join(root, id, 'index.html'), 'utf8');
  const start = html.indexOf('class="post-body"');
  const end = html.indexOf('class="post-sources"');
  if (start < 0 || end < 0 || end < start) {
    rows.push(`ERROR\t${id}\tpost-body or post-sources not found`);
    unsourced++;
    continue;
  }
  const scope = html.slice(start, end);
  let k = 0;
  for (const m of scope.matchAll(BLOCK)) {
    k++;
    const inner = m[2];
    const text = plain(inner);
    const numberText = text.replace(/\[\d+\]/g, ' ').replace(/\b(19|20)\d\d\b/g, ' ');
    const hasNumber = /\d/.test(numberText);
    const hasStudy = STUDY.test(text);
    if (!hasNumber && !hasStudy) continue;
    flagged++;
    const links = [...inner.matchAll(/<a\s[^>]*href="([^"]+)"/g)].map((x) => x[1]);
    const refs = text.match(/\[\d+\]/g) || [];
    const ok = links.length > 0 || refs.length > 0;
    if (!ok) unsourced++;
    const why = [hasNumber && 'number', hasStudy && 'study'].filter(Boolean).join('+');
    rows.push(`${ok ? 'SOURCED' : 'UNSOURCED'}\t${id}#${m[1]}${k}\t${why}\tlinks=${links.join(' ') || '-'}\trefs=${refs.join('') || '-'}\t${text.slice(0, 160)}`);
  }
}
console.log(rows.join('\n'));
console.log(`claim-check: ${pages.length} retrospectives, ${flagged} flagged paragraph(s), ${unsourced} unsourced`);
if (pages.length === 0) {
  console.log('claim-check: FAIL (no retrospective pages)');
  process.exit(1);
}
console.log(`claim-check: ${unsourced ? 'FAIL' : 'PASS'}`);
process.exit(unsourced ? 1 : 0);
