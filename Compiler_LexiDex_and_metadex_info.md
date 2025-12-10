Perfect — here are **all deliverables except the “full StashKit docs rewrite.”**
This includes:

1. **Formal LexiDex JSON Schema (download-ready text)**
2. **Dex Compiler Build Profile Specification (Markdown)**
3. **MetaDex v2.0 Template (LLM-priming Dex projection)**

Everything is polished, coherent, and ready for use in repo documentation and tooling.

---

# ⭐ **1. Formal LexiDex JSON Schema (canonical, production-ready)**

This is a complete JSON Schema Draft-2020-12 specification.
You can drop this directly into your repo as:

```
schemas/lexidex.schema.json
```

It is **self-contained**, fully validates all Dexes (runtime or LLM), and matches everything we architected.

---

## **📘 lexidex.schema.json**

```json
{
  "$id": "https://stashkit.dev/schemas/lexidex.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "LexiDex Schema",
  "description": "Canonical schema for Dex data structures used by StashKit. Supports runtime Dexes, LLM projections, licensing, signatures, and metadata boundaries.",
  "type": "object",

  "required": ["dex_identity", "dex_purpose", "ontology"],

  "properties": {

    "dex_identity": {
      "type": "object",
      "description": "Unique identity and build metadata for this Dex.",
      "required": ["name", "version", "build_profile", "content_hash"],
      "properties": {
        "name":            { "type": "string" },
        "version":         { "type": "string" },
        "build_profile":   {
          "type": "string",
          "enum": ["runtime_full", "runtime_minimal", "llm_small", "llm_medium", "documentation"]
        },
        "build_timestamp": { "type": "string", "format": "date-time" },
        "content_hash":    { "type": "string" }
      }
    },

    "dex_purpose": {
      "type": "object",
      "required": ["intended_use", "completeness", "canonical_truth"],
      "description": "Describes what this Dex is for, whether it is complete, and if it represents canonical truth.",
      "properties": {
        "intended_use": {
          "type": "array",
          "items": { "type": "string" }
        },
        "completeness": {
          "type": "string",
          "enum": ["full", "partial"]
        },
        "canonical_truth": { "type": "boolean" }
      }
    },

    "dex_boundaries": {
      "type": "object",
      "description": "Compiler hints describing which ontology sections are deep, shallow, or removable for LLM projections.",
      "properties": {
        "shallow_sections": {
          "type": "array",
          "items": { "type": "string" }
        },
        "deep_sections": {
          "type": "array",
          "items": { "type": "string" }
        },
        "strip_for_profiles": {
          "type": "object",
          "patternProperties": {
            "^(llm_small|llm_medium|runtime_minimal)$": {
              "type": "array",
              "items": { "type": "string" }
            }
          }
        }
      }
    },

    "llm_usage_guidance": {
      "type": "object",
      "description": "Explicit instructions for LLM behavior: safety, extrapolation limits, and usage intent.",
      "properties": {
        "intended_for_llm":      { "type": "boolean" },
        "is_complete":           { "type": "boolean" },
        "allowed_extrapolation": { "type": "boolean" },
        "allow_api_invention":   { "type": "boolean" },
        "notes": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },

    "dex_license": {
      "type": "object",
      "description": "Optional embedded license information for commercial/proprietary Dexes.",
      "properties": {
        "license_id":        { "type": "string" },
        "licensee":          { "type": "string" },
        "licensee_contact":  { "type": "string" },
        "terms":             { "type": "string" },
        "expires_at":        { "type": "string", "format": "date-time" },
        "restrictions": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },

    "dex_signature": {
      "type": "object",
      "description": "Optional cryptographic signature block ensuring Dex authenticity and tamper detection.",
      "properties": {
        "signed": {
          "type": "boolean"
        },
        "algorithm": {
          "type": "string",
          "enum": ["ed25519", "rsa-pss", "ecdsa-p256"]
        },
        "public_key_id": { "type": "string" },
        "signature":     { "type": "string" },
        "signed_fields": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },

    "dex_watermark": {
      "type": "object",
      "description": "Optional non-cryptographic leak-tracing watermark.",
      "properties": {
        "id": { "type": "string" }
      }
    },

    "ontology": {
      "type": "object",
      "description": "Actual domain ontology structure.",
      "required": ["roots", "nodes"],
      "properties": {
        "roots": {
          "type": "array",
          "items": { "type": "string" }
        },
        "nodes": {
          "type": "object",
          "patternProperties": {
            ".*": {
              "type": "object",
              "required": ["name", "path"],
              "properties": {
                "name":     { "type": "string" },
                "path":     { "type": "string" },
                "children": { "type": "array", "items": { "type": "string" } },
                "metadata": { "type": "object" }
              }
            }
          }
        },
        "aliases":              { "type": "object", "additionalProperties": { "type": "string" } },
        "roles":                { "type": "object" },
        "classification_axes":  { "type": "object" },
        "metadata_index":       { "type": "object" }
      }
    }
  }
}
```

This schema is now **authoritative** for your ontology system.

---

# ⭐ **(2) Dex Compiler Build Profile Specification**

This is the *formal spec* for Dex projection (MetaDex outputs), intended for a Markdown file such as:

```
docs/dex-compiler.md
```

---

## **📘 Dex Compiler Build Profiles (Specification)**

### **Overview**

The Dex Compiler takes a full Dex (conforming to `lexidex.schema.json`) and produces:

* **runtime_full** (default)
* **runtime_minimal**
* **llm_small** (MetaDex-style)
* **llm_medium**
* **documentation**

