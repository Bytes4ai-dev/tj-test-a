#!/usr/bin/env bash
# TJD-641 + TJD-643 + TJD-644 static checks on a fresh build. No network, no Jira. Exit 0 = all pass.
#   tokens file holds only the six colors + three fonts; every page has OG/twitter tags and its og:image exists;
#   Experience strip == data/experience.json == TJD-640 facts; Platform banner + JSON-sourced numbers;
#   checklist not in dist; deny-list red-before (planted phone number) then clean.
set -uo pipefail
cd "$(dirname "$0")/.."
fails=0
ok() { echo "PASS $1"; }
no() { echo "FAIL $1"; fails=$((fails + 1)); }

[ "${SKIP_BUILD:-0}" = 1 ] || npm run build >/dev/null 2>&1 || { echo "FAIL build"; exit 1; }

# 1. design tokens
colors="$(grep -oiE '#[0-9a-f]{6}' src/styles/tokens.css | tr a-f A-F | sort -u | tr '\n' ' ')"
[ "$colors" = "#0B6B63 #10141A #7FD6CB #E6E9E2 #F2B66B #F3F4F0 " ] && ok "tokens colors" || no "tokens colors: $colors"
fonts="$(grep -oE "'(Bricolage Grotesque|IBM Plex Sans|IBM Plex Mono)'" src/styles/tokens.css | sort -u | wc -l | tr -d ' ')"
[ "$fonts" = 3 ] && ok "tokens fonts" || no "tokens fonts"
grep -rnoiE '#[0-9a-f]{3,8}\b' src --include=*.astro --include=*.css | grep -v 'src/styles/tokens.css' | grep -q . && no "hex color outside tokens" || ok "no hex outside tokens"

# 2. pages + share previews (TJD-641 pages + TJD-643 post pages); og:url/og:image absolute on the site URL
SITE="$(node -e "import('./src/config/site.mjs').then(m => console.log(m.site.url.replace(/\/\$/, '')))")"
pages="index about/index platform/index insights/index timeline/index"
for f in src/content/posts/*.md; do pages="$pages posts/$(basename "$f" .md)/index"; done
for f in src/content/retrospectives/*.md; do pages="$pages timeline/$(basename "$f" .md)/index"; done  # TJD-644
for p in $pages; do
  f="dist/$p.html"
  [ -f "$f" ] || { no "page $p missing"; continue; }
  miss=""
  for t in 'property="og:title"' 'property="og:description"' 'property="og:image"' 'property="og:url"' 'name="twitter:card"'; do
    grep -q "$t" "$f" || miss="$miss $t"
  done
  url="$(grep -o 'property="og:url" content="[^"]*"' "$f" | sed 's/.*content="//; s/"$//')"
  imgurl="$(grep -o 'property="og:image" content="[^"]*"' "$f" | sed 's/.*content="//; s/"$//')"
  case "$url" in "$SITE"/*) ;; *) miss="$miss og:url-not-on-site($url)";; esac
  case "$imgurl" in "$SITE"/*) ;; *) miss="$miss og:image-not-on-site($imgurl)";; esac
  img="${imgurl#"$SITE"}"
  [ -f "dist$img" ] || miss="$miss og:image-file($img)"
  case "$p" in posts/*) grep -q 'property="og:type" content="article"' "$f" || miss="$miss og:type-article"
    [ "$img" = "/og/${p%/index}.png" ] || miss="$miss own-og-image";; esac
  [ -z "$miss" ] && ok "page $p meta" || no "page $p:$miss"
done
grep -rlq 'localhost' dist --include=*.html --include=*.xml && no "localhost URL in dist" || ok "no localhost URL in dist"

# 2b. TJD-643 post template, Insights, Timeline shell, RSS
n_posts="$(ls src/content/posts/*.md | wc -l | tr -d ' ')"
[ "$n_posts" = 15 ] && ok "15 posts migrated" || no "posts: $n_posts"
python3 - <<'PY2' && ok "post template parts" || no "post template parts"
import glob, re
for f in glob.glob("dist/posts/*/index.html"):
    s = open(f).read()
    for need in ('<h1>', 'class="label"', 'Ravi Singh', '<time datetime="', ' min read', 'class="post-hero"', 'class="post-body"', 'href="/#readiness"'):
        assert need in s, (f, need)
