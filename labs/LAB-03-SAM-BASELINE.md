# LAB 03 — SAM baseline: build a licence position and watch it lie (90 min)

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

**Goal:** produce one defensible compliance number for three software titles, then break it
by changing one commercial assumption — the moment SAM stops being data entry and becomes a
business conversation.

Read [`docs/08-SAM-SETUP.md`](../docs/08-SAM-SETUP.md) first; this lab is its hands-on.

---

## Prerequisites

- [ ] SAM Foundation or SAM Pro installed **and entitled**. Check before you start:
      `All > System Applications > All Available Applications`, or run `scripts/sn_probe.js`
      and look at the `sam` section (empty table list = no SAM schema).
- [ ] Admin on a dev instance or PDI
- [ ] 10 minutes with `scripts/sn_probe.js` output in hand

### If your PDI has no SAM (common)

Do **Part 0-B** instead: you will still build a licence position, with the same reasoning,
using only `alm_asset` + `cmdb_model`. The concept survives the missing plugin; the menu
labels do not.

---

## Part 0-A — Map what you have (10 min)

Run the probe. Then answer in writing:

1. Is the SAM schema present (`samp_*` / `cmdb_sam_*` tables)?
2. How many computer CIs exist, and how many have a `discovery_source`?
3. Is any discovery/connector plugin active?

If (1) is no → Part 0-B. If (2) is "few or none" → your compliance number will be fiction;
say so out loud before you build it, because that is the professional behaviour.

---

## Part 0-B — No-SAM fallback (20 min)

Build the same position by hand, which is exactly what SAM automates:

1. `All > Asset > Assets > Hardware` → create 3 computer assets (or use existing), each
   linked to a CI.
2. `All > Asset > Portfolios > Product Models` → create 3 software models: e.g. *Acme Suite
   Standard*, *Acme Suite Pro*, *Globex Reporting*.
3. Record "installs" in a simple custom table or even a spreadsheet: 12 Acme Standard, 4
   Acme Pro, 20 Globex.
4. Record "rights": 10 Acme Standard, 4 Acme Pro, 25 Globex.
5. Compute the position by hand: Acme Standard **−2 (short)**, Acme Pro **0**, Globex **+5
   (spare)**.

You now have the model. Everything SAM does is this arithmetic plus discovery, normalisation
and scale.

---

## Part 1 — Three titles, three decisions (15 min)

Pick three real-ish titles with *different* licensing shapes. This is deliberate: one metric
type teaches nothing.

| Title | Metric | Rights | Installs | Naive answer |
|---|---|---|---|---|
| Acme Suite Standard | per device | 10 | 12 | 2 short |
| Acme Suite Pro | per user | 4 | 6 devices / 3 users | **depends** |
| Globex Reporting | per core (server) | 8 cores | 1 server, 4 cores | 4 spare |

The middle row is the lesson: 6 installs vs 4 licences looks like a 2-licence gap until you
realise the metric is per *user* and only 3 people use it.

---

## Part 2 — Build entitlements (20 min)

For each title:

1. Create/locate the normalised software product.
2. Create the entitlement: quantity, **metric**, start/end date, licence type
   (subscription/perpetual), and the contract/PO reference.
3. **No document, no entitlement.** If you cannot attach a reference, leave it out and note
   why — inventing rights is how audits go wrong.

**Checkpoint:** every entitlement has a metric and a date range. An entitlement with no
metric will never reconcile usefully.

---

## Part 3 — Reconcile (15 min)

Run reconciliation (SAM admin menu, or the OOB job — label varies by release; probe lists
what exists). Then open the licence position and read the **exceptions**, not the headline.

For each of the three titles write:

- Rights / installs / observed metric
- Compliance verdict
- **Confidence**: what share of your estate is actually discovered? (If 20%, write "20%
  confidence" next to the number. This single habit prevents most SAM embarrassment.)

---

## Part 4 — Break it on purpose (15 min) — the actual lab

| Change | What happens | Lesson |
|---|---|---|
| Acme Standard metric: per device → per user | Position flips from −2 to (probably) +large | Metric is a commercial decision, not a config detail |
| Entitlement end date → last month | Title flips to unlicensed | Expiry is silent |
| Add a second discovery source for the same machines | Install count roughly doubles | Dedupe before you trust |
| Delete the normalisation mapping for Acme Suite | Product splits; entitlement matches nothing | Normalisation is load-bearing |
| Set rights to "unlimited" for Globex | Always compliant, always useless | Vanity metrics hide spend |

Fix each one. Note **which screen told you what was wrong**.

---

## Part 5 — Publish it honestly (10 min)

Build a one-screen view with four tiles:

1. Compliance position (per title) — with coverage %
2. Installs without a normalised product (data quality)
3. Renewals in the next 90 days
4. A link to the filtered list of exceptions

Then write one sentence per tile a non-technical manager would understand. If you cannot,
the tile is wrong, not the manager.

---

## Common mistakes (all of them cost money)

1. Publishing a compliance number without discovery coverage.
2. Treating installs as usage.
3. Per-core contracts modelled per device.
4. Entitlements with no contract reference.
5. Ignoring downgrade rights (overstating non-compliance, buying twice).
6. Loading two discovery sources with no de-duplication.
7. Leaving normalisation at defaults for the top-10 titles.
8. No owner, no cadence, dashboard unopened.
9. Building on a PDI that has no SAM and assuming you tested SAM.
10. Skipping the renewal alert, then discovering auto-renewal after the fact.

---

## Prove it

- [ ] One compliance number, with its coverage % beside it
- [ ] Three titles, three different metrics, three correct verdicts
- [ ] You can explain why "6 installs vs 4 licences" is not necessarily a gap
- [ ] You broke the position by changing a metric and can explain the flip
- [ ] You can name the four tiles a manager actually needs

---

## Official sources

- Product documentation (SAM, licence metrics, reconciliation) — <https://www.servicenow.com/docs/search?q=software+asset+management> (read 2026-11-04)
- Now Create Success Pack for SAM/ITAM (phases and prerequisites) — <https://learning.servicenow.com/lxp> search "Now Create" (read 2026-11-04)
- Now Learning: ITAM/SAM courses (CIS-ITAM path) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Community (audit stories and reconciliation gotchas) — <https://community.servicenow.com/> (read 2026-11-04)
- Now Support KB (reconciliation/normalisation errors) — <https://support.servicenow.com/now> (read 2026-11-04)

> Cultural note: a number you cannot defend is worse than no number. "We cover 20% of the
> estate and here is the gap" is a credible statement; "we are 97% compliant" with partial
> discovery is how organisations fail audits and lose trust.
