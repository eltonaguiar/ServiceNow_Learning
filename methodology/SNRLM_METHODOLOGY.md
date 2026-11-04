# ServiceNow Rapid Learning Methodology (SNRLM)

**Agent:** Hermes Agent
**Date:** 2026-11-04
**Version:** 1.0
**Purpose:** Speed up the time to learn anything from a ServiceNow module to a concept, generate infographics, and build practical labs at a very rapid pace.

---

## Overview

SNRLM is a repeatable, step-by-step system for learning any ServiceNow topic — from a single module to a complex integration — in the shortest time possible. It combines:

1. **Concept decomposition** — Break the topic into bite-sized pieces
2. **ELI5 translation** — Explain like you're 5 years old
3. **Breadcrumb mapping** — Find exactly where to click in the UI
4. **Critical vs. Optional vs. Mandatory** — Know what you MUST configure vs. what's nice-to-have
5. **Common mistakes** — Learn from others' errors before you make them
6. **Hands-on lab** — Build something real immediately
7. **Infographic generation** — Visual summary for memory retention

---

## The SNRLM 7-Step Cycle

### Step 1: Decompose the Topic
Take any ServiceNow module or concept and break it into:
- **What it is** (1 sentence)
- **What problem it solves** (1 sentence)
- **Where it lives** (navigation path in ServiceNow)
- **Who uses it** (role/persona)
- **Key components** (tables, forms, scripts, records)

### Step 2: ELI5 Translation
Rewrite the concept using simple analogies. No jargon without a plain-English explanation first.

### Step 3: Breadcrumb Mapping
Document the exact click path: `Menu > Module > Sub-module > Record > Related List > Field`

### Step 4: Classify Fields & Configuration
Every field gets one of three labels:
- **CRITICAL** — Without this, nothing works
- **MANDATORY** — Required by the system to save
- **OPTIONAL** — Nice to have, configure later

### Step 5: Common Mistakes
List the top 5 mistakes beginners make with this topic, plus how to avoid each.

### Step 6: Build a Practical Lab
Create a hands-on exercise that produces a working result (not just theory).

### Step 7: Generate Infographic
Create a one-page visual summary for quick reference and memory retention.

---

## ServiceNow Success Packs — Prerequisites

Success Packs are pre-built content packages (applications, workflows, dashboards) that accelerate adoption of specific ServiceNow capabilities.

### General Prerequisites (all Success Packs)
| Prerequisite | Why It Matters | Critical? |
|-------------|---------------|-----------|
| ServiceNow instance (any release) | You need a place to install | CRITICAL |
| Admin role or equivalent | Required to install applications | CRITICAL |
| Sufficient storage space | Success Packs can be large | MANDATORY |
| Network access to ServiceNow Store | To download the pack | CRITICAL |
| Signed ServiceNow license agreement | Required for some packs | MANDATORY |

### Common Success Pack Prerequisites by Type
| Success Pack Type | Additional Prerequisites | Critical? |
|------------------|-------------------------|-----------|
| ITSM Success Pack | Incident, Problem, Change management processes defined | CRITICAL |
| CSM Success Pack | Customer service processes and account structure | CRITICAL |
| HRSD Success Pack | HR case categories, employee documents | CRITICAL |
| SecOps Success Pack | Security incident response processes | CRITICAL |
| ITOM Success Pack | Discovery, Service Mapping, Event Management | CRITICAL |
| App Engine Studio | Low-code app development permissions | MANDATORY |

---

## Out-of-Box Features to Know

### Guided Setup
ServiceNow's Guided Setup walks administrators through initial configuration step-by-step.
- **Path:** `System Definition > Guided Setup > Define Guided Setup`
- **What it covers:** Company info, users, roles, basic IT service management
- **Critical:** Company name, time zone, default language

### Out-of-Box Workflows
Pre-built automated processes:
- **Incident Management:** Auto-assign, notify, resolve
- **Change Management:** Approval flows, risk assessment
- **Problem Management:** Root cause analysis
- **Request Management:** Service catalog ordering

### Integrations
| Integration Type | Common Use Case | Critical Fields |
|-----------------|----------------|-----------------|
| REST Message | Call external APIs | Endpoint, HTTP method, Authentication |
| SOAP Message | Legacy system integration | WSDL URL, Endpoint |
| MID Server | On-premise connectivity | Instance name, Version, Status |
| Flow Designer | Low-code automation | Trigger, Action, Condition |
| IntegrationHub | Spoke-based integration | Spoke name, Connection, Authentication |

### Playbooks
Pre-built response procedures for:
- Security incidents
- Major incidents
- IT service outages
- Change emergency procedures

### Metrics & Dashboards
| Metric Type | What It Measures | Where to Find |
|------------|-----------------|---------------|
| KPIs | Key performance indicators | `Metrics > KPI Definitions` |
| Indicators | Measurable values | `Metrics > Indicator Definitions` |
| Dashboards | Visual data summaries | `Dashboards > All` |
| Reports | Tabular/chart data | `Reports > All` |

---

## How to Use This Methodology

1. Pick a ServiceNow topic (module, concept, integration)
2. Run `python generators/generate_learning_path.py --topic "<your topic>"`
3. Follow the 7-step cycle using the generated output
4. Build the lab using `python generators/generate_lab.py --type <rest_message\|remote_table>`
5. Generate an infographic using `python generators/generate_infographic.py --topic "<your topic>"`

---

## File Structure

```
methodology/         — Core methodology documents
generators/          — Python scripts to auto-generate guides, labs, infographics
templates/           — Markdown templates for guides, labs, cheat sheets
labs/                — Practical hands-on labs (REST Message, Remote Table)
infographics/        — SVG/HTML visual summaries
```
