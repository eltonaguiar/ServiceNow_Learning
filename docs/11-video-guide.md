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

## Part C — Material other agents dropped (checked 2026-11-04)

Reviewed both repositories and every branch: **no video files and no specific video URLs exist
yet.** What is there is useful preparation, so it is linked rather than duplicated:

| Agent | What it actually is | Link |
|---|---|---|
| KiloCode | SAM video learning path, 8 items, titles + provider + length, no URLs | <https://github.com/eltonaguiar/ServiceNow_Learning_SAM/blob/main/KiloCode/docs/video-guide-getting-started.md> |
| opencode | 25–30 min recording script, scene by scene | <https://github.com/eltonaguiar/ServiceNow_Learning_SAM/blob/main/opencode/guides/courses/video-guide-getting-started.md> |
| opencode | Slide deck companion to that recording | <https://github.com/eltonaguiar/ServiceNow_Learning_SAM/blob/main/opencode/guides/courses/video-slides.md> |
| Kilo (learning repo) | Course ordering with YouTube search links | <https://github.com/eltonaguiar/ServiceNow_Learning/blob/main/docs/courses/top-servicenow-learning-courses-order.md> |

Two honest observations: a video *path* without links is a reading list, and a recording
*script* is not a video. Both are worth keeping — they are the input to the recording described
in Part B — but neither should be presented to a beginner as "the video".

> Provenance note: this material has since been merged into `main` on both repositories, so the
> links above are stable rather than branch-dependent.

---

## Part D — Watch the generated version (the one that exists today)

**`video/getting-started.mp4`** — 4:35, 1280×720, H.264/AAC, burned-in captions, with
`video/getting-started.vtt` beside it.

- **What it is:** the eight-scene script above, rendered as an animated walkthrough — a
  stylised ServiceNow screen, a cursor that travels to each target, a highlight ring that holds
  on the element being described, and burned-in captions. Generated by
  `scripts/build_video.py` (ffmpeg + espeak-ng + PIL). Deterministic: re-run it and you get the
  same file.
- **What it is not:** a screencast of a live instance. There is no ServiceNow instance in this
  repository to record, so the screen is drawn, not captured. Every frame carries that in the
  footer, and each scene's "ON YOUR INSTANCE" block is the real instruction.
- **Beats are fractions of scene audio**, not absolute seconds, so re-wording a line moves the
  cursor with it instead of leaving it pointing at nothing.
- **Why 4:35 and not 8:00:** speech runs faster than a human demo with pauses. The eight
  minutes in Part B remains the target for *your* screencast; this file rehearses the words.
- **Rebuild:** `python3 scripts/build_video.py` (needs `ffmpeg`, `ffprobe`, `espeak-ng`).

Edit `SCENES` in `scripts/build_video.py` to change narration; the captions regenerate with it.

---

## Part E — Verified official videos by topic (checked 2026-11-04)

**All 8 SAM topics resolve to a ServiceNow-owned video, and every link was verified through
YouTube's oEmbed endpoint** — which returns the real title and channel, so a dead or
re-uploaded video fails rather than 404s quietly.

