# ServiceNow Learning Methodology — Design

**Target repo:** `github.com/eltonaguiar/ServiceNow_Learning`
**Branch:** `zoo-2026-11-04-servicenow-learning-methodology`
**Author:** Zoo · 2026-11-04

---

## 1. Problem

Learning a ServiceNow module "at a rapid pace" needs five things the docs don't put in one place:

1. What it *is*, in plain language (ELI5)
2. Exactly **where to click** (breadcrumbs, verbatim nav paths)
3. Which fields/related lists are **critical** vs **mandatory-and-boring** vs **optional-but-useful**
4. What **breaks** (common mistakes, silent failures)
5. A lab that **does something real** with the data — not just "call the REST Message and look at the response"

The repo already has the right skeleton (`methodology/`, `generators/templates/`, `infographics/`, `labs/rest_message_integration/`, `labs/remote_table/`) but every directory is empty and the README is one line. This design fills that skeleton.

## 2. Core architecture — 4 layers, independently testable

| Layer | Path | Authored by | Purpose |
|---|---|---|---|
| **Spine** | `content/<slug>.yaml` | Human | The deterministic facts: breadcrumbs, field tables, checklist, lab steps |
| **Contract** | `schemas/module.schema.json` | Human | JSON Schema; every content file must validate |
| **Prose cache** | `prose/<slug>.cache.json` | AI, then committed | ELI5 explainer, analogies, "why this matters", mistake narratives |
| **Renderer** | `generators/pack.py` | Human | Validate → merge → render Markdown + SVG → rebuild index |

**Why this split:** the risky content (a wrong breadcrumb sends a beginner to a dead end) is never AI-generated. The low-risk content (an analogy for "what is a REST Message") is AI-generated once and frozen. Rebuilds are deterministic and diffable because the prose is cached on disk, not re-fetched.

**Prose cache contract:** a cache entry is `{slug, prose_key, model, generated_at, text}`. A content file references a cache entry via `eli5: {prose_key: eli5}` — i.e. `prose_key` is exactly the cache entry's `prose_key` field, so the lookup is a plain string match with no derivation logic. `--refresh-prose` is opt-in only. If the entry exists, the generator never calls an API. If it's missing and no key is available, the section renders as a visible `> ⚠️ PROSE MISSING` block and the build still exits 0 — so the repo is always buildable by a contributor with no API keys.

## 3. Mandatory schema sections (all 9 required for every module)

```yaml
slug: rest-message-integration
title: REST Message Integration
description: "..."               # 2-3 sentences, what + why
prerequisites: [...]             # each: {label, why_needed, how_to_get}
validation_checklist: [...]      # each: {id, path, expected, tier, how_to_prove}
infographic: {layout: ..., nodes: [...]}   # declarative spec, not raw SVG
eli5: {prose_key: eli5}          # AI-filled; prose_key matches the cache entry
common_mistakes: [...]           # each: {symptom, cause, fix, how_to_spot}
practical_example: {...}         # the "do something with it" scenario
lab_tasks: [...]                 # each: {rung, goal, steps, success_check}
```

`additionalProperties: false` in the schema so typos in a content file fail the build instead of silently vanishing.

### 3.1 The field-classification model (the heart of the "what's critical" ask)

Every field/related-list entry carries `tier`, one of exactly four values:

- **`critical`** — misconfigure it and the integration silently does nothing (e.g. REST Message *Endpoint* omitted → request never leaves; Remote Table *Parent Table* wrong → no rows surface; ACL missing → 0 rows with no error)
- **`mandatory`** — the form refuses to save without it
- **`optional_useful`** — not required, but the top candidates for actually being useful (e.g. `Retry Policy`, `Timeout`, related list `HTTP Methods` pre/post scripts)
- **`optional_skip`** — exists, ignore for now

This is the field the user explicitly asked for ("which are CRITICAL to setup"). It drives both the Markdown table and the infographic colour coding.

### 3.2 Breadcrumb format

```
path: System Web Services → Outbound → REST Message
```
Rendered verbatim, in a code font, with `→` separators. A test asserts every `path` matches `^(Application Navigator|[A-Z][\w &/\-]+)( → [\w &/\-()]+)+$` and that no segment is a placeholder like `...`. This is the main defence against hallucinated navigation.

### 3.3 Validation checklist entries

```yaml
- id: RT-04
  path: System Definition → Tables → (your table)
  expected: "Rows returned by the remote API appear as records in list view"
  tier: critical
  how_to_prove: "Open list view; count rows; compare against the raw API response count"
```
`how_to_prove` is mandatory — a checklist item you can't observe is not a checklist item.

## 4. Lab depth model — 5 rungs (this is what makes the labs real)

