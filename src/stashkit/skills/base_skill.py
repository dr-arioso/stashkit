from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol, Set
from stashkit.claims import Claims

@dataclass(frozen=True)
class SkillDescriptor:
    name: str
    requires: Set[str] = field(default_factory=set)
    consumes: Set[str] = field(default_factory=set)
    produces: Set[str] = field(default_factory=set)
    cost: str = "medium"  # low | medium | high
    baseline_reliability: float = 0.5
    max_runs: int | None = None

class StashSkill(Protocol):
    descriptor: SkillDescriptor
    def run(self, state: "ResolverState") -> "SkillResult":
        ...

@dataclass
class SkillResult:
    claims: Claims = field(default_factory=Claims)
    notes: list[str] = field(default_factory=list)

    # Capability advertisement (not claims, not evidence)
    # field_name -> metadata dict (source, confidence, structured, fetchable, ...)
    available_fields: dict[str, dict] | None = None

