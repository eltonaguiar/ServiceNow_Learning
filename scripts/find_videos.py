#!/usr/bin/env python3
"""find_videos.py — resolve real, official ServiceNow video links for a topic list.

    python3 scripts/find_videos.py                 # resolve + verify, write data/video_links.json
    python3 scripts/find_videos.py --report        # print a markdown table from the JSON

Why this exists: hand-written "video link" tables rot, and inventing a video id is the
worst possible failure — it looks authoritative and 404s. So every candidate is checked
against YouTube's oEmbed endpoint, which returns the real title and channel. Anything whose
author is not a ServiceNow-owned channel is dropped, not "best guess"-ed.

Method (deliberately small): one search page per topic from each official channel, parse the
video ids out of the page, verify each with oEmbed, score by keyword overlap with the topic,
keep the best verified match. No API key, no bulk crawling — 2 requests per topic plus one
verification per candidate.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "video_links.json"

CHANNELS = {
    "servicenow": "https://www.youtube.com/@ServiceNow",
    "devprogram": "https://www.youtube.com/@ServiceNowDevProgram",
}
# oEmbed's author_name values that count as ServiceNow-owned.
OFFICIAL_AUTHORS = {"servicenow", "servicenow dev program"}

TOPICS = [
    ("fundamentals", "ServiceNow Fundamentals", ["fundamentals"], ["servicenow"]),
    ("admin", "ServiceNow Administration Fundamentals", ["administration", "fundamentals"], ["servicenow"]),
    ("sam-overview", "SAM overview", ["software asset", "asset management", "sam"], ["servicenow", "devprogram"]),
    ("ham", "Hardware Asset Management overview", ["hardware asset", "asset management"], ["servicenow"]),
    ("license", "Software license management", ["license", "software asset"], ["servicenow", "devprogram"]),
    ("procurement", "Procurement and contract management", ["procurement", "contract"], ["servicenow"]),
    ("cmdb", "CMDB fundamentals", ["cmdb", "configuration management"], ["servicenow", "devprogram"]),
    ("integration", "IntegrationHub and Discovery", ["integrationhub", "integration", "discovery"], ["devprogram", "servicenow"]),
]

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}


def fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def search_channel(channel_url: str, query: str) -> list[tuple[str, str]]:
    """Return [(video_id, title)] from a channel search page."""
    url = f"{channel_url}/search?query={urllib.parse.quote(query)}"
    try:
        html = fetch(url)
    except Exception as exc:  # noqa: BLE001
        print(f"  ! search failed for {query!r}: {type(exc).__name__}", file=sys.stderr)
        return []

    # Titles and ids appear as parallel arrays in ytInitialData; walk renderers in order.
    pairs: list[tuple[str, str]] = []
    for chunk in re.split(r'"videoRenderer":', html)[1:]:
        vid = re.search(r'"videoId":"([A-Za-z0-9_-]{11})"', chunk[:400])
        title = re.search(r'"title":\{"runs":\[\{"text":"([^"]{3,140})"', chunk[:2000])
        if vid and title:
            pairs.append((vid.group(1), title.group(1).encode().decode("unicode_escape", "ignore")))
    # de-duplicate, keep order
    seen, out = set(), []
    for vid, title in pairs:
        if vid not in seen:
            seen.add(vid)
            out.append((vid, title))
    return out


def verify(video_id: str) -> dict | None:
    url = ("https://www.youtube.com/oembed?format=json&url="
           + urllib.parse.quote(f"https://www.youtube.com/watch?v={video_id}", safe=""))
    try:
        data = json.loads(fetch(url, timeout=20))
    except Exception:  # noqa: BLE001 - a dead/removed video is expected sometimes
        return None
    author = (data.get("author_name") or "").strip()
    if author.lower() not in OFFICIAL_AUTHORS:
        return None
    return {"id": video_id, "title": data.get("title", ""), "author": author,
            "url": f"https://www.youtube.com/watch?v={video_id}"}


def score(title: str, keywords: list[str]) -> int:
    t = title.lower()
    return sum(3 for k in keywords if k in t)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="print the markdown table instead of searching")
    args = ap.parse_args()

    if args.report:
        if not OUT.exists():
            sys.exit("no data/video_links.json yet — run without --report first")
        data = json.loads(OUT.read_text(encoding="utf-8"))
        print("| Topic | Verified video | Channel |")
        print("|---|---|---|")
        for topic, entry in data["topics"].items():
            if entry.get("video"):
                v = entry["video"]
                print(f"| {entry['label']} | [{v['title']}]({v['url']}) | {v['author']} |")
            else:
                print(f"| {entry['label']} | _no verified match_ | — |")
        return

    result = {"generated": time.strftime("%Y-%m-%d"),
              "method": "youtube channel search + oEmbed verification; only ServiceNow-owned authors kept",
              "topics": {}}

    for key, label, keywords, channels in TOPICS:
        print(f"[{key}] {label}")
        best = None
        for ch in channels:
            for vid, title in search_channel(CHANNELS[ch], label)[:8]:
                s = score(title, keywords)
                if s == 0:
                    continue
                info = verify(vid)
                if not info:
                    continue
                info["score"] = s
                if best is None or s > best["score"]:
                    best = info
                time.sleep(0.2)
        if best:
            print(f"   -> {best['title']} ({best['author']}) {best['url']}")
        else:
            print("   -> no verified match")
        result["topics"][key] = {"label": label, "keywords": keywords, "video": best}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    found = sum(1 for t in result["topics"].values() if t["video"])
    print(f"\nwrote {OUT.relative_to(ROOT)} — {found}/{len(TOPICS)} topics resolved to official videos")


if __name__ == "__main__":
    main()
