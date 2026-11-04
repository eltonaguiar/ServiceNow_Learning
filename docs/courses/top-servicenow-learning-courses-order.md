# Top ServiceNow Learning Courses - Recommended Order

**Agent:** Kilo  
**Date:** 2026-11-04  
**Purpose:** Practical learning path for job readiness (Toronto/Canada market focus)

---

## Learning Philosophy

Follow this order: **Fundamentals → Platform Skills → Role-Specific → Hands-On Labs → Certification Prep**

Focus on **doing over watching**. For every course module, complete the corresponding lab from this repo.

---

## Recommended Learning Path (In Order)

### Phase 1: ServiceNow Fundamentals (Weeks 1-2) - FREE

| Order | Course/Resource | Platform | Cost | Focus | Notes |
|-------|-----------------|----------|------|-------|-------|
| **1** | [ServiceNow Developer Site - Now Learning](https://nowlearning.servicenow.com/) | ServiceNow Now Learning | Free (most content) | Platform basics, navigation, tables, forms, lists | **Start here.** Create a free account. Do all beginner modules. |
| **2** | [ServiceNow Product Documentation](https://docs.servicenow.com/) | ServiceNow Docs | Free | Official docs - always reference these | Use as your go-to reference when stuck. |
| **3** | [ServiceNow Community](https://community.servicenow.com/) | ServiceNow Community | Free | Ask questions, see real solutions | Great for troubleshooting real issues. |

**Goal:** Understand tables, forms, lists, roles, ACLs, Update Sets, Application Navigator.

---

### Phase 2: Platform Development Core (Weeks 2-4) - FREE/PRACTICAL

| Order | Course/Resource | Platform | Cost | Focus | Notes |
|-------|-----------------|----------|------|-------|-------|
| **4** | [Now Learning - Application Development Fundamentals](https://nowlearning.servicenow.com/) | Now Learning | Free | App creation, tables, forms, business rules, client scripts | Search for "Application Development" path. |
| **5** | [Flow Designer Training](https://nowlearning.servicenow.com/) | Now Learning | Free | Modern automation (replaces workflows) | **Critical** - Focus heavily here. |
| **6** | [UI Policies, Data Policies & ACLs](https://nowlearning.servicenow.com/) | Now Learning | Free | Access control & form behavior | Essential for platform roles. |

**Goal:** Build a custom app from scratch. Create flows, business rules, ACLs.

---

### Phase 3: Integrations & Advanced (Weeks 4-6) - FREE

| Order | Course/Resource | Platform | Cost | Focus | Notes |
|-------|-----------------|----------|------|-------|-------|
| **7** | [REST API / Integration Basics](https://nowlearning.servicenow.com/) | Now Learning | Free | REST Messages, REST API Explorer | **Do our lab:** `labs/rest-message-integration/` |
| **8** | [Import Sets & Transform Maps](https://nowlearning.servicenow.com/) | Now Learning | Free | Data loading | Very common in implementations. |
| **9** | [Remote Tables](https://docs.servicenow.com/) | ServiceNow Docs | Free | Display external data live | **Do our lab:** `labs/remote-table/` |
| **10** | [IntegrationHub Basics](https://nowlearning.servicenow.com/) | Now Learning | Free | Spokes, connections, actions | If available in your instance. |

**Goal:** Build working integrations. Understand inbound/outbound patterns.

---

### Phase 4: ITSM + Job-Ready Skills (Weeks 6-8) - PRIORITY FOR TORONTO MARKET

| Order | Course/Resource | Platform | Cost | Focus | Notes |
|-------|-----------------|----------|------|-------|-------|
| **11** | [ITSM Fundamentals](https://nowlearning.servicenow.com/) | Now Learning | Free | Incident, Problem, Change, Request | **Highest demand** in Toronto job market (per our BESTIEJOB data) |
| **12** | [Service Catalog & Service Portal Basics](https://nowlearning.servicenow.com/) | Now Learning | Free | Catalog items, workflows, UI | Common in implementations |
| **13** | [Reporting & Dashboards](https://nowlearning.servicenow.com/) | Now Learning | Free | Reports, Performance Analytics basics | Good to have for BA/Consultant roles |

**Goal:** Be comfortable working in ITSM modules. This matches most ServiceNow job postings.

---

### Phase 5: SAM Focus (If Targeting SAM Roles) - SPECIALIZED

| Order | Course/Resource | Platform | Cost | Focus | Notes |
|-------|-----------------|----------|------|-------|-------|
| **14** | [Software Asset Management (SAM)](https://nowlearning.servicenow.com/) | Now Learning | Free | Software models, entitlements, reconciliation, compliance | Check if available in your learning path |
| **15** | [Hardware Asset Management (HAM)](https://nowlearning.servicenow.com/) | Now Learning | Free | Asset lifecycle, contracts, procurement | Often paired with SAM |
| **16** | [SAM Implementation](https://docs.servicenow.com/) | ServiceNow Docs | Free | Deep dive using our SAM repo materials | Use `ServiceNow_Learning_SAM/KiloCode/` with infographics |

**Goal:** For SAM-specific roles (we see these on BESTIEJOB). Use our infographics-heavy materials.

---

## Certification Path (Optional but Helpful)

| Certification | When to Take | Notes |
|---------------|---------------|-------|
| **CSA (Certified System Administrator)** | After Phases 1-2, solid hands-on practice | Most common entry-level cert. Highly recommended for Toronto market. |
| **CAD (Certified Application Developer)** | After Phases 1-3 with custom app built | Great if targeting developer roles. |
| **CIS - ITSM** | After Phase 4 with ITSM hands-on | Good for ITSM-focused roles. |
| **CIS - SAM** | After Phase 5 if targeting SAM roles | Niche but valuable for SAM positions. |

**Note:** Certification prep is easier if you've done all the hands-on labs. Focus on practical skills first.

---

## Free Practice Resources

| Resource | Purpose | Notes |
|----------|---------|-------|
| [ServiceNow Developer Instance](https://developer.servicenow.com/) | Free personal instance for practice | **Essential.** Get one and use it daily. |
| [Now Learning](https://nowlearning.servicenow.com/) | Official courses & trails | Free account required. Do interactive exercises. |
| [ServiceNow Community](https://community.servicenow.com/) | Solutions, tutorials, Q&A | Great for real-world scenarios. |
| [Our Repos](https://github.com/eltonaguiar) | Our labs, methodologies, SAM materials | Use alongside official courses. |

---

## 90-Day Action Plan

| Days | Focus | Goal |
|------|-------|------|
| **1-14** | Now Learning Fundamentals + Navigation | Comfortable in UI, know tables/forms/roles |
| **15-30** | App Development + Flow Designer | Build a custom app with flows |
| **31-45** | REST Messages + Remote Tables + Labs | Complete both labs from our repo |
| **46-60** | ITSM deep dive + real scenarios | Work through Incident/Change/Request |
| **61-75** | Build portfolio projects | Document 2-3 projects using our concept-summary template |
| **76-90** | Review + Practice + CSA prep if ready | Solid foundation, portfolio ready |

---

## Tips for Toronto Job Market

Based on our BESTIEJOB scans:
- **ITSM roles** are most common (Incident/Change/Request, ITAM/CMDB)
- **ServiceNow Developer/Consultant** roles appear frequently
- **SAM/ITAM** roles exist but less common - good niche to target
- **Focus on Flow Designer, REST APIs, ACLs** - these appear in many postings
- **Hands-on > certs alone** - show your work (GitHub repos with labs)

---

## Final Recommendation

**Minimum viable path for job readiness:**
1. Now Learning Fundamentals (Free)
2. Flow Designer (Free)  
3. ITSM Fundamentals (Free)
4. Do our REST Message lab + Remote Table lab
5. Build 1 custom app end-to-end
6. Document everything in GitHub

**Time investment:** 8-12 hours/week for 90 days will get you interview-ready for junior ServiceNow roles.

---

*Generated by Kilo on 2026-11-04. Part of the ServiceNow_Learning repository at github.com/eltonaguiar/ServiceNow_Learning.*


---

## Video Guide: Getting Started (Step by Step)

### Recommended YouTube Channels & Playlists (Free)

| Channel/Resource | Focus | Notes |
|------------------|-------|-------|
| [ServiceNow](https://www.youtube.com/@ServiceNow) | Official tutorials, product demos, Now Learning highlights | Best for official features and updates |
| [ServiceNow Community](https://www.youtube.com/results?search_query=ServiceNow+Community+tutorial) | Community-led tutorials, real implementations | Great for practical tips from practitioners |
| [Mark Terry](https://www.youtube.com/results?search_query=Mark+Terry+ServiceNow) | Clear, beginner-friendly explanations | Very popular for CSA prep and fundamentals |
| [ServiceNow Ninja](https://www.youtube.com/results?search_query=ServiceNow+Ninja) | Hands-on labs, flow designer, scripting | Great step-by-step walkthroughs |
| [Basico ServiceNow Training](https://www.youtube.com/results?search_query=Basico+ServiceNow) | Comprehensive beginner series | Good structured learning path |

---

### Video Learning Plan (Watch in Order)

| Step | Video Topic to Search | Time | What to Do |
|------|------------------------|------|------------|
| **1. Getting Started** | `ServiceNow introduction for beginners` | 30-45 min | Watch, follow along in your dev instance |
| **2. Navigation & UI** | `ServiceNow application navigator tables forms lists` | 45-60 min | Practice navigating, creating records |
| **3. Tables & Fields** | `ServiceNow tables dictionary fields` | 45-60 min | Create custom table in dev instance |
| **4. Update Sets** | `ServiceNow update sets tutorial` | 20-30 min | Create update set, capture changes |
| **5. Business Rules** | `ServiceNow business rules tutorial` | 45-60 min | Write your first before/after business rule |
| **6. Client Scripts** | `ServiceNow client scripts tutorial` | 45-60 min | Add form validation |
| **7. Flow Designer** | `ServiceNow flow designer tutorial for beginners` | 60-90 min | Build approval flow (most important!) |
| **8. ACLs** | `ServiceNow ACLs tutorial` | 45-60 min | Secure your table |
| **9. REST Message** | `ServiceNow REST Message integration tutorial` | 45-60 min | Follow along, then do our lab |
| **10. ITSM Basics** | `ServiceNow ITSM incident management tutorial` | 60-90 min | Work through full incident lifecycle |

**Total Video Time:** ~8-10 hours of watching + **2-3x practice time** in your dev instance

---

### YouTube Search Queries (Copy/Paste)

Use these exact search terms on YouTube for best results:

```
1. "ServiceNow tutorial for beginners 2024 2025"
2. "ServiceNow CSA certification training free"
3. "ServiceNow Flow Designer tutorial step by step"
4. "ServiceNow REST API tutorial"
5. "ServiceNow ITSM tutorial"
6. "ServiceNow business rules client scripts"
7. "ServiceNow ACL tutorial"
8. "ServiceNow update sets tutorial"
```

---

### Getting Started Checklist with Videos

- [ ] **Day 1:** Get dev instance at [developer.servicenow.com](https://developer.servicenow.com/) + Now Learning account
- [ ] **Watch & Practice:** For each video above, pause and do it in your instance
- [ ] **Take Notes:** Use our `concept-summary-template.md` for each topic
- [ ] **Build Projects:** After learning, build something without following video
- [ ] **Document:** Push your learnings to GitHub
- [ ] **Review:** Re-watch weak areas, practice more

---

### Pro Tips for Video Learning

1. **2x speed with caution** - Slow down for complex topics (ACLs, scripting)
2. **Code-along** - Don't just watch, type everything
3. **Pause often** - Understand before moving to next step
4. **Use subtitles** - Helpful for technical terms
5. **Practice in same session** - Watch 10 min, practice 20-30 min
6. **Follow along with docs** - Cross-reference with ServiceNow docs
7. **Take screenshots** - Build your own visual notes

---

*Video resources change frequently. If a link is broken, search the topic on YouTube - there are always new tutorials available.*
