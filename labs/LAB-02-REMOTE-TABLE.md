# LAB 02 — A practical Remote Table (60 min)

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

**Goal:** make an external REST API behave like a ServiceNow table you can list, filter and
report on — then learn exactly where that illusion breaks.

**Scenario:** a "vendor directory" that lives outside ServiceNow. You want it inside: on a
list, filterable, usable in a reference field and a report — without copying the data.

> **Read this first:** Remote Tables are **read-only views**. No inserts, updates or deletes;
> no business rules in the usual sense; performance is the remote API's problem. If you need
> writes, use REST + Flow (Lab 01) or a scheduled import instead. Choosing the wrong one of
> these three is the single most common integration design error.

**Timebox:** 15 min design, 25 min build, 10 min verify, 10 min limits.

---

## Prerequisites

- [ ] PDI or dev, admin
- [ ] Both ends reachable from the instance (this lab uses *your own* instance as the
      "external" system — that keeps it deterministic and offline-safe)
- [ ] Ability to create a Scripted REST API (Lab 01 Part 4 if you have not)

---

## Part 1 — Design the contract (15 min)

Before configuring anything, write down the shape. A remote table needs the external side
to answer the same questions a table would:

| Question | Answer for this lab |
|---|---|
| What is one row? | A vendor: id, name, category, status, renewal date |
| What is the id? | `vendor_id` (stable, unique) |
| List endpoint | `GET /api/x_lab_vendors/vendors?sysparm_offset=0&sysparm_limit=20` |
| Single-row endpoint | `GET /api/x_lab_vendors/vendors/{id}` |
| Fields & types | id (string), name (string), category (string), active (boolean), renewal_date (date) |
| Auth | Basic auth with an integration user for the lab; OAuth 2.0 in real life |

**Check the exact URL/parameter conventions for your release** in the docs page for Remote
Tables — the contract has specific expectations (offset/limit naming, metadata endpoint)
that have changed across releases. Build to the doc for *your* version, not to a blog.

---

## Part 2 — Build the external side (25 min)

1. `All > System Web Services > Scripted REST APIs` → **New**
   - Name: `Lab Vendors`, API ID: `x_lab_vendors`
2. Create **Resource** #1: `GET /vendors`
   ```javascript
   (function process(request, response) {
       var offset = parseInt(request.queryParams.sysparm_offset || '0', 10);
       var limit  = parseInt(request.queryParams.sysparm_limit || '20', 10);

       // In real life this is the external system. Here: derive rows from your own data.
       var rows = [];
       var gr = new GlideRecord('core_company');   // vendors ≈ companies, good enough for a lab
       gr.addQuery('vendor', true);
       gr.orderBy('name');
       gr.chooseWindow(offset, offset + limit);
       gr.query();
       while (gr.next()) {
           rows.push({
               vendor_id: gr.getUniqueValue(),
               name: gr.getValue('name'),
               category: gr.getValue('notes') || 'uncategorised',
               active: gr.getValue('active') === '1',
               renewal_date: gr.getValue('u_renewal_date') // add this field, or drop the key
           });
       }
       response.setStatus(200);
       response.setBody({ result: rows });
   })(request, response);
   ```
   *(If adding `u_renewal_date` is a hassle, drop that key from the response and from your
   design table — the lab still teaches everything.)*
3. Create **Resource** #2: `GET /vendors/{id}`
   ```javascript
   (function process(request, response) {
       var id = request.pathParams.id;
       var gr = new GlideRecord('core_company');
       if (!gr.get(id)) {
           response.setStatus(404);
           response.setBody({ error: 'not found' });
           return;
       }
       response.setStatus(200);
       response.setBody({ result: { vendor_id: id, name: gr.getValue('name'), active: gr.getValue('active') === '1' } });
   })(request, response);
   ```
4. **Test both** in the API Explorer. Fix until the JSON shape matches your design table.

**Checkpoint:** the list endpoint honours `sysparm_limit` (ask for 2, get 2).

---

## Part 3 — Build the remote table (15 min)

1. `All > System Web Services > Remote Tables` → **New** (label varies by release — if you
   cannot find it, search the filter navigator for `remote table`, and if it is absent your
   release does not ship the feature)
2. Point it at the base URL of your Scripted REST API, choose the auth (basic, integration
   user), and name the table (e.g. `u_lab_vendor`).
3. Define the columns exactly as in your design table, with the **id column marked as the
   key**. A wrong key produces duplicated rows — the classic remote-table bug.
4. Save, then open the table's list view.

**Checkpoint:** you see rows, and the count matches what the API returns for the same limit.

---

## Part 4 — Use it like a table (10 min)

- [ ] Filter the list (e.g. `active = true`) and confirm the filter is pushed to the API
      (watch the API's request log / add a `gs.info` of the query params)
- [ ] Sort by name
- [ ] Build a report on the remote table
- [ ] Add it as a related list on a company record (if the release supports it)
- [ ] Put it in a dashboard

This is the payoff: the illusion holds for reading.

---

## Part 5 — Where it breaks (10 min) — the important part

| Expectation | Reality | Do this instead |
|---|---|---|
| Insert/update a row | Read-only; the write silently fails or errors | REST + Flow, or a persisted table |
| Business rules run on remote rows | They do not behave like local table rules | Validate on the external side |
| Fast joins with local tables | Every query is a network call | Persist a copy if you need to join at scale |
| ACLs protect the rows | Access is at the table level, not row level | Filter on the external API; do not rely on ACLs |
| Data is current every second | Caching exists; TTL varies by release | Know your cache window before you promise freshness |
| 50k rows paginate happily | Each page is a call; latency multiplies | Aggregate externally; sync instead |

**Decision rule:** *read rarely and live* → remote table. *Read often and join* → scheduled
import. *Need to write* → REST + flow/scripted action.

---

## Common mistakes

1. **Wrong id/key column** → duplicated rows in every list.
2. **Ignoring pagination** → you see the first 20 rows and believe that is the data.
3. **Expecting writes.** It is a view, by design.
4. **Using it for a high-volume report** and then blaming ServiceNow for latency.
5. **Basic auth with an admin account** instead of a least-privilege integration user.
6. **No timeout/retry thinking** — the external API's availability becomes your UI's
   availability.
7. **Building it when an Import Set would do** — a nightly sync is often the better design.

---

## Prove it

- [ ] A list of remote rows renders, with a filter applied server-side
- [ ] You can explain why the id column is the key
- [ ] You can name the three designs (remote table / import / REST+flow) and when each wins
- [ ] You tried an insert and saw it fail (and know what to do instead)

---

## Official sources

- Product documentation (Remote Tables, Scripted REST APIs, import sets) — <https://www.servicenow.com/docs/search?q=remote+table> (read 2026-11-04)
- Developer portal: API Explorer — <https://developer.servicenow.com/dev.do> (read 2026-11-04)
- Community (remote table limitations in practice) — <https://community.servicenow.com/> (read 2026-11-04)
- Now Learning (integration fundamentals) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
