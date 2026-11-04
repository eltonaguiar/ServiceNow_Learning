# 08 — Applied module: setting up Software Asset Management (SAM)

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

This is the first *applied* module in the kit: not "what is SAM", but the order of work
that ends with a licence position you can defend in a vendor audit.

**Read this with the probe open.** SAM Foundation and SAM Pro do not use identical tables,
and entitlements change what you can even install. Anything marked **verify** is confirmed
by `scripts/sn_probe.js app sam` on your instance, never by this document.

---

## 1. ELI5 — the three questions SAM answers

| Question | Plain English | SAM object |
|---|---|---|
| **What do we own?** | What we are legally entitled to run, and until when | Entitlement / licence record, contract |
| **What is actually installed?** | What is really running on machines, found by discovery | Software installation records, tied to CIs |
| **Are they the same?** | The gap. Over-installed = audit risk. Under-installed = wasted money | Reconciliation result, compliance position |

Everything else — normalisation, publisher packs, licence metrics, true-up — exists to make
those three questions answerable. If a step does not improve one of them, question why you
are doing it.

> The classic beginner error: SAM is not "an asset register". A register tells you what
> someone typed in. SAM compares *rights* against *observed installs* and reports the
> difference. Without discovery data it is a spreadsheet with extra steps.

---

## 2. Prerequisites — check every box before you configure anything

| # | Prerequisite | Why it blocks you | How to confirm |
|---|---|---|---|
| 1 | **Entitlement + plugin** for SAM (Foundation vs Professional differ substantially) | No plugin, no tables; no entitlement, no production use | `All > System Applications > All Available Applications`; probe `v_plugin` |
| 2 | **Roles**: asset manager, SAM admin/user, plus an **integration user** for data feeds | Configuring as admin then deploying without roles = instant support tickets | Probe `sys_user_role` for `sam*` / `asset*` |
| 3 | **Discovery data source** — SCCM, Intune, Jamf, Agent Client Collector, or Service Graph Connector | SAM's entire value is observed installs; hand-entered data proves nothing | Probe for Service Graph Connector / discovery plugins; check a sample CI has `discovery_source` |
| 4 | **CMDB identification rules** for computer CI classes (a CMDB/IRE prerequisite, *not* SAM configuration — see §4) | Duplicate CIs double-count installs and destroy the compliance number | `All > Configuration Management > CI Identifiers` |
| 5 | **Content library / publisher packs** reachable | Normalisation and publisher licence rules come from downloaded content, not from your typing | SAM admin menu → content library status; probe for content tables |
| 6 | **Licence metric decisions** written down | Per-user vs per-device vs per-core changes the answer by millions; it is a commercial decision, not a config choice | A signed one-pager from the licence owner. Not optional |
| 7 | **Contract and purchase-order data** (or a plan for it) | Entitlement without a PO trail fails audit | `ast_contract`, purchase records |
| 8 | **A named owner** for reconciliation output | Unowned compliance reports are ignored | Org decision |

If 1–3 are missing, stop. You cannot "set up SAM" on top of missing discovery — you can
only set up the shell.

---

## 3. Build order (do not reorder)

Each step has a checkpoint. Do not proceed with an unchecked checkpoint; the next step
assumes it.

### Step 1 — Install and confirm the plugin
- `All > System Applications > All Available Applications > All` → search Software Asset
  Management → install/activate (admin, and entitlement permitting).
- **Checkpoint:** a SAM menu group exists in the filter navigator, and `v_plugin` shows the
  SAM plugin active. **Verify the exact plugin id on your instance** — Foundation and Pro
  differ.

### Step 2 — Guided Setup (if your release ships it)
- Type `guided setup` in the filter navigator. SAM/ITAM ships guided setup on recent
  releases; the label and depth move between families. **Verify** with the probe, which
  lists every module whose name contains "Guided Setup".
- Use it as the syllabus: read all steps first, then execute in its order. Where it
  conflicts with this document, the guided setup wins for *your* release.

### Step 3 — Roles and the integration user
- Create a dedicated integration user (not a human admin) with the minimum roles your data
  feed needs. Give it a non-expiring, documented credential in a Connection & Credential
  alias — never in a script.
- **Checkpoint:** impersonate a SAM user and confirm they can see the licence position but
  cannot edit the schema.

### Step 4 — Discovery / connector feeds
- Configure one connector first (SCCM **or** Intune **or** ACC). One. Not three.
- Scope it to a pilot group (e.g. 50 machines), run it, and **look at what arrived**.
- **Checkpoint:** a sampled computer CI has a real `discovery_source`, and its software
  installs appear as records — not as a paragraph in the description field.

### Step 5 — Normalisation and content
- Run/review normalisation so "Microsoft Office 365 ProPlus" and "Microsoft 365 Apps for
  enterprise" resolve to one product. Download the content library if your instance uses it.
- **Checkpoint:** pick the 5 most common software titles in your estate; each maps to
  exactly one normalised product. If two titles map to one product and their licence
  metrics differ, you have a reconciliation bug waiting.

