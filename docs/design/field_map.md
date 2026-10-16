# Complaint Extraction Field Map

## Purpose

Extract explicit complaint facts from customer narratives and convert them into structured JSON.

## General Rules

1. Extract only facts explicitly stated in the complaint text.
2. Do not infer, guess, normalize, or calculate values.
3. Every populated field must have supporting evidence.
4. Evidence must be copied exactly from the source text.
5. If a value is not explicitly present, return `null`.

## Field Mapping

### `customer_id`

**Evidence rule**

- Customer identifier explicitly mentioned by the customer.
- Examples:
  - "Customer ID CUST12345"
  - "My customer number is 987654"

**Output:** String value  
**Missing behavior:** Return `null`

---

### `account_id`

**Evidence rule**

- Account number or account identifier explicitly referenced.
- Examples:
  - "Account number 123456789"
  - "Account ID ACC-98765"

**Output:** String value  
**Missing behavior:** Return `null`

---

### `amount`

**Evidence rule**

- Monetary value explicitly stated.
- Examples:
  - "$250"
  - "charged $5.75"

**Output:** Numeric value only  
**Missing behavior:** Return `null`

**Notes**

- Do not calculate amounts.
- Do not infer currency.

---

### `transaction_date`

**Evidence rule**

- Explicit transaction date referenced in the complaint.
- Examples:
  - "2025-09-05"
  - "Transaction from March 2nd"

**Output:** String value copied from the source or normalized per implementation rules  
**Missing behavior:** Return `null`

---

### `requested_action`

**Evidence rule**

- Explicit customer request.
- Examples:
  - "refund the charge"
  - "reverse the fee"
  - "investigate the transaction"

**Output:** String  
**Missing behavior:** Return `null`

---

### `evidence_spans`

**Evidence rule**

- Exact text snippets copied from the complaint narrative.
- Include one span for each populated field.

**Output:** Array of strings  
**Missing behavior:** Return an empty array when no extractable facts exist.

## Prohibited Behavior

Do not:

- Guess identifiers.
- Infer missing dates.
- Estimate amounts.
- Predict desired actions.
- Use classification labels as extracted facts.

**Example complaint:** "I was charged unexpectedly."

**Correct output:**

```json
{
  "customer_id": null,
  "account_id": null,
  "amount": null,
  "transaction_date": null,
  "requested_action": null,
  "evidence_spans": []
}
```
