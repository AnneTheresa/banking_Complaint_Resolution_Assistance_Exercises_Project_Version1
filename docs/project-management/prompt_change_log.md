# Prompt Change Log

**Version:** 1.0 → 2.0  
**Date:** 2026-10-14

## Test Summary

- Cases executed: 15
- Pass: 13
- Fail: 2
- Accuracy: 86.67%

---

## Failure Group 1

### Digital Banking vs. Account Access

**Example:** "App login fails after update"

**Observed:** Classifier selected Digital Banking.  
**Expected:** Account Access.

**Cause:** The prompt did not define category precedence clearly.

### Change Applied

Added rule:

> If the primary problem is authentication, login, lockout, password reset, or access to an account, classify as Account Access.
>
> If the user can access the system but functionality is broken, classify as Digital Banking.

---

## Failure Group 2

### Fees vs. Service Quality

**Example:** "Rude service and unexplained fee"

**Observed:** Classifier selected Service Quality.  
**Expected:** Fees.

**Cause:** The primary complaint selection rule was unclear.

### Change Applied

Added rule:

> When multiple complaint types appear, classify according to the issue that has direct financial impact.

**Priority order:**

1. Mortgage Servicing
2. Card or Transaction Dispute
3. Fees
4. Account Access
5. Digital Banking
6. Service Quality

---

## Reason for Revision

The failures occurred because overlapping complaint categories lacked precedence rules.

The prompt was updated using evidence from the test cases rather than changing expected labels.

## Expected Impact

- Improved consistency.
- Reduced ambiguity.
- Better alignment with complaint intake specification and assisted journey.
- No changes were made to approved categories.
- No schema changes were introduced.
