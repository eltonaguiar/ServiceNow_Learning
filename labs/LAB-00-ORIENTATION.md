# LAB 00 — Orientation (30 minutes, nothing to break)

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

**Goal:** leave with the mental model, not with a working configuration.
**Instance:** your PDI (<https://developer.servicenow.com/dev.do>) or any dev instance.
**Risk of breaking something:** none — you create nothing in this lab.

---

## Prerequisites

- [ ] You can log in
- [ ] You know your instance URL (`https://<name>.service-now.com`)
- [ ] You have (or can request) admin on the PDI. If not, the labs still work read-only

---

## Exercise 1 — Find things the way people who are fast find them (5 min)

Type each of these into the **filter navigator** (top-left, or the **All** menu) and press
Enter. Write down the table name each one lands on (you will need it later):

| Type this | Land on | Table |
|---|---|---|
| `incident` | Incident list | `incident` |
| `tables` | Tables & Columns | `sys_db_object` |
| `application menus` | Application Menus | `sys_app_module` |
| `users` | Users | `sys_user` |
| `guided setup` | Whatever this release ships | varies |

**Why:** the filter navigator searches module names, which are records — so it never lies
to you about where something lives.

---

## Exercise 2 — Read a form like a developer (5 min)

1. Open any incident.
2. **Right-click the form header → Configure → Form Layout.** Look at the two columns
   (Selected / Available). Notice that fields are chosen, not hardcoded. **Cancel.**
3. Scroll to the bottom. Those are **related lists** — each is another table filtered to
   this record. Note three of them.
4. Click a value in the **Caller** field — it opens the user record. That is a **reference
   field**; the incident stores a `sys_id`, not a name.

**Checkpoint:** explain out loud, in one sentence each, the difference between a *field*, a
*reference field*, and a *related list*.

---

## Exercise 3 — The map behind the screen (7 min)

1. `All > System Definition > Tables & Columns`. Search `incident`.
2. Open it. Note: **Superclass = `task`**. That is why incident, problem, change and catalog
   tasks share fields.
3. Open the **Columns** related list. Filter `Mandatory = true`. These are the dictionary-level
   mandatory fields — the ones that apply even via API and import.
4. Now open an incident form and find a field that is required *on the form* but **not**
   mandatory in the dictionary (hint: closure fields). That difference is a **UI policy** —
   form-level rules that the dictionary knows nothing about.

**Checkpoint:** "mandatory in the dictionary" and "mandatory on the form" are different
things, and both can block you.

---

## Exercise 4 — See it as someone else (5 min)

1. Click your **avatar (top-right) → Impersonate user** → pick a user without admin.
2. Try to open the incident from Exercise 2. Note what disappears or goes read-only.
3. **Impersonation banner → Stop impersonating.** (Never leave a session impersonating.)

**Checkpoint:** name two things the non-admin could not do. That is ACL/role enforcement,
and it is why "it worked when I tested it" is not a test.

---

## Exercise 5 — Prove your instance's facts (8 min)

Run the probe from this repo (see `docs/07-probe.md` for how to paste it into a background
script). Save the JSON it prints.

Then answer:

1. How many modules on *your* instance contain "Guided Setup"?
2. Which of `incident`, `change_request`, `cmdb_ci` has the most dictionary-mandatory fields?
3. Is the SAM plugin installed?

You have just done in one minute what would take an hour of clicking — and you did it
against your instance rather than someone's blog.

---

## Done when

- [ ] You can name the primary table for incidents without looking
- [ ] You found a UI-policy-mandatory field that the dictionary does not enforce
- [ ] You impersonated a user and saw a real difference
- [ ] You have a `probe.json` from your own instance
- [ ] You can explain field vs reference field vs related list to a beginner

## If you got stuck

| Symptom | Cause | Fix |
|---|---|---|
| Filter navigator returns nothing | Typo, or the module truly is not installed | Try the table name (`sys_db_object`) or check All Available Applications |
| Cannot see Tables & Columns | No admin role | Use the PDI you own, or ask for admin on dev |
| Impersonate option missing | Not admin, or impersonation disabled by property | Use a PDI; property is `glide.impersonate.enabled` (verify) |
| Probe prints nothing | Script ran as non-admin, or output is above the visible log | Run as admin in `System Definition > Scripts - Background` and read the full response |

---

## Official sources

- Product documentation — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Developer portal + PDI — <https://developer.servicenow.com/dev.do> (read 2026-11-04)
- Now Learning fundamentals — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Community — <https://community.servicenow.com/> (read 2026-11-04)
