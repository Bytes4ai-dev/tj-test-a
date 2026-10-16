#!/usr/bin/env python3
"""TJD-644: draw the original visuals for the 12 Timeline retrospectives into public/timeline/<id>/.
hero.svg  = 1200x400 house-style illustration; ONE recurring motif per Insights tag:
            Governance = concentric rings + gate bar, Agents = connected nodes, Observability = pulse line over a grid,
            Engineering = stacked blocks, Data and people = dot grid.
chart.svg = 1200x675 chart or diagram; every number comes from the source named in the post's chart caption and
            is repeated in the SVG's own "Source:" line.
Pure stdlib, deterministic (same output every run), theme colors only. No stock, AI or third-party imagery.
Usage: python3 scripts/make-retro-visuals.py [--check]   (--check: exit 1 if any committed file differs)"""
import hashlib
import os
import sys
from xml.sax.saxutils import escape

INK, PAPER, PANEL, TEAL, MINT, AMBER = "#10141A", "#F3F4F0", "#E6E9E2", "#0B6B63", "#7FD6CB", "#F2B66B"
FONT = "IBM Plex Sans, Arial, sans-serif"
MONO = "IBM Plex Mono, monospace"
HEAD = "Bricolage Grotesque, Arial, sans-serif"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "timeline")

POSTS = {
    "rag-goes-mainstream": ("Data and people", "RAG goes mainstream"),
    "open-weight-models-close-the-gap": ("Engineering", "Open-weight models close the gap"),
    "eu-ai-act-enters-into-force": ("Governance", "The EU AI Act enters into force"),
    "reasoning-models-change-evaluation": ("Observability", "Reasoning models change evaluation"),
    "mcp-arrives": ("Agents", "MCP arrives"),
    "the-agent-hype-year": ("Agents", "The agent hype year"),
    "vibe-coding-and-the-quality-question": ("Engineering", "Vibe coding and the quality question"),
    "prompt-injection-and-agent-security": ("Governance", "Prompt injection becomes real"),
    "ai-regulation-obligations-bite": ("Governance", "AI obligations start to bite"),
    "shadow-ai": ("Data and people", "Shadow AI"),
    "the-governance-containment-gap": ("Observability", "The governance-containment gap"),
    "whats-next-governed-autonomy": ("Governance", "Governed, evidence-backed autonomy"),
}


def seed(pid, n):
    return [b for b in hashlib.sha256(pid.encode()).digest()][:n]


def svg(w, h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f'<title>{escape(title)}</title><rect width="{w}" height="{h}" fill="{PAPER}"/>'
            f'<rect width="{w}" height="16" fill="{TEAL}"/>{body}</svg>\n')


def text(x, y, s, size=28, fill=INK, font=FONT, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}">{escape(s)}</text>')


# ---------- hero motifs (one per tag) ----------
def motif_governance(pid):
    s = seed(pid, 4)
    cx, cy = 900, 210
    out = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="10"/>'
                  for r in (150, 105, 60))
    out += f'<circle cx="{cx}" cy="{cy}" r="24" fill="{TEAL}"/>'
    bars = 1 + s[0] % 2
    for i in range(bars):
        y = cy - 14 + i * 40 - (bars - 1) * 20
        out += f'<rect x="{cx - 190}" y="{y}" width="380" height="22" rx="6" fill="{AMBER}" stroke="{INK}" stroke-width="6"/>'
    return out


