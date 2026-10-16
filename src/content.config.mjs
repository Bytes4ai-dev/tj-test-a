// Content collections (TJD-645). ONE collection, `posts`, read from src/content/posts.
// DEV-only fixture archive: src/content/fixtures joins the collection ONLY through the hook block below (DEV builds,
// never TJ_SITE_ENV=production). scripts/remove-fixtures.sh deletes the fixture directory and the hook block.
// Production guard: a TJ_SITE_ENV=production build FAILS if any entry in the collection is a fixture
// (frontmatter fixture: true, or a title starting "[TEST]"), naming the file.
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const production = process.env.TJ_SITE_ENV === 'production';
const patterns = ['posts/**/*.md'];

// FIXTURES-HOOK-BEGIN (DEV-only test archive; removed by scripts/remove-fixtures.sh)
if (process.env.TJ_SITE_FIXTURES === '1' && !production) patterns.push('fixtures/**/*.md');
// FIXTURES-HOOK-END

export const isFixture = (data) => data.fixture === true || String(data.title || '').startsWith('[TEST]');

function guardedGlob() {
  const inner = glob({
    pattern: patterns,
    base: './src/content',
    generateId: ({ entry }) => entry.replace(/^(posts|fixtures)\//, '').replace(/\.md$/, ''),
  });
  return {
    name: 'posts-with-fixture-guard',
    load: async (ctx) => {
      await inner.load(ctx);
      if (!production) return;
      const bad = [...ctx.store.values()].filter((e) => isFixture(e.data)).map((e) => e.filePath || e.id);
      if (bad.length) {
        throw new Error(
          `TJ_SITE_ENV=production build refused: fixture entr${bad.length === 1 ? 'y' : 'ies'} in content collections: ${bad.join(', ')}`,
        );
      }
    },
  };
}

const posts = defineCollection({
  loader: guardedGlob(),
  // TJD-643: the migrated donor posts carry `excerpt` (+ `draft`) and stay byte-for-byte as the donor wrote them,
  // so either `description` or `excerpt` is accepted; pages read `description`.
  schema: z
    .object({
      title: z.string(),
      date: z.coerce.date(),
      tags: z.array(z.string()).min(1),
      description: z.string().optional(),
      excerpt: z.string().optional(),
      draft: z.boolean().default(false),
      fixture: z.boolean().default(false),
    })
    .refine((d) => d.description || d.excerpt, { message: 'description or excerpt is required' })
    .transform((d) => ({ ...d, description: d.description || d.excerpt })),
});

export const collections = { posts };
