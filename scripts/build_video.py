#!/usr/bin/env python3
"""build_video.py — render the getting-started video from docs/11-video-guide.md.

    python3 scripts/build_video.py                 # build video/getting-started.mp4
    python3 scripts/build_video.py --check         # verify tooling only

What this produces: a slide-and-narration video, 1280x720, roughly eight minutes, with
burned-in captions and a matching .vtt. Every scene states what to show on a real instance;
the footage itself has to be your own, because this repo has no ServiceNow instance to
screen-record.

That distinction is the whole point, so it is stated on screen and in the README: a narrated
deck is a rehearsal script you can watch, not a screencast of a live PDI.

Requires: ffmpeg + espeak-ng + PIL (DejaVu fonts).
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "video"
W, H = 1280, 720

BG = (11, 17, 32)
PANEL = (17, 28, 51)
INK = (229, 236, 247)
MUTED = (148, 163, 184)
ACCENTS = [(56, 189, 248), (167, 139, 250), (34, 211, 238), (52, 211, 153),
           (249, 115, 22), (244, 114, 182), (96, 165, 250), (250, 204, 21)]


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


# ---- the eight scenes (mirrors docs/11-video-guide.md, with fuller narration) -----------
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
    },
]


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


def render_scene(scene: dict, index: int, total: int) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    accent = ACCENTS[index % len(ACCENTS)]

    # header band
    d.rectangle([0, 0, W, 6], fill=accent)
    d.text((64, 56), scene["kicker"].upper(), font=font(20, True), fill=accent)
    d.text((64, 92), scene["title"], font=font(48, True), fill=INK)
    d.text((W - 64, 64), f"{index + 1}/{total}", font=font(22, True), fill=MUTED)

    # "on screen" panel
    d.rounded_rectangle([64, 190, W - 64, 340], radius=16, fill=PANEL, outline=(31, 44, 71))
    d.text((92, 214), "ON YOUR INSTANCE", font=font(17, True), fill=MUTED)
    y = 250
    for line in scene["screen"]:
        d.text((92, y), line, font=font(24), fill=INK)
        y += 38

    # narration
    nar_f = font(24)
    lines = wrap(d, scene["narration"], nar_f, W - 160)
    y = 386
    for line in lines[:9]:
        d.text((64, y), line, font=nar_f, fill=(203, 213, 225))
        y += 36

    # footer
    d.text((64, H - 58), "ServiceNow Learning · buffy · mimo-v2.6-flash · 2026-11-04",
           font=font(18), fill=(100, 116, 139))
    d.text((W - 64, H - 58), "narration over slides — not a live-instance screencast",
           font=font(18), fill=(100, 116, 139), anchor="ra")
    return img


def require(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        sys.exit(f"missing required tool: {tool}")
    return path


def tts(text: str, out_wav: Path, wpm: int = 145) -> None:
    subprocess.run(
        ["espeak-ng", "-v", "en-us", "-s", str(wpm), "-p", "35", "-a", "160", "-w", str(out_wav), text],
        check=True, capture_output=True,
    )


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
         "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


def vtt_time(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
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
            png = tmp / f"s{i:02d}.png"
            mp4 = tmp / f"s{i:02d}.mp4"

            tts(scene["narration"], wav)
            dur = duration(wav) + 0.9  # a beat of silence after each scene
            render_scene(scene, i, len(SCENES)).save(png)

            subprocess.run([
                "ffmpeg", "-y", "-loglevel", "error",
                "-loop", "1", "-i", str(png), "-i", str(wav),
                "-af", "apad=pad_dur=0.9",
                "-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "26",
                "-pix_fmt", "yuv420p", "-r", "25",
                "-c:a", "aac", "-b:a", "128k",
                "-shortest", str(mp4),
            ], check=True)
            parts.append(mp4)

            vtt += [f"{vtt_time(clock)} --> {vtt_time(clock + dur)}",
                    scene["narration"], ""]
            clock += dur
            print(f"scene {i + 1}/{len(SCENES)}: {dur:5.1f}s  {scene['title']}")

        listing = tmp / "list.txt"
        listing.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
        final = OUTDIR / "getting-started.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
            "-i", str(listing), "-c", "copy", "-movflags", "+faststart", str(final),
        ], check=True)

        (OUTDIR / "getting-started.vtt").write_text("\n".join(vtt), encoding="utf-8")

    total = duration(final)
    size_mb = final.stat().st_size / 1_048_576
    print(f"\nwrote {final.relative_to(ROOT)} — {int(total // 60)}m{int(total % 60):02d}s, {size_mb:.1f} MB")
    print(f"wrote {(OUTDIR / 'getting-started.vtt').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
