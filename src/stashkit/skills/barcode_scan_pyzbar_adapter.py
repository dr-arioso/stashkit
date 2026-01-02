
from __future__ import annotations
from typing import Any, Optional, Dict

class PyzbarAdapter:
    name = "pyzbar/zbar"

    def decode_upc_ean(self, image_ref: Any) -> Optional[str | Dict[str, str]]:
        try:
            from PIL import Image
            from pyzbar.pyzbar import decode
        except Exception as e:
            return {"status": "dependency_missing", "detail": str(e)}

        try:
            img = Image.open(str(image_ref)).convert("L")
        except Exception as e:
            return {"status": "image_load_error", "detail": str(e)}

        try:
            results = decode(img)
        except Exception as e:
            return {"status": "runtime_error", "detail": str(e)}

        if not results:
            return None

        for r in results:
            digits = "".join(c for c in r.data.decode(errors="ignore") if c.isdigit())
            if len(digits) in (12, 13):
                return digits

        return None
