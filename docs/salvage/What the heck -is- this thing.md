# Adaptive scoring interplay: BarcodeScanSkill vs OCRSkill

This is a practical note for expected behavior under `AdaptiveStrategy` (stashkit/resolvers/strategies/adaptive.py).

## Key facts encoded in descriptors

- `BarcodeScanSkill`
  - `cost="low"`
  - `baseline_reliability=0.98`
  - `produces={"upc_code"}`
  - `consumes={"image_ref"}`

- `OCRSkill`
  - `cost="medium"`
  - `baseline_reliability=0.70`
  - `produces={"raw_ocr_text","raw_barcode_text"}`
  - `consumes={"image_ref"}`

- `UPCSkill`
  - `cost="low"`
  - `baseline_reliability=0.95`
  - `produces={"upc_code"}`
  - `consumes={"raw_upc","raw_barcode_text"}`

## Typical Barback progression (starting from `image_ref` only)

1) Resolver needs `upc_code` (directly or indirectly), so any skill producing `upc_code` gets high "coverage".
2) `BarcodeScanSkill` produces `upc_code` directly at low cost and high reliability.
3) `OCRSkill` produces inputs that *may* enable `UPCSkill` to produce `upc_code`, but at higher cost and lower reliability.
4) Result: AdaptiveStrategy should prefer:
   - `BarcodeScanSkill` first
   - then `DBLookupSkill` (once `upc_code` exists)
   - then `OCRSkill` only if barcode scan fails to produce `upc_code`

## Why OCR still matters

- OCR extracts brand / product-name signals even when barcodes fail or are absent.
- OCR may surface a printed UPC digits line (human-readable) that `UPCSkill` can normalize.
- OCR is therefore the "fallback acquisition" skill, not the first-line barcode decoder.

## Configuration note

If you want OCR to be attempted earlier for label-driven resolution, increase OCR's score by:
- lowering cost to "low" (not recommended generally), or
- increasing baseline_reliability (only if you have a strong OCR engine+workflow), or
- adjusting AdaptiveStrategy weights in Barback (not StashKit) via a custom strategy implementation.
