#!/usr/bin/env python3
"""sn_sheet.py — turn sn_probe.js output into a markdown study sheet.

    python3 scripts/sn_sheet.py probe.json
    python3 scripts/sn_sheet.py probe.json --out docs/generated/probe-sheet.md
    python3 scripts/sn_sheet.py probe.json --module itom-cmdb   # focus one module

Reads the JSON printed by scripts/sn_probe.js (the block between the SNPROBE markers),
cross-references data/modules.json, and reports what your instance actually has — plus a
gap list of what the kit expected and you do not have.

Stdlib only. Never writes to ServiceNow; this is a local renderer.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ROOT / "data" / "modules.json"


def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    # Accept a raw log dump: grab the block between the markers if present.
    if "=== SNPROBE BEGIN ===" in text:
        start = text.index("=== SNPROBE BEGIN ===") + len("=== SNPROBE BEGIN ===")
        end = text.index("=== SNPROBE END ===")
        text = text[start:end].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        sys.exit(f"{path}: not valid probe JSON ({exc}). Copy only the object between the markers.")


def table_md(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


def render(probe: dict, kb: dict, focus: str | None) -> str:
    tables = probe.get("tables", {})
    gs = probe.get("guided_setup", {})
    flows = probe.get("automation", {})
    apis = probe.get("apis", {})
    analytics = probe.get("analytics", {})
    sam = probe.get("sam", {})
    plugins = probe.get("plugins", {})

    lines = [
        "# Instance study sheet",
        "",
        f"> **Agent:** buffy (mimo-v2.6-flash) · **Updated:** 2026-11-04 · **Rendered from:** probe "
        f"`{probe.get('probe_version', '?')}` generated {probe.get('generated', '?')}",
        "",
        f"**Instance:** `{probe.get('instance', 'unknown')}` · **Release:** "
        f"{probe.get('release_name', '?')} / {probe.get('release', '?')} · **Probed as:** "
        f"`{probe.get('user', '?')}`",
        "",
        "> This file is instance-specific. Do not commit it: it names your instance and user.",
        "",
        "## 1. Headline",
        "",
        table_md(
            ["Signal", "Value", "Read it as"],
            [
                ["Core tables present", f"{sum(1 for t in tables.values() if t.get('exists'))}/{len(tables)}",
                 "tables the probe asked about that exist here"],
                ["Guided Setup modules", str(gs.get("count", 0)),
                 "0 = this release/app set ships none, or your modules are named differently"],
                ["Flows (active / total)", f"{flows.get('flows_active', '?')} / {flows.get('flows_total', '?')}",
                 "OOB automation already available to copy"],
                ["Scripted REST APIs", str(apis.get("scripted_rest_apis", "?")), "inbound surface you own"],
                ["REST Messages", str(apis.get("rest_messages", "?")), "outbound integrations configured"],
                ["Indicators / reports / dashboards",
                 f"{analytics.get('indicators', '?')} / {analytics.get('reports', '?')} / {analytics.get('dashboards', '?')}",
                 "whether analytics is real here or theoretical"],
                ["SAM schema", f"{sam.get('sam_tables_found', 0)} tables",
                 "0 = SAM not installed (Foundation vs Pro matters)"],
                ["Active plugins listed", str(plugins.get("total_listed", 0)), "first 60 only"],
            ],
        ),
        "",
    ]

    # ---- foundation data
    fnd = probe.get("foundation") or {}
    lines += ["## 2. Foundation data (the layer every module assumes)", ""]
    counts = fnd.get("counts") or {}
    if counts or fnd.get("missing"):
        rows = []
        for table in sorted(set(list(counts) + (fnd.get("missing") or []))):
            if table in (fnd.get("missing") or []):
                rows.append([f"`{table}`", "—", "MISSING", "table not in this instance"])
            else:
                n = counts.get(table, 0)
                state = "EMPTY" if n == 0 else "ok"
                note = "nothing loaded — every dependent feature degrades" if n == 0 else ""
                rows.append([f"`{table}`", str(n), state, note])
        lines.append(table_md(["Object", "Rows", "State", "Read it as"], rows))
        hyg = fnd.get("hygiene") or {}
        if hyg:
            lines += ["", "**Hygiene (the numbers that predict bad reports):**", ""]
            for k, v in hyg.items():
                flag = "⚠️" if v else "✅"
                lines.append(f"- {flag} {k.replace('_', ' ')}: **{v}**")
        cmn = fnd.get("cmn_tables") or []
        if cmn:
            lines += ["", f"Schedule-related tables present: {', '.join('`'+c+'`' for c in cmn)}"]
        lines += ["", "Load order (company → location → department → cost centre → users → groups → "
                      "schedules) is in `docs/09-foundation-data.md`."]
    else:
        lines.append("_The probe did not report foundation data — re-run it with the current "
                     "`scripts/sn_probe.js`._")
    lines.append("")

    # ---- guided setup
    lines += ["## 3. Guided Setup modules found", ""]
    mods = gs.get("modules", [])
    if mods:
        lines.append(table_md(["Module title", "Target"], [[m.get("title", ""), m.get("target", "")] for m in mods]))
        lines += ["", "If an app you care about is missing here, it either has no guided setup on this "
                      "release or the module is titled differently — do not assume it is missing."]
    else:
        lines.append("**None found.** Either this instance's release/app set ships no guided setup, or "
                     "the modules use different titles. Cross-check in the filter navigator by typing "
                     "`guided setup`.")
    lines.append("")

    # ---- per-table detail
    lines += ["## 4. Per-table facts (mandatory fields are the real answer)", ""]
    for name, info in tables.items():
        if focus and focus in kb_map(kb) and name not in kb_map(kb)[focus].get("tables", []):
            continue
        if not info.get("exists"):
            lines += [f"### `{name}` — **not present**", "",
                      "The table does not exist on this instance (plugin/app not installed).", ""]
            continue
        mand = info.get("mandatory", [])
        lines += [f"### `{name}` — {info.get('label', '')} · {info.get('row_count', '?')} rows", ""]
        if mand:
            lines.append(table_md(["Mandatory field", "Type", "Label"],
                                  [[m.get("field"), m.get("type", ""), m.get("label", "")] for m in mand]))
        else:
            lines.append("_No dictionary-mandatory fields (any 'required' behaviour here is a UI or data policy)._")
        rel = info.get("related_lists") or []
        lines += ["", f"**Related lists configured:** {', '.join('`'+r+'`' for r in rel) if rel else '_none found_'}", ""]

    # ---- gaps vs the kit
    lines += ["## 5. Gaps vs what the kit expects", ""]
    gaps = []
    for mod in kb["modules"]:
        primary = mod.get("primary_table")
        if primary and primary in tables and not tables[primary].get("exists"):
            gaps.append(f"- `{mod['id']}`: primary table `{primary}` is missing — module not installed here")
        if mod.get("guided_setup", {}).get("available") and gs.get("count", 0) == 0:
            gaps.append(f"- `{mod['id']}`: kit expects guided setup, instance shows none")
    if sam.get("sam_tables_found", 0) == 0:
        gaps.append("- SAM: no `samp_*` / `cmdb_sam_*` tables — the SAM guide is theory until you get a "
                    "SAM-entitled instance (see labs/LAB-03-SAM-BASELINE.md Part 0-B for the fallback)")
    if not gaps:
        gaps.append("- No structural gaps detected. Next: check whether the mandatory fields match what "
                    "the docs describe for your release.")
    lines += gaps + [""]

    # ---- errors
    errs = probe.get("errors") or []
    lines += ["## 6. Probe errors (each one is a release difference)", ""]
    lines += [f"- {e}" for e in errs] if errs else ["- None. Every query in the probe succeeded."]
    lines += ["", "## 7. What to do next", "",
              "0. Empty foundation rows in section 2 mean no module will behave: load them first "
              "(see docs/09-foundation-data.md).",
              "1. Compare section 4 against `docs/04-fields.md` — differences are your release's truth.",
              "2. Open every module in section 5's gap list and confirm whether it is genuinely absent.",
              "3. Run the lab for the module you are learning, then re-run the probe and diff the sheet.", ""]
    return "\n".join(lines)


_KB_CACHE: dict | None = None


def kb_map(kb: dict) -> dict:
    return {m["id"]: m for m in kb["modules"]}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("probe", type=Path, help="probe.json (or a log dump containing the markers)")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--module", help="focus one module id from data/modules.json")
    args = ap.parse_args()

    if not args.probe.exists():
        sys.exit(f"no such file: {args.probe}")
    probe = load_json(args.probe)
    kb = load_json(MODULES) if MODULES.exists() else {"modules": []}
    if args.module and args.module not in kb_map(kb):
        sys.exit(f"unknown module '{args.module}'. Known: {', '.join(kb_map(kb))}")

    text = render(probe, kb, args.module)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
