#!/usr/bin/env bash
# TJD-641: regenerate src/data/platform-status.json from live Jira (read-only).
# Uses TJGraph-Local/jira.sh search; the JQL and generated_at are written into the JSON.
# Usage: bash scripts/platform-status.sh [out.json]   (JIRA_SH overrides the helper path)
set -euo pipefail
cd "$(dirname "$0")/.."
JIRA_SH="${JIRA_SH:-$HOME/MyAgentLand/TJGraph-Local/jira.sh}"
OUT="${1:-src/data/platform-status.json}"
IN=scripts/platform-capabilities.json

keys="$(python3 -c 'import json,sys; print(",".join(sorted({k for c in json.load(open(sys.argv[1]))["cards"] for k in c["keys"]})))' "$IN")"
jql="project = TJD AND key in ($keys) ORDER BY key ASC"
tsv="$("$JIRA_SH" search "$jql" 200)"
[ -n "$tsv" ] || { echo "platform-status: empty Jira result" >&2; exit 3; }

JQL="$jql" TSV="$tsv" python3 - "$IN" "$OUT" <<'PY'
import json, os, sys, datetime
cards = json.load(open(sys.argv[1]))["cards"]
status = {}
for line in os.environ["TSV"].splitlines():
    parts = line.split("\t")
    if len(parts) >= 2:
        status[parts[0]] = parts[1]
out = []
for c in cards:
    st = {k: status.get(k) for k in c["keys"]}
    if any(v is None for v in st.values()):
        sys.exit("platform-status: missing Jira key in result: %s" % st)
    if all(v == "Done" for v in st.values()):
        chip, cls = "Working in DEV", "working"
    elif all(v == "To Do" for v in st.values()):
        chip, cls = "Planned", "planned"
    else:
        chip, cls = "In build", "build"
    filt = chip
    if c.get("override"):
        chip, cls = c["override"]["chip"], c["override"]["class"]
    out.append({"id": c["id"], "title": c["title"], "body": c["body"], "keys": c["keys"],
                "jira_status": st, "filter": filt, "chip": chip, "chip_class": cls})
doc = {"generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
       "source": "TJGraph-Local/jira.sh search (read-only)", "jql": os.environ["JQL"], "cards": out}
with open(sys.argv[2], "w") as f:
    json.dump(doc, f, indent=2)
    f.write("\n")
print("platform-status: wrote %s (%d cards)" % (sys.argv[2], len(out)))
PY
