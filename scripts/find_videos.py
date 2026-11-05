#!/usr/bin/env python3
"""find_videos.py — resolve real, official ServiceNow video links for a topic list.

    python3 scripts/find_videos.py                 # resolve + verify, write data/video_links.json
    python3 scripts/find_videos.py --report        # print a markdown table from the JSON
    python3 scripts/find_videos.py --verify        # CI: re-check every published link, exit 1 on failure

--verify is what CI runs: it never searches and never writes, so a push cannot silently
"fix" the table by swapping in whatever search happens to return that day. It fails the build
if a published video is gone, renamed, or re-uploaded to a non-ServiceNow channel.

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
import html
import json
import os
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

# One entry per topic. `match` is a case-insensitive substring of the real title — pinned so
# resolution is deterministic instead of "highest score wins today". `kind` is published next
# to the link, because a conference keynote and a six-part teaching series are not the same
# thing and a reader deserves to know which they are about to watch.
TOPICS = [
    {"key": "fundamentals", "label": "ServiceNow Fundamentals",
     "query": "ServiceNow Foundations", "match": "where do i fit",
     "channels": ["devprogram"], "kind": "teaching series (#1 of 6)"},
    {"key": "admin", "label": "ServiceNow Administration Fundamentals",
     "query": "ServiceNow Foundations", "match": "get started building",
     "channels": ["devprogram"], "kind": "teaching series (#2 of 6) — the closest official "
                                     "material to admin basics"},
    {"key": "sam-overview", "label": "SAM overview",
     "query": "asset management", "match": "what's new in it asset management",
     "channels": ["servicenow"], "kind": "conference keynote (Knowledge 2022), feature tour"},
    {"key": "ham", "label": "Hardware Asset Management overview",
     "query": "asset management", "match": "what's new in it asset management",
     "channels": ["servicenow"], "kind": "same keynote — no separate HAM video exists"},
    {"key": "license", "label": "Software license management",
     "query": "software asset management", "match": "southstate bank",
     "channels": ["servicenow"], "kind": "customer story, not a how-to"},
    {"key": "procurement", "label": "Procurement and contract management",
     "query": "procurement", "match": "put ai to work in procurement",
     "channels": ["servicenow"], "kind": "product/marketing"},
    {"key": "cmdb", "label": "CMDB fundamentals",
     "query": "CMDB", "match": "model your data",
     "channels": ["devprogram"], "kind": "teaching series (#4 of 6) — data model and CMDB"},
    {"key": "integration", "label": "IntegrationHub and Discovery",
     "query": "IntegrationHub", "match": "integrationhub overview",
     "channels": ["devprogram"], "kind": "teaching series — Integrations on the Now Platform"},
]

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}


def fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


# Channel ids for the two official channels, resolved with
#   channels.list?part=id&forHandle=@ServiceNow
# on 2026-11-04 (and re-resolvable the same way if a handle ever moves). Searching *inside* a
# channel is what makes the query matter: a global search returns third-party creators first,
# which is how an earlier pass ended up with nothing for Fundamentals/CMDB.
CHANNEL_IDS = {
    "servicenow": "UCLukrOQYSgsHUR_NSiVZndQ",
    "devprogram": "UCdXorgCT87YlFRN9n8oJ7_A",
}

# channelTitle values the Data API returns for the same channels as OFFICIAL_AUTHORS.
OFFICIAL_CHANNEL_TITLES = {"servicenow", "servicenow dev program"}


def api_key() -> str | None:
    """YouTube Data API v3 key, if this environment has one.

    Two names because that is how it is actually exported here (YOUTUBE_API_V3_KEY) while the
    documented name is plainer. Never printed, never committed.
    """
    for name in ("YOUTUBE_API_KEY", "YOUTUBE_API_V3_KEY"):
        v = os.environ.get(name, "").strip()
        if v:
            return v
    return None


def api_search(query: str, channel_id: str, limit: int = 25) -> list[tuple[str, str]]:
    """Search *within one official channel* via the Data API.

    The API honours the query (the channel search *page* does not — it returns channel promo
    content regardless of the term), and returns relevance-ordered results, which is why it is
    the preferred path whenever a key exists.
    """
    key = api_key()
    if not key:
        return []
    params = urllib.parse.urlencode({
        "part": "snippet", "type": "video", "maxResults": str(limit),
        "q": query, "channelId": channel_id, "key": key,
    })
    try:
        data = json.loads(fetch(f"https://www.googleapis.com/youtube/v3/search?{params}", timeout=30))
    except Exception as exc:  # noqa: BLE001 - quota/network problems fall back to page search
        print(f"  ! api search failed for {query!r}: {type(exc).__name__}", file=sys.stderr)
        return []

    out: list[tuple[str, str]] = []
    for item in data.get("items", []):
        vid = (item.get("id") or {}).get("videoId")
        snip = item.get("snippet") or {}
        channel = (snip.get("channelTitle") or "").strip()
        if not vid or channel.lower() not in OFFICIAL_CHANNEL_TITLES:
            continue
        # API titles arrive HTML-escaped ("What&#39;s New…"); unescape or every apostrophe
        # in a pinned `match` silently fails to match.
        out.append((vid, html.unescape(snip.get("title") or "")))
    return out


def search_channel(channel_url: str, query: str) -> list[tuple[str, str]]:
    """Fallback: parse a channel search page. Does not honour the query well; last resort."""
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
            pairs.append((vid.group(1), html.unescape(title.group(1).encode().decode("unicode_escape", "ignore"))))
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


def verify_published() -> int:
    """Re-check every link already in data/video_links.json. Returns an exit code."""
    if not OUT.exists():
        print(f"FAIL: {OUT.relative_to(ROOT)} is missing", file=sys.stderr)
        return 1
    data = json.loads(OUT.read_text(encoding="utf-8"))
    failures: list[str] = []
    checked = 0

    for key, entry in data.get("topics", {}).items():
        video = entry.get("video")
        if not video:
            # A named gap is a pass: refusing to invent a link is the correct state.
            print(f"  gap   {key}: no published video (expected)")
            continue
        checked += 1
        info = verify(video["id"])
        if info is None:
            failures.append(f"{key}: {video['url']} no longer resolves to a ServiceNow-owned video")
            print(f"  FAIL  {key}: {video['url']}")
            continue
        if info["title"].strip() != video["title"].strip():
            failures.append(
                f"{key}: title changed\n         published: {video['title']}\n         now:       {info['title']}"
            )
            print(f"  FAIL  {key}: title drifted -> {info['title']}")
            continue
        print(f"  ok    {key}: {info['title']} ({info['author']})")
        time.sleep(0.2)

    expected = len(data.get("topics", {}))
    if checked == 0:
        failures.append("no published videos to verify — the table is empty")

    print(f"\nverified {checked}/{expected} published links")
    for f in failures:
        print(f"\nFAIL: {f}", file=sys.stderr)
    if failures:
        print("\nRe-resolve with: python3 scripts/find_videos.py  (then review the diff before committing)",
              file=sys.stderr)
        return 1
    print("all published video links are still live and still ServiceNow-owned")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="print the markdown table instead of searching")
    ap.add_argument("--verify", action="store_true", help="re-check published links only (no search, no write)")
    args = ap.parse_args()

    if args.verify:
        sys.exit(verify_published())

    if args.report:
        if not OUT.exists():
            sys.exit("no data/video_links.json yet — run without --report first")
        data = json.loads(OUT.read_text(encoding="utf-8"))
        print("| Topic | Verified video | Type |")
        print("|---|---|---|")
        for topic, entry in data["topics"].items():
            if entry.get("video"):
                v = entry["video"]
                title = v["title"].replace("|", "\\|")
                kind = entry.get("kind", "").replace("|", "\\|")
                print(f"| {entry['label']} | [{title}]({v['url']}) | {kind} |")
            else:
                print(f"| {entry['label']} | _no verified match_ | — |")
        return

    result = {"generated": time.strftime("%Y-%m-%d"),
              "method": ("youtube data api v3 search (official channels only) + oEmbed verification"
                         if api_key() else
                         "youtube channel search pages + oEmbed verification"),
              "topics": {}}

    for topic in TOPICS:
        key, label = topic["key"], topic["label"]
        print(f"[{key}] {label}  (expecting: {topic['match']!r})")

        candidates: list[tuple[str, str]] = []
        if api_key():
            for ch in topic["channels"]:
                hits = api_search(topic["query"], CHANNEL_IDS[ch])
                if not hits:
                    print(f"   ! no API hits inside @{ch} for {topic['query']!r}")
                candidates += hits
        else:
            for ch in topic["channels"]:
                candidates += search_channel(CHANNELS[ch], topic["query"])[:8]

        best = None
        for vid, title in candidates:
            if topic["match"] not in title.lower():
                continue
            info = verify(vid)
            if not info:
                continue
            # The pinned title must survive verification too: a re-upload with a different
            # title is exactly the drift this table must not silently absorb.
            best = info
            break

        if best:
            print(f"   -> {best['title']} ({best['author']}) {best['url']}")
        else:
            print("   -> no verified match")
        result["topics"][key] = {"label": label, "kind": topic["kind"],
                                 "match": topic["match"], "video": best}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    found = sum(1 for t in result["topics"].values() if t["video"])
    print(f"\nwrote {OUT.relative_to(ROOT)} — {found}/{len(TOPICS)} topics resolved to official videos")


if __name__ == "__main__":
    main()
