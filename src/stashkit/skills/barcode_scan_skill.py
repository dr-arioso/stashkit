from __future__ import annotations

from typing import Iterable, List, Optional, Any

from stashkit.skills.base_skill import StashSkill, SkillDescriptor, SkillResult
from stashkit.claims import FieldValue, SemanticType
from stashkit.runtime.checkpoint import checkpoint


class BarcodeScanSkill(StashSkill):
    """
    Attempt to extract a UPC/EAN barcode from an image using one or more
    barcode decoding adapters.

    Easy mode:
        BarcodeScanSkill()

    Advanced mode:
        BarcodeScanSkill(adapters=[CustomAdapter(), ...])
    """

    descriptor = SkillDescriptor(
        name="BarcodeScanSkill",
        requires={"image_ref"},
        consumes={"image_ref"},
        produces={"upc_code"},
        cost=0.1,
        baseline_reliability=0.95,
    )

    def __init__(self, adapters: Optional[Iterable[Any]] = None):
        if adapters is None:
            adapters = self._default_adapters()
        self.adapters: List[Any] = list(adapters)

    @staticmethod
    def _default_adapters() -> List[Any]:
        adapters: List[Any] = []

        # Fast, local, best UX when available
        try:
            from stashkit.skills.barcode_scan_pyzbar_adapter import PyzbarAdapter
            adapters.append(PyzbarAdapter())
        except Exception:
            pass

        # Clean fallback (pure wheel)
        try:
            from stashkit.skills.barcode_scan_zxing_cpp_adapter import ZXingCPPAdapter
            adapters.append(ZXingCPPAdapter())
        except Exception:
            pass

        return adapters

    def run(self, state) -> SkillResult:
        res = SkillResult()

        image_ref = state.available_value("image_ref")
        if not image_ref:
            return res

        missing_dependencies = []

        for adapter in self.adapters:
            try:
                result = adapter.decode_upc_ean(image_ref)
            except Exception as e:
                checkpoint(
                    verbosity=state.verbosity,
                    severity="warning",
                    context="BarcodeScanSkill",
                    notes=[f"{adapter}: unexpected error — {e}"],
                )
                continue

            if isinstance(result, dict):
                status = result.get("status")
                if status == "dependency_missing":
                    missing_dependencies.append(result.get("detail"))
                checkpoint(
                    verbosity=state.verbosity,
                    severity="warning",
                    context="BarcodeScanSkill",
                    notes=[f"{adapter}: {status} — {result.get('detail')}"],
                )
                continue

            if isinstance(result, str):
                res.claims.add(
                    "upc_code",
                    FieldValue(
                        value=result,
                        provenance=f"BarcodeScanSkill:{adapter}",
                        confidence=0.95,
                        semantic_type=SemanticType.IDENTIFIER,
                    ),
                )
                return res

        if missing_dependencies:
            res.needs_user_action(
                action="install_barcode_dependencies",
                context=missing_dependencies,
            )

        return res
