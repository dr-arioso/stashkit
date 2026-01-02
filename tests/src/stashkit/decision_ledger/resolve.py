Read-time authority for Project Decision Ledger (PDL).

This module interprets append-only ledger entries to answer
questions such as:
  - Is a subject deprecated?
  - What replaced it?
  - What is the current canonical decision?

This module is deterministic, read-only, and side-effect free.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "decisions.db"

def resolve_subject(subject: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM decisions
        WHERE subject = ? OR supersedes LIKE ?
        ORDER BY id ASC
        """,
        (subject, f"%{subject}%"),
    )

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    replaced_by = [r["subject"] for r in rows if r.get("supersedes") and subject in r.get("supersedes")]
    deprecated = any(r["category"] == "deprecation" and r["subject"] == subject for r in rows)

    status = "active"
    if replaced_by:
        status = "replaced"
    elif deprecated:
        status = "deprecated"

    latest = rows[-1] if rows else None

    return {
        "subject": subject,
        "status": status,
        "replaced_by": replaced_by or None,
        "latest_decision": latest,
        "history": rows,
    }
