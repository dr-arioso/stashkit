# StashKit — Brand Assets & Visual Governance

This directory defines the **canonical visual language** for StashKit.
These assets are not interchangeable. Each exists to serve a distinct semantic role.

---

## Primary Identity Mark

### **Converging Delta (v1.0)**

**Role:**  
The **identity invariant** of StashKit.

This mark represents structured convergence: ambiguous or noisy input collapsing into stable definition.

**Use when:**
- Identifying StashKit
- Branding and navigation
- App icons, favicons, headers
- CLI splash screens
- Documentation headers
- Any repeated or reduced context

**Design characteristics:**
- Inverted triangular outer form (delta)
- Asymmetrical inner negative space
- One planar interior angle acting as a visual anchor
- A deliberate notch along the right outer edge

This mark is evergreen. Once finalized, its geometry should not be altered except for scale-safe reduction (e.g., favicon variants).

---

## Notch Rationale

The Converging Delta incorporates a deliberate notch along one edge of the outer form to signal that the system it represents is **structured but not closed**.

While the overall triangular boundary conveys stability, rigor, and convergence, the notch introduces a controlled asymmetry that implies the possibility of **informed intervention**. This reflects StashKit’s design philosophy: systems should resolve ambiguity into structure without becoming brittle or inaccessible.

The notch is not decorative. It functions as a visual affordance, indicating that the framework permits refinement, correction, and extension without loss of coherence.

---

## Explanatory System Mark

### **StashKit_Flow_Glyph**

**Role:**  
A **conceptual and narrative diagram**, not a logo.

This glyph exists to explain *how* StashKit works, not to identify *that* it exists.

**Use when:**
- Onboarding new readers
- Explaining system architecture
- “How it works” sections
- Whitepapers, talks, and decks
- Patent or deep technical documentation

**Use constraints:**
- Use sparingly (typically once per surface)
- Never reduced to favicon or badge size
- Never used in navigation or headers

**Freeze policy:**  
The Flow Glyph is frozen. It should not be iterated or stylistically modified.
If the system evolves, explanation should occur in text, not by redesigning this mark.

---

## Platform-Specific Assets

- `converging-delta-v1.svg` — canonical master
- `converging-delta-v1-favicon.svg` — reduction-safe favicon geometry
- `favicon.ico` — multi-size browser icon
- `apple-touch-icon.png` — iOS / iPadOS home screen
- `safari-pinned-tab.svg` — Safari pinned tab mask (monochrome)

---

## Non-Negotiable Design Rules

- No rounding
- No gradients, shadows, or effects
- Solid fill only
- Preserve negative space
- Do not substitute one mark for another
- Do not modify the master geometry

---

## Rationale Summary

StashKit separates **process** from **essence**.

- The **Flow Glyph** explains the system (ontogeny).
- The **Converging Delta** represents the system once understood (ontology).

When understanding is achieved, explanation disappears — and only the invariant remains.
---

## Dark Mode Usage

On dark backgrounds, the Converging Delta should be rendered using a **near‑white, cool neutral** to preserve contrast and negative space without appearing luminous.

**Recommended dark‑mode mark color:**
- `#E6EAF0` (cool light gray)

**Guidelines:**
- Geometry must remain unchanged.
- Do not add outlines, shadows, glows, or effects.
- Do not invert or recolor internal negative space.
- Only luminance may change between light and dark contexts.

This ensures the mark remains authoritative, legible, and consistent across themes.
