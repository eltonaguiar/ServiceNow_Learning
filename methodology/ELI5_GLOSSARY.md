# ServiceNow ELI5 Glossary

**Agent:** Hermes Agent  
**Date:** 2026-11-04  
**Purpose:** Plain-English explanations of ServiceNow terminology for absolute beginners.

---

## How to Use This Glossary

When you see a ServiceNow term you don't understand, look it up here. Each entry has:

- **The Term** — what ServiceNow calls it
- **ELI5** — explain-like-I'm-five version (analogy)
- **Real Example** — a concrete example you can relate to
- **Where to Find It** — navigation path in ServiceNow

---

## Core Concepts

### Instance
**ELI5:** Your very own copy of ServiceNow that lives on the internet. Like having your own private website that only your company can use.

**Real Example:** `https://mycompany.service-now.com` is your instance.

**Where to Find It:** Your browser address bar when you log in.

---

### Table
**ELI5:** A digital spreadsheet. Each row is one record (like one ticket), each column is one piece of information (like priority or description).

**Real Example:** The Incident table has rows for each IT ticket, columns for number, priority, state, etc.

**Where to Find It:** `System Definition > Tables`

---

### Record
**ELI5:** One row in the table. One ticket. One user. One computer.

**Real Example:** Incident INC0010001 is one record in the Incident table.

**Where to Find It:** Open any list view (e.g., `Incident > All`)

---

### Field
**ELI5:** One cell in the spreadsheet. One piece of data about a record.

**Real Example:** The "Priority" field on an incident record.

**Where to Find It:** Open any form, fields are the boxes you fill in.

---

### Form
**ELI5:** The screen where you view and edit one record. Like opening one row of the spreadsheet in a detailed view.

**Real Example:** Clicking on an incident number opens the incident form.

**Where to Find It:** Click any record in a list view.

---

### List
**ELI5:** A screen showing many records at once, like a spreadsheet view.

**Real Example:** `Incident > All` shows all incidents in a list.

**Where to Find It:** Module list views.

---

### Module
**ELI5:** A menu item in the left navigation. A doorway to a specific part of ServiceNow.

**Real Example:** "Incidents" is a module under "Incident Management".

**Where to Find It:** Left navigation menu (Application Navigator).

---

### Application
**ELI5:** A group of related modules that work together for one purpose. Like a folder containing related tools.

**Real Example:** Incident Management, Change Management, CMDB are all separate applications.

**Where to Find It:** `System Applications > All` or the left nav groups.

---

### Role
**ELI5:** A permission badge. It says what you're allowed to do in ServiceNow.

**Real Example:** The "admin" role can do everything. The "itil" role can see and edit incidents.

**Where to Find It:** `User Administration > Roles`

---

### User
**ELI5:** A person who logs into ServiceNow.

**Real Example:** "jsmith" is a user record.

**Where to Find It:** `User Administration > Users`

---

### Group
**ELI5:** A team of users. Used to assign work to the right team.

**Real Example:** "Network Team" group contains all network engineers.

**Where to Find It:** `User Administration > Groups`

---

## Integration Terms

### REST Message
**ELI5:** A way for ServiceNow to send a message to another computer over the internet, like sending a text message to another system and waiting for a reply.

**Real Example:** ServiceNow tells a monitoring tool "server X is down" via REST.

**Where to Find It:** `System Web Services > Outbound > REST Messages`

### REST Message Function
**ELI5:** A reusable script that sends a specific REST message. Like saving a text message template you can send again later.

**Real Example:** A function called "Create Ticket in Jira" that sends ticket data to Jira.

**Where to Find It:** `System Web Services > Outbound > REST Message Functions`

### Remote Table
**ELI5:** A table in ServiceNow that shows data from another system without copying it. Like looking through a window at data that lives somewhere else.

**Real Example:** A ServiceNow table showing customer data that actually lives in Salesforce.

**Where to Find It:** `System Definition > Remote Tables`

### MID Server
**ELI5:** A small program installed in your office that acts as a bridge between ServiceNow (in the cloud) and your local computers/servers.

**Real Example:** ServiceNow uses MID Server to scan computers inside your office network.

**Where to Find It:** `MID Server > Servers`

### IntegrationHub
**ELI5:** ServiceNow's app store for connections to other systems. Pre-built "spokes" (connectors) for popular tools.

**Real Example:** The ServiceNow-Salesforce spoke lets you sync data between them without writing code.

