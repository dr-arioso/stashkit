# MetaDex Schemas

This directory contains **schema-level definitions** for **MetaDex artifacts** used throughout the **StashKit** ecosystem.

MetaDex schemas define **what kinds of machine-interpretable context artifacts exist** and **what structure they must follow** in order to reliably prime large language models (LLMs).

MetaDex artifacts are intentionally:

- **descriptive**, not procedural  
- **inert**, not executable  
- **reusable** across projects and domains  
- **safe to load into LLM context**, without inducing control, authority, or behavior  

If a file in this directory were removed, **no application logic should break** — only **context fidelity and interpretive stability** would degrade.

---

## Core Principle (MetaDex v2.0)

> **MetaDex exists for one purpose: to reliably prime LLM interpretation by preventing default epistemological collapse.**

As of **MetaDex v2.0**, this principle is enforced **structurally rather than by convention**.

Any artifact that does not reliably perturb default LLM assumptions is **not a valid MetaDex**, regardless of how well-documented it may be.

---

## BaseMetaDex (v2.0)

`base_metadex_v2.0.schema.json`

Defines the **foundational contract** shared by all MetaDex artifacts.

BaseMetaDex answers the question:

> **“What does it mean for something to be a MetaDex at all?”**

### What BaseMetaDex guarantees

Every MetaDex conforming to BaseMetaDex v2.0 must declare:

- **identity and versioning**
- **purpose and non-goals**
- a **mandatory epistemic core**, consisting of:
  - **semantic invariants**
  - **non-equivalences**
  - **assumption surface areas**

The epistemic core is **constitutive**, not advisory.  
If it is absent, the artifact is **not a valid MetaDex**.

BaseMetaDex explicitly forbids:

- procedural logic  
- execution semantics  
- priority or override rules  
- authority assignment  

---

## PersonaMetaDex (v2.0)

`PersonaMetaDex_v2.0.schema.json`

Defines the structure for **describing personas as inert interpretive lenses**, not agents.

PersonaMetaDex is used to describe:

- roles (e.g., examiner, adversarial counsel)
- domains of expertise
- incentives and biases
- explicit boundaries and non-capabilities

PersonaMetaDex **does not**:

- assign authority  
- define interaction modes  
- trigger behavior  
- specify how personas should be applied  

PersonaMetaDex answers the question:

> **“Who exists in the interpretive landscape, and how must their presence not be misunderstood?”**

### Why PersonaMetaDex requires an epistemic core

Personas are one of the strongest triggers for LLM misinterpretation.  
Without explicit epistemic perturbation, LLMs will default to treating personas as:

- agents  
- speakers  
- authorities  
- instruction sources  

For this reason, PersonaMetaDex **inherits BaseMetaDex v2.0** and **requires a full epistemic core** clarifying that personas are descriptive only.

---

## Relationship to MuDex

**MetaDex describes context.**  
**MuDex governs interpretive transformation.**

- MetaDex **stabilizes interpretation**.  
- MuDex **constrains how interpretation may change across modes, roles, or phases**.

Here, “procedural” (as applied to MuDex) means **defining permissible interpretive transformations**,  
*not* specifying executable steps, control flow, or decision logic.

This separation is intentional and critical.

PersonaMetaDex describes *what personas are*.  
MuDex artifacts (e.g., FishbowlDiscussionMuDex) describe *how personas may be used*.

---

## When to Add PersonaDescriptorMuDex (and When Not To)

A PersonaDescriptorMuDex should **not** be introduced lightly.

Do **not** add PersonaDescriptorMuDex if you only need to:

- describe personas  
- select personas via prompt or convention  
- constrain interaction using an existing MuDex  

Consider adding PersonaDescriptorMuDex **only if** you need to encode policies *about persona usage itself*, such as:

- restricting when a persona may be used  
- constraining which interaction modes a persona supports  
- defining persona lifecycle state (active, deprecated, historical)  
- shaping persona output types independent of interaction mode  

If you are unsure whether you need PersonaDescriptorMuDex, you probably do not.

---

## Design Principle

> **MetaDex describes reality.**  
> **MuDex describes change.**  
> **Authority always remains external.**

If you feel tempted to blur these lines, pause and reconsider the abstraction boundary.

---

## Versioning Note: MetaDex v1.x → v2.0

MetaDex v2.0 introduces a **mandatory epistemic core**.

This change reflects observed failure modes in v1.x, where descriptive context was silently misinterpreted by LLMs as execution, authority, or instruction.

### What changed

- Epistemic perturbation is now **structural**, not optional
- All MetaDex artifacts must include:
  - semantic invariants
  - non-equivalences
  - assumption surface areas

### What did not change

- MetaDex remains descriptive and non-executory
- MetaDex does not control behavior
- MetaDex does not replace prompts or MuDex

MuDex remains unchanged by this transition.

---

