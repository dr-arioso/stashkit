# What the Heck *Is* This Thing?

*A developer-oriented introduction to evidentiary identity and non-collapsing entity resolution.*

---

## The problem we’re actually solving

Most real systems don’t start with clean, authoritative data.

They start with **messy inputs**:

* partial observations
* repeated sightings
* conflicting values
* probabilistic signals
* human input mixed with automation

Yet most software systems make a quiet assumption:

> **At some point, you must decide what something *is*.**

Once that decision is made, new information either overwrites the old value, is ignored, or triggers a painful merge.

This project is about what happens **before certainty**—when information is still messy, incomplete, contradictory, and evolving over time.

---

## A different mental model

Instead of asking:

> “What is this thing?”

we ask:

> **“What evidence do we have, and what identity hypothesis does it support?”**

Identity is treated as a **working hypothesis**, not a fact.

We never throw evidence away.
We summarize it when we need to act.

---

## Metaphor #1: Waldo Reconnaissance 🛰️

Imagine you’re tasked with extracting Waldo from a hostile zone.

You don’t get a clean ID scan.
You get **satellite images**.

* One image shows a red-and-white blur.
* Another shows stripes near a crowd.
* A third shows a figure with glasses.

Any single sighting could be wrong.

But **multiple independent sightings**, over time, begin to converge.

You don’t declare:

> “This pixel *is* Waldo.”

You maintain a **dossier**:

* sightings
* locations
* confidence
* contradictions

When it’s time to act, you use the **best-supported hypothesis**—without deleting the rest of the evidence.

That’s how identity works in this system.

---

## Metaphor #2: Cryptid Watch 🐾

Now imagine a Cryptid Watch Program.

Reports come in:

* footprints
* blurry photos
* eyewitness accounts
* contradictory descriptions

No single report proves anything.

Instead, the program maintains a **living case file**:

* every report is preserved
* confidence rises with corroboration
* disagreement is allowed to coexist

Periodically, the program publishes a **summary report**:

> “Based on current evidence, here’s our best guess.”

The report can change tomorrow.
The evidence never disappears.

That’s how reconciliation works here.

---

## Okay—but seriously: what does this mean for software?

### Traditional approach: last overwrite wins (with variations)

Most systems ultimately converge on some form of **last overwrite wins**.

If they’re simple, the newest value just replaces the old one.

If they’re more sophisticated, they may:

* track confidence or priority metadata
* prefer certain sources over others
* only overwrite data statically declared to be lower-confidence

These approaches are improvements—but they still share a core assumption:

> **At any moment, there is exactly one correct value, and older alternatives can be discarded.**

History is collapsed.
Disagreement disappears.
Confidence is implied, not accumulated.

---

### This system: evidence accumulates, views reconcile

Here, we separate concerns:

* **Evidence**: what we’ve observed
* **Identity**: what those observations suggest
* **Instances**: specific, physical or logical objects
* **Reconciliation**: how we summarize evidence for use

Nothing is overwritten by default.

---

## A concrete example: two identical bottles

You scan two bottles of the same product.

Traditional system:

* one product record
* one entry updated twice
* quantity maybe increments
* details collapse together

This system:

* **two instances** (two physical bottles)
* **one shared identity hypothesis** (same product)
* evidence from both strengthens confidence
* each bottle can still diverge (opened, damaged, misplaced)

Same identity.
Different instances.
No contradiction.

---

## The pattern: Evidentiary Identity

We call this the **Evidentiary Identity Pattern**
*(also known formally as the **Compositional Identity Hypothesis Model**).*

In this pattern:

* Identity is **derived from evidence**
* Confidence **accumulates over time**
* Instances remain distinct
* No observation is discarded

Identity answers:

> “What do we think this is, and how confident are we?”

It does **not** answer:

> “What is this, absolutely?”

---

## Reconciliation without destruction

Eventually, you *do* need an answer:

* to display a value
* to make a decision
* to store something

This system does that using **Projection-Based Reconciliation**.

Reconciliation:

* produces a **representative view**
* follows a **policy** (e.g., highest confidence)
* is **reversible**
* never deletes or rewrites evidence

Think:

* expense report vs receipts
* weather forecast vs raw satellite data
* wanted poster vs case file

The summary is not the truth.
It’s a **useful projection**.

---

## Why this matters (especially for devs)

This approach is designed for systems where inputs remain messy longer than we’d like to admit.

It shines when:

* data comes from multiple sources
* observations repeat over time
* inputs are noisy or probabilistic
* identity is ambiguous

It avoids:

* premature merges
* silent data loss
* “why did this change?” bugs
* brittle pipelines

And it gives you something rare:

> **The ability to change your conclusions without erasing your past.**

---

## If this feels unfamiliar—that’s the point

Most software pretends certainty arrives earlier than it actually does.

This system is designed for the long, messy middle:

* before confidence is high
* before truth is settled
* before collapse is justified

If you’ve ever thought:

> “I wish we hadn’t thrown that data away…”

Then you already understand why this exists.

---

## What to read next

If this clicked:

* Read the **two-bottle walkthrough**
* Look at how identity, instances, and reconciliation are separated
* Notice how *nothing* relies on “last write wins”

If it didn’t:

* That’s okay
* This isn’t for every system
* But for the ones it fits, it fits *very* well

---

*Identity isn’t a fact.
It’s a hypothesis supported by evidence.*

That’s the whole thing.