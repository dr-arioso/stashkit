# Skills

**Status: Foundational — this document defines what Skills are in the StashKit architecture.**

Skills are the *capability layer* of StashKit.
They are the executable units that Resolvers reason over, schedule, and invoke.

Skills never control flow, assert sufficiency, or decide what happens next.

---

## Core Principle

> **Skills execute. Resolvers decide.**

This boundary is strict and intentional.

---

## What a Skill Is

A **Skill** is a self-contained, stateless execution unit that:

- consumes available evidence
- emits zero or more claims
- annotates claims with provenance, confidence, and semantic meaning
- may emit exploratory claims when explicitly permitted by the resolver
- is immutable after instantiation

Skills are designed to be:

- composable
- swappable
- testable
- domain-focused

---

## What a Skill Is Not

A Skill does **not**:

- decide whether it should run
- decide whether its output is sufficient
- schedule other Skills
- retry itself
- reason about resolver state
- own UX, logging, or policy decisions

If a component needs system authority, coordination, or memory, it does **not** belong at the Skill layer.

---

## Skills and Resolvers

Resolvers reason *over* Skills.

They use SkillDescriptors to:

- determine eligibility
- compare costs and reliability
- plan execution order
- interpret results

Skills never inspect or manipulate resolver internals.

---

## Skill Identity

Each Skill:

- owns a static SkillDescriptor
- exposes that descriptor for resolver inspection
- executes via a stable `run(...)` interface

The descriptor describes **capability**.
Execution fulfills that capability.

---

## Claims as Output

Skills emit **claims**, and nothing else.

Claims are the atomic epistemic unit of StashKit.
They are later merged, reconciled, accepted, or rejected by Resolvers.

Skills do not write directly to state.

---

## Asserted vs Exploratory Behavior

By default, Skills behave conservatively and emit only claims that satisfy their descriptor’s `produces` contract.

Resolvers may explicitly allow exploration for a given invocation.

When exploration is enabled:

- Skills may emit additional claims
- Such claims must be explicitly flagged as `exploratory`
- Exploratory claims are preserved but excluded from sufficiency by default

Exploration is a **resolver policy**, not a Skill attribute.

---

## Adapters and Infrastructure

Some Skills may delegate execution mechanics to helper components (historically called *adapters*).

These components:

- encapsulate external dependencies
- normalize protocol or API interactions
- contain no planning or decision logic

The Skill remains the unit of reasoning.

---

## Distribution and Ownership

Skills may originate from:

- StashKit core
- BoosterPacks
- Applications

As long as the Skill contract is honored, Resolvers treat all Skills uniformly.

---

## Related Documents

- **04a_SkillDescriptor_Contract** — authoritative semantics of SkillDescriptors
- **04b_Skill_Execution_Contract** — authoritative runtime behavior and claim semantics

---

## Summary

- Skills execute; Resolvers decide
- Skills emit claims, not decisions
- Capabilities are declared, not inferred
- Exploration is explicit and controlled
- Contracts are strict by design

