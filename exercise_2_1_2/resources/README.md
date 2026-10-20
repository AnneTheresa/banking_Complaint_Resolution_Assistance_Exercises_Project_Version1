# FDM Week 2 — Exercise 2.1.2: Query Complaint Data

## Required submission files

- `basic_queries.sql` — eight readable SQLite queries corresponding to the supplied question list.
- `basic_query_results.csv` — actual query outputs from the supplied synthetic data, including a zero-rows marker for Q7.
- `query_exploration.md` — database exploration, 16 table counts, types, null checks, integrity and anomalies.
- `query_notes.md` — filters, date, null handling, dialect, validation and the Q7 schema limitation.

## Extra files for reproducibility

- `run_basic_queries.py` — standard-library-only Python runner; build, test and export in one command.
- `BankCRS_seeded.sqlite` — populated SQLite database for browsing/running individual queries.
- `TableCreationSQLiteScript.sql`, `seeddatacrs.sql`, `basic_query_questions.md` — unchanged source files.

## Run on your Windows PC

Have Python 3 installed. Extract this folder, open a terminal in the extracted directory and run:

```powershell
python run_basic_queries.py
```

This reconstructs the SQLite database, runs eight SQL statements, verifies normal and negative/boundary cases, and re-exports the CSV. It does not need a Python package installation.

You can open `BankCRS_seeded.sqlite` in DB Browser for SQLite (or another SQLite client), and execute the statements from `basic_queries.sql` one at a time. Q5 and Q6 require bound parameters; examples are provided in `query_notes.md`.

**Question 7 warning:** The worksheet asks for a `date_closed` field that is missing from the provided schema. The implemented Q7 checks missing timestamped CLOSED history records instead. This produces zero results for the seed, but it is not the same as verifying a `date_closed` value. This limitation is intentional and documented, rather than silently changing the team's schema.

## Suggested Git handoff

Add the four named deliverables to your exercise's directory on a feature branch. The reproducibility files are helpful if permitted by your coach. Suggested pull-request title:

`[Your name] Query Complaint Data (Week 2)`

In the PR description, mention the query counts, that integrity and boundary checks passed, and the unresolved Q7 schema discrepancy. Tag the coach; wait for review before merging.
