# StashKit

StashKit is a lightweight semantic interpretation framework for turning messy inputs into structured entities.

It does this with:

- **Dexes** – domain ontologies represented as JSON
- **LexiDex** – a small wrapper for querying Dex data
- **Resolvers** – orchestrators that coordinate Skills and Dex lookups
- **Skills** – atomic extraction / classification units
- **BoosterPacks** – installable bundles of Dex + resolvers + skills
- **Stash** – optional persistence for resolved entities

This repo also defines the **LexiDex v2.1 schema**, including LLM-aware fields like `llm_guidance` and Dex zoning
(`ontology_core`, `ontology_extended`, `ontology_heavy`).
=======
**StashKit** is a Python framework for building domain-aware interpreters that transform incomplete, ambiguous, or messy inputs into clean, structured entities.

It does this using:
*	**Dexes** — lightweight, portable domain ontologies (JSON)
*	**LexiDex** — a thin access layer over Dex data
*	**Resolvers** — orchestrators that iteratively interpret signals
*	**Skills** — atomic extraction and normalization steps
*	**BoosterPacks** — plug-in bundles that ship Dexes + resolvers + skills

StashKit makes it easy to build:
*	Product and entity classifiers
*	AI-assisted data ingestion pipelines
*	LLM-guided reasoning tools
*	Custom domain knowledge interpreters

StashKit also includes a **Dex Compiler** that produces safe, LLM-optimized projections (“MetaDex”), enabling models to reason effectively without hallucinating structure or inventing APIs.

Whether you're interpreting barcodes, architectural descriptions, cocktails, code, or end-user inputs, StashKit gives you the tools to make sense of the world — one Dex at a time.

---

## Documentation Map

StashKit documentation serves multiple purposes. Files are grouped by intent:

### Normative (Library Contract)
These documents describe StashKit as it exists today.
If something here changes, it is a breaking or versioned change.
- `docs/00_Overview.md`
- `docs/01_Architecture.md`
- `docs/03_Resolvers.md`
- `docs/04_Skills.md`
- `docs/05_BoosterPacks.md`
- `docs/09_Stash.md`

### Conceptual / Exploratory
Design rationale, experiments, and forward-looking ideas.
These inform the system but are not binding.
- `docs/concepts/`
- `docs/architecture/Architecture_Foundations.md`
- `docs/adaptive_scoring_barcode_vs_ocr.md`

### Meta / Schema / Filing Infrastructure
Schemas, MetaDexes, and material used for tooling, governance, or IP work.
- `schemas/`
- `metadex/`
- `μDex/`

### Branding & Identity
Visual assets and brand documentation.
- `Branding/`
