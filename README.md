# StashKit

**StashKit** is a lightweight semantic interpretation framework for turning messy, incomplete, or ambiguous inputs into clean, structured entities.

Think: “signals in → meaning out” — using portable domain knowledge (**Dexes**) and small, composable interpretation steps (**Skills**) coordinated by **Resolvers**.

---

## Core ideas

StashKit is built from a few simple parts:

- **LexiDex** — or just **Dex**; portable domain ontologies represented as JSON (your “knowledge substrate”)
- **Skills** — atomic extraction / normalization / classification units (one job, well-defined I/O)
- **Resolvers** — orchestrators that iteratively interpret signals using Skills + Dex lookups
- **BoosterPacks** — installable bundles that ship Dexes + resolvers + skills for a domain
- **Stash** — persistence for resolved entities, traces, or intermediate artifacts. Resolutions are preserved as observations (not overwritten); queries return a current best-available projection.

StashKit is designed so you can:
- start small with a few Skills + a tiny Dex
- grow into richer ontologies and more capable resolvers
- keep your domain knowledge portable and versionable

---

## What you can build with it

StashKit is a good fit for:
- product/entity classification (barcodes, listings, OCR text, receipts)
- AI-assisted ingestion pipelines (semi-structured → structured)
- domain-aware interpreters (architecture descriptions, cocktails, code-ish inputs, user prompts)
- LLM-guided reasoning tools that must stay grounded in a declared ontology

---

## Dex Compiler and LLM projections

StashKit includes a **Dex Compiler** that can emit safe, LLM-optimized projections.

The intent is practical:
- reduce model confusion about “what exists”
- keep structure explicit and schema-validated
- prevent invented fields/APIs by supplying a tight, model-readable view of the ontology

---

## Schemas

This repo defines the **LexiDex schema v3.3**.

LexiDex is the canonical ontologic JSON schema used by StashKit.

---

## Documentation map

StashKit documentation serves multiple purposes. Files are grouped by intent:

### Normative (Library contract)
These documents describe StashKit as it exists today.
If something here changes, it is a breaking or versioned change.

- `docs/00_Overview.md`
- `docs/01_Architecture.md`
- `docs/03_Resolvers.md`
- `docs/04_Skills.md`
- `docs/05_BoosterPacks.md`
- `docs/09_Stash.md`

### Conceptual / exploratory
Design rationale, experiments, and forward-looking ideas.
These inform the system but are not binding.

- `docs/concepts/`
- `docs/architecture/Architecture_Foundations.md`
- `docs/adaptive_scoring_barcode_vs_ocr.md`

### Meta / schema / filing infrastructure
Schemas, projections, and material used for tooling, governance, or IP work.

- `schemas/`
- `metadex/`
- `μDex/`

### Branding & identity
Visual assets and brand documentation.

- `Branding/`

---

## Design goals (quick read)

- **Portable knowledge**: Dexes live as plain JSON, versioned like code.
- **Composable interpretation**: small Skills + explicit resolver orchestration.
- **Deterministic where possible**: make “what the system can know” explicit.
- **LLM-friendly without being LLM-dependent**: projections help models behave, but the ontology stays the source of truth.

---

## Status

StashKit is evolving. Expect a bias toward:
- explicit schemas
- stable contracts for normative docs
- forward-looking work to live in conceptual/ folders until it’s ready to become contract

---
