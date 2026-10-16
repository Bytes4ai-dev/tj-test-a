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

## Timeline retrospectives (TJD-644, Phase 3)
Twelve posts in `src/content/retrospectives/`, written by Dev from public sources in October 2026. They are **not in RP's name**: the byline is "Bytes4AI" (`src/data/retrospectives.json`). RP reviews the words before launch.
- [ ] **Byline and voice.** Confirm "Bytes4AI" as the byline, or put RP's name on the ones RP approves.
- [ ] **Publish date.** One value for all 12: `published` in `src/data/retrospectives.json` = the merge day (2026-10-16). If they go live on another day, change that value. Each page also says "Written in 2026, looking back at <year>".
- [ ] **Sources.** `node scripts/claim-check.mjs dist` lists every paragraph with a number or a named study and fails if one has no link. Dev fetched each source page on 2026-10-16 and found the cited figure in the page text, except where marked "not fetched" below.
- [ ] **Charts and illustrations.** All 24 SVGs are drawn by `scripts/make-retro-visuals.py` (stdlib, theme colors). One motif per tag: Governance rings + gate bar, Agents connected nodes, Observability pulse line, Engineering stacked blocks, Data and people dot grid. Confirm the style.

Per-retrospective claims to confirm (U = unverified by Dev's fetch; everything else was found in the source text):
- [ ] RAG goes mainstream: Menlo 31% → 51% (vendor survey); Anthropic 49% / 67% are Anthropic's own tests; GraphRAG publish date (Microsoft page says 13 Feb 2024).
- [ ] Open-weight models close the gap: AI Index "8% to 1.7% on some benchmarks" (the post's chart labels these "early 2024 / early 2025", Dev's reading of "in a single year"); Llama 3.1 405B / 15T tokens (July 2024 date: Dev's knowledge, U); DeepSeek-V3 2.788M H800 GPU hours (December 2024 date: arXiv id 2412, U).
- [ ] EU AI Act: dates and Article 99 fines from artificialintelligenceact.eu (unofficial explorer; EUR-Lex is the official text). Any later amendment (e.g. Commission simplification proposals) to the 2026/2027 dates is NOT covered: re-check before launch.
- [ ] Reasoning models: AIME 12% / 74% / 83% / 93% from OpenAI "Learning to reason with LLMs" — **U: openai.com returns 403 to scripts**, figures from Dev's knowledge of that page; o1 "September 2024" U. ARC o3 75.7% / 87.5% / 172x verified.
- [ ] MCP arrives: "November 2024" launch month U (Anthropic page undated in fetch); 10,000+ servers and 97M+ monthly SDK downloads verified (Dec 2025 post).
- [ ] Agent hype year: Gartner ">40% canceled by end of 2027", the three reasons and "agent washing" — **U: gartner.com returns 403 to scripts**; headline matches the press-release URL. METR 19% verified.
- [ ] Vibe coding: Karpathy quote verified (post date February 2025 U); METR 16 devs / 246 issues / 19% / 24% / 20% verified (METR now marks these results out of date, said in the post); Veracode 45% verified.
- [ ] Prompt injection: OWASP LLM01:2025 verified; lethal trifecta 16 June 2025 verified; CVE-2025-32711 text and CVSS 9.3 from the CVE record API (published 2025-06-11).
- [ ] AI regulation bites: EU dates verified; GPAI Code of Practice published 10 July 2025 verified; Colorado SB25B-004 delay to 30 June 2026, approved 28 Aug 2025, verified.
- [ ] Shadow AI: Microsoft WTI 75% / 78% verified; IBM one in five, $670,000, 13%, 97%, 63% verified (IBM newsroom, 30 July 2025).
- [ ] Governance-containment gap: Kiteworks 58% / 59% / 60% / 63% / 55% verified; chart shows "can terminate quickly" as 40% = 100% − 60% (Dev's derivation, same as the Home gap meter). Article 14 "stop button" wording verified.
- [ ] What's next: NIST AI RMF released 26 January 2023 verified (linked by DOI because the nist.gov URL trips the deny-list's secret pattern); TejasLand paragraph says "early product" and points to the Platform page; it claims no tested kill switch.
