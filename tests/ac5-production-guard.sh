#!/usr/bin/env bash
# TJD-643 AC5 red-before, on the ONE fixture guard (TJD-645, src/content.config.mjs; no second implementation):
# `TJ_SITE_ENV=production npm run build` exits non-zero when a content entry has fixture: true, or only a title
# starting "[TEST]" (no flag), and names the file; 0 on the clean tree with the 15 real posts.
# Runs in a temp copy of the tree (node_modules symlinked) so the working tree is never changed.
set -uo pipefail
cd "$(dirname "$0")/.."
fails=0
ok() { echo "PASS $1"; }
no() { echo "FAIL $1"; fails=$((fails + 1)); }
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
fresh() {
  rm -rf "$tmp/t"; mkdir "$tmp/t"
  tar --exclude=./node_modules --exclude=./dist --exclude=./.astro --exclude=./.git -cf - . | tar -xf - -C "$tmp/t"
  ln -s "$PWD/node_modules" "$tmp/t/node_modules"
}
prod() { (cd "$tmp/t" && TJ_SITE_ENV=production npm run build >"$tmp/build.log" 2>&1); }

fresh
prod && [ "$(ls "$tmp/t/dist/posts" | wc -l | tr -d ' ')" = 15 ] && ok "clean tree: production build rc 0, 15 post pages" || no "clean tree: production build"

fresh
printf -- '---\ntitle: "Flag only"\ndate: 2026-01-01\ntags: [agents]\nexcerpt: "x"\nfixture: true\n---\nplaceholder\n' >"$tmp/t/src/content/posts/zz-flag.md"
if prod; then no "fixture: true: production build exited 0"
else grep -q 'refused: fixture entr.*zz-flag.md' "$tmp/build.log" && ok "fixture: true: production rc non-zero, names the file" || no "fixture: true: file not named"; fi

fresh
printf -- '---\ntitle: "[TEST] Title only"\ndate: 2026-01-01\ntags: [agents]\nexcerpt: "x"\n---\nplaceholder\n' >"$tmp/t/src/content/posts/zz-title.md"
if prod; then no "[TEST] title: production build exited 0"
else grep -q 'refused: fixture entr.*zz-title.md' "$tmp/build.log" && ok "[TEST] title (no flag): production rc non-zero, names the file" || no "[TEST] title: file not named"; fi

echo "ac5-production-guard: $fails failure(s)"
[ "$fails" -eq 0 ]
