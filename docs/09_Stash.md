# Stash

The **Stash** is an optional persistence mechanism for resolved entities.

It is aware of:

- which Dex a given entity was interpreted under
- which resolver produced it
- versioning so entities can be re-evaluated under newer Dexes

Stash is intentionally simple and pluggable:

- store entities in a database
- or a document store
- or flat files – whatever fits your needs


---

### Stash Semantics (Conceptual, v2)

A Stash is a durable evidence locker containing committed artifacts—structured bundles of observations that the system is willing to preserve, index, and reason over long-term. Artifacts in a Stash (e.g., resolved cards) need not represent ontological certainty or singular truth; they may encode uncertainty, multiplicity, and even internal contradiction. What distinguishes Stash contents is not correctness, but commitment: the system has crossed an intentional threshold and chosen to treat these artifacts as stable reference points for future resolution, identity linking, and user interaction. Provisional, speculative, or opportunistic observations may exist elsewhere, but entry into a Stash signifies that the evidence is sufficiently coherent, scoped, and valuable to retain beyond the transient resolution process.
