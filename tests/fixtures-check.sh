#!/usr/bin/env bash
# TJD-645 fixture archive checks. No network. Exit 0 = all pass. Runs the builds in a temp copy of the tree
# (node_modules symlinked) so the working tree is never changed.
#   1 TJ_SITE_FIXTURES=1 build: 40 +/- 2 [TEST] posts on Insights, archive pages, tag/year chips, RSS newest first
#   2 default build: 0 [TEST] in dist/, deny-list passes
#   3 TJ_SITE_ENV=production: a fixture forced into src/content/posts -> non-zero naming the file; without it -> 0
#   4 scripts/remove-fixtures.sh: no fixture dir, no hook; the three builds above then behave with 0 fixtures
set -uo pipefail
cd "$(dirname "$0")/.."
fails=0
ok() { echo "PASS $1"; }
no() { echo "FAIL $1"; fails=$((fails + 1)); }
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
mkdir "$tmp/t"
tar --exclude=./node_modules --exclude=./dist --exclude=./.astro --exclude=./.git -cf - . | tar -xf - -C "$tmp/t"
ln -s "$PWD/node_modules" "$tmp/t/node_modules"
T="$tmp/t"
build() { (cd "$T" && rm -rf dist && env "$@" npm run build >"$tmp/build.log" 2>&1); }
tests_in() { grep -rIFo -- '[TEST]' "$T/dist" 2>/dev/null | wc -l | tr -d ' '; }
posts_on_insights() { grep -o 'class="card post-item"' "$T/dist/insights/index.html" | wc -l | tr -d ' '; }

check_fixture_build() { # $1 = expected count mode: "40" or "0"
  build TJ_SITE_FIXTURES=1 || { no "fixture build rc"; return; }
  python3 - "$T/dist" "$1" <<'PY' && ok "fixture build ($1 mode): Insights/archive/filters/RSS" || no "fixture build ($1 mode)"
import re, sys, os, glob, email.utils as eu
d, mode = sys.argv[1], sys.argv[2]
ins = open(f"{d}/insights/index.html").read() if os.path.exists(f"{d}/insights/index.html") else ""
items = re.findall(r'<li class="card post-item".*?</li>', ins, re.S)
test_items = [i for i in items if "[TEST]" in i]
rss = open(f"{d}/rss.xml").read()
titles = re.findall(r"<item><title>(.*?)</title>", rss)
dates = [eu.parsedate_to_datetime(x) for x in re.findall(r"<pubDate>(.*?)</pubDate>", rss)]
assert all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1)), "rss order"
arch = sorted(glob.glob(f"{d}/insights/archive/*/index.html"))
arch_n = sum(len(re.findall(r'class="card post-item"', open(p).read())) for p in arch)
if mode == "0":
    assert not test_items and not [t for t in titles if "[TEST]" in t] and not glob.glob(f"{d}/posts/test-fixture-*"), "fixtures present"
    sys.exit(0)
n = len(test_items)
assert 38 <= n <= 42, f"insights count {n}"
assert len([t for t in titles if t.startswith("[TEST]")]) == n, "rss count"
assert arch_n == len(items) and len(arch) >= 2, f"archive pages {len(arch)} items {arch_n}"
assert len(glob.glob(f"{d}/posts/test-fixture-*/index.html")) == n, "post pages"
tags = {}; years = {}
for i in test_items:
    for t in re.search(r'data-tags="([^"]*)"', i).group(1).split("|"): tags[t] = tags.get(t, 0) + 1
    y = re.search(r'data-year="(\d+)"', i).group(1); years[y] = years.get(y, 0) + 1
for t in ["Governance", "Agents", "Observability", "Engineering", "Data and people"]:
    assert tags.get(t, 0) > 0 and f'data-tag="{t}"' in ins, f"tag {t}"
for y in ["2024", "2025", "2026"]:
    assert years.get(y, 0) > 0 and f'data-year="{y}">' in ins, f"year {y}"
assert all("Test fixture" in i for i in test_items), "fixture label"
print(f"  insights={n} rss={len(titles)} archive_pages={len(arch)} tags={tags} years={years}")
PY
}

check_default_and_prod() {
  build || { no "default build rc"; return; }
  [ "$(tests_in)" = 0 ] && ok "default build: 0 [TEST] in dist" || no "default build: [TEST] in dist ($(tests_in))"
  bash scripts/prelaunch-check.sh "$T/dist" >/dev/null && ok "default build: deny-list passes" || no "default build: deny-list"
  local src; src="$(ls "$T"/src/content/fixtures/*.md 2>/dev/null | head -1)"
  if [ -z "$src" ]; then src="$tmp/forced.md"; printf -- '---\ntitle: "[TEST] forced"\ndate: 2025-01-01\ntags: ["Agents"]\ndescription: "forced"\nfixture: true\n---\nforced\n' >"$src"; fi
  cp "$src" "$T/src/content/posts/forced-fixture.md"
  if build TJ_SITE_ENV=production TJ_SITE_FIXTURES=1; then no "production with forced fixture exited 0"
  elif grep -q 'refused: fixture entr.*src/content/posts/forced-fixture.md' "$tmp/build.log"; then ok "production + forced fixture: non-zero, names the file"
  else no "production + forced fixture: message does not name the file"; fi
  rm -f "$T/src/content/posts/forced-fixture.md"
  build TJ_SITE_ENV=production TJ_SITE_FIXTURES=1 && [ "$(tests_in)" = 0 ] && ok "production build without fixture entry: rc 0, 0 [TEST]" || no "production build without fixture entry"
}

echo "== with fixtures"
check_fixture_build 40
check_default_and_prod
echo "== after scripts/remove-fixtures.sh"
(cd "$T" && bash scripts/remove-fixtures.sh >"$tmp/rm.log" 2>&1) && [ ! -e "$T/src/content/fixtures" ] && ok "remove-fixtures: no fixture dir" || no "remove-fixtures"
grep -rqE 'TJ_SITE_FIXTURES|FIXTURES-HOOK' "$T/src" "$T/Dockerfile" "$T/scripts/prelaunch-check.sh" && no "hook left after removal" || ok "remove-fixtures: no hook left"
check_fixture_build 0
check_default_and_prod

echo "fixtures-check: $fails failure(s)"
[ "$fails" -eq 0 ]
