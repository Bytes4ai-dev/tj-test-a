#!/usr/bin/env python3
"""TJD-641: draw the original share-preview images (1200x630 PNG, one per page) into public/og/.
Pure stdlib (zlib); simple geometric house-style shapes in the six theme colors. No stock, AI or third-party imagery."""
import os
import struct
import sys
import zlib

W, H = 1200, 630
INK, PAPER, PANEL = (0x10, 0x14, 0x1A), (0xF3, 0xF4, 0xF0), (0xE6, 0xE9, 0xE2)
TEAL, MINT, AMBER = (0x0B, 0x6B, 0x63), (0x7F, 0xD6, 0xCB), (0xF2, 0xB6, 0x6B)


def canvas(bg):
    return [bytearray(bytes(bg) * W) for _ in range(H)]


def rect(px, x0, y0, x1, y1, c):
    for y in range(max(0, y0), min(H, y1)):
        row = px[y]
        row[3 * max(0, x0):3 * min(W, x1)] = bytes(c) * (min(W, x1) - max(0, x0))


def card(px, x0, y0, x1, y1, fill, shadow=12, border=8):
    if shadow:
        rect(px, x0 + shadow, y0 + shadow, x1 + shadow, y1 + shadow, INK)
    rect(px, x0, y0, x1, y1, INK)
    rect(px, x0 + border, y0 + border, x1 - border, y1 - border, fill)


def disc(px, cx, cy, r, c, ring=0):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            d = (x - cx) ** 2 + (y - cy) ** 2
            if d <= r * r and (not ring or d >= (r - ring) ** 2) and 0 <= x < W and 0 <= y < H:
                px[y][3 * x:3 * x + 3] = bytes(c)


def save(px, path):
    raw = b"".join(b"\x00" + bytes(r) for r in px)
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


def frame(bg=PAPER):
    px = canvas(bg)
    rect(px, 0, 0, W, 24, TEAL)  # top band
    return px


def home(px):  # gap meter: monitor 58% vs can stop 40%
    card(px, 120, 150, 1080, 500, PAPER)
    rect(px, 180, 220, 1020, 290, INK); rect(px, 188, 228, 1012, 282, PAPER); rect(px, 188, 228, 188 + int(824 * .58), 282, TEAL)
    rect(px, 180, 350, 1020, 420, INK); rect(px, 188, 358, 1012, 412, PAPER); rect(px, 188, 358, 188 + int(824 * .40), 412, AMBER)


def platform(px):  # capability tiles in three states
    fills = [TEAL, TEAL, TEAL, PANEL, PANEL, AMBER]
    for i, f in enumerate(fills):
        x, y = 140 + (i % 3) * 320, 130 + (i // 3) * 220
        card(px, x, y, x + 280, y + 180, f, shadow=8)


def insights(px):  # stacked cards
    for i in range(3):
        card(px, 260 + i * 60, 140 + i * 60, 900 + i * 60, 400 + i * 60, [PANEL, PAPER, MINT][i], shadow=0)


def timeline(px):  # line with three markers
    rect(px, 120, 305, 1080, 325, INK)
    for i, c in enumerate([TEAL, TEAL, AMBER]):
        disc(px, 250 + i * 350, 315, 60, INK); disc(px, 250 + i * 350, 315, 48, c)


def about(px):  # circle mark
    disc(px, 600, 315, 200, INK); disc(px, 600, 315, 188, TEAL); disc(px, 600, 315, 120, MINT, ring=24)


def post(px):  # page with a chart
    card(px, 330, 90, 870, 560, PAPER)
    for i, h in enumerate([120, 200, 280]):
        rect(px, 420 + i * 130, 480 - h, 500 + i * 130, 480, AMBER if i == 2 else TEAL)


def post_card(px, slug):  # TJD-643: one original image per post, bars drawn from the post id
    h = 0
    for ch in slug:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    card(px, 150, 110, 1050, 520, PAPER)
    hot = h % 5
    for i in range(5):
        v = 80 + ((h >> (i * 5)) % 220)
        rect(px, 230 + i * 160, 460 - v, 330 + i * 160, 460, AMBER if i == hot else TEAL)
    rect(px, 200, 460, 1000, 472, INK)


def posts_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "content", "posts")


def main(out):
    os.makedirs(out, exist_ok=True)
    for name, fn, bg in [("home", home, PANEL), ("platform", platform, PAPER), ("insights", insights, PAPER),
                         ("timeline", timeline, PANEL), ("about", about, PAPER), ("post", post, PANEL)]:
        px = frame(bg)
        fn(px)
        save(px, os.path.join(out, name + ".png"))
        print("og:", name)
    os.makedirs(os.path.join(out, "posts"), exist_ok=True)
    for f in sorted(os.listdir(posts_dir())):
        if f.endswith(".md"):
            slug = f[:-3]
            px = frame(PANEL)
            post_card(px, slug)
            save(px, os.path.join(out, "posts", slug + ".png"))
            print("og: posts/" + slug)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "public", "og"))
