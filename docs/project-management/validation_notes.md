# Extraction Validation Notes

## Validation Objective

Verify that extracted values:

1. Match source text.
2. Conform to schema.
3. Are supported by explicit evidence.
4. Do not contain inferred values.

---

## Validation Checklist

### Schema Validation

**Fields verified:**

- `customer_id`
- `account_id`
- `amount`
- `transaction_date`
- `requested_action`
- `evidence_spans`

**Result:** PASS

---

### Evidence Verification

**Checks:**

- Every populated field has supporting evidence.
- Evidence is quoted exactly.
- Evidence is not paraphrased.

**Result:** PASS

---

### Unsupported Value Review

**Observed issues:** None

**Checks performed:**

- No guessed customer IDs.
- No guessed account numbers.
- No estimated amounts.
- No inferred dates.
- No inferred requested actions.

**Result:** PASS

---

### Negative Test Review

**Input lacked:**

- `customer_id`
- `account_id`
- `amount`
- `transaction_date`

**Expected:** null values  
**Observed:** null values

**Result:** PASS

---

## Limitations

- Extraction quality depends on information explicitly provided by the customer.
- Ambiguous references are not resolved.
- No entity inference is permitted.
- Classification decisions are intentionally excluded from extraction.

---

## Definition of Done Verification

- JSON validates against schema.
- Evidence spans provided.
- Missing values represented as null.
- No unsupported values found.
- Negative case validated.

**Status:** COMPLETE
