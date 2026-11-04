# Instance study sheet

> **Agent:** buffy (mimo-v2.6-flash) · **Updated:** 2026-11-04 · **Rendered from:** probe `1.0.0` generated 2026-11-04 23:40:00

**Instance:** `dev12345` · **Release:** Zurich / zurich · **Probed as:** `admin`

> This file is instance-specific. Do not commit it: it names your instance and user.

## 1. Headline

| Signal | Value | Read it as |
|---|---|---|
| Core tables present | 2/3 | tables the probe asked about that exist here |
| Guided Setup modules | 2 | 0 = this release/app set ships none, or your modules are named differently |
| Flows (active / total) | 21 / 37 | OOB automation already available to copy |
| Scripted REST APIs | 3 | inbound surface you own |
| REST Messages | 5 | outbound integrations configured |
| Indicators / reports / dashboards | 14 / 88 / 4 | whether analytics is real here or theoretical |
| SAM schema | 0 tables | 0 = SAM not installed (Foundation vs Pro matters) |
| Active plugins listed | 42 | first 60 only |

## 2. Guided Setup modules found

| Module title | Target |
|---|---|
| CMDB Guided Setup | cmdb_guided_setup |
| ITSM Guided Setup | itsm_guided_setup |

If an app you care about is missing here, it either has no guided setup on this release or the module is titled differently — do not assume it is missing.

## 3. Per-table facts (mandatory fields are the real answer)

### `incident` — Incident · 412 rows

| Mandatory field | Type | Label |
|---|---|---|
| short_description | string | Short description |
| caller_id | reference | Caller |

**Related lists configured:** `task_sla`, `incident_task`

### `cmdb_ci` — Configuration Item · 128 rows

| Mandatory field | Type | Label |
|---|---|---|
| name | string | Name |

**Related lists configured:** `cmdb_rel_ci`

### `alm_license` — **not present**

The table does not exist on this instance (plugin/app not installed).

## 4. Gaps vs what the kit expects

- SAM: no `samp_*` / `cmdb_sam_*` tables — the SAM guide is theory until you get a SAM-entitled instance (see labs/LAB-03-SAM-BASELINE.md Part 0-B for the fallback)

## 5. Probe errors (each one is a release difference)

- pa_dashboards: Invalid table

## 6. What to do next

1. Compare section 3 against `docs/04-fields.md` — differences are your release's truth.
2. Open every module in section 4's gap list and confirm whether it is genuinely absent.
3. Run the lab for the module you are learning, then re-run the probe and diff the sheet.
