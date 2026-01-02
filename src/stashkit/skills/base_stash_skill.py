# stashdex/skills/base_stash_skill.py
# 2nd/new iteration of Skill contract

from __future__ import annotations
from abc import ABC, abstractmethod


class BaseStashSkill(
    allow_exploration : bool = False
):
    descriptor: SkillDescriptor

    @property
    def name(self) -> str:
        return self.descriptor.name

    @property
    def requires(self) -> set[str]:
        return self.descriptor.requires

    @property
    def produces(self) -> set[str]:
        return self.descriptor.produces

    @property
    def cost(self) -> float | None:
        return getattr(self.descriptor, "cost", None)


    @abstractmethod
    def run(self, context) -> None:
        """
        Attempt to produce new evidence.

        Returned in a SkillResult, made up primarily of Claims
        """
        raise NotImplementedError