def motif_agents(pid):
    s = seed(pid, 12)
    pts = [(700 + (s[i] % 9) * 50, 70 + (s[i + 6] % 6) * 50) for i in range(6)]
    hub = (900, 200)
    out = "".join(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="{INK}" stroke-width="6"/>' for x, y in pts)
    out += "".join(f'<circle cx="{x}" cy="{y}" r="22" fill="{MINT if i % 2 else PANEL}" stroke="{INK}" stroke-width="6"/>'
                   for i, (x, y) in enumerate(pts))
    return out + f'<circle cx="{hub[0]}" cy="{hub[1]}" r="40" fill="{TEAL}" stroke="{INK}" stroke-width="8"/>'


def motif_observability(pid):
    s = seed(pid, 10)
    out = "".join(f'<line x1="{x}" y1="60" x2="{x}" y2="340" stroke="{PANEL}" stroke-width="4"/>' for x in range(660, 1160, 50))
    out += "".join(f'<line x1="640" y1="{y}" x2="1160" y2="{y}" stroke="{PANEL}" stroke-width="4"/>' for y in range(60, 360, 50))
    pts = " ".join(f"{660 + i * 55},{300 - (s[i] % 200)}" for i in range(10))
    out += f'<polyline points="{pts}" fill="none" stroke="{TEAL}" stroke-width="10" stroke-linejoin="round"/>'
    return out + f'<line x1="640" y1="110" x2="1160" y2="110" stroke="{AMBER}" stroke-width="8" stroke-dasharray="18 12"/>'


def motif_engineering(pid):
    s = seed(pid, 8)
    out = ""
    for col in range(4):
        h = 2 + s[col] % 3
        for row in range(h):
            x, y = 690 + col * 115, 320 - (row + 1) * 62
            fill = AMBER if (s[4 + col] + row) % 7 == 0 else (TEAL if row == h - 1 else PANEL)
            out += f'<rect x="{x + (s[col] % 3) * 4 * (row % 2)}" y="{y}" width="100" height="54" rx="8" fill="{fill}" stroke="{INK}" stroke-width="6"/>'
    return out + f'<rect x="660" y="322" width="480" height="10" fill="{INK}"/>'


def motif_data(pid):
    s = seed(pid, 16)
    out = ""
    for r in range(5):
        for c in range(9):
            on = (s[(r * 9 + c) % 16] >> (c % 8)) & 1
            out += f'<circle cx="{700 + c * 52}" cy="{90 + r * 56}" r="15" fill="{TEAL if on else PANEL}" stroke="{INK}" stroke-width="4"/>'
    return out + f'<rect x="{700 + (s[0] % 9) * 52 - 26}" y="60" width="52" height="290" rx="26" fill="none" stroke="{AMBER}" stroke-width="8"/>'


MOTIFS = {"Governance": motif_governance, "Agents": motif_agents, "Observability": motif_observability,
          "Engineering": motif_engineering, "Data and people": motif_data}


def hero(pid, tag, title):
    body = (f'<rect x="40" y="56" width="560" height="300" rx="20" fill="{INK}"/>'
            f'<rect x="28" y="44" width="560" height="300" rx="20" fill="{PANEL}" stroke="{INK}" stroke-width="8"/>'
            + text(64, 110, tag.upper(), 22, TEAL, MONO, 600) + wrap(64, 170, title, 40, 22, HEAD, 700)
            + text(64, 318, "Bytes4AI · Timeline", 20, INK, MONO) + MOTIFS[tag](pid))
    return svg(1200, 400, f"{title}: original illustration ({tag} motif)", body)


def wrap(x, y, s, size, width, font=FONT, weight=400, fill=INK, lh=1.2):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return "".join(text(x, y + i * size * lh, ln, size, fill, font, weight) for i, ln in enumerate(lines))


# ---------- charts and diagrams ----------
def frame(title, source):
    return text(60, 80, title, 36, INK, HEAD, 700), text(60, 640, "Source: " + source, 20, INK, MONO)


def bars(title, source, items, unit="%", maxv=100):
    """Horizontal bars: items = [(label, value, highlight)]"""
    t, src = frame(title, source)
    out = t
    n = len(items)
    gap = min(110, 470 // n)
    for i, (label, v, hot) in enumerate(items):
        y = 130 + i * gap
        w = int(700 * abs(v) / maxv)
        out += text(60, y + 32, label, 22)
        out += f'<rect x="440" y="{y}" width="720" height="50" rx="10" fill="{PANEL}" stroke="{INK}" stroke-width="4"/>'
        out += f'<rect x="440" y="{y}" width="{max(w, 6)}" height="50" rx="10" fill="{AMBER if hot else TEAL}" stroke="{INK}" stroke-width="4"/>'
        out += text(450 + max(w, 6) + 10 if w < 560 else 450 + w - 100, y + 34, f"{v:g}{unit}", 24, INK, MONO, 700)
    return svg(1200, 675, title, out + src)


def timeline(title, source, events):
    t, src = frame(title, source)
    out = t + f'<rect x="80" y="330" width="1040" height="10" fill="{INK}"/>'
    step = 1040 // (len(events) - 1)
    for i, (date, label, hot) in enumerate(events):
        x = 80 + i * step
        out += f'<circle cx="{x}" cy="335" r="22" fill="{AMBER if hot else TEAL}" stroke="{INK}" stroke-width="6"/>'
        up = i % 2 == 0
        out += text(x, 270 if up else 410, date, 22, INK, MONO, 700, "middle")
        out += "".join(text(x, (300 if up else 440) + j * 26, ln, 20, INK, FONT, 400, "middle") for j, ln in enumerate(label))
    return svg(1200, 675, title, out + src)


def boxflow(title, source, steps, note=None):
    t, src = frame(title, source)
    out = t
    n = len(steps)
    w = (1080 - (n - 1) * 30) // n
    for i, (lines, hot) in enumerate(steps):
        x = 60 + i * (w + 30)
        out += f'<rect x="{x + 8}" y="248" width="{w}" height="170" rx="16" fill="{INK}"/>'
        out += f'<rect x="{x}" y="240" width="{w}" height="170" rx="16" fill="{AMBER if hot else PANEL}" stroke="{INK}" stroke-width="6"/>'
        out += "".join(text(x + w // 2, 300 + j * 30, ln, 22, INK, FONT, 600 if j == 0 else 400, "middle") for j, ln in enumerate(lines))
        if i < n - 1:
            out += f'<polygon points="{x + w + 6},315 {x + w + 26},325 {x + w + 6},335" fill="{INK}"/>'
    if note:
        out += text(600, 500, note, 22, INK, MONO, 400, "middle")
    return svg(1200, 675, title, out + src)


def mcp_diagram():
    title = "One protocol instead of many connectors"
    t, src = frame(title, "Anthropic, Introducing the Model Context Protocol (Nov 2024)")
    out = t + text(300, 140, "Without a shared protocol", 24, INK, MONO, 700, "middle") + text(900, 140, "With MCP", 24, INK, MONO, 700, "middle")
    apps = [(100, 220 + i * 120) for i in range(3)]
    tools = [(500, 200 + i * 95) for i in range(4)]
    out += "".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{AMBER}" stroke-width="5"/>' for a in apps for b in tools)
    out += "".join(f'<rect x="{x - 40}" y="{y - 25}" width="80" height="50" rx="10" fill="{PANEL}" stroke="{INK}" stroke-width="5"/>' for x, y in apps)
    out += "".join(f'<circle cx="{x}" cy="{y}" r="24" fill="{MINT}" stroke="{INK}" stroke-width="5"/>' for x, y in tools)
    out += text(100, 560, "AI apps", 20, INK, MONO, 400, "middle") + text(500, 560, "tools and data", 20, INK, MONO, 400, "middle")
    hub = (900, 340)
    apps2 = [(700, 220 + i * 120) for i in range(3)]
    tools2 = [(1100, 200 + i * 95) for i in range(4)]
    out += "".join(f'<line x1="{x}" y1="{y}" x2="{hub[0]}" y2="{hub[1]}" stroke="{TEAL}" stroke-width="6"/>' for x, y in apps2 + tools2)
    out += "".join(f'<rect x="{x - 40}" y="{y - 25}" width="80" height="50" rx="10" fill="{PANEL}" stroke="{INK}" stroke-width="5"/>' for x, y in apps2)
    out += "".join(f'<circle cx="{x}" cy="{y}" r="24" fill="{MINT}" stroke="{INK}" stroke-width="5"/>' for x, y in tools2)
    out += f'<rect x="850" y="310" width="100" height="60" rx="12" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>' + text(900, 350, "MCP", 24, PAPER, MONO, 700, "middle")
    out += f'<rect x="598" y="130" width="6" height="440" fill="{INK}"/>'
    return svg(1200, 675, title, out + src)


def trifecta():
    title = "The lethal trifecta for AI agents"
    t, src = frame(title, "Simon Willison, The lethal trifecta for AI agents (16 June 2025)")
    out = t
    for (cx, cy, label, dx, dy) in ((390, 270, ["Access to", "private data"], -50, -30),
                                    (630, 270, ["Exposure to", "untrusted content"], 30, -30),
                                    (510, 430, ["Ability to", "communicate out"], 0, 60)):
        out += f'<circle cx="{cx}" cy="{cy}" r="140" fill="{MINT}" fill-opacity="0.45" stroke="{INK}" stroke-width="6"/>'
        out += "".join(text(cx + dx, cy + dy + j * 26, ln, 22, INK, FONT, 600, "middle") for j, ln in enumerate(label))
    out += f'<circle cx="510" cy="330" r="30" fill="{AMBER}" stroke="{INK}" stroke-width="6"/>'
    out += text(840, 330, "All three together:", 22, INK, MONO, 700) + text(840, 360, "data can be stolen.", 22, INK, MONO) + text(840, 390, "Remove one leg.", 22, INK, MONO)
    return svg(1200, 675, title, out + src)


def governed_loop():
    title = "A governed, evidence-backed change loop"
    t, src = frame(title, "Bytes4AI diagram; functions from the NIST AI Risk Management Framework 1.0")
    out = t
    nodes = [(300, 200, "Propose", "agent drafts a change"), (800, 200, "Review", "separate check"),
             (800, 470, "Approve", "gate, human if needed"), (300, 470, "Ship + record", "evidence kept")]
    for i, (x, y, a, b) in enumerate(nodes):
        nx, ny = nodes[(i + 1) % 4][:2]
        out += f'<line x1="{x}" y1="{y}" x2="{nx}" y2="{ny}" stroke="{TEAL}" stroke-width="8"/>'
    for x, y, a, b in nodes:
        out += f'<rect x="{x - 130}" y="{y - 55}" width="260" height="110" rx="16" fill="{PANEL}" stroke="{INK}" stroke-width="6"/>'
        out += text(x, y - 8, a, 26, INK, HEAD, 700, "middle") + text(x, y + 26, b, 20, INK, FONT, 400, "middle")
    out += f'<rect x="980" y="300" width="180" height="80" rx="16" fill="{AMBER}" stroke="{INK}" stroke-width="6"/>' + text(1070, 348, "Tested stop", 22, INK, MONO, 700, "middle")
    out += text(550, 345, "Govern · Map · Measure · Manage", 20, INK, MONO, 400, "middle")
    return svg(1200, 675, title, out + src)


CHARTS = {
    "rag-goes-mainstream": lambda: bars("RAG in enterprise AI implementations", "Menlo Ventures, 2024: The State of Generative AI in the Enterprise",
                                        [("2023", 31, False), ("2024", 51, True)]),
    "open-weight-models-close-the-gap": lambda: bars("Gap between top closed and open-weight models", "Stanford HAI, AI Index Report 2025",
                                                     [("Early 2024", 8, True), ("Early 2025", 1.7, False)], maxv=10),
    "eu-ai-act-enters-into-force": lambda: timeline("EU AI Act: when the rules apply", "artificialintelligenceact.eu implementation timeline; Regulation (EU) 2024/1689",
                                                    [("1 Aug 2024", ["Enters into force"], True), ("2 Feb 2025", ["Prohibitions,", "AI literacy"], False),
                                                     ("2 Aug 2025", ["General-purpose", "AI model rules"], False), ("2 Aug 2026", ["Most remaining", "rules"], False),
                                                     ("2 Aug 2027", ["Earlier GPAI", "models comply"], False)]),
    "reasoning-models-change-evaluation": lambda: bars("AIME 2024: GPT-4o vs o1 at three compute settings", "OpenAI, Learning to reason with LLMs (Sept 2024)",
                                                       [("GPT-4o", 12, False), ("o1, 1 sample", 74, True), ("o1, consensus of 64", 83, True), ("o1, re-rank 1,000", 93, True)]),
    "mcp-arrives": mcp_diagram,
    "the-agent-hype-year": lambda: boxflow("Why agent projects get canceled", "Gartner press release, 25 June 2025",
                                           [(["Announce", "an agent"], False), (["Pilot"], False), (["Checkpoint:", "cost, value,", "risk controls"], True), (["Scale", "or cancel"], False)],
                                           "Gartner predicts over 40% of agentic AI projects canceled by end of 2027"),
    "vibe-coding-and-the-quality-question": lambda: bars("AI tools and task time: felt vs measured", "METR, early-2025 study of 16 experienced open-source developers",
                                                         [("Expected speed-up", 24, False), ("Believed speed-up", 20, False), ("Measured: slower by", 19, True)], maxv=30),
    "prompt-injection-and-agent-security": trifecta,
    "ai-regulation-obligations-bite": lambda: timeline("AI obligations in 2025", "artificialintelligenceact.eu; European Commission; Colorado General Assembly SB25B-004",
                                                       [("2 Feb 2025", ["EU prohibitions,", "AI literacy"], True), ("10 Jul 2025", ["GPAI Code of", "Practice published"], False),
                                                        ("2 Aug 2025", ["EU GPAI model", "rules apply"], True), ("30 Jun 2026", ["Colorado AI Act", "(delayed to)"], False)]),
    "shadow-ai": lambda: bars("AI in breaches, 2025", "IBM, Cost of a Data Breach Report 2025 (press release, 30 July 2025)",
                              [("AI model/app breached", 13, False), ("..of those, weak AI access", 97, True),
                               ("Breached, no AI policy", 63, False), ("Breach via shadow AI", 20, True)]),
    "the-governance-containment-gap": lambda: bars("Watching vs stopping AI agents", "Kiteworks, 2026 Data Security Forecast (self-reported survey)",
                                                   [("Continuous monitoring in place", 58, False), ("Can terminate an agent quickly", 40, True)]),
    "whats-next-governed-autonomy": governed_loop,
}


def main():
    check = "--check" in sys.argv
    bad = 0
    for pid, (tag, title) in POSTS.items():
        d = os.path.join(ROOT, pid)
        os.makedirs(d, exist_ok=True)
        for name, data in (("hero.svg", hero(pid, tag, title)), ("chart.svg", CHARTS[pid]())):
            p = os.path.join(d, name)
            if check:
                if not os.path.exists(p) or open(p).read() != data:
                    print("DIFFERS", p); bad += 1
            else:
                with open(p, "w") as f:
                    f.write(data)
    if check:
        print("make-retro-visuals --check:", "PASS" if not bad else f"FAIL ({bad})")
        sys.exit(1 if bad else 0)
    print("wrote", 2 * len(POSTS), "SVGs under public/timeline/")


if __name__ == "__main__":
    main()
