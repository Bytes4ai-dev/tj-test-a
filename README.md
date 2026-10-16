# Bytes4AI website (tj-test-a)

Astro static site for the rv-demo project `bytes4ai-site` (TJD-640 / TJD-641 Phase 1).

- `npm ci && npm run build` → `dist/`
- `bash tests/site-check.sh` → build + static checks (tokens, share previews, Experience facts, Platform data, deny-list)
- `bash scripts/prelaunch-check.sh [dist]` → deny-list (phone, personal email, secret-looking tokens, `[TEST]`)
- `bash scripts/platform-status.sh` / `bash scripts/proof-of-loop.sh` → regenerate `src/data/*.json` from Jira (read-only; needs TJGraph-Local `jira.sh`)
- `python3 scripts/make-og.py` → redraw `public/og/*.png`
- Container: `docker build .` serves on `$PORT` (default 8080) as non-root; `GET /healthz` → 200. `cloudbuild.yaml` is unchanged (TJD-191/546 contract).
- Posts: `src/content/posts/*.md` (collection `posts`, `src/content.config.mjs`) → `/insights/` (search, tag + year filters, count), `/insights/archive/N/`, `/posts/<id>/`, `/rss.xml` (newest first)
- DEV-only `[TEST]` fixture archive (TJD-645): `src/content/fixtures/` (40 posts, `fixture: true`) is built only with `TJ_SITE_FIXTURES=1` (Docker: `--build-arg TJ_SITE_FIXTURES=1`). `TJ_SITE_ENV=production` excludes them and fails if any fixture entry (`fixture: true` or title `[TEST]…`) is in the collection. `bash scripts/remove-fixtures.sh` removes the directory and the env hook. `bash tests/fixtures-check.sh` checks all of it.
- Config (contact, site URL, author): `src/config/site.mjs` only. Open items: `PRELAUNCH-CHECKLIST.md`.
