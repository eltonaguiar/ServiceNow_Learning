# ServiceNow Success Packs — Prerequisites & Installation Guide

**Agent:** Hermes Agent  
**Date:** 2026-11-04  
**Purpose:** Document what you need before installing any ServiceNow Success Pack, plus step-by-step installation and validation.

---

## What Is a Success Pack?

A Success Pack is a pre-built content package from ServiceNow that includes:
- Tables (data structures)
- Forms (data entry screens)
- Workflows (automated processes)
- Dashboards (visual reports)
- Playbooks (response procedures)
- Integrations (connections to other systems)

Think of it like an app you install on your phone — but for your ServiceNow instance.

---

## Universal Prerequisites (Required for ALL Success Packs)

Before installing ANY Success Pack, you must have:

| # | Prerequisite | ELI5 Explanation | Critical? | How to Verify |
|---|-------------|-----------------|-----------|---------------|
| 1 | ServiceNow instance | You need a running ServiceNow system | CRITICAL | Log in to your instance URL |
| 2 | Admin role | You need permission to install applications | CRITICAL | Check your user record has "admin" role |
| 3 | Network access to ServiceNow Store | You need to download the pack from ServiceNow's app store | CRITICAL | Try opening `https://store.servicenow.com` |
| 4 | Sufficient storage | Success Packs can be 100MB–5GB | MANDATORY | Check instance storage in System Diagnostics |
| 5 | Accepted license terms | You must agree to ServiceNow's terms | MANDATORY | Check during installation wizard |

---

## Success Pack Type-Specific Prerequisites

### ITSM Success Pack
| Prerequisite | ELI5 | Critical? | Where to Configure |
|-------------|------|-----------|-------------------|
| Incident Management process defined | You know how tickets should flow | CRITICAL | `Incident > Administration > Process` |
| Change Management process defined | You know how changes get approved | CRITICAL | `Change > Administration > Process` |
| Problem Management process defined | You know how root causes are found | CRITICAL | `Problem > Administration > Process` |
| CMDB populated | You know what computers/services you have | MANDATORY | `CMDB > Tables` |
| Assignment groups created | You know which teams handle what | CRITICAL | `User Administration > Groups` |

### CSM (Customer Service Management) Success Pack
| Prerequisite | ELI5 | Critical? | Where to Configure |
|-------------|------|-----------|-------------------|
| Customer accounts created | You know who your customers are | CRITICAL | `Customer Service > Accounts` |
| Case categories defined | You know what types of issues customers report | CRITICAL | `Customer Service > Administration > Case Categories` |
| Service offerings defined | You know what services you provide | MANDATORY | `Customer Service > Service Offerings` |

### HRSD (HR Service Delivery) Success Pack
| Prerequisite | ELI5 | Critical? | Where to Configure |
|-------------|------|-----------|-------------------|
| HR case categories defined | You know what types of HR issues employees have | CRITICAL | `HR Administration > Case Categories` |
| Employee documents configured | You know what HR forms you use | MANDATORY | `HR Administration > Documents` |
| HR teams assigned | You know which HR staff handle what | CRITICAL | `User Administration > Groups` |

### SecOps Success Pack
| Prerequisite | ELI5 | Critical? | Where to Configure |
|-------------|------|-----------|-------------------|
| Security incident response process defined | You know what to do when hacked | CRITICAL | `Security Incidents > Administration` |
| Vulnerability response process defined | You know how to fix security holes | CRITICAL | `Vulnerability Response > Administration` |
| Threat intelligence sources configured | You know where to get security alerts | MANDATORY | `SecOps > Threat Intelligence` |

### ITOM (IT Operations Management) Success Pack
| Prerequisite | ELI5 | Critical? | Where to Configure |
|-------------|------|-----------|-------------------|
| Discovery installed | You can find computers on your network | CRITICAL | `Discovery > Discovery Schedules` |
| Service Mapping configured | You know how services connect | CRITICAL | `Service Mapping > Maps` |
| Event Management enabled | You can receive alerts from monitoring tools | CRITICAL | `Event Management > Administration` |

### App Engine Studio
| Prerequisite | ELI5 | Critical? | Where to Configure |
|-------------|------|-----------|-------------------|
| App Engine permissions | You can build low-code apps | MANDATORY | `User Administration > Roles > app_engine_admin` |
| Development instance | You have a place to build without breaking things | CRITICAL | Separate dev instance |

---

## Pre-Installation Checklist

Run this checklist before installing any Success Pack:

```
[ ] I have admin access to the ServiceNow instance
[ ] I can access the ServiceNow Store from my browser
[ ] The instance has sufficient storage space
[ ] I know which application(s) this Success Pack extends
[ ] Required base applications are installed and active
[ ] Required user roles are assigned to my account
[ ] I have reviewed the Success Pack documentation
[ ] I have a backup or snapshot of the instance (if production)
[ ] I plan to test in a non-production instance first
```

---

## Installation Steps

1. **Navigate to the Store:** `System Applications > All > Store`
2. **Search for the Success Pack:** Type the name (e.g., "ITSM Success Pack")
3. **Review details:** Read the description, prerequisites, and release notes
4. **Click "Get" or "Install":** Starts the download
5. **Accept terms:** Check the box to accept the license agreement
6. **Select scope:** Choose the application scope (usually the Success Pack's own scope)
7. **Wait for installation:** Progress bar shows status
8. **Activate the application:** Go to `System Applications > All Applications` and set the Success Pack to Active
9. **Run guided setup (if provided):** Some packs include a setup wizard
10. **Verify:** Check that new tables, modules, and dashboards appear

---

## Post-Installation Validation

After installing, verify:

| Check | How to Verify | Pass Criteria |
|-------|--------------|---------------|
| New modules appear | Left navigation shows new menu items | Expected modules visible |
| New tables exist | `System Definition > Tables` shows new tables | Expected tables present |
| New dashboards load | `Dashboards > All` shows new dashboards | Dashboards open without errors |
| Workflows active | `System Policy > Workflow > Workflows` shows active workflows | Workflow state = Published |
| Users can access | Test with a non-admin user with appropriate roles | User can see expected modules |

---

## Common Installation Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Installing without admin role | "Insufficient permissions" error | Assign admin role to your user |
| Missing base application | "Dependency not found" error | Install required base application first |
| Installing in production directly | Broke live system for everyone | Test in dev/sub-prod first |
| Not activating after install | Modules don't appear | Set application to Active in `System Applications > All Applications` |
| Ignoring prerequisites | Installation fails partway | Review and complete all prerequisites first |
