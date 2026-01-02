# MuDex (μDex)

**Mutation / Modulation Dex**  
**Last updated:** 2025-12-16

MuDex defines how **meaning may be transformed or constrained** without executing logic
or making decisions.

---

## Role in Resolution

MuDex anchors **identity stability**, not workflow.

Resolvers may consult MuDex to determine whether an identity is unique and reusable,
but MuDex does not guide procedural behavior.

---

## Candidate vs Committed Identity

Candidate identities are transient and exploratory.
Committed MuDex entries represent stable identity bindings.

Candidate identities MUST NOT be written to MuDex.

---

## Semantic Authority and Fuzzability

MuDex assumes that **authoritativeness and fuzzability are semantic properties of fields**.

- Formal identifiers and identity anchors are unfuzzable
- Lexical labels are fuzzable
- Fuzzing may only generate candidates

Resolvers rely on this semantic distinction rather than hard-coded mappings.

---

## Layered Overlays

MuDex may be composed from base, remote, and local layers.
Overlay composition affects lookup behavior, not semantic meaning.

---

## Summary

MuDex preserves identity clarity while allowing resolvers to explore ambiguity safely.
