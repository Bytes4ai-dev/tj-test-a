# Pre-launch checklist (Bytes4AI website v1: TJD-641 Phase 1, TJD-643 Phase 2)

This file stays at the repo root and is never copied into `dist/` (`scripts/prelaunch-check.sh` fails if it is).
Every item below must be resolved by RP (or confirmed as-is) before the site goes to a public domain.

## Waiting on RP
- [ ] **Contact.** `src/config/site.mjs` → `contact.mode` is `placeholder`. Supply a business email (`mailto`) or a hosted form URL (`form`). No phone number, no personal email.
- [ ] **Photo.** About uses an initials avatar ("RS"). Supply a photo if wanted.
- [ ] **Domain.** `site.url` defaults to the DEV URL `https://rvdemo-app-crnwvkk4ua-uc.a.run.app` (TJD-643; override with `SITE_URL` at build). og:url / og:image / RSS links use it; set it to the real domain before launch. Ownership of bytes4ai.com is still open.
- [ ] **Publish dates.** Every migrated post keeps the donor's own `date:` (2026-09-21 to 2026-09-29); none is backdated. Confirm before launch; a post without a date would get its go-live date.
- [ ] **Typos.** The 15 posts are byte-for-byte copies of the donor files (`tests/posts-diff.py`). Any typo fix needs RP's approval on TJD-640 first.
- [ ] **Post-template slots** (`src/data/post-extras.json`): pull quote, "What to do this week" callout, Sources list and chart/diagram are empty for every post and so not shown. Supply them per post if wanted (a pull quote must be an exact sentence from the post).
- [ ] **Unpublished drafts.** Location still to be supplied (Phase 3).
- [ ] **[TEST] fixture archive (TJD-645).** DEV builds with `TJ_SITE_FIXTURES=1` show ~40 placeholder "[TEST]" posts. Before launch run `bash scripts/remove-fixtures.sh` (deletes `src/content/fixtures/` and the env hook) and build with `TJ_SITE_ENV=production`, which fails on any fixture entry.

## Platform statuses (re-check against Jira on the day of publishing)
Regenerate with `bash scripts/platform-status.sh` (writes `src/data/platform-status.json` with JQL + generated_at). Status at build:
- [ ] Merge gate (TJD-38) — Working in DEV
- [ ] Budgets and policy (TJD-16) — Working in DEV
- [ ] Customer plane baseline (TJD-191) — Working in DEV
- [ ] Grounded read-only chat (TJD-85) — Working in DEV
- [ ] Builder PRs on your repo (TJD-545, TJD-434) — Planned
- [ ] Signed policy snapshots (TJD-97) — Planned
- [ ] Freeze and stop (TJD-99) — pending supervised drill (TJD-99). Do not claim a tested kill switch until TJD-99 Part B passes.

## Proof of loop
- [ ] Regenerate with `bash scripts/proof-of-loop.sh` the day of publishing; counts and JQL live in `src/data/proof-of-loop.json`.
- [ ] Confirm the metric definitions (inferred by Dev, TJD-641): "shipped" = devlead tickets Done; "independent QA review" = devlead tickets that reached Ready for Merge (QA PASS by a separate agent run; not necessarily a different model); "human approved" = devlead tickets with the `rp-approved` label.

## Inferred or placeholder content (written by Dev, not RP's words; review or replace)
- [ ] Hero sub-line: "Most teams can watch their agents. Far fewer can stop one. We help close that gap."
- [ ] Gap meter "Where we help you get" view: goal text, no number claimed.
- [ ] TejasLand product block text on Home.
- [ ] One-line descriptions of the five services.
- [ ] Readiness check: the four questions, the scoring bands and the result texts.
- [ ] Latest insights ×3 on Home: the three newest real posts (title, excerpt, date from the post files).
- [ ] Insights tags (TJD-643): the five chips (Governance, Agents, Observability, Engineering, Data and people) are mapped from each post's own donor tags in `src/lib/posts.mjs` (governance/safety/containment/security → Governance; agents → Agents; observability/evals → Observability; engineering/infrastructure/reliability → Engineering; data/privacy → Data and people; ai/opinion/critical → none). The post files keep their donor tags. Confirm the mapping.
- [ ] Timeline page: layout with year chips and placeholder text (content = Phase 3).
- [ ] Post hero illustration: an original geometric bar mark drawn from the post id (no stock or AI imagery). Per-post share images `public/og/posts/*.png` likewise (`scripts/make-og.py`).
- [ ] About text: built only from the TJD-640 resume facts; confirm wording.
- [ ] Capability card descriptions on Platform (`scripts/platform-capabilities.json`).
- [ ] Share images (`public/og/*.png`, made by `scripts/make-og.py`): simple original geometric shapes in the theme colors; no text.
- [ ] Footer line "Built and run on DEV through TejasLand."

## Sources
- Gap meter 58% / 40%: Kiteworks, 2026 Data Security Forecast — https://www.kiteworks.com/cybersecurity-risk-management/2026-data-security-forecast-ai-governance-predictions/ (self-reported vendor survey).
