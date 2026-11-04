# LAB 01 — A REST Message that actually *does* something (75 min)

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

**Goal:** call an external API, and turn the answer into a real record with real data — not
a "hello world" that prints a string. Then break it and fix it.

**Scenario:** the Toronto office building. If the outside temperature drops below 5 °C,
raise an incident for Facilities to check the heating. Silly? It is a real pattern:
*external condition → ServiceNow record.*

API: Open-Meteo (`https://api.open-meteo.com/v1/forecast`) — free, no key, JSON, stable.
If it is unavailable, any public JSON API works; only the parsing changes.

---

## Prerequisites

- [ ] A PDI or dev instance, admin
- [ ] You completed [`LAB-00-ORIENTATION.md`](LAB-00-ORIENTATION.md)
- [ ] You can create a Flow Designer flow (or you will, in step 3)
- [ ] Outbound internet from your instance (PDIs have it; locked-down prod may not)

**Timebox:** 20 min build, 25 min make it real, 20 min break/fix, 10 min prove.

---

## Part 1 — Prove the API works before touching ServiceNow (5 min)

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&current=temperature_2m"
```

Expected shape:

```json
{"latitude":43.65,"longitude":-79.38,"current":{"time":"...","temperature_2m":7.4,"interval":900}}
```

Note the nesting: the value you want is `current.temperature_2m`. Half of all integration
bugs are a wrong path into JSON, so **write the path down now**.

> Rule: if curl/Postman cannot do it, ServiceNow cannot do it. Test outside first.

---

## Part 2 — Build the REST Message (15 min)

1. `All > System Web Services > Outbound > REST Message` → **New**
2. Name: `Open-Meteo Toronto`. Endpoint: `https://api.open-meteo.com/v1/forecast`
3. Save. In the **HTTP Methods** related list, open the default `GET` → rename to
   `get_current_temperature`
4. Add HTTP query parameters (or append to the endpoint):
   - `latitude` = `43.65`
   - `longitude` = `-79.38`
   - `current` = `temperature_2m`
5. **HTTP Headers** related list: add `Accept: application/json`
   *(Open-Meteo does not require it; every enterprise API you meet later will. Build the habit.)*
6. No authentication for this API. For a real one you would use **Connection & Credential
   aliases**, never a token typed into the message.
7. Click **Test** (the link on the method record). You should see the JSON body.

**Checkpoint:** the test returns a body containing `temperature_2m`. If it returns 4xx, read
the actual response — do not guess.

---

## Part 3 — Make it do something (25 min)

### Option A — no code (recommended first pass)

1. `All > Process Automation > Flow Designer` → **New → Flow**
2. Trigger: **Schedule** — daily at 06:00 (or "Run once" while testing)
3. Action: **REST step** → *ServiceNow* → **REST Step**
   - Connection: create/reuse an HTTP connection, or use the REST Message you just built
   - Method: GET, URL as in Part 1
4. Action: **If** → condition on the response body. Simplest reliable form: a
   **Script step** that parses and returns a boolean:
   ```javascript
   // Flow Designer script step — inputs: body (string)
   var data = JSON.parse(inputs.body);
   return data.current.temperature_2m < 5;
   ```
5. If true → **Create Record** on `incident`:
   - `short_description` = `Facilities: outside temperature {temp}°C at Toronto office — check heating`
   - `caller_id` = a service account user (not yourself — see mistakes)
   - `assignment_group` = Facilities (create one if needed)
   - `description` = raw JSON + timestamp (evidence beats prose)
6. **Prevent duplicates** (this is the part people skip and then hate): before creating,
   look for an open incident with the same short_description prefix from today. If found,
   add a work note instead.

Turn the flow **active**, run it once, verify the incident exists and contains the real
temperature.

### Option B — scripted (for when you need it in a Script Include)

