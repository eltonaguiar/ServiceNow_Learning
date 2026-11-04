# 02 — Success Packs: the official shortcut everyone skips

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

**What they are.** Now Create's Success Packs are ServiceNow's own implementation packages
for a product: process guides, starter stories, implementation insights, architecture
blueprints, prerequisites, and a recommended sequence. They are the closest thing to
official "how to implement this correctly" documentation.

**Where they live.** Now Create, reached through Now Learning / ServiceNow University —
search **"Now Create"** at <https://learning.servicenow.com/lxp>. (The
`nowcreate.servicenow.com` host also exists but wants a partner/customer login; it was not
reachable from the environment that wrote this page, so treat the learning-portal route as
the reliable one.)

**Why it matters more than the docs.** Product docs answer *how do I configure this field*.
A Success Pack answers *what order, what must exist first, and what does done look like* —
which is exactly what a beginner lacks and what causes rebuilds.

---

## The sequencing: Crawl → Walk → Run → Fly

This is Now Create's own phasing. Use it as scope control, not decoration.

| Phase | You are doing | You are NOT doing | Exit test |
|---|---|---|---|
| **Crawl** | One process, one team, one data source, minimal config, manual where needed | Every integration, every edge case, every department | A real user completes the process end-to-end unaided |
| **Walk** | Add the second team/region, automate the top manual step, start measuring | Full self-service, all reports | The metric you promised moves in the right direction |
| **Run** | Scale to the org, integrations in place, governance cadence | Optimisation theatre | Operating without the implementation team in the room |
| **Fly** | Optimise, automate the long tail, predictive/AI features | Greenfield rewrites | The process improves without a project |

Most failed implementations are a **Fly-shaped design delivered as a Crawl-skinned
deployment**. The Success Pack tells you where you actually are.

---

## How to read a Success Pack in 20 minutes

Do this *before* you configure anything, and write the answers down:

1. **Scope statement** (2 min) — which processes are in, and explicitly which are out.
2. **Prerequisites** (5 min) — plugins, entitlements, roles, data readiness, integrations.
   Copy them into your own checklist; this is the list that saves you.
3. **Phases and deliverables** (5 min) — what each phase produces. Compare to your reality.
4. **Acceptance criteria / success measures** (5 min) — how the pack says you are done. If
   your project has no equivalent, you have no definition of done.
5. **Risks and common pitfalls** (3 min) — usually the same four: data quality, unclear
   ownership, skipping prerequisites, over-scoping phase one.

Then, and only then, open the docs and start Step 1.

---

## Prerequisites by app (what typically bites)

These are the recurring prerequisites across packs. **Verify the exact list for your
release and entitlement in the pack itself** — packs are updated per family release, and
entitlement changes what is available.

### ITSM (Incident / Problem / Change / Request)
- ITSM plugin(s) active; roles (`itil`, plus writer roles per process)
- Assignment groups and at least one support model decision (tiered? pooled?)
- SLA definitions decided before go-live (not after)
- Notification/SMTP path working (or every flow silently fails)
- Knowledge base decision: OOB article states, or you will regret it in week two

### CMDB / ITOM
- CI class model agreed (what a "server" is *here*)
- **Identification rules configured before any data load**
- One discovery source scoped to a pilot
- Data owner per CI class (unowned classes rot)

### SAM / ITAM
- SAM Foundation vs Professional decision (they are not the same product)
- Discovery/connector feed (SCCM, Intune, Jamf, ACC, Service Graph)
- Content library / publisher packs reachable
- **Licence metric decisions in writing** — commercial, not technical
- Contract/PO data for entitlements
Full applied guide: [`08-SAM-SETUP.md`](08-SAM-SETUP.md)

### HRSD
- HR services catalog designed (not one giant "ask HR")
- Confidentiality model (ACLs) designed before data
- COE structure and assignment groups that match the org chart
- Employee data source (HRIS integration or import)

### CSM
- Account/contact data model agreed; entitlement model decided
- Portal branding + external user authentication
- Case types defined (they gate what agents can do)

### Security Operations
- Alert sources and correlation rules (alert ≠ incident)
- SOC tier model and assignment groups
- Threat intel feeds selected; observable tuning plan
- Playbooks chosen per incident category

### FSM
- Territories, skills, and working hours configured (constraints data is the product)
- Mobile app rollout plan (field agents do not use desktop)
- Work order → task → assignment model understood by the business

---

## Pre-flight checklist (paste this into your project doc)

```
[ ] Success Pack read; scope statement copied
[ ] Prerequisites list copied and each item marked have/missing
[ ] Entitlement verified (plugin available, not just "we bought it")
[ ] Roles defined, including one integration user (not a human admin)
[ ] Data owner named per table that will be populated
[ ] Discovery/integration path tested on ONE source, small scope
[ ] Phase-one scope fits Crawl (one team, one process)
[ ] Acceptance criteria written in measurable terms
[ ] Rollback decision: what we turn off if phase one fails
```

If three or more boxes are unchecked, the honest answer is "not ready to configure", and
the next hour belongs to prerequisites, not to forms.

---

## Anti-patterns

- **Reading the pack after building.** Then it becomes a list of things you did wrong.
- **Copying the pack's full scope into phase one.** The pack phases exist because the full
  scope does not fit in one release.
- **Treating "prerequisite" as "nice to have".** Every one of them has a failure mode that
  surfaces at go-live, in front of users.
- **Assuming your PDI contains the app.** PDIs are not entitled for everything; check
  before you plan a lab around a licensed product.

---

## Official sources

- Now Create (Success Packs) via Now Learning — <https://learning.servicenow.com/lxp> search "Now Create" (read 2026-11-04)
- Product documentation — <https://www.servicenow.com/docs/> (read 2026-11-04)
- ServiceNow Store activation notes / entitlements — <https://store.servicenow.com/store> (read 2026-11-04)
- Now Learning courses per app — <https://learning.servicenow.com/lxp> (read 2026-11-04)

> Phasing names (Crawl/Walk/Run/Fly) are Now Create's; this page paraphrases the method and
> does not reproduce pack content.
