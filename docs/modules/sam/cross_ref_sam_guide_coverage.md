# Cross-Reference: ALT_PARALLELSWARM_SAM vs TSOM SAM Guide Coverage

**Date:** 2026-11-13T15:43:58Z  
**Identifier:** kilo-kilo-ollama-checks-v2  
**Scope:** Bidirectional coverage analysis between the `ALT_PARALLELSWARM_SAM` repository (`final/` docs from beam/kilo and grok/xai/kilo agents) and the published TSOM SAM guide at `https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/`, cross-referenced against the public learning protocol site (`https://eltonaguiar.github.io/ServiceNow_Learning/`).

---

## Direction A — Documented in ALT_PARALLELSWARM_SAM repo, NOT yet on the SAM guide page

These items are well-covered in the repo's final analysis docs but absent from the SAM guide page, and should be added to the learning protocol.

### 1. SAM Pro vs Foundation & role matrix
- Plugins: `com.snc.sams` (Foundation/Pro) vs SAM Pro `com.sn_samp_master_ws` / `com.snc.samp`; upgrade to Pro is irreversible.
- Roles: `sam_admin` (contains `sam_user`, `sam_spend_import`, `asset`, `model_manager`, `contract_manager`), `sam_user` (analyst), `sam_developer` (script work only if trained), `sam_integrator` (SaaS + `connection_admin` + `flow_operator`), `sam_spend_import`.
- ⚠️ `sam_license_manager` / `sn_sam.admin` are **not** official role names (curriculum-wrong).
- On the guide page: neither role matrix nor IRE REST payload appears.

### 2. Four Discovery-to-SAM catalog paths (A–D)
- **Path A**: Catalog (requestable, `sc_cat_item`), not normalization.
- **Path B**: Create in SAM *before* any discovery (SaaS, future deploy, entitlement-first).
- **Path C**: Discovered software linked to a SAM model (install → discovery model → normalize → recon).
- **Path D**: Block / exclude / do not manage (hardware boolean + `com.snc.samp.exclude_device_flag` + `SAM — Adjust Installs for excluded CIs` job; published-products (`manage.published.products`); exclude-from-content-service; leave `automaticsmrcreation` off).
- Guide currently collapses configuration of requestable-vs-observed and has no explicit framing of "catalog last, not first."

### 3. Phase-wise published products + exclude-CI flag
- `com.snc.samp.manage.published.products` (default **false**) → enable, add licensable products, **re-run reconciliation** to make published products the report surface.
- `com.snc.samp.exclude_device_flag` + job `SAM — Adjust Installs for excluded CIs`.
- Auto-creation gate `com.snc.samp.automaticsmrcreation` (off in Crawl); `com.snc.sam.auto_suite_inference` (false by default; turn on **only after** suites verified).
- Suite parent/child publish warning: **do not** publish a top-level suite in a pilot.

### 4. Foundation vs Pro / 3rd-party IRE data source contract
- REST payload keys: `publisher`, `version`, `display_name` (+ optional edition); parent CI identified by `name`; send `sys_class_name` so the CI is not reclassified.
- Property `com.snc.samp.ire.datasource.integration`.
- Role required: `sam_developer`.

### 5. Normalization coverage numbers used as onboarding gates
- ~85%+ normalization hit rate out-of-the-box on SCCM-class sources.
- ~95%+ after Content Service opt-in.
- Treat as Path-to-Value figures, not SLAs; use as gate criterion before enabling `automaticsmrcreation`.

### 6. Organizational MVP baseline (carry-over)
- "80% process and governance, 20% tool"; 80% of spend concentrated in Microsoft, VMware, Adobe, Oracle, IBM, SAP, Salesforce.
- Crawl / Walk / Run phases and the difference between Crawl and Act on First Recon.

