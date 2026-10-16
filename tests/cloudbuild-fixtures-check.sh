#!/usr/bin/env bash
# TJD-649 cloudbuild.yaml fixture build-arg checks. Exit 0 = all pass.
#   1 static: the build step passes --build-arg TJ_SITE_FIXTURES=${_TJ_SITE_FIXTURES} once; substitution default is ""
#   2 docker: the build step's own args, run on a git-archive copy of HEAD with _TJ_SITE_FIXTURES "" -> 0 fixture
#     posts in the image, "1" -> one post per src/content/fixtures/*.md (40)
#   3 docker: the "" image serves / and /platform/ 200, /platform -> relative Location, /healthz "ok"
# Docker checks need a reachable daemon (colima: DOCKER_HOST=unix://$HOME/.colima/default/docker.sock); without one
# they are SKIPPED, or FAIL when REQUIRE_DOCKER=1. Images are tagged tjd649-check:* and removed on exit.
set -uo pipefail
cd "$(dirname "$0")/.."
fails=0
ok() { echo "PASS $1"; }
no() { echo "FAIL $1"; fails=$((fails + 1)); }

# Prints the build step args as JSON, substituted with _TJ_SITE_FIXTURES=$1 (cloudbuild.yaml's own substitution form).
build_args() {
  python3 - "$1" <<'PY'
import json, re, sys
s = open("cloudbuild.yaml").read()
m = re.search(r"- id: build\n\s+name: gcr\.io/cloud-builders/docker\n\s+args: (\[.*\])\n", s)
args = json.loads(m.group(1))
subs = {"_TJ_SITE_FIXTURES": sys.argv[1], "_TJ_REPO": "tjd649-check", "COMMIT_SHA": "fx" + (sys.argv[1] or "none")}
print(json.dumps([re.sub(r"\$\{(\w+)\}", lambda g: subs[g.group(1)], a) for a in args]))
PY
}

# 1 static
python3 - <<'PY' && ok "static: build-arg + substitution default empty" || no "static: build-arg + substitution default empty"
import json, re
s = open("cloudbuild.yaml").read()
m = re.search(r"- id: build\n\s+name: gcr\.io/cloud-builders/docker\n\s+args: (\[.*\])\n", s)
args = json.loads(m.group(1))
assert args.count("--build-arg") == 1, args
i = args.index("--build-arg")
assert args[i + 1] == "TJ_SITE_FIXTURES=${_TJ_SITE_FIXTURES}", args
assert s.count("TJ_SITE_FIXTURES") == 3, "TJ_SITE_FIXTURES outside the build step / substitution"
sub = s[s.index("\nsubstitutions:\n"):]
assert re.search(r'\n  _TJ_SITE_FIXTURES: ""\n', sub), "substitution default not empty"
PY

# 2 + 3 docker
if [ -z "${DOCKER_HOST:-}" ] && [ -S "$HOME/.colima/default/docker.sock" ]; then
  export DOCKER_HOST="unix://$HOME/.colima/default/docker.sock"
fi
if ! docker info >/dev/null 2>&1; then
  if [ "${REQUIRE_DOCKER:-0}" = 1 ]; then no "docker daemon reachable"; else echo "SKIP docker checks (no daemon)"; fi
  echo "fails=$fails"; [ "$fails" -eq 0 ]; exit
fi
tmp="$(mktemp -d)"; cid=""
cleanup() { [ -n "$cid" ] && docker rm -f "$cid" >/dev/null 2>&1; docker rmi -f tjd649-check/app:fxnone tjd649-check/app:fx1 >/dev/null 2>&1; rm -rf "$tmp"; }
trap cleanup EXIT
git archive HEAD | tar -xf - -C "$tmp"
want="$(find src/content/fixtures -name '*.md' -type f | wc -l | tr -d ' ')"
count() { docker run --rm --entrypoint sh "$1" -c 'ls -d /usr/share/nginx/html/posts/test-fixture-* 2>/dev/null | wc -l' | tr -d ' '; }
for v in "" 1; do
  tag="tjd649-check/app:fx${v:-none}"
  args="$(build_args "$v")"
  if ! (cd "$tmp" && python3 -c 'import json,sys,subprocess; sys.exit(subprocess.call(["docker"] + json.loads(sys.argv[1])))' "$args") >"$tmp.build${v:-none}.log" 2>&1; then
    no "docker build _TJ_SITE_FIXTURES='$v' (log $tmp.build${v:-none}.log)"; continue
  fi
  n="$(count "$tag")"
  if [ -z "$v" ]; then exp=0; else exp="$want"; fi
  [ "$n" = "$exp" ] && ok "image _TJ_SITE_FIXTURES='$v': $n fixture posts (want $exp)" || no "image _TJ_SITE_FIXTURES='$v': $n fixture posts (want $exp)"
done
rm -f "$tmp".build*.log

port="${CHECK_PORT:-9649}"
cid="$(docker run -d -e PORT=8080 -p "127.0.0.1:$port:8080" tjd649-check/app:fxnone 2>/dev/null)" || { no "run default image"; echo "fails=$fails"; exit 1; }
for _ in $(seq 1 30); do curl -fsS "http://127.0.0.1:$port/healthz" >/dev/null 2>&1 && break; sleep 1; done
code() { curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$port$1"; }
[ "$(curl -s "http://127.0.0.1:$port/healthz")" = ok ] && ok "default image /healthz ok" || no "default image /healthz"
[ "$(code /)" = 200 ] && ok "default image / 200" || no "default image / $(code /)"
[ "$(code /platform/)" = 200 ] && ok "default image /platform/ 200" || no "default image /platform/ $(code /platform/)"
loc="$(code /platform)|$(curl -sI "http://127.0.0.1:$port/platform" | tr -d '\r' | sed -n 's/^[Ll]ocation: //p')"
case "$loc" in "301|/platform/") ok "default image /platform -> 301 relative Location /platform/" ;; *) no "default image /platform redirect: $loc" ;; esac

echo "fails=$fails"
[ "$fails" -eq 0 ]
