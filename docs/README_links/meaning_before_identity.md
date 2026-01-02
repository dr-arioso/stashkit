# Walkthrough: Meaning Before Identity

> **Related walkthrough:**  
> If you want to see how shared identity works across multiple instances, see  
> [Two Bottles, One Identity](two_bottles_walkthrough.md).

This walkthrough shows how ontology can enrich meaning
even when identity remains unresolved.

---

# Walkthrough: Two Bottles, One Identity

*A concrete example of evidentiary identity and projection-based reconciliation.*

---

## The setup

You have **two physical bottles** of Patrón Blanco tequila.

They are:

* the same brand
* the same product
* the same size
* indistinguishable at a glance

But they are **two distinct physical objects**.

You scan them separately.

---

## Step 1: First bottle arrives

You scan the first bottle.

From various sources, you obtain evidence:

* OCR sees the word “Patrón”
* A barcode scan yields a UPC
* A database lookup associates that UPC with:

  * Patrón Blanco
  * 750 mL
  * 40% ABV

### What the system records

* **Evidence (claims)**
  Individual observations with source and confidence.

* **Identity hypothesis (MuDex)**

  > “Based on current evidence, this bottle is *probably* Patrón Blanco 750 mL.”

  Confidence: moderate to high.

* **Ontological enrichment (also evidence)**
  Additional claims may now be attached, such as:

  * this is a **distilled agave spirit**
  * it is produced via **distillation**, not fermentation
  * it commonly functions as a **base spirit** in cocktails like margaritas and palomas

  These do **not** change what the bottle *is* — they enrich what the system knows *about* it.

* **Instance (BottleCard)**
  Represents *this specific bottle*:

  * unopened
  * full
  * label intact

Nothing is overwritten.
Nothing is finalized.

At this point, the system is saying:

> “This appears to be Patrón Blanco, and here is what that implies ontologically — with confidence proportional to the evidence.”

---

## Step 2: Second bottle arrives

You scan the second bottle later.

You see:

* the same UPC
* the same branding
* similar OCR results

### What happens now

* New evidence is added.
* The system notices that this evidence supports an **existing identity hypothesis**.
* Confidence in that identity increases.

Crucially:

* **No existing data is replaced**
* **No merge decision is forced**
* **No assumption is made that this is ‘the same bottle’**

### The state now looks like this

* **One shared identity hypothesis**

  * “Patrón Blanco 750 mL”
  * Higher confidence than before

* **Two distinct instances**

  * Bottle A
  * Bottle B

Each instance has its own:

* state
* history
* future

---

## Step 3: Divergence over time

Later, Bottle A is opened.

New evidence arrives:

* fill level decreases
* seal broken

This evidence attaches to **Bottle A only**.

Bottle B remains:

* unopened
* full

### Important observation

The **identity hypothesis does not change**.

The system now knows:

* These bottles share identity
* They do *not* share state

---

## Step 4: Reconciliation for use

Eventually, you want to *use* this data.

Maybe you want to:

* display inventory
* decide where bottles can be placed
* export a summary

This is where **projection-based reconciliation** happens.

The Stash produces a **representative view**:

* Product: Patrón Blanco 750 mL
* Quantity: 2 bottles
* Type: distilled agave spirit
* Usage: base spirit for common tequila cocktails
* Status:

  * 1 unopened
  * 1 opened

This view is:

* policy-driven
* derived
* reversible

If new evidence arrives tomorrow, the view can change—without rewriting history.

---

## What didn’t happen (and why that matters)

At no point did the system:

* overwrite earlier observations
* collapse two bottles into one
* discard conflicting data
* pretend certainty arrived early

Instead:

* evidence accumulated
* confidence strengthened
* identity remained a hypothesis
* ontology enriched opportunistically
* instances stayed distinct

---

## The takeaway

Two bottles can:

* share identity
* diverge in state
* strengthen confidence together
* accumulate ontological meaning
* be summarized cleanly when needed

And the system never has to pretend it knows more than it does.

---

### One sentence summary

> **We keep every observation, form identity from evidence, enrich meaning opportunistically, and create summaries only when we need them.**
