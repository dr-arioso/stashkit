from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

from stashkit.skills.db_lookup_adapters import LookupFailure


class OpenFoodFactsAdapter:
    """OpenFoodFacts lookup adapter.

    Uses the OpenFoodFacts public API to retrieve product data by barcode.

    Notes:
    - Coverage is best for food/grocery items; alcohol coverage varies.
    - This adapter normalizes a *subset* of fields into StashKit-friendly keys.
    """

    name = "openfoodfacts"

    def __init__(self, *, timeout_s: float = 12.0, user_agent: str = "StashKit/0.x (barback)"):
        self.timeout_s = float(timeout_s)
        self.user_agent = user_agent
        
    def advertised_fields(self) -> Mapping[str, Mapping[str, Any]]:
        return {
            "ingredients": {
                "confidence": 0.9,
                "structured": False,
                "fetchable": True,
            },
            "nutrition_facts": {
                "confidence": 0.9,
                "structured": True,
                "fetchable": True,
            },
            "alcohol_by_volume": {
                "confidence": 0.6,
                "structured": True,
                "fetchable": True,
            },
        }


    def lookup_by_upc(self, upc: str) -> Optional[Mapping[str, Any]]:
        """Return normalized field->value mapping, or None if not found.

        On dependency or network issues, returns a dict with a reserved key
        '__failure__' containing a LookupFailure.
        """
        try:
            import requests  # type: ignore
        except Exception as e:
            return {"__failure__": LookupFailure(code="dependency_missing", detail=f"requests not available: {e}")}

        barcode = str(upc).strip()
        if not barcode:
            return None

        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        headers = {"User-Agent": self.user_agent}

        try:
            r = requests.get(url, headers=headers, timeout=self.timeout_s)
        except Exception as e:
            return {"__failure__": LookupFailure(code="network_error", detail=str(e))}

        if r.status_code == 404:
            return None

        if r.status_code in (429, 500, 502, 503, 504):
            return {"__failure__": LookupFailure(code="http_error", detail=f"{r.status_code} from OpenFoodFacts")}

        try:
            payload = r.json()
        except Exception as e:
            return {"__failure__": LookupFailure(code="parse_error", detail=str(e))}

        if payload.get("status") == 0:
            return None

        product = payload.get("product") or {}
        out: Dict[str, Any] = {}

        out["external_product_id"] = product.get("id") or product.get("_id") or barcode

        name = product.get("product_name") or product.get("product_name_en") or product.get("generic_name")
        if name:
            out["product_name"] = name

        brand = product.get("brands") or product.get("brand_owner")
        if brand:
            out["brand"] = str(brand).split(",")[0].strip()

        img = product.get("image_url") or product.get("image_front_url")
        if img:
            out["product_photo"] = img  # pointer, not binary

        qty = product.get("quantity")
        if qty:
            out["labeled_quantity"] = qty

        # Dimensions: OFF typically does not have reliable physical dims.
        # Keep hooks if present in custom fields.
        for k in ("height_mm", "width_mm", "depth_mm", "max_diameter_mm", "weight_g"):
            if k in product and product[k] is not None:
                out[k] = product[k]

        return out or None
