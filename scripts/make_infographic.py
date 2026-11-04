#!/usr/bin/env python3
"""make_infographic.py — generate the study infographics as SVG (+ PNG if a converter exists).

    python3 scripts/make_infographic.py            # all three, SVG + PNG
    python3 scripts/make_infographic.py loop --svg-only

Why SVG: it is text, so it diffs, reviews and regenerates — unlike a screenshot. PNG is
emitted for anywhere that will not render SVG (slides, chat, print).

Images produced:
    infographics/learning-loop.svg/.png      the 95-minute loop, five gates
    infographics/module-anatomy.svg/.png     the five questions every module answers
    infographics/integration-flow.svg/.png   outbound / remote table / inbound — pick one
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "infographics"

BG = "#0b1120"
PANEL = "#111c33"
LINE = "#1f2c47"
INK = "#e5ecf7"
MUTED = "#94a3b8"
ACCENTS = ["#f97316", "#38bdf8", "#a78bfa", "#22d3ee", "#34d399", "#f472b6"]

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,DejaVu Sans,Arial,sans-serif"


def esc(t: str) -> str:
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def svg_open(w: int, h: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="{FONT}">',
        "<defs>",
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#64748b"/></marker>',
        '<marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{ACCENTS[0]}"/></marker>',
        "</defs>",
        f'<rect width="{w}" height="{h}" fill="{BG}"/>',
    ]


def text(x: int, y: int, t: str, size: int = 14, fill: str = INK, weight: str = "400",
         anchor: str = "start") -> str:
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{esc(t)}</text>')


def box(x: int, y: int, w: int, h: int, title: str, lines: list[str], accent: str,
        title_size: int = 16) -> list[str]:
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{PANEL}" stroke="{accent}" '
        f'stroke-width="1.6" stroke-opacity="0.85"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="4" rx="2" fill="{accent}"/>',
        text(x + 16, y + 32, title, title_size, INK, "650"),
    ]
    for i, ln in enumerate(lines):
        parts.append(text(x + 16, y + 56 + i * 19, ln, 12.5, MUTED))
    return parts


def arrow(x1: int, y1: int, x2: int, y2: int, color: str = "#64748b", width: int = 1.6,
          dash: str | None = None, marker: str = "arrow") -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'
            f'{d} marker-end="url(#{marker})"/>')


def title_block(w: int, title: str, subtitle: str) -> list[str]:
    return [text(40, 52, title, 26, INK, "700"), text(40, 80, subtitle, 13.5, MUTED)]


def learning_loop() -> list[str]:
    w, h = 1180, 460
    parts = svg_open(w, h) + title_block(
        w, "The 95-minute loop",
        "One module, five gates. Artifacts are the unit of progress — not hours watched.")
    gates = [
        ("1 · Orient", ["10 min", "Filter navigator + 3 lists", "Artifact: 3 breadcrumbs"], ACCENTS[1]),
        ("2 · Model", ["20 min", "Tables, states, roles", "Artifact: one page + diagram"], ACCENTS[2]),
        ("3 · Practise", ["45 min", "Lab, then break it", "Artifact: fix + 'what broke'"], ACCENTS[3]),
        ("4 · Prove", ["10 min", "Probe sheet + quiz", "Artifact: probe.json diff"], ACCENTS[4]),
        ("5 · Teach", ["10 min", "5 sentences + diagram", "Artifact: teach-back note"], ACCENTS[0]),
    ]
    bw, bh, gap, y = 200, 150, 22, 130
    x = 40
    for i, (t, lines, accent) in enumerate(gates):
        parts += box(x, y, bw, bh, t, lines, accent)
        if i < len(gates) - 1:
            parts.append(arrow(x + bw + 3, y + bh // 2, x + bw + gap - 3, y + bh // 2))
        x += bw + gap
    # feedback arrow
    parts.append(f'<path d="M {x - gap - bw // 2} {y + bh + 14} L {x - gap - bw // 2} {y + bh + 46} '
                 f'L {40 + bw // 2} {y + bh + 46} L {40 + bw // 2} {y + bh + 16}" fill="none" '
                 f'stroke="{ACCENTS[5]}" stroke-width="1.6" stroke-dasharray="6 5" marker-end="url(#arrow)"/>')
    parts.append(text(w // 2, y + bh + 82, "Teach-back exposes the gap → next day starts at Orient",
                      12.5, MUTED, anchor="middle"))
    parts.append(text(40, h - 24, "Targets, not measured benchmarks. Stop at the timebox; "
                                  "unfinished work becomes tomorrow's first gate.", 11.5, "#64748b"))
    parts.append("</svg>")
    return parts


def module_anatomy() -> list[str]:
    w, h = 1180, 520
    parts = svg_open(w, h) + title_block(
        w, "Every module answers the same five questions",
        "Learn the machine once; a new module then costs an hour, not a week.")
    rows = [
        ("What is the record?", ["incident", "change_request", "sn_hr_core_case", "wm_order"], ACCENTS[1]),
        ("What are the states?", ["new → in progress → resolved", "drives SLA, flows, metrics"], ACCENTS[2]),
        ("Who can see it?", ["itil", "sn_incident_write", "sn_hr_core.case_writer", "ACLs"], ACCENTS[3]),
        ("How does work move?", ["assignment groups", "approvals", "flows", "playbooks"], ACCENTS[4]),
        ("How is it proven?", ["indicator", "breakdown", "dashboard", "task_sla"], ACCENTS[0]),
    ]
    y = 118
    for q, chips, accent in rows:
        parts.append(f'<rect x="40" y="{y}" width="1100" height="62" rx="10" fill="{PANEL}" '
                     f'stroke="{LINE}"/>')
        parts.append(f'<rect x="40" y="{y}" width="5" height="62" rx="2.5" fill="{accent}"/>')
        parts.append(text(62, y + 38, q, 15.5, INK, "600"))
        cx = 420
        for c in chips:
            cw = max(90, 9 * len(c) + 22)
            parts.append(f'<rect x="{cx}" y="{y + 18}" width="{cw}" height="26" rx="13" '
                         f'fill="#0f1a2d" stroke="{accent}" stroke-opacity="0.5"/>')
            parts.append(text(cx + cw // 2, y + 36, c, 12, MUTED, anchor="middle"))
            cx += cw + 10
        y += 72
    parts.append(text(40, h - 26, "If you cannot answer all five from memory, you have read "
                                  "about the module — you have not learned it.", 12, "#64748b"))
    parts.append("</svg>")
    return parts


def integration_flow() -> list[str]:
    w, h = 1180, 470
    parts = svg_open(w, h) + title_block(
        w, "Three integration shapes — pick one deliberately",
        "The most common design error is choosing the wrong row for the data's behaviour.")
    cols = [
        ("Outbound REST", ["ServiceNow calls an API",
                           "REST Message / Flow REST step",
                           "Can read AND write",
                           "Log: sys_outbound_http_log"], ACCENTS[1],
         ["Tickets ↔ vendor system", "Trigger actions from data", "Scheduled syncs"]),
        ("Remote Table", ["An API appears as a table",
                          "Read-only view, live",
                          "No writes, no local joins",
                          "Cost: one HTTP call per query"], ACCENTS[2],
         ["Reference data, rarely changing", "Vendor directories", "Small lookups"]),
        ("Inbound API", ["The world calls ServiceNow",
                         "Scripted REST API",
                         "You control validation",
                         "Auth: OAuth / basic + ACLs"], ACCENTS[4],
         ["Webhooks from SaaS", "External portals", "Event ingestion"]),
    ]
    bw, bh, gap = 340, 250, 40
    x = 40
    for title, lines, accent, use_for in cols:
        parts += box(x, 118, bw, bh, title, lines, accent)
        yy = 118 + 56 + len(lines) * 19 + 10
        parts.append(text(x + 16, yy + 12, "Use it for:", 12, accent, "600"))
        for i, u in enumerate(use_for):
            parts.append(text(x + 16, yy + 34 + i * 18, "· " + u, 12, MUTED))
        x += bw + gap
    parts.append(arrow(40 + bw + 4, 240, 40 + bw + gap - 6, 240, "#475569", 1.4, "5 5"))
    parts.append(arrow(40 + 2 * bw + gap + 4, 240, 40 + 2 * bw + 2 * gap - 6, 240, "#475569", 1.4, "5 5"))
    parts.append(text(40, h - 28, "Read rarely and live → remote table.  Read often and join → "
                                  "scheduled import.  Must write → REST + flow.", 12, "#64748b"))
    parts.append("</svg>")
    return parts


BUILDERS = {"loop": learning_loop, "anatomy": module_anatomy, "flow": integration_flow}
NAMES = {"loop": "learning-loop", "anatomy": "module-anatomy", "flow": "integration-flow"}


def to_png(svg_path: Path) -> str:
    for cmd in (["rsvg-convert", "-z", "2"], ["inkscape", "--export-dpi=180"],
                ["convert", "-density", "144"]):
        if shutil.which(cmd[0]):
            png = svg_path.with_suffix(".png")
            try:
                subprocess.run(cmd + [str(svg_path), "-o" if cmd[0] == "rsvg-convert" else str(png)]
                               if cmd[0] == "rsvg-convert" else cmd + [str(svg_path), str(png)],
                               check=True, capture_output=True)
                if png.exists():
                    return f"png via {cmd[0]} ({png.stat().st_size // 1024} KB)"
            except subprocess.CalledProcessError as exc:
                last = exc.stderr.decode()[:160] if exc.stderr else str(exc)
                continue
    return "png skipped (no rsvg-convert / inkscape / imagemagick)"


def main() -> None:
    args = sys.argv[1:]
    svg_only = "--svg-only" in args
    which = [a for a in args if not a.startswith("-")] or list(BUILDERS)
    OUT.mkdir(exist_ok=True)
    for key in which:
        if key not in BUILDERS:
            sys.exit(f"unknown target '{key}'. Choose from: {', '.join(BUILDERS)}")
        svg_path = OUT / f"{NAMES[key]}.svg"
        svg_path.write_text("\n".join(BUILDERS[key]()), encoding="utf-8")
        msg = f"wrote {svg_path.relative_to(ROOT)}"
        if not svg_only:
            msg += " · " + to_png(svg_path)
        print(msg)


if __name__ == "__main__":
    main()
