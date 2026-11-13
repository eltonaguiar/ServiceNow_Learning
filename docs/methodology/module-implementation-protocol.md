# Module Implementation Protocol — gaps and proposed additions

**Author:** `kilo-sam-deepdive__kilo__cli` · **Date:** 2026-11-13
**Stamp:** 2026-11-13T15:44:29Z · **run-id:** `4178ec70-e3f5-4bc9-a0ab-9c7cdb2acf25`
**Status:** proposed gap register — no changes applied beyond this file

## Purpose

The rapid-learning methodology covers *learning* a module (orient → configure → build → verify → teach back). This note documents what the protocol lacks for *implementing/delivering* a module in production, based on a cross-reference of the `alt_parallelswarm_SAM` fleet research against standard ServiceNow implementation practice.

## What the protocol covers well

- 5-step learning loop (`docs/methodology/rapid-learning-methodology.md`)
- Module anatomy and the 10-question module checklist (`docs/modules/servicenow-module-framework.md`)
- OOB components overview (`docs/out-of-box/out-of-box-workflows-integrations.md`)
- Mandatory vs critical fields pattern (`docs/fields/mandatory-vs-critical-fields.md`)
- Breadcrumb cheatsheet (`docs/navigation/breadcrumbs-cheatsheet.md`)
- Common mistakes, labs, and checklists

## Gaps (with proposed placement)

| # | Gap | Proposed target | Why |
|---|---|---|---|
| B1 | No implementation gate checklist (pilot/go-no-go, acceptance thresholds, evidence) | New section in this file; extend `scripts/rapid-learning-checklist.md` | Learning stops at "it works"; delivery needs trust criteria |
| B2 | No prerequisite/dependency map template (plugin, roles, dependent modules, release pin, content services, irreversible upgrades) | This file | Every module has hard prerequisites; SAM's are version-gated |
| B3 | No RACI / ownership matrix template | This file | Data domains need named owners |
| B4 | No source-system contract template (frequency, required fields, error handling, fallback) | This file | Integrations fail silently without contracts |
| B5 | No test-case catalogue pattern (scenario → expected result → evidence) | This file + `scripts/concept-summary-template.md` | Zero concrete test cases exist in the SAM corpus |
| B6 | No change-control procedure for configuration that alters results | This file | Model/metric/rule changes silently change compliance numbers |
| B7 | No validation / rollback / exception procedures | This file | Misclassification and bad imports need documented recovery |
| B8 | No cutover / hypercare / monitoring / runbook / training plan | This file | Day-2 operations are undocumented |
| B9 | OOB inventory audit recipe (how to enumerate shipped jobs/BRs/flows/ACLs when vendors don't publish them) | `docs/out-of-box/out-of-box-workflows-integrations.md` | Reusable for any module; SAM recipe exists |
| B10 | Parameter-tiering pattern (configure at go-live / tune later / never touch) | `docs/fields/mandatory-vs-critical-fields.md` | Generalises the SAM Tier 0/1/2 property finding |
| B11 | Breadcrumb verification rule (confirm against actual UI; label release; prefer workspace paths) | `docs/navigation/breadcrumbs-cheatsheet.md` | The SAM curriculum breadcrumbs were wrong; encode the lesson |
| B12 | **No SAM entry in `data/modules.json`** | `data/modules.json` | Catalog currently has tsom/csm/fsm/sales-crm/ham/itsm only |

## Proposed implementation gate checklist (B1/B2/B8 draft)

1. Plugin/subscription and role prerequisites verified (exact plugin ids, role list).
2. Dependency map recorded: dependent modules/plugins, release pin, content-service opt-ins, irreversible upgrade notes.
3. Data model defined: authoritative sources per data type, required fields, update frequency, error handling, ownership.
4. Core configuration choices decided: primary table(s), key record types, insert/update rules.
5. Process flows and exception handling designed (owner + SLA per exception queue).
6. Test cases written with expected results and executed; acceptance thresholds met.
7. Validation/rollback procedures documented and rehearsed.
8. Reporting/dashboard consumption path confirmed; alerts and monitoring assigned.
9. Pilot scope, success metrics and go/no-go criteria defined and signed off.
10. Cutover/hypercare plan and training/runbooks published.

## SAM catalog entry proposal (B12)

`data/modules.json` should gain a SAM object following the existing schema:

```json
{
  "id": "sam",
  "name": "ServiceNow Software Asset Management (SAM)",
  "app": "ITAM — SAM Pro",
  "confidence": "verified",
  "why": "SAM reconciles purchased entitlements against discovered/installed and consumed software to produce compliance positions, license positions, reclamation candidates and true-up costs.",
  "primary_table": "alm_license",
  "tables": ["cmdb_sam_sw_install", "cmdb_sam_sw_discovery_model", "cmdb_software_product_model", "alm_license", "samp_reconciliation_result", "samp_product_result", "samp_license_metric_result", "samp_sw_usage"],
  "roles": ["sam_admin", "sam_user", "sam_developer", "sam_integrator", "model_manager", "asset", "contract_manager"],
  "breadcrumbs": [
    "Workspaces > Software Asset Workspace",
    "All > Software asset > Administration > Properties",
    "All > Software Asset > Licensing > Software Models",
    "All > Software Asset > Discovery > Discovery models"
  ],
  "guided_setup": {"available": false},
  "oob": {
    "jobs": ["SAM - Normalize discovery models using content library rules", "SAM - Trigger Full Scan", "Weekly reconciliation"],
    "business_rules": ["Install -> discovery model match/create (unnamed)"],
    "script_includes": ["Reconciliation logic in com.sn_itam_samp (Yokohama+)"],
    "flows": ["Reclamation flow", "Software request workflow"],
    "metrics": ["% normalized installs", "compliance by publisher", "reclaimed value"],
    "dashboards": ["Software asset overview", "License Position report", "Normalization and content"]
  },
  "fields": {
    "critical": [
      {"field": "cmdb_sam_sw_discovery_model.Normalization status", "why": "Drives whether reconciliation counts the install"},
      {"field": "cmdb_sam_sw_discovery_model.Software model", "why": "Link from normalized discovery model to purchased model"},
      {"field": "alm_license.license_metric", "why": "Counting basis; mismatch silently breaks reconciliation"},
      {"field": "alm_license.Publisher Part Number", "why": "PPN resolution into software models"}
    ]
  }
}
```

> Field names above are drawn from official Brazil/Australia documentation and should be re-verified per release before publication.

## Source & method

Cross-reference performed 2026-11-13: `alt_parallelswarm_SAM` fleet finals (`final/FINAL_kilo-sam-deepdive.md`, `final/FINAL_grok-4.6__xai__kilo.md`, `final/FINAL_SAM_MODULE_REFERENCE.md`), official product docs corpus (66 mirrored articles), live CIS-SAM curriculum page, and this repository's existing docs. See `research/servicenow-sam/COVERAGE_GAP_ANALYSIS.md` and `BIDIRECTIONAL_GAP_DIFF.md` in the fleet repo for the full matrices.
