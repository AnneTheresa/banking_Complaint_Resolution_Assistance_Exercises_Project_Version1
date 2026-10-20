# Exercise 2.1.2 — Database Exploration

## Scope and setup

- **System:** Banking Complaint Resolution Assistant / `BankCRS` training dataset.
- **Dialect:** SQLite 3. Database generated using `TableCreationSQLiteScript.sql` and `seeddatacrs.sql`.
- **Rebuild:** `python run_basic_queries.py` creates `BankCRS_seeded.sqlite`, runs checks and exports `basic_query_results.csv`.
- **Schema compatibility adjustment:** The provided SQLite script starts with `use BankCRS`, which SQLite does not support. The runner strips this one directive from the loaded SQL string; the supplied source file remains unchanged.
- **Records:** This is supplied synthetic training data, not live complaint records.

## Step 1 — Tables and row counts

The imported database contains **16 user-defined tables** and **160 records**. `sqlite_sequence` (if shown by a SQLite browser) is internal and is excluded from the table count.

| Table | Rows | Main use / representative declared types |
|---|---:|---|
| `employee` | 10 | Analysts/reviewers; IDs, names, role `TEXT` |
| `customer` | 10 | Customer identity; names `TEXT`, `date_created DATETIME` |
| `account` | 10 | Customer accounts; balance `DECIMAL(15,2)`, `opened_date DATE` |
| `complaint` | 10 | Main query source; priority/status `TEXT`, `received_at DATETIME` |
| `complaint_status_history` | 10 | Status events; `history_id INTEGER`, `changed_at DATETIME` |
| `transactions` | 10 | Financial transactions; amount `DECIMAL(15,2)`, `processed_at DATETIME` |
| `fee` | 10 | Charges; amount `DECIMAL(10,2)`, reversed flag `INTEGER` |
| `service_request` | 10 | Requests; `created_at DATETIME`, `closed_at DATETIME` |
| `policy_document` | 10 | Policy metadata; `effective_date DATE` |
| `policy_section` | 10 | Policy text and section title `TEXT` |
| `investigation` | 10 | Investigation timelines `DATETIME`, summary `TEXT` |
| `recommendation` | 10 | Proposed actions; `confidence_score DECIMAL(5,2)` |
| `review_request` | 10 | Human review and status `TEXT` |
| `review_decision` | 10 | Decision values `TEXT` with `CHECK` constraint |
| `customer_response` | 10 | Customer replies; `sent_date DATETIME` |
| `audit_log` | 10 | Audit events; `audit_id INTEGER`, `event_timestamp DATETIME` |

### Complaint table: important columns and types

| Column | Declared SQLite type | Nullable? |
|---|---|---|
| `complaint_id` | TEXT, primary key | No (identifier) |
| `customer_id` | TEXT, foreign key | No |
| `account_id` | TEXT, foreign key | Yes |
| `channel` | TEXT | No |
| `category` | TEXT | No |
| `complaint_text` | TEXT | No |
| `priority` | TEXT | Yes |
| `status` | TEXT | No |
| `received_at` | DATETIME | No |
| `assigned_analyst_id` | TEXT, foreign key | Yes |

**Important:** The supplied `complaint` table has **no `date_closed` column**. The separate `complaint_status_history` table has `changed_at`, which records the time of a status-history event. The fields are not interchangeable without an approved business rule.

SQLite uses type affinity: `DATETIME` and `DATE` are declared types rather than native timestamp storage types. Dates in the seed are ISO-like strings. SQLite `DECIMAL` is not guaranteed to provide exact fixed-point money arithmetic by itself.

## Step 1 — Null patterns

| Table.column | Missing | Total | Observation |
|---|---:|---:|---|
| `complaint.account_id` | 0 | 10 | Every seeded complaint has an account |
| `complaint.priority` | 0 | 10 | Nullable by schema, but populated in seed |
| `complaint.assigned_analyst_id` | 0 | 10 | All complaints have analysts in seed |
| `complaint.status` | 0 | 10 | Required field |
| `complaint.received_at` | 0 | 10 | Required field |
| `complaint_status_history.old_status` | 5 | 10 | Five initial status events have no previous status |
| `complaint_status_history.changed_at` | 0 | 10 | Timestamp defaults supplied by the database |
| `investigation.completed_at` | 8 | 10 | Most seeded investigations not yet completed |
| `service_request.closed_at` | 6 | 10 | Open service requests have no closure timestamp |
| `fee.transaction_id` | 6 | 10 | Some fees have no associated transaction row |
| `customer.email` | 0 | 10 | All seeded customers have email |

Nulls are not the same as empty strings, and `COUNT(column)` ignores `NULL` while `COUNT(*)` counts rows.

## Step 1 — Complaint distribution

**Status:**

| Status | Complaints |
|---|---:|
| `OPEN` | 5 |
| `IN_PROGRESS` | 2 |
| `UNDER_REVIEW` | 2 |
| `CLOSED` | 1 |
| **Total** | **10** |

**Priority:** `Critical`: 1; `High`: 4; `Medium`: 3; `Low`: 2.

**Category:** `Fee Dispute`: 3; `Transaction Error`: 2; `Card Issue`: 1; `Customer Service`: 1; `Fraud Claim`: 1; `Online Banking`: 1; `Service Delay`: 1.

Earliest complaint: `CMP001`, `2025-01-01 09:00:00`.
Latest complaint: `CMP010`, `2025-01-25 08:45:00`.

## Observations / unexpected data

1. **Missing field for question 7:** `complaint.date_closed` does not exist. Therefore the literal question cannot be executed against the supplied schema. The query pack checks for missing timestamped `CLOSED` history events as an **explicitly non-equivalent proxy**. In this dataset, `CMP005` is closed and has a `CLOSED` event, so the proxy returns zero rows.
2. **History dates are not historical closure dates:** The seed omits `changed_at` in the status-history inserts. SQLite fills it using `CURRENT_TIMESTAMP` at import, not the complaint's 2025 operational timeline. A timestamped event exists but may not represent actual closure time.
3. **Review workflow inconsistency:** Seven `review_request.status` values differ from the corresponding `review_decision.decision` values. This may represent independent workflow states, but should be reviewed before treating the two fields as interchangeable.
4. **Sample is small:** All sixteen tables have exactly 10 seeded rows. It can confirm functionality, not performance or production data quality.
5. **Priority labels matter:** `High` and `Critical` are two distinct values. Query 2 selects exactly `High`, with unresolved statuses `OPEN`, `IN_PROGRESS` or `UNDER_REVIEW`; it does not silently include `Critical`.

## Integrity checks

- `PRAGMA integrity_check` returned `ok`.
- `PRAGMA foreign_key_check` returned zero violations after import with foreign-key enforcement enabled.
- Counts in query 3 and query 4 both sum to the 10 complaint rows.

For repeatability, run `python run_basic_queries.py` after changes to the schema, seed data or query pack, and update this document if the results change.
