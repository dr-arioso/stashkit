from __future__ import annotations

from stashkit.state import ResolverState
from stashkit.skills.base_skill import SkillResult
from stashkit.stashbench import StashBench
from pathlib import Path
from typing import Any

class BaseResolver:
    """Generic resolver loop.

    Key invariant:
    - Eligibility is structural and cheap (requires satisfied, max_runs).
    - Execution identity is handled via ResolverState.SkillSignature.
    """

    def __init__(self, skills=None, strategy=None, max_steps: int = 25):
        self.skills = skills or []
        self.strategy = strategy
        self.max_steps = max_steps
        
    # -------------------------------------------------
    # Hook dispatch (private, optional by presence)
    # -------------------------------------------------

    def _maybe(self, hook: str, *args) -> None:
        fn = getattr(self, hook, None)
        if fn is not None:
            fn(*args)        

    def eligible_skills(self, state: ResolverState):
        eligible = []

        state.add_trace(
            f"available at eligibility: "
            f"inputs={state.inputs}, "
            f"known={state.known.fields}, "
            f"structural={set(state.available_fields.keys())}"
        )
        available_structural_fields = set(state.available_fields.keys())
        
        eligible = []
        for sk in self.skills:
            desc = sk.descriptor

            if desc.requires:
                eligible_flag = desc.requires.issubset(available_structural_fields)
            else:
                if desc.consumes:
                    eligible_flag = bool(desc.consumes & available_structural_fields)
                else:
                    eligible_flag = True  # truly ambient skill

            if eligible_flag:
                eligible.append(sk)
        return eligible

    def choose_next_skill(self, state: ResolverState, eligible):
        if self.strategy is None:
            return eligible[0] if eligible else None
        return self.strategy.select_skill(state, eligible)


    def resolve(self, state_or_input: Any, *, verbosity: int = 0) -> ResolverState:
        if isinstance(state_or_input, ResolverState):
            state = state_or_input
        else:
            state = ResolverState(verbosity=verbosity)

            if isinstance(state_or_input, (str, Path)):
                nfq = StashBench.data.filesystem.normalize_file_queue(
                    state_or_input,
                    as_field="image_ref",
                    recurse=False,
                    strict=False,
                )
                state.queue_input(nfq)
            else:
                state.queue_input(state_or_input)

        return self._resolve(state)


    def _resolve(self, state: ResolverState) -> ResolverState:
        """
        Canonical resolver entry point.

        Accepts:
        - ResolverState
        - Path
        - dict

        Normalizes input into ResolverState, then delegates to _resolve().
        """
        state.add_trace("resolve: start")
        self._maybe("on_resolve_start", state)

        steps = 0
        while steps < self.max_steps:

            if self.is_sufficient(state):
                self._maybe("on_sufficient", state)
                state.add_trace(f"resolve: complete -> stop (steps={steps})")
                break

            eligible = self.eligible_skills(state)
            if not eligible:
                state.no_new_execution_opportunities = True
                self._maybe("on_exhausted", state)
                state.add_trace("resolve: no eligible skills -> stop")
                break

            # choose an unexecuted opportunity
            chosen = None
            chosen_sig = None
            while eligible:
                sk = self.choose_next_skill(state, eligible)
                if sk is None:
                    break

                sig = state.skill_signature(sk.descriptor)
                if state.has_executed(sig):
                    eligible.remove(sk)
                    continue

                chosen = sk
                chosen_sig = sig
                break

            if chosen is None:
                state.no_new_execution_opportunities = True
                self._maybe("on_exhausted", state)
                state.add_trace(
                    "resolve: no new execution opportunities (all eligible skills exhausted) -> stop"
                )
                break

            d = chosen.descriptor
            state.add_trace(f"run: {d.name} (sig={chosen_sig.short()}...)")

            result = chosen.run(state)
            state.record_execution(chosen_sig, result)

            claims = getattr(result, "claims", None)
            if claims:
                state.merge_claims(claims)

            self._maybe("after_step", state)
            steps += 1

        self._maybe("on_resolve_end", state)
        state.add_trace(f"resolve: end (steps={steps})")
        return state

        
    def is_sufficient(self, state: ResolverState) -> bool:
        raise NotImplementedError("Resolvers must define is_sufficient()")
