# ServiceNow_Learning

**Rapid ServiceNow Learning Methodology (SNRLM)**  
**Agent:** Hermes Agent | **Date:** 2026-11-04 | **Version:** 1.0

---

## Philosophy

ServiceNow is a massive platform. It has thousands of tables, hundreds of modules, and dozens of applications. Trying to learn it "by clicking around" is like trying to drink from a firehose — you'll get soaked but won't stay hydrated.

**The philosophy of this repo:**

> **Learn by doing, not by reading.** Break every ServiceNow topic into bite-sized pieces. Translate jargon into plain English (ELI5). Map every breadcrumb — exactly where to click in the UI. Build working labs, not just theory. Generate visual summaries for memory retention.

We believe:
- **Concepts stick faster when you build them** — not just read about them
- **Breadcrumbs matter** — knowing exactly which menu to click saves hours of hunting
- **CRITICAL vs. MANDATORY vs. OPTIONAL** — not every field needs to be filled; know which ones break things if you skip them
- **Common mistakes are shortcuts** — learn from others' errors before you make them
- **Visuals aid retention** — infographics help you remember what you learned

---

## The Entire Point

This repo exists to answer one question:

> **"I need to learn [ServiceNow topic] quickly — what do I actually need to know, where do I click, and what do I build to prove I understand it?"**

Whether you're:
- A new admin trying to understand Incident Management
- A developer building a REST Message integration
- A student preparing for a ServiceNow certification
- A team lead creating onboarding material

…this methodology gives you a repeatable, 7-step system to go from "I've never heard of this" to "I built a working lab" in the shortest time possible.

---

## The SNRLM 7-Step Cycle

| Step | What You Do | Output |
|------|-------------|--------|
| 1. Decompose | Break the topic into: what it is, what problem it solves, where it lives, who uses it, key components | Topic breakdown |
| 2. ELI5 | Translate into plain English with analogies | ELI5 explanation |
| 3. Breadcrumbs | Map exact click path in ServiceNow UI | Navigation map |
| 4. Classify | Label every field CRITICAL / MANDATORY / OPTIONAL | Field classification |
| 5. Mistakes | List top 5 beginner mistakes + how to avoid | Mistake avoidance guide |
| 6. Lab | Build a hands-on exercise with a working result | Practical lab |
| 7. Infographic | Generate a one-page visual summary | Visual cheat sheet |

---

## Repository Structure

```
ServiceNow_Learning/
├── README.md                          # This file — philosophy and overview
├── methodology/
│   ├── SNRLM_METHODOLOGY.md           # Full 7-step methodology
│   ├── ELI5_GLOSSARY.md               # Plain-English ServiceNow terminology
│   ├── SUCCESS_PACKS_PREREQS.md       # Success Pack prerequisites & installation
│   └── OUT_OF_BOX_FEATURES.md         # Guided setup, workflows, integrations, playbooks, metrics, dashboards
├── generators/
│   ├── generate_learning_path.py      # Auto-generate a learning path for any topic
│   ├── generate_lab.py                # Auto-generate hands-on labs
│   └── generate_infographic.py        # Auto-generate SVG/HTML infographics
├── scripts/
│   ├── ai_agent_prompts/              # Reusable prompts for AI agents
│   │   ├── concept_summary_prompt.md
│   │   ├── lab_builder_prompt.md
│   │   └── infographic_prompt.md
│   ├── rest_message_lab.py            # Practical REST Message integration lab
│   └── remote_table_lab.py            # Practical Remote Table lab
├── labs/
│   ├── rest_message_integration/      # Lab: Build a working REST Message integration
│   └── remote_table/                  # Lab: Build a practical Remote Table
├── templates/
│   ├── learning_path_template.md      # Template for topic guides
│   ├── lab_template.md                # Template for hands-on labs
│   └── infographic_template.html      # Template for visual summaries
└── infographics/
    └── (generated SVG/HTML files)
```

---

## Quick Start

### For Learners (Humans)
1. Pick a ServiceNow topic (e.g., "REST Message Integration")
2. Read the ELI5 glossary for terms you don't know
3. Follow the 7-step cycle in `methodology/SNRLM_METHODOLOGY.md`
4. Build a lab from `labs/` to practice
5. Generate an infographic for quick reference

### For AI Agents
1. Use prompts in `scripts/ai_agent_prompts/` to generate learning content
2. Use `generators/` scripts to auto-create labs and infographics
3. Each prompt is designed to produce beginner-friendly, ELI5 content

---

## Example: Learning REST Message Integration

**Topic:** REST Message Integration  
**Time to learn:** ~2 hours with this methodology vs. ~8 hours without

**The 7 steps:**
1. **Decompose:** REST Message = ServiceNow calling an external API over HTTP
2. **ELI5:** "ServiceNow sends a text message to another computer and waits for a reply"
3. **Breadcrumbs:** `System Web Services > Outbound > REST Messages > New`
4. **Classify:** Endpoint (CRITICAL), HTTP Method (CRITICAL), Authentication (MANDATORY), Headers (OPTIONAL)
5. **Mistakes:** Forgetting to set the HTTP method, wrong auth type, not testing the connection
6. **Lab:** Build a REST Message that fetches weather data and creates an Incident with the temperature
7. **Infographic:** One-page diagram showing the request → response flow

**Lab:** See `labs/rest_message_integration/` for the complete hands-on exercise.

---

## Contributing

This is a methodology repo — contributions should follow the SNRLM 7-step cycle:

1. Pick a ServiceNow topic
2. Create a folder under `labs/` or `methodology/`
3. Follow the 7-step cycle
4. Include ELI5 explanations
5. Include breadcrumb maps
6. Include a practical lab
7. Include an infographic

Open a PR with your addition.

---

## License

MIT — Use this methodology to learn, teach, or build your own ServiceNow training materials.
