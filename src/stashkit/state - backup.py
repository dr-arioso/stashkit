from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional
from pathlib import Path
import json
from enum import Enum

from stashkit.claims import Claims, FieldValue


@dataclass
class ResolverState:
    """Runtime state carried through a resolver invocation.

    Responsibilities:
    - Track known claims and their provenance/confidence
    - Track which skills have run (and on what inputs)
    - Provide stable input hashing for adaptive strategies
    - Accumulate trace + diagnostics for UX/debug
    - Carry user-facing action requests emitted by Skills
    """

    def __init__(
        self,
        image_path: str | None = None,
        verbosity: int = 0,
        unresolved_required_fields: set[str] | None = None,
        **kwargs,
    ):
        self.image_path = image_path
        self.verbosity = verbosity
        self.unresolved_required_fields = unresolved_required_fields or set()

        # ✅ REQUIRED: initialize claims store
        self.known = Claims()

        # Runtime signals
        self.trace: List[str] = []
        self.diagnostics: List[str] = []
        self.user_action: Optional[Any] = None

        # Skill execution bookkeeping
        self.skill_runs: Dict[str, int] = {}
        self.run_inputs: Dict[str, set] = {}

        # Completion / termination instrumentation (pragmatic)
        # True  => resolver determined no further enrichment is possible
        # False => enrichment still possible
        # None  => unknown / not instrumented
        self.enrichment_exhausted: Optional[bool] = None

    # ---- Skill execution bookkeeping ----

    def record_run(self, descriptor, result) -> None:
        """Record that a skill has run, and capture any side effects."""
        name = descriptor.name
        self.skill_runs[name] = self.skill_runs.get(name, 0) + 1

        ih = self.input_hash(descriptor.consumes)
        self.run_inputs.setdefault(name, set()).add(ih)

        if getattr(result, "user_action", None) is not None:
            self.user_action = result.user_action

    def has_run(self, skill_name: str, input_hash: str) -> bool:
        return input_hash in self.run_inputs.get(skill_name, set())

    # ---- Claims handling ----

    def merge_claims(self, claims: Claims) -> None:
        self.known.merge(claims)

    # ---- Input hashing ----

    def input_hash(self, fields: Iterable[str]) -> str:
        raw = json.dumps(
            self.effective_inputs_snapshot(fields),
            sort_keys=True,
        ).encode("utf-8")
        return raw.hex()

    def effective_inputs_snapshot(self, fields: Iterable[str]) -> Dict[str, Any]:
        snap: Dict[str, Any] = {}
        for f in sorted(fields):
            vals = self.known.get(f)
            snap[f] = [
                {
                    "value": self._hashable_value(v.value),
                    "provenance": v.provenance,
                    "confidence": v.confidence,
                    "semantic_type": self._hashable_value(v.semantic_type),
                }
                for v in vals
            ]
        return snap

    def _hashable_value(self, value: Any) -> Any:
        """Convert values into a JSON-stable representation suitable for hashing."""
        if isinstance(value, Path):
            return str(value.resolve())
        if isinstance(value, Enum):
            return value.value
        return value

    # ---- Diagnostics helpers ----

    def add_trace(self, msg: str) -> None:
        self.trace.append(msg)

    def add_diagnostic(self, msg: str) -> None:
        self.diagnostics.append(msg)
