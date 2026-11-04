# ServiceNow Out-of-Box Features Reference

**Agent:** Hermes Agent  
**Date:** 2026-11-04  
**Purpose:** Document guided setup, workflows, integrations, playbooks, metrics, and dashboards available out of the box in ServiceNow.

---

## Guided Setup

ServiceNow's Guided Setup helps administrators configure their instance step-by-step.

### Where to Find It
`System Definition > Guided Setup > Define Guided Setup`

### What It Covers
| Setup Area | What You Configure | Critical? |
|-----------|-------------------|-----------|
| Company information | Company name, logo, address | CRITICAL |
| Users and roles | Admin users, basic roles | CRITICAL |
| Time zone and language | Default time zone, language | MANDATORY |
| IT service management | Incident, problem, change basics | MANDATORY |
| CMDB | Basic configuration items | OPTIONAL |

### Beginner Tip
Always run Guided Setup on a fresh instance before doing anything else. It sets the foundation.

---

## Out-of-Box Workflows

Pre-built automated processes included with ServiceNow.

### Incident Management Workflows
| Workflow | What It Does | Where to Find |
|----------|-------------|---------------|
| Incident Auto-Assignment | Assigns incidents to groups based on category | `System Policy > Workflow > Workflows` |
| Incident Notification | Notifies assignees when incident is assigned | `System Policy > Workflow > Workflows` |
| Incident Escalation | Escalates overdue incidents to managers | `System Policy > Workflow > Workflows` |
| Incident Resolution | Closes incident and notifies caller | `System Policy > Workflow > Workflows` |

### Change Management Workflows
| Workflow | What It Does | Where to Find |
|----------|-------------|---------------|
| Change Approval | Routes change requests for approval | `System Policy > Workflow > Workflows` |
| Change Risk Assessment | Calculates risk based on impact/urgency | `System Policy > Workflow > Workflows` |
| Change Implementation | Coordinates change execution tasks | `System Policy > Workflow > Workflows` |

### Request Management Workflows
| Workflow | What It Does | Where to Find |
|----------|-------------|---------------|
| Catalog Item Fulfillment | Processes service catalog orders | `System Policy > Workflow > Workflows` |
| Approval Routing | Sends requests to appropriate approvers | `System Policy > Workflow > Workflows` |

---

## Integrations (Out-of-Box)

### REST Messages
| Integration | Use Case | Critical Fields |
|------------|----------|-----------------|
| Generic REST Call | Call any REST API | Endpoint, HTTP Method, Authentication |
| Webhook Receiver | Receive webhooks from external systems | URL, HTTP Method |

### SOAP Messages
| Integration | Use Case | Critical Fields |
|------------|----------|-----------------|
| Generic SOAP Call | Call legacy SOAP services | WSDL URL, Endpoint, Namespace |

### MID Server
| Type | Use Case | Where to Find |
|------|----------|---------------|
| Discovery | Find devices on your network | `MID Server > Servers` |
| Service Mapping | Map service dependencies | `MID Server > Servers` |
| Event Management | Receive events from monitoring tools | `MID Server > Servers` |

### Flow Designer (Low-Code Integration)
| Action | Use Case |
|--------|----------|
| Send Email | Send notifications |
| Create Record | Create records in any table |
| Update Record | Update existing records |
| Call Subflow | Reuse another flow |
| Wait for Condition | Pause until something happens |

### IntegrationHub Spokes
Common pre-built connectors:
- ServiceNow ↔ Salesforce
- ServiceNow ↔ Jira
- ServiceNow ↔ Slack
- ServiceNow ↔ Microsoft Teams
- ServiceNow ↔ Email
- ServiceNow ↔ Service Catalog

---

## Playbooks

Pre-built response procedures.

| Playbook | Use Case | Where to Find |
|----------|----------|---------------|
| Security Incident Response | Respond to security breaches | `SecOps > Playbooks` |
| Major Incident Response | Handle major IT outages | `Incident > Playbooks` |
| Change Emergency Process | Fast-track emergency changes | `Change > Playbooks` |
| Problem Investigation | Investigate recurring issues | `Problem > Playbooks` |

---

## Metrics

### KPIs (Key Performance Indicators)
| KPI | What It Measures | Where to Find |
|-----|-----------------|---------------|
| Mean Time to Resolve (MTTR) | Average time to close incidents | `Metrics > KPI Definitions` |
| First Contact Resolution Rate | % of incidents resolved on first contact | `Metrics > KPI Definitions` |
| Change Success Rate | % of changes implemented without issues | `Metrics > KPI Definitions` |
| Customer Satisfaction (CSAT) | How happy customers are with service | `Metrics > KPI Definitions` |

### Indicators
| Indicator | What It Measures | Where to Find |
|-----------|-----------------|---------------|
| Incident Count | Number of incidents created | `Metrics > Indicator Definitions` |
| Incident Duration | How long incidents stay open | `Metrics > Indicator Definitions` |
| Change Volume | Number of changes requested | `Metrics > Indicator Definitions` |

### Where to Configure Metrics
- **KPI Definitions:** `Metrics > KPI Definitions`
- **Indicator Definitions:** `Metrics > Indicator Definitions`
- **Metric Definitions:** `Metrics > Metric Definitions`

---

## Dashboards

### Out-of-Box Dashboards
| Dashboard | What It Shows | Where to Find |
|-----------|--------------|---------------|
| Incident Dashboard | Open incidents, by priority, by assignment group | `Dashboards > All` |
| Change Dashboard | Changes in progress, upcoming changes | `Dashboards > All` |
| Problem Dashboard | Open problems, root causes | `Dashboards > All` |
| Service Dashboard | Service health, SLA compliance | `Dashboards > All` |
| Performance Analytics Dashboard | KPI trends over time | `Dashboards > All` |

### Creating a Custom Dashboard
1. Navigate to `Dashboards > All`
2. Click "New"
3. Give it a name and description
4. Add indicators/reports as dashboard elements
5. Configure layout (columns, rows)
6. Save and publish

---

## Common Mistakes — Out-of-Box Features

| Feature | Mistake | Consequence | Fix |
|---------|---------|-------------|-----|
| Guided Setup | Skipping it on a new instance | Missing foundational config | Always run Guided Setup first |
| Workflows | Not publishing after editing | Changes don't take effect | Click "Publish" in workflow editor |
| REST Messages | Wrong authentication | 401/403 errors | Check authentication type and credentials |
| MID Server | Wrong version | Connection failures | Match MID Server version to instance |
| Dashboards | Not sharing with users | Users can't see data | Set sharing to "All" or specific groups |
| Playbooks | Not assigning playbook owner | Playbook never triggers | Assign an owner in playbook settings |
