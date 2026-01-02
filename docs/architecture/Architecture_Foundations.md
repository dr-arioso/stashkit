# Architecture Foundations

**Project:** StashKit / Barback  
**Last updated:** 2025-12-17

This document explains how to *think* about the architecture before explaining how to use it.
It is written for developers and maintainers.

You do not need to read this to use the code —  
but reading it will make the code much easier to understand, extend, and debug.

---

## 1. The Short Version

This project deliberately separates three concerns that are often mixed together in software systems:

- **What a thing is**
- **How we figure out what it is**
- **Which specific thing it turns out to be**

Keeping these separate avoids hidden assumptions, brittle pipelines, and premature identity commitment.

---

## 2. The Three Layers

### Ontology — *What kinds of things exist*
**(LexiDex)**

Ontology defines shared meaning:

- categories and polyhierarchies
- relationships and constraints
- common vocabulary across domains

Ontology answers:

> *What could this be?*

Ontology is:
- stable
- slow-changing
- independent of observation

Ontology does **not**:
- resolve instances
- manage uncertainty
- assign identity

---

### Ontogeny — *How something becomes known*
**(Resolvers + Skills)**

Ontogeny describes the process by which a specific thing becomes known over time under uncertainty.

Resolvers:
- start with incomplete or noisy information
- gather evidence using Skills
- balance information gain, cost, and confidence
- decide when knowledge is “sufficient”

Resolvers are **ontogeny optimization engines**.

They answer:

> *How do we most efficiently and safely come to know what this is?*

Resolvers:
- do not define ontology
- do not assign identity
- do not store durable knowledge

---

### Identity — *Which specific thing it is*
**(MuDex)**

Identity anchors a specific, reusable reference once something is known.

MuDex:
- defines unique identity bindings
- distinguishes “this instance” from “that instance”
- supports layered overlays (base / remote / local)
- remains auditable and correctable

Identity answers:

> *Which one is it, exactly?*

Identity is committed only when:
- uniqueness is established, or
- the user explicitly accepts it

---

## 3. Why This Separation Matters

Many systems collapse at least two of these layers:

- identity baked into ontology
- pipelines pretending to be classification
- identities committed before uncertainty is resolved

These shortcuts work — until they don’t.

By maintaining explicit boundaries:

- ontology remains clean and reusable
- resolution remains adaptive
- identity remains stable and trustworthy

---

## 4. Practical Consequences

This separation leads to concrete design choices:

- Skills are reusable across domains
- Resolvers reason over capabilities, not concrete types
- Fuzzing expands hypotheses but never asserts truth
- Confidence and provenance are first-class
- User input is authoritative about intent, not spelling
- Storage commitment is gated by sufficiency

These behaviors emerge naturally from the model.

---

## 5. Design Discipline

Nothing in this document is enforced by the type system.

Instead, this document establishes a **design discipline**:
- a shared mental model
- a way to detect conceptual drift
- a guide for future contributors

If a change blurs ontology, ontogeny, and identity,
it is a signal to slow down and reconsider.

---

## Summary

- **Ontology** defines what exists  
- **Ontogeny** optimizes how we come to know  
- **Identity** fixes which specific thing it is  

This separation is the architectural foundation of the project.
