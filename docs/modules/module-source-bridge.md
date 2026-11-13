# Module Source Bridge — connecting research repos, training pages and this protocol

**Author:** `kilo-sam-deepdive__kilo__cli` · **Date:** 2026-11-13
**Stamp:** 2026-11-13T15:44:29Z · **run-id:** `4178ec70-e3f5-4bc9-a0ab-9c7cdb2acf25`
**Status:** proposed navigation aid

---

## ELI5

Every ServiceNow module has **three textbooks**:

1. a **research repo** on GitHub (deep technical notes written by agents),
2. a **training page** (the study guide you read first),
3. this **learning protocol** (how to learn and how to deliver).

They do not agree perfectly. This page is the *translator*: it tells you which book to open for which question, and where each one is missing pages.

---

## Source map

| Module | Research repo | Training page | Protocol coverage |
|---|---|---|---|
| **SAM** | `eltonaguiar/alt_parallelswarm_SAM` (fleet finals + `research/servicenow-sam/`) | `.../modules/sam/sam-guide/` | Experimental guidance + mnemonics added; SAM catalog entry proposed |
| **CMDB** | `eltonaguiar/alt_parallelswarm` (`final/DISCOVERY_INSERT_VS_UPDATE_GUIDE.md`, merged references) | `.../modules/cmdb/cmdb-guide/` | Not yet bridged (protocol gap) |
| **Discovery** | same repo (`research/servicenow-discovery/`) | `.../modules/discovery/discovery-guide/` | Not yet bridged (protocol gap) |
| **HAM** | **none** (no dedicated research repo) | `.../modules/ham/ham-guide/` | HAM entry exists in `data/modules.json`; research counterpart missing |

---

## Which book answers which question?

| Question | Best source |
|---|---|
| "What does this module do, in one sentence?" | Training page |
| "What are the exact tables, fields and property names?" | Research repo finals |
| "How do I configure it step by step?" | Training page labs + research procedures |
| "Why is my result wrong?" | Research troubleshooting + anti-patterns |
| "How do I deliver this in production?" | This protocol (gates, RACI, change control) |
| "How do I pass the exam?" | Training page quiz + mnemonics (💡 blocks) |
| "Is this claim official or community lore?" | Cross-check both; official docs win |

---

## Known gaps to bridge (as of 2026-11-13)

### SAM

- Page has **errors** (`cmdb_sam_sw_usage`, `sam_sw_reconciliation_result`, nightly cadence, SUMN, plugin tip) → corrections documented in `updates/2026-11-13-sam-guide-gaps-and-additions.md`.
- Page lacks OOB inventory, parameter tiers, result-field schema, hygiene controls → additions listed in the same file; full detail in `alt_parallelswarm_SAM/final/FINAL_kilo-sam-deepdive.md`.
- Research repo lacks success criteria, test cases, ownership/RACI, source contracts, change control, rollback, UAT/cutover → protocol gap register.

### CMDB / Discovery

- Training pages are deep (IRE four-rule deep dive, e-bonding, OpenTelemetry SGC, webhooks, pattern customization).
- Research repo is deep on IRE rules, insert-vs-update decisions, duplicate root causes, property catalogs, health/hygiene.
- **Both lack**: concrete test cases, implementation gates, ownership/RACI, change control, cutover/hypercare, Success Pack practice.
- Cross-reference: `alt_parallelswarm/final/DISCOVERY_INSERT_VS_UPDATE_GUIDE.md` is the shared decision authority.

### HAM

- Training page covers lifecycle, asset states, model lifecycle, CMDB integration, file-based discovery console, file signature normalization.
- **No research counterpart** — a fleet repo should be commissioned, or the page should be treated as sole source (higher risk of uncorrected errors).

---

## Bridging rules (use every time)

1. **Official docs > training page > community packs.** If two disagree, quote both and label the conflict.
2. **Never copy breadcrumbs without verifying against the UI.** Paths decay between releases.
3. **Mark UNVERIFIED instead of guessing.** A guess repeated becomes "fact" quickly.
4. **Separate documented defaults from practice guidance.** Label the latter.
5. **Every research claim should cite a source id; every training claim should link back to the repo.**
6. **When you fix a page error, log it in `updates/` and notify the research repo owner.**

---

## Visual summaries (assets)

| Asset | Content |
|---|---|
| `assets/servicenow-sam-pipeline-infographic.svg` | SAM pipeline: sources → install → discovery model → software model ← entitlement → reconcile → remediate/reclaim/renew, with IRE gates and DIN MERR² / UNC / APEX callouts |
| `assets/servicenow-module-implementation-lifecycle.svg` | Ten-gate delivery lifecycle (prerequisites → dependency map → data model → configuration → process design → test cases → rollback → consumption → pilot → cutover/hypercare) |

---

*Bridge document — navigation aid only. Verify every technical claim against official documentation for your release.*
