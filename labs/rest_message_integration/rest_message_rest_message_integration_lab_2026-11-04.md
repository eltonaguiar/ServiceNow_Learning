# Lab: REST Message Integration — REST Message Integration

**Agent:** Hermes Agent  
**Date:** 2026-11-04  
**Topic:** REST Message Integration  
**Type:** REST Message Integration

---

## Prerequisites

- Admin access to a ServiceNow instance
- External API endpoint

---

## Steps

### Step 1: Create the REST Message
**Breadcrumb:** `System Web Services > Outbound > REST Messages > New`

| Field | Value | Classification |
|-------|-------|---------------|
| Name | Descriptive name | CRITICAL |
| Endpoint | API URL | CRITICAL |
| HTTP Method | GET/POST/PUT/DELETE | CRITICAL |
| Authentication type | None/Basic/Bearer | MANDATORY |
| Active | true | MANDATORY |

### Step 2: Create the REST Message Function
**Breadcrumb:** `System Web Services > Outbound > REST Message Functions > New`

### Step 3: Test the Connection
Use the Test button on the REST Message record.

### Step 4: Process the Response
Parse JSON, extract fields, use in ServiceNow.

### Step 5: Error Handling
Check HTTP status, wrap JSON parsing in try/catch.

---

## Validation Checklist

- [ ] REST Message created and Active
- [ ] Test returns HTTP 200
- [ ] Response data is parsed correctly
- [ ] Error handling works

