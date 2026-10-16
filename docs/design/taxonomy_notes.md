# Complaint Classification Taxonomy Notes

**Version:** 1.0

## Approved Categories

The classifier may only return the following categories:

1. Fees
2. Card or Transaction Dispute
3. Digital Banking
4. Service Quality
5. Mortgage Servicing
6. Account Access

No additional categories are permitted.

## Category Definitions

### Fees

Customer disputes service fees, maintenance fees, overdraft fees, account fees, or penalties.

**Examples**

- Unknown monthly fee
- Unexpected account charge

### Card or Transaction Dispute

Customer disputes a card transaction or reports unauthorized activity.

**Examples**

- Unauthorized purchase
- Debit card charge dispute

### Digital Banking

Customer reports problems using digital channels.

**Examples**

- Mobile app failure
- Online banking unavailable

### Service Quality

Customer dissatisfaction with service received.

**Examples**

- Delayed response
- Poor follow-up
- Staff handling concerns

### Mortgage Servicing

Issues relating to mortgage servicing or payment application.

**Examples**

- Incorrect mortgage payment
- Mortgage account servicing issue

### Account Access

Customer cannot access an account.

**Examples**

- Locked account
- Login failure
- Password reset difficulty

## Potential Overlaps

### Digital Banking vs. Account Access

**Example:** "I cannot log into the banking app."

**Possible categories**

- Digital Banking
- Account Access

**Rule:** If the primary issue is authentication or access, use **Account Access**. If the primary issue is application functionality, use **Digital Banking**.

### Service Quality vs. Fees

**Example:** "The agent was rude and would not explain a fee."

The primary complaint determines classification.

### Mortgage Servicing vs. Fees

Mortgage servicing complaints take precedence when the issue involves mortgage processing or payment application.

### Card Dispute vs. Service Quality

A transaction issue takes precedence when financial loss is reported.

## Unclear Rules Requiring Future Clarification

1. Confidence threshold requiring review.
2. Escalation threshold between Medium and High urgency.
3. Multi-category ranking logic.
4. Low urgency examples are not defined in the supplied material.