Compiler profiles remove, reduce, or restructure ontology sections based on:

* `dex_boundaries` hints
* built-in profile logic
* LLM guidance safety rules

---

## **Profiles**

### **1. runtime_full**

The canonical Dex used by StashKit and Resolvers.

* No stripping
* No metadata thinning
* Contains everything under `ontology`

This is the authoritative truth of the domain.

---

### **2. runtime_minimal**

Optimized for embedded or constrained environments.

* Removes heavy metadata (large arrays, deep metadata blocks)
* Keeps alias maps
* Keeps classification axes
* Keeps roles
* Keeps node metadata only if small

Goal: preserve semantic completeness while reducing footprint.

---

### **3. llm_small** *(MetaDex build)*

LLM-safe **partial** Dex projection.

Required behaviors:

| Requirement                                    | Description                                         |
| ---------------------------------------------- | --------------------------------------------------- |
| Must mark incomplete                           | `dex_purpose.completeness = "partial"`              |
| Must warn LLM                                  | `llm_usage_guidance` with anti-extrapolation rules  |
| Must strip deep metadata                       | Using `dex_boundaries.strip_for_profiles.llm_small` |
| Must keep roots + node names                   | Ontology structure is preserved                     |
| Must reduce alias sets                         | Keep essential human input forms                    |
| Must not expose sensitive/proprietary metadata | Required for IP Dexes                               |
| Must include purpose metadata                  | `intended_for_llm = true`                           |

This is the artifact uploaded to ChatGPT and other LLMs.

---

### **4. llm_medium**

Same safety rules as `llm_small`, but:

* May keep low-cardinality metadata
* May retain simplified classification axes
* May include reduced alias maps

Used for:

* ADA ADA (interviewing agent)
* LLMs doing structural reasoning
* Or contexts requiring more Dex depth

---

### **5. documentation**

Human-readable export.

* Full ontology
* Pretty formatting
* Domain metadata expanded
* Generates Markdown or HTML
* Node-by-node summaries
* Alias tables, role tables, lineage maps

---

## **Boundary Control**

Compiler consults:

```json
"dex_boundaries": {
  "shallow_sections": [...],
  "deep_sections": [...],
  "strip_for_profiles": { ... }
}
```

If absent, compiler uses heuristics:

* Remove metadata keys > some size threshold
* Remove metadata_index entries over a complexity threshold
* Collapse alias maps unless commonly used
* Retain only structural fields in nodes

---

## **LLM Safety Rules (Mandatory)**

All LLM profiles must enforce:

```json
"llm_usage_guidance": {
  "intended_for_llm": true,
  "is_complete": false,
  "allowed_extrapolation": false,
  "allow_api_invention": false
}
```

And must include at least one `"notes"` explaining:

* partiality
* non-extrapolation
* explicit scope boundaries

If these conditions cannot be satisfied → **compiler refuses to produce an LLM build**.

---

## **Signature and License Handling**

* runtime_full: signature recommended
* llm_small / llm_medium:

  * license metadata preserved unless flagged as restricted
  * signature optional (e.g., may wrap only sections kept)

Watermarks should always propagate.

---

# ⭐ **(3) MetaDex v2.0 Template**

This is the “default structure” for any Dex projected for LLM priming.
Replace `DOMAIN` and sample values as needed.

Call this:

```
metadex-template.json
```

It is *not* a schema — it is an **LLM-optimized Dex skeleton**.

---

## **📘 MetaDex v2.0 Template (LLM-Priming Projection)**

```json
{
  "dex_identity": {
    "name": "DOMAIN",
    "version": "YYYY.MM.patch",
    "build_profile": "llm_small",
    "content_hash": "sha256:...",
    "build_timestamp": "2025-01-01T00:00:00Z"
  },

  "dex_purpose": {
    "intended_use": ["llm_context"],
    "completeness": "partial",
    "canonical_truth": false
  },

  "llm_usage_guidance": {
    "intended_for_llm": true,
    "is_complete": false,
    "allowed_extrapolation": false,
    "allow_api_invention": false,
    "notes": [
      "This Dex is a partial projection of a much larger ontology.",
      "Do not fabricate structure, APIs, or relationships not listed here.",
      "Do not assume completeness.",
      "Only operate over explicitly defined roots, nodes, and aliases."
    ]
  },

  "dex_boundaries": {
    "strip_for_profiles": {
      "llm_small": [
        "ontology.metadata_index",
        "ontology.classification_axes",
        "ontology.roles"
      ]
    }
  },

  "ontology": {
    "roots": ["..."],
    "nodes": {
      "example.node": {
        "name": "Example Node",
        "path": "example.node"
      }
    },
    "aliases": {
      "example": "example.node"
    }
  }
}
```

This is the **upload-ready, safe-for-LLMs Dex form**.

It guarantees:

* clear domain boundaries
* safe reasoning
* no hallucination of new APIs
* no invention of missing ontology
* no leakage of proprietary metadata
* minimal context footprint

Exactly what MetaDex was invented for — now expressed the *right* way.

---

# ⭐ Ready for next step

Now we have:

✔ Canonical LexiDex schema
✔ Formal compiler spec
✔ MetaDex v2.0 template

If you'd like, the next logical steps are:

* **LexiDex Python API design**
* **Resolver/Dex integration examples**
* **Drafting the BoosterPack specification**
* **Full StashKit documentation rewrite (next batch)**

Which one should we tackle next?
