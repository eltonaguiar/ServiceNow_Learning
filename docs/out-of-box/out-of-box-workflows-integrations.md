# Out-of-Box Workflows, Integrations, Playbooks, Metrics & Dashboards

**Agent:** Kilo  
**Date:** 2026-11-04  

---

## Purpose

This document covers what ServiceNow provides out of the box (OOB) — workflows, integrations, playbooks, metrics, and dashboards — so you know what you get for free and what you need to build yourself.

---

## Out-of-Box Workflows

ServiceNow ships with pre-built workflows for common business processes.

### ITSM Workflows

| Workflow | Triggers On | What It Does | Where to Find |
|----------|-------------|--------------|---------------|
| Incident Assignment | Incident created | Assigns incident to appropriate group based on category | Workflow → All |
| Incident Escalation | Incident priority changes | Escalates high-priority incidents to management | Workflow → All |
| Change Approval | Change request created | Routes change through approval chain | Workflow → All |
| Problem Resolution | Problem resolved | Closes related incidents and tasks | Workflow → All |

### How to View Workflows

1. Go to **Workflow → All**
2. Search for the workflow name
3. Click the workflow name to view the diagram
4. Click **Edit** to see the activities

### What to Look For

- Which table the workflow runs on
- What activities are included (approvals, notifications, script actions)
- What conditions start the workflow
- What the end state is

---

## Out-of-Box Integrations

ServiceNow connects to other systems out of the box.

### Outbound REST Messages

| Integration | What It Does | Where to Find |
|-------------|--------------|---------------|
| Outbound REST Message | Sends data from ServiceNow to another system | System Web Services → Outbound REST Messages |

### Inbound REST APIs

| API | What It Does | Where to Find |
|-----|--------------|---------------|
| Table API | Create, read, update, delete records via REST | System Web Services → Table API |
| Record API | Create, read, update, delete specific records | System Web Services → Record API |

### Import Sets

| Import Type | What It Does | Where to Find |
|-------------|--------------|---------------|
| CSV Import | Import data from CSV files | System Import Sets → Load Data |
| Excel Import | Import data from Excel files | System Import Sets → Load Data |

### MID Server

| Component | What It Does | Where to Find |
|-----------|--------------|---------------|
| MID Server | Connects ServiceNow to on-premise systems | MID Server → Servers |

### How to Test Integrations

1. **Outbound REST Message:** Create a REST Message, set the endpoint to a public API (e.g., `https://jsonplaceholder.typicode.com/posts`), run it, check the response
2. **Inbound Table API:** Use a tool like Postman or curl to POST to `https://your-instance.service-now.com/api/now/table/incident`
3. **Import Set:** Upload a CSV file and watch it create records

---

## Out-of-Box Playbooks

ServiceNow provides pre-built playbooks for common business processes.

| Playbook | What It Does | Where to Find |
|----------|--------------|---------------|
| Incident Response | Guides responders through incident handling | Flow Designer → Playbooks |
| Change Management | Guides changes through approval and implementation | Workflow → Change Management |
| Major Incident | Coordinates response to major incidents | Flow Designer → Playbooks |

---

## Out-of-Box Metrics & Indicators

ServiceNow tracks these metrics out of the box:

### ITSM Metrics

| Metric | What It Measures | Where to Find |
|--------|-----------------|---------------|
| Incident Volume | Number of incidents over time | Performance Analytics → Indicators |
| Mean Time to Resolve | Average time to resolve incidents | Performance Analytics → Indicators |
| Change Success Rate | Percentage of successful changes | Performance Analytics → Indicators |
| SLA Compliance | Percentage of SLAs met | Performance Analytics → Indicators |

### CMDB Metrics

| Metric | What It Measures | Where to Find |
|--------|-----------------|---------------|
| CMDB Completeness | Percentage of CIs with complete data | Performance Analytics → Indicators |
| CI Count | Total number of CIs | Performance Analytics → Indicators |

---

## Out-of-Box Dashboards

ServiceNow provides pre-built dashboards:

| Dashboard | What It Shows | Where to Find |
|-----------|---------------|---------------|
| Incident Overview | Incident volume, status, priority | Dashboards → Incident Overview |
| Change Overview | Change volume, risk, status | Dashboards → Change Overview |
| Problem Overview | Problem volume, root causes | Dashboards → Problem Overview |
| CMDB Overview | CI count, classes, relationships | Dashboards → CMDB Overview |

### How to View Dashboards

1. Go to **Dashboards → All**
2. Click a dashboard name to open it
3. Click **Edit** to customize it
4. Click **Configure** to change filters or time ranges

---

## How to Explore Out-of-Box Content

### Step 1: List What's Available

1. Go to **System Definition → Tables**
2. Filter by the application you're interested in
3. Note the table names

### Step 2: List Workflows

1. Go to **Workflow → All**
2. List all workflows
3. Read the description of each

### Step 3: List Reports & Dashboards

1. Go to **Reports → All**
2. List all reports
3. Go to **Dashboards → All**
4. List all dashboards

### Step 5: Test One

1. Pick one workflow, report, or dashboard
2. Run it
3. Understand what it does
4. Modify it slightly
5. Save your version

---

## What's NOT Out of the Box

Don't expect these to work immediately:

- **Custom integrations** with your specific systems
- **Custom workflows** for your unique processes
- **Custom dashboards** for your specific KPIs
- **Custom reports** for your specific data needs
- **Custom SLAs** for your specific business hours

These require configuration or development.

---

*Generated by Kilo on 2026-11-04.*
