# Skill Execution Contract

**Status: Authoritative — this document defines required runtime behavior
for all Skills in the StashKit ecosystem.**

This contract applies to all Skills, regardless of origin
(StashKit core, BoosterPacks, or application-specific).

---

## Core Principle

> **Skills execute. Resolvers decide.**

A Skill is an executable capability that emits claims.
It never plans, schedules, or evaluates system-level outcomes.

---

## 1. Skill Responsibilities

A Skill:

- consumes available evidence
- emits zero or more claims
- annotates claims with provenance, confidence, and semantic meaning
- may emit exploratory claims when explicitly permitted
- is immutable after instantiation

A Skill does **not**:

- reason about resolver state
- decide whether it should run
- schedule other skills
- assert sufficiency or completion
- mutate global state

If a component needs authority, memory, or coordination, it is **not** a Skill.

---

## 2. Execution Interface

All Skills implement the following interface:

```python
run(evidence, *, allow_exploration: bool = False) -> SkillResult
```

### Parameters

- **evidence**  
  A read-only view of available claims and structural fields.  
  The exact interface is intentionally minimal.

- **allow_exploration**  
  Resolver-controlled flag.  
  If `True`, the Skill may emit exploratory claims
  outside its descriptor’s `produces` contract.

Skills MUST treat `allow_exploration=False` as the default.

---

## 3. SkillResult and Claims

### SkillResult

A Skill returns a `SkillResult`, whose primary payload is **claims**.

Skills MUST NOT return:
- raw dictionaries
- ad-hoc data structures
- mutated state objects

### Claims

Claims are the atomic epistemic unit of StashKit.

Every claim includes:

- field name
- value
- confidence (0–1)
- provenance
- semantic type
- flags

---

## 4. Claim Flags

At minimum, the following flags are defined:

### `asserted`

- Claim satisfies the SkillDescriptor’s `produces` contract
- Eligible for resolver sufficiency and completion logic

### `exploratory`

- Claim lies outside the descriptor’s `produces` contract
- Emitted only when `allow_exploration=True`
- Preserved, but excluded from sufficiency by default
- May trigger follow-on skills or confirmation

Skills MUST explicitly flag claims; no flag is implicit.

---

## 5. Descriptor vs Execution Boundary

- **SkillDescriptor** defines *capability*
- **Skill execution** defines *behavior*

Descriptors are:
- static
- immutable
- resolver-facing

Execution behavior:
- may vary per invocation
- is governed by resolver policy
- must not mutate descriptors

---

## 6. Exploration Semantics

Exploration is a **runtime policy**, not a skill attribute.

- Skills do not decide when exploration is appropriate
- Resolvers explicitly enable exploration per invocation
- Skills may emit additional claims when permitted
- All exploratory claims must be flagged

This enables:

- conservative default behavior
- controlled hypothesis generation
- safe incremental enrichment

---

## 7. Authority Boundaries

- Skills are domain-aware but system-dumb
- Skills may specify *what* and *where* to query
- Skills do not select backends opportunistically
- Skills may delegate mechanics to StashBench

StashBench provides execution machinery.
Resolvers provide planning and authority.

---

## 8. Easy Mode Guarantee

The default invocation:

```python
skill.run(evidence)
```

must be:

- safe
- conservative
- deterministic
- free of hidden side effects

Advanced behavior is opt-in and explicit.

---

## Summary

- Skills emit claims — nothing else
- Exploration is resolver-controlled
- Asserted vs exploratory claims are explicit
- Descriptors define promises; execution fulfills them
- Authority boundaries are strict

This contract is intentionally narrow.
Violations should be treated as architectural errors.

