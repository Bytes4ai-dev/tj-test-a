# Pre-launch checklist (TJD-641, Bytes4AI website v1 Phase 1)

This file stays at the repo root and is never copied into `dist/` (`scripts/prelaunch-check.sh` fails if it is).
Every item below must be resolved by RP (or confirmed as-is) before the site goes to a public domain.

## Waiting on RP
- [ ] **Contact.** `src/config/site.mjs` → `contact.mode` is `placeholder`. Supply a business email (`mailto`) or a hosted form URL (`form`). No phone number, no personal email.
- [ ] **Photo.** About uses an initials avatar ("RS"). Supply a photo if wanted.
- [ ] **Domain.** `site.url` defaults to `http://localhost:8080` (override with `SITE_URL` at build). og:url / og:image use it, so set it to the DEV URL for the DEV deploy and to the real domain before launch. Ownership of bytes4ai.com is still open.
- [ ] **Unpublished drafts.** Location still to be supplied (Phase 3).

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
- [ ] Latest insights ×3: placeholders ("Insight N coming soon") until Phase 2 posts land.
- [ ] Insights and Timeline pages: layout with placeholder text.
- [ ] Post template (`/posts/sample/`): placeholder text and placeholder illustration.
- [ ] About text: built only from the TJD-640 resume facts; confirm wording.
- [ ] Capability card descriptions on Platform (`scripts/platform-capabilities.json`).
- [ ] Share images (`public/og/*.png`, made by `scripts/make-og.py`): simple original geometric shapes in the theme colors; no text.
- [ ] Footer line "Built and run on DEV through TejasLand."

## Sources
- Gap meter 58% / 40%: Kiteworks, 2026 Data Security Forecast — https://www.kiteworks.com/cybersecurity-risk-management/2026-data-security-forecast-ai-governance-predictions/ (self-reported vendor survey).
