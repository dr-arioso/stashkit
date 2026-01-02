"""
Bootstrap script for the Project Decision Ledger (PDL).

This script is **safe to import** (no side effects at import time).
All filesystem writes, database initialization, and self-tests occur
**only** when executed as a script.

Target structure:

src/stashkit/decision_ledger/
  ├─ __init__.py
  ├─ resolve.py
  ├─ decisions.db
  ├─ add_decision.py
  ├─ query_decisions.py
  └─ templates/
      ├─ resolve.py.tpl
      ├─ add_decision.py.tpl
      └─ query_decisions.py.tpl
"""

from pathlib import Path
import sqlite3
import argparse
import sys

# ------------------------------------------------------------------
# Path computation (SAFE AT IMPORT TIME)
# ------------------------------------------------------------------

BOOTSTRAP_FILE = Path(__file__).resolve()
ROOT = BOOTSTRAP_FILE.parents[1]        # repo root (tests/ -> repo/)
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

PDL_DIR = SRC / "stashkit" / "decision_ledger"
TEMPLATE_DIR = PDL_DIR / "templates"
DB_PATH = PDL_DIR / "decisions.db"

FILES = {
    "resolve.py": TEMPLATE_DIR / "resolve.py.tpl",
    "add_decision.py": TEMPLATE_DIR / "add_decision.py.tpl",
    "query_decisions.py": TEMPLATE_DIR / "query_decisions.py.tpl",
}

# ------------------------------------------------------------------
# Bootstrap implementation
# ------------------------------------------------------------------

def bootstrap(*, dry_run: bool = False, force: bool = False) -> None:
    if dry_run:
        print("[DRY-RUN] Would create:", PDL_DIR)
        print("[DRY-RUN] Would create:", TEMPLATE_DIR)
    else:
        PDL_DIR.mkdir(parents=True, exist_ok=True)
        TEMPLATE_DIR.mkdir(exist_ok=True)
        (PDL_DIR / "__init__.py").touch(exist_ok=True)

    for target, template in FILES.items():
        out_path = PDL_DIR / target

        if out_path.exists() and not force:
            continue

        if dry_run:
            print(f"[DRY-RUN] Would write {out_path} from {template.name}")
            continue

        if not template.exists():
            raise FileNotFoundError(f"Missing template: {template}")

        out_path.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")

    if dry_run:
        print("[DRY-RUN] Would initialize database:", DB_PATH)
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,

            scope TEXT NOT NULL,
            category TEXT NOT NULL,
            subject TEXT NOT NULL,

            decision TEXT NOT NULL,
            rationale TEXT,

            definition_ref TEXT,
            supersedes TEXT,
            status TEXT NOT NULL,

            strength REAL,
            doc_projection TEXT
        );
        """
    )

    conn.commit()
    conn.close()

# ------------------------------------------------------------------
# Self-test (EXECUTION ONLY)
# ------------------------------------------------------------------

def self_test() -> None:
    from stashkit.decision_ledger.resolve import resolve_subject
    if not callable(resolve_subject):
        raise RuntimeError("resolve_subject is not callable")
    print("[SELF-TEST] resolve_subject import OK")

# ------------------------------------------------------------------
# CLI entrypoint
# ------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap Project Decision Ledger (PDL)")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated files")
    args = parser.parse_args()

    bootstrap(dry_run=args.dry_run, force=args.force)

    if not args.dry_run:
        self_test()

    print("[DONE] Project Decision Ledger bootstrap complete.")