import { defineConfig } from 'astro/config';
import { site } from './src/config/site.mjs';

export default defineConfig({
  site: site.url,
  trailingSlash: 'ignore',
  // TJD-643: posts are RP's words verbatim, so no typographic rewriting of quotes or dashes on render.
  markdown: { smartypants: false },
});
