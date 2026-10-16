#!/usr/bin/env bash
# TJD-641: regenerate src/data/proof-of-loop.json from live Jira (read-only). Numbers are counted, never typed.
# Uses TJGraph-Local/jira.sh search; every JQL string and generated_at are written into the JSON.
# Usage: bash scripts/proof-of-loop.sh [out.json]   (JIRA_SH overrides the helper path)
set -euo pipefail
cd "$(dirname "$0")/.."
JIRA_SH="${JIRA_SH:-$HOME/MyAgentLand/TJGraph-Local/jira.sh}"
OUT="${1:-src/data/proof-of-loop.json}"
MAX=5000

Q_SHIPPED='project = TJD AND labels = devlead AND status = Done'
Q_REVIEWED='project = TJD AND labels = devlead AND status WAS "Ready for Merge"'
Q_HUMAN='project = TJD AND labels = devlead AND labels = rp-approved'
Q_LAST='project = TJD AND labels = devlead AND status = Done ORDER BY updated DESC'

count() { "$JIRA_SH" search "$1" "$MAX" | grep -c . || true; }
shipped="$(count "$Q_SHIPPED")"
reviewed="$(count "$Q_REVIEWED")"
human="$(count "$Q_HUMAN")"
last_key="$("$JIRA_SH" search "$Q_LAST" 1 | head -1 | cut -f1)"
[ -n "$last_key" ] || { echo "proof-of-loop: no Done ticket found" >&2; exit 3; }
last_updated="$("$JIRA_SH" get "$last_key" | python3 -c 'import json,sys; print(json.load(sys.stdin)["updated"])')"

SHIPPED="$shipped" REVIEWED="$reviewed" HUMAN="$human" LAST_KEY="$last_key" LAST_UPDATED="$last_updated" \
Q_SHIPPED="$Q_SHIPPED" Q_REVIEWED="$Q_REVIEWED" Q_HUMAN="$Q_HUMAN" Q_LAST="$Q_LAST" python3 - "$OUT" <<'PY'
import json, os, sys, datetime
e = os.environ
doc = {
  "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
  "source": "TJGraph-Local/jira.sh search (read-only), project TJD",
  "metrics": [
    {"id": "shipped", "label": "Changes shipped by agents", "value": int(e["SHIPPED"]),
     "definition": "Agent-built tickets closed Done", "jql": e["Q_SHIPPED"]},
    {"id": "reviewed", "label": "Passed an independent QA review", "value": int(e["REVIEWED"]),
     "definition": "Agent-built tickets a separate QA agent run passed (reached Ready for Merge)", "jql": e["Q_REVIEWED"]},
    {"id": "human", "label": "Human approved", "value": int(e["HUMAN"]),
     "definition": "Agent-built tickets carrying RP's rp-approved label", "jql": e["Q_HUMAN"]},
  ],
  "last_change": {"key": e["LAST_KEY"], "updated": e["LAST_UPDATED"], "jql": e["Q_LAST"]},
}
with open(sys.argv[1], "w") as f:
    json.dump(doc, f, indent=2)
    f.write("\n")
print("proof-of-loop: wrote %s shipped=%s reviewed=%s human=%s last=%s" % (sys.argv[1], e["SHIPPED"], e["REVIEWED"], e["HUMAN"], e["LAST_KEY"]))
PY
