
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional

_SEVERITY_LEVELS = {
    "info": 1,
    "warning": 2,
    "error": 3,
    "fatal": 4,
}

def checkpoint(*, verbosity: int, severity: str, context: str, notes: Optional[Iterable[str]] = None) -> None:
    sev_level = _SEVERITY_LEVELS.get(severity, 1)
    should_surface = verbosity >= sev_level or sev_level >= 3
    if not should_surface:
        return

    timestamp = datetime.now().isoformat(timespec="seconds")
    header = f"[{timestamp}] {severity.upper()}: {context}"
    lines = [header]

    if notes:
        for n in notes:
            lines.append(f"  - {n}")

    message = "\n".join(lines)

    if severity == "fatal":
        raise RuntimeError(message)

    if severity == "error" and verbosity >= 3:
        raise RuntimeError(message)

    print(message)
