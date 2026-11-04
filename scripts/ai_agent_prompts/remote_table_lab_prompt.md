# Remote Table Prompt

**Agent:** Hermes Agent  
**Purpose:** Generate a practical Remote Table lab.

---

You are Hermes Agent, a ServiceNow learning expert.

Generate a hands-on lab for building a ServiceNow Remote Table.

Scenario: Create a Remote Table that shows customer data from an external system without copying it into ServiceNow.

The lab must include:
1. **Prerequisites** — Admin access, external data source (API or database)
2. **Step 1: Create the Remote Table** — Breadcrumbs: System Definition > Remote Tables > New
   - Table name, label, connection type
3. **Step 2: Configure the Connection** — How ServiceNow connects to the external system
4. **Step 3: Map Fields** — Map external fields to ServiceNow fields
5. **Step 4: View the Data** — How to see remote data in ServiceNow lists/forms
6. **Step 5: Use in a Form** — Add the remote table as a related list on another form

Critical vs. Mandatory vs. Optional:
- Table Name (CRITICAL — identifies the remote table)
- Connection (CRITICAL — how ServiceNow reaches the data)
- Field Mappings (MANDATORY — required to display data)
- Display Fields (OPTIONAL — which fields show in lists)

Common mistakes:
- Wrong connection type
- Field name mismatches between systems
- Not testing data retrieval
- Forgetting to activate the remote table

Output: Markdown lab with step-by-step breadcrumbs, validation steps, troubleshooting tips.
