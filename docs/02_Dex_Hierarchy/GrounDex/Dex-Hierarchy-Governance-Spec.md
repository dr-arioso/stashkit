# Dex Hierarchy Governance Specification

## Structural Rules for Dex Layering and Extension

**Status:** Stable
**Version:** 1.0
**Applies To:** LexiDex, GrounDex, MetaDex, AppDex, and future Dex layers
**Normative Language:** RFC 2119 (MUST, SHALL, SHOULD, MAY)

---

## 1. Purpose

This document defines **governance rules** for the Dex hierarchy, specifying how concepts are introduced, extended, and constrained across layers.

The goal is to:

* Preserve **clear separation of concerns**
* Prevent **semantic bleed** between Dex layers
* Enable **independent evolution and patentability** of each Dex
* Provide durable guidance for both human and automated contributors

This specification is **normative** and applies to all current and future Dex schemas.

---

## 2. Dex Hierarchy Overview

The Dex hierarchy is organized as a **layered abstraction stack**, where each layer introduces additional responsibilities without redefining or subsuming lower layers.

### 2.1 Current Layers

| Layer        | Primary Responsibility                         |
| ------------ | ---------------------------------------------- |
| **LexiDex**  | Canonical semantic lexicon                     |
| **GrounDex** | Behavioral configuration and optimization      |
| **MetaDex**  | Epistemic framing and contextual guidance      |
| **AppDex**   | Application behavior, structure, and workflows |

Each layer SHALL be treated as an **independent conceptual domain**.

---

## 3. Extension Principles (Normative)

### 3.1 Additive-Only Rule

A Dex layer SHALL extend its parent layer **additively only**.

A layer MUST NOT:

* Remove parent concepts
* Redefine parent semantics
* Narrow parent expressiveness

---

### 3.2 Local-First Extension Rule

Newly discovered concepts SHALL be introduced **at the lowest appropriate layer**.

A concept MUST remain local to a layer if:

* It is required to express that layer’s invention
* Removing it would weaken that layer’s claims
* Its reuse outside the layer is speculative or hypothetical

Upward promotion MUST NOT occur by default.

---

### 3.3 Promotion Criteria (Strict)

A concept MAY be promoted upward only if **all** of the following are true:

1. The concept is **domain-agnostic**
2. The concept is **descriptive, not operational**
3. At least **two concrete, non-hypothetical use cases** exist outside the originating layer
4. Promotion does not:

   * weaken separateness of inventions
   * force unintended inheritance on sibling layers

Failure of any criterion SHALL prohibit promotion.

---

## 4. Layer-Specific Responsibilities

### 4.1 LexiDex

LexiDex SHALL:

* Define canonical vocabulary and semantic categories
* Remain non-executive and non-operational
* Avoid behavioral, epistemic, or application logic

LexiDex MUST NOT:

* Encode optimization, enforcement, or runtime behavior

---

### 4.2 GrounDex

GrounDex SHALL:

* Encode behavioral configuration intent
* Describe optimization, harmonization, and stabilization
* Remain declarative and execution-neutral

GrounDex MUST NOT:

* Perform epistemic reasoning
* Encode application workflows
* Assume execution or orchestration semantics

---

### 4.3 MetaDex

MetaDex SHALL:

* Abstract epistemic guidance from external sources
* Frame how context, constraints, and expectations are conveyed
* Remain advisory rather than coercive

MetaDex MUST NOT:

* Execute behavioral enforcement
* Override GrounDex optimization intent
* Encode application control flow

---

### 4.4 AppDex

AppDex SHALL:

* Describe application structure, behavior, and state
* Model workflows, components, and transitions

AppDex MUST NOT:

* Redefine canonical semantics
* Perform behavioral normalization or epistemic framing

---

## 5. Patent Alignment Rule

During patent drafting or locking phases:

* Hierarchy refactors SHOULD be avoided
* Concept promotion MUST be treated as a **material change**
* Elegance SHALL be subordinated to **legal clarity**

If a conflict arises between abstraction purity and invention separateness, **separateness SHALL prevail**.

---

## 6. Documentation Requirements

Each Dex extension SHALL be accompanied by a **schema extension specification** that:

* Describes purpose and scope
* Enumerates normative concepts
* Explicitly states non-scope
* Justifies hierarchy placement

Undocumented extensions SHOULD be treated as provisional.

---

## 7. Change Control

Once a Dex schema is declared **locked**:

* Changes MUST be versioned
* Changes MUST be additive
* Breaking changes REQUIRE explicit justification