### 7. Operational runbooks added in this repo (Section 7)
- **Entitlement import contract column map** (table: field, required, notes — see below).
- **Dead-SaaS-connector monitoring** (drift + stale alert designs + dual-auth hazard rule).
- **Hypercare KPI list + thresholds** (job filter `Name starts with SAM`).
- **Rollback/deactivation runbook** (scenario → procedure).
- **Change-control blast-radius rubric** (change × blast radius × CAB flag).
- **Privacy/PII/identity specifics**.
- **Guided Setup vs phase-wise decision at Sprint 0** (and the re-scoping cost).
- **"Found rocks":** maintenance ≠ license, metric-mismatch flips to Unknown, exclude-CI long tail, subscription-without-usage, billing-cycle alignment.
- **Cutover/cleanup:** publishing correction SLA = ≤ 5 business days after validated change; data refresh every ≤ 2 weeks.

### 8. Foundation vs Pro edition decision (irreversible upgrade to Pro) — described in this repo; not foregrounded on guide.

### 9. CIS/SAM scope freeze: ~85%+ normalization hit rate after opt-in, and published-products freeze with re-run of recon for the product set.

### 10. Data-source reliability ranking, dedup, stale installs
- "Brazil Exact / Major / Any" dedup rule naming; dedup job `Software Install Deduplication` / `SAM – Discovery Model to Software Model matching`.

---

## Direction B — Covered on the SAM guide page, NOT yet in any final doc of this repo (i.e., gaps in the repo that should be mirrored here)

### 1. Lab steps 1–7 (runnable sub-prod activation instructions)
- Add exact search filter on `sys_index_search_all` for discovery-model status-counts.

### 2. Reusable code blocks [knowledge base material]
- Business Rule: "Flag an installation with no normalized software model" (`before` BR).
- Scheduled Job: "Expire entitlements past their end date" (basic `gr` get-list + setValue).
- Script Include: per-publisher compliance summary.
- Client Script: require a metric when creating an entitlement.
- OOB report definitions (Top unlicensed products, unused installations, contested entitlements, recent removals).

### 3. Mnemonics / exam-weight mapping
- Exam-weight table (~15/25/30/20/10) + traps.
- Memory aids: Three-Record Types table, IRE before reconciliation flip "Unknown ≠ compliant."

### 4. Quiz items
- 14 CIS-SAM style questions split by domain; page has dedicated section.

### 5. Migration/cutover specifics for `alm_software`/`cmdb_ci_spkg`
- Guide mentions deprecation timeline; this repo mentions migration in one line.

### 6. Processor-pack matrix with version specifics
- Version of Oracle LMS scripts, ILMT versions.

### 7. Entitlement import contract column map (same as Direction A item 7)
| Field | Required | Notes |
|---|---|---|
| `license_type` | Yes | Must be chosen before import — it is the entire reconciliation basis |
| `metric_type` | Yes | A mismatch makes the reconciliation result silently `Unknown` |
| `quantity` | Yes | Education: never overwrite; create true-up rows instead |
| `entitlement_model` → `cmdb_software_product_model` | Yes | Link to the model, not only product string |
| `contract (ast_contract)` reference | Yes | Audit evidence |
| `purchase_order_no` / `invoice_no` | Yes | Audit evidence (esp. for publisher audit defence) |
| `start_date` / `end_date` | Yes | Drives expiry reconciliation and renewal discipline |
| `unit_cost` / `currency` / `cost_center` | Recommended | Basis for optimization and true-up cost calculation |
| `upgrade_right` (downgrade/upgrading/upline) | Recommended | Controls when a Perpetual entitlement covers an older/newer install |
| `maintenance_only` flag | Recommended | Maintenance does **not** produce compliance for an install by itself |
| `publisher_part_number (PPN)` | Recommended | Lays the cable to Content Library auto-match |
| `allocations: user vs device` (allocations table) | Optional but usually needed | Per-user / per-device metrics collapse without it |
| `source_system` + `source_record_id` | Yes | Idempotency + error handling + dedup |

