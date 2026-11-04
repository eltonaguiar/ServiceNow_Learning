# 00 — The rapid-learning methodology

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

ServiceNow has an enormous surface area for a simple reason: it is one platform wearing
dozens of costumes. ITSM, HRSD, SecOps, CSM, FSM and IRM are not different products with
different machinery — they are the same machinery pointed at different tables with
different roles and different automation. Once you internalise the machinery, a new module
costs you an hour instead of a week.

That is the entire thesis of this repo. Everything below is machinery for doing it fast,
in an order that keeps you honest.

---

## 1. The thing you are actually learning

Every module answers the same five questions. Learn to answer them on sight and you never
have to "study a module" again.

| Question | Where the answer lives | Why it matters |
|---|---|---|
| **What is the record?** | The primary table (`incident`, `change_request`, `sn_hr_core_case`, `wm_order`, `cmdb_ci`) | Everything else is a view, a flow or a report on this table |
| **What are the states?** | The `state` / `status` choice list on that table | States drive SLAs, flows, closure rules and every metric |
| **Who can see it?** | Roles (`itil`, `sn_incident_read`, `sn_hr_core.case_writer`) + ACLs | If you only test as admin, you have tested nothing |
| **How does work move?** | Assignment groups, approvals, Flow Designer flows, playbooks | This is the operating model, not the form layout |
| **How is it proven?** | Indicators → breakdowns → dashboards; SLA records | This is how anyone believes your work happened |

A module you "know" is one where you can answer all five from memory, then verify each
answer on your own instance.

---

## 2. The loop: ORIENT → MODEL → PRACTISE → PROVE → TEACH

Timeboxes below are **targets**, not measured claims. They are deliberately short so that
unfinished work becomes tomorrow's first gate rather than today's excuse.

| Gate | Target | You do | Artifact you must produce | Pass test |
|---|---|---|---|---|
| **Orient** | 10 min | Open the module's 3 key lists via the filter navigator; note the primary table | 3 breadcrumbs + table name | You can reach any list without searching the menu |
| **Model** | 20 min | Read the docs page for structure only; draw the data model | One page: tables, states, roles, arrows | You can explain it to a colleague without the screen |
| **Practise** | 45 min | The lab: build it, **break it on purpose**, fix it | Working config + one written "what broke" note | It works, and you know why it stopped working |
| **Prove** | 10 min | Run `sn_probe.js` on your instance, answer the quiz from memory | `probe.json` → study sheet | The sheet matches your expectations; mismatches are your gaps |
| **Teach** | 10 min | 5 sentences a non-technical person understands + one diagram | Teach-back note + infographic | A beginner asks a follow-up you can answer |

Total: about **95 minutes** per module. That is the number this repo optimises. Not "read
everything", not "watch a 6-hour course", not "click around until it makes sense".

### Why the order matters

- **Orient before Model** — the docs are written for people who already know where the
  module lives. If you read first, you spend the reading time lost.
- **Model before Practise** — clicking without a data model produces cargo-cult config
  that breaks on first edge case.
- **Practise before Prove** — a probe against a module you have not touched tells you what
  exists, not what you understand.
- **Prove before Teach** — teaching without verification is how wrong facts propagate to
  your team.
- **Teach last, always** — it is the only gate that catches "I recognise this" masquerading
  as "I know this".

---

## 3. Five multipliers (each one saves hours)

1. **The instance beats the docs.** Docs describe *a* release with *some* plugins. Your
   instance is the truth for your job. `scripts/sn_probe.js` reads yours in one run:
   mandatory fields from `sys_dictionary`, related lists from `sys_ui_related_list`,
   which apps are installed from `v_plugin`, whether a "Guided Setup" module even exists,
   how many flows you have. Prose cannot do that.
2. **Impersonation beats permission guessing.** Profile avatar → *Impersonate user*. Look
   at the module as the person who will actually use it. This is the single highest-yield
   habit on the platform, and it costs two clicks.
3. **Guided Setup is a syllabus, not a chore.** Where an app ships guided setup (CMDB, many
   ITSM/HR/CSM/SecOps apps — confirm for your release), its step list *is* the official
   order of operations. Steal the order even if you do not do the steps.
4. **Success Packs are scope control.** Now Create's Success Packs give the Crawl → Walk →
   Run → Fly sequence plus prerequisites and acceptance criteria. Reading one before you
   build is what stops the "we deployed it, then rebuilt it" cycle.
5. **One diagram per concept, drawn from memory.** Not a screenshot. A diagram you drew,
   then corrected against docs, exposes exactly which relationship you had wrong.

---

## 4. Source ladder — official first, always

Read in this order. Stop as soon as the question is answered.

