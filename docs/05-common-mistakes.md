# 05 — Common mistakes, by symptom

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

Format: **symptom → real cause → fix**. Start from the symptom you are seeing; the headings
are just where the mistakes tend to breed.

---

## "It works for me but not for them"

| Symptom | Real cause | Fix |
|---|---|---|
| Admin sees it, user does not | ACL/role, or UI policy hides it | Impersonate the user. Always. Add the role the user actually needs |
| Field is greyed out for one group only | UI policy with a condition on role/state | `sys_ui_policy` — check conditions before suspecting ACLs |
| Record visible in a list but 404 on open | Read allowed, write/read on related table missing | Check ACLs on both parent and child tables |
| Everything works until go-live | You tested as admin | Re-test the whole path as each persona before sign-off |

**Prevention:** impersonation is a habit, not a debugging step.

---

## "Nothing happens" (automation)

| Symptom | Real cause | Fix |
|---|---|---|
| Flow never fires | Trigger condition never true, or flow is inactive/draft | Flow Designer → check **active** + run a test with the same record |
| Flow fires but field unchanged | Action targets a different record, or field is read-only via data policy | Open the flow run → inspect each action's input/output |
| Notifications never sent | SMTP/email property unset (common in PDIs) | `sys_properties` email settings; send a test |
| Approval stuck forever | Approver inactive/no user, or approval rule never generated | Check `sysapproval_approver` records exist at all |
| Scheduled job "ran" but did nothing | Condition false, or scope/cross-scope access denied | System Logs → All, filter by job name |

**Prevention:** every automation gets one test record and one negative test.

---

## "The integration returns 200 but nothing happens"

| Symptom | Real cause | Fix |
|---|---|---|
| HTTP 200, no data | Error payload inside a 200 response; you never checked the body | Log the body; branch on it |
| 401 / 403 | Wrong credential, expired token, or missing scope | Connection & Credential alias; re-auth |
| 415 / 400 | Content-Type missing or wrong | Set `Content-Type: application/json` explicitly |
| Timeout on a slow API | Default timeout too short | Raise the REST message timeout; consider async |
| Works in Postman, fails in ServiceNow | Headers, TLS, or egress proxy differs | `sys_outbound_http_log` shows the exact request/response |
| Credentials leaked to a repo | Hardcoded in script or message body | Move to Connection & Credential; rotate; never in update sets |

**Prevention:** the first place you look after any failed call is
`All > System Logs > Outbound HTTP Requests`. Not the API vendor's status page.

---

## ITSM-specific

| Symptom | Real cause | Fix |
|---|---|---|
| Priority is always 3 | Impact/urgency defaults, or the matrix is missing | Check the priority lookup/matrix; set sane defaults |
| SLA always breached | SLA start condition wrong, or schedule (24×7 vs business hours) wrong | Inspect `task_sla` start/pause/stop fields |
| Reports show blank close codes | Closure enforced only by UI policy, bypassed by import/API | Add a data policy or business rule if the API path matters |
| Ticket bounced between groups | No routing rule, or default group on the record | Fix assignment rules before blaming people |
| Reopened tickets break metrics | State model reuses "in progress" for reopened | Add a distinct reopened state or measure on reopen count |

---

## CMDB-specific

| Symptom | Real cause | Fix |
|---|---|---|
| Thousands of duplicate CIs | No identification rules before load | Configure CI identifiers, then merge/dedupe deliberately (never bulk-delete) |
| Health score meaningless | Completeness measured on fields nobody populates | Pick 3 fields that matter, populate them, then score |
| Impact analysis empty | Relationships one-directional or missing | `cmdb_rel_ci` both sides; use the relationship editor |
| Discovery creates new CIs nightly | Identification rules mismatch discovery's keys | Align identifiers with discovery source attributes |

---

## SAM-specific (the expensive ones)

| Symptom | Real cause | Fix |
|---|---|---|
| "We are 40% non-compliant" | Partial discovery published as truth | Publish coverage % alongside; scope discovery wider before believing it |
| Same product listed three times | Normalisation not run/approved | Normalise, then map titles to products |
| Compliance flips monthly | Metric mismatch (per-core contract, per-device model) | Align metric to contract wording |
| Entitlement exists, no contract | Data entry without evidence | Every entitlement must trace to a PO/contract |
| Renewal missed | No 90-day alert | Renewal notification job + owner |

Full guide: [`08-SAM-SETUP.md`](08-SAM-SETUP.md).

---

## Learning-process mistakes (the meta ones)

| Symptom | Real cause | Fix |
|---|---|---|
| "I watched the course but can't do it" | No artifact produced | Do a lab; produce a probe sheet |
| Confidently wrong in a meeting | Learned from a blog/screenshot | Verify on instance + docs before teaching |
| Endless reading, no progress | Docs used as narrative | Question first, then docs |
| Rebuilding what shipped | Never read the Success Pack / OOB content | Inventory OOB before designing |
| Same module learned twice, forgotten | No teach-back | Write 5 sentences + one diagram from memory |

---

## The five that waste the most hours

1. Testing as admin.
2. Skipping `sys_outbound_http_log` when debugging integrations.
3. Changing dictionary mandatory flags instead of using UI policies.
4. Loading CMDB data before identification rules.
5. Publishing SAM compliance numbers without discovery coverage.

---

## Official sources

- Product documentation — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Now Support KB (known errors, exact error strings) — <https://support.servicenow.com/now> (read 2026-11-04)
- Community (practitioner gotchas) — <https://community.servicenow.com/> (read 2026-11-04)
- Now Learning (fundamentals that prevent half of these) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
