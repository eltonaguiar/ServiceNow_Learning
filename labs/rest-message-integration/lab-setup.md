# Lab Setup: REST Message Integration

**Time:** 5-10 minutes  

---

## 1. Create Update Set
**Breadcrumb:** System Update Sets → Local Update Sets → New

- Name: `Lab_REST_Message_Integration`
- Description: `Learning lab for outbound REST Message`
- Set as Current

---

## 2. Choose a Public API (No Auth)

We'll use a simple public API for learning:

**Option A (Recommended): JSONPlaceholder**
- URL: `https://jsonplaceholder.typicode.com/users/1`
- Returns user info as JSON
- No authentication required
- Great for learning

**Option B:** `https://api.agify.io/?name=michael` (predicts age by name)
- Also no auth, simple response

We'll use **Option A** in the steps below.

---

## 3. Prepare Test Record
**Breadcrumb:** Incident → All → New

Create a test incident:
- Short description: `Test REST Message Lab`
- Caller: Yourself
- Submit and note the **Number** (e.g., INC0010001)

---

## 4. Verify Access
You need to be able to access:
- System Web Services → Outbound → REST Message
- System Definition → Business Rules (or Script Includes)
- Incident table

If any are missing, check your roles (need `admin` for lab).

---

## Ready to Start
Proceed to `lab-steps.md`
