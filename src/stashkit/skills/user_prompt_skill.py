from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Optional, Any

from stashkit.skills.base_skill import SkillDescriptor, SkillResult
from stashkit.claims import FieldValue, SemanticType
from stashkit.state import ResolverState


PromptFn = Callable[[ResolverState], Mapping[str, Any]]


@dataclass
class UserPromptSkill:
    """User input collection skill.

    This is a library-level bridge to whatever UI layer exists (CLI/TUI/GUI).
    It does not implement UI; instead it calls an injected PromptFn.

    Design constraints:
    - User-provided values are treated as authoritative for intent
    - Confidence defaults to 1.0
    - The resolver decides *what to ask for* by configuring the prompt function
      (e.g., based on missing required fields)
    """

    prompt_fn: PromptFn
    semantic_map: Optional[Mapping[str, str]] = None

    descriptor = SkillDescriptor(
        name="UserPromptSkill",
        requires={
            "user_prompt_text"
        },
        consumes={
            "user_prompt_text",
            "ui_elements",
            "illustration",
            "thumbnail",
        },
        produces=set(),   # determined by prompt_fn return keys
        cost="high",
        baseline_reliability=1.0,
    )


    def run(self, state: ResolverState) -> SkillResult:
        res = SkillResult()
        answers = dict(self.prompt_fn(state) or {})
        if not answers:
            return res

        for field, value in answers.items():
            sem = (self.semantic_map or {}).get(field, SemanticType.UNKNOWN)
            res.claims.add(
                field,
                FieldValue(
                    value=value,
                    provenance="UserPromptSkill",
                    confidence=1.0,
                    semantic_type=sem,
                ),
            )
            res.notes.append(f"user provided {field}")
        return res
