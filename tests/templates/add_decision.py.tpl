import json
import sqlite3
from datetime import datetime
from pathlib import Path
import sys

DB_PATH = Path(__file__).parent / "decisions.db"

if len(sys.argv) != 2:
    print("Usage: python add_decision.py <decision.json>")
    sys.exit(1)

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute(
    """
    INSERT INTO decisions (
        timestamp,
        scope,
        category,
        subject,
        decision,
        rationale,
        definition_ref,
        supersedes,
        status,
        strength,
        doc_projection
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        datetime.utcnow().isoformat(),
        payload["scope"],
        payload["category"],
        payload["subject"],
        payload["decision"],
        payload.get("rationale"),
        payload.get("definition_ref"),
        payload.get("supersedes"),
        payload["status"],
        payload.get("strength"),
        payload.get("doc_projection"),
    ),
)

conn.commit()
conn.close()

print(f"[OK] Recorded decision: {payload['subject']}")
