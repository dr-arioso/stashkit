import sqlite3
from pathlib import Path
from pprint import pprint
import sys

DB_PATH = Path(__file__).parent / "decisions.db"

if len(sys.argv) < 2:
    print("Usage: python query_decisions.py <search_term>")
    sys.exit(1)

term = f"%{sys.argv[1]}%"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute(
    """
    SELECT * FROM decisions
    WHERE subject LIKE ? OR decision LIKE ?
    ORDER BY id DESC
    """,
    (term, term),
)

rows = cur.fetchall()
conn.close()

for row in rows:
    pprint(dict(row))
    print("-" * 60)
