# Experimental SAM Guidance — learning science, personas, formats & mnemonics

**Author:** `kilo-sam-deepdive__kilo__cli` · **Date:** 2026-11-13
**Stamp:** 2026-11-13T15:44:29Z · **run-id:** `4178ec70-e3f5-4bc9-a0ab-9c7cdb2acf25`
**Status:** experimental add-on — designed to sit in collapsible (`<details>`) sections at the bottom of the SAM learning material

---

## ELI5 — why this exists

People learn differently, and one long page cannot serve everyone. This section is a *toolbox*: pick the tool that matches how you learn best. Everything here collapses by default so it never clutters the main guide; click a lightbulb to open the trick you want.

---

## 1. Learning best practices (evidence-informed)

| Technique | What it is | How to apply it to SAM |
|---|---|---|
| **Retrieval practice** | Test yourself instead of re-reading | Close the guide and redraw the pipeline from memory; answer the quiz without peeking |
| **Spaced repetition** | Review at increasing intervals | Day 1 / 3 / 7 / 14 flashcard reviews of record types, statuses, properties |
| **Dual coding** | Combine words + visuals | Pair every concept with its diagram (pipeline, IRE flow, state machine) |
| **Interleaving** | Mix topics instead of blocking | Alternate normalization, entitlements and reconciliation drills in one session |
| **Elaboration** | Explain *why* in your own words | For each status transition, say why it happens out loud |
| **Concrete examples** | Anchor abstractions in cases | Always work a named example (e.g., "Office16 ProPlus") not a generic "software" |
| **Cognitive load management** | Chunk; remove redundancy | Learn one record type per session; hide advanced sections until needed |
| **Deliberate practice** | Target weak spots with feedback | Drill the exact tables/queries you keep forgetting |
| **Feynman technique** | Teach a beginner | Explain reconciliation to a colleague in 5 sentences |
| **Andragogy (adult learning)** | Problem-centred, experience-based, self-directed | Start from a real audit/true-up problem you own, not chapter 1 |

> Note: "learning styles" (VARK) as a fixed trait is **not supported by evidence**. Use *multiple formats* because everyone benefits from variety, not because "you are a visual learner".

---

## 2. Paths by persona

| Persona | Goal | Suggested route |
|---|---|---|
| **SAM Administrator** | Run daily operations | Pipeline → normalization statuses → reconcile → License Workbench → removal candidates → health check |
| **SAM Developer / Integrator** | Automate and extend | Business rule contract → IRE REST integration → dedup rules → properties → audit recipe |
| **License Manager / Auditor** | Defend compliance | Entitlements → license types → true-up → publisher traps → evidence chain |
| **ITAM Manager / Procurement** | Govern and optimize | Maturity stages → success goals → reclamation → renewals → savings reporting |
| **Executive sponsor** | Understand value | Purpose → compliance positions → KPI targets → pilot gates |

---

## 3. Alternative guidance formats

1. **Flashcard deck (Anki-style)** — front: term; back: definition + one example + source table.
2. **One-page cheat sheet** — record types, statuses, jobs, roles, top 5 properties.
3. **Scenario drills** — "Entitlement qty = 1, installs = 3 → expected shortfall?" style.
4. **Teach-back script** — 5-sentence explanations per core concept.
5. **Video storyboard** — screen-walkthrough script with timestamps and callouts.
6. **Audio/podcast notes** — 10-minute spoken summaries per theme for commute learning.
7. **Infographic** — single-page pipeline + decision flow (see §5).
8. **Lab checklist** — hands-on steps with expected observations at each step.
9. **Quiz variants** — MCQ, ordering ("put the pipeline in order"), matching (term ↔ table), true/false with corrections.

---

## 4. Key-term mnemonics (click each lightbulb)

<details>
<summary>💡 Pipeline order — "DIN MERR²"</summary>

**D**iscover → **I**nstall record created → **N**ormalize discovery model → **M**atch software model → **E**ntitle the rights → **R**econcile → **R**eclaim unused → **R**enew.

Say it as: "*Discover, Install, Normalize, Match, Entitle, Reconcile, Reclaim, Renew*" — the three R's are results, recovery, renewal.
</details>

<details>
<summary>💡 Record types — "MIES R"</summary>

