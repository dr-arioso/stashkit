from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class SemanticType(Enum):
    """
    High-level semantic classification for FieldValue contents.
    """

    TEXT = "text"                    # human-readable language
    NUMBER = "number"                # numeric quantities
    BOOLEAN = "boolean"
    MEDIA_REF = "media_ref"          # paths, URLs, blobs
    UNSTRUCTURED_TEXT = "unstructured_text"
    LEXICAL_LABEL = "lecical_label"
    UNKNOWN = "unknown"

    IDENTIFIER = "identifier"        # UPC, EAN, SKU, ISBN, UUID, etc.


@dataclass
class FieldValue:
    value: Any
    provenance: str
    confidence: Optional[float] = None
    semantic_type: SemanticType = SemanticType.TEXT

    def effective_confidence(self) -> float:
        """
        Returns a usable confidence value.

        A confidence of None indicates 'unspecified by producer' and
        defaults to 0.0 for interpretation purposes.
        """
        return self.confidence if self.confidence is not None else 0.0

    @classmethod
    def observed(
        cls,
        value: Any,
        *,
        provenance: str,
        confidence: float,
        semantic_type: SemanticType = SemanticType.TEXT,
    ) -> "FieldValue":
        """
        Construct a FieldValue from an explicit observation with
        calibrated confidence.
        """
        return cls(
            value=value,
            provenance=provenance,
            confidence=confidence,
            semantic_type=semantic_type,
        )

    @classmethod
    def asserted(
        cls,
        value: Any,
        *,
        provenance: str,
        semantic_type: SemanticType = SemanticType.TEXT,
    ) -> "FieldValue":
        """
        Construct a FieldValue asserted without confidence calibration.
        Confidence remains unspecified (None).
        """
        return cls(
            value=value,
            provenance=provenance,
            confidence=None,
            semantic_type=semantic_type,
        )


@dataclass
class Claims:
    def __init__(self):
        self.data: dict[str, list[FieldValue]] = {}
        self._fields_cache: set[str] | None = None

    """
    Aggregates FieldValue instances by field name.
    Multiple claims for the same field may coexist.
    """

    @property
    def fields(self) -> set[str]:
        if self._fields_cache is None:
            self._fields_cache = {k for k, v in self.data.items() if v}
        return self._fields_cache


    def add(self, field_name: str, fv: FieldValue) -> None:
        self.data.setdefault(field_name, []).append(fv)

    def add_value(
        self,
        field_name: str,
        value: Any,
        *,
        provenance: str,
        confidence: Optional[float] = None,
        semantic_type: SemanticType = SemanticType.TEXT,
    ) -> None:
        """
        Convenience wrapper around add() for easy-mode callers.
        """
        self.add(
            field_name,
            FieldValue(
                value=value,
                provenance=provenance,
                confidence=confidence,
                semantic_type=semantic_type,
            ),
        )

    def has(self, field_name: str) -> bool:
        return field_name in self.data and len(self.data[field_name]) > 0

    def get(self, field_name: str) -> List[FieldValue]:
        return self.data.get(field_name, [])
    
    def merge(self, other: "Claims") -> None:
        """
        Merge another Claims object into this one.

        Claims are accumulated, not adjudicated.
        Multiple FieldValue instances per field are preserved.
        """
        for k, vals in other.data.items():
            self.data.setdefault(k, []).extend(vals)
        self._fields_cache = None