| # | Source | Use it for |
|---|---|---|
| 1 | Product documentation — <https://www.servicenow.com/docs/> | Configuration steps, field/table definitions, release notes |
| 2 | Now Create Success Packs — via <https://learning.servicenow.com/lxp>, search "Now Create" | Implementation sequence, prerequisites, acceptance criteria |
| 3 | Now Learning / ServiceNow University — <https://learning.servicenow.com/lxp> | Courses, learning paths, certification tracks |
| 4 | Developer portal + PDI — <https://developer.servicenow.com/dev.do> | Free instance, API Explorer, hands-on labs |
| 5 | Community — <https://community.servicenow.com/> | Real-world gotchas; peer content, verify before teaching |
| 6 | Store — <https://store.servicenow.com/store> | Activation notes, which entitlement a capability needs |
| 7 | Now Support / KB — <https://support.servicenow.com/now> | Known errors, troubleshooting (login usually required) |

**ToS guardrails.** Read manually, summarise in your own words, cite the URL. Do not
bulk-scrape, crawl, mirror or republish ServiceNow content, and do not sell guides that are
mostly copied material. This repo ships no scraper: the only automated network calls are a
seven-request HTTP status check in `python3 scripts/sn_learn.py sources --check`.

**Rule of record:** a claim is only "known" once an official source says it *and* your
instance demonstrates it. Community is for the gap between those two, never instead of them.

---

## 5. When someone asks you to "just summarise a concept"

Speed comes from a fixed shape, not from writing faster. Answer in four quadrants, in this
order, 30 seconds each:

| Quadrant | Question | Example (Remote Table) |
|---|---|---|
| **What it is** | One sentence, no jargon | An external REST API that ServiceNow shows as if it were a database table |
| **What it touches** | Tables, roles, one dependency | `sys_remote_table`, a Scripted REST API or REST message as the source, a read-only role |
| **What breaks** | The 2-3 failure modes | Pagination off by one; timeouts on big queries; people expect to write to it (it is read-only) |
| **Where to click** | 3 breadcrumbs | `All > System Web Services > Remote Tables`; the table definition record; the data source |

Then: **if the request was "build a lab"**, turn the four quadrants into a runnable path —
prerequisites → build → break → verify. This repo's labs are that shape exactly
(`labs/LAB-01-REST-MESSAGE.md`, `labs/LAB-02-REMOTE-TABLE.md`).

A summary that stops at "what it is" is a dictionary entry. The value is in *what breaks*.

---

## 6. Three-day ramp (first module, from zero)

| Day | 90-minute block | Output |
|---|---|---|
| 0 (30 min) | Get a PDI, log in, run `sn_probe.js`, open `docs/01-ELI5.md` | A probe sheet and a working login |
| 1 | `platform-basics`, then `itsm-incident` with `LAB-00-ORIENTATION.md` | Two teach-back notes, one incident you raised and resolved |
| 2 | `integration` + `LAB-01-REST-MESSAGE.md` | A REST Message that creates a real record from an external API |
| 3 | `itom-cmdb` + `LAB-02-REMOTE-TABLE.md` | A remote table you can report on, plus the fields/related-lists audit |

After that, each additional module is one 95-minute loop, mostly Practise.

---

## 7. Anti-patterns that look like progress

- **Menu tourism** — clicking through every module without a data model. Feels productive,
  teaches the layout, not the machine.
- **Doc reading as study** — the docs are reference, not narrative. Read a page *after* a
  question, never instead of one.
- **Course completion as competence** — a finished video leaves no artifact. This repo's
  currency is artifacts: a probe sheet, a broken-and-fixed config, a teach-back note.
- **Testing only as admin** — admin bypasses ACLs and UI policies, so "it works" is
  meaningless for the user who will use it.
- **Building before reading the Success Pack** — the rebuild usually costs more than the
  module's whole timebox.
- **Custom before OOB** — in every module, at least half the "requirement" already ships.

---

## 8. How you know it worked

Three artifacts, in increasing order of honesty:

1. `probe.json` + rendered sheet — what the instance has (facts, not feelings)
2. quiz answered from memory — what you can recall without looking
3. teach-back note + hand-drawn diagram — what you can explain

If the teach-back needs the docs open, you have completed Orient and Model, not the loop.
That is a fine place to stop for the day; it is just not the same thing as knowing it.

---

## Official sources

- Product documentation — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Now Create Success Packs — <https://learning.servicenow.com/lxp> search "Now Create" (read 2026-11-04)
- Now Learning / ServiceNow University — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Developer portal + PDI — <https://developer.servicenow.com/dev.do> (read 2026-11-04)
- Community — <https://community.servicenow.com/> (read 2026-11-04)
- Now Support / KB — <https://support.servicenow.com/now> (read 2026-11-04)

> Source: the ladder above; Notion of "Crawl → Walk → Run → Fly" is Now Create's Success
> Pack sequencing, credited there rather than re-derived here.
