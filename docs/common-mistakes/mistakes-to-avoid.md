# Common Mistakes to Avoid

**Agent:** Kilo  
**Date:** 2026-11-04  

---

## Purpose

A collection of the most common mistakes beginners make when learning ServiceNow, and how to avoid or fix them.

---

## Configuration Mistakes

### 1. Forgetting to Log Out After Role Changes

**Mistake:** You add a role to your user record but don't log out and back in. The new role doesn't take effect.

**Fix:** Always log out and log back in after adding a role.

**Prevention:** Always log out and back in after adding a role.

---

### 2. Editing Directly on Production

**Mistake:** Making changes directly on a production instance without testing first.

**Fix:** Always develop and test on a developer or test instance first. Use Update Sets to move changes to production.

**Prevention:** Never work on production. Period.

---

### 3. Not Understanding Update Sets

**Mistake:** Making changes without an active Update Set, or forgetting which Update Set your changes are going into.

**Fix:** Always create an Update Set before making changes. Mark it as "Current." Verify your changes are going into it.

**Prevention:** Create the Update Set first, then do the work.

---

### 4. Modifying Out-of-Box Records Directly

**Mistake:** Editing out-of-box records (like out-of-box business rules, UI policies, or scripts) directly.

**Fix:** Clone or copy the out-of-box record, then modify the copy. Leave the original intact.

**Prevention:** Never edit an out-of-box record. Always clone first.

---

### 5. Creating Duplicate Fields

**Mistake:** Creating a new field on a table when a similar field already exists (e.g., creating `u_my_priority` when `priority` already exists).

**Fix:** Search existing fields before creating new ones. Use existing fields when possible.

**Prevention:** Search System Definition → Fields before creating new fields.

---

### 6. Not Using Table Scope

**Mistake:** Creating records or scripts in the wrong application scope, causing them to be invisible or inaccessible.

**Fix:** Check the Application Scope dropdown when creating records. Know which scope you're working in.

**Prevention:** Always verify scope before creating anything.

---

## Scripting Mistakes

### 7. Not Using `current` Object in Business Rules

**Mistake:** Trying to access field values without using the `current` object in a Business Rule.

**Fix:** Always use `current.field_name` to access field values in Business Rules.

**Prevention:** Remember: `current` = the record being saved/deleted.

---

### 8. Forgetting `current.update()` in Business Rules

**Mistake:** Changing a field value in a Business Rule but not calling `current.update()`, so the change doesn't persist.

**Fix:** Always call `current.update()` after modifying field values in a Business Rule (unless it's a before insert/update that modifies the same record).

**Prevention:** Remember: changes to `current` don't save automatically in all contexts.

---

### 9. Hardcoding sys_ids

**Mistake:** Hardcoding `sys_id` values in scripts instead of querying by name or other stable field.

**Fix:** Query by name or other stable field, then get the `sys_id` dynamically.

**Prevention:** Never hardcode `sys_id`. Query by name instead.

---

### 10. Infinite Loops in Business Rules

**Mistake:** A Business Rule that updates a field, which triggers itself again, creating an infinite loop.

**Fix:** Use `previous.value` to check if the field actually changed before taking action. Or set `current.setWorkflow(false)` to prevent recursive triggers.

**Prevention:** Always check `previous.value` before updating in a Business Rule.

---

## Integration Mistakes

### 11. Not Testing REST Messages with a Real Endpoint

**Mistake:** Configuring a REST Message but never testing it against a real endpoint.

**Fix:** Always test against a real endpoint (even a public one like `https://jsonplaceholder.typicode.com/posts`) before relying on it.

**Prevention:** Test every REST Message before depending on it.

---

### 12. Not Handling API Errors

**Mistake:** Assuming every REST call succeeds. Not checking response status codes or error bodies.

**Fix:** Always check the response status code and handle errors gracefully.

**Prevention:** Write error handling before writing success logic.

---

### 13. Not Setting MID Server Correctly

**Mistake:** Configuring a MID Server but not assigning it to the MID Server list, or not activating it.

**Fix:** Ensure the MID Server record is Active and assigned to the correct MID Server list.

**Prevention:** Verify MID Server status before testing integrations.

---

## Data Mistakes

### 14. Creating Duplicate Records

**Mistake:** Creating multiple records with the same data because you didn't check if one already existed.

**Fix:** Query for existing records before creating new ones.

**Prevention:** Always search before creating.

---

### 15. Not Understanding sys_id vs Display Value

**Mistake:** Confusing `sys_id` (internal ID) with `display_value` (what the user sees), especially in reference fields.

**Fix:** Remember: `field_name` returns the display value, `field_name.sys_id` returns the internal ID.

**Prevention:** Know the difference. Test both.

---

## Reporting Mistakes

### 16. Creating Reports Without Filters

**Mistake:** Creating reports that show ALL records instead of filtering to relevant ones.

**Fix:** Always add conditions/filters to your reports.

**Prevention:** Always add at least one condition to every report.

---

### 17. Not Sharing Reports/Dashboards

**Mistake:** Creating reports that only you can see.

**Fix:** Share reports with the appropriate groups or make them public (if appropriate).

**Prevention:** Always set sharing permissions when creating reports.

---

## General Mistakes

### 18. Not Reading Error Messages

**Mistake:** Ignoring error messages or not reading them carefully.

**Fix:** Always read the full error message. It usually tells you exactly what's wrong.

**Prevention:** Read errors completely before troubleshooting.

---

### 19. Not Documenting Changes

**Mistake:** Making changes without documenting what you did and why.

**Fix:** Document every change: what, why, when, and who.

**Prevention:** Keep a change log for every instance you work on.

---

### 20. Giving Up Too Soon

**Mistake:** Getting frustrated when something doesn't work immediately and giving up.

**Fix:** ServiceNow has a learning curve. Use the documentation, check the community, and try again.

**Prevention:** Take breaks. Ask for help. Remember that everyone started as a beginner.

---

## Quick Troubleshooting Checklist

- [ ] Did I log out and back in after adding a role?
- [ ] Am I in the correct Application Scope?
- [ ] Is my Update Set active?
- [ ] Did I check the System Log for errors?
- [ ] Did I query by name instead of hardcoding sys_id?
- [ ] Did I check `previous.value` in Business Rules?
- [ ] Did I test with a user who has the correct role?
- [ ] Did I create an Update Set before making changes?

---

*Generated by Kilo on 2026-11-04.*
