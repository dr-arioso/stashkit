from __future__ import annotations

from typing import Iterable, List, Mapping, Optional

from stashkit.skills.base_skill import SkillDescriptor, SkillResult
from stashkit.claims import FieldValue, SemanticType
from stashkit.state import ResolverState
from stashkit.runtime.checkpoint import checkpoint

from stashkit.skills.db_lookup_adapters import ProductLookupAdapter, LookupFailure
from stashkit.skills.db_lookup_openfoodfacts_adapter import OpenFoodFactsAdapter


class DBLookupSkill:
    """Generic product database lookup skill.

    Purpose:
    - Consume authoritative identifiers (e.g., UPC/EAN)
    - Query one or more configured data sources via adapters
    - Emit structured product attributes when available

    Easy mode:
        DBLookupSkill()

    Advanced mode:
        DBLookupSkill(adapters=[MyAdapter(), ...])
    """

    descriptor = SkillDescriptor(
        name="DBLookupSkill",
        requires={"upc_code"},
        consumes={"upc_code"},
        produces={
            # identity / mapping
            "external_product_id",
            "product_name",
            "brand",
            "product_photo",
            "labeled_quantity",
            # physical hints (optional)
            "height_mm",
            "width_mm",
            "depth_mm",
            "max_diameter_mm",
            "weight_g",
        },
        cost=0.4,
        baseline_reliability=0.6,
    )

    def __init__(self, adapters: Optional[Iterable[ProductLookupAdapter]] = None):
        if adapters is None:
            adapters = self._default_adapters()
        self.adapters: List[ProductLookupAdapter] = list(adapters)

    @staticmethod
    def _default_adapters() -> List[ProductLookupAdapter]:
        return [OpenFoodFactsAdapter()]

    def run(self, state: ResolverState) -> SkillResult:
        res = SkillResult()

        upcs = state.available_value("upc_code", [])
        if not upcs:
            return res

        # Prefer most recent/highest-confidence UPC. For now, take last.
        upc = str(upcs[-1]).strip()

        if not upc:
            return res

        for adapter in self.adapters:
            record = adapter.lookup_by_upc(upc)
            if not record:
                continue

            failure = record.get("__failure__") if isinstance(record, Mapping) else None
            if isinstance(failure, LookupFailure):
                checkpoint(
                    verbosity=state.verbosity,
                    severity="warning",
                    context="DBLookupSkill",
                    notes=[f"{adapter.name}: {failure.code} — {failure.detail}"],
                )
                if failure.code == "dependency_missing":
                    res.needs_user_action(
                        action="install_db_lookup_dependencies",
                        context=[failure.detail],
                    )
                    return res
                continue

            for field, value in record.items():
                if field == "__failure__" or value is None:
                    continue

                res.claims.add(
                    field,
                    FieldValue(
                        value=value,
                        provenance=f"DBLookupSkill:{adapter.name}",
                        confidence=self._confidence_for(field),
                        semantic_type=self._semantic_for(field),
                    ),
                )
            if hasattr(adapter, "advertised_fields"):
                advertised = adapter.advertised_fields()
                if advertised:
                    res.available_fields = {
                        field: {
                            **meta,
                            "source": adapter.name,
                        }
                        for field, meta in advertised.items()
                    }            
            state.add_trace(
                f"DBLookupSkill: adapter={adapter.name}, has_advertised={hasattr(adapter, 'advertised_fields')}"
            )
            return res
            # Advertise additional fields this adapter can provide
        return res

    def _semantic_for(self, field: str) -> str:
        if field in ("height_mm", "width_mm", "depth_mm", "max_diameter_mm", "weight_g"):
            return SemanticType.MEASUREMENT
        if field in ("product_name", "brand", "labeled_quantity"):
            return SemanticType.LEXICAL_LABEL

        # Keep compatibility with your evolving SemanticType enum:
        if field in ("external_product_id",):
            return getattr(SemanticType, "IDENTIFIER", SemanticType.UNKNOWN)
        if field in ("product_photo",):
            return getattr(SemanticType, "MEDIA_REF", SemanticType.UNKNOWN)
        return SemanticType.UNKNOWN

    def _confidence_for(self, field: str) -> float:
        if field in ("product_name", "brand"):
            return 0.7
        if field in ("external_product_id", "product_photo", "labeled_quantity"):
            return 0.6
        if field in ("height_mm", "width_mm", "depth_mm", "max_diameter_mm", "weight_g"):
            return 0.4
        return 0.5
