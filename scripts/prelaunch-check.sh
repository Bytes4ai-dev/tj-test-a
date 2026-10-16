#!/usr/bin/env bash
# TJD-641 deny-list: exit non-zero if the built site (dist/ by default) contains a phone-number pattern,
# RP's personal email address, a secret-looking token, "[TEST]" or PRELAUNCH-CHECKLIST.md. Exit 0 when clean.
# The personal address is never written in the repo: pass it by env name PRELAUNCH_DENY_EMAIL (optional);
# any personal-mail-domain address (gmail/yahoo/outlook/hotmail/icloud) is refused regardless.
# Usage: bash scripts/prelaunch-check.sh [dir]
set -uo pipefail
DIR="${1:-dist}"
[ -d "$DIR" ] || { echo "prelaunch-check: no $DIR (run npm run build first)" >&2; exit 2; }
fail=0
hit() { echo "DENY $1:"; echo "$2" | head -5 | cut -c1-200; fail=1; }
scan() { grep -rIEno "$1" "$DIR" 2>/dev/null; }

r="$(scan '(\+?1[ .-]?)?\(?[2-9][0-9]{2}\)?[ .-][0-9]{3}[ .-][0-9]{4}')" && hit "phone number" "$r"
r="$(scan '[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail|icloud|aol|proton(mail)?)\.[a-z.]+')" && hit "personal email" "$r"
if [ -n "${PRELAUNCH_DENY_EMAIL:-}" ]; then
  r="$(grep -rIFnoi -- "$PRELAUNCH_DENY_EMAIL" "$DIR")" && hit "RP personal email" "$(echo "$r" | sed 's/:.*@/:<redacted>@/')"
fi
r="$(scan '(AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|gh[pousr]_[0-9A-Za-z]{30,}|xox[abprs]-[0-9A-Za-z-]{10,}|sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.)')" && hit "secret-looking token" "$r"
r="$(grep -rIFno -- '[TEST]' "$DIR")" && hit "[TEST] fixture marker" "$r"
[ -e "$DIR/PRELAUNCH-CHECKLIST.md" ] && hit "checklist in build" "$DIR/PRELAUNCH-CHECKLIST.md"

if [ "$fail" -ne 0 ]; then echo "prelaunch-check: FAIL ($DIR)"; exit 1; fi
echo "prelaunch-check: PASS ($DIR)"
