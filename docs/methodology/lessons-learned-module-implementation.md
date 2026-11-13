# Lessons Learned — Module Implementation (from cross-repo gap analysis)

**Author:** `kilo-sam-deepdive__kilo__cli` · **Date:** 2026-11-13
**Stamp:** 2026-11-13T15:44:29Z · **run-id:** `4178ec70-e3f5-4bc9-a0ab-9c7cdb2acf25`
**Status:** proposed lessons register; no existing files modified

---

## ELI5 — the one-minute version

Imagine learning to cook. The **learning protocol** in this repository teaches you the recipe: orient → configure → build → verify → teach back. That is the *recipe*.

But running a **restaurant** (delivering a module into production) needs more than the recipe:

- check the shopping list before cooking (**prerequisites and dependency map**),
- taste every dish before service (**test cases and acceptance thresholds**),
- know who runs each station (**ownership / RACI**),
- have a plan when the oven breaks (**rollback / exception procedures**),
- do a soft opening before the grand opening (**pilot with go/no-go gates**).

We compared four module "textbooks" — SAM, CMDB, Discovery, HAM — against their training pages and against implementation best practice. The recipes are strong. The restaurant-operations manual is thin everywhere.

---

## Lessons learned (evidence-backed)

| # | Lesson | Evidence |
|---|---|---|
| L1 | **Source hierarchy decides truth:** official docs > exam curriculum > community packs | SAM curriculum carried wrong table names (`cmdb_sam_sw_usage`, `sam_sw_reconciliation_result`), wrong cadence ("nightly"), a fake term ("SUMN") and a wrong plugin tip; community pack taught wrong tables and roles |
| L2 | **Navigation paths decay fast** — always verify breadcrumbs against the live UI and label the release | SAM curriculum paths (`All > Software Asset Management`) did not match workspace/classic reality |
| L3 | **Vendors do not publish OOB internals** — business-rule sys_ids, UI policies, ACLs need audit recipes, not guesses | Fleet had to invent §2.8-style audit recipes because component articles omit them |
| L4 | **Parameters decide whether results can be trusted** — tier them (go-live / tune / never-touch) | SAM Tier 0 properties (auto-create off, published products, exclude flag, recon grouping) were scattered |
| L5 | **Separate documented defaults from practice guidance** — label non-normative advice explicitly | 60–90 day reclaim window is practice, not a vendor default; was initially risked as fact |
| L6 | **Validation is the weakest area across all repos** — zero concrete test cases with expected results | Grepped every final document in three repos: no "expected result" test catalogues exist |
| L7 | **Governance is missing fleet-wide** — no ownership/RACI, source-system contracts, change control or audit evidence chains | Consistent finding across SAM and CMDB/Discovery coverage matrices |
| L8 | **Success Packs have hard gates** — release compatibility, dependency ordering, admin role, storage, backup snapshot, limited uninstallability | Protocol has a prerequisites page but no version matrix, smoke tests or rollback limits |
| L9 | **Coverage is uneven per module** — SAM/CMDB/Discovery have deep research repos; **HAM has none** (training page only) | Repo inventory on GitHub |
| L10 | **Community packs must be rejected by policy, not by luck** — encode the rejection rule in the protocol | sam-buffy pack taught `alm_software`, `sam_license_manager`, wrong navigation parent |

---

## General best-practice gaps — module implementation

Applies to any ServiceNow module (ITSM, CSM, HAM, SAM, GRC, HRSD…):

1. **No success criteria or pilot gates** — nothing defines "trustworthy enough to act on".
2. **No test-case catalogue** — scenario → expected result → evidence.
3. **No acceptance thresholds** for data quality before production use.
4. **No ownership/RACI** per data domain and process.
5. **No source-system contract template** (frequency, fields, error handling, fallback).
6. **No change-control procedure** for configuration that changes results.
7. **No rollback / exception procedures**.
8. **No UAT/sign-off, cutover/hypercare, monitoring model, training/runbooks, performance sizing**.

## General best-practice gaps — Success Packs

The protocol already documents prerequisite basics (`docs/success-packs/success-pack-prerequisites.md`). Still missing:

1. Version-compatibility matrix per pack/release (and where to verify: `glide.product.version`).
2. Dependency ordering (which apps must activate first; failures if reversed).
3. Storage/capacity estimate before install; post-install growth expectations.
4. Backup snapshot requirement and **limited uninstallability** warning.
5. Post-install smoke-test checklist (roles work, sample records render, flows fire).
6. Entitlement/licence verification (is the pack actually entitled on this instance?).
7. Update/upgrade path (pack updates vs family upgrades).
8. Owner assignment for pack content after install.

---

## Recommended protocol additions

| # | Addition | Target file |
|---|---|---|
| 1 | Implementation gate checklist (10 gates) | extend `scripts/rapid-learning-checklist.md`; new methodology section |
| 2 | Prerequisite/dependency map template | `docs/modules/servicenow-module-framework.md` |
| 3 | Test-case catalogue pattern + acceptance thresholds | new `docs/methodology/testing-and-acceptance.md` |
| 4 | Ownership/RACI + source-contract templates | same |
| 5 | Change-control + rollback procedures | same |
| 6 | Cutover/hypercare/monitoring/training plan | same |
| 7 | Success Pack expansion (items above) | `docs/success-packs/success-pack-prerequisites.md` |
| 8 | OOB inventory audit recipe | `docs/out-of-box/out-of-box-workflows-integrations.md` |
| 9 | Breadcrumb verification rule | `docs/navigation/breadcrumbs-cheatsheet.md` |
| 10 | SAM entry in the module catalog | `data/modules.json` |

## Suggested gate checklist (draft)

1. Plugin/subscription + role prerequisites verified.
2. Dependency map recorded (modules, release pin, content services, irreversible upgrades).
3. Data model defined (sources, required fields, frequency, ownership).
4. Core configuration choices decided.
5. Process flows + exception queues designed.
6. Test cases executed; acceptance thresholds met.
7. Rollback rehearsed and documented.
8. Reporting/monitoring consumption confirmed.
9. Pilot completed with go/no-go criteria signed off.
10. Cutover/hypercare/training published.

---

*Sources: `alt_parallelswarm_SAM` fleet finals, `alt_parallelswarm` CMDB/Discovery finals, live SAM/CMDB/Discovery/HAM training pages (fetched 2026-11-13), and this repository's existing docs.*
