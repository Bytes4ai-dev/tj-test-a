#!/usr/bin/env python3
"""TJD-643 AC3: dist/rss.xml is a valid RSS 2.0 feed listing every post newest first by publish date.
Checks: well-formed XML; channel title/link/description + atom:link self; one item per post in src/content/posts
(fixture entries excluded); each item has title/link/guid/pubDate (RFC 822); order = pubDate descending;
item links are absolute on the site URL and map to a built page. When the feedparser module is importable it
must also parse the feed with 0 errors (bozo = 0).
Usage: python3 tests/rss-check.py [dist-dir] [site-url]"""
import email.utils
import os
import re
import sys
import xml.etree.ElementTree as ET

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
dist = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "dist")
site_url = (sys.argv[2] if len(sys.argv) > 2 else os.environ.get("SITE_URL") or "https://rvdemo-app-crnwvkk4ua-uc.a.run.app").rstrip("/")
feed = os.path.join(dist, "rss.xml")
fails = []

posts = {}
pdir = os.path.join(root, "src", "content", "posts")
for f in sorted(os.listdir(pdir)):
    if f.endswith(".md"):
        fm = re.match(r"^---\n(.*?)\n---", open(os.path.join(pdir, f), encoding="utf-8").read(), re.S).group(1)
        if re.search(r"(?m)^fixture:\s*true\b", fm) or re.search(r'(?m)^title:\s*["\']?\[TEST\]', fm):
            continue
        posts[f[:-3]] = re.search(r"(?m)^date:\s*(\S+)", fm).group(1)

tree = ET.parse(feed)
rss = tree.getroot()
ch = rss.find("channel")
if rss.tag != "rss" or rss.get("version") != "2.0" or ch is None:
    fails.append("not an RSS 2.0 document")
for tag in ("title", "link", "description"):
    if ch is None or not (ch.findtext(tag) or "").strip():
        fails.append("channel missing " + tag)
self_link = ch.find("{http://www.w3.org/2005/Atom}link") if ch is not None else None
if self_link is None or self_link.get("href") != site_url + "/rss.xml" or self_link.get("rel") != "self":
    fails.append("atom:link self missing or not %s/rss.xml" % site_url)

items = ch.findall("item") if ch is not None else []
seen, dates = [], []
for it in items:
    link = it.findtext("link") or ""
    for tag in ("title", "link", "guid", "pubDate", "description"):
        if not (it.findtext(tag) or "").strip():
            fails.append("item %s missing %s" % (link, tag))
    try:
        dates.append(email.utils.parsedate_to_datetime(it.findtext("pubDate")))
    except Exception:
        fails.append("item %s pubDate not RFC 822" % link)
    m = re.fullmatch(re.escape(site_url) + r"/posts/([^/]+)/", link)
    if not m:
        fails.append("item link not absolute on site URL: " + link)
        continue
    seen.append(m.group(1))
    if not os.path.exists(os.path.join(dist, "posts", m.group(1), "index.html")):
        fails.append("item link has no built page: " + link)
if sorted(seen) != sorted(posts):
    fails.append("feed items != posts (feed %d, posts %d)" % (len(seen), len(posts)))
if dates != sorted(dates, reverse=True):
    fails.append("items not newest first by pubDate")
want_order = sorted(posts, key=lambda k: posts[k], reverse=True)
if [posts[s] for s in seen] != [posts[s] for s in want_order]:
    fails.append("item dates do not follow the posts' publish dates newest first")

try:
    import feedparser
    d = feedparser.parse(feed)
    print("feedparser %s: bozo=%s entries=%d version=%s" % (feedparser.__version__, d.bozo, len(d.entries), d.version))
    if d.bozo:
        fails.append("feedparser bozo: %s" % d.bozo_exception)
    if len(d.entries) != len(posts):
        fails.append("feedparser entries %d != %d" % (len(d.entries), len(posts)))
except ImportError:
    print("feedparser not installed: structural checks only")

print("rss items: %d (posts %d); order:" % (len(items), len(posts)))
for s, d in zip(seen, dates):
    print("  %s  %s" % (d.date().isoformat(), s))
for f in fails:
    print("FAIL " + f)
print("rss-check: %d failure(s)" % len(fails))
sys.exit(1 if fails else 0)
