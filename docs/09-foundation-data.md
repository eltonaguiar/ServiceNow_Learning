# 09 — Foundation data: the load nobody puts on the plan

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

Every module in this kit assumes a layer underneath it already exists: **people, places,
groups, and the clock.** ServiceNow calls that layer foundation data. It is not a module, it
has no guided setup of its own, and it is the single most common reason a brand-new
implementation "doesn't work" while every setting looks correct.

An incident with no caller, no assignment group, no location and no business-hours schedule
is not a broken module. It is a missing foundation.

---

## The invisible dependency

| What you try to do | What it silently needs |
|---|---|
| Raise an incident | A caller (`sys_user`), an assignment group, a location for TZ, a schedule for SLA |
| Approve a change | A manager chain (`sys_user.manager`) and group membership |
| Route to a team | An assignment group with members and a manager |
| Report by department / region | `cmn_department`, `cmn_location` populated on users |
| Run an SLA | Business hours schedule; wrong time zone = wrong clock |
| Allocate licence cost | `cmn_cost_center` on users and assets |
| Discover a server | A location to attach it to, else impact analysis has no geography |

No error message tells you this. The record simply sits there, unassigned and unscheduled.

---

## The objects, in load order

Load in dependency order. Each row depends on the rows above it.

| # | Object | Table | Depends on | Critical fields |
|---|---|---|---|---|
| 1 | Company | `core_company` | — | `name`, `manufacturer` flag |
| 2 | Location | `cmn_location` | company | `name`, `parent`, **`time_zone`**, `street`/`city`/`country` |
| 3 | Department | `cmn_department` | company | `name`, `parent`, `dept_head` |
| 4 | Cost centre | `cmn_cost_center` | department | `name`, `account_number`, `department` |
| 5 | Users | `sys_user` | company, location, department, manager | `user_name`, `active`, `department`, `manager`, `email` |
| 6 | Group types | `sys_user_group_type` | — | `name` (itil, service desk, change…) |
| 7 | Groups | `sys_user_group` | users, location, group type | `name`, `manager`, `parent`, `type`, `email` |
| 8 | Schedules / business hours | schedules (`cmn_*` — confirm names with the probe) | time zone | start/end times, work days, holidays |
| 9 | Categories / choice lists | `sys_choice` | — | the values your reports will group by |

**Verify the schedule table names on your instance.** They vary by release and the probe
lists every `cmn_*` table it finds — that is faster and safer than trusting a blog.

---

## How to load it (three ways, in increasing order of effort)

| Method | Use when | Notes |
|---|---|---|
| **Manual entry** | ≤ 20 records, or a lab | Slowest, but teaches the dependencies by hand — which is the point of Lab 04 |
| **Import Set from CSV** | The normal case | `All > System Import Sets > Load Data`. Map by column, use **coalesce** on `user_name` / `name` so re-imports update instead of duplicate |
| **Integration / feed** | Users and org come from HR or AD | Transform map + a scheduled import. Coalesce is non-negotiable; a second feed without it doubles your users |

Rules that save a week:

1. **Coalesce on a stable key** (`user_name`, group `name`, location `name`). Without it,
   every re-run duplicates the whole file.
2. **Load a 20-row slice first**, eyeball the references, then load the rest.
3. **Never delete-and-recreate users.** Update them. Deactivate with `active = false`.
4. **Do it in dev**, promote with update sets for config and a documented import for data.
5. **Record the source of truth** for each object. Two feeds writing the same field is a
   data-quality incident waiting to happen.

---

## Minimum viable foundation (what "done" looks like)

You can stop here for a lab or a demo:

- [ ] 1 company, 2 locations with real time zones
- [ ] 2 departments, 1–2 cost centres
- [ ] 6 users: 1 requester, 3 agents, 1 manager, 1 service account for integrations
- [ ] 3 groups with managers and members: service desk, facilities, change
- [ ] 1 business-hours schedule (e.g. Mon–Fri 08:00–17:00, your TZ)
- [ ] Categories: a deliberately short list (5–7), not the OOB 40

For a real deployment, add: full user base with manager chains, location hierarchy by
region, department tree matching finance, group types, holiday calendars, and the HR/AD feed
with coalesce.

---

## Verify it (five minutes, no guessing)

Run `scripts/sn_probe.js` — its `foundation` section reports row counts per object and flags
empties. Then check these by hand:

| Check | Where | Pass |
|---|---|---|
| Users have org data | Users list, add columns Department / Location / Manager | < 5% blank |
| Groups are staffed | Groups list, Members column | every routing group has a manager + members |
| Locations have TZ | Locations list, Time zone column | none blank |
| Schedule exists | Schedules list | at least one business-hours schedule |
| Categories are short | Incident form, Category choice | you can name every value in a meeting |
| No duplicate users | Users list grouped by `user_name` | zero duplicates |

---

## How the modules consume it (so you can argue for the load)

| Module | Uses foundation as |
|---|---|
| Incident / Change | caller, assignment group, manager approvals, SLA schedule |
| CMDB | CI location, managed-by group, department ownership |
| SAM / ITAM | cost centre, department, location — the spend dimensions |
| HRSD | department, manager, location (and confidentiality on top) |
| CSM | company/account, contact location |
| Analytics | every breakdown you will want later is one of these fields |

This is why a "quick ITSM pilot" with no foundation data produces dashboards nobody trusts:
the breakdowns are empty because the dimensions were never loaded.

---

## Ten mistakes

1. Users before departments (every user ends up with an empty org).
2. No coalesce key → duplicate everything on the second import.
3. Delete-and-recreate users → broken historical approvals.
4. Manager chains that loop (A manages B, B manages A).
5. A location parented to its own child.
6. Time zone left blank → SLAs compute against UTC.
7. One group per person instead of per function.
8. 40 categories retained "because they were there" → unusable reporting.
9. Loading straight into production because "it's just reference data".
10. Two feeds writing the same field with no agreed owner.

---

## Official sources

- Product documentation (users, groups, locations, departments, schedules, import sets) — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Now Create Success Packs (foundation data load is an explicit early phase) — <https://learning.servicenow.com/lxp> search "Now Create" (read 2026-11-04)
- Now Learning (user administration and data-loading fundamentals) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Community (import/coalesce gotchas) — <https://community.servicenow.com/> (read 2026-11-04)

> Table and field names for schedules vary by release; the probe resolves them on your
> instance rather than this page asserting them.
