# SAM Learning Map — Software Asset Management (Rapid Protocol)

**Module:** SAM | **App:** IT Asset Management (ITAM) | **Confidence:** verify

This is the rapid-learning map for **Software Asset Management (SAM)**, the software counterpart to [HAM](../ham/ham-guide.md). Detailed exam-depth guide lives in the TSOM/SAM guide: <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/>.

---

## Purpose (one sentence)

SAM answers: *Are we legally and financially in control of the software we actually run?* — by reconciling what was purchased (entitlements) against what is installed (discovery) and consumed (usage) per **software model** and **license metric**.

---

## RAPID map (Orient → Model → Practice → Prove)
### Orient (10 min)

- SAM = software half of ITAM; shares `alm_*` with HAM; adds discovery model → software model → install → usage → entitlement → reconciliation result.
- Plugin: `com.snc.sams` (Foundation/Pro) vs SAM Pro `com.sn_samp_master_ws`; upgrade to Pro is irreversible.
- Core problem: reconciliation of owned rights vs installed/consumed software — not CI existence.

### Model (25 min) — the six records

| Record | Table | Meaning | Creator |
|---|---|---|---|
| Software Model | `cmdb_software_product_model` | Canonical product | Content Library (auto) or admin |
| Discovery Model | `cmdb_sam_sw_discovery_model` | Raw field fingerprint | Discovery/SCCM/Intune import |
| Installation | `cmdb_sam_sw_install` | One concrete install on one device | Discovery |
| Usage | `cmdb_sam_sw_usage` | Launch count / last-used (evidence) | Usage connectors |
| Entitlement | `alm_license` | Right to use N units under metric | Admin |
| Reconciliation Result | computed | Compliance verdict | Reconciliation job |

Rule of thumb: *Software model = what it is · Entitlement = what you may use · Installation = what exists · Usage = what is used · Reconciliation = the difference.*

### Key tables
- `cmdb_sam_sw_install`, `cmdb_sam_sw_discovery_model`, `cmdb_software_product_model`, `alm_license`, `cmdb_sam_sw_usage`.
- `ast_contract`, `alm_asset` (shared with HAM).

### Roles
- `sam_admin` (contains sam_user, sam_spend, asset, model_manager, contract_manager).
- `sam_user` (analyst), `sam_developer` (scripts, trained admins), `sam_integrator` (SaaS + connection_admin + flow_operator), `sam_spend_import`. Note: `sam_license_manager`/`sn_sam.admin` are **not** official role names.

### Practice (40 min) — repeatable lab

1. Choose and verify a software model (check metric type).
2. Create an entitlement far below demand (never overwrite; create true-up on fix).
3. Confirm installs exist.
4. Run reconciliation (on demand, not only weekly).
5. Prove the fix — compliance position flips from Under-licensed → Compliant.
6. Prove normalization matters — mismatched metric → **Unknown ≠ Compliant**.
7. Teach back — write it down.

### Prove (10 min) — validation checklist

- 1 per-device entitlement + 2 active installs → shortfall **1**.
- Named-user entitlement with inactive allocations → allocations (> 0) and stale exclusion.
- Maintenance-only entitlement → **does not** count until linked to a perpetual.
- Two sources for one IBM install → one Active after dedup.
- Retired CI → installs removed; excluded CI → omitted after Adjust job.
- Catalog publish creates a requestable item **without** changing reconciliation.
- Metric mismatched on the model → result is **Unknown**, never "compliant."

### Compliance positions

Compliant / Over-licensed / Under-licensed / Unlicensed / Not counted / Unknown — "Unknown ≠ Compliant" is the #1 reason audit penalties appear unexpectedly.

### Publisher traps (high-level)

Microsoft (SQL per-core with min 4, suite overlap), Oracle (core-factor, server-not-VM, LMS scripts), IBM (PVU + ILMT), SAP (named-user + indirect/digital access), Adobe (VIP/ETLA, shared device), VMware (per-processor aggregation), ServiceNow (subscription by fulfilled user, billed not audited).

### Learning guard-rails & pitfalls

- CMDB "CI inserted correctly" is **not** the SAM success criterion; the closed loop is.
- Do not treat the first reconciliation as a true-up invoice — it is a data-quality loop.
- Never redefine a license metric on an existing model in place; create a new model (or a corrected one) and re-run reconciliation; treat it as high blast radius change.
- Keep `automaticsmrcreation` off in Crawl; leave Content Service **opt-in**; do not enable `auto_suite_inference` until suites verified.
- Do not attach SSO + direct SaaS integration to the same app.

### Reconciliation / properties worth memorizing

- Roles: `sam_admin`, `sam_user`, `sam_developer`, `sam_integrator`, `sam_spend_import`.
- Jobs filter: `Name starts with SAM`.
- Version pins: record a Brazil/Yokohama/Zurich owner pin; role names differ by release.
- See: <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/> for the full property catalog and reconciliation details.

