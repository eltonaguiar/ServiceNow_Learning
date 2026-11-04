# Mandatory vs Critical vs Optional Fields

**Agent:** Kilo  
**Date:** 2026-11-04  

---

## Purpose

This document helps you understand the difference between mandatory, critical, and optional fields in ServiceNow — and why knowing the difference matters when building forms, scripts, and integrations.

---

## Field Importance Levels

| Level | Definition | Example | Consequence of Missing |
|-------|-----------|---------|----------------------|
| **Mandatory** | The system won't let you save the record without it | `number` on Incident, `short_description` on Incident | Record won't save. System throws an error. |
| **Critical** | The record saves, but the process breaks downstream | `assignment_group` on Incident, `state` on Change | Record saves but workflows break, SLAs don't start, notifications don't fire |
| **Optional** | Nice to have, but not required for core functionality | `comments`, `work_notes`, `corporate` | Record saves fine. Process continues. Data is just incomplete. |

---

## Mandatory Fields

**Definition:** Fields that must have a value before the record can be saved. ServiceNow enforces this at the database level.

### How to Identify Mandatory Fields

1. Look for a red asterisk (*) next to the field label on the form
2. Check the table definition: System Definition → Tables → [table] → Fields → look for `Mandatory = true`
3. Try saving without the value — the system will block you

### Examples

| Table | Mandatory Fields | Why |
|-------|-----------------|-----|
| `incident` | `number`, `short_description`, `state` | Every incident needs a number, description, and state |
| `change_request` | `number`, `short_description`, `state` | Every change needs to be identifiable and trackable |
| `cmdb_ci` | `name` | Every CI needs a name to be identifiable |
| `sn_hr_core_case` | `number`, `short_description`, `state` | Every HR case needs tracking |

### Best Practice

Never try to bypass mandatory fields. If you need to create a record without a value for a mandatory field, you're likely approaching the problem wrong.

---

## Critical Fields

**Definition:** Fields that aren't enforced by the database but are required for business processes to work correctly. The record saves, but downstream processes fail.

### How to Identify Critical Fields

1. Look at business rules that reference the field
2. Look at workflows and flows that depend on the field
3. Look at notifications that use the field
4. Check SLAs that depend on the field
5. Ask the process owner

### Examples

| Table | Critical Field | Why It's Critical |
|-------|---------------|-------------------|
| `incident` | `assignment_group` | Without it, no one knows who should work the incident |
| `incident` | `assigned_to` | Without it, no specific person is accountable |
| `change_request` | `risk` | Without it, the change can't be properly assessed |
| `cmdb_ci` | `ip_address` | Without it, discovery and ITOM can't find the device |
| `sn_hr_core_case` | `employee` | Without it, HR doesn't know who the case is for |

### Downstream Impacts of Missing Critical Fields

| Missing Field | Downstream Impact |
|---------------|-------------------|
| `assignment_group` on Incident | SLA doesn't start, no one gets notified, incident sits unassigned |
| `assigned_to` on Incident | No clear accountability, incident may be ignored |
| `state` on Change | Change can't progress through approval workflow |
| `risk` on Change | Change advisory board can't assess risk level |
| `employee` on HR Case | HR doesn't know which employee needs help |

---

## Optional Fields

**Definition:** Fields that are nice to have but not required for core functionality.

### Examples

| Table | Optional Field | Why It's Optional |
|-------|---------------|-------------------|
| `incident` | `comments` | Helpful for context, but not required to resolve |
| `incident` | `work_notes` | Internal notes, helpful but not required |
| `cmdb_ci` | `serial_number` | Helpful for tracking, but CI can exist without it |
| `change_request` | `justification` | Helpful for auditors, but change can proceed without it |

### Best Practice

Fill optional fields when you have the information, but don't block process flow waiting for them.

---

## Field Decision Matrix

Use this table to decide how to treat each field:

| Field Characteristic | Mandatory | Critical | Optional |
|---------------------|-----------|----------|----------|
| Database prevents save without value | Yes | No | No |
| Business process breaks without it | Yes | Yes | No |
| Workflows depend on it | Yes | Yes | No |
| Notifications use it | Often | Yes | Rarely |
| SLAs depend on it | Often | Yes | Rarely |
| User can proceed without it | No | Yes | Yes |

---

## Practical Exercise

Pick any table (e.g., `incident`) and answer:

1. What are the 3 most important mandatory fields?
2. What are the 3 most important critical fields?
3. What are 3 optional fields you often see filled in?
4. What happens if you create an incident without `assignment_group`?
5. What happens if you create an incident without `comments`?

---

## Related Lists

**Note:** Related Lists are different from fields. They show related records (e.g., all tasks related to an incident, all changes related to a CI).

| Related List Type | Mandatory? | Critical? | Notes |
|-------------------|-----------|-----------|-------|
| Child records (e.g., tasks on a case) | No | Often | Important for workflows |
| Related records (e.g., CI on an incident) | No | Critical | Links records together |
| Approval records | Sometimes | Often | Needed for change approval |

---

*Generated by Kilo on 2026-11-04.*
