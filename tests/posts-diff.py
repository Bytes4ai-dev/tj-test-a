#!/usr/bin/env python3
"""TJD-643 AC1: every donor post is migrated verbatim.
For each post in <donor>/src/content/posts (rpsk82/bytes4ai-website, read-only clone):
  body diff     : body (text after the frontmatter) of src/content/posts/<id>.md vs the donor file -> must be EMPTY
  frontmatter   : title / date / excerpt / tags lines identical to the donor
  rendered diff : visible text of dist/posts/<id>/index.html .post-body vs the donor body with markdown syntax
                  removed (headings, bold, list markers, link targets) -> must be EMPTY
Prints one line per post plus any diff; exit 0 only when all are empty and the post sets match.
Usage: python3 tests/posts-diff.py <donor-repo-dir> [dist-dir]"""
import difflib
import html
import os
import re
import sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
donor = os.path.join(sys.argv[1], "src", "content", "posts")
dist = sys.argv[2] if len(sys.argv) > 2 else os.path.join(root, "dist")
ours = os.path.join(root, "src", "content", "posts")


def split(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    return (m.group(1), text[m.end():]) if m else ("", text)


def md_text(body):
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body)
    t = re.sub(r"(?m)^\s*#+\s+", "", t)
    t = re.sub(r"(?m)^\s*([-*+]|\d+\.)\s+", "", t)
    t = re.sub(r"(?m)^\s*>\s?", "", t)
    t = t.replace("**", "").replace("`", "")
    t = re.sub(r"(?<![\w*])\*(?!\s)([^*\n]+?)\*(?!\w)", r"\1", t)
    return " ".join(t.split())


def page_text(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r'<div class="post-body"[^>]*>(.*?)</div>\s*(<aside|<section class="post-sources"|<div class="card post-cta")', s, re.S)
    if not m:
        return None
    t = re.sub(r"</?(p|h[1-6]|li|ul|ol|blockquote|br|hr|pre|div)\b[^>]*>", " ", m.group(1))
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", t)).split())


def fm_fields(fm):
    return {k: v for k, v in re.findall(r"(?m)^(title|date|excerpt|tags):\s*(.*)$", fm)}


donor_ids = sorted(f[:-3] for f in os.listdir(donor) if f.endswith(".md"))
our_ids = sorted(f[:-3] for f in os.listdir(ours) if f.endswith(".md"))
fails = 0
if donor_ids != our_ids:
    print("FAIL post set differs: only donor=%s only ours=%s" % (sorted(set(donor_ids) - set(our_ids)), sorted(set(our_ids) - set(donor_ids))))
    fails += 1
print("donor posts: %d, migrated posts: %d" % (len(donor_ids), len(our_ids)))
for pid in donor_ids:
    d_fm, d_body = split(open(os.path.join(donor, pid + ".md"), encoding="utf-8").read())
    p = os.path.join(ours, pid + ".md")
    if not os.path.exists(p):
        print("FAIL %s: missing" % pid); fails += 1; continue
    o_fm, o_body = split(open(p, encoding="utf-8").read())
    body_diff = list(difflib.unified_diff(d_body.splitlines(), o_body.splitlines(), "donor/" + pid, "site/" + pid, lineterm=""))
    fm_ok = fm_fields(d_fm) == fm_fields(o_fm)
    rendered = page_text(os.path.join(dist, "posts", pid, "index.html"))
    want = md_text(d_body)
    r_diff = [] if rendered == want else list(difflib.unified_diff(
        re.split(r"(?<=[.!?:])\s", want), re.split(r"(?<=[.!?:])\s", rendered or ""), "donor-text", "rendered-text", lineterm=""))
    ok = not body_diff and fm_ok and rendered is not None and not r_diff
    print("%s %s: body diff %s, frontmatter %s, rendered diff %s" % (
        "PASS" if ok else "FAIL", pid, "EMPTY" if not body_diff else "%d lines" % len(body_diff),
        "same" if fm_ok else "DIFFERS", "EMPTY" if rendered is not None and not r_diff else ("no page" if rendered is None else "%d lines" % len(r_diff))))
    for line in body_diff + r_diff[:40]:
        print("  " + line)
    fails += 0 if ok else 1
print("posts-diff: %d failure(s)" % fails)
sys.exit(1 if fails else 0)
