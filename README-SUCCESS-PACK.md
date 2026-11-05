# ServiceNow Success Pack — Hermes (2026)

**Branch:** `hermes-success-pack-2026-11-06`  
**Generated:** 2026-11-06 by Hermes Agent  
**Source:** https://github.com/eltonaguiar/ServiceNow_Learning

## Purpose

This branch contains **SUCCESS_PACK_HERMES.MD** — a playbook for landing a ServiceNow role (Administrator, Developer, Consultant, Architect) in 2026, based on real success stories and deep-dive research into six high-demand ServiceNow modules.

## What's Inside

### SUCCESS_PACK_HERMES.MD

The main document covers:

1. **2026 ServiceNow Job Market Reality** — Canadian market data, top employers, certifications that matter
2. **Certification Roadmap** — CSA → CAD → CIS → CTA with prep time and jobs unlocked
3. **Getting Started Guide** for six modules:
   - **ITSM** (IT Service Management) — Incident, Problem, Change, CMDB, SLAs
   - **TSOM** (Telecom Service Operations Management) — Service orders, alarms, network inventory
   - **CSM** (Customer Service Management) — Cases, accounts, entitlements, portal
   - **FSM** (Field Service Management) — Work orders, dispatch, territories, scheduling
   - **Sales CRM** — Leads, opportunities, quotes, orders, pipeline
   - **HAM** (Hardware Asset Management) — Asset lifecycle, licenses, contracts
4. **Each module includes:**
   - Purpose and navigation breadcrumbs
   - Re-usable code / metadata (scopes, roles, business rules, UI policies, script includes, snippets)
   - Out-of-box features (flows, playbooks, dashboards, metrics)
   - Key table hierarchy (core tables, relationships, CMDB mapping)
   - Integrations (protocols, directions, purposes)
   - Key fields (critical fields and why they matter)
   - Common mistakes and fixes
   - Hands-on lab with step-by-step instructions
   - Quiz for self-check
5. **Evidence Portfolio** — What to show in interviews (screenshots, code snippets, lab validation)
6. **Job Search Strategy** — Canada-focused, ranked sources, blocked sources and workarounds
7. **Success Stories** — Patterns from real candidates who got hired
8. **30-Day Plan** — Week-by-week execution plan

## Module Quick Reference

| Module | Primary Table | Key Roles |
|--------|--------------|-----------|
| ITSM | `incident` | `itil`, `admin` |
| TSOM | `sn_tsom_service` | `sn_tsom.admin`, `sn_tsom.user` |
| CSM | `sn_customerservice_case` | `sn_customerservice_agent`, `admin` |
| FSM | `wm_order` | `wm_admin`, `wm_dispatcher`, `wm_agent` |
| Sales CRM | `sn_sales_opportunity` | `sn_sales.admin`, `sn_sales.user` |
| HAM | `alm_asset` | `asset`, `itil`, `sam` |

## Related Content in This Repo

- `docs/modules/itsm/itsm-guide.md` — Full ITSM module guide
- `docs/modules/tsom/tsom-guide.md` — Full TSOM module guide
- `docs/modules/csm/csm-guide.md` — Full CSM module guide
- `docs/modules/fsm/fsm-guide.md` — Full FSM module guide
- `docs/modules/sales-crm/sales-crm-guide.md` — Full Sales CRM module guide
- `docs/modules/ham/ham-guide.md` — Full HAM module guide
- `data/modules.json` — Machine-readable module metadata
- `labs/rest-message-integration/` — REST Message integration lab
- `labs/remote-table/` — Remote Table lab

## GitHub Pages

This branch deploys to GitHub Pages via `.github/workflows/pages.yml`. The published site includes the SUCCESS_PACK and all module docs.
