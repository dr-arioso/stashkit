from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Tuple
from pathlib import Path
import json
from enum import Enum
import os

from stashkit.claims import Claims


class ResolverState:
    """Runtime state carried through a resolver invocation.

    Responsibilities:
    - Track known claims and their provenance/confidence
    - Track which skills have run (and on what inputs)
    - Provide stable hashing for adaptive / non-linear resolution
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

        # Claims store
        self.known = Claims()

        # Runtime signals
        self.trace: List[str] = []
        self.diagnostics: List[str] = []
        self.user_action: Optional[Any] = None

        # Skill execution bookkeeping
        self.skill_runs: Dict[str, int] = {}
        self.run_inputs: Dict[str, set[str]] = {}

        # Capability advertisement from skills (not claims)
        self.available_fields: Dict[str, Dict[str, Any]] = {}

        # Hash caches (purely derived from known claims)
        self._input_hash_cache: Dict[frozenset[str], str] = {}
        self._execution_hash_cache: Dict[
            Tuple[frozenset[str], Tuple[str, ...]], str
        ] = {}

    # ------------------------------------------------------------------
    # Skill execution bookkeeping
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Claims handling
    # ------------------------------------------------------------------

    def merge_claims(self, claims: Claims) -> None:
        """Merge new claims into known evidence."""
        self.known.merge(claims)

        # Invalidate all derived hashes (inputs have changed)
        self._input_hash_cache.clear()
        self._execution_hash_cache.clear()

    # ------------------------------------------------------------------
    # Hashing
    # ------------------------------------------------------------------

    def execution_hash(
        self,
        *,
        consumes: Iterable[str],
        produces: Iterable[str],
    ) -> str:
        """
        Compute an execution identity hash for a skill run.

        Execution identity is defined over:
        - effective input snapshot of consumed fields
        - declared output frontier (produces)

        Produces participation ensures that expanding produces
        constitutes a distinct execution opportunity.
        """
        key = (frozenset(consumes), tuple(sorted(produces)))
        cached = self._execution_hash_cache.get(key)
        if cached is not None:
            return cached

        payload = {
            "inputs": self.effective_inputs_snapshot(consumes),
            "produces": list(key[1]),
        }

        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        h = raw.hex()
        self._execution_hash_cache[key] = h
        return h

    def input_hash(self, fields: Iterable[str]) -> str:
        """
        Compute (and memoize) a stable hash over consumed inputs only.

        This must be:
        - deterministic
        - free of filesystem I/O
        - invalidated whenever claims change
        """
        key = frozenset(fields)
        cached = self._input_hash_cache.get(key)
        if cached is not None:
            return cached

        raw = json.dumps(
            self.effective_inputs_snapshot(fields),
            sort_keys=True,
        ).encode("utf-8")
        h = raw.hex()
        self._input_hash_cache[key] = h
        return h

    def effective_inputs_snapshot(self, fields: Iterable[str]) -> Dict[str, Any]:
        """Return a JSON-stable snapshot of consumed inputs."""
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
            # Avoid filesystem access / Windows hangs
            return os.fspath(value)
        if isinstance(value, Enum):
            return value.value
        return value

    # ------------------------------------------------------------------
    # Diagnostics helpers
    # ------------------------------------------------------------------

    def add_trace(self, msg: str) -> None:
        self.trace.append(msg)

    def add_diagnostic(self, msg: str) -> None:
        self.diagnostics.append(msg)
