# ServiceNow Remote Table Lab

**Lab:** ServiceNow Developer / Technical Consultant  
**Module:** Integration / Data Access  
**Target Role:** ServiceNow Developer  
**Difficulty:** Intermediate  
**Estimated Time:** 45 minutes  
**Source:** https://github.com/eltonaguiar/ServiceNow_Learning  
**Agent:** Kilo  
**Date:** 2026-11-04  

---

## Lab Overview

**Goal:** Create a ServiceNow Remote Table that connects to an external data source and displays the data in ServiceNow without copying it.

**What You'll Learn:**
- What a Remote Table is and when to use it
- How to create a Remote Table in ServiceNow
- How to configure the external data source connection
- How to view remote table data in ServiceNow
- When to use Remote Table vs Import Set vs Integration

**Prerequisites:**
- ServiceNow developer instance access
- `web_service_admin` role (or `admin`)
- Access to an external data source (or use a public API as a simulation)

---

## Lab Setup

### Step 1: Verify Access

1. Log into your ServiceNow instance
2. Navigate to **System Definition → Remote Tables**
3. Verify you can see the list (if not, you need the `web_service_admin` role)
4. Log out and back in after adding any roles

### Step 2: Create an Update Set

1. Go to **System Update Sets → Local Update Sets**
2. Click **New**
3. Name: `Remote Table Lab - [Your Name]`
4. State: `In Progress`
5. Click **Submit**
6. Click **Make Current**

---

## Lab Steps

### Step 1: Create the Remote Table

1. Go to **System Definition → Remote Tables**
2. Click **New**
3. Fill in:
   - **Name:** `External Employee Data`
   - **Table Name:** `u_external_employee`
   - **Application:** `Global`
   - **Description:** `Remote table connecting to external HR data source`
4. Click **Submit**

### Step 2: Configure Remote Table Fields

1. Open the Remote Table record you just created
2. Scroll to the **Remote Table Fields** related list
3. Click **New**
4. Add fields that match your external data source:
   - Field Name: `employee_id`, Type: `string`, Max Length: 50
   - Field Name: `first_name`, Type: `string`, Max Length: 100
   - Field Name: `last_name`, Type: `string`, Max Length: 100
   - Field Name: `email`, Type: `string`, Max Length: 255
   - Field Name: `department`, Type: `string`, Max Length: 100
5. Click **Submit** after each field

### Step 3: Configure the Data Source

1. Go to **System Definition → Remote Tables → Data Sources**
2. Click **New**
3. Fill in:
   - **Name:** `External HR System`
   - **Type:** `REST` (or `JDBC` if you have a database)
   - **URL:** `https://your-external-api.com/employees` (replace with actual endpoint)
   - **Authentication:** `None` (or Basic Auth if required)
4. Click **Submit**

### Step 4: Link Data Source to Remote Table

1. Go back to your Remote Table record
2. In the **Data Source** field, select the data source you just created
3. Click **Update**

### Step 5: Test the Remote Table

1. Go to **System Definition → Remote Tables**
2. Open your `External Employee Data` record
3. Click **Refresh** (if available) or **Test Connection**
4. Navigate to the remote table list view:
   - Go to **System Definition → Tables**
   - Search for `u_external_employee`
   - Click the table name
   - Click **Show All** or view the list

---

## Lab Validation

- [ ] Remote Table record created with correct table name
- [ ] Remote Table Fields created matching external data structure
- [ ] Data Source configured with correct endpoint
- [ ] Remote Table linked to Data Source
- [ ] Remote table list view displays data (or shows connection status)
- [ ] No errors in System Log

---

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Wrong endpoint URL | Connection timeout | Verify the URL is accessible from your ServiceNow instance |
| Missing authentication | 401 Unauthorized | Add authentication credentials to the data source |
| Wrong field names | Data doesn't map | Ensure field names match the external data source exactly |
| No `web_service_admin` role | Can't see Remote Table menu | Add role to your user and log out/in |

---

## Critical Fields

| Field | Why It's Critical |
|-------|-------------------|
| Remote Table Name | Identifies the table in ServiceNow |
| Table Name | The actual table name in the database (`u_` prefix) |
| Data Source | Where the data comes from |
| Field Names | Must match the external data source exactly |

---

## Related Lists

| Related List | What It Shows | Why It Matters |
|--------------|---------------|----------------|
| Remote Table Fields | Fields mapped from external source | Defines what data is visible |
| Data Source | The connection configuration | Determines where data comes from |
| Error Log | Failed connection attempts | Debug connection issues |

---

## Remote Table vs Import Set vs Integration

| Feature | Remote Table | Import Set | Integration |
|---------|-------------|------------|-------------|
| Data Location | Stays external | Imported into ServiceNow | Stays external or pushed |
| Real-time | Yes (live) | No (snapshot) | Can be real-time |
| Write Support | Read-only typically | Write to ServiceNow | Can write both ways |
| Setup Complexity | Medium | Low | High |
| Best For | Live external data | One-time migration | Ongoing integration |

---

## Next Steps

1. Connect to a real external data source (your company's HR system, CRM, etc.)
2. Create a UI Page or UI Action that displays remote table data
3. Build a Flow Designer flow that triggers on remote table data changes
4. Create a report on remote table data
5. Set up ACLs to control who can see the remote table data

---

*Generated by Kilo on 2026-11-04. Part of the ServiceNow_Learning repository at github.com/eltonaguiar/ServiceNow_Learning.*
