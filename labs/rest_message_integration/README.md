#!/usr/bin/env python3
"""
rest_message_lab.py — Practical REST Message Integration Lab Generator

Generates a complete hands-on lab for building a ServiceNow REST Message
integration that fetches external data and creates an Incident.

Agent: Hermes Agent
Date: 2026-11-04
"""

import json
import sys
from pathlib import Path


def generate_lab(output_path: str = None) -> str:
    """Generate the REST Message integration lab content."""

    lab = """# Lab: Practical REST Message Integration

**Agent:** Hermes Agent  
**Date:** 2026-11-04  
**Estimated Time:** 45-60 minutes  
**Level:** Beginner

---

## Learning Objective

By the end of this lab, you will be able to:
- Create a ServiceNow REST Message that calls an external API
- Build a REST Message Function to process the response
- Create a ServiceNow Incident using data from the API
- Handle errors when the external API is down or returns bad data

---

## Prerequisites

- Admin access to a ServiceNow instance
- An external API to call (we'll use a free public API for this lab)
- Basic understanding of what an Incident is in ServiceNow

---

## What We're Building

We'll build a REST Message integration that:

1. Calls a public API to get random user data
2. Takes the user's name and email from the response
3. Creates a new ServiceNow Incident with that information
4. Handles errors gracefully if the API is down

**ELI5:** Think of this like ServiceNow sending a letter to another computer, asking for information, and then creating a ticket based on the reply.

---

## Breadcrumb Map

Every step starts from the main ServiceNow navigation:

```
System Web Services > Outbound > REST Messages
```

---

## Step-by-Step Instructions

### Step 1: Create the REST Message

**Breadcrumb:** `System Web Services > Outbound > REST Messages > New`

1. In the left navigation, type "REST Messages" in the filter navigator
2. Click **REST Messages** under "Outbound"
3. Click **New**
4. Fill in the following fields:

| Field | Value | Classification | Why |
|-------|-------|---------------|-----|
| Name | "Get Random User" | CRITICAL | Identifies this REST Message |
| Endpoint | `https://randomuser.me/api/` | CRITICAL | The web address of the API |
| HTTP Method | GET | CRITICAL | We're retrieving data, not sending it |
| Authentication type | None | MANDATORY | This public API doesn't require auth |
| Active | true | MANDATORY | Must be active to work |

5. Click **Submit**

**Validation:** The REST Message record is saved and appears in the list.

---

### Step 2: Create the REST Message Function

**Breadcrumb:** `System Web Services > Outbound > REST Message Functions > New`

1. Navigate to `System Web Services > Outbound > REST Message Functions`
2. Click **New**
3. Fill in the following fields:

| Field | Value | Classification | Why |
|-------|-------|---------------|-----|
| Name | "Process Random User" | CRITICAL | Identifies this function |
| REST message | "Get Random User" | CRITICAL | Links to the message we created |
| Function type | Execute | MANDATORY | Tells ServiceNow to run this function |
| Active | true | MANDATORY | Must be active to work |

4. Click **Submit**
5. In the function form, scroll to the **Script** section
6. Replace the script with:

```javascript
(function process(/*RESTMessageResponse*/ response, /*RESTRequest*/ request) {
    try {
        var httpStatus = response.getStatusCode();
        var body = response.getBody();
        
        // ELI5: Parse the JSON response (like reading a letter)
        var jsonData = JSON.parse(body);
        var results = jsonData.results;
        var user = results[0];
        
        var userName = user.name.first + " " + user.name.last;
        var userEmail = user.email;
        var userCountry = user.location.country;
        
        gs.print("Retrieved user: " + userName + " (" + userEmail + ") from " + userCountry);
        
        // Return the data so other scripts can use it
        return {
            name: userName,
            email: userEmail,
            country: userCountry,
            status: "success"
        };
    } catch (ex) {
        gs.print("Error processing response: " + ex.message);
        return {
            status: "error",
            message: ex.message
        };
    }
})(request, response);
```

7. Click **Submit**

**Validation:** The function script is saved without syntax errors.

---

### Step 3: Test the Connection

**Breadcrumb:** `System Web Services > Outbound > REST Messages > Get Random User > Related Links > Test`

1. Open the "Get Random User" REST Message record
2. Click **Test** in the related links (or click the test button)
3. You should see a response with status code 200 and JSON data
4. If you see an error, check:
   - Is the Endpoint correct? (`https://randomuser.me/api/`)
   - Is the HTTP Method set to GET?
   - Is Active set to true?

**Validation:** You receive HTTP 200 with JSON data containing user information.

---

### Step 4: Create an Incident Using the API Data

**Breadcrumb:** `System Web Services > Outbound > REST Message Functions > Process Random User > Related > New`

Now we'll create a script that calls our REST Message function and creates an Incident with the data.

1. Navigate to `System Web Services > Outbound > REST Message Functions`
2. Open "Process Random User"
3. Click **New** on the **Script Includes** related list (or create a standalone script)
4. Use this script:

```javascript
var CreateIncidentFromAPI = Class.create();
CreateIncidentFromAPI.prototype = Object.extendsObject(AbstractAjaxProcessor, {
    createIncident: function() {
        try {
            // Call our REST Message function
            var sm = new sn_ws.RESTMessageV2("Get Random User", "process");
            sm.setHttpMethod("get");
            var response = sm.execute();
            
            var httpStatus = response.getStatusCode();
            if (httpStatus != 200) {
                return "Error: API returned status " + httpStatus;
            }
            
            var body = response.getBody();
            var jsonData = JSON.parse(body);
            var user = jsonData.results[0];
            
            // Create Incident with API data
            var incident = new GlideRecord("incident");
            incident.initialize();
            
            // CRITICAL fields for Incident
            incident.short_description = "New user from API: " + user.name.first + " " + user.name.last;
            incident.description = "User created automatically from REST Message integration.\nEmail: " + user.email + "\nCountry: " + user.location.country;
            incident.urgency = "3";
            incident.impact = "3";
            incident.priority = "3";
            incident.category = "inquiry";
            incident.subcategory = "general";
            
            // MANDATORY fields
            incident.caller_id = "admin";  // or a valid user
            
            var sysId = incident.insert();
            
            return "Incident created: " + incident.number + " (sys_id: " + sysId + ")";
        } catch (ex) {
            return "Error: " + ex.message;
        }
    },
    type: 'CreateIncidentFromAPI'
});
```

5. Save the script include
6. Open **Incident > Create New** and manually create one to verify the Incident form works

**Validation:** You can run the script include and see "Incident created: INC001XXXX" in the output.

---

### Step 5: Error Handling

**What can go wrong:**

| Problem | Symptom | Fix |
|---------|---------|-----|
| API is down | HTTP 500 or connection timeout | Check if `https://randomuser.me/api/` is accessible |
| Wrong endpoint | HTTP 404 | Verify the Endpoint URL in the REST Message |
| Wrong auth type | HTTP 401/403 | Set Authentication type to "None" for this public API |
| Invalid JSON | Script error | Verify the API returns valid JSON |
| Missing Incident fields | Incident won't save | Ensure short_description and caller_id are set |

**How to handle errors in your script:**
- Always check `httpStatus != 200` before processing
- Wrap JSON parsing in try/catch
- Log errors with `gs.print()` for debugging
- Return meaningful error messages to the caller

---

## Common Mistakes — Beginner Edition

| Mistake | What Happens | How to Avoid |
|---------|-------------|-------------|
| Forgetting HTTP Method | API call fails or returns wrong data | Always set GET/POST/PUT/DELETE explicitly |
| Wrong authentication | 401 Unauthorized errors | Use "None" for public APIs, Basic/Bearer for secured ones |
| Not setting Active = true | REST Message never runs | Check the Active checkbox on every record |
| Not handling empty responses | Script crashes when API returns no data | Check if results array has items before accessing [0] |
| Missing caller_id on Incident | Incident won't save | Always set caller_id when creating incidents via script |

---

## Validation Checklist

- [ ] REST Message "Get Random User" is created and Active
- [ ] REST Message Function "Process Random User" is created with script
- [ ] Test call returns HTTP 200 with JSON data
- [ ] Script can call the REST Message and parse the response
- [ ] Incident is created with data from the API
- [ ] Error handling works when API is unavailable

---

## Next Steps

After completing this lab, try:
1. **Modify the API** — Call a different public API (e.g., weather, quotes)
2. **Add authentication** — Use Basic auth with a secured API
3. **Create more records** — Create not just Incidents, but also Tasks or Change Requests
4. **Schedule it** — Use a Scheduled Job to call the API automatically every hour

---

## CRITICAL vs. MANDATORY vs. OPTIONAL — Summary

| Element | Classification | Why |
|---------|---------------|-----|
| REST Message Name | CRITICAL | Without it, you can't find or reference the message |
| Endpoint URL | CRITICAL | Without it, there's nowhere to send the request |
| HTTP Method | CRITICAL | Without it, ServiceNow doesn't know what kind of request to make |
| Authentication type | MANDATORY | Required field on the form |
| Active flag | MANDATORY | Inactive messages don't execute |
| Function script | MANDATORY | Without it, the function does nothing |
| Headers | OPTIONAL | Only needed for APIs requiring custom headers |
| MID Server | OPTIONAL | Only needed if the API is behind a firewall |
| Description | OPTIONAL | Helpful for documentation, not required |
