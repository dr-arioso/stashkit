from .barcode_scan_skill import BarcodeScanSkill
from .ocr_skill import OCRSkill
from .upc_skill import UPCSkill
from .db_lookup_skill import DBLookupSkill
from dataclasses import dataclass, field
from typing import Set

__all__ = [
    "BarcodeScanSkill",
    "OCRSkill",
    "UPCSkill",
    "DBLookupSkill",
]

@dataclass(frozen=True)
class SkillDescriptor:
    """
    Declarative description of a skill's epistemic capability.

    This object is:
      - inert
      - inspectable
      - resolver-facing
    """

    name: str

    requires: Set[str] = field(default_factory=set)
    produces: Set[str] = field(default_factory=set)


    def is_eligible(self, available_fields: Set[str]) -> bool:
        if not self.enabled:
            return False
        return self.requires.issubset(available_fields)
