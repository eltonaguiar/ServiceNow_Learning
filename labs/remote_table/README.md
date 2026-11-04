#!/usr/bin/env python3
"""
remote_table_lab.py — Practical Remote Table Lab Generator

Generates a complete hands-on lab for building a ServiceNow Remote Table
that displays external data without copying it into ServiceNow.

Agent: Hermes Agent
Date: 2026-11-04
"""

import json
import sys
from pathlib import Path


def generate_lab(output_path: str = None) -> str:
    """Generate the Remote Table lab content."""

    lab = """# Lab: Practical Remote Table

**Agent:** Hermes Agent  
**Date:** 2026-11-04  
**Estimated Time:** 45-60 minutes  
**Level:** Beginner

---

## Learning Objective

By the end of this lab, you will be able to:
- Create a ServiceNow Remote Table that displays external data
- Configure a connection to an external data source
- Map external fields to ServiceNow fields
- View remote data in ServiceNow lists and forms
- Add the remote table as a related list on another form

---

## Prerequisites

- Admin access to a ServiceNow instance
- An external data source (we'll use a public REST API for this lab)
- Basic understanding of ServiceNow tables and forms

---

## What We're Building

We'll build a Remote Table that:

1. Connects to a public API (randomuser.me)
2. Displays user data in a ServiceNow list view
3. Shows the data on an Incident form as a related list
4. Updates when you refresh (data stays external, not copied)

**ELI5:** Think of a Remote Table like looking through a window at data that lives in another building. You can see it in ServiceNow, but it's not actually stored in ServiceNow — it lives somewhere else.

---

## Breadcrumb Map

```
System Definition > Remote Tables > New
```

---

## Step-by-Step Instructions

### Step 1: Create the Remote Table

**Breadcrumb:** `System Definition > Remote Tables > New`

1. In the left navigation, type "Remote Tables" in the filter navigator
2. Click **Remote Tables** under "System Definition"
3. Click **New**
4. Fill in the following fields:

| Field | Value | Classification | Why |
|-------|-------|---------------|-----|
| Name | "x_usr_random_user" | CRITICAL | Unique identifier for the remote table |
| Label | "Random User" | CRITICAL | Human-friendly name shown in UI |
| Table | "x_usr_random_user" | CRITICAL | The actual table name (auto-filled from Name) |
| Connection type | REST | CRITICAL | How ServiceNow connects to external data |
| Active | true | MANDATORY | Must be active to display data |

5. Click **Submit**

**Validation:** The Remote Table record is saved and appears in the list.

---

### Step 2: Configure the Connection

1. Open the "Random User" Remote Table record you just created
2. Scroll to the **Connection** related list
3. Click **New**
4. Fill in the following fields:

| Field | Value | Classification | Why |
|-------|-------|---------------|-----|
| Name | "Random User API" | CRITICAL | Identifies this connection |
| URL | `https://randomuser.me/api/?results=10` | CRITICAL | The API endpoint (returns 10 users) |
| HTTP Method | GET | CRITICAL | Retrieving data |
| Authentication type | None | MANDATORY | Public API doesn't need auth |
| Active | true | MANDATORY | Connection must be active |

5. Click **Submit**

**Validation:** The connection record is saved and linked to the Remote Table.

---

### Step 3: Map Fields

1. Still on the "Random User" Remote Table record
2. Scroll to the **Field Maps** related list
3. Click **New** for each field you want to display:

| External Field | ServiceNow Field | Classification | Why |
|---------------|-----------------|---------------|-----|
| results[].name.first | first_name | MANDATORY | User's first name |
| results[].name.last | last_name | MANDATORY | User's last name |
| results[].email | email | MANDATORY | User's email address |
| results[].location.country | country | OPTIONAL | User's country (nice to have) |
| results[].phone | phone | OPTIONAL | User's phone number |

**To create each field map:**
1. Click **New** on the Field Maps related list
2. Select the Remote Table field (or create it first)
3. Map to the external JSON path
4. Click **Submit**

**Note:** You may need to create the ServiceNow fields first:
- Navigate to `System Definition > Dictionary > New`
- Create fields on your remote table with appropriate types (string, etc.)

---

### Step 4: View the Data

1. Open the "Random User" Remote Table record
2. Click **View Records** or navigate to the table directly:
   - Breadcrumb: `Random User > All` (or search for your table name)
3. You should see a list of users from the API
4. Click on a user to see the form view

**Validation:** The list shows user data from the external API, not from ServiceNow's database.

---

### Step 5: Add Remote Table as Related List on Incident Form

1. Navigate to `Incident > Administration > Form Layout` (or open any Incident form)
2. Click **Configure > Related Lists** (or use Form Designer)
3. Add "Random User" to the related lists
4. Save the form layout
5. Open an Incident record
6. Scroll to the bottom — you should see the "Random User" related list

**Validation:** The Incident form shows remote user data as a related list.

---

## CRITICAL vs. MANDATORY vs. OPTIONAL — Summary

| Element | Classification | Why |
|---------|---------------|-----|
| Remote Table Name | CRITICAL | Unique identifier — can't be changed after creation |
| Label | CRITICAL | What users see in the UI |
| Connection Type | CRITICAL | Determines how ServiceNow connects to external data |
| Connection URL | CRITICAL | Where the external data lives |
| Active flag | MANDATORY | Inactive tables show no data |
| Field Mappings | MANDATORY | Without mappings, there's nothing to display |
| Display Fields | OPTIONAL | Which fields appear in list views |
| Description | OPTIONAL | Helpful for documentation |
| Related List on Incident | OPTIONAL | Convenience, not required for the table to work |

---

## Common Mistakes — Beginner Edition

| Mistake | What Happens | How to Avoid |
|---------|-------------|-------------|
| Wrong connection type | Can't connect to the data source | Choose REST for APIs, JDBC for databases |
| Field name mismatches | Data doesn't appear in ServiceNow | Match external JSON paths exactly to ServiceNow fields |
| Not testing data retrieval | Empty list, no error message | Use the "Test" button on the connection |
| Forgetting to activate | Table exists but shows nothing | Set Active = true on both table and connection |
| Creating fields on wrong table | Fields don't appear in remote table | Create dictionary entries ON the remote table, not Incident |

---

## Validation Checklist

- [ ] Remote Table "Random User" is created and Active
- [ ] Connection "Random User API" is configured and Active
- [ ] Field Maps are created for at least 3 fields
- [ ] List view shows user data from the external API
- [ ] Form view shows details for individual users
- [ ] Remote Table appears as related list on Incident form

---

## Key Breadcrumbs — Where to Find Things

| What You Need | Navigation Path |
|--------------|-----------------|
| Remote Tables list | `System Definition > Remote Tables` |
| Create new Remote Table | `System Definition > Remote Tables > New` |
| Connection settings | Open Remote Table record > Connection related list |
| Field mappings | Open Remote Table record > Field Maps related list |
| View remote data | `<Your Table Name> > All` |
| Form layout (related lists) | `Incident > Administration > Form Layout` |
| Dictionary (create fields) | `System Definition > Dictionary` |

---

## Next Steps

After completing this lab, try:
1. **Connect to a different API** — Weather data, currency exchange rates, etc.
2. **Add write capability** — Some remote tables allow creating records in the external system
3. **Schedule data refresh** — Use a Scheduled Job to refresh the remote data
4. **Build a dashboard** — Create a dashboard showing remote table metrics