### Step 6 — Entitlements (rights)
- Create entitlements from contracts/POs: product, quantity, metric, start/end dates,
  licence type (subscription vs perpetual), and **downgrade/upgrade rights**.
- **Checkpoint:** every entitlement traces to a document. No document, no entitlement —
  otherwise you are inventing rights you do not own.

### Step 7 — Licence metrics
- For each in-scope publisher, decide the metric: per user, per device, per core, per
  processor, per server. This is commercial, and it is where audits are won or lost.
- **Checkpoint:** the metric in the platform matches the metric in the contract. A
  per-core contract modelled per-device will always look compliant and always fail audit.

### Step 8 — Reconciliation and the compliance position
- Run reconciliation. Then read the *exceptions*, not the headline number: the top 10
  products by spend, and anything showing over-licensed or unlicensed.
- **Checkpoint:** you can explain the top 3 gaps in one sentence each, and one of them is
  a data problem rather than a licence problem (there is always one).

### Step 9 — Dashboards, reporting, cadence
- Licence position dashboard, software spend, renewals in the next 90 days.
- Set the cadence: weekly exceptions review, monthly position, quarterly true-up input.
- **Checkpoint:** a named person opens it on a schedule. An unopened dashboard is decoration.

---

## 4. Identity: identification rules, normalisation, metrics — three different things

People say "we need identification rules for Adobe" and mean normalisation. That confusion
costs weeks, so keep the layers apart:

| Mechanism | Question it answers | Where it is configured | Applies to |
|---|---|---|---|
| **CI identification rules** (Identification and Reconciliation Engine, IRE) | Is this incoming CI new, or the one I already have? | CI Class Manager / CI Identifiers, per CI class | **CMDB → every CI**, including all hardware: servers, laptops, network gear. This is what **HAM** relies on |
| **Asset↔CI reconciliation** (HAM) | Which asset record is this CI? | HAM asset sync, matched on **serial number** | Hardware assets ↔ hardware CIs — related to identification, but a separate mechanism |
| **Software normalisation / recognition** | Is "Microsoft 365 Apps for enterprise" the same product as "Office 365 ProPlus"? | SAM normalisation, content library / publisher packs | **SAM** — this is SAM's real "identification" problem |
| **Licence metric** | How are rights counted: per user, device, core, processor? | Entitlement record | **SAM** — commercial decision, not a technical one |
| **Licence reconciliation** | Rights vs installs → compliance position | SAM reconciliation | **SAM** — the output you defend |

**So: does it apply to SAM, HAM, or both?**

- **HAM: yes, directly.** Hardware identity is the whole game: one laptop seen by SCCM, Intune
  and a manual import must resolve to one CI, and the serial number is usually the anchor. Bad
  identification rules give you three laptops, three assets, and an asset register nobody trusts.
- **SAM: not directly, but fatally exposed.** There are no identification rules for software
  products — you normalise instead. However every software install record hangs off a CI, so
  duplicate CIs duplicate installs, and duplicate installs inflate the compliance gap. Fix CI
  identification for the computer classes **before** you reconcile, or you will spend a week
  explaining a shortage that is really a duplicate.
- **Both** depend on the same underlying data quality, which is why it belongs in the SAM
  prerequisites as a **CMDB** item — the fix is in the CMDB, not in SAM.

> Practical test: if the thing you are deduplicating is *a machine*, it is IRE and lives in the
> CMDB. If it is *a software title*, it is normalisation and lives in SAM. If it is *a quantity
> of rights*, it is a licence metric and is a commercial decision.

---

## 5. Fields: critical vs useful vs optional

Field names below are the conventional ones; **verify on your instance** — SAM Foundation
and Pro differ, and admins add mandatory fields.

### Entitlement / licence record
| Field | Verdict | Why |
|---|---|---|
| Product (normalised) | **Critical** | Without the right product, the entitlement never matches installs |
| Quantity / rights | **Critical** | The number you defend in an audit |
| Licence metric | **Critical** | Wrong metric = permanently wrong compliance answer |
| Start / end date | **Critical** | Expired entitlement silently turns into unlicensed installs |
| Licence type (subscription/perpetual) | **Critical** | Changes how "owned" is calculated |
| Publisher / contract link | Useful | Traceability to the PO; auditors ask for it |
| Cost, cost centre | Useful | Spend reporting, not compliance |
| Downgrade rights | Useful (critical for some publishers) | Ignoring them overstates non-compliance |
| Asset tag / serial | Optional | Rarely meaningful for software rights |

### Software install record
| Field | Verdict | Why |
|---|---|---|
| Linked CI | **Critical** | An install without a device cannot be counted |
| Normalised product | **Critical** | Drives matching |
| Version / edition | Useful | Edition differences decide licence tier |
| Install date, last seen | Useful | Stale installs inflate counts; age tells you which |
| Discovery source | Useful | Tells you whether to trust it |

### Related lists worth configuring
- Entitlement → **contracts**, **assets/installs covered**, **compliance results**
- Product → **versions**, **entitlements**, **installs**
- CI → **software installs**, **incidents**, **changes** (this is how SAM connects to ITSM)
- Contract → **entitlements**, **renewal tasks**

