# 06 — Inventory: Guided Setup, OOB flows, playbooks, integrations, metrics

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

The question this page answers: **"does ServiceNow already do this?"** — because in every
module, at least half of what a project calls "requirements" already ships.

**Do not trust this table for your release.** It is a checklist of what to look for; the
probe tells you what you actually have. Where an entry says *verify*, that is deliberate:
menu labels, flow names and dashboard packs change between family releases and with
entitlement.

---

## How to enumerate it on your own instance (5 minutes)

| What | Where | Query the probe uses |
|---|---|---|
| Guided Setup modules | Filter navigator: type `guided setup` | `sys_app_module` where `title LIKE '%Guided Setup%'` |
| Installed apps/plugins | All Available Applications | `v_plugin` |
| Flows and subflows | Flow Designer | `sys_hub_flow` count + names |
| Playbooks | Process Automation Designer | `sys_pd_process_definition` (verify) |
| Scripted REST APIs | System Web Services | `sys_ws_definition` |
| Outbound REST messages | System Web Services | `sys_rest_message` |
| Dashboards | Platform Analytics | `pa_dashboards` (verify) |
| Reports | Reports | `sys_report` count |
| Indicators | Platform Analytics | `pa_indicators` count |

Running the probe once answers all nine rows for *your* instance in a single pass.

---

## Per-app inventory

| App | Guided Setup | OOB automation to check before building | Integrations / spokes | Metrics & dashboards |
|---|---|---|---|---|
| **Platform** | n/a | Flow Designer templates, approval actions | — | Platform Analytics basics |
| **ITSM — Incident** | **Yes** (verify label) | Assignment/escalation flows, SLA task flows, notify-on-comment, "create knowledge" loop | Email → incident, Teams/Slack notify, monitoring → alert | Open by priority, MTTR, reassignment count, SLA % |
| **ITSM — Problem/Change** | **Yes** (verify) | Change approval flow, conflict detection, standard change templates, problem→known error | DevOps change creation, calendar sync | Change success rate, unauthorized changes, lead time |
| **CMDB / ITOM** | **Yes** | Health scoring jobs, discovery create/update, service mapping (separate entitlement) | Service Graph Connectors (SCCM, Intune, AWS, Azure, vCenter), Discovery, ACC | CMDB health, duplicate count, orphan CIs |
| **SAM / ITAM** | **Yes** (verify) | Asset lifecycle flows, reconciliation jobs, renewal notifications | SCCM/Intune/Jamf feeds, publisher connectors (Pro) | Licence position, spend, normalisation gaps, renewals |
| **HRSD** | **Yes** | Case triage, lifecycle events (onboarding/offboarding), document tasks | Workday/SuccessFactors spokes, DocuSign, Employee Center | Case volume, time to close, CSAT, SLA per service |
| **SecOps** | **Yes** | Alert→incident correlation, response tasks, intel enrichment, post-incident review | Splunk, CrowdStrike, Defender, Palo Alto, Qualys, STIX/TAXII | MTTD/MTTR, alerts per source, false positives |
| **CSM** | **Yes** | Case assignment, entitlement validation, CSAT survey, case→work order | Email/chat/messaging spokes, ERP/CRM sync, portal | FCR, CSAT, backlog by account, entitlement breaches |
| **FSM** | **Yes** (verify) | Work order → task → assignment → schedule, travel/time tracking, mobile sync | Maps/travel time, Now Mobile, CSM/ITSM order creation | On-time arrival, first-time fix, utilisation |
| **GRC / IRM** | **Yes** (verify) | Risk assessment cycles, control attestations, issue→remediation, policy acknowledgement | VR feed, TPRM questionnaires, regulatory content | Residual risk, control test pass rate, overdue issues |
| **App Engine** | n/a (builder) | App templates (request, approvals) | REST step in Flow Designer, spokes from app scope | App usage analytics |
| **Integration** | per-spoke only | Flow Designer REST step, IntegrationHub actions | REST/SOAP/JDBC/LDAP/email/file, MID Server for on-prem | Outbound HTTP error rate, job duration |
| **Analytics** | **Yes** (verify) | OOB content packs per module, data collectors | Power BI/Tableau export, warehouse snapshots | Indicator → breakdown → dashboard is the model |

---

## What "OOB first" looks like in practice

Before you write a single line of script or build a flow:

1. **Search Flow Designer** for the app name. If a flow already does 80% of it, copy it and
   modify — copying keeps the OOB one upgradeable.
2. **Check the app's Guided Setup** steps for the capability. If the vendor thought about it,
   there is usually a config path.
3. **Check the Store** for a spoke/connector before writing an integration. A certified
   spoke is cheaper than your maintenance forever.
4. **Check OOB dashboards** before designing one. Start from theirs, delete widgets nobody
   opens, add one that answers a real question.
5. **Only then** design custom. And when you do, record *why OOB was insufficient* — future
   you will ask.

---

## Metrics: the four questions every dashboard must answer

Most dashboards fail because they answer "what happened" and nothing else. A dashboard that
gets looked at answers all four:

1. **Are we okay?** — one number against a target (SLA %, compliance %, on-time %)
2. **Where is it bad?** — a breakdown (by group, priority, publisher, territory)
3. **What changed?** — a trend, not a snapshot
4. **What do I do about it?** — a link to the filtered list of the actual records

If a widget does not serve one of those, it is decoration. Delete it.

---

## Official sources

- Product documentation (Guided Setup per app, OOB content, dashboards) — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Now Create Success Packs (what "out of the box" is *supposed* to deliver per phase) — <https://learning.servicenow.com/lxp> search "Now Create" (read 2026-11-04)
- ServiceNow Store (spokes, connectors, activation notes) — <https://store.servicenow.com/store> (read 2026-11-04)
- Now Learning (app courses list the OOB features) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Community (which OOB flow people actually use) — <https://community.servicenow.com/> (read 2026-11-04)
