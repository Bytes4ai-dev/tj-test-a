# Bytes4AI website (tj-test-a)

Astro static site for the rv-demo project `bytes4ai-site` (TJD-640 / TJD-641 Phase 1).

- `npm ci && npm run build` → `dist/`
- `bash tests/site-check.sh` → build + static checks (tokens, share previews, Experience facts, Platform data, deny-list)
- `bash scripts/prelaunch-check.sh [dist]` → deny-list (phone, personal email, secret-looking tokens, `[TEST]`)
- `bash scripts/platform-status.sh` / `bash scripts/proof-of-loop.sh` → regenerate `src/data/*.json` from Jira (read-only; needs TJGraph-Local `jira.sh`)
- `python3 scripts/make-og.py` → redraw `public/og/*.png`
- Container: `docker build .` serves on `$PORT` (default 8080) as non-root; `GET /healthz` → 200. `cloudbuild.yaml` is unchanged (TJD-191/546 contract).
- Config (contact, site URL, author): `src/config/site.mjs` only. Open items: `PRELAUNCH-CHECKLIST.md`.
