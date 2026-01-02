from __future__ import annotations

from typing import Optional
from stashkit.skills.base_skill import SkillDescriptor, SkillResult
from stashkit.claims import FieldValue, SemanticType
from stashkit.state import ResolverState


class UPCSkill:
    """Generic UPC/EAN normalization skill.

    Library-level skill:
    - Domain-agnostic
    - No OCR or vision
    - No fuzzing of numeric identifiers
    - Safe for any ProductResolver

    Consumes pre-extracted textual or numeric signals.
    """

    descriptor = SkillDescriptor(
        name="UPCSkill",
        requires=set(),  # opportunistic
        consumes={
            "raw_upc",
            "raw_barcode_text",
        },
        produces={
            "upc_code",
        },
        cost="low",
        baseline_reliability=0.95,
    )

    def run(self, state: ResolverState) -> SkillResult:
        res = SkillResult()

        raw_values = [
            str(raw)
            for field in ("raw_upc", "raw_barcode_text")
            for raw in state.available_value(field, [])
        ]


        if not raw_values:
            return res

        for raw in raw_values:
            normalized = self._normalize(raw)
            if not normalized:
                continue

            res.claims.add(
                "upc_code",
                FieldValue(
                    value=normalized,
                    provenance="UPCSkill",
                    confidence=0.95,
                    semantic_type=SemanticType.FORMAL_IDENTIFIER,
                ),
            )
            res.notes.append(f"normalized UPC/EAN candidate: {normalized}")

        return res

    def _normalize(self, raw: str) -> Optional[str]:
        digits = "".join(c for c in raw if c.isdigit())
        if len(digits) in (12, 13):
            return digits
        return None