---

## 8. Rationale (Informative)

This governance model is designed to:

* Support long-lived schema evolution
* Enable independent patent strategies
* Allow partial adoption of the Dex stack
* Reduce contributor and tooling ambiguity

---

## 9. Status

This specification is **normative** and applies to all Dex layers beginning with GrounDex v1.

---

### End of Specification

Excellent — this neatly closes the loop and makes the architecture **explicit, enforceable, and future-proof**.

Below are **both deliverables**, written to drop straight into your repo with no hand-waving.

---

# 1. Addendum to **Dex-Hierarchy-Governance-Spec.md**

## Schema Authority and Source-of-Truth Rules

This section should be appended as a new normative section (recommended as **Section 10**).

---

## 10. Schema Authority and Source of Truth (Normative)

### 10.1 Authoritative Schema Location

For each Dex layer, there SHALL exist exactly **one authoritative schema definition**.

For all Dex layers governed by StashKit:

* The authoritative schema definitions SHALL reside within the **StashKit repository**
* Schemas SHALL be versioned and governed centrally
* No Dex-specific repository SHALL redefine its own schema independently

The StashKit repository SHALL be treated as the **system of record** for all Dex schemas.

---

### 10.2 Non-Authoritative Mirrors

Dex-specific repositories (e.g., GrounDex, MetaDex) MAY include **non-authoritative schema mirrors** for convenience, testing, or local tooling, provided that:

* The mirrored files are explicitly marked as **NON-AUTHORITATIVE**
* The authoritative source and version are clearly identified
* The mirrored files are not edited directly
* The repository documentation states that the schema is governed externally by StashKit

Failure to meet all of the above conditions SHALL render the mirror invalid.

---

### 10.3 Documentation Requirements

Dex-specific documentation MUST:

* Reference the authoritative schema by repository path and version
* Avoid embedding full schema definitions
* Treat schema files as external, governed artifacts

Documentation SHALL describe **semantics and constraints**, not reproduce schema syntax.

---

### 10.4 Change Control and Version Pinning

When a Dex implementation depends on a particular schema version:

* The dependency SHALL be explicitly version-pinned
* Schema upgrades SHALL be deliberate and documented
* Silent drift between schema versions MUST be avoided

---

### 10.5 Rationale (Informative)

This authority model ensures:

* Elimination of schema drift
* Clear ownership of semantic definitions
* Consistent patent alignment
* Long-term maintainability across multiple Dex implementations

---

# 2. **GrounDex Repository README.md**

## Relationship to StashKit and Schema Governance

This is a **repo-root `README.md`** for the GrounDex repository.

---

# GrounDex

## Overview

GrounDex is a behavioral configuration and optimization layer within the **StashKit Dex hierarchy**.

It provides mechanisms for expressing canonical, model-agnostic behavioral intent for generative inference systems and supports cross-model interoperability, optimization, and stabilization.

---

## Relationship to StashKit

GrounDex is **specified, governed, and versioned** by **StashKit**.

* The GrounDex schema is **not defined in this repository**
* The GrounDex specification is **not authored here**
* This repository consumes and implements GrounDex as defined upstream

The authoritative GrounDex schema and specification are maintained in the StashKit repository.

---

## Schema Authority

The authoritative GrounDex schema is defined in StashKit at:

```
stashkit/schemas/groundex/groundex_schema.fixed.yaml
stashkit/schemas/groundex/groundex_schema.min.json
```

Version: **v1.0 (LOCKED)**

Any schema files present in this repository are **non-authoritative mirrors** provided for convenience only.

Such files:

* MUST NOT be edited directly
* MUST clearly identify the authoritative source
* MUST match the pinned schema version exactly

---

## Documentation Authority

The normative GrounDex specification is defined in StashKit at:

```
stashkit/docs/02_Dex_Hierarchy/GrounDex/GrounDex-Schema-Spec.md
```

This repository’s documentation SHOULD reference, not reproduce, normative definitions.

---

## Intended Use of This Repository

This repository MAY contain:

* Reference implementations
* Tooling
* Examples
* Tests
* Integrations

This repository MUST NOT:

* Redefine GrounDex schema semantics
* Introduce hierarchy refactors
* Override StashKit governance rules

---

## Governance

All changes to GrounDex semantics, schema, or scope MUST occur through the StashKit governance process.

See:

```
stashkit/docs/02_Dex_Hierarchy/Dex-Hierarchy-Governance-Spec.md
```

---

## Status

This repository implements **GrounDex v1.0**, as governed by StashKit.
