Below is a **public API doc draft** for `StashBench.ontologics` (Python-facing). It’s written to be readable by “future-us” and stable even as internals evolve (ArtifactProvider/Loader, DexLoader, LLZen tooling, etc.).

---

# StashBench Ontologics Public API

`ontologics` is the StashBench namespace for **loading, managing, and transforming ontologies** used by StashKit’s resolver framework.

It is designed to be:

* **Approachable** (Pythonic verbs, minimal ceremony)
* **Format-flexible** (files, BoosterPacks, pre-loaded objects)
* **LLZen-agnostic by default** (LLZen is supported as a transform/overlay layer, not required)
* **Deterministic** (stable hashing, stable loader selection, explicit profiles)

## Concepts

### Ontology Source

An “ontology source” can be:

* a filesystem path (`"./ExistentialDex.v1.0.json"`)
* a BoosterPack identifier (`"boozedex://default"`)
* a pre-loaded Python object (dict / Dex object)
* later: URLs / registries (out of scope for the minimal API)

### DexHandle

`attach()` returns a **DexHandle**, a lightweight object that represents a loaded ontology (or ontology bundle) and its identity.

A DexHandle is usable as:

* an argument to `transform()`, `describe()`, etc.
* a value you pass into other StashBench/StashKit systems that accept dex inputs

> Internally, DexHandle may wrap a canonical LexiDex graph object, plus provenance metadata.

---

## API Overview

### `sb.ontologics.attach(source, *, profile=None, name=None, version=None, strict=True) -> DexHandle`

Attach an ontology source and return a handle.

**Parameters**

* `source`
  Path, BoosterPack ID, dict-like JSON, or already-loaded Dex object.
* `profile` *(optional)*
  Loader hint. Examples: `"lexidex_v3"`, `"legacy_lexidex_2x"`, `"domain_dex_wrapped"`.

  * If omitted, loader selection is automatic.
* `name`, `version` *(optional)*
  Overrides/annotations when identity cannot be inferred.
* `strict` *(default: True)*
  If True, schema/graph validation errors raise immediately.
  If False, returns a handle with warnings in `describe()`.

**Returns**

* `DexHandle` with stable identity (`id/name/version/hash`) when available.

**Raises**

* `OntologyLoadError` (unrecognized format, parse error)
* `OntologyValidationError` (schema/graph invalid in strict mode)
* `OntologyAmbiguityError` (multiple loaders match and `profile` not provided)

**Example**

```python
dex = sb.ontologics.attach("./ExistentialDex.v1.0.json")
booze = sb.ontologics.attach("boozedex://default")
```

---

### `sb.ontologics.describe(x) -> dict`

Return a structured description of an attached ontology (or source-like object).

Includes:

* identity (name/version/hash if known)
* loader profile used
* counts (entities/predicates/axes/axioms/constraints)
* validation status + warnings
* provenance (source path / BoosterPack id)

**Example**

```python
info = sb.ontologics.describe(dex)
print(info["counts"])
```

---

### `sb.ontologics.transform(x, target, *, profile=None, include=None, exclude=None) -> str | dict`

Transform an ontology into a target representation.

This is the public place where LLZen projection lives (without making LLZen mandatory elsewhere).

**Parameters**

* `x`
  DexHandle or attachable source.
* `target`
  String enum. Typical targets:

  * `"llzen"`: emit `.llzen` projection (string)
  * `"json"`: emit canonical JSON (dict)
  * `"packed"`: emit compact JSON optimized for LLM input (dict or string)
* `profile` *(optional)*
  Transform profile hint (e.g., `"llzen_v1"`, `"llzen_v2_rollup"`).
* `include` / `exclude` *(optional)*
  Optional selectors for pruning sections (e.g., include only `ontology_core`).

**Returns**

* `str` for text projections (`"llzen"`)
* `dict` for JSON returns (`"json"`, `"packed"`), unless explicitly stringified

**Example**

```python
llzen_text = sb.ontologics.transform(dex, "llzen")
packed = sb.ontologics.transform(dex, "packed")
```

---

### `sb.ontologics.list() -> list[DexHandle]`

List currently attached ontologies (if StashBench maintains a registry).

This is optional; StashBench may also be stateless and only operate on handles.

---

### `sb.ontologics.detach(handle_or_id) -> None` *(optional)*

Detach an ontology from the active registry (if maintained).

Not required for a stateless design.

---

## DexHandle (public contract)

A DexHandle should minimally provide:

* `handle.id` *(stable internal identifier; may be derived)*
* `handle.name`
* `handle.version`
* `handle.hash` *(sha256 when available)*
* `handle.format` *(e.g., `"LexiDex"`, `"OpenAPI"` later)*
* `handle.schema_version` *(e.g., `"3.2"`)*
* `handle.dex` *(optional direct access to underlying Dex object)*

Recommended: DexHandle is JSON-serializable via `describe()`.

---

## Loader/format rules (user-visible guarantees)

### Automatic loader selection

`attach()` attempts to:

1. detect “LLZen-wrapped domain_dex” vs “bare LexiDex”
2. select the best matching loader
3. validate deterministically (strict mode)

### Legacy acceptance

Legacy LexiDex forms (e.g., 2.x variants) may be accepted via:

* `profile="legacy_lexidex_2x"` or auto-detection
* normalization during load or during `transform("llzen")`

### Validation

Validation has two levels:

* **schema validation** (JSON Schema)
* **graph validity** (ontology constraints/axioms reducible to constraints)

In strict mode, failures raise immediately.

---

## Relationship to BoosterPacks

BoosterPacks can ship:

* one or more dex files
* skill sets + configuration
* default activation profile

`attach("boozedex://default")` may:

* attach the BoozeDex ontology
* return a handle (or bundle-handle) referencing all attached dexes
* optionally register a named profile for resolvers

(BoosterPack semantics are still independent of LLZen.)

---

## Not in scope (yet)

* Following references recursively (`--follow`) and rollups
* Remote artifact registries / caching policies
* Mapping application / overlay composition (DexMapping) as a first-class call
  (likely future: `sb.ontologics.apply_mapping(dex, mapping)`)

---

## Suggested Exceptions (names)

* `OntologyLoadError`
* `OntologyValidationError`
* `OntologyAmbiguityError`
