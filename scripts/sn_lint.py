#!/usr/bin/env python3
"""sn_lint.py — keep the kit honest.

    python3 scripts/sn_lint.py           # human readable
    python3 scripts/sn_lint.py --quiet   # exit code only

Checks (each one exists because it caught a real problem):
  1. Every doc has a title, an AGENT stamp and an UPDATED date — so a reader knows how stale
     it is and who to ask.
  2. Every doc has an "Official sources" section, containing at least one URL, and EVERY
     URL in that section is on the ServiceNow allowlist. This is the "official sources only"
     rule, enforced instead of hoped for.
  3. No TODO/TBD/FIXME left in published prose.
  4. Every relative link resolves on disk (no dead links on the Pages site).
  5. data/modules.json: unique ids, required keys, labs that exist.
  6. data/sources.json: allowlist present and non-empty.
  7. Infographics referenced by the site exist as .svg and .png.

Exit code 1 if anything fails.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
# Only the docs this kit owns are held to the conventions below. Contributed material that
# arrived by merge lives in subdirectories (docs/<topic>/, labs/<lab>/) and is vendored as-is —
# rewriting someone else's file to satisfy our lint would misrepresent their work.
DOCS = (
    sorted(p for p in (ROOT / "docs").glob("*.md"))
    + sorted((ROOT / "labs").glob("*.md"))
    + [ROOT / "README.md"]
)
REQUIRED_MODULE_KEYS = {"id", "name", "app", "why", "primary_table", "tables", "roles",
                        "breadcrumbs", "fields", "must_know", "mistakes", "timebox_min", "quiz"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://[^\s)>\]]+")


class Result:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def load_allowlist() -> list[str]:
    data = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
    return data.get("allowlisted_domains", [])


def check_doc(path: Path, allow: list[str], res: Result) -> None:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")

    if not text.lstrip().startswith("# "):
        res.err(f"{rel}: no H1 title")
    if "**Agent:**" not in text:
        res.err(f"{rel}: missing '**Agent:**' stamp")
    if not re.search(r"\*\*Updated:\*\*\s*\d{4}-\d{2}-\d{2}", text):
        res.err(f"{rel}: missing '**Updated:** YYYY-MM-DD'")

    for bad in ("TODO", "TBD", "FIXME", "XXX"):
        if re.search(rf"\b{bad}\b", text):
            res.err(f"{rel}: contains {bad}")

    # official sources section
    m = re.search(r"^## Official sources\s*$((?:(?!^## ).)*)", text, re.S | re.M)
    if not m:
        res.err(f"{rel}: no '## Official sources' section")
    else:
        section = m.group(1)
        urls = URL_RE.findall(section)
        if not urls:
            res.err(f"{rel}: 'Official sources' has no URL")
        for u in urls:
            host = urlparse(u).netloc.lower()
            if not any(host == d or host.endswith("." + d) for d in allow):
                res.err(f"{rel}: non-official source in 'Official sources': {u}")

    # relative links resolve
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#")[0]
        if not clean:
            continue
        candidate = (path.parent / clean).resolve()
        if not candidate.exists():
            # allow links that point at generated files not yet built
            if "generated/" in clean:
                res.warn(f"{rel}: link to generated file not built yet: {clean}")
            else:
                res.err(f"{rel}: dead relative link -> {clean}")


def check_modules(res: Result) -> None:
    path = ROOT / "data" / "modules.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    seen = set()
    for mod in data.get("modules", []):
        missing = REQUIRED_MODULE_KEYS - set(mod)
        if missing:
            res.err(f"modules.json [{mod.get('id', '?')}]: missing keys {sorted(missing)}")
        mid = mod.get("id")
        if mid in seen:
            res.err(f"modules.json: duplicate id {mid}")
        seen.add(mid)
        for lab in mod.get("labs", []):
            if not (ROOT / lab).exists():
                res.err(f"modules.json [{mid}]: lab missing on disk -> {lab}")


def check_infographics(res: Result) -> None:
    for name in ("learning-loop", "module-anatomy", "integration-flow"):
        for ext in ("svg", "png"):
            p = ROOT / "infographics" / f"{name}.{ext}"
            if not p.exists():
                res.err(f"infographics: missing {p.name} (run: python3 scripts/make_infographic.py)")


def main() -> None:
    res = Result()
    allow = load_allowlist()
    if not allow:
        res.err("sources.json: allowlisted_domains empty")

    for doc in DOCS:
        if doc.exists():
            check_doc(doc, allow, res)

    check_modules(res)
    check_infographics(res)

    quiet = "--quiet" in sys.argv
    if not quiet:
        for w in res.warnings:
            print(f"warn  {w}")
        for e in res.errors:
            print(f"ERROR {e}")
        print(f"\nchecked {len([d for d in DOCS if d.exists()])} docs · "
              f"{len(res.errors)} errors · {len(res.warnings)} warnings")
    sys.exit(1 if res.errors else 0)


if __name__ == "__main__":
    main()