Both labs implement the same ladder so learners see progression:

| Rung | REST Message lab | Remote Table lab |
|---|---|---|
| **1 Skeleton** | Create REST Message + endpoint, no method | Create data source by URL, no parent table |
| **2 Wire** | Add GET method, headers, run "Test" | Point at a real JSON API, confirm preview |
| **3 Transform** | Parse response into a record via script | Map remote columns → real fields |
| **4 Do something** | Upsert results into `u_incident_feed`; attach the raw payload | Surface rows in a list + report grouped by remote field |
| **5 Prove** | Validation checklist RT-01..RT-08 all green; run twice to prove idempotence | Prove ACL: a non-admin role can read; prove refresh interval |

**"Do something with it"** is deliberately rung 4, not rung 2. Calling an endpoint and staring at JSON teaches nothing; writing it to a table, then reporting on it, is the transferable skill.

## 5. Infographic generation

Declarative, not free-drawn. Node `kind` draws from the same vocabulary as §3.1, plus `step`:

```yaml
infographic:
  layout: vertical-flow        # one of: vertical-flow | hub-spoke | tier-matrix
  nodes:
    - {id: nav,  label: "Navigator",        kind: step}
    - {id: ep,   label: "Endpoint",         kind: critical}
    - {id: hdr,  label: "HTTP Headers",     kind: optional_useful}
```

Allowed `kind` values: `step`, `critical`, `mandatory`, `optional_useful`, `optional_skip`.

`generators/infographic.py` turns that into hand-tuned SVG (palette keyed to `kind`). Deterministic output → committed SVG, diffable, no external service, no binary files.

## 6. Data flow

```
content/*.yaml ──validate──▶ merge prose cache ──render──▶ labs/<slug>/README.md
                                              └─────────▶ infographics/<slug>.svg
                                              └─────────▶ docs/index.md  (module catalog)
```

One command: `python -m generators.pack --all` (or `--slug rest-message-integration`).

## 7. Error handling

| Failure | Behaviour |
|---|---|
| Content file fails schema | Print every violation as `path: message`, exit 1, write nothing |
| Breadcrumb contains `...` or a placeholder | Fail with the offending line number |
| Infographic node references an unknown `kind` | Fail at validation, before rendering |
| Prose cache entry missing, no API key | Render `> ⚠️ PROSE MISSING` block, exit 0, warn |
| AI call fails mid-generation | Keep the existing cache file untouched; never overwrite with empty text |

## 8. Testing

| Test | Asserts |
|---|---|
| `tests/test_schema.py` | Every `content/*.yaml` validates against the schema |
| `tests/test_breadcrumbs.py` | No placeholder segments; every path matches the nav regex |
| `tests/test_labs.py` | Both labs have all 5 rungs and ≥8 checklist items, each with `how_to_prove` |
| `tests/test_render.py` | Golden-file snapshot of both generated READMEs and both SVGs |
| `tests/test_cache.py` | Build with no API key still exits 0; build twice produces byte-identical output |

CI: `.github/workflows/test.yml` → `pytest -q` on push and PR.

## 9. Extension path (the "rapid pace" goal)

Adding module #3 is: copy a content YAML, fill 9 sections, run `pack --slug`. Target 30 minutes per new module. The methodology doc (`methodology/HOW_TO_ADD_A_MODULE.md`) is generated from the schema itself so it cannot drift.

## 10. Non-goals for v1

- **No live ServiceNow instance required.** Every lab is written to be runnable on a Personal Developer Instance, but nothing in CI touches the network.
- **No 10-module catalog.** One deep vertical slice (2 labs) proves the pattern first.
- **No programmatic Figma authoring.** No Figma API token or MCP server exists in this environment, so no board can be created or linked from here. See the blocker note below for the substitute.

---

## ⚠️ Blocker to confirm — Figma

You asked for a Figma board plus a share link. **I have no Figma access in this environment** — no API token, no MCP server for it. I can't create a board or produce a link, and I won't fabricate one.

Available substitutes, in order of usefulness:

1. **Committed SVG** (what §5 already specifies) — diffable, reviewable in the GitHub file viewer, generated from the same YAML as the labs. Strictly better for a git-hosted learning repo.
2. **Figma-importable spec** — an extra `infographics/<slug>.figma.json` containing frames/text/colour per `kind`, formatted so you can paste it into Figma via a plugin such as "html.to.design". You do the import in ~2 minutes and get an editable board on your side.
3. **Mermaid diagrams** in the Markdown — renders natively on GitHub, zero tooling.

**Recommendation:** 1 as the deliverable, plus 2 as a by-product so you still get an editable Figma board on your side.
