#!/usr/bin/env python3
"""build_video.py — render the getting-started video from docs/11-video-guide.md.

    python3 scripts/build_video.py                 # build video/getting-started.mp4
    python3 scripts/build_video.py --check         # verify tooling only

What this produces: an animated, narrated walkthrough, 1280x720, with a mock ServiceNow UI on
the right, a cursor that travels to the thing being described, a highlight ring on the target,
and burned-in captions plus a matching .vtt.

The UI is a *drawing*, not a recording: no ServiceNow instance exists in this repository, so
every scene paints a stylised screen and every beat says what to click for real on your own
instance. That is stated on screen, so a viewer is never misled into thinking it is live
footage.

Requires: ffmpeg + espeak-ng + PIL (DejaVu fonts).
"""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "video"
W, H = 1280, 720
FPS = 12

BG = (11, 17, 32)
PANEL = (17, 28, 51)
INK = (229, 236, 247)
MUTED = (148, 163, 184)
DIM = (100, 116, 139)
ACCENTS = [(56, 189, 248), (167, 139, 250), (34, 211, 238), (52, 211, 153),
           (249, 115, 22), (244, 114, 182), (96, 165, 250), (250, 204, 21)]

# mock screen geometry
PX, PY, PW, PH = 604, 150, 612, 470


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    raise SystemExit("no usable TTF font found (install fonts-dejavu)")


