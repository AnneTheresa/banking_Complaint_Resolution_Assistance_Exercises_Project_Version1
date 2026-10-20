"""Rebuild SQLite sample database, validate eight Week 2 queries, and export CSV.

Run: python run_basic_queries.py
The schema and seed are the original, unmodified supplied files.
"""
import csv
import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "TableCreationSQLiteScript.sql"
SEED = HERE / "seeddatacrs.sql"
SQL = HERE / "basic_queries.sql"
DB = HERE / "BankCRS_seeded.sqlite"
OUT = HERE / "basic_query_results.csv"

PARAMS = {
    5: {"customer_id": "CUS001"},
    6: {"start_date": "2025-01-09", "end_date": "2025-01-20"},
}
QUESTIONS = {
    1: "All open complaints",
    2: "High-priority unresolved complaints",
    3: "Complaints by status",
    4: "Complaints by category",
    5: "Complaints for customer ID",
    6: "Complaints in date range",
    7: "CLOSED complaints without timestamped CLOSED history event (schema proxy)",
    8: "Ten most recent complaints",
}


def load_queries(path):
    contents = path.read_text(encoding="utf-8")
    found = re.findall(r"^-- BEGIN Q(\d+)\s*\n(.*?)^-- END Q\1\s*$", contents, re.MULTILINE | re.DOTALL)
    queries = {int(num): sql.strip() for num, sql in found}
    if set(queries) != set(range(1, 9)):
        raise ValueError(f"Expected eight queries, found {sorted(queries)}")
    return queries


def build_db():
    # The supplied file begins with `use BankCRS`, which is not valid SQLite.
    schema = SCHEMA.read_text(encoding="utf-8-sig")
    schema = re.sub(r"^\s*use\s+BankCRS\s*;?\s*(?:\r?\n|$)", "", schema, count=1, flags=re.I)
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(schema)
    conn.executescript(SEED.read_text(encoding="utf-8-sig"))
    conn.commit()
    return conn


def verify(conn, queries, result_sets):
    expected_row_counts = {1: 5, 2: 4, 3: 4, 4: 7, 5: 1, 6: 5, 7: 0, 8: 10}
    for number, expected in expected_row_counts.items():
        actual = len(result_sets[number])
        assert actual == expected, f"Q{number} returned {actual} rows; expected {expected}"
    assert sum(row["complaint_count"] for row in result_sets[3]) == 10
    assert sum(row["complaint_count"] for row in result_sets[4]) == 10
    assert {row["complaint_id"] for row in result_sets[2]} == {"CMP001", "CMP003", "CMP006", "CMP007"}
    assert [row["complaint_id"] for row in result_sets[5]] == ["CMP001"]
    assert [row["complaint_id"] for row in result_sets[6]] == ["CMP003", "CMP004", "CMP005", "CMP006", "CMP007"]
    assert result_sets[8][0]["complaint_id"] == "CMP010"
    assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    assert conn.execute("SELECT COUNT(*) FROM complaint WHERE status = 'CLOSED'").fetchone()[0] == 1
    # Negative test: unknown customer must return zero rows.
    assert conn.execute(queries[5], {"customer_id": "CUS999"}).fetchall() == []
    # End-date boundary test: timestamps on the end date are included.
    on_end_date = conn.execute(queries[6], {"start_date": "2025-01-20", "end_date": "2025-01-20"}).fetchall()
    assert [row["complaint_id"] for row in on_end_date] == ["CMP007"]
    # Missing closure evidence must be detected, and the test record rolled back.
    conn.execute("SAVEPOINT closure_edge_case")
    try:
        conn.execute("""INSERT INTO complaint
            (complaint_id,customer_id,account_id,channel,category,complaint_text,priority,status,received_at,assigned_analyst_id)
            VALUES ('CMP_TEST_MISSING_HISTORY','CUS001','ACC001','Web','Fee Dispute','Test only',NULL,'CLOSED','2025-01-25 12:00:00',NULL)""")
        detected = conn.execute(queries[7]).fetchall()
        assert [r["complaint_id"] for r in detected] == ["CMP_TEST_MISSING_HISTORY"]
    finally:
        conn.execute("ROLLBACK TO SAVEPOINT closure_edge_case")
        conn.execute("RELEASE SAVEPOINT closure_edge_case")
    assert conn.execute(queries[7]).fetchall() == []
    print("PASS: 8 query row counts, aggregates, exact IDs, integrity, null/history and date-boundary checks")


def export_csv(result_sets):
    headers = ["query_id", "question", "parameters", "result_state", "returned_rows", "row_number",
               "complaint_id", "customer_id", "account_id", "channel", "category", "priority",
               "status", "received_at", "assigned_analyst_id", "complaint_count"]
    with OUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for query_id, records in sorted(result_sets.items()):
            params = "; ".join(f"{k}={v}" for k, v in PARAMS.get(query_id, {}).items())
            if not records:
                writer.writerow({"query_id": f"Q{query_id}", "question": QUESTIONS[query_id],
                                 "parameters": params, "result_state": "NO_ROWS", "returned_rows": 0})
                continue
            for number, row in enumerate(records, start=1):
                record = dict(row)
                record.update({"query_id": f"Q{query_id}", "question": QUESTIONS[query_id],
                               "parameters": params, "result_state": "RESULT", "returned_rows": len(records),
                               "row_number": number})
                writer.writerow(record)
    print(f"Wrote {OUT.name}")


def main():
    queries = load_queries(SQL)
    conn = build_db()
    try:
        results = {number: conn.execute(query, PARAMS.get(number, {})).fetchall()
                   for number, query in sorted(queries.items())}
        verify(conn, queries, results)
        export_csv(results)
        for number, rows in results.items():
            print(f"Q{number}: {len(rows)} result rows")
        print(f"Database: {DB.name}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