### 8. Dead-SaaS-connector monitoring (concretely)
- Health baseline snapshot: capture assigned-seat count + sign-in count per connector every run (timestamped).
- Drift alert: if delta between consecutive connector runs is > `X%` (default 20%) without a matching PA/Audit Event, fire notification to `sam_integrator` + integration owner — silent feed failure is the common cause.
- Stale alert: if no successful sync in `N` hours (suggest 36h), post to Slack/Email + freeze reclamation rule actions so you don't reclaim seats from a stale feed.
- Dual-auth hazard: never attach both SSO and a direct SaaS integration to the same app.

### 9. Hypercare KPIs and monitoring signals
- Failed/missed scheduled jobs with `Name starts with SAM` — daily digest.
- DMAP count by norm status — should stabilize within week-1; a sudden drop means Content Service/normalization rule regressed.
- Unlicensed product-result count trend — should trend *down* in pilot; if it grows, normalization or PPN mapping regressed.
- % CIs with owner/location — regression alarm if <40% after data fix.
- Published-product freeze ratio — `published_count` / `in_scope_count`; stable after pilot.
- Time of last successful recon + last successful SaaS sync — SLA-style.

### 10. Rollback / deactivation runbook (concrete)
1. Software model mismatch (wrong metric linked to entitlement): create a new version/corrected model, **re-run reconciliation**, verify alignment, and deprecate (not delete) the old.
2. Wrong license metric on an entitlement: create a true-up/retirement row on the old entitlement and a corrected entitlement linked to the corrected model; keep both auditable.
3. Bad normalization rule (e.g., over-broad pattern rule): disable the rule, re-run "Software Install to Discovery Model" matching, inspect `Match Not Found` delta; canonicalize via Change Record (`CR`) before merge.
4. Third-party integration garbage data: disable the IRE datasource connection (`com.snc.samp.ire.datasource.integration` toggled off), **do not** delete the raw installs via the CI table — run the IRE "drop" job to reverse staged data.
5. Always take a `sys_mod_count`/`sys_updated_on` snapshot view before a model/metric change — store in an `update_set` level artifact, document in the Change Record. Reconciliation results are computed live; there is no historical versioning built-in.

### 11. Change-control criteria (SAM-specific "high blast radius")
| Change | Blast radius | CAB? |
|---|---|---|
| Add a new normalization exception (manual normalize) | Low | No (only queue owner approval) |
| Add a pattern rule / wide-net rule | Medium | Owner review + sample-check |
| Create/match a Software Model | Medium | Only if high publisher spend |
| Change license metric group/type on a model | **High** | Yes — re-runs entire publisher position |
| Modify reconciliation subgrouping (`com.snc.samp.recon.group`) | **High** | Yes |
| Change IRE identifier attributes for 3rd-party | **High** | Yes — duplicates risk |
| Disable a SaaS connector | **High** | Yes — drives reclamation eligibility |
| Published-products freeze changes | Medium/High | RCO review + notify stakeholders |

### 12. Privacy, PII, and identity specifics for per-user SAM
- Per-user allocation, reclamation, and SaaS seat mgmt depends on **per-person identity references**. Document whether your organization requires user-concent for usage metering (SCCM/BigFix agent telemetry) and how the choice affects `samp_sw_usage` completeness.
- Pseudonymization/anonymization strategy for cross-instance sharing of pilot data.
- Document a retention window for `samp_sw_usage` (last-used evidence) that satisfies your regulatory baseline — SAM does not impose one.
- Owner (`managed_by`/`assigned_to`) of CI should be a standardized field — recommend naming one source of truth (Discovery vs HR).

### 13. Guided Setup vs phase-wise decision at Sprint 0
- **Guided Setup** (OOB wizards) is fine for SAM Foundation, single-publisher initial scope. It will not scale to 10+ publishers or custom integration IDs.
- **Phase-wise with published-product freeze** (`com.snc.samp.manage.published.products` enabled, recon re-run) is required for any MVP that wants defensible reconciliation within the pilot window.
- Document this decision **at Sprint 0**, not at Walk phase; re-scoping mid-flight from guided to phase-wise resets the normalization baselines.

