# stashbench/filesystem.py
from pathlib import Path
from typing import Iterable, List, Tuple
from PIL import Image

from stashkit.core.fields import FIELD_REGISTRY, StructuredFieldSpec


class NormalizedFileQueue:
    def __init__(self):
        self.files: List[Tuple[str, Path]] = []
        self.diagnostics: List[str] = []


def normalize_file_queue(
    paths: str | Path | Iterable[str | Path],
    *,
    as_field: str = "image_ref",
    recurse: bool = False,
    strict: bool = False,
) -> NormalizedFileQueue:
    """
    Normalize filesystem inputs into a queue of structurally valid files
    for a declared structured field (e.g. image_ref).
    """
    result = NormalizedFileQueue()
    
    if isinstance(paths, (str, Path)):
        paths = [paths]    

    if as_field not in FIELD_REGISTRY:
        raise ValueError(f"Unknown structured field: {as_field}")

    spec: StructuredFieldSpec = FIELD_REGISTRY[as_field]

    def handle_path(p: Path):
        if not p.is_file():
            return

        if spec.extensions and p.suffix.lower() not in spec.extensions:
            msg = f"{p}: extension not valid for {as_field}"
            if strict:
                result.diagnostics.append(msg)
                return
            result.diagnostics.append(msg)
            return

        # Header validation via Pillow
        try:
            with Image.open(p) as img:
                img.verify()
        except Exception as e:
            msg = f"{p}: failed {as_field} header validation ({e})"
            if strict:
                result.diagnostics.append(msg)
                return
            result.diagnostics.append(msg)
            return

        result.files.append((as_field, p))

    for raw in paths:
        p = Path(raw)
        if p.is_file():
            handle_path(p)
        elif p.is_dir():
            try:
                for child in p.iterdir():
                    if child.is_file():
                        handle_path(child)
            except Exception as e:
                result.diagnostics.append(
                    f"Failed to enumerate directory {p}: {e}"
                )
        else:
            result.diagnostics.append(f"Unsupported path input: {p}")

    return result
