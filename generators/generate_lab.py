#!/usr/bin/env python3
"""
generate_lab.py — Auto-generate hands-on labs for ServiceNow topics

Supports: rest_message, remote_table, and generic lab types.

Agent: Hermes Agent
Date: 2026-11-04
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path


def generate_lab(lab_type: str, topic: str, output_dir: str = "labs") -> str:
    """Generate a lab markdown file."""

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_topic = topic.lower().replace(" ", "_").replace("/", "_")
    filename = f"{lab_type}_{safe_topic}_lab_{date_str}.md"
    filepath = Path(output_dir) / filename

    if lab_type == "rest_message":
        content = generate_rest_message_lab(topic, date_str)
    elif lab_type == "remote_table":
        content = generate_remote_table_lab(topic, date_str)
    else:
        content = generate_generic_lab(topic, date_str)

    filepath.write_text(content)
    return str(filepath)


def generate_rest_message_lab(topic: str, date_str: str) -> str:
    return f"""# Lab: {topic} — REST Message Integration

**Agent:** Hermes Agent  
**Date:** {date_str}  
**Topic:** {topic}  
**Type:** REST Message Integration

---

## Prerequisites

- Admin access to a ServiceNow instance
- External API endpoint

---

## Steps

### Step 1: Create the REST Message
**Breadcrumb:** `System Web Services > Outbound > REST Messages > New`

| Field | Value | Classification |
|-------|-------|---------------|
| Name | Descriptive name | CRITICAL |
| Endpoint | API URL | CRITICAL |
| HTTP Method | GET/POST/PUT/DELETE | CRITICAL |
| Authentication type | None/Basic/Bearer | MANDATORY |
| Active | true | MANDATORY |

### Step 2: Create the REST Message Function
**Breadcrumb:** `System Web Services > Outbound > REST Message Functions > New`

### Step 3: Test the Connection
Use the Test button on the REST Message record.

### Step 4: Process the Response
Parse JSON, extract fields, use in ServiceNow.

### Step 5: Error Handling
Check HTTP status, wrap JSON parsing in try/catch.

---

## Validation Checklist

- [ ] REST Message created and Active
- [ ] Test returns HTTP 200
- [ ] Response data is parsed correctly
- [ ] Error handling works

"""


def generate_remote_table_lab(topic: str, date_str: str) -> str:
    return f"""# Lab: {topic} — Remote Table

**Agent:** Hermes Agent  
**Date:** {date_str}  
**Topic:** {topic}  
**Type:** Remote Table

---

## Prerequisites

- Admin access to a ServiceNow instance
- External data source

---

## Steps

### Step 1: Create the Remote Table
**Breadcrumb:** `System Definition > Remote Tables > New`

| Field | Value | Classification |
|-------|-------|---------------|
| Name | Table name | CRITICAL |
| Label | Display name | CRITICAL |
| Connection type | REST/JDBC | CRITICAL |
| Active | true | MANDATORY |

### Step 2: Configure the Connection
Set up URL, HTTP method, authentication.

### Step 3: Map Fields
Map external JSON paths to ServiceNow fields.

### Step 4: View the Data
Check list view shows remote data.

### Step 5: Add as Related List
Add to Incident or other form.

---

## Validation Checklist

- [ ] Remote Table created and Active
- [ ] Connection configured and Active
- [ ] Field mappings created
- [ ] Data visible in list view
- [ ] Related list appears on form

"""


def generate_generic_lab(topic: str, date_str: str) -> str:
    return f"""# Lab: {topic}

**Agent:** Hermes Agent  
**Date:** {date_str}  
**Topic:** {topic}

---

## Learning Objective

By the end of this lab, you will understand and be able to use {topic} in ServiceNow.

---

## Prerequisites

- Admin access to a ServiceNow instance

---

## Steps

Follow the SNRLM 7-step cycle:
1. Decompose the topic
2. ELI5 translation
3. Breadcrumb mapping
4. Field classification
5. Common mistakes
6. Build a practical exercise
7. Create an infographic

---

## Validation Checklist

- [ ] Can navigate to the module
- [ ] Can create a record
- [ ] Can explain the concept in plain English
- [ ] Built a working example

"""


def main():
    parser = argparse.ArgumentParser(description="Generate ServiceNow learning labs")
    parser.add_argument("--type", required=True, choices=["rest_message", "remote_table", "generic"],
                        help="Type of lab to generate")
    parser.add_argument("--topic", required=True, help="ServiceNow topic for the lab")
    parser.add_argument("--output", default="labs", help="Output directory")
    args = parser.parse_args()

    filepath = generate_lab(args.type, args.topic, args.output)
    print(f"Lab generated: {filepath}")


if __name__ == "__main__":
    main()