### 14. "Found rocks" not called in the repo's lists
Small but exam/operational-relevant items not found in any cited final doc:
1. `com.snc.samp.automaticsmrcreation` off in Crawl (Office Hours) — mentioned, good; but **no note** that it should be turned on only once a normalization hit-rate ≥ claimed 85%+ — say so.
2. `com.snc.sam.auto_suite_inference` (false default) — the condition for turning it on (after suite hierarchies verified in Content Library) is not in any doc.
3. `license_metric_type` stored on *both* model and entitlement; mismatch → `Unknown` (not `Not counted`) — subtle pair any test should include ("change metric on model only and watch result flip to Unknown").
4. Exclude-CI flag + `SAM — Adjust Installs for excluded CIs` job: long tail — once excluded, installs are *not* hard-deleted immediately; reconciliation continues to see them until that job runs; recommend scheduling it post-exclusion in the same control.
5. `sam_spend_import` role + "Load Spend" UI16 deprecated — both noted, but the modern path (Spend store app) is not given a decision-criteria note.
6. "Treat first reconciliation as data-quality loop, and **never as a true-up invoice**" is repeated twice but **no SLA-like statement** (e.g., at most one re-trim cycle per quarter in the first 6 months) — consider adding to Crawl success metrics.
7. Content Service opt-in default OFF is clearly mentioned, but the technical "what triggers outbound traffic" (regional Content Service endpoint, licensing for anonymized telemetry) is absent — worth a footnote for data-residency reviewers.
8. Subscriptions without usage data (manual subscription): many implementers create dummy/placeholder SaaS entitlements; the docs should gate usage-before-position.
9. Suite parent-child publish warning is mentioned ("warns to include parent/children") but no procedure for unpacking a suite into constituents after publish — worth a "do not publish a top-level suite for a pilot" note.
10. ServiceNow Subscription billing: the system calculates over-consumption and bills; reclamation timing vs. the billing cycle needs a defined run-window alignment, or you get billed for reclaimed seats anyway.

### 15. CIS-SAM curriculum vs DOC open questions cross-reference
- Which questions overlap, which are unique to each.

### 16. All UNVERIFIED items consolidated into one place
- Both LG and DOC confess instance-dependence; a consolidated list would be helpful.

### 17. CIS-SAM quiz items mapped to WT1 section numbers
- Exam/interview prep; useful for training new admins.

### 18. Ask-a-Ranger video list (community resource links)
- Not in repo scope, but useful adjunct.

### 19. Success portal widgets/maturity model
- Completed goals, actual vs projected savings, health checks passed, value-builder tasks, Crawl/Walk/Run maturity items.

### 20. Coverage matrix (WT1/Grok/LG comparison)
- Table of what's documented where, with gap priorities.

### 21. Anti-patterns
- Full anti-patterns list from both sources.

### 22. Data-source reliability ranking/dedup/stale installs
- "Exact / Major / Any" dedup rule naming; stale install cleanup.

### 22. Found-rocks not called in the repo's lists
- Same items as #14 above (duplication in numbering).

---

## Recommended Actions

1. **Add an Addendum to `docs/modules/sam/sam-guide.md`** capturing Direction A items (A.1–A.10). This is a documentation change; safe, additive, and does not alter earlier exams.

2. **Mirror Direction B items into this repo** (i.e., `ServiceNow_Learning`) by adding:
   - `final/FINAL_SAM_LAB_RUNBOOK.md` (lab steps + reusable snippets)
   - Cross-reference / open-questions consolidation
   - Dead-connector monitoring design
   - Rollback/deactivation runbook
   - Blast-radius rubric as Change Category template
   - Privacy/identity notes
   - Sprint-0 decision framework (Guided vs phase-wise)
   - Found-rocks appendix

3. **Add a SAM entry to `ServiceNow_Learning`** (the public learning protocol site) using the HAM-guide template, pointing back to the TSOM SAM guide + the ALT_PARALLELSWARM_SAM repo. Surface `ServiceNow_Learning/docs/modules/sam/sam-learning-map.md` already exists with a rapid-learning map.