# Exercise 2.1.2 — Query Notes and Validation

## Basis and parameters

All eight statements in `basic_queries.sql` correspond, in order, to the eight prompts in `basic_query_questions.md`. They run in **SQLite 3** against the supplied `seeddatacrs.sql` loaded into the supplied SQLite table schema. `basic_query_results.csv` is an export of these real seeded results, not fabricated example outputs.

The two parameterized statements use **named bound parameters**, not string interpolation:

- **Q5:** `:customer_id` — tested with `CUS001`.
- **Q6:** `:start_date` and `:end_date` — tested with `2025-01-09` through `2025-01-20`, inclusive. Caller should validate that dates are valid `YYYY-MM-DD` values and that start is not after end.

Python `sqlite3` example: `conn.execute(query, {"customer_id": "CUS001"})`. To use the SQLite CLI interactively, bind a variable before executing the individual query, e.g. `.parameter init` followed by `.parameter set :customer_id 'CUS001'`.

## SQL reasoning (required Step 4)

### One filter: Q2 high-priority unresolved

`priority = 'High'` performs an exact match on the seeded priority label. The additional filter `status IN ('OPEN', 'IN_PROGRESS', 'UNDER_REVIEW')` includes the three observed unresolved states and excludes `CLOSED`. This produces 4 seeded complaints: `CMP001`, `CMP003`, `CMP006`, `CMP007`. The seeded `Critical` complaint `CMP009` is excluded by design; whether it should be included under a broader *high or above* definition is a business decision, not a SQL default.

### One date condition: Q6 inclusive date range

`received_at >= datetime(:start_date)` **and** `received_at < datetime(:end_date, '+1 day')` implements a half-open timestamp range, which includes all times on the supplied end date. For example, `CMP007` at `2025-01-20 09:30:00` is included when the user enters end date `2025-01-20`. This avoids the common error of matching only midnight at the start of the last day. The condition assumes the database's consistent ISO-style local timestamp strings and a single agreed timezone convention.

### One null-handling choice: Q7 closure-history check

The source question requests **closed complaints with missing `date_closed`**, but `complaint` has **no `date_closed` field**. The query therefore performs a *proxy* consistency check: for complaints currently `CLOSED`, use `NOT EXISTS` to find complaints that lack **any** status-history event with `new_status = 'CLOSED'` and non-null `changed_at`.

`NOT EXISTS` is preferable here to a regular join: duplicate history events do not duplicate complaint rows, and a missing history row is correctly detectable. This **does not prove that `date_closed` is populated**, because no such column exists. The one seeded `CLOSED` complaint, `CMP005`, has a timestamped closure event, so the proxy returns **zero rows**, matching the *expected zero* under the proxy definition only.

The seed inserts status history without `changed_at`, causing SQLite's `CURRENT_TIMESTAMP` default to populate import-time timestamps. These cannot be interpreted as authoritative historical closure times. A literal implementation of Q7 requires an approved migration adding `complaint.date_closed` (and suitable write-time rules), or approval to change the question to explicitly reference history events. No schema alteration was performed here.

## Query result summary

| Query | Expected business question | Seeded result | Check |
|---|---|---:|---|
| Q1 | All `OPEN` complaints | 5 rows | Pass |
| Q2 | High-priority unresolved | 4 rows | Pass |
| Q3 | Count by status | 4 groups; total 10 | Pass |
| Q4 | Count by category | 7 groups; total 10 | Pass |
| Q5 | Complaints for `CUS001` | 1 row (`CMP001`) | Pass |
| Q6 | Complaints from Jan 9 to Jan 20 | 5 rows (`CMP003`–`CMP007`) | Pass |
| Q7 | Missing closure date | 0 proxy rows | **Schema gap; literal requirement untestable** |
| Q8 | Ten most recent complaints | 10 rows; newest `CMP010` | Pass |

`basic_query_results.csv` uses one normalized CSV table for all eight output sets. The columns `query_id`, `question`, `parameters`, `returned_rows`, `row_number` and `result_state` identify each query. The group counts for Q3/Q4 appear in `complaint_count`. A `NO_ROWS` metadata record is included for Q7 so the empty result is visible without inventing a complaint row.

## Validation checks actually executed

The reproducible `run_basic_queries.py` script:

1. Creates a fresh `BankCRS_seeded.sqlite` with the 16 supplied tables and seed records.
2. Enables SQLite foreign keys; checks `PRAGMA integrity_check = 'ok'` and that `PRAGMA foreign_key_check` reports no violations.
3. Runs all 8 queries against the populated database using the example parameter values, verifying counts, group totals and selected complaint IDs.
4. Tests Q5 with nonexistent customer `CUS999` (returns zero rows).
5. Tests Q6 with the single inclusive boundary date `2025-01-20` (returns `CMP007`).
6. Uses a savepoint to insert a temporary `CLOSED` complaint without a closure-history event; confirms Q7 flags it, then rolls it back. The exported sample and final database do **not** contain this test record.
7. Exports the executed results to `basic_query_results.csv`.

All programmatic checks passed on the supplied seed.

## SQL dialect and limitations

- **SQLite SQL**, not PostgreSQL, SQL Server or MySQL. `datetime(:end_date, '+1 day')` and `LIMIT 10` are SQLite-specific syntax choices. Adapt if the project switches databases.
- The provided `TableCreationSQLiteScript.sql` starts with `use BankCRS`, which is not valid SQLite syntax. The runner removes that single initial line at load time without altering the original file.
- Dates are based on `received_at` (the available creation/opening timestamp) rather than a distinct `opened_at` column, which the schema does not define.
- Date ordering and `datetime()` assume the supplied ISO-like format; timezone and timestamp conventions must be specified for production data.
- **Q7 is not literally answered until a valid `date_closed` definition exists.** This is the only outstanding exercise-specific schema mismatch.
- A broader unresolved/high-priority classification may need coach-approved status and severity taxonomies.

## Handover

The `complaint` and `complaint_status_history` table names, key fields, query inputs and parameter patterns remain unchanged for Exercise **2.2.1**, which builds joins. Request clarification/approval for the missing closure-date field before implementing any downstream API or joining on `date_closed`.
