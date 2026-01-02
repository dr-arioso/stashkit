from __future__ import annotations
from typing import Iterable, Any, List, Optional

from stashkit.skills.base_skill import SkillDescriptor, SkillResult
from stashkit.claims import FieldValue, SemanticType
from stashkit.state import ResolverState
from stashkit.runtime.checkpoint import checkpoint


class OCRSkill:
    descriptor = SkillDescriptor(
        name="OCRSkill",
        requires={"image_ref"},
        consumes={"image_ref"},
        produces={"raw_ocr_text"},
        cost="medium",
        baseline_reliability=0.7,
    )

    def __init__(self, adapters: Optional[Iterable[Any]] = None):
        if adapters is None:
            adapters = self._default_adapters()
        self.adapters: List[Any] = list(adapters)

    @staticmethod
    def _default_adapters() -> List[Any]:
        adapters: List[Any] = []

        try:
            from stashkit.skills.ocr_tesseract_adapter import TesseractAdapter
            adapters.append(TesseractAdapter())
        except Exception:
            pass

        return adapters

    def run(self, state: ResolverState) -> SkillResult:
        res = SkillResult()
        image_ref = state.available_value("image_ref")
        if not image_ref:
            return res
            
        for ad in self.adapters:
            try:
                result = ad.extract_text(image_ref)
            except Exception as e:
                checkpoint(
                    verbosity=state.verbosity,
                    severity="warning",
                    context="OCRSkill",
                    notes=[f"{ad}: unexpected error — {e}"],
                )
                continue

            if isinstance(result, dict):
                res.notes.append(
                    f"OCRSkill ({ad}) unavailable: "
                    f"{result.get('status')} — {result.get('detail','')}"
                )
                continue

            if not result or not result.strip():
                continue

            res.claims.add(
                "raw_ocr_text",
                FieldValue(
                    value=result,
                    provenance=f"OCRSkill:{ad}",
                    confidence=0.7,
                    semantic_type=SemanticType.UNSTRUCTURED_TEXT,
                ),
            )
            break

        return res
