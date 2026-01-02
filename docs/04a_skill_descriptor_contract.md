# SkillDescriptor Contract

**Status: Authoritative — this document defines the semantics of SkillDescriptors used by Resolvers.**

SkillDescriptors declare *what a Skill can do*, without invoking it.
Resolvers rely on these declarations for eligibility, planning, tracing, and safety.

---

## Core Principle

> **Resolvers reason over descriptors, not skill internals.**

Descriptors must therefore be honest, explicit, and conservative.

---

## Descriptor Scope

A SkillDescriptor:

- describes capability, not behavior
- is static and immutable
- is safe to inspect without executing code
- contains no execution policy

Descriptors do **not** change at runtime.

---

## Descriptor Fields

### `requires` — Hard requirements (AND semantics)

**Meaning**

- Structural fields that **must** be present for the Skill to be eligible.

**Eligibility rule**

- A Skill is eligible only if *all* fields in `requires` are structurally available.

**When to use**

- The Skill cannot operate meaningfully without these inputs.

**Example**

```python
requires = {"image_ref"}
```

---

### `consumes` — Soft input frontier (OR semantics)

**Meaning**

- Structural fields the Skill knows how to use.
- Expresses flexibility, not necessity.

**Eligibility rule**

- If `requires` is empty and `consumes` is non-empty, the Skill is eligible if *any* field in `consumes` is available.

**When to use**

- The Skill can operate on one of several alternative inputs.
- Common for inference or enrichment Skills.

**Example**

```python
requires = set()
consumes = {"image_ref", "text_block"}
```

---

### Ambient Skills (discouraged)

**Definition**

- `requires = ∅` and `consumes = ∅`

**Semantics**

- Skill is always eligible.

**Policy**

- Must be rare, deliberate, and explicitly documented.

---

### `produces` — Asserted output frontier

**Meaning**

- Fields the Skill may emit as **asserted claims**.

**Rules**

- Producing a field does not imply it was required or consumed.
- `produces` defines the *contractual promise* of the Skill.

Exploratory claims emitted at runtime are governed by execution policy and are **not** declared here.

---

### Optional Metadata

Descriptors may include additional metadata used for planning or comparison:

- `cost` — relative execution cost
- `baseline_reliability` — historical correctness of the Skill
- `max_runs` — guard against pathological retry loops

These values are advisory and comparative, not absolute.

---

## Validation Guidance

Skill authors are encouraged to validate descriptors during development:

- `requires ≠ ∅` → hard-require Skill
- `requires = ∅`, `consumes ≠ ∅` → soft-require Skill
- `requires = ∅`, `consumes = ∅` → ambient Skill (document explicitly)

---

## Anti-patterns

Do **not**:

- encode scheduling or priority intent in descriptors
- list fields in `requires` that are optional
- omit fields from `consumes` that the Skill may read
- treat `produces` as a dynamic or mutable set

---

## Relationship to Execution

- Descriptors declare *what may be asserted*
- Execution determines *what is actually asserted*
- Exploration and claim flags are runtime concerns

See **04b_Skill_Execution_Contract** for execution semantics.

---

## Summary

- Descriptors are static capability declarations
- Resolvers trust descriptors; Skills must not misrepresent them
- Execution policy does not belong in descriptors
- Honest descriptors enable safe planning