PY2
python3 - <<'PY2' && ok "Insights: 15 cards, 5 tag chips, count, body search text" || no "Insights page"
import re
s = open("dist/insights/index.html").read()
items = re.findall(r'<li class="card post-item".*?</li>', s, re.S)
assert len(items) == 15, len(items)
chips = re.findall(r'data-tag="([^"]*)"', s)
assert chips == ["", "Governance", "Agents", "Observability", "Engineering", "Data and people"], chips
assert all(re.search(r'data-tags="[^"]+"', i) for i in items), "post without an Insights tag"
assert 'aria-live="polite" data-count' in s and ">15 posts<" in s and 'type="search"' in s
assert "honest caveat" in s, "body text not in search index"
assert not re.search(r"fetch\(|XMLHttpRequest|sendBeacon|WebSocket|import\(", s)
PY2
python3 - <<'PY2' && ok "Timeline shell: title + 2024/2025/2026 chips" || no "Timeline shell"
s = open("dist/timeline/index.html").read()
assert "How we got here 2024-2026" in s
assert all('data-year="%s" aria-pressed' % y in s for y in ("2024", "2025", "2026"))
PY2
python3 - <<'PY2' && ok "internal links resolve" || no "internal links resolve"
import glob, os, re
bad = []
for f in glob.glob("dist/**/*.html", recursive=True):
    for h in re.findall(r'href="(/[^"#?]*)', open(f).read()):
        t = "dist" + h
        if not (os.path.isfile(t) or os.path.isfile(os.path.join(t, "index.html")) or t.endswith("/") and os.path.isfile(t + "index.html")):
            bad.append((f, h))
assert not bad, bad[:5]
PY2
python3 tests/rss-check.py dist "$SITE" >/dev/null && ok "rss.xml valid, 15 items newest first" || no "rss.xml"
python3 tests/retro-check.py dist >/dev/null && ok "TJD-644 retrospectives (retro-check.py: 5/4/3, claim-check, own SVGs, dates)" || no "retro-check.py"

# 3. experience strip text
want="$(python3 -c 'import json; d=json.load(open("src/data/experience.json")); print("\n".join(d["facts"]+[" · ".join(d["certs"])]))')"
got="$(python3 - <<'PY'
import re, html
s = open("dist/index.html").read()
m = re.search(r'id="experience".*?<ul>(.*?)</ul>', s, re.S)
print("\n".join(html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<li[^>]*>(.*?)</li>", m.group(1), re.S)))
PY
)"
[ "$want" = "$got" ] && ok "experience strip == experience.json" || no "experience strip differs"
for fact in "125M+ patient records moved to cloud with zero customer impact" "30-40% lower analytics operating cost" "~95% of requests resolved by a production AI system with no LLM on the hot path"; do
  grep -qF "$fact" src/data/experience.json || no "experience.json missing TJD-640 fact: $fact"
done

# 4. platform honesty + JSON-sourced numbers
grep -q 'We do not claim product-market fit, certified compliance or proven production scale' dist/platform/index.html && ok "platform banner" || no "platform banner"
grep -q 'pending supervised drill (TJD-99)' dist/platform/index.html && ok "freeze/stop pending chip" || no "freeze/stop chip"
python3 - <<'PY' && ok "platform numbers from JSON" || no "platform numbers from JSON"
import json, sys
s = open("dist/platform/index.html").read()
loop = json.load(open("src/data/proof-of-loop.json")); st = json.load(open("src/data/platform-status.json"))
assert loop["generated_at"] and st["generated_at"] and all(m["jql"] for m in loop["metrics"]) and st["jql"]
for m in loop["metrics"]:
    assert ">%d<" % m["value"] in s, m
for c in st["cards"]:
    assert c["chip"] in s and c["title"] in s, c
PY
grep -q 'kiteworks.com/cybersecurity-risk-management/2026-data-security-forecast' dist/index.html && ok "gap meter source link" || no "gap meter source link"

# 5. checklist + deny-list
[ -f PRELAUNCH-CHECKLIST.md ] && [ ! -e dist/PRELAUNCH-CHECKLIST.md ] && ok "checklist at root, not in dist" || no "checklist placement"
tmp="$(mktemp -d)"; cp -R dist "$tmp/d"; echo '<p>Call 817-555-0142</p>' >> "$tmp/d/index.html"
bash scripts/prelaunch-check.sh "$tmp/d" >/dev/null 2>&1 && no "deny-list red-before (planted phone passed)" || ok "deny-list red-before (planted phone -> non-zero)"
rm -rf "$tmp"
bash scripts/prelaunch-check.sh dist >/dev/null && ok "deny-list clean on build" || no "deny-list on build"

echo "site-check: $fails failure(s)"
[ "$fails" -eq 0 ]