# ---- the eight scenes ------------------------------------------------------------------
# `beats` are fractions of the scene's audio duration, so the cursor cannot drift out of sync
# when the narration is re-worded: [fraction, element_id]. `ui` is what gets painted.
SCENES = [
    {
        "title": "ServiceNow in eight minutes",
        "kicker": "scene 1 · what this is",
        "screen": ["Show: the login page, then the home dashboard",
                   "Do not click yet. Just look."],
        "narration": (
            "This is ServiceNow. One platform, many costumes: IT service management, HR, "
            "security operations, customer service, field service. They look like different "
            "products. They are the same machine pointed at different records. In the next "
            "eight minutes I will show you the machine, not a tour of menus. Everything you "
            "see is a row in a table; everything you can do is a rule about those rows. If "
            "that sounds abstract now, it will not by the end: you will watch one incident "
            "travel from a person who cannot log a ticket to a team that fixes it."
        ),
        "ui": {"kind": "nav", "path": "nav_to.do?uri=home.do", "query": "",
               "results": ["Incidents", "Users", "Asset"], "title": "ServiceNow"},
        "beats": [(0.15, "filter"), (0.62, "menubar")],
    },
    {
        "title": "Everything is a record",
        "kicker": "scene 2 · navigation and lists",
        "screen": ["Type 'incident' into the filter navigator",
                   "Open the list, then open one record"],
        "narration": (
            "Start in the filter navigator, top left. Type incident. This is the fastest way to "
            "navigate, and it teaches you the real name of things. What opens is a list: many "
            "records of one type. Click any row and you get a form: one record, with fields. "
            "So there are only three shapes to learn. A table holds records. A list shows many "
            "of them. A form shows one. The menu is just a saved pointer to a list, which is "
            "why the menu can move between releases and nothing about your data changes."
        ),
        "ui": {"kind": "list", "path": "incident_list.do", "title": "Incidents",
               "query": "incident",
               "rows": [("INC0010023", "Email is down", "In progress", "High"),
                        ("INC0010022", "Laptop won't boot", "New", "Moderate"),
                        ("INC0010021", "VPN drops hourly", "New", "Low")]},
        "beats": [(0.12, "filter"), (0.45, "row0"), (0.74, "row1")],
    },
    {
        "title": "Related lists: the rest of the story",
        "kicker": "scene 3 · the record's context",
        "screen": ["Scroll to the bottom of the incident form",
                   "Point at Task SLA, Approvers, Work notes"],
        "narration": (
            "Scroll to the bottom of the form. These are related lists, and they are the part "
            "beginners skip. Each one is another table, filtered to this record. Task SLA is "
            "the promise and its clock. Approvers are the people who can block. Work notes are "
            "the history. Affected configuration items are what this incident is about. If you "
            "only read the fields at the top, you are reading the cover of the book."
        ),
        "ui": {"kind": "form", "path": "incident.do", "title": "INC0010023",
               "fields": [("Number", "INC0010023"), ("Caller", "Sarah Chen"),
                          ("Assignment group", "Service Desk"), ("State", "In progress")],
               "related": ["Task SLA", "Approvers", "Work notes", "Affected CIs"]},
        "beats": [(0.28, "fields"), (0.62, "related")],
    },
    {
        "title": "Fields are configuration, not code",
        "kicker": "scene 4 · where 'mandatory' really lives",
        "screen": ["Right-click the header, Configure, Form Layout",
                   "Then Tables and Columns, incident, Columns"],
        "narration": (
            "Right click the header and choose configure, form layout. Fields are chosen, not "
            "hardcoded, and that change is reversible. Now the important part. Open tables and "
            "columns, search incident, and look at the columns. This is the dictionary, the "
            "definition of every field. A field can be mandatory here, which blocks forms, "
            "imports and APIs, or mandatory only through a UI policy, which blocks one form for "
            "one group of people. Those are different things, and confusing them breaks "
            "integrations that used to work."
        ),
        "ui": {"kind": "dict", "path": "sys_dictionary_list.do", "title": "Dictionary · incident",
               "columns": [("short_description", "String", "true"),
                           ("caller_id", "Reference", "true"),
                           ("assignment_group", "Reference", "false")]},
        "beats": [(0.2, "header"), (0.5, "col0"), (0.8, "mandatory")],
    },
    {
        "title": "The layer underneath: foundation data",
        "kicker": "scene 5 · people, places, groups, clock",
        "screen": ["Users: department, location, manager",
                   "Groups: manager and members",
                   "Schedules: business hours"],
        "narration": (
            "Under every module is a layer people forget to load. Users with a department, a "
            "location and a manager. Groups with a manager and members. Locations with a time "
            "zone. A business hours schedule. Skip these and the module looks broken: an "
            "incident with no caller, no assignment group and no schedule is not a bug, it is "
            "missing foundation data. Load them in dependency order, company, location, "
            "department, users, groups, schedules. Reversing that order creates orphans you "
            "will chase for weeks."
        ),
        "ui": {"kind": "load", "path": "load_data.do", "title": "Foundation load order",
               "steps": ["1  Company", "2  Location", "3  Department",
                         "4  Users", "5  Groups", "6  Schedules"]},
        "beats": [(0.2, "step0"), (0.45, "step3"), (0.7, "step5")],
    },
    {
        "title": "One process, two people",
        "kicker": "scene 6 · impersonation and the SLA clock",
        "screen": ["Impersonate a requester, raise an incident",
                   "Stop impersonating, assign the group, resolve",
                   "Show the Task SLA record"],
        "narration": (
            "Here is the whole idea in one flow. I impersonate an employee and raise an "
            "incident. Notice what they can see: almost nothing, by design. Back as an agent, I "
            "pick it up, assign a group, work it, resolve it. Now look at task SLA: a record "
            "with a clock that started when the ticket did and will pause when the state "
            "pauses. That is the difference between a promise in a contract and a number "
            "somebody can actually watch."
        ),
        "ui": {"kind": "flow", "path": "incident.do · process", "title": "Incident lifecycle",
               "nodes": ["Requester raises", "Agent assigns", "Agent resolves", "SLA clock"],
               "related": ["Task SLA · has breached", "Approvers", "Work notes"]},
        "beats": [(0.18, "node0"), (0.42, "node1"), (0.68, "node3"), (0.86, "related")],
    },
    {
        "title": "Automation and integration",
        "kicker": "scene 7 · flows, then a REST call",
        "screen": ["Flow Designer: open one out-of-the-box flow",
                   "REST Message: test it, show the response body",
                   "System Logs, Outbound HTTP Requests"],
        "narration": (
            "Automation lives in flow designer. Before you build one, open an existing flow and "
            "read it out loud: trigger, condition, action. Most requirements are already a flow "
            "you can copy. Integrations are the same discipline in a different shape: a "
            "request, a body, a status code, and a record. Test the endpoint outside the "
            "platform first, then look at outbound HTTP requests before you blame the other "
            "system. That log answers more integration questions than any document."
        ),
        "ui": {"kind": "flow", "path": "flow_designer.do", "title": "Flow: new high incident",
               "nodes": ["Trigger: incident created", "Condition: priority = 1",
                         "Action: notify group", "Action: call REST"],
               "related": ["Outbound HTTP Requests · 200 OK"]},
        "beats": [(0.18, "node0"), (0.4, "node1"), (0.62, "node2"), (0.84, "related")],
    },
    {
        "title": "What to do next",
        "kicker": "scene 8 · the order that works",
        "screen": ["ServiceNow Fundamentals, then Administration Fundamentals",
                   "CSA before any CIS specialization",
                   "Then one lab per module"],
        "narration": (
            "If you are starting: ServiceNow Fundamentals, then administration fundamentals, "
            "then the certified system administrator path. That last one gates every "
            "specialisation, so take it before a product certification rather than after. "
            "Automation before scripting. Measurement once you have something worth measuring. "
            "And do the lab next to every course, because a course without a lab teaches you to "
            "recognise a screen, not to build one. The order and the labs are in this "
            "repository. Start with the orientation lab, and record your own version of this "
            "video when you finish it."
        ),
        "ui": {"kind": "load", "path": "docs/10-course-path.md", "title": "Course order",
               "steps": ["1  ServiceNow Fundamentals", "2  Administration Fundamentals",
                         "3  Certified System Administrator", "4  One lab per module"]},
        "beats": [(0.25, "step0"), (0.55, "step2"), (0.82, "step3")],
    },
]

