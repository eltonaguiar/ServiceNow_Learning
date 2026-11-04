# 10 — The self-directed course path, in order

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

All courses are ServiceNow's own, on **Now Learning / ServiceNow University**
(<https://learning.servicenow.com/lxp>). Free unless marked otherwise. Titles drift between
releases, so each row gives the search term to use rather than pretending a URL is permanent.

**The order is the point.** CSA before any CIS. Automation before integration. Measurement
after you have something worth measuring. Most people take a CIS course first, fail to use
it, and conclude the platform is hard.

---

## Stage 0 — Orientation (2 hours, do it today)

| # | Course | Why now | Do this alongside |
|---|---|---|---|
| 0 | Search **"Welcome to ServiceNow"** | Gives you the vocabulary to understand every later course | [`01-ELI5.md`](01-ELI5.md) |

Skip this only if you already work in a ServiceNow team daily.

---

## Stage 1 — Platform core (10–12 hours)

| # | Course | Why now | Do this alongside |
|---|---|---|---|
| 1 | **ServiceNow Fundamentals** (free, on-demand) | The single highest-value course on the platform: navigation, tables, forms, lists, roles, reporting | [`LAB-00-ORIENTATION.md`](../labs/LAB-00-ORIENTATION.md) |
| 2 | **ServiceNow Administration Fundamentals** (free-ish; check your account) | Users, groups, ACLs, imports, update sets — the admin job | [`09-foundation-data.md`](09-foundation-data.md) + [`LAB-04-FOUNDATION-DATA.md`](../labs/LAB-04-FOUNDATION-DATA.md) |

**Milestone:** you can explain table vs record vs form vs related list, and you have loaded
a foundation data set that makes an incident behave.

---

## Stage 2 — Certification anchor: CSA (4–6 weeks part-time)

| # | Course | Why now | Do this alongside |
|---|---|---|---|
| 3 | **Certified System Administrator (CSA)** learning path + exam | CSA is the prerequisite gate for nearly every CIS. It forces breadth you would otherwise skip | Every module in this kit, one loop at a time |

Take CSA **before** specialising. It is the cheapest way to stop being surprised by the
platform later.

---

## Stage 3 — Automation (8–10 hours)

| # | Course | Why now | Do this alongside |
|---|---|---|---|
| 4 | **Flow Designer Fundamentals** (free) | 80% of what people build by hand is a flow. Learn it before scripting | [`06-inventory.md`](06-inventory.md) — find the OOB flows first |
| 5 | **Scripting in ServiceNow Fundamentals** (free) | Only after flows: scripting is for what flows cannot express | [`LAB-01-REST-MESSAGE.md`](../labs/LAB-01-REST-MESSAGE.md) Part 3 Option B |

---

## Stage 4 — Build your own app (6–8 hours)

| # | Course | Why now | Do this alongside |
|---|---|---|---|
| 6 | **App Engine Studio / Application Development Fundamentals** (search both titles) | Teaches scope, tables, roles, UI and deployment as one workflow | [`LAB-02-REMOTE-TABLE.md`](../labs/LAB-02-REMOTE-TABLE.md) |

---

## Stage 5 — Integration (6–10 hours)

| # | Course | Why now | Do this alongside |
|---|---|---|---|
| 7 | **IntegrationHub Fundamentals** (free course, paid product) | REST/SOAP, spokes, credentials, error handling — the highest-leverage skill on the platform | [`LAB-01-REST-MESSAGE.md`](../labs/LAB-01-REST-MESSAGE.md) end-to-end |

---

## Stage 6 — Measurement (4–6 hours)

| # | Course | Why now | Do this alongside |
|---|---|---|---|
| 8 | **Performance Analytics / Platform Analytics Fundamentals** | Indicator → breakdown → dashboard is how your work becomes believable | [`06-inventory.md`](06-inventory.md) §Metrics |

---

## Stage 7 — Specialise: pick **one** CIS (3–6 weeks each)

Take the one that matches the job you actually have. Not all of them.

| Course (search this) | Take it if you… | Kit companion |
|---|---|---|
| **CIS-ITSM** | work incidents/changes/problems — the commonest path | [`05-common-mistakes.md`](05-common-mistakes.md) |
| **CIS-ITAM** (+ SAM/HAM courses) | own licences, hardware, audits | [`08-SAM-SETUP.md`](08-SAM-SETUP.md) + [`LAB-03-SAM-BASELINE.md`](../labs/LAB-03-SAM-BASELINE.md) |
| **CIS-CSM** | serve external customers | [`02-success-packs.md`](02-success-packs.md) CSM prereqs |
| **CIS-HRSD** | run HR services / employee centre | [`02-success-packs.md`](02-success-packs.md) HRSD prereqs |
| **CIS-Security Incident Response** | work a SOC on the platform | [`03-breadcrumbs.md`](03-breadcrumbs.md) SecOps |
| **CIS-FSM** | schedule field engineers | [`02-success-packs.md`](02-success-packs.md) FSM prereqs |
| **CIS-Discovery / CMDB** | own the CMDB and discovery | [`LAB-02-REMOTE-TABLE.md`](../labs/LAB-02-REMOTE-TABLE.md) + CMDB brief |
| **CAD** (Certified Application Developer) | build custom apps, not processes | Stage 4 courses |

**CMDB/CSDM note:** if you touch CMDB at all, take the **CMDB/CSDM fundamentals** course
before the Discovery CIS. Identification rules and class design are where CMDB projects die.

---

## Stage 8 — Sustain (ongoing, 1–2 hours/month)

- Re-read the **release notes** for your family release: <https://www.servicenow.com/docs/>
- One micro-certification per quarter (search **"Micro-Certification"** in Now Learning —
  Flow Designer, Platform Analytics, Application Development, IntegrationHub).
- Re-take the quiz for any module you have not touched in 90 days.

---

## If you only have 10 hours

1. ServiceNow Fundamentals (6h)
2. [`LAB-00-ORIENTATION.md`](../labs/LAB-00-ORIENTATION.md) (30 min)
3. Flow Designer Fundamentals, first half (3h)
4. One module brief + its lab — pick ITSM incident or SAM

That is enough to be useful in a team meeting, honestly.

---

## How this maps to the kit's loop

| Course stage | Kit loop gate it feeds |
|---|---|
| Stage 1–2 | **Orient** and **Model** — the vocabulary and the map |
| Stage 3–5 | **Practise** — automation and integration labs |
| Stage 6 | **Prove** — indicators make claims checkable |
| Stage 7 | **Teach** — a CIS forces you to explain a domain to an examiner |

A course without a lab leaves you able to recognise, not to do. Keep them paired.

---

## Practical notes

- **Free vs paid:** "Fundamentals" courses are generally free on-demand; certification exams
  and many role courses need a paid or subscription account. Check the label on each course
  page rather than trusting a list, including this one.
- **Titles change** between releases. Always search the term, do not chase a bookmarked URL.
- **PDI is required** for the labs and is free: <https://developer.servicenow.com/dev.do>
- **Now Create** (search "Now Create") is not a course but is the implementation companion to
  Stage 7 — read the Success Pack for your CIS before the exam.

---

## Official sources

- Now Learning / ServiceNow University (all courses above) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Certification paths and exam prerequisites — <https://learning.servicenow.com/lxp> search "Certification" (read 2026-11-04)
- Now Create Success Packs (implementation companion to the CIS tracks) — <https://learning.servicenow.com/lxp> search "Now Create" (read 2026-11-04)
- Product documentation and release notes — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Developer portal + free PDI — <https://developer.servicenow.com/dev.do> (read 2026-11-04)

> Course names, durations and free/paid status are paraphrased from the official catalogue
> and change between releases; the catalogue is the authority, not this page.