| SAM topic | Verified official video | What it actually is |
|---|---|---|
| ServiceNow Fundamentals | [What is ServiceNow & Where Do I Fit? (ServiceNow Foundations #1)](https://www.youtube.com/watch?v=XErEM1jLxeU) | teaching series (#1 of 6) |
| ServiceNow Administration Fundamentals | [How Do I Get Started Building on ServiceNow? (ServiceNow Foundations #2)](https://www.youtube.com/watch?v=HPCTwBFvgBc) | teaching series (#2 of 6) — the closest official material to admin basics |
| SAM overview | [What's New In IT Asset Management With Now Platform San Diego Release \| Knowledge 2022](https://www.youtube.com/watch?v=rTWFbjAcQ7Q) | conference keynote (Knowledge 2022), feature tour |
| Hardware Asset Management overview | [What's New In IT Asset Management With Now Platform San Diego Release \| Knowledge 2022](https://www.youtube.com/watch?v=rTWFbjAcQ7Q) | same keynote — no separate HAM video exists |
| Software license management | [Presidio helps SouthState Bank improve audit readiness and software asset visibility with ServiceNow](https://www.youtube.com/watch?v=UZRehk5SqIU) | customer story, not a how-to |
| Procurement and contract management | [Put AI to work in procurement](https://www.youtube.com/watch?v=KlqbDTaq7Ns) | product/marketing |
| CMDB fundamentals | [How does ServiceNow Model Your Data? (ServiceNow Foundations #4)](https://www.youtube.com/watch?v=TTIcvlp4XNs) | teaching series (#4 of 6) — data model and CMDB |
| IntegrationHub and Discovery | [IntegrationHub Overview - Learn Integrations on the Now Platform](https://www.youtube.com/watch?v=RO707H-b5iY) | teaching series — Integrations on the Now Platform |

**Read the right-hand column before you press play.** Four of these are genuine teaching
material: the *ServiceNow Foundations* series (#1, #2, #4) and *IntegrationHub Overview*. The
other four are not instruction — a Knowledge keynote, one customer story, and a
procurement-marketing clip. ServiceNow does not publish SAM tutorials on its public channels;
that content lives in Now Learning course lessons, which is why
[`10-course-path.md`](10-course-path.md) is still the primary path and this table is the
supplement.

### How the table is produced and kept honest

`scripts/find_videos.py` searches **inside** each official channel through the YouTube Data
API (`channelId` scoped — a global search returns third-party creators first, which is how an
earlier pass found nothing for Fundamentals or CMDB), then pins each result by a substring of
its real title. Two failure modes are handled deliberately:

- **No key, no guessing.** Without `YOUTUBE_API_KEY`/`YOUTUBE_API_V3_KEY` the script falls
  back to parsing channel search pages and will report a topic as unresolved rather than invent
  an id.
- **No silent drift.** `python3 scripts/find_videos.py --verify` re-checks published links only
  — no search, no writes — and fails if a video is gone or its title changed. CI runs exactly
  that, so a dead video breaks the build instead of the reader's trust.

`python3 scripts/find_videos.py --report` prints the table above from
`data/video_links.json`; the doc is generated from that file, so they cannot disagree.

## Part C — Material other agents dropped (checked 2026-11-04)

Reviewed both repositories and every branch: **no video files and no specific video URLs exist
yet.** What is there is useful preparation, so it is linked rather than duplicated:

| Agent | What it actually is | Link |
|---|---|---|
| KiloCode | SAM video learning path, 8 items, titles + provider + length, no URLs | <https://github.com/eltonaguiar/ServiceNow_Learning_SAM/blob/main/KiloCode/docs/video-guide-getting-started.md> |
| opencode | 25–30 min recording script, scene by scene | <https://github.com/eltonaguiar/ServiceNow_Learning_SAM/blob/main/opencode/guides/courses/video-guide-getting-started.md> |
| opencode | Slide deck companion to that recording | <https://github.com/eltonaguiar/ServiceNow_Learning_SAM/blob/main/opencode/guides/courses/video-slides.md> |
| Kilo (learning repo) | Course ordering with YouTube search links | <https://github.com/eltonaguiar/ServiceNow_Learning/blob/main/docs/courses/top-servicenow-learning-courses-order.md> |

Two honest observations: a video *path* without links is a reading list, and a recording
*script* is not a video. Both are worth keeping — they are the input to the recording described
in Part B — but neither should be presented to a beginner as "the video".

> Provenance note: this material has since been merged into `main` on both repositories, so the
> links above are stable rather than branch-dependent.

---

## Part D — Watch the generated version (the one that exists today)

**`video/getting-started.mp4`** — 4:35, 1280×720, H.264/AAC, burned-in captions, with
`video/getting-started.vtt` beside it.

- **What it is:** the eight-scene script above, rendered as an animated walkthrough — a
  stylised ServiceNow screen, a cursor that travels to each target, a highlight ring that holds
  on the element being described, and burned-in captions. Generated by
  `scripts/build_video.py` (ffmpeg + espeak-ng + PIL). Deterministic: re-run it and you get the
  same file.
- **What it is not:** a screencast of a live instance. There is no ServiceNow instance in this
  repository to record, so the screen is drawn, not captured. Every frame carries that in the
  footer, and each scene's "ON YOUR INSTANCE" block is the real instruction.
- **Beats are fractions of scene audio**, not absolute seconds, so re-wording a line moves the
  cursor with it instead of leaving it pointing at nothing.
- **Why 4:35 and not 8:00:** speech runs faster than a human demo with pauses. The eight
  minutes in Part B remains the target for *your* screencast; this file rehearses the words.
- **Rebuild:** `python3 scripts/build_video.py` (needs `ffmpeg`, `ffprobe`, `espeak-ng`).

Edit `SCENES` in `scripts/build_video.py` to change narration; the captions regenerate with it.

---

## Part E — Verified official videos by topic (checked 2026-11-04)

`scripts/find_videos.py` resolves a topic to a video by searching the official channel, then
**verifying every candidate through YouTube's oEmbed endpoint** — which returns the real title
and channel. Anything not authored by a ServiceNow channel is dropped rather than guessed.
`python3 scripts/find_videos.py --report` prints the table from `data/video_links.json`.

**5 of 8 topics resolved.** Read the type column before you press play — these are not a
beginner curriculum:

| SAM topic | Verified video | Type |
|---|---|---|
| SAM overview | [What's New In IT Asset Management (Knowledge 2022)](https://www.youtube.com/watch?v=rTWFbjAcQ7Q) | conference keynote, ~feature tour |
| Hardware Asset Management | [same Knowledge 2022 session](https://www.youtube.com/watch?v=rTWFbjAcQ7Q) | no separate HAM video was found |
| Software license management | [Presidio helps SouthState Bank improve audit readiness](https://www.youtube.com/watch?v=UZRehk5SqIU) | customer story, not a how-to |
| Procurement and contract management | [Put AI to work in procurement](https://www.youtube.com/watch?v=KlqbDTaq7Ns) | product/marketing |
| IntegrationHub | [Excel Imports in Integration Hub — Live Coding Happy Hour](https://www.youtube.com/watch?v=_B5m3gcihqI) | developer livestream |
| ServiceNow Fundamentals | _no verified match_ | — |
| Administration Fundamentals | _no verified match_ | — |
| CMDB fundamentals | _no verified match_ | — |

**Why three topics are empty, stated plainly:** topic *search* on YouTube needs the Data API
(an API key), and the web-search provider was unavailable from this environment on 2026-11-04.
Fetching the channel's search page returns channel-promo content rather than query matches, so
the honest output is "not found" rather than a plausible-looking id that 404s.

**What this means for learning:** official *instruction* is not on the public channel, it is in
the **video lessons inside Now Learning courses** — which is exactly why the course path in
[`10-course-path.md`](10-course-path.md) is the primary recommendation and this page is the
supplement. Re-run `find_videos.py` when an API key or search provider is available; it will
fill the gaps without changing any published link.

---

## Official sources

- Now Learning / ServiceNow University (video lessons inside the courses) — <https://learning.servicenow.com/lxp> (read 2026-11-04)
- Product documentation — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Developer portal (PDI and API Explorer used in the demo) — <https://developer.servicenow.com/dev.do> (read 2026-11-04)
- Community (recorded community sessions) — <https://community.servicenow.com/> (read 2026-11-04)

Video channels used above are ServiceNow-owned: `youtube.com/@ServiceNow` and
`youtube.com/@ServiceNowDevProgram`, both verified 2026-11-04. Individual video links are
deliberately not hardcoded — they move, and a dead link teaches nothing.
