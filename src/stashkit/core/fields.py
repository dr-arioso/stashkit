# stashbench/fields.py
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple

@dataclass(frozen=True)
class StructuredFieldSpec:
    name: str
    python_type: type
    extensions: Tuple[str, ...]
    description: str


IMAGE_REF = StructuredFieldSpec(
    name="image_ref",
    python_type=Path,
    extensions=(".jpg", ".jpeg", ".png", ".webp", ".tiff"),
    description="Filesystem path to an image-like file, mechanically validated"
)

FIELD_REGISTRY = {
    IMAGE_REF.name: IMAGE_REF,
}
