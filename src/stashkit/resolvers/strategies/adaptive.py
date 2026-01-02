from __future__ import annotations

from typing import List

from stashkit.state import ResolverState


class AdaptiveStrategy:
    """
    Adaptive resolution strategy.

    - Selects the next best skill based on declared cost and availability
    - Determines sufficiency based on unresolved required fields
    """

    def select_skill(self, state: ResolverState, eligible_skills: List):
        """
        Select the next skill to run.

        Current heuristic:
        - Prefer lowest cost
        - Stable ordering otherwise
        """

        if not eligible_skills:
            raise RuntimeError("select_skill called with no eligible skills")

        # Sort by declared cost (low < medium < high)
        def cost_rank(skill):
            cost = getattr(skill.descriptor, "cost", "medium")
            return {"low": 0, "medium": 1, "high": 2}.get(cost, 1)

        eligible_skills = sorted(eligible_skills, key=cost_rank)
        return eligible_skills[0]
