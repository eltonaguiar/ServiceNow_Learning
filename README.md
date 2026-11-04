# ServiceNow Learning — learn any module in 95 minutes, then prove it

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

**Website:** <https://eltonaguiar.github.io/ServiceNow_Learning/>
**SAM track:** <https://github.com/eltonaguiar/ServiceNow_Learning_SAM>

ServiceNow is one platform wearing dozens of costumes. ITSM, HRSD, SecOps, CSM, FSM, SAM and
IRM are the same machinery — tables, states, roles, routing, proof — pointed at different
records. This repository teaches the machinery **once**, then gives you a repeatable loop to
absorb any module, plus beginner guides, applied SAM setup, hands-on labs, and a read-only
probe that turns your own instance into the source of truth.

Built in the open, from official ServiceNow sources only. No doc mirrors, no scraped content,
no "10 tricks" listicles.

---

## Contents

- [Start here](#start-here)
- [The loop](#the-loop)
- [The applied module: SAM](#the-applied-module-sam)
- [Labs](#labs)
- [The toolkit](#the-toolkit)
- [Repository map](#repository-map)
- [Official sources](#official-sources)
- [What is verified, and what is not](#what-is-verified-and-what-is-not)
- [Conventions](#conventions)

---

## Start here

| Read | Why |
|---|---|
| [`docs/01-ELI5.md`](docs/01-ELI5.md) | The building-and-filing-cabinet analogy, a 30-minute first session, and a glossary that defines every term before using it |
| [`docs/00-methodology.md`](docs/00-methodology.md) | The five-gate loop, why the order matters, and the five multipliers that save hours |
| [`labs/LAB-00-ORIENTATION.md`](labs/LAB-00-ORIENTATION.md) | A zero-risk first 30 minutes on your own instance |

Then pick a module and run one loop. That is the whole product.

---

## The loop

| Gate | Target | Artifact | Pass test |
|---|---|---|---|
| **Orient** | 10 min | 3 breadcrumbs + primary table | Reach any list without searching menus |
| **Model** | 20 min | One page: tables, states, roles, arrows | Explain it without the screen |
| **Practise** | 45 min | Working config + "what broke" note | It works, and you know why it stopped |
| **Prove** | 10 min | `probe.json` → study sheet | Sheet matches expectations; gaps are your gaps |
| **Teach** | 10 min | 5 sentences + one diagram | A beginner's follow-up gets a real answer |

Timeboxes are targets, not measured benchmarks. The point is to stop before diminishing
returns and let the next session start from what you could not explain.

Infographics: [`infographics/learning-loop.png`](infographics/learning-loop.png) ·
[`infographics/module-anatomy.png`](infographics/module-anatomy.png) ·
[`infographics/integration-flow.png`](infographics/integration-flow.png)

---

## The applied module: SAM

The first module carried all the way to a defensible number:

- [`docs/08-SAM-SETUP.md`](docs/08-SAM-SETUP.md) — prerequisites, the nine-step build order,
  critical vs useful fields, the metrics that lie, and ten mistakes that cost money.
- [`labs/LAB-03-SAM-BASELINE.md`](labs/LAB-03-SAM-BASELINE.md) — build one compliance
  position for three titles with three different licence metrics, then break it on purpose.
- Part 0-B of the lab covers instances **without** SAM entitlement (PDIs usually qualify),
  so the reasoning is learnable even when the plugin is not.

---

## Labs

| Lab | What you build | Time |
|---|---|---|
| [`LAB-00-ORIENTATION.md`](labs/LAB-00-ORIENTATION.md) | Nothing — you learn to read the platform | 30 min |
| [`LAB-01-REST-MESSAGE.md`](labs/LAB-01-REST-MESSAGE.md) | A REST Message that creates a real incident from live external data, with dedupe, plus the inbound direction | 75 min |
| [`LAB-02-REMOTE-TABLE.md`](labs/LAB-02-REMOTE-TABLE.md) | A REST API exposed as a read-only table, used in a report, with its limits demonstrated | 60 min |
| [`LAB-03-SAM-BASELINE.md`](labs/LAB-03-SAM-BASELINE.md) | A licence position you can defend — and can break with one metric change | 90 min |

Every lab has a **break-it-on-purpose** phase. That phase, not the typing, is where learning
happens.

---

## The toolkit

| Tool | What it does |
|---|---|
| [`scripts/sn_probe.js`](scripts/sn_probe.js) | Read-only ServiceNow-side probe: mandatory fields, related lists, plugins, Guided Setup modules, flows, APIs, SAM presence. Run in *Scripts - Background*; see [`docs/07-probe.md`](docs/07-probe.md) |
| [`scripts/sn_sheet.py`](scripts/sn_sheet.py) | Renders probe JSON into a study sheet with a gap list against the knowledge base |
| [`scripts/sn_learn.py`](scripts/sn_learn.py) | `list`, `brief`, `plan`, `quiz`, `sources` over `data/modules.json` — a timeboxed brief per module |
| [`scripts/make_infographic.py`](scripts/make_infographic.py) | Regenerates the three infographics as SVG (+ PNG when a converter exists) |
| [`scripts/build_site.py`](scripts/build_site.py) | Regenerates the GitHub Pages landing pages |
| [`scripts/sn_lint.py`](scripts/sn_lint.py) | Enforces this repo's rules: stamps, dates, official-source allowlist, live links, valid KB |

```bash
# the whole toolkit, no dependencies beyond python3
python3 scripts/sn_learn.py list
python3 scripts/sn_learn.py brief itom-cmdb
python3 scripts/sn_learn.py plan itsm-incident --start 09:30
python3 scripts/sn_sheet.py probe.json --out docs/generated/probe-sheet.md
python3 scripts/make_infographic.py
python3 scripts/sn_lint.py
```

---

## Repository map

```
data/
  modules.json     13-module knowledge base: breadcrumbs, fields, OOB, mistakes, quizzes
  sources.json     official source ladder + ToS guardrails + per-module docs queries
docs/
  00-methodology.md     the loop, the multipliers, the anti-patterns
  01-ELI5.md            beginner guide + 40-term glossary
  02-success-packs.md   Now Create sequencing, prerequisites per app
  03-breadcrumbs.md     where things live, with table names
  04-fields.md          three kinds of required; four related lists worth adding
  05-common-mistakes.md symptom → cause → fix
  06-inventory.md       Guided Setup / OOB flows / spokes / metrics per app
  07-probe.md           how to run and use the probe
  08-SAM-SETUP.md       applied SAM guide
labs/                   4 hands-on labs, each with a break-it phase
scripts/                probe, sheet, brief generator, infographics, site, lint
infographics/           SVG + PNG, regenerable
```

---

## Official sources

Everything here is paraphrased and linked; nothing is mirrored.

| Source | Used for |
|---|---|
| <https://www.servicenow.com/docs/> | Configuration steps, schema, release notes |
| <https://learning.servicenow.com/lxp> | Now Create Success Packs (search "Now Create") and Now Learning courses |
| <https://developer.servicenow.com/dev.do> | Free PDI, API Explorer, developer learning |
| <https://community.servicenow.com/> | Practitioner gotchas; never the source of record |
| <https://store.servicenow.com/store> | Spokes, connectors, activation notes |
| <https://support.servicenow.com/now> | Known errors, KB articles |

**Terms-of-service guardrails.** Read manually, summarise in your own words, cite the URL. Do
not scrape, crawl, mirror or republish ServiceNow content, and do not sell guides that are
mostly copied material. This repo ships no scraper: the only automated network access is a
seven-request HTTP status check in `python3 scripts/sn_learn.py sources --check`.

---

## What is verified, and what is not

- **Verified here:** URLs and HTTP reachability of the official sources (2026-11-04); the
  scripts run; the infographics regenerate; the lint passes.
- **Not verified here:** behaviour inside a licensed SAM/FSM/SecOps instance. No instance
  was available, so those guides are documentation-grounded and explicitly mark every
  release-dependent claim **verify** — the probe is how you resolve them.
- **Timeboxes** are targets for pacing, not measured benchmarks.
- **Menu labels** move between releases; the guides give the table name alongside the path
  for exactly that reason.

---

## Conventions

- Every doc carries an agent stamp and an `Updated:` date.
- Every doc ends with an **Official sources** section; `scripts/sn_lint.py` fails the build if
  a non-ServiceNow domain sneaks in.
- Every claim that varies by release is marked **verify** and resolvable via the probe.
- Facts beat feelings: a module is learned when there is an artifact (probe sheet, broken and
  fixed config, teach-back note), not when a video finished.

Issues and corrections: <https://github.com/eltonaguiar/ServiceNow_Learning/issues>
