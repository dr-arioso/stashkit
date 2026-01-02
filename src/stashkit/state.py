from __future__ import annotations

import json
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from stashkit.stashbench import StashBench
from stashkit.stashbench.filesystem import NormalizedFileQueue

from stashkit.claims import Claims


@dataclass(frozen=True)
class SkillSignature:
    """Opaque identifier for a specific execution opportunity of a skill."""

    skill_name: str
    digest: str

    def short(self, n: int = 8) -> str:
        return self.digest[:n]


class ResolverState:
    """Runtime state carried through a resolver invocation.

    Responsibilities:
    - Track known claims and their provenance/confidence
    - Track which execution opportunities have already run successfully
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

        # Structurally available inputs (pre-epistemic)
        # These gate skill eligibility but are NOT claims.
        self.inputs: set[str] = set()
        if image_path is not None:
            self.inputs.add("image_ref")        

        # Claims store
        self.known = Claims()

        # Runtime signals
        self.trace: List[str] = []
        self.diagnostics: List[str] = []
        self.user_action: Optional[Any] = None

        # Execution bookkeeping
        self.skill_runs: Dict[str, int] = {}
        self.executed_signatures: set[SkillSignature] = set()

        # Resolver-level termination signal (domain-agnostic)
        # True iff resolution stopped because no new execution opportunities exist
        self.no_new_execution_opportunities: bool = False     

        # Domain-level enrichment status (tri-state)
        #   True  -> enrichment exhausted
        #   False -> enrichment still possible
        #   None  -> unknown / not yet inferred
        self.enrichment_exhausted: bool | None = None        

        # Capability advertisement from skills (not claims)
        # field_name -> metadata dict (source, confidence, structured, fetchable, ...)
        self.available_fields: Dict[str, Dict[str, Any]] = {}

        # Cache: signature computation is centralized here (architecturally owned).
        # Invalidate when claims change.
        self._signature_cache: Dict[
            Tuple[str, frozenset[str], Tuple[str, ...]], SkillSignature
        ] = {}
        
        
    # ------------------------------------------------------------------
    # Input intake (pre-epistemic)
    # ------------------------------------------------------------------

    def queue_input(self, obj: Any) -> None:
        """
        Normalize external inputs into structural availability.

        Supported shapes:
        - pathlib.Path (file or directory, non-recursive)
        - dict (explicit structural availability)

        This method:
        - populates self.inputs and self.available_fields
        - does NOT create claims
        - does NOT inspect file contents
        - emits non-blocking diagnostics for unsupported inputs
        """
        
        if isinstance(obj, NormalizedFileQueue):
            for field, p in obj.files:
                self._register_structural_field(
                    field=field,
                    source="resolver_input",   # structural provenance, not caller identity
                    structured=True,
                    fetchable=False,
                    value=p,
                )
            for msg in obj.diagnostics:
                self.add_diagnostic(msg)
            return

        # -------------------------
        # Support for iterables
        # -------------------------        if isinstance(obj, (list, tuple)):
        if isinstance(obj, (list, tuple)):
            for item in obj:
                self.queue_input(item)
            return

        # -------------------------
        # dict input
        # -------------------------
        if isinstance(obj, dict):
            for field, meta in obj.items():
                # Minimal normalization: trust caller, but stay structural
                self.inputs.add(field)
                self.available_fields[field] = {
                    "source": meta.get("source", "dict"),
                    "confidence": meta.get("confidence"),
                    "structured": meta.get("structured", True),
                    "fetchable": meta.get("fetchable", False),
                }
            return

        # -------------------------
        # Unsupported input
        # -------------------------
        self.add_diagnostic(
            f"queue_input: unsupported input type {type(obj).__name__}; skipping"
        )

    def _register_structural_field(
        self,
        *,
        field: str,
        source: str,
        structured: bool,
        fetchable: bool,
        confidence: Optional[float] = None,
        value: Any | None = None,          # ← add
    ) -> None:
        self.inputs.add(field)
        self.available_fields[field] = {
            "source": source,
            "value": value,                # ← add
            "confidence": confidence,
            "structured": structured,
            "fetchable": fetchable,
        }
    
    def available_value(self, field: str, default=None):
        return self.available_fields.get(field, {}).get("value", default)    


    # ------------------------------------------------------------------
    # Claims handling
    # ------------------------------------------------------------------

    def merge_claims(self, claims: Claims) -> None:
        self.known.merge(claims)

        for field in claims.fields:
            if field not in self.available_fields:
                self._register_structural_field(
                    field=field,
                    source="claim",
                    structured=True,
                    fetchable=False,
                    value=[c.value for c in claims.get(field)],
                )

        self.inputs.update(claims.fields)
        self._signature_cache.clear()

    # ------------------------------------------------------------------
    # SkillSignature API
    # ------------------------------------------------------------------

    def skill_signature(self, descriptor) -> SkillSignature:
        """Return an opaque SkillSignature for this descriptor under current state."""
        produces = tuple(sorted(getattr(descriptor, "produces", []) or []))
        key = (descriptor.name, frozenset(descriptor.consumes), produces)
        cached = self._signature_cache.get(key)
        if cached is not None:
            return cached

        payload = {
            "inputs": self.effective_inputs_snapshot(descriptor.consumes),
            "produces": list(produces),
        }
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        sig = SkillSignature(skill_name=descriptor.name, digest=raw.hex())
        self._signature_cache[key] = sig
        return sig

    def has_executed(self, signature: SkillSignature) -> bool:
        return signature in self.executed_signatures

    def record_execution(self, signature: SkillSignature, result) -> None:
        """Record successful execution and capture any side effects."""
        self.executed_signatures.add(signature)
        self.skill_runs[signature.skill_name] = self.skill_runs.get(signature.skill_name, 0) + 1

        if getattr(result, "user_action", None) is not None:
            self.user_action = result.user_action

    # ------------------------------------------------------------------
    # Snapshotting for signatures (internal)
    # ------------------------------------------------------------------

    def effective_inputs_snapshot(self, fields: Iterable[str]) -> Dict[str, Any]:
        """Return a JSON-stable snapshot of consumed inputs."""
        snap: Dict[str, Any] = {}
        for f in sorted(fields):
            vals = self.known.get(f)
            snap[f] = [
                {
                    "value": self._hashable_value(v.value),
                    "provenance": v.provenance,
                    "confidence": (
                        v.effective_confidence() if hasattr(v, "effective_confidence") else v.confidence
                    ),
                    "semantic_type": self._hashable_value(v.semantic_type),
                }
                for v in vals
            ]
        return snap

    def _hashable_value(self, value: Any) -> Any:
        """Convert values into a JSON-stable representation suitable for signatures."""
        if isinstance(value, Path):
            # No filesystem I/O, no pathlib parsing (cross-platform).
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
