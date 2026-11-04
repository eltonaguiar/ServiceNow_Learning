# 04 — Mandatory vs useful vs optional fields (and which related lists to turn on)

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

There are three different kinds of "required" in ServiceNow, and conflating them is one of
the most common beginner mistakes:

| Kind | Where it lives | Blocks |
|---|---|---|
| **Dictionary-mandatory** | `sys_dictionary.mandatory = true` | UI, API, import, scripts — everything |
| **UI-policy-mandatory** | `sys_ui_policy` | The form only (e.g. close_code on resolve) |
| **Data-policy-mandatory** | `sys_data_policy` | UI + import, not direct script writes |

So "the field is required" is never a complete sentence. Ask: *required by what, for whom,
at which state?*

**How to check yours in one run:** `scripts/sn_probe.js` reads `sys_dictionary` for every
listed table and prints the mandatory fields, plus the related lists from
`sys_ui_related_list`. That output beats any table on this page, because it is your
instance.

---

## The golden rule for related lists

A related list is cheap to configure and expensive to under-configure. The test: *would
someone working this record need to ask a follow-up question that this list answers?*

| Related list | Verdict | Why |
|---|---|---|
| Task SLA (incident/change) | **Critical** | Without it nobody can see if the clock is running or paused |
| Approvers | **Critical** where approvals exist | Silent approval queues are the #1 "why is this stuck" cause |
| Affected CIs | **Critical** for impact | Impact analysis and problem correlation depend on it |
| Additional comments / Work notes | **Critical** | The audit trail; also where flows write |
| Child tasks (change tasks, catalog tasks) | **Critical** | Work is executed at task level, not parent level |
| Contracts on an asset/licence | **Critical** (SAM) | Entitlement without provenance fails audit |
| Relationships (CMDB, both directions) | **Critical** | One-directional relationship data breaks impact analysis |
| Knowledge articles | Useful | Speeds resolution; OOB "create knowledge" loop |
| Parent/child incidents | Useful | Stops duplicate effort |
| Attachments | Useful | Evidence for audit/compliance work |
| Audit history / field changes | Useful (on demand) | Who changed priority and when |
| SLAs on a service | Optional | Only if you model service-level commitments, not tickets |

---

## Per-table field guidance

### `incident`
| Field | Verdict | Note |
|---|---|---|
| `number` | Critical | Never hand-edit; it is the identifier people quote |
| `caller_id` | Critical | Wrong caller ⇒ wrong SLA, comms and reporting |
| `short_description` | Critical (dictionary) | The searchable one-line summary |
| `assignment_group` | Critical | Empty = orphaned ticket, no matter what else you configured |
| `state` | Critical | Drives SLA, flows, closure rules, metrics |
| `impact` + `urgency` | Critical | Priority derives from them via a matrix |
| `close_code` + `close_notes` | Critical at close (UI policy) | Blank closes corrupt reporting |
| `cmdb_ci` | Useful | Links impact analysis |
| `category` / `subcategory` | Useful | Reporting; keep the list short |
| `assigned_to` | Useful | Person, but group is what routes |
| `location`, `department` | Optional | Often derivable from the caller |
| `parent_incident` | Optional | Use for genuinely related work |

### `change_request`
Critical: `type`, `short_description`, `start_date`/`end_date`, `assignment_group`,
`risk`, `impact`, `implementation_plan`, `backout_plan`, `test_plan`.
Useful: `cmdb_ci`, `cab_required`, `conflict_status`, `review_status`.
Optional: justification prose fields, validation dates.

### `problem`
Critical: `short_description`, `assignment_group`, `state`, `cause`/`fix` at close.
Useful: `cmdb_ci`, linked incidents (related list), `known_error` link, `workaround`.

### `cmdb_ci` (+ subclasses)
Critical: `name`, `sys_class_name`, `install_status`, `operational_status`, `environment`,
`managed_by_group`, `discovery_source`.
Useful: `fqdn`/`ip_address`, `serial_number`, `assigned_to`, `model_id`, `location`.
Optional: business fields (`u_*`) — only when a report demands them.

### `alm_asset` / software licence
Critical: `asset_tag`, `model_id`, `state`/`substate`, `assigned_to`, contract dates,
licence metric and quantity on the entitlement.
Useful: `cost`, `cost_center`, `po_number`, `vendor`, `warranty_expiration`.
Optional: depreciation, `reserved_for`.
See [`08-SAM-SETUP.md`](08-SAM-SETUP.md) for the full SAM matrix.

### `sn_hr_core_case`
Critical: `subject_person`, `hr_service`, `state`, `opened_for`/`opened_by`,
`assignment_group`.
Useful: `priority`, `due_date`, `confidential` flag, `short_description`.
Optional: attachments, department-derived fields.

### `sn_si_incident`
Critical: `category`, `priority`, `assignment_group`, `state`, observables.
Useful: `cmdb_ci`, `business_impact`, MITRE technique mapping, related alerts.
Optional: external ticket reference, regulatory flags.

### `sn_customerservice_case`
Critical: `account`, `contact`/`consumer`, `entitlement`, `case type`, `priority`.
Useful: `product`, `channel`, `assignment_group`.
Optional: billing fields, special handling notes.

### `wm_order` / `wm_task`
Critical: `territory`, `scheduled_start`/`scheduled_end`, `assigned_agent`/crew, task type
+ skills, location coordinates.
Useful: `priority`, `estimated_duration`, parts required.
Optional: billing codes, equipment detail.

---

## Related lists: the four you should add today

On most implementations these four are missing or half-configured, and each one costs
someone a meeting:

1. **Task SLA** on incident and change — makes the clock visible.
2. **Approvers** on anything that can block — makes queues visible.
3. **Affected CIs** on incident, change, problem — makes impact visible.
4. **Relationships** on CI forms (both directions) — makes dependency visible.

Everything else is a judgment call. More related lists is not better; *the four* are better.

---

## How to change them without fear

- **Fields:** open a record → right-click header → *Configure* → *Form Layout*. This is a
  UI change, reversible, and does not touch the schema.
- **Related lists:** *Configure* → *Related Lists*; you can add, reorder and rename labels.
- **Making a field mandatory:** prefer **UI policy** (scoped to a form and state) over
  dictionary changes. A dictionary change applies to APIs and imports and will break
  integrations that were happily writing before.
- **Always** do this in a dev instance, capture it in an update set, then promote.

---

## Official sources

- Product documentation (dictionary, UI policies, data policies, related lists) — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Now Create Success Packs (the pack states which fields matter for the process) — <https://learning.servicenow.com/lxp> search "Now Create" (read 2026-11-04)
- Now Learning fundamentals — <https://learning.servicenow.com/lxp> (read 2026-11-04)

> Field lists here are guidance, not schema truth. Your instance is the authority: run the
> probe, read `sys_dictionary`.
