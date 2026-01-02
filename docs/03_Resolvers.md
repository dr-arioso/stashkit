# Resolvers

> **Status:** Normative — this document describes how resolvers behave in StashKit today.

Resolvers are responsible for **turning partial information into resolved identity**.

They do not perform work themselves. They decide *what work to do next*, based on what is known, what is missing, and what is likely to be useful.

---

## TL;DR

* Resolvers operate on a `ResolverState`
* They select Skills based on declared capabilities
* They merge claims, track provenance and confidence
* They decide when resolution is sufficient
* They never mutate ontology or stash data directly

---

## What a Resolver Is

A Resolver is an **ontogeny engine**.

Given uncertain, partial, or conflicting inputs, it incrementally builds confidence in an entity’s identity by:

1. Inspecting the current state
2. Selecting an appropriate Skill
3. Running that Skill
4. Merging the results
5. Reassessing sufficiency

This process continues until:

* resolution criteria are met, or
* no further useful work can be done

---

## ResolverState

All resolution happens against a `ResolverState`.

The state contains:

* known claims (with provenance and confidence)
* unresolved required fields
* run history (to avoid unproductive repetition)
* diagnostics and trace information

Resolvers never operate on raw inputs directly. Inputs are first normalized into state.

This allows:

* reproducibility
* explainability
* interruption and inspection

---

## Strategies

Resolvers delegate *how* they select Skills to a **strategy**.

StashKit currently provides:

* **LinearStrategy** — run each eligible Skill once, in order
* **AdaptiveStrategy** — dynamically select the next Skill based on expected value

Strategies:

* are interchangeable
* do not change resolver contracts
* control iteration, not semantics

A resolver may expose a default strategy, but strategy selection is not a class fork.

---

## Skill Selection

Resolvers reason over **SkillDescriptors**, not Skill implementations.

Each SkillDescriptor declares:

* required inputs
* consumed inputs
* produced outputs
* relative cost
* baseline reliability

The resolver evaluates:

* which Skills are eligible given current state
* which have already run
* which are likely to advance resolution

Skills may be revisited if new inputs become available.

There is no fixed pipeline.

---

## Resolution Loop (Conceptual)

```text
while not sufficient:
    choose next Skill
    run Skill
    merge claims into state
    reassess sufficiency
```

This loop is intentionally simple.

All complexity lives in:

* the strategy
* the descriptors
* the sufficiency criteria

---

## Sufficiency

Resolvers decide when an entity is "resolved enough".

Sufficiency is:

* domain-dependent
* configurable
* explicit

Examples:

* "identity resolved"
* "identity + physical dimensions known"
* "user-confirmed resolution"

Resolvers may stop early or continue enrichment depending on configuration.

---

## What Resolvers Do *Not* Do

Resolvers do **not**:

* perform OCR or vision
* call databases directly
* mutate Dex schemas
* stash entities themselves

They coordinate work; they do not perform it.

---

## Composition and Specialization

Resolvers may be specialized by composition.

For example:

* `ItemResolver` → general identity resolution
* `ProductResolver` → product-specific sufficiency rules
* `BottleResolver` (in Barback) → bottle- and BoozeDex-specific behavior

Specialization happens by:

* selecting different Skills
* setting different sufficiency criteria
* choosing different defaults

Not by rewriting the resolution loop.

---

## Summary

Resolvers are the decision-making layer of StashKit.

They:

* operate on state
* reason over capabilities
* select work adaptively
* make explicit sufficiency decisions

This makes resolution observable, explainable, and extensible.