**Where to Find It:** `IntegrationHub > Spokes`

---

## Automation Terms

### Flow Designer
**ELI5:** A visual tool to build automation by dragging and connecting blocks. Like building with LEGO blocks instead of writing code.

**Real Example:** "When an incident is created, send an email to the manager."

**Where to Find It:** `Flow Designer > All`

### Flow
**ELI5:** One automation recipe built in Flow Designer.

**Real Example:** "Auto-assign High Priority Incidents" flow.

**Where to Find It:** `Flow Designer > Flows`

### Action
**ELI5:** One step in a flow. Like "Send Email" or "Create Record."

**Real Example:** The "Send Notification" action sends an email.

**Where to Find It:** `Flow Designer > Actions`

### Subflow
**ELI5:** A mini-flow that can be reused inside other flows. Like a function in programming.

**Real Example:** "Validate Email Address" subflow used by 10 different flows.

**Where to Find It:** `Flow Designer > Subflows`

---

## Metrics & Reporting Terms

### KPI (Key Performance Indicator)
**ELI5:** A number that tells you if something important is going well or badly.

**Real Example:** "Average time to resolve incidents" is a KPI.

**Where to Find It:** `Metrics > KPI Definitions`

### Indicator
**ELI5:** A measurable value that feeds into KPIs.

**Real Example:** "Number of incidents resolved today" is an indicator.

**Where to Find It:** `Metrics > Indicator Definitions`

### Dashboard
**ELI5:** A screen with charts and numbers showing how things are going. Like a car's dashboard.

**Real Example:** "IT Operations Dashboard" shows open incidents, avg resolution time, etc.

**Where to Find It:** `Dashboards > All`

### Report
**ELI5:** A chart or table showing data. One piece of a dashboard.

**Real Example:** "Incidents by Priority" bar chart.

**Where to Find It:** `Reports > All`

---

## Administration Terms

### Update Set
**ELI5:** A package of changes you've made, ready to move to another instance (like from test to production).

**Real Example:** You create a new field in test, put it in an update set, then move it to production.

**Where to Find It:** `System Update Sets > Update Sets`

### Dictionary Entry
**ELI5:** The definition of a field. Says what type of data it holds (text, number, date, etc.).

**Real Example:** The "Priority" dictionary entry says it's a choice field with values 1-5.

**Where to Find It:** `System Definition > Dictionary`

### Business Rule
**ELI5:** A behind-the-scenes script that runs automatically when something happens.

**Real Example:** "When an incident is resolved, set the resolved by field to current user."

**Where to Find It:** `System Definition > Business Rules`

### Client Script
**ELI5:** A script that runs in the user's browser when they interact with a form.

**Real Example:** "When the user changes the priority to 1, show a warning message."

**Where to Find It:** `System Definition > Client Scripts`

### UI Policy
**ELI5:** A rule that shows, hides, or makes fields required based on conditions. No coding required.

**Real Example:** "If category is Hardware, make the 'Asset' field required."

**Where to Find It:** `System Definition > UI Policies`

### Data Policy
**ELI5:** Like a UI Policy but also works when data comes in via import or API, not just forms.

**Real Example:** "Always require the 'Description' field, even when importing via CSV."

**Where to Find It:** `System Definition > Data Policies`

---

## Success Pack Terms

### Success Pack
**ELI5:** A pre-built box of ServiceNow content for a specific purpose. Install it and you get ready-to-use tables, forms, workflows, and dashboards.

**Real Example:** "ITSM Success Pack" gives you Incident, Problem, and Change management out of the box.

**Where to Find It:** ServiceNow Store (`System Applications > All > Store`)

### Prerequisite
**ELI5:** Something you must have or do before you can install or use a Success Pack.

**Real Example:** You need the ITSM application installed before installing the ITSM Success Pack.

**Where to Find It:** The Success Pack's documentation page in the Store.

---

## Common Mistakes — Beginner Edition

| Mistake | What Happens | How to Avoid |
|---------|-------------|--------------|
| Forgetting to set the Active field to true | Record won't appear in lists | Always check "Active" when creating records |
| Not assigning a group to a record | Work never gets assigned | Always set the "Assignment group" field |
| Using the wrong field type | Data won't save or display correctly | Check the dictionary entry before creating fields |
| Forgetting to publish a flow | Automation never runs | Click "Publish" after building a flow |
| Not testing in a sub-production instance first | Breaks production for everyone | Always test in dev/test before production |
