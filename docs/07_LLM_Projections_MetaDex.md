# LLM Projections & MetaDex

Historically, MetaDex was a separate "shallow Dex" for priming LLMs.

With the updated schema, you have two good options:

1. **Use the full Dex**, and rely on:
   - `llm_guidance`
   - zoning (`ontology_core`, `ontology_extended`, `ontology_heavy`)
   - per-field LLM tags

2. **Generate a MetaDex-style projection** via `llm_small`:
   - includes only `ontology_core`
   - strictly partial
   - clearly labeled as incomplete

Either way, LLMs see explicit instructions like:

- do not extrapolate missing nodes
- do not invent new APIs
- treat this as partial context only