# geometry of each painted element, filled by draw_ui()
GEOM: dict[str, tuple[int, int, int, int]] = {}


def rrect(d: ImageDraw.ImageDraw, box, r=10, fill=PANEL, outline=(31, 44, 71), width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def draw_ui(img: Image.Image, ui: dict, accent) -> dict[str, tuple[int, int, int, int]]:
    """Paint the mock screen and return {element_id: (x0, y0, x1, y1)} for the cursor."""
    d = ImageDraw.Draw(img)
    geom: dict[str, tuple[int, int, int, int]] = {}

    rrect(d, (PX, PY, PX + PW, PY + PH), r=14, fill=(13, 20, 36), outline=(38, 52, 82))
    # window chrome
    d.rounded_rectangle((PX, PY, PX + PW, PY + 34), radius=14, fill=(22, 33, 58))
    d.rectangle((PX, PY + 24, PX + PW, PY + 34), fill=(22, 33, 58))
    for i, c in enumerate([(239, 108, 108), (245, 191, 79), (98, 197, 84)]):
        d.ellipse((PX + 14 + i * 18, PY + 11, PX + 24 + i * 18, PY + 21), fill=c)
    d.rounded_rectangle((PX + 78, PY + 8, PX + PW - 14, PY + 26), radius=6, fill=(9, 14, 26))
    d.text((PX + 88, PY + 11), f"service-now.com/{ui['path']}", font=font(12), fill=DIM)

    kind = ui["kind"]
    x0, y0 = PX + 16, PY + 50
    inner_w = PW - 32

    if kind in ("nav", "list"):
        # filter navigator strip
        box = (x0, y0, x0 + inner_w, y0 + 34)
        rrect(d, box, r=8, fill=(11, 18, 33), outline=(45, 60, 94))
        d.text((x0 + 10, y0 + 9), "Filter:  " + (ui.get("query") or "Filter navigator"),
               font=font(14), fill=INK if ui.get("query") else MUTED)
        geom["filter"] = box
        y = y0 + 46

        if kind == "nav":
            d.text((x0, y), "Menus", font=font(12, True), fill=DIM)
            y += 22
            for i, item in enumerate(ui["results"]):
                box = (x0, y, x0 + inner_w, y + 30)
                rrect(d, box, r=7, fill=(17, 27, 48) if i % 2 else (19, 30, 53), outline=(32, 45, 74))
                d.text((x0 + 12, y + 7), item, font=font(14), fill=INK)
                geom[f"row{i}"] = box
                y += 34
            geom["menubar"] = (x0, y + 4, x0 + inner_w, y + 34)
            rrect(d, geom["menubar"], r=7, fill=(17, 27, 48), outline=(32, 45, 74))
            d.text((x0 + 12, y + 11), "All  ›  Favorites  ›  History", font=font(13), fill=MUTED)
        else:
            d.text((x0, y), "Incidents   ·   " + str(len(ui["rows"])) + " rows",
                   font=font(13, True), fill=MUTED)
            y += 22
            for i, (num, short, state, pri) in enumerate(ui["rows"]):
                box = (x0, y, x0 + inner_w, y + 38)
                rrect(d, box, r=7, fill=(17, 27, 48) if i % 2 == 0 else (19, 30, 53), outline=(32, 45, 74))
                d.text((x0 + 10, y + 11), num, font=font(12), fill=accent)
                d.text((x0 + 100, y + 10), short, font=font(13), fill=INK)
                d.text((x0 + 340, y + 11), state, font=font(12), fill=MUTED)
                d.text((x0 + 460, y + 11), pri, font=font(12), fill=MUTED)
                geom[f"row{i}"] = box
                y += 42

    elif kind == "form":
        d.text((x0, y0), ui["title"], font=font(15, True), fill=accent)
        geom["header"] = (x0, y0 - 4, x0 + 260, y0 + 20)
        y = y0 + 28
        for label, value in ui["fields"]:
            d.text((x0, y + 6), label, font=font(12), fill=MUTED)
            d.text((x0 + 170, y + 4), value, font=font(13), fill=INK)
            d.line((x0, y + 28, x0 + inner_w, y + 28), fill=(28, 40, 66))
            y += 34
        geom["fields"] = (x0, y0, x0 + inner_w, y + 2)
        y += 8
        d.text((x0, y), "Related lists", font=font(12, True), fill=DIM)
        y += 20
        for i, rl in enumerate(ui["related"]):
            h = 34
            box = (x0, y, x0 + inner_w, y + h)
            rrect(d, box, r=7, fill=(17, 27, 48), outline=(32, 45, 74))
            d.text((x0 + 10, y + 8), "▸ " + rl, font=font(13), fill=INK)
            geom["related" if i == 0 else f"rel{i}"] = box
            y += h + 6

    elif kind == "dict":
        d.text((x0, y0), ui["title"], font=font(14, True), fill=accent)
        geom["header"] = (x0, y0 - 4, x0 + inner_w, y0 + 20)
        y = y0 + 28
        d.text((x0 + 8, y), "column", font=font(12, True), fill=DIM)
        d.text((x0 + 260, y), "type", font=font(12, True), fill=DIM)
        d.text((x0 + 400, y), "mandatory", font=font(12, True), fill=DIM)
        y += 20
        d.line((x0, y, x0 + inner_w, y), fill=(38, 52, 82))
        y += 8
        for i, (col, typ, mand) in enumerate(ui["columns"]):
            box = (x0, y, x0 + inner_w, y + 36)
            rrect(d, box, r=7, fill=(17, 27, 48) if i % 2 == 0 else (19, 30, 53), outline=(32, 45, 74))
            d.text((x0 + 10, y + 10), col, font=font(13), fill=INK)
            d.text((x0 + 260, y + 10), typ, font=font(12), fill=MUTED)
            mbox = (x0 + 400, y + 8, x0 + 470, y + 28)
            rrect(d, mbox, r=5, fill=(22, 45, 40) if mand == "true" else (34, 30, 46),
                  outline=(40, 120, 90) if mand == "true" else (70, 55, 95))
            d.text((x0 + 408, y + 10), mand, font=font(12), fill=(110, 231, 183) if mand == "true" else (196, 181, 253))
            if i == 0:
                geom["col0"] = box
                geom["mandatory"] = mbox
            y += 40

    elif kind == "load":
        d.text((x0, y0), ui["title"], font=font(14, True), fill=accent)
        y = y0 + 26
        for i, step in enumerate(ui["steps"]):
            box = (x0, y, x0 + inner_w, y + 36)
            rrect(d, box, r=8, fill=(17, 27, 48) if i % 2 == 0 else (19, 30, 53), outline=(32, 45, 74))
            d.ellipse((x0 + 12, y + 12, x0 + 24, y + 24), fill=accent)
            d.text((x0 + 36, y + 9), step, font=font(14), fill=INK)
            geom[f"step{i}"] = box
            y += 42

    elif kind == "flow":
        y = y0
        for i, node in enumerate(ui["nodes"]):
            box = (x0, y, x0 + inner_w, y + 40)
            rrect(d, box, r=8, fill=(17, 27, 48), outline=(45, 62, 96))
            d.rectangle((x0, y, x0 + 4, y + 40), fill=accent)
            d.text((x0 + 16, y + 11), node, font=font(13), fill=INK)
            geom[f"node{i}"] = box
            if i < len(ui["nodes"]) - 1:
                d.line((x0 + inner_w // 2, y + 40, x0 + inner_w // 2, y + 48), fill=(60, 80, 120))
            y += 48
        for i, rl in enumerate(ui.get("related", [])):
            box = (x0, y + 6, x0 + inner_w, y + 40)
            rrect(d, box, r=7, fill=(20, 33, 55), outline=(45, 62, 96))
            d.text((x0 + 12, y + 15), "▸ " + rl, font=font(13), fill=(148, 226, 213))
            geom["related"] = box
            y += 40

    return geom


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def base_slide(scene: dict, index: int, total: int) -> tuple[Image.Image, dict]:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    accent = ACCENTS[index % len(ACCENTS)]

    d.rectangle([0, 0, W, 6], fill=accent)
    d.text((64, 46), scene["kicker"].upper(), font=font(18, True), fill=accent)
    d.text((64, 76), scene["title"], font=font(40, True), fill=INK)
    d.text((W - 64, 52), f"{index + 1}/{total}", font=font(20, True), fill=MUTED)

    # left column: what to do for real, then the narration
    y = 150
    d.text((64, y), "ON YOUR INSTANCE", font=font(14, True), fill=DIM)
    y += 26
    for line in scene["screen"]:
        for seg in wrap(d, line, font(17), 500)[:2]:
            d.text((64, y), seg, font=font(17), fill=(203, 213, 225))
            y += 24
        y += 4
    y += 14
    nar = wrap(d, scene["narration"], font(18), 500)
    for line in nar[:11]:
        d.text((64, y), line, font=font(18), fill=(148, 163, 184))
        y += 26

    geom = draw_ui(img, scene["ui"], accent)

    d.text((64, H - 46), "ServiceNow Learning · buffy · mimo-v2.6-flash · generated walkthrough",
           font=font(15), fill=DIM)
    d.text((W - 64, H - 46), "stylised mock UI — not a live-instance recording",
           font=font(15), fill=DIM, anchor="ra")
    return img, geom


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def cursor_points(geom: dict, beats: list, dur: float) -> list[tuple[float, str, int, int]]:
    """[(arrival_time, element_id, x, y)] — one per beat, in element centres."""
    out = []
    for frac, el in beats:
        box = geom.get(el)
        if not box:
            continue
        cx = (box[0] + box[2]) // 2
        cy = (box[1] + box[3]) // 2
        out.append((dur * frac, el, cx, cy))
    return out


def draw_cursor(img: Image.Image, x: float, y: float, click: float) -> None:
    """Arrow plus an expanding click ring; `click` is 0..1 of the pulse."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if click > 0:
        r = 8 + 26 * click
        alpha = int(180 * (1 - click))
        d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 255, alpha), width=3)
    pts = [(x, y), (x + 13, y + 13), (x + 6, y + 14), (x + 10, y + 22),
           (x + 6, y + 24), (x + 2, y + 16), (x - 2, y + 21)]
    d.polygon(pts, fill=(255, 255, 255, 255), outline=(13, 20, 36, 255))
    img.paste(layer, (0, 0), layer)


def draw_highlight(img: Image.Image, box, accent, alpha_frac: float) -> None:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pad = 4
    d.rounded_rectangle((box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad),
                        radius=9, outline=(*accent, 235), width=3)
    d.rounded_rectangle((box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad),
                        radius=9, fill=(*accent, int(38 * alpha_frac)))
    img.paste(layer, (0, 0), layer)


def require(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        sys.exit(f"missing required tool: {tool}")
    return path


def tts(text: str, out_wav: Path, wpm: int = 148) -> None:
    subprocess.run(["espeak-ng", "-v", "en-us", "-s", str(wpm), "-p", "35", "-a", "160",
                    "-w", str(out_wav), text], check=True, capture_output=True)


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(path)],
                         check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def vtt_time(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def render_scene_frames(scene, i, total, dur, frames_dir) -> None:
    base, geom = base_slide(scene, i, total)
    accent = ACCENTS[i % len(ACCENTS)]
    points = cursor_points(geom, scene["beats"], dur)
    n = max(1, int(round(dur * FPS)))

    # cursor starts at the first target so the very first frame is not empty
    start = points[0][2:] if points else (PX + PW // 2, PY + PH // 2)

    for f in range(n):
        t = f / FPS
        img = base.copy()

        x, y = start
        click = 0.0
        active_el = None
        age = 0.0

        if points:
            prev_t, px, py = -0.8, *start
            prev_el = None
            for (at, el, cx, cy) in points:
                if t >= at:
                    travel = 0.8
                    if t < at + travel:
                        k = ease((t - at) / travel)
                        x, y = px + (cx - px) * k, py + (cy - py) * k
                    else:
                        x, y = cx, cy
                    click = (t - at) / 0.35
                    active_el = el
                    age = t - at
                    prev_t, px, py, prev_el = at, cx, cy, el
                else:
                    # travelling toward the next beat: keep the previous target highlighted
                    active_el = prev_el
                    age = 9.0
                    if t > at - 0.8:
                        k = ease((t - (at - 0.8)) / 0.8)
                        x, y = px + (cx - px) * k, py + (cy - py) * k
                    break

        # A highlight persists until the cursor moves to the next target: a ring that vanishes
        # after two seconds leaves most frames with nothing marked, which reads as a slideshow.
        if active_el and active_el in geom:
            draw_highlight(img, geom[active_el], accent, min(1.0, 0.35 + age))

        draw_cursor(img, x, y, click if 0 <= click <= 1 else 0.0)
        img.save(frames_dir / f"s{i:02d}_{f:05d}.png")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--keep-frames", action="store_true")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe", "espeak-ng"):
        print(f"{tool}: {require(tool)}")
    if args.check:
        return

    OUTDIR.mkdir(exist_ok=True)
    vtt: list[str] = ["WEBVTT", ""]

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        parts: list[Path] = []
        clock = 0.0

        for i, scene in enumerate(SCENES):
            wav = tmp / f"s{i:02d}.wav"
            mp4 = tmp / f"s{i:02d}.mp4"
            frames = tmp / f"frames{i:02d}"
            frames.mkdir()

            tts(scene["narration"], wav)
            d_audio = duration(wav)
            dur = d_audio + 1.1  # a beat of silence so the highlight can settle
            render_scene_frames(scene, i, len(SCENES), d_audio, frames)

            subprocess.run([
                "ffmpeg", "-y", "-loglevel", "error",
                "-framerate", str(FPS), "-i", str(frames / f"s{i:02d}_%05d.png"),
                "-i", str(wav),
                "-af", "apad=pad_dur=1.1",
                "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                "-pix_fmt", "yuv420p", "-r", "25",
                "-c:a", "aac", "-b:a", "128k", "-shortest", str(mp4),
            ], check=True)
            parts.append(mp4)

            vtt += [f"{vtt_time(clock)} --> {vtt_time(clock + dur)}", scene["narration"], ""]
            clock += dur
            print(f"scene {i + 1}/{len(SCENES)}: {dur:5.1f}s  {len(scene['beats'])} beats  "
                  f"{scene['title']}")

        listing = tmp / "list.txt"
        listing.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
        final = OUTDIR / "getting-started.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", str(listing), "-c", "copy", "-movflags", "+faststart",
                        str(final)], check=True)

    (OUTDIR / "getting-started.vtt").write_text("\n".join(vtt), encoding="utf-8")
    total = duration(final)
    print(f"\nwrote {final.relative_to(ROOT)} — {int(total // 60)}m{int(total % 60):02d}s, "
          f"{final.stat().st_size / 1_048_576:.1f} MB")
    print(f"wrote {(OUTDIR / 'getting-started.vtt').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