```javascript
// Background script / Script Include — outbound call with error handling
var req = new sn_rest.RESTMessageV2('Open-Meteo Toronto', 'get_current_temperature');
req.setRequestHeader('Accept', 'application/json');
req.setEccParameter('skip_sensor', true); // direct call, no MID Server
try {
    var resp = req.execute();
    var status = resp.getStatusCode();
    var body = resp.getBody();
    if (status !== 200) {
        gs.error('Open-Meteo HTTP ' + status + ' :: ' + body);
    } else {
        var data = JSON.parse(body);
        gs.info('Toronto temperature: ' + data.current.temperature_2m + ' C');
        // then: new GlideRecord('incident') ... insert()
    }
} catch (e) {
    gs.error('Open-Meteo call failed: ' + e.message);
}
```

Note what is *missing* from the naive version: retry, timeout tuning, dedupe. That is
exactly what the flow gives you for free.

---

## Part 4 — The inbound direction (15 min, optional but clarifying)

ServiceNow calling out is half the story. The other half is someone calling in.

1. `All > System Web Services > Scripted REST APIs` → **New** → name `Lab Readings`, API id
   `x_lab_readings`
2. Add a **Resource**: method `POST`, path `/reading`
3. Script:
   ```javascript
   (function process(request, response) {
       var payload = request.body.data;
       if (!payload || !payload.temperature) {
           response.setStatus(400);
           response.setBody({ error: 'temperature is required' });
           return;
       }
       var gr = new GlideRecord('u_temperature_reading'); // create this table, or use 'incident'
       gr.initialize();
       gr.setValue('short_description', 'Reading: ' + payload.temperature + ' C');
       var sysId = gr.insert();
       response.setStatus(201);
       response.setBody({ sys_id: sysId });
   })(request, response);
   ```
4. Test it in the **API Explorer** (developer portal) or with curl using basic auth.
5. Check `sys_outbound_http_log` — no, wrong log: for inbound use `All > System Logs > All`
   and filter on your API name.

**Why this matters:** once you have built both directions, "integration" stops being magic.
It is a request, a body, a status code, and a record.

---

## Part 5 — Break it on purpose (20 min) — the actual learning

| Break | Expected behaviour | What you should learn |
|---|---|---|
| Endpoint → `https://api.open-meteo.com/v1/nope` | 404, flow should not create an incident | Error branches are not optional |
| Remove `current` parameter | 400 with a message naming the missing param | Read the vendor's error body |
| `JSON.parse` a truncated body | Exception in the script step | Always guard parse |
| Condition `< 500` instead of `< 5` | Incident every run | A wrong threshold is a spam cannon |
| Delete the assignment group | Incident created unassigned | Silent orphaning |
| Set a 1-second timeout on a slow call | Timeout error in the log | Timeouts are configuration |

After each break: fix it, re-run, and note **what told you what was wrong**. Usually
`sys_outbound_http_log` or the flow run's action output — not the docs.

---

## Common mistakes

1. **Hardcoding credentials** in the message or script. Use Connection & Credential aliases.
2. **Not checking the status code.** A 200 can carry an error payload.
3. **Parsing without guarding.** One malformed response kills a flow with no useful log.
4. **Testing with "Run once" and shipping without a schedule.**
5. **No dedupe** — the flow creates a new incident every run, forever.
6. **Wrong content type** on POST (`415 Unsupported Media Type`).
7. **Caller = your admin account**, so every incident looks like you reported it.
8. **Ignoring `sys_outbound_http_log`** and blaming the vendor.

---

## Prove it

- [ ] `All > System Logs > Outbound HTTP Requests` shows a 200 for your message
- [ ] A real incident exists with the real temperature in the description
- [ ] Running the flow twice does **not** create two incidents
- [ ] You can break the endpoint and explain which log told you why
- [ ] You can draw the flow: trigger → REST → parse → condition → create record

---

## Official sources

- Product documentation (REST messages, Flow Designer REST step, Scripted REST APIs) — <https://www.servicenow.com/docs/search?q=rest+message> (read 2026-11-04)
- Developer portal: API Explorer (try inbound endpoints live) — <https://developer.servicenow.com/dev.do> (read 2026-11-04)
- Now Learning (Flow Designer + integration fundamentals) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Community (real-world REST gotchas) — <https://community.servicenow.com/> (read 2026-11-04)
