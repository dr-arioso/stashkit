from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Protocol


class ProductLookupAdapter(Protocol):
    """Adapter interface for product lookups.

    Implementations may call OpenFoodFacts, Open Product Data, internal databases, etc.
    """

    name: str

    def lookup_by_upc(self, upc: str) -> Optional[Mapping[str, Any]]:
        """Return a mapping of field->value, or None if not found."""
        ...


@dataclass(frozen=True)
class LookupFailure:
    """Structured failure information for adapters."""

    code: str  # e.g. "dependency_missing", "network_error", "rate_limited"
    detail: str


class StubProductLookupAdapter:
    """In-memory adapter used for local tests and scaffolding."""

    name = "stub"

    def __init__(self, records: Optional[Mapping[str, Mapping[str, Any]]] = None):
        self._records = dict(records or {})

    def lookup_by_upc(self, upc: str) -> Optional[Mapping[str, Any]]:
        return self._records.get(str(upc))
