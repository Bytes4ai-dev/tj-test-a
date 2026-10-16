#!/usr/bin/env python3
"""TJD-644 static checks on a built site (run npm run build first). No network. Exit 0 = all pass.
AC1  /timeline/ lists 12 retrospectives; data-year 2024/2025/2026 = 5/4/3; each has its own page.
AC2  scripts/claim-check.mjs passes on dist, and fails on a copy with one planted unsourced number (red-before).
AC3  every image on the 12 pages is a local SVG under /timeline/<id>/ that exists in public/ and is byte-identical to
     what scripts/make-retro-visuals.py draws; no external image URL; every chart has a figcaption naming its source.
AC4  each page shows the publish date from src/data/retrospectives.json (a 2026 date) and the "Written in 2026" note;
     no <time> or article:published_time on these pages starts with 2024 or 2025.
Usage: python3 tests/retro-check.py [dist]"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
dist = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist"))
fails = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f": {detail}"))
    if not cond:
        fails.append(name)


ids = sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(ROOT, "src/content/retrospectives/*.md")))
published = json.load(open(os.path.join(ROOT, "src/data/retrospectives.json")))["published"]

# AC1
tl = open(os.path.join(dist, "timeline/index.html")).read()
items = re.findall(r'<li class="card post-item timeline-item"[^>]*data-year="(\d{4})"', tl)
counts = {y: items.count(y) for y in ("2024", "2025", "2026")}
check("AC1 12 retrospectives on /timeline/", len(ids) == 12 and len(items) == 12, (len(ids), len(items)))
check("AC1 year counts 2024/2025/2026 = 5/4/3", counts == {"2024": 5, "2025": 4, "2026": 3}, counts)
check("AC1 chips All/2024/2025/2026", re.findall(r'<button type="button" data-year="([^"]*)" aria-pressed', tl) == ["", "2024", "2025", "2026"])
check("AC1 one page per retrospective", all(os.path.isfile(os.path.join(dist, "timeline", i, "index.html")) for i in ids))
check("AC1 timeline makes no requests", not re.search(r"fetch\(|XMLHttpRequest|sendBeacon|WebSocket|import\(", tl))

# AC2
r = subprocess.run(["node", os.path.join(ROOT, "scripts/claim-check.mjs"), dist], capture_output=True, text=True)
check("AC2 claim-check PASS on dist", r.returncode == 0, r.stdout[-300:])
tmp = tempfile.mkdtemp()
try:
    shutil.copytree(os.path.join(dist, "timeline"), os.path.join(tmp, "timeline"))
    f = os.path.join(tmp, "timeline", ids[0], "index.html")
    s = open(f).read().replace('<div class="post-body">', '<div class="post-body"><p>Planted: 42% of teams agree.</p>', 1)
    open(f, "w").write(s)
    r2 = subprocess.run(["node", os.path.join(ROOT, "scripts/claim-check.mjs"), tmp], capture_output=True, text=True)
    check("AC2 claim-check red-before (planted unsourced number -> rc 1)", r2.returncode == 1 and "UNSOURCED" in r2.stdout, r2.returncode)
finally:
    shutil.rmtree(tmp)

# AC3
r3 = subprocess.run([sys.executable, os.path.join(ROOT, "scripts/make-retro-visuals.py"), "--check"], capture_output=True, text=True)
check("AC3 committed SVGs == make-retro-visuals.py output", r3.returncode == 0, r3.stdout[-300:])
for i in ids:
    s = open(os.path.join(dist, "timeline", i, "index.html")).read()
    art = s[s.index("<article"):s.index("</article>")]
    srcs = re.findall(r'<img[^>]*\ssrc="([^"]+)"', art)
    ok = srcs == [f"/timeline/{i}/hero.svg", f"/timeline/{i}/chart.svg"] and all(
        os.path.isfile(os.path.join(ROOT, "public", p.lstrip("/"))) for p in srcs)
    check(f"AC3 {i}: images = own hero.svg + chart.svg, local", ok, srcs)
    check(f"AC3 {i}: no external image URL", not re.search(r'(src|srcset)="(https?:)?//', art))
    cap = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', art, re.S)
    check(f"AC3 {i}: chart caption names source with link", bool(cap) and "Source:" in cap.group(1) and "<a " in cap.group(1))
    chart = open(os.path.join(ROOT, "public/timeline", i, "chart.svg")).read()
    check(f"AC3 {i}: chart SVG carries its Source line, no external refs", "Source: " in chart and not re.search(r'(href|src)="https?:', chart))

# AC4
check("AC4 publish date is a 2026 date", re.fullmatch(r"2026-\d\d-\d\d", published) is not None, published)
for i in ids:
    s = open(os.path.join(dist, "timeline", i, "index.html")).read()
    dates = re.findall(r'<time datetime="([^"]+)"', s) + re.findall(r'article:published_time" content="([^"]+)"', s)
    check(f"AC4 {i}: shows publish date {published}, none 2024/2025",
          dates and all(d == published for d in dates) and not any(d.startswith(("2024", "2025")) for d in dates), dates)
    check(f"AC4 {i}: 'Written in 2026' note", "Written in 2026, looking back at" in s)
    check(f"AC4 {i}: ends with 'What to do about it' pointing to one service",
          len(re.findall(r'href="/#services"', s[s.index('class="post-body"'):s.index('class="post-sources"')])) == 1
          and "What to do about it" in s)

print(f"retro-check: {len(fails)} failure(s)")
sys.exit(1 if fails else 0)
