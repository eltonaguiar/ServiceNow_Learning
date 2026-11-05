# Lab Setup: Remote Table

**Time:** 5-10 minutes  

---

## 1. Create Update Set
**Breadcrumb:** System Update Sets → Local Update Sets → New

- Name: `Lab_Remote_Table`
- Description: `Learning lab for Remote Table configuration`
- Set as Current

---

## 2. Choose Data Source
We'll use JSONPlaceholder again - it returns an array of users.

Endpoint: `https://jsonplaceholder.typicode.com/users`

This returns JSON array like:
```json
[
  {"id": 1, "name": "...", "email": "...", ...},
  {"id": 2, "name": "...", "email": "...", ...}
]
```

Perfect for a Remote Table showing multiple records.

---

## 3. Notes
- Remote Tables need a Data Source configured
- The external API must return data in a format ServiceNow can consume
- For learning with public APIs, authentication is usually not needed
- Some instances may need MID Server depending on network restrictions

---

## Ready
Proceed to `lab-steps.md`
