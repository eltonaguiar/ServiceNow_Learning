# LAB 04 — Foundation data, then prove a module works (60 min)

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

**Goal:** build the smallest foundation data set that makes ITSM actually behave, then break
each dependency one at a time and watch the module fail in a way no error message explains.

**Why this lab exists:** every other lab starts on top of an instance that already has
people, groups and a clock. This one builds that layer by hand so you know what "loaded" means.

**Timebox:** 15 min load, 20 min prove, 20 min break, 5 min record.

---

## Prerequisites

- [ ] PDI or dev instance, admin
- [ ] `LAB-00-ORIENTATION.md` done (you can read a form and a related list)
- [ ] Empty-ish instance, or a note of which records are yours (prefix names with `LAB-`)

---

## Part 1 — Load in dependency order (15 min)

Do not jump ahead. Each step's record references the one above it.

| # | Create | Where | Values for this lab |
|---|---|---|---|
| 1 | Company | `All > Organization > Companies` | `LAB-Acme` |
| 2 | Location ×2 | `All > Organization > Locations` | `LAB-Toronto` (America/Toronto), `LAB-London` (Europe/London) — **set the time zone** |
| 3 | Department ×2 | `All > Organization > Departments` | `LAB-IT`, `LAB-Facilities` |
| 4 | Cost centre | `All > Organization > Cost Centers` | `LAB-CC-100`, department `LAB-IT` |
| 5 | Users ×6 | `All > User Administration > Users` | 1 requester, 3 agents, 1 manager, 1 `lab.integration` service account |
| 6 | Group ×3 | `All > User Administration > Groups` | `LAB-Service Desk`, `LAB-Facilities`, `LAB-Change` — give each a **manager** and **members** |
| 7 | Schedule | `All > Service Level Management > Schedules` | `LAB-Business Hours`: Mon–Fri 08:00–17:00 |

Set users' `department`, `location`, and `manager` **while creating them** — retrofitting is
the mistake this lab is designed to prevent.

**Checkpoint:** open one user. Department, location and manager are populated. Open one
group. Manager and at least one member are populated.

---

## Part 2 — Prove the module works because of it (20 min)

1. Impersonate the requester. Create an incident: caller = them, category = a real value,
   short description `LAB foundation check`.
2. As admin, set `assignment_group = LAB-Service Desk`.
3. Open the incident and look at:
   - **Caller** resolves to a real user with a department (not blank).
   - **Task SLA** related list: a record exists and its clock is *running*, not paused.
   - The SLA's business-hours behaviour matches `LAB-Business Hours` (a ticket raised at
     22:00 should not burn 7 hours overnight).
4. Build a report: incidents by **Department**. It groups — because the caller has one.
5. Build a report: incidents by **Location**. Same.

If step 3 has no Task SLA record, the SLA definition, the schedule, or both are missing —
that is foundation, not "SLA is broken".

---

## Part 3 — Break each dependency (20 min) — the actual lesson

| Break | What you will see | The lesson |
|---|---|---|
| Clear the caller's `department` | Report by Department shows `(empty)` | Reporting dimensions are foundation, not reporting config |
| Set `LAB-Toronto` time zone to UTC | SLA clock shifts by hours, breach times look wrong | Time zone is an SLA setting you never knew you had |
| Remove the group's manager | Escalation/approval path has nowhere to go | A group without a manager is an orphan queue |
| Give a user no `manager` | Manager approval stage stalls or is skipped | Approvals walk the manager chain |
| Create a second user with the same `user_name` | Assignment and history become ambiguous | Coalesce keys exist for a reason |
| Point `LAB-IT`'s parent at `LAB-IT` | Tree views break / recursion | Parent fields must not self-reference |

Fix each one. Note which screen told you what was wrong — usually a report, not an error.

---

## Part 4 — Record what "loaded" means (5 min)

Write five lines your successor could act on:

1. Company / locations / departments created: …
2. Users: count, and how many have department + manager: …
3. Groups: routing groups, each with manager + members: …
4. Schedule: name, hours, time zone: …
5. What still has no owner (real answer, not "none"): …

Then run `scripts/sn_probe.js` and confirm the `foundation` section shows non-zero rows for
what you just built.

---

## Common mistakes (all seen in real deployments)

1. Users loaded before departments and companies.
2. Locations with no time zone — the quietest SLA bug on the platform.
3. Groups with members but no manager (or the reverse).
4. Manager chains that loop.
5. Two users with the same `user_name` from two feeds.
6. Deleting a user instead of deactivating them.
7. One group per person instead of per function.
8. 40 OOB categories left in place, then unusable reporting.
9. No business-hours schedule, then blaming the SLA engine.
10. Loading it all straight into production.

---

## Prove it

- [ ] Six users, three groups, two locations with time zones, one schedule, all referencing each other
- [ ] An incident with a real caller, group and a **running** Task SLA
- [ ] Two reports group by Department and Location without blanks
- [ ] You broke three dependencies and can name the symptom each produced
- [ ] Probe `foundation` section is non-zero

---

## Official sources

- Product documentation (users, groups, locations, departments, schedules, SLA definitions) — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Now Learning (user administration and foundation data fundamentals) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Now Create Success Pack (foundation data is an explicit early phase) — <https://learning.servicenow.com/lxp> search "Now Create" (read 2026-11-04)
- Community (import coalesce and duplicate-user gotchas) — <https://community.servicenow.com/> (read 2026-11-04)
