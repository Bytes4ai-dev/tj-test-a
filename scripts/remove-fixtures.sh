#!/usr/bin/env bash
# TJD-645: the ONE switch that removes the DEV-only [TEST] fixture archive.
# Deletes src/content/fixtures/ and every "FIXTURES-HOOK-BEGIN ... FIXTURES-HOOK-END" block (the TJ_SITE_FIXTURES
# env hook in src/content.config.mjs, Dockerfile and scripts/prelaunch-check.sh). The production fixture guard stays.
# Idempotent. Exit 0 = tree has no fixture directory and no TJ_SITE_FIXTURES hook left.
# Usage: bash scripts/remove-fixtures.sh
set -euo pipefail
cd "$(dirname "$0")/.."
self="scripts/remove-fixtures.sh"

rm -rf src/content/fixtures
for f in $(grep -rlF 'FIXTURES-HOOK-BEGIN' --exclude-dir=node_modules --exclude-dir=dist --exclude-dir=.astro --exclude-dir=.git . | sed 's|^\./||'); do
  [ "$f" = "$self" ] && continue
  sed -i.bak '/FIXTURES-HOOK-BEGIN/,/FIXTURES-HOOK-END/d' "$f" && rm -f "$f.bak"
  echo "remove-fixtures: hook removed from $f"
done

[ ! -e src/content/fixtures ] || { echo "remove-fixtures: src/content/fixtures still present" >&2; exit 1; }
left="$(grep -rlE 'TJ_SITE_FIXTURES|FIXTURES-HOOK' src Dockerfile scripts 2>/dev/null | grep -v "^$self$" || true)"
[ -z "$left" ] || { echo "remove-fixtures: hook still referenced in: $left" >&2; exit 1; }
echo "remove-fixtures: done (no fixture directory, no TJ_SITE_FIXTURES hook)"
