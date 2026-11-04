#!/usr/bin/env python3
"""sam_readiness.py — score how ready an instance actually is for SAM, from probe output.

    python3 scripts/sam_readiness.py probe.json
    python3 scripts/sam_readiness.py probe.json --out docs/generated/sam-readiness.md

Ten checks, each PASS / WARN / FAIL, each with the next action. The score is deliberately
conservative: a missing discovery feed or missing SAM schema caps the grade, because those
two make every downstream number fiction.

Input: the JSON from scripts/sn_probe.js. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if "=== SNPROBE BEGIN ===" in text:
        text = text.split("=== SNPROBE BEGIN ===")[1].split("=== SNPROBE END ===")[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        sys.exit(f"{path}: not probe JSON ({exc})")


def plugins_text(probe: dict) -> str:
    items = probe.get("plugins", {}).get("items", [])
    return " ".join(f"{i.get('id', '')} {i.get('name', '')}".lower() for i in items)


def check(probe: dict) -> list[dict]:
    tables = probe.get("tables", {})
    sam = probe.get("sam", {})
    gs_titles = " ".join(m.get("title", "").lower() for m in probe.get("guided_setup", {}).get("modules", []))
    plugs = plugins_text(probe)
    flows = probe.get("automation", {})
    analytics = probe.get("analytics", {})
    errors = probe.get("errors") or []

    def t(name: str) -> dict:
        return tables.get(name, {})

    rows: list[dict] = []

    def add(key: str, label: str, state: str, detail: str, action: str) -> None:
        rows.append({"key": key, "label": label, "state": state, "detail": detail, "action": action})

    # 1. SAM schema (hard gate)
    n = sam.get("sam_tables_found", 0)
    if n:
        add("schema", "SAM schema installed", "PASS", f"{n} samp_*/cmdb_sam_* tables", "confirm Foundation vs Professional")
    else:
        add("schema", "SAM schema installed", "FAIL", "no SAM tables found",
            "install/entitle SAM before anything else; use Lab 03 Part 0-B meanwhile")

    # 2. Asset tables
    if t("alm_asset").get("exists"):
        add("assets", "Asset tables present", "PASS", f"alm_asset, {t('alm_asset').get('row_count', '?')} rows",
            "verify assets link to CIs")
    else:
        add("assets", "Asset tables present", "FAIL", "alm_asset missing", "install Asset Management")

    # 3. CMDB CIs
    ci = t("cmdb_ci")
    if ci.get("exists") and (ci.get("row_count") or 0) > 0:
        add("cmdb", "CMDB populated", "PASS" if (ci.get("row_count") or 0) > 100 else "WARN",
            f"cmdb_ci: {ci.get('row_count')} rows", "check identification rules before loading more")
    else:
        add("cmdb", "CMDB populated", "FAIL", "cmdb_ci empty or missing",
            "configure CI identifiers, then discovery — SAM cannot reconcile without CIs")

    # 4. Discovery / connector
    if any(k in plugs for k in ("discovery", "service graph", "client collector", "acc")):
        add("discovery", "Discovery / connector plugin visible", "PASS", "matched in active plugin list",
            "scope one connector to a pilot and confirm installs arrive")
    else:
        add("discovery", "Discovery / connector plugin visible", "WARN",
            "not seen in the first 60 active plugins",
            "confirm in All Available Applications; without a feed, compliance is hand-entered")

    # 5. Contracts
    if t("ast_contract").get("exists"):
        add("contracts", "Contract table present", "PASS", "ast_contract available",
            "load POs/contracts so entitlements trace to evidence")
    else:
        add("contracts", "Contract table present", "FAIL", "ast_contract missing",
            "asset/contract plugin needed for entitlement provenance")

    # 6. Licence record table
    if t("alm_license").get("exists"):
        add("licences", "Licence record table present", "PASS", "alm_license available", "load entitlements with metrics")
    else:
        add("licences", "Licence record table present", "WARN", "alm_license not found on this instance",
            "verify the licence table name for your edition with the probe")

    # 7. Guided setup for asset/SAM
    if any(k in gs_titles for k in ("asset", "software", "sam")):
        add("guided", "SAM/Asset Guided Setup found", "PASS", "guided setup module present",
            "read every step before executing any")
    else:
        add("guided", "SAM/Asset Guided Setup found", "WARN", "no matching guided setup module",
            "search the filter navigator; on this release it may be titled differently")

    # 8. Automation
    active = flows.get("flows_active", 0) or 0
    add("flows", "Active automation", "PASS" if active > 0 else "WARN", f"{active} active flows",
        "reuse OOB lifecycle/reconciliation flows before building")

    # 9. Analytics
    ind = analytics.get("indicators")
    add("analytics", "Analytics in use", "PASS" if (ind or 0) > 0 else "WARN",
        f"indicators={ind}, reports={analytics.get('reports')}",
        "publish licence position with coverage %, not just a number")

    # 10. Probe cleanliness
    add("errors", "Probe ran clean", "PASS" if not errors else "WARN",
        "no query errors" if not errors else f"{len(errors)} query errors",
        "each error is a release difference worth reading" if errors else "nothing to do")

    return rows


def score(rows: list[dict]) -> tuple[int, str]:
    pts = {"PASS": 1.0, "WARN": 0.5, "FAIL": 0.0}
    raw = sum(pts[r["state"]] for r in rows)
    pct = round(100 * raw / len(rows))
    hard_fail = any(r["state"] == "FAIL" and r["key"] in ("schema", "cmdb", "assets") for r in rows)
    if hard_fail:
        grade = "NOT READY — a hard prerequisite is missing"
    elif pct >= 85:
        grade = "READY — proceed to reconciliation and cadence"
    elif pct >= 60:
        grade = "PARTIAL — prerequisites first, then compliance numbers"
    else:
        grade = "EARLY — do not publish a compliance figure yet"
    return pct, grade


def render(probe: dict, rows: list[dict], pct: int, grade: str) -> str:
    icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}
    out = [
        "# SAM readiness scorecard",
        "",
        f"> **Agent:** buffy (mimo-v2.6-flash) · **Updated:** 2026-11-04 · **Instance:** "
        f"`{probe.get('instance', '?')}` · **Release:** {probe.get('release_name', '?')}",
        "",
        f"## Score: {pct}/100 — {grade}",
        "",
        "| # | Check | State | What the probe saw | Next action |",
        "|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | {r['label']} | {icon[r['state']]} {r['state']} | {r['detail']} | {r['action']} |")
    out += [
        "",
        "## How to read this",
        "",
        "- A **hard failure** in schema, assets or CMDB caps the grade regardless of the score: "
        "SAM on top of missing discovery produces confident nonsense.",
        "- **WARN** usually means \"release difference or entitlement gap\", not \"broken\".",
        "- Re-run after every prerequisite you fix; the score is a work queue, not a verdict.",
        "",
        "## The three that matter most",
        "",
        "1. **Schema + entitlement** — without it, everything else is theory.",
        "2. **CMDB populated with identification rules** — duplicates double your exposure.",
        "3. **A discovery feed** — hand-typed installs are an asset register, not SAM.",
        "",
        "Guide: `docs/08-SAM-SETUP.md` · Lab: `labs/LAB-03-SAM-BASELINE.md`",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("probe", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    probe = load(args.probe)
    rows = check(probe)
    pct, grade = score(rows)
    text = render(probe, rows, pct, grade)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out} — {pct}/100 ({grade})")
    else:
        print(text)


if __name__ == "__main__":
    main()
