from __future__ import annotations
from typing import List, Optional
from stashkit.skills.base import StashSkill

class LinearStrategy:
    def choose(self, state, eligible: List[StashSkill]) -> Optional[StashSkill]:
        return eligible[0] if eligible else None
