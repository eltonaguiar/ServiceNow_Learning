# SAM readiness scorecard

> **Agent:** buffy (mimo-v2.6-flash) · **Updated:** 2026-11-04 · **Instance:** `dev12345` · **Release:** Zurich

## Score: 50/100 — NOT READY — a hard prerequisite is missing

| # | Check | State | What the probe saw | Next action |
|---|---|---|---|---|
| 1 | SAM schema installed | ❌ FAIL | no SAM tables found | install/entitle SAM before anything else; use Lab 03 Part 0-B meanwhile |
| 2 | Asset tables present | ❌ FAIL | alm_asset missing | install Asset Management |
| 3 | CMDB populated | ✅ PASS | cmdb_ci: 128 rows | check identification rules before loading more |
| 4 | Discovery / connector plugin visible | ⚠️ WARN | not seen in the first 60 active plugins | confirm in All Available Applications; without a feed, compliance is hand-entered |
| 5 | Contract table present | ❌ FAIL | ast_contract missing | asset/contract plugin needed for entitlement provenance |
| 6 | Licence record table present | ⚠️ WARN | alm_license not found on this instance | verify the licence table name for your edition with the probe |
| 7 | SAM/Asset Guided Setup found | ⚠️ WARN | no matching guided setup module | search the filter navigator; on this release it may be titled differently |
| 8 | Active automation | ✅ PASS | 21 active flows | reuse OOB lifecycle/reconciliation flows before building |
| 9 | Analytics in use | ✅ PASS | indicators=14, reports=88 | publish licence position with coverage %, not just a number |
| 10 | Probe ran clean | ⚠️ WARN | 1 query errors | each error is a release difference worth reading |

## How to read this

- A **hard failure** in schema, assets or CMDB caps the grade regardless of the score: SAM on top of missing discovery produces confident nonsense.
- **WARN** usually means "release difference or entitlement gap", not "broken".
- Re-run after every prerequisite you fix; the score is a work queue, not a verdict.

## The three that matter most

1. **Schema + entitlement** — without it, everything else is theory.
2. **CMDB populated with identification rules** — duplicates double your exposure.
3. **A discovery feed** — hand-typed installs are an asset register, not SAM.

Guide: `docs/08-SAM-SETUP.md` · Lab: `labs/LAB-03-SAM-BASELINE.md`
