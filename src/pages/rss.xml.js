// RSS 2.0 feed (TJD-645): every post in the `posts` collection, newest publish date first (same order as Insights).
import { site } from '../config/site.mjs';
import { getPosts, postUrl } from '../lib/posts.mjs';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export async function GET() {
  const base = site.url.replace(/\/$/, '');
  const posts = await getPosts();
  const items = posts
    .map((p) => {
      const link = base + postUrl(p);
      const cats = p.data.tags.map((t) => `<category>${esc(t)}</category>`).join('');
      return `<item><title>${esc(p.data.title)}</title><link>${esc(link)}</link><guid isPermaLink="true">${esc(link)}</guid><pubDate>${p.data.date.toUTCString()}</pubDate><description>${esc(p.data.description)}</description>${cats}</item>`;
    })
    .join('\n');
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>
<title>${esc(site.name)} Insights</title>
<link>${esc(base)}/insights/</link>
<atom:link href="${esc(base)}/rss.xml" rel="self" type="application/rss+xml"/>
<description>Insights on AI agent governance, observability and data from ${esc(site.name)}.</description>
<language>en</language>
${items}
</channel></rss>
`;
  return new Response(body, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
}
