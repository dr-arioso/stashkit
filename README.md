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
