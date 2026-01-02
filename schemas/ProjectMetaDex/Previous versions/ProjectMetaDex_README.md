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
