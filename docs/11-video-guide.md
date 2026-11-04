# 11 — Video guide: what to watch, and the 8-minute video to record

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

Two parts:

- **Part A** — official video to watch, in order, with one action per video.
- **Part B** — an 8-minute "getting started" video you record yourself on your own PDI.
  Scripted scene by scene, with narration. Recording it is the fastest way to find out what
  you do not actually understand.

---

## Part A — Official video, in the order that works

Only ServiceNow's own channels and Now Learning. Both channels verified as ServiceNow-owned
on 2026-11-04; video titles change, so search the term rather than trusting a link to a
specific video.

| # | Source | Search / where | Watch for | Do this right after |
|---|---|---|---|---|
| 1 | **ServiceNow** (YouTube, `@ServiceNow`) | "ServiceNow platform overview" | The vocabulary: what the platform *is* before how to click it | Write 5 nouns you heard (table, form, flow…) |
| 2 | **Now Learning** (`learning.servicenow.com`) | **ServiceNow Fundamentals** — the video lessons | Navigation, tables, forms, lists, roles | [`LAB-00-ORIENTATION.md`](../labs/LAB-00-ORIENTATION.md) |
| 3 | **ServiceNow Dev Program** (YouTube, `@ServiceNowDevProgram`) | "Flow Designer" walkthroughs | Trigger → action → output, and how a run is inspected | Find one OOB flow in your instance and read it |
| 4 | **Now Learning** | **ServiceNow Administration Fundamentals** video lessons | Users, groups, imports, update sets | [`LAB-04-FOUNDATION-DATA.md`](../labs/LAB-04-FOUNDATION-DATA.md) |
| 5 | **ServiceNow Dev Program** | "REST" / "IntegrationHub" sessions | A live call, the response body, and the error path | [`LAB-01-REST-MESSAGE.md`](../labs/LAB-01-REST-MESSAGE.md) |
| 6 | **ServiceNow** (YouTube) | knowledge/keynote sessions for your product area | How customers describe outcomes — useful for framing, not for config | Note one outcome you could measure |

**Rule:** never watch two of these back to back. Video without a lab is entertainment; the
action column is the actual course.

### The one thing to skip

Long "full course" compilations. They feel efficient and leave no artifact. A 20-minute
walkthrough plus the lab beats a 6-hour playlist every time.

---

## Part B — The 8-minute getting-started video (record it yourself)

**Why record instead of just watching?** Because you cannot narrate a table relationship you
do not understand. The recording is the *Prove* and *Teach* gates of the loop in one artifact.

**Setup (5 minutes before recording)**

- PDI logged in as admin, browser at 1080p, one tab only
- Demo data present (or your foundation set from Lab 04)
- Screen recorder ready (any recorder; OBS, QuickTime, Game Bar, Loom — no preference)
- Mic level tested: say "ServiceNow, one platform, many costumes" and listen back
- Close Slack/email. Every notification you leave in will be in the video forever

### Storyboard

| Time | On screen | Say (roughly) |
|---|---|---|
| **0:00–0:45** | Login page → dashboard | "This is ServiceNow: one platform, many costumes. ITSM, HR, security, field service — same machine, different records. In eight minutes I'll show you the machine, not a tour of menus." |
| **0:45–1:45** | Filter navigator → type `incident` → open a list → open one record | "Everything you see is a record in a table. This is the incident table. A list is many records; a form is one. Left is navigation, top is where you are." |
| **1:45–2:30** | Scroll to related lists on the form | "These are related lists — other tables filtered to this record. Task SLA is the promise, approvers are who can block, work notes are the history." |
| **2:30–3:15** | Right-click header → Configure → Form Layout; then Tables & Columns → `incident` → Columns | "Fields are configuration, not code. Here's the form layout. And here's the same field in the dictionary — that's where 'mandatory' actually lives." |
| **3:15–4:15** | Users → one user with department/location/manager; Groups; Schedules | "Under every module is foundation data: people, places, groups, and the clock. An incident with no caller and no group isn't broken — it's missing the layer underneath." |
| **4:15–5:15** | Create an incident as a non-admin (impersonate), then switch back as agent, assign group, resolve | "I'll raise this as the requester. Notice what they can see. Back as an agent: I assign a group, work it, resolve. One process, two personas." |
| **5:15–6:00** | Task SLA related list | "The SLA record is live: started, and it will pause if the state pauses. That's the difference between a promise and a field." |
| **6:00–6:45** | Flow Designer → open one OOB flow | "Automation lives here. Trigger, conditions, actions. Read one out loud before you build one — most 'requirements' are already a flow." |
| **6:45–7:30** | REST Message → Test → response body; then System Logs → Outbound HTTP Requests | "Integrations are a request, a body, a status code, and a record. Test it outside first, then check the outbound log before blaming the other system." |
| **7:30–8:00** | Course list from [`10-course-path.md`](10-course-path.md) | "If you're starting: Fundamentals, then the admin course, then CSA. Automation before scripting. And do the lab — a course without a lab teaches recognition, not skill." |

### Delivery notes

- One idea per scene. If a scene needs two sentences of apology, cut it.
- Say the table name out loud every time you open a list — it fixes the vocabulary.
- Leave the mistake in: click the wrong menu, recover, and say what told you it was wrong.
  That 10 seconds is worth more than a perfect take.
- 8 minutes is a limit, not a target. Six tight minutes beats ten loose ones.

### After you record

- [ ] Watch it once with the sound off: is the on-screen action legible?
- [ ] Watch it once with your eyes closed: does the narration alone make sense?
- [ ] Caption it (auto-captions are fine; fix the table names)
- [ ] Post it in your team channel — teaching is the last gate, and this is how you close it
- [ ] Re-record in 90 days; the diff in what you explain is your progress

---

## Official sources

- Now Learning / ServiceNow University (video lessons inside the courses) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Product documentation — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Developer portal (PDI and API Explorer used in the demo) — <https://developer.servicenow.com/dev.do> (read 2026-11-04)
- Community (recorded community sessions) — <https://community.servicenow.com/> (read 2026-11-04)

Video channels used above are ServiceNow-owned: `youtube.com/@ServiceNow` and
`youtube.com/@ServiceNowDevProgram`, both verified 2026-11-04. Individual video links are
deliberately not hardcoded — they move, and a dead link teaches nothing.