- **M**odel = what it **is** (canonical product)
- **I**nstallation = what **exists**
- **E**ntitlement = what you may **use**
- **S**ubscription = what you're **assigned** (SaaS)
- **R**econciliation = the **difference**

Sentence: "*The Model says what it is; the Install says what exists; the Entitlement says what you may use.*"
</details>

<details>
<summary>💡 Normalization statuses — "NN PP MM"</summary>

- **N**ew / **N**ormalized
- **P**artially Normalized / **P**ublisher Normalized
- **M**atch Not Found / **M**anually Normalized

Fully automatic statuses: Normalized, Partially, Publisher. Operator-owned: New, Match Not Found, Manually Normalized. Pattern-normalized is locked like manual.
</details>

<details>
<summary>💡 Roles — "AUDIS"</summary>

- **A**dmin — full control
- **U**ser — daily operations
- **D**eveloper — scripts/integrations
- **I**ntegrator — SaaS profiles
- **S**pend import — financial transactions

Admin ⊃ User; Developer ⊃ Admin (dangerous, restrict); Integrator and Spend Import are special-purpose.
</details>

<details>
<summary>💡 Go-live properties — "APEX"</summary>

- **A**uto-create software models → OFF during Crawl
- **P**ublished products → phase-wise scope
- **E**xclude-device flag → set before first reconciliation
- Con**X**? No — remember **X** = the unknown you must clear: normalization backlog + recon grouping.

Expanded: **A**uto-create off · **P**ublished scope · **E**xclude flag · recon grou**X**/subgroup.
</details>

<details>
<summary>💡 IRE four rules — "I D R R" (I Really Do Reconcile)</summary>

- **I**dentification — does the CI exist?
- **D**ata Source Rule — may this source insert it?
- **R**econciliation — which source may update which attribute?
- **R**efresh (Data Refresh) — is the winner stale?

Order of application: Identify → (match: Reconcile → Refresh) / (no match: Data Source gate).
</details>

<details>
<summary>💡 Compliance truth — "UNC"</summary>

- **U**nknown is **N**ever **C**ompliant.

Unlicensed installs and rights-needed are the exposure signals; report them explicitly.
</details>

<details>
<summary>💡 License types — "PPS MUSAF"</summary>

- **P**erpetual
- **P**erpetual + **S**oftware Assurance (Microsoft)
- **S**ubscription
- **M**aintenance (non-Microsoft; link to perpetual!)
- **U**pgrade / **S**tep-up (edition moves)
- **A**dd-on / **F**rom SA (Microsoft 365 transitions)

Maintenance and SA alone are **not** reconciled unless linked to a base perpetual licence.
</details>

<details>
<summary>💡 Reclamation — "60–90 Silent Days"</summary>

Never reclaim on one night of data. Require **60–90 days** of sustained inactivity plus business-owner sign-off. Rule types: Total Usage Time, Last Used Date (also Peak Concurrent Usage, Active Transaction Codes). Usage evidence lives in `samp_sw_usage`.
</details>

<details>
<summary>💡 True-up — "Least Rights × Price"</summary>

True-up cost = **least number of rights needed** × price per right. If no licence cost on the model, the system falls back to the **average entitlement cost** — verify that fallback or the number lies.
</details>

<details>
<summary>💡 Insert/update — "Identify First, Gate Inserts"</summary>

Reconciliation never gates inserts; IRE Data Source Rules do. Blocked insert = `INSERT_NOT_ALLOWED_FOR_SOURCE`. Specific-attribute rules beat all-attributes rules regardless of priority. Priority: lower number wins.
</details>

---

## 5. Infographic concept (for the SVG asset)

One canvas, left-to-right pipeline:

```
[Discovery/SCCM/SaaS] → cmdb_sam_sw_install → cmdb_sam_sw_discovery_model
   → (normalize) → cmdb_software_product_model ← alm_license (entitlements)
   → reconciliation (weekly) → License Position / LMR results
   → remediation: allocations · remove installs · POs
   → reclamation (60–90 days) → savings → renewals
```

Four IRE pillars float above as decision gates; UNC/APEX callouts sit below.

---

*Experimental section — safe to hide behind `<details>`; mnemonics are memory aids, not documentation.*
