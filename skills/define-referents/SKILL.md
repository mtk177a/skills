---
name: define-referents
description: Defines concrete referents, semantic roles, relationships, and naming constraints before a new or ambiguous term can collapse distinct concepts in a design, investigation, explanation, or identifier. Use as a semantic preflight when terminology itself could distort later reasoning or when the user requests a referent table; return a referent-and-naming handoff to the originating workflow. Not for clarifying the overall request, drafting the downstream document or code, mechanical edits, established-name reuse, ordinary wording choices, boilerplate, casual conversation, or short text using established terminology.
license: MIT
---

# Define Referents

## Objective

- Ground each material term in a concrete referent, its role, and its relationships before proposing the term.
- Prevent a fluent label from hiding distinct conditions, states, events, values, records, purposes, means, entities, or other context-specific roles.
- Return a referent-and-naming contract to the originating workflow without taking over its design, investigation, writing, or implementation responsibility.

## Required reference

Read [references/referents-before-labels.md](references/referents-before-labels.md) completely whenever this Skill triggers. Use it as the semantic decision guide and this file as the execution contract.

## Evidence and inputs

Gather what is available:

- the source requirement, observation, evidence, or reasoning sequence
- the intended document, design element, explanation, or identifier
- established domain terms and their authoritative sources
- the originating workflow and the work it must resume after semantic preflight
- explicit authorization for a separate file, when one is requested

Distinguish confirmed information, inference, assumptions, and unknowns. Use safe, relevant read-only inspection to resolve discoverable facts when the target and inspection scope are clear. Do not invent a purpose, referent, role, relationship, or naming authority to complete a table.

## Workflow

1. Identify only the terms that would be introduced or reused with a broader or ambiguous meaning that could materially change later reasoning.
2. Confirm that the source contains enough information to distinguish the relevant referents and relationships. If a material fact is missing, ask a focused question or report `Blocked`; do not generate a naming table from incomplete grounding.
3. Create the Grounding table first. Do not include candidate terms, first-use definitions, or wording that presupposes a candidate term in this phase.
4. Validate the Grounding table on its own: each row identifies a concrete referent, its current semantic role, its place in the reasoning, and any uncertainty without relying on a label.
5. Only after every relevant Grounding row passes validation, create the Naming table. Prefer an established or user-provided term. If no precise term shortens the concrete wording without changing its boundary, use `concrete wording` instead of introducing a term.
6. Choose the state:
   - `Ready`: the mapping and naming constraints are settled enough for the originating workflow to continue.
   - `Decision required`: competing mappings or candidate terms imply materially different public contracts or domain boundaries. Present the grounded alternatives and ask the decision-relevant question without selecting silently.
   - `Blocked`: material evidence, information, or authority needed to ground the referent is unavailable.
7. For a direct naming request, return the tables and state as the final deliverable. For a broader task, return them as a handoff and stop this Skill so the originating workflow can resume.
8. If a Grounding row is corrected, invalidate every dependent Naming row, revise the grounding, and regenerate only the affected naming proposal. Do not overwrite user-authored or downstream content.

## Grounding table contract

Use this column order:

| ID | Source | Purpose | Concrete referent | Semantic role | Sequence / relationship | Uncertainty |
| --- | --- | --- | --- | --- | --- | --- |

- Use stable mechanical IDs such as `R1`; an ID is only a cross-table reference and is not a domain term.
- State what the referent is rather than restating a proposed label.
- Describe the semantic role in the current explanation or design. The common roles in the required reference are examples, not a closed taxonomy; use a precise context-specific role when needed.
- Split rows when one label would otherwise hide distinct referents or materially different roles. Do not split the same referent merely because it participates in several relationships.
- Preserve user-supplied reasoning order and uncertainty.
- Record uncertainty as `confirmed`, `inferred`, `assumed`, or `unknown`, with a short basis when it is not obvious.
- Split a table only when purposes or reasoning stages are meaningfully separate, or when the mapping can no longer be reviewed coherently. Do not split by a fixed row count.

## Naming table contract

Create this table only after the Grounding table is complete:

| ID | Candidate term | Status | First-use definition |
| --- | --- | --- | --- |

- Use the Grounding ID to preserve an explicit one-to-one mapping.
- Use `established`, `proposed`, `concrete wording`, or `decision required` for `Status`.
- Define every proposed new term precisely as “X means ...”. For an established term, identify it as established and preserve the authoritative mapping from the Grounding table.
- Multiple alternatives may reference the same ID only when the state is `Decision required`; state the semantic trade-off instead of choosing one silently.
- Read each candidate term alone. It must not truthfully name another row whose distinction matters.
- Hide the entire Naming table. The Grounding table must remain understandable without it.

## Output and file handling

- Start with `State: Ready`, `State: Decision required`, or `State: Blocked`.
- Include the Grounding table whenever grounding is complete enough to support it. Include the Naming table only after the grounding passes its checks.
- For `Decision required`, include the unresolved semantic choice, why it affects the public contract or domain boundary, and the question the user must decide.
- For `Blocked`, include the missing evidence or information, the mapping left unsettled, and what can unblock it.
- Return tables in the response by default. Create a separate referent-table file only when the user explicitly authorizes that additional artifact; authorization to create the target document does not authorize a sidecar file.
- Never use a hash, file timestamp, or user confirmation as a substitute for the observable Grounding-then-Naming order.

## Boundaries

- Do not require user confirmation when the mapping is complete and only a low-impact, local, reversible naming choice remains.
- Do not treat this Skill as authorization to write the target document, design, report, or code.
- Do not clarify the overall request when the ambiguity is not specifically about referents or terminology; return that responsibility to `clarify-request` or the originating workflow.
- Do not force every referent into a closed role list or split tables at a fixed row count.
- Do not use a corrected-word blacklist as the main safeguard.
- Do not introduce a new term without a precise mapping and first-use definition.
- Do not fetch the external provenance article at runtime; the bundled reference is self-contained.
