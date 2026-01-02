# StashKit & Dex Family  
## Wordmark Specification

### Version
v1.0

### Scope
This document specifies the construction, typography, color usage, and governed exceptions for the **StashKit wordmark** and the **Dex-family wordmarks** (e.g., LexiDex, AppDex, MetaDex, GroundDex, μDex).

This is a design specification, not a style guide.  
All decisions described here are intentional and normative.

---

## 1. Design Intent

The StashKit wordmark system encodes architectural meaning through restrained typographic variation.

The system is designed to:
- read clearly at small sizes
- scale across a family of related products
- express structural roles through form, not ornament
- permit divergence only where conceptually justified

Negative space and controlled irregularity are treated as structural elements.

---

## 2. Core Structure

### 2.1 Primary Symbol
The Converging Delta symbol is the primary brand mark.

- Geometry is fixed
- Negative space is integral to meaning
- The symbol represents structure emerging via convergence

The symbol may appear independently or paired with wordmarks.

---

### 2.2 Dex as an Invariant Suffix

“Dex” denotes an engine, framework, or structural substrate.

Accordingly:
- Dex is invariant across all products
- Dex is always rendered in the darker tone
- Dex always uses the same letterforms
- The uppercase **D** includes a fixed internal cutout

The internal cutout:
- is derived from the Converging Delta
- appears **only** in the uppercase D of “Dex”
- must not be modified, repeated, or stylized
- functions as a family marker

Dex geometry, proportions, and cutout shape are frozen.

---

## 3. Prefix Rules

Prefixes describe the *role* of a given Dex.

General rules:
- Prefixes are rendered in a lighter tone
- Prefixes are typographically quieter than Dex
- Prefixes do not introduce new structural motifs
- Prefixes remain upright and sans-serif

Examples:
- LexiDex → linguistic / interpretive interface
- MetaDex → reflective / descriptive layer
- GroundDex → foundational substrate
- AppDex → applied / executable layer

Prefixes are lexical, not symbolic.

---

## 4. Color Specification

Color is semantic, not decorative.

### 4.1 Primary Colors

| Role      | Color Name        | RGB           | Hex       |
|-----------|-------------------|---------------|-----------|
| Prefix    | Slate Blue        | 93, 111, 140  | #5D6F8CFF |
| Dex       | Deep Navy         | 31, 64, 90    | #1F405AFF |

Rules:
- Prefixes always use Slate Blue
- Dex always uses Deep Navy
- No additional colors are introduced within wordmarks

Grayscale equivalents may be used where color is unavailable.

---

## 5. Typography

### 5.1 Primary Typeface (Lexical Marks)

**Eras Demi ITC**

Used for:
- StashKit
- LexiDex
- MetaDex
- GroundDex
- AppDex
- Dex suffix in all marks

Notes:
- Typeface is used as a construction tool only
- All wordmarks are converted to vector outlines prior to distribution
- No live text is shipped
- Kerning and baseline adjustments are optical, not mechanical

---

### 5.2 μDex Exception (Symbolic / Identity Mark)

μDex represents the **Identity** pillar of the architecture and derives conceptually from *MutaDex* (mutation / transformation).

μ is treated as **notation**, not as a lexical prefix.

#### μ Glyph Rules
- μ is rendered as a symbolic operator
- μ may diverge typographically from lexical prefixes
- μ may use a **math-optimized semi-serif glyph**

For the μ glyph:
- No literal serifs are present
- Stroke modulation and implied terminals are permitted
- Slight baseline or x-height divergence is acceptable
- μ–D ligature through kerning is encouraged to signal operator → engine handoff

#### Typeface for μ
- **Cambria (or equivalent math-optimized serif glyph)**
- Used **only** for the μ character
- Not used elsewhere in the system

Dex remains invariant and upright.

---

### 5.3 Constraints on the μDex Exception

- μ is the **only** glyph allowed typographic divergence
- Serif implication must remain subtle
- No other prefixes inherit this exception
- No additional symbolic glyphs are introduced without explicit architectural justification

μDex is intentionally allowed to be slightly irregular.

Identity is not fully normalized.

---

## 6. Optical Adjustments

Permitted adjustments include:
- Manual kerning (e.g., tightening i–D or μ–D)
- Slight baseline lifts for Dex to balance weight
- Manual ligatures where they reinforce semantic continuity

Prohibited adjustments:
- Decorative alternates
- Repeated flourishes
- Per-product stylistic reinvention

Consistency is the design move.

---

## 7. Distribution Rules

- All wordmarks must be distributed as vector outlines
- No font files are embedded or redistributed
- SVG, PDF, and raster exports are permitted
- Platform-specific raster assets must be derived from the canonical SVGs

---

## 8. Summary

The StashKit and Dex family wordmarks form a **notation system** as much a logo collection.

- The Delta expresses macro-structure
- Dex expresses enginehood
- Prefixes express role
- μ expresses transformation and identity (from the original MutaDex internal name)

Divergence is permitted only where it clarifies meaning.

Everything else remains still.
