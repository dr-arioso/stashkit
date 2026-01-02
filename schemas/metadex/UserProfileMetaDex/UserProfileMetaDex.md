# UserProfileMetaDex

**Version:** 1.0  
**Last updated:** 2025-12-16

## Overview

UserProfileMetaDex is a specialization of MetaDex intended to encode **interaction preferences, collaboration ergonomics, and interpretive guidance** for working with a specific user.

Unlike project- or system-oriented MetaDexes, UserProfileMetaDex does **not** describe software, architecture, or ontology. Instead, it describes *how to work well with a human interlocutor* across sessions and contexts.

The goal is not personalization for its own sake, but **alignment efficiency**:
- reducing rediscovery overhead
- preventing predictable misinterpretations
- selecting appropriate interaction modes early

---

## Design Principles

UserProfileMetaDex adheres to the following principles:

### 1. Descriptive, not prescriptive
The MetaDex biases interpretation and defaults, but **never overrides explicit user instructions**.

### 2. Ergonomic, not psychological
It encodes collaboration patterns (e.g., output format preferences, explanation style), not personality traits, diagnoses, or demographics.

### 3. Provisional and user-governed
All entries are:
- revisable
- context-sensitive
- subject to correction by the user

### 4. Non-creepy by construction
The schema explicitly avoids:
- sensitive personal data
- behavioral scoring
- claims of immutability

---

## Intended Use Cases

UserProfileMetaDex is most useful when:

- working with a user across **multiple sessions**
- producing **artifacts** (code, schemas, documents)
- operating in domains with **multiple valid interaction modes**
- collaborating with users who have **strong but implicit preferences**

It is *not* intended for:
- one-off factual queries
- anonymous, high-volume chat scenarios
- behavioral prediction

---

## Core Sections

### Engagement Profile

Describes *how* the user typically engages.

Examples:
- common use cases (e.g., casual chat vs long-term projects)
- typical session length and depth
- preference for continuity across sessions
- use of priming artifacts

This section helps select the correct **interaction mode** early.

---

### Output Preferences

Describes how the user prefers results to be delivered.

Common signals:
- inline text vs downloadable files
- full regeneration vs patch-style edits
- acceptable cases for on-screen display only

This section prevents common friction such as:
> "Please give me a file instead."

---

### Explanation Style

Describes *what counts as a helpful explanation* for the user.

This may include:
- preferred ordering of explanation lenses (e.g., convention → heuristic → structure)
- tolerance for uncertainty
- desire for explicit tradeoffs or rationale

This section is especially important for technical or architectural discussions.

---

### Interaction Control

Describes preferences around questioning and confirmation.

Examples:
- whether clarifying questions are welcome
- whether the system should make best-effort assumptions
- when explicit confirmation is preferred

---

### Communication Shims

Encodes **known interpretation hazards** and how to compensate for them.

Examples:
- soft language that should not be read as uncertainty
- questions that should not be interpreted as rejection
- exploratory phrasing that should remain provisional

This section exists specifically to prevent repeated, predictable misalignment.

---

### Tone and Register

Describes preferred conversational tone and register.

This may include:
- formality level
- humor tolerance
- styles to avoid (e.g., salesy, performative)

---

### Risk Posture (Optional)

Encodes how the user prefers risk to be handled in high-stakes domains such as:
- legal
- medical
- financial

This may influence:
- conservatism of advice
- use of disclaimers
- citation expectations

---

### Revision Policy

Describes how and when the UserProfileMetaDex should be revisited.

Typical patterns:
- misalignment-triggered review
- user-only revision authority
- explicit retirement if no longer useful

---

## Relationship to Other MetaDexes

UserProfileMetaDex is orthogonal to:

- **Project MetaDex** (describes a system or codebase)
- **MuDex** (interpretive bindings and commitments)
- **Patent Context MetaDex** (legal framing)

Multiple MetaDexes may be loaded simultaneously, each contributing a distinct interpretive lens.

---

## Anti-Goals

UserProfileMetaDex explicitly does **not** aim to:

- predict behavior
- enforce personality typing
- replace conversation
- encode immutable identity

It exists to *support* collaboration, not define the collaborator.

---

## Summary

UserProfileMetaDex provides a lightweight, inspectable way to answer:

> *“How should I work with this person to minimize friction and maximize shared understanding?”*

When used well, it fades into the background—noticed only when it prevents something from going wrong.
