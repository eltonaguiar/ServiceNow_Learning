#!/usr/bin/env python3
"""
generate_learning_path.py — Auto-generate a learning path for any ServiceNow topic

Uses the SNRLM 7-step methodology to create a complete learning guide.

Agent: Hermes Agent
Date: 2026-11-04
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def generate_learning_path(topic: str, output_dir: str = "methodology") -> str:
    """Generate a learning path markdown file for the given topic."""

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_topic = topic.lower().replace(" ", "_").replace("/", "_")
    filename = f"{safe_topic}_learning_path_{date_str}.md"
    filepath = Path(output_dir) / filename

    content = f"""# Learning Path: {topic}

**Agent:** Hermes Agent  
**Date:** {date_str}  
**Topic:** {topic}  
**Methodology:** SNRLM 7-Step Cycle

---

## Overview

This learning path was generated using the ServiceNow Rapid Learning Methodology (SNRLM).
Follow the 7 steps below to go from "I've never heard of this" to "I built a working lab."

---

## Step 1: Decompose the Topic

**What is {topic}?**
*[To be filled in — what is this ServiceNow concept?]*

**What problem does it solve?**
*[To be filled in — why does this exist?]*

**Where does it live in ServiceNow?**
*[To be filled in — navigation path]*

**Who uses it?**
*[To be filled in — roles/personas]*

**Key components:**
*[To be filled in — tables, forms, scripts, records]*

---

## Step 2: ELI5 Translation

*[To be filled in — explain like you're 5, with analogies]*

---

## Step 3: Breadcrumb Mapping

**Exact click path:**
*[To be filled in — Menu > Module > Sub-module > Record > Field]*

---

## Step 4: Field Classification

| Field | CRITICAL / MANDATORY / OPTIONAL | Why |
|-------|--------------------------------|-----|
| *[field]* | *[classification]* | *[reason]* |
| *[field]* | *[classification]* | *[reason]* |
| *[field]* | *[classification]* | *[reason]* |

---

## Step 5: Common Mistakes

| Mistake | What Happens | How to Avoid | How to Fix |
|---------|-------------|-------------|------------|
| *[mistake]* | *[consequence]* | *[prevention]* | *[fix]* |
| *[mistake]* | *[consequence]* | *[prevention]* | *[fix]* |

---

## Step 6: Practical Lab

**Objective:** *[what the user will build]*

**Prerequisites:** *[what they need]*

**Steps:**
1. *[step 1 with breadcrumbs]*
2. *[step 2 with breadcrumbs]*
3. *[step 3 with breadcrumbs]*

**Validation:** *[how to know it worked]*

---

## Step 7: Infographic Outline

**Elements to include:**
- [ ] Title bar with ELI5 definition
- [ ] Flow diagram (left-to-right)
- [ ] Breadcrumb path
- [ ] Field classification table
- [ ] Mistake warnings (top 3)
- [ ] Quick reference fields/tables/modules
- [ ] Lab link

---

## Quick Reference

**Most important tables:** *[table names]*  
**Most important modules:** `[module names]`  
**Most important fields:** `[field names]`  
**CRITICAL fields:** `[must-have fields]`  
**MANDATORY fields:** `[required to save]`  
**OPTIONAL fields:** `[nice-to-have]*  
"""
    filepath.write_text(content)
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Generate ServiceNow learning path")
    parser.add_argument("--topic", required=True, help="ServiceNow topic for the learning path")
    parser.add_argument("--output", default="methodology", help="Output directory")
    args = parser.parse_args()

    filepath = generate_learning_path(args.topic, args.output)
    print(f"Learning path generated: {filepath}")


if __name__ == "__main__":
    main()
