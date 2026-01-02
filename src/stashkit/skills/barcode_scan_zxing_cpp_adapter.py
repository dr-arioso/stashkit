from __future__ import annotations

from typing import Optional, Any

class ZXingCPPAdapter:
    """
    Pure pip-installable barcode decoder using the zxing-cpp Python wheels.
    This has no system-level dependencies and works on all platforms.

    It is less reliable than ZBar for UPC/EAN on curved/glare surfaces,
    but provides broad fallback coverage.
    """

    name = "zxing-cpp"

    def __init__(self):
        try:
            from zxingcpp import read_barcodes  # type: ignore
            self._read_barcodes = read_barcodes
            self.available = True
        except Exception:
            self.available = False
            self._read_barcodes = None

    def decode_upc_ean(self, image_ref: Any) -> Optional[str]:
        """
        Return a normalized UPC/EAN digit string, or None if none can be decoded.
        """

        if not self.available:
            # Adapter is present but backend unavailable
            return {"status": "dependency_missing", "detail": "zxing-cpp not installed"}

        from pathlib import Path

        try:
            from PIL import Image
        except Exception as e:
            return {"status": "dependency_missing", "detail": str(e)}

        # Load image
        try:
            if isinstance(image_ref, (str, Path)):
                img = Image.open(str(image_ref))
            else:
                img = image_ref  # assume PIL.Image.Image
        except Exception as e:
            return {"status": "invalid_image", "detail": str(e)}

        try:
            results = self._read_barcodes(img)
        except Exception as e:
            return {"status": "runtime_error", "detail": str(e)}

        if not results:
            return None

        # Try to extract digits from EAN/UPC results first
        for r in results:
            fmt = getattr(r, "format", None)
            txt = getattr(r, "text", "") or ""
            digits = "".join(c for c in txt if c.isdigit())

            if fmt in ("EAN_13", "EAN_8", "UPC_A") and len(digits) in (12, 13):
                return digits

        # Fallback: any symbology producing a reasonable digit sequence
        for r in results:
            txt = getattr(r, "text", "") or ""
            digits = "".join(c for c in txt if c.isdigit())
            if len(digits) >= 8:
                return digits

        return None
