# 07 — The probe: make your instance the source of truth

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

Every table of "mandatory fields" on the internet is a guess about *some* release with
*some* plugins. The probe replaces the guess with a measurement of your own instance.

It is **read-only**: `get()` and `COUNT` queries only. No writes, no schema changes, no
installs.

---

## 1. Run it (2 minutes)

1. `All > System Definition > Scripts - Background`
2. Paste the contents of [`scripts/sn_probe.js`](../scripts/sn_probe.js)
3. Choose **Global** scope, click **Run script**
4. The response pane shows the JSON between `=== SNPROBE BEGIN ===` and `=== SNPROBE END ===`

On a Fix Script instead: create the record, paste, **Run Fix Script**, then read the log.

What it collects:

| Section | What you get | Why you care |
|---|---|---|
| `tables` | For 15 core tables: label, superclass, **dictionary-mandatory fields**, **related lists**, row count | The fields question, answered per instance |
| `plugins` | Active plugins (first 60) | Which apps are actually installed |
| `guided_setup` | Every active module whose title contains "Guided Setup" | Whether your release ships guided setup, and for what |
| `automation` | Flow count, active count, recently updated flows | OOB automation you should reuse |
| `apis` | Scripted REST APIs, outbound REST messages | What integration surface already exists |
| `analytics` | Indicator / report / dashboard counts | Whether PA is actually in use |
| `sam` | All `samp_*` / `cmdb_sam_*` tables present | SAM Foundation vs Pro vs not installed |
| `errors` | Any query that failed | Honest gaps instead of silent zeros |

---

## 2. Save it

Copy the JSON into `probe.json` (gitignored — it contains your instance name and user).
**Do not commit probe output**: it is instance-specific and mildly sensitive.

---

## 3. Render it into a study sheet

```bash
python3 scripts/sn_sheet.py probe.json --out docs/generated/probe-sheet.md
```

The sheet gives you, per table: mandatory fields (with type and label), related lists,
row counts — plus a **gap list**: expectations from `data/modules.json` that your instance
does not show (e.g. "no Guided Setup module found for this release", "SAM tables absent",
"no flows active").

That gap list is the most useful output: it is the difference between what the kit expects
and what you actually have to work with.

---

## 4. Use it as the Prove gate

The loop in [`00-methodology.md`](00-methodology.md) ends in *Prove*. Concretely:

- [ ] Run the probe **after** you finish a lab, not before
- [ ] Check the tables you touched show up with the fields you configured
- [ ] Confirm the related lists you added are present
- [ ] Check `errors` is empty; each entry is a release difference worth knowing

If the sheet disagrees with what you built, the sheet is right — and you have found a real
gap rather than an imagined one.

---

## 5. Limits (be honest about them)

| Limit | Consequence |
|---|---|
| Only 15 tables by default | Edit the `TABLES` array at the top to widen scope |
| 60-row cap per list | Designed for readability, not exhaustive audit |
| First 60 active plugins | Very large instances truncate; raise `MAX_ROWS` if you need all |
| Field names differ by release | Each section is wrapped in try/catch; failures land in `errors`, never silently |
| No ACL/role evaluation | It reports config, not "what this user can see" — impersonate for that |
| Not a substitute for docs | It tells you *what exists*, not *why it works that way* |

---

## 6. Extending it

Add a table: append to `TABLES`. Add a section: copy the `safe()` pattern so one bad query
cannot take down the whole probe. Keep it read-only — the moment it writes, people will
(rightly) refuse to run it on anything but a sandbox.

---

## Official sources

- Product documentation (tables, dictionary, related lists, application modules) — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Developer portal (API Explorer, background scripts, PDI) — <https://developer.servicenow.com/dev.do> (read 2026-11-04)
- Now Learning (scripting fundamentals) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Community (probe-style audit scripts; compare approaches) — <https://community.servicenow.com/> (read 2026-11-04)
