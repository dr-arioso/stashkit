from __future__ import annotations

from typing import Optional, Protocol, Any


class BarcodeScanAdapter(Protocol):
    """Adapter interface for barcode decoding engines.

    Implementations may wrap zbar/pyzbar, ZXing, native mobile scanners, etc.
    """

    name: str

    def decode_upc_ean(self, image_ref: Any) -> Optional[str]:
        """Return a normalized UPC/EAN digit string if found, else None."""
        ...