---

## 6. Metrics and dashboards that matter (and the ones that lie)

| Metric | Use it? | Caution |
|---|---|---|
| Licence compliance position (per publisher) | Yes | Meaningless if discovery is partial — publish the coverage % beside it |
| Software spend vs entitlement | Yes | Needs cost data you probably have not loaded yet |
| Installs without normalised product | **Yes — best first KPI** | This is the data-quality number that predicts every other number |
| Renewals within 90 days | Yes | Cheap, high value, wins stakeholder trust early |
| "Number of unlicensed installs" alone | No | Without coverage context it is fear, not information |
| Raw install count as "usage" | **No** | Installed ≠ used; usage needs metering |

Dashboards: licence position by publisher · normalisation gaps · discovery coverage ·
renewal calendar. Four is plenty; add the fifth only when someone asks.

---

## 7. Guided Setup, OOB content and Success Packs — what to expect

| Thing | Status | Note |
|---|---|---|
| **Guided Setup** | Usually present for SAM/ITAM on recent releases | Label and depth vary; probe for it, do not trust a blog screenshot |
| **Out-of-box flows** | Lifecycle: request → procure → receive → deploy → retire; reconciliation jobs; renewal notifications | Reuse before building |
| **OOB dashboards** | Licence position, spend, renewals (entitlement-dependent) | Start from OOB, delete what nobody opens |
| **Success Pack** | Yes — SAM/ITAM has Now Create content with phases and prerequisites | Read it before Step 1; it is the official version of this page |
| **IntegrationHub spokes** | Service Graph Connectors for SCCM/Intune/Jamf; publisher connectors for Oracle/SAP/Microsoft on Pro | Which ones you get depends on entitlement — check the Store activation notes |

**Crawl → Walk → Run → Fly, applied to SAM** (Now Create's sequencing):

- **Crawl** — one publisher, one discovery source, entitlements loaded, first compliance
  position. Prove the loop end-to-end on something small.
- **Walk** — normalisation coverage, renewal alerts, monthly cadence, exceptions triage.
- **Run** — multi-publisher, true-up inputs, spend reporting, change/incident linkage.
- **Fly** — optimisation (reclaim, right-size, cloud/SaaS in scope), continuous compliance.

Do not skip from Crawl to Fly because a vendor demo looked good.

---

## 8. Ten mistakes that cost real money

1. **Installing SAM and calling it done.** The plugin is 5% of the work; discovery and
   normalisation are the other 95%.
2. **Partial discovery published as full compliance.** Always publish coverage % next to
   the number.
3. **Wrong licence metric** (per-core modelled per-device). Looks compliant, fails audit.
4. **Normalisation left alone** so one product appears as six, splitting entitlements and
   inventing shortages.
5. **Entitlements without contract/PO evidence** — rights you cannot document.
6. **Ignoring downgrade rights**, overstating non-compliance and buying licences twice.
7. **Multiple discovery sources with no de-duplication** — the same install counted twice,
   doubling your apparent exposure.
8. **Treating installs as usage.** Installed ≠ used; optimisation needs metering.
9. **No owner for the output.** Compliance reports nobody reads change nothing.
10. **Expired entitlements unnoticed** — the position silently flips to unlicensed.

---

## 9. Your first lab

`labs/LAB-03-SAM-BASELINE.md` — build a three-product baseline, reconcile it, then break it
by changing a licence metric and watch the position flip. That last step is the one that
teaches SAM; the rest is typing.

---

## 10. "Is our SAM actually set up?" — verification checklist

- [ ] Plugin active, entitlement documented
- [ ] One discovery source feeding real installs, coverage % known
- [ ] Normalisation: top-10 titles each map to exactly one product
- [ ] Every entitlement traceable to a contract/PO
- [ ] Licence metric matches contract wording, per publisher
- [ ] Reconciliation runs on a schedule and completes without error
- [ ] Compliance position published with coverage context
- [ ] Renewal alerts fire ≥ 90 days ahead
- [ ] A named owner reviews exceptions weekly
- [ ] A SAM user (not admin) can see exactly what they should and nothing more

If any box is unchecked, that is the next hour's work — not a new module.

---

## Official sources

- Product documentation (SAM / ITAM) — <https://www.servicenow.com/docs/search?q=software+asset+management> (read 2026-11-04)
- Now Create Success Pack for SAM/ITAM — <https://learning.servicenow.com/lxp> search "Now Create" (read 2026-11-04)
- Now Learning: SAM/ITAM courses and the CIS-ITAM path — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- ServiceNow Store (which SAM/connector content your entitlement includes) — <https://store.servicenow.com/store> (read 2026-11-04)
- Now Support KB (reconciliation and normalisation errors) — <https://support.servicenow.com/now> (read 2026-11-04)
- Community (audit gotchas from practitioners) — <https://community.servicenow.com/> (read 2026-11-04)

> This page is a paraphrase and an ordering, not a copy of ServiceNow documentation.
> Where it disagrees with the docs or your Success Pack for your release, they win.
