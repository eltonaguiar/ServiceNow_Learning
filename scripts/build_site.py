#!/usr/bin/env python3
"""build_site.py — generate the GitHub Pages landing pages.

    python3 scripts/build_site.py            # writes index.html AND docs/index.html

Two copies on purpose: GitHub Pages may be configured to serve the repository root OR the
/docs folder. A page written for one breaks on the other, so this emits both with links
adjusted. It is a single source of truth (this script) and therefore cannot drift.

The page is self-contained: no CDN, no JS framework, no external fonts. It must render on a
locked-down network, which is where most ServiceNow people actually work.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/eltonaguiar/ServiceNow_Learning"
BRANCH = "buffy-mimo-v2.6-flash-2026-11-04"
UPDATED = "2026-11-04"

# (section, title, path-without-.html-suffix, description, tag)
PAGES = [
    ("Start here", "ELI5: ServiceNow for beginners", "docs/01-ELI5",
     "The building-and-filing-cabinet analogy, a 30-minute first session, and a glossary that defines every term before it is used.", "guide"),
    ("Start here", "Video guide: watch, then record", "docs/11-video-guide",
     "Official channels in order, then an eight-minute getting-started video scripted scene by scene for you to record on your own instance.", "start"),
    ("Start here", "The full course path", "docs/10-course-path",
     "Every stage from orientation to CSA to one CIS, with what to do alongside each course and a ten-hour minimum path.", "start"),
    ("Start here", "Foundation data: the layer everyone skips", "docs/09-foundation-data",
     "Companies, locations, departments, cost centres, users, groups, business hours — the objects every module assumes exist, in dependency order.", "start"),
    ("Start here", "The rapid-learning methodology", "docs/00-methodology",
     "Five gates in 95 minutes: orient, model, practise, prove, teach. Why that order, and what each gate must produce.", "method"),
    ("Start here", "Official sources only", "docs/00-methodology#4-source-ladder--official-first-always",
     "Docs, Now Create, Now Learning, Developer PDI, Community, Store, Support — and the ToS rules that keep you out of trouble.", "sources"),

    ("Guides", "Success Packs and prerequisites", "docs/02-success-packs",
     "Now Create's Crawl → Walk → Run → Fly sequencing, how to read a pack in 20 minutes, and per-app prerequisites that actually bite.", "guide"),
    ("Guides", "Breadcrumbs: where things live", "docs/03-breadcrumbs",
     "The 12 bookmarks that cover most work, plus exact paths per module — with the table name, because menus move.", "nav"),
    ("Guides", "Mandatory vs useful vs optional fields", "docs/04-fields",
     "Three kinds of 'required', the four related lists worth adding today, and per-table field guidance.", "fields"),
    ("Guides", "Common mistakes by symptom", "docs/05-common-mistakes",
     "Symptom → real cause → fix. Starts with 'it works for me but not for them', ends with the five that waste the most hours.", "fix"),
    ("Guides", "Guided Setup & OOB inventory", "docs/06-inventory",
     "What ships out of the box per app — guided setup, flows, playbooks, spokes, metrics — and how to enumerate yours in five minutes.", "oob"),

    ("Applied: SAM", "SAM setup guide", "docs/08-SAM-SETUP",
     "The applied module: prerequisites, the nine-step build order, field matrix, metrics that lie, and ten mistakes that cost money.", "sam", "start"),
    ("Applied: SAM", "SAM baseline lab", "labs/LAB-03-SAM-BASELINE",
     "Build one defensible compliance number for three titles with three different licence metrics — then break it on purpose.", "sam"),

    ("Labs", "Lab 00 — orientation (30 min)", "labs/LAB-00-ORIENTATION",
     "Zero-risk first session: navigation, forms as records, dictionary-mandatory vs UI-policy-mandatory, impersonation.", "lab"),
    ("Labs", "Lab 01 — REST Message that does something", "labs/LAB-01-REST-MESSAGE",
     "Call a real API, turn the answer into an incident with a dedupe guard, build the inbound direction, then break it five ways.", "lab"),
    ("Labs", "Lab 04 — foundation data, then proof", "labs/LAB-04-FOUNDATION-DATA",
     "Load the smallest foundation set that makes ITSM behave, then break each dependency and watch the module fail without an error message.", "lab"),
    ("Labs", "Lab 02 — practical Remote Table", "labs/LAB-02-REMOTE-TABLE",
     "Expose a REST API as a read-only table, use it in a report, and learn exactly where the illusion breaks.", "lab"),

    ("Toolkit", "The probe (make your instance the truth)", "docs/07-probe",
     "scripts/sn_probe.js reads your instance: mandatory fields, related lists, guided setup, flows, SAM presence. Read-only.", "tool"),
    ("Toolkit", "sn_learn.py — briefs, plans, quizzes", "docs/generated/brief-itsm-incident",
     "Renders a timeboxed study brief per module from the knowledge base. Example output included.", "tool"),
]

# Ordered self-directed curriculum. Kept here (not only in markdown) so the landing page
# shows it above the fold; docs/10-course-path.md carries the rationale and timings.
COURSES = [
    ("0", "Welcome to ServiceNow", "Day 0 · 1–2 h", "docs/01-ELI5", "the vocabulary"),
    ("1", "ServiceNow Fundamentals (free)", "First 10 hours", "labs/LAB-00-ORIENTATION", "Lab 00"),
    ("2", "ServiceNow Administration Fundamentals", "Before any admin work", "docs/09-foundation-data", "foundation data + Lab 04"),
    ("3", "Certified System Administrator (CSA) path + exam", "After 1–2 · gates every CIS", "docs/00-methodology", "the loop, one module at a time"),
    ("4", "Flow Designer Fundamentals", "Before your first script", "docs/06-inventory", "find the OOB flow first"),
    ("5", "Scripting in ServiceNow Fundamentals", "After flows, not before", "labs/LAB-01-REST-MESSAGE", "Lab 01, option B"),
    ("6", "App Engine Studio / Application Development", "When you must build an app", "labs/LAB-02-REMOTE-TABLE", "Lab 02"),
    ("7", "IntegrationHub Fundamentals", "Before any integration", "labs/LAB-01-REST-MESSAGE", "Lab 01 end-to-end"),
    ("8", "Platform / Performance Analytics Fundamentals", "Once there is data worth measuring", "docs/06-inventory", "indicators that matter"),
    ("9", "One CIS only — ITSM, ITAM/SAM, CSM, HRSD, SecOps, FSM, Discovery", "When your role is clear", "docs/08-SAM-SETUP", "the SAM track if that is you"),
]

TAG_COLOR = {
    "start": "#f97316", "guide": "#38bdf8", "method": "#a78bfa", "sources": "#22d3ee",
    "nav": "#4ade80", "fields": "#fbbf24", "fix": "#fb7185", "oob": "#60a5fa",
    "sam": "#f472b6", "lab": "#34d399", "tool": "#94a3b8",
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def page(strip_docs: bool) -> str:
    """Render the landing page.

    strip_docs=True is for docs/index.html: GitHub Pages may serve the /docs folder as the
    site root, in which case "docs/01-ELI5.html" would resolve to /docs/docs/01-ELI5.html.
    The same content, with the segment removed, works in both configurations.
    """

    def ref(path: str) -> str:
        p = path[len("docs/"):] if strip_docs and path.startswith("docs/") else path
        return p + ".html"

    def img(path: str) -> str:
        # docs/index.html sits one level down, so ../infographics/... is correct there
        return ("../" + path) if strip_docs else path

    sections: dict[str, list[tuple]] = {}
    for item in PAGES:
        sections.setdefault(item[0], []).append(item)

    toc_items = []
    for section, items in sections.items():
        make_toc(section, anchor(section), toc_items, ref)

    cards = []
    for section, items in sections.items():
        cards.append(f'<h2 id="{anchor(section)}">{esc(section)}</h2>')
        cards.append('<div class="grid">')
        for item in items:
            section_name, title, path, desc, tag = item[:5]
            tagc = TAG_COLOR.get(tag, "#94a3b8")
            cards.append(
                f'<a class="card" href="{esc(ref(path))}">'
                f'<span class="tag" style="--tag:{tagc}">{esc(tag)}</span>'
                f'<h3>{esc(title)}</h3><p>{esc(desc)}</p></a>'
            )
        cards.append("</div>")

    toc_html = ('<li><a href="#courses"><strong>Courses in order</strong></a></li>\n'
                '<li><a href="#video"><strong>Video guide</strong></a></li>\n' + "\n".join(toc_items))

    course_rows = "\n".join(
        f'<tr><td class="num">{n}</td><td><strong>{esc(title)}</strong></td>'
        f'<td class="when">{esc(when)}</td>'
        f'<td><a href="{esc(ref(path))}">{esc(companion)}</a></td></tr>'
        for n, title, when, path, companion in COURSES)

    course_block = f"""
    <section class="courses">
      <h2 class="sec" id="courses">Self-directed courses — in this order</h2>
      <p>All official: Now Learning / ServiceNow University. The order matters more than the
      list — CSA before any CIS, automation before scripting, measurement after you have
      something worth measuring. Rationale and timings:
      <a href="{esc(ref('docs/10-course-path'))}">the full course path</a>.</p>
      <table>
        <tr><th>#</th><th>Course (search this on Now Learning)</th><th>Take it when</th><th>Do this alongside</th></tr>
        {course_rows}
      </table>
      <p class="fine">Only ten hours? Fundamentals → Lab 00 → the first half of Flow Designer →
      one module brief plus its lab. That is enough to be genuinely useful in a team meeting.</p>

      <h2 class="sec" id="video">Video guide — watch in order, then record eight minutes</h2>
      <p>Official video first (<code>@ServiceNow</code> and <code>@ServiceNowDevProgram</code>,
      plus the video lessons inside the courses above), each paired with one action. Then
      record your own eight-minute getting-started video from the scene-by-scene script in
      <a href="{esc(ref('docs/11-video-guide'))}">docs/11-video-guide.md</a> — narrating a table
      relationship you cannot explain is impossible, which is exactly why it works as a test.</p>

      <h3 class="sub">Watch: generated walkthrough (4:48)</h3>
      <video controls preload="none" width="100%" style="max-width:760px;border-radius:12px;border:1px solid var(--line)"
             src="{esc(img('video/getting-started.mp4'))}">
        Your browser does not support video.
      </video>
      <p class="fine">Narration over slides, built by <code>scripts/build_video.py</code> — not a
      live-instance screencast (there is no instance here to record). Captions:
      <a href="{esc(img('video/getting-started.vtt'))}">getting-started.vtt</a>. Only five of the
      eight SAM topics resolved to a verified ServiceNow-owned video, and what exists is a keynote,
      a customer story and a dev session — the gaps are named, not filled with guesses. See
      <a href="{esc(ref('docs/11-video-guide'))}">docs/11-video-guide.md</a>.</p>

      <h3 class="sub">Video material the other agents dropped</h3>
      <p class="fine">Checked both repositories and all branches on 2026-11-04: there are
      <strong>no video files and no specific video URLs</strong> yet. What exists is preparation —
      linked here, not copied:</p>
      <ul class="agents">
        <li><strong>KiloCode</strong> — curated SAM video path, 8 items, titles only (no URLs):
          <a href="https://github.com/eltonaguiar/ServiceNow_Learning_SAM/blob/main/KiloCode/docs/video-guide-getting-started.md">video-guide-getting-started.md</a></li>
        <li><strong>opencode</strong> — 25–30 minute recording script, scene by scene:
          <a href="https://github.com/eltonaguiar/ServiceNow_Learning_SAM/blob/main/opencode/guides/courses/video-guide-getting-started.md">video script</a> ·
          <a href="https://github.com/eltonaguiar/ServiceNow_Learning_SAM/blob/main/opencode/guides/courses/video-slides.md">slides</a></li>
        <li><strong>Kilo (learning repo)</strong> — course order with YouTube search links:
          <a href="https://github.com/eltonaguiar/ServiceNow_Learning/blob/main/docs/courses/top-servicenow-learning-courses-order.md">top-servicenow-learning-courses-order.md</a></li>
      </ul>
      <p class="fine">A path without links is a reading list; a script is not a video. The only
      ServiceNow-owned channels verified on 2026-11-04 are
      <a href="https://www.youtube.com/@ServiceNow">@ServiceNow</a> and
      <a href="https://www.youtube.com/@ServiceNowDevProgram">@ServiceNowDevProgram</a>.</p>
    </section>
    """
    body = "\n".join(cards)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ServiceNow Learning — rapid, official-source-first</title>
<meta name="description" content="A 95-minute loop for learning any ServiceNow module, with beginner guides, SAM setup, labs and a read-only instance probe.">
<style>
  :root {{ --bg:#0b1120; --panel:#111c33; --ink:#e5ecf7; --muted:#94a3b8; --line:#1f2c47; --accent:#38bdf8; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
         font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  a {{ color:var(--accent); }}
  header {{ padding:56px 24px 28px; border-bottom:1px solid var(--line);
            background:radial-gradient(900px 300px at 15% -10%, #16304f 0%, transparent 70%); }}
  .wrap {{ max-width:1180px; margin:0 auto; }}
  .kicker {{ color:var(--muted); letter-spacing:.14em; text-transform:uppercase; font-size:12px; }}
  h1 {{ font-size:clamp(28px,4vw,44px); margin:10px 0 12px; line-height:1.15; }}
  .lede {{ color:var(--muted); max-width:70ch; margin:0 0 18px; }}
  .pill {{ display:inline-block; border:1px solid var(--line); border-radius:999px;
           padding:4px 12px; margin:0 8px 8px 0; font-size:13px; color:var(--muted); }}
  .layout {{ display:grid; grid-template-columns:260px 1fr; gap:40px; padding:32px 24px 80px; }}
  @media (max-width:900px) {{ .layout {{ grid-template-columns:1fr; }} nav.toc {{ position:static; }} }}
  nav.toc {{ position:sticky; top:24px; align-self:start; border:1px solid var(--line);
             border-radius:14px; padding:18px; background:var(--panel); }}
  nav.toc h2 {{ font-size:13px; text-transform:uppercase; letter-spacing:.12em; color:var(--muted); margin:0 0 10px; }}
  nav.toc ul {{ list-style:none; margin:0; padding:0; }}
  nav.toc li {{ margin:6px 0; font-size:14px; }}
  nav.toc .sub {{ padding-left:12px; border-left:1px solid var(--line); margin:6px 0 12px; }}
  nav.toc .sub li {{ font-size:13px; }}
  h2.sec {{ margin:36px 0 14px; font-size:22px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:14px; }}
  .card {{ display:block; text-decoration:none; color:inherit; background:var(--panel);
           border:1px solid var(--line); border-radius:14px; padding:18px; transition:.15s; }}
  .card:hover {{ border-color:var(--accent); transform:translateY(-2px); }}
  .card h3 {{ margin:8px 0 6px; font-size:16px; color:var(--ink); }}
  .card p {{ margin:0; color:var(--muted); font-size:13.5px; }}
  .tag {{ font-size:11px; text-transform:uppercase; letter-spacing:.08em; color:var(--tag);
          border:1px solid color-mix(in srgb, var(--tag) 45%, transparent); border-radius:6px;
          padding:2px 7px; }}
  .start {{ border-color:#f97316; box-shadow:0 0 0 1px #f97316 inset; }}
  .courses table {{ width:100%; border-collapse:collapse; margin:14px 0 10px; font-size:14px; }}
  .courses th {{ text-align:left; color:var(--muted); font-size:11.5px; text-transform:uppercase;
                 letter-spacing:.06em; padding:8px 10px; border-bottom:1px solid var(--line); }}
  .courses td {{ padding:9px 10px; border-bottom:1px solid var(--line); vertical-align:top; }}
  .courses td.num {{ color:var(--accent); font-weight:700; width:28px; }}
  .courses td.when {{ color:var(--muted); white-space:nowrap; }}
  .courses .fine {{ color:var(--muted); font-size:13px; }}
  .courses h3.sub {{ font-size:15px; margin:22px 0 6px; }}
  .courses ul.agents {{ margin:8px 0 6px; padding-left:20px; font-size:14px; }}
  .courses ul.agents li {{ margin:5px 0; }}
  .figrow {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; padding:26px 24px 0; }}
  @media (max-width:820px) {{ .figrow {{ grid-template-columns:1fr; }} }}
  .figrow a {{ display:block; border:1px solid var(--line); border-radius:14px; overflow:hidden;
               background:var(--panel); }}
  .figrow img {{ display:block; width:100%; height:auto; }}
  footer {{ border-top:1px solid var(--line); padding:26px 24px 60px; color:var(--muted); font-size:14px; }}
  footer a {{ color:var(--accent); }}
  code {{ background:#0f1a2d; padding:1px 6px; border-radius:5px; font-size:13px; }}
</style>
</head>
<body>
<header><div class="wrap">
  <div class="kicker">ServiceNow Learning · agent buffy · mimo-v2.6-flash · {UPDATED}</div>
  <h1>Learn any ServiceNow module in 95 minutes — and prove it</h1>
  <p class="lede">ServiceNow is one platform wearing dozens of costumes. This kit teaches the
  machine once — tables, states, roles, routing, proof — then gives you a timeboxed loop,
  beginner guides, applied SAM setup, hands-on labs, and a read-only probe that turns your
  own instance into the source of truth.</p>
  <span class="pill">Official sources first</span>
  <span class="pill">Crawl → Walk → Run → Fly</span>
  <span class="pill">Built for beginners</span>
  <span class="pill">Read-only probe</span>
</div></header>

<div class="figrow">
  <a href="{esc(img('infographics/learning-loop.svg'))}" title="The 95-minute loop">
    <img src="{esc(img('infographics/learning-loop.svg'))}" alt="The 95-minute learning loop: orient, model, practise, prove, teach">
  </a>
  <a href="{esc(img('infographics/module-anatomy.svg'))}" title="Module anatomy">
    <img src="{esc(img('infographics/module-anatomy.svg'))}" alt="Every module answers the same five questions">
  </a>
</div>

<div class="wrap layout">
  <nav class="toc">
    <h2>Contents</h2>
    <ul>
      {toc_html}
    </ul>
    <h2 style="margin-top:20px">Links</h2>
    <ul>
      <li><a href="{REPO}">GitHub repository</a></li>
      <li><a href="{REPO}/tree/{BRANCH}">This branch</a></li>
      <li><a href="{REPO}/blob/{BRANCH}/README.md">README</a></li>
      <li><a href="{REPO}/issues">Issues / feedback</a></li>
      <li><a href="https://github.com/eltonaguiar/ServiceNow_Learning_SAM">SAM track repository</a></li>
    </ul>
  </nav>

  <main>
    {course_block}
    {body}

    <h2 class="sec" id="how-to-read">How to use this in an afternoon</h2>
    <p>       <strong>1.</strong> Read <a href="{esc(ref('docs/01-ELI5'))}">the ELI5 guide</a> (20 min).
       <strong>2.</strong> Get a free PDI at
       <a href="https://developer.servicenow.com/dev.do">developer.servicenow.com</a> and run
       <a href="{esc(ref('labs/LAB-00-ORIENTATION'))}">Lab 00</a> (30 min).
       <strong>3.</strong> Pick one module, render its brief with
       <code>python3 scripts/sn_learn.py brief itsm-incident</code>, and run the loop.
       <strong>4.</strong> For SAM specifically, start at
       <a href="{esc(ref('docs/08-SAM-SETUP'))}">the SAM setup guide</a>.</p>

    <h2 class="sec" id="honesty">What is verified, and what is not</h2>
    <p>Every guide cites official ServiceNow sources and links out rather than copying them.
    Menu paths, field lists and "does guided setup exist" are marked <em>verify</em> wherever
    they vary by release and entitlement — the probe resolves them against your instance.
    Timeboxes are targets, not measured benchmarks. Nothing here has been executed against a
    licensed SAM instance: the SAM material is documentation-grounded, and the lab says so.</p>
  </main>
</div>

<footer><div class="wrap">
  Built by <strong>buffy</strong> (mimo-v2.6-flash) on branch
  <code>{BRANCH}</code>, {UPDATED}. Content is paraphrased guidance with links to
  <a href="https://www.servicenow.com/docs/">official documentation</a>,
  <a href="https://learning.servicenow.com/lxp">Now Learning / Now Create</a>,
  <a href="https://developer.servicenow.com/dev.do">the developer portal</a> and
  <a href="https://community.servicenow.com/">Community</a>. No ServiceNow content is mirrored here.
  <br>Start here: <a href="{REPO}">github.com/eltonaguiar/ServiceNow_Learning</a>
</div></footer>
</body>
</html>
"""


def anchor(name: str) -> str:
    return name.lower().replace(" ", "-").replace(":", "").replace("&", "and")


def make_toc(section: str, section_anchor: str, out: list[str], ref) -> None:
    out.append(f'<li><a href="#{section_anchor}"><strong>{esc(section)}</strong></a></li>')
    subs = [f'<li><a href="{esc(ref(p))}">{esc(t)}</a></li>'
            for s, t, p, d, *_ in PAGES if s == section]
    out.append('<li><ul class="sub">' + "".join(subs) + "</ul></li>")


def registry_json() -> str:
    return json.dumps(
        [{"section": s, "title": t, "path": p, "description": d, "tag": tag}
         for s, t, p, d, tag, *_ in PAGES],
        indent=2,
    )


def main() -> None:
    root_page = page(strip_docs=False)
    docs_page = page(strip_docs=True)
    (ROOT / "index.html").write_text(root_page, encoding="utf-8")
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(docs_page, encoding="utf-8")
    (ROOT / "data" / "site_registry.json").write_text(registry_json(), encoding="utf-8")
    print(f"wrote index.html and docs/index.html ({len(PAGES)} entries)")


if __name__ == "__main__":
    main()
