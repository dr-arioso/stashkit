# ProjectMetaDex

ProjectMetaDex is a structured, explicit configuration document that describes
what a project is and how it should be reasoned about and structured.

It is intended to preserve architectural intent across sessions, collaborators,
and AI-assisted work.

## What belongs in a ProjectMetaDex

### Semantic and reasoning conventions

A ProjectMetaDex may describe semantic disciplines that affect how concepts, predicates, and names are chosen—particularly in systems where precision is required to prevent conceptual collapse or unintended equivalence.


Typical contents include:

- Project purpose and scope
- Architectural constraints and invariants
- Implementation direction (preferred approaches within the architecture)
- Domain conventions
- Explicit non-goals
- Optionally, a small set of recorded architectural decisions

ProjectMetaDex does not imply execution order or workflow; architectural elements may interact non-linearly unless explicitly constrained.

## Architectural constraints vs implementation direction

- **Architectural constraints** describe structural commitments that must not be violated.
- **Implementation direction** describes preferred structural and semantic approaches within those constraints.

This distinction is intentional. ProjectMetaDex is not a task list.

## Decision record (optional)

A ProjectMetaDex may include a limited `decision_record` section capturing
important architectural decisions.

Each entry should clearly state:
- what was decided
- whether the decision is binding or provisional
- why it was made

This provides architectural memory without narrative sprawl.

## What does NOT belong here

ProjectMetaDex intentionally does **not** include:

- task lists
- milestones
- timelines
- tickets or issue references

Those belong in project management tools, not architectural context.

## Authority and usage

- ProjectMetaDex may override default assistant behavior, including reasoning heuristics and semantic assumptions, for a project.
- If a ProjectMetaDex conflicts with a UserProfile MetaDex, clarification is required.
- ProjectMetaDexes are never persistent across sessions unless explicitly re-uploaded.

ProjectMetaDexes can be shared among team members to support consistent
collaboration across humans and AI.
## Schema changelog

### ProjectMetaDex schema v0.5

Version 0.5 introduces an **explicit, declarative interaction semantics capability** to ProjectMetaDex.  
This change is additive and backward-compatible.

#### New: `interaction_semantics` (optional)

ProjectMetaDex v0.5 may include an `interaction_semantics` section that **describes intended interpretation behavior** when the document is used as contextual input to an AI system or other reasoning agent.

This section is:

- purely descriptive
- non-executing
- optional
- safe to ignore without breaking compatibility

It exists to reduce ambiguity and preserve architectural intent across long-running, stateful, or multi-session interactions.

#### What `interaction_semantics` may describe

When present, `interaction_semantics` can declaratively specify:

- **Snapshot semantics**  
  The intended meaning of a snapshot request (e.g. a `/snapshot` trigger), including:
  - what constitutes authoritative project state
  - which fields must be captured
  - what information must be excluded (e.g. hypotheticals or exploratory branches)

- **Rehydration semantics**  
  How captured project state is intended to be reinstated when the ProjectMetaDex is reloaded, including:
  - which sections are authoritative
  - which invariants should be confirmed before further reasoning
  - the intended next objective, if any

- **Self-monitoring semantics (descriptive)**  
  Named patterns of interaction degradation (e.g. loss of invariant fidelity or context pressure), along with intended stabilizing responses such as snapshotting or explicit invariant confirmation.

These semantics describe **interpretive intent**, not workflow, execution, or automation.

#### What this change does *not* do

ProjectMetaDex v0.5 does **not**:

- introduce execution order or control flow
- require tools or assistants to comply with declared semantics
- imply awareness of system internals, resource limits, or model behavior
- convert ProjectMetaDex into a task or process specification

All semantics remain advisory and descriptive.

#### Rationale

As ProjectMetaDex is frequently used to preserve architectural intent across:
- long design sessions
- multiple collaborators
- AI-assisted reasoning
- interrupted or resumed work

v0.5 formalizes a way to describe **how project state is captured, reloaded, and stabilized**, without embedding behavior or coupling to any specific tool or model.

This allows ProjectMetaDex to remain:
- structurally explicit
- semantically stable
- context-portable
- aligned with its original purpose as architectural memory rather than workflow definition

---

### Compatibility note

All ProjectMetaDex documents valid under v0.4 remain valid under v0.5.  
Consumers that do not recognize `interaction_semantics` may safely ignore it.

