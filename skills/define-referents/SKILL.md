---
name: define-referents
description: Use before drafting design documents, investigation reports, cause-isolation or countermeasure proposals, reasoning summaries, or identifiers when a new or ambiguous term could collapse different referents or semantic roles. Establish and obtain approval for a referent table before naming or prose. Do not use for quotations, mechanical edits, reuse of established names, boilerplate, casual conversation, or short text that uses only established terminology.
license: MIT
---

# Define Referents

## Purpose

- Fix each concrete referent and semantic role before assigning a term.
- Prevent one fluent label from conflating a condition, state, event, value, record, purpose, or means.
- Preserve the user's reasoning order across prose, design elements, and code identifiers.

## Required reference

Read [references/referents-before-labels.md](references/referents-before-labels.md) completely whenever this Skill triggers. Use it as the semantic decision guide; keep this file as the execution contract.

## Inputs

- The source requirement, observation, or reasoning sequence
- The intended document, design element, or identifier
- The output location, when the user authorized file creation

## Workflow

1. Identify the terms that would be introduced or reused with a potentially broader meaning.
2. Create the referent table before drafting any body text or identifier.
3. Fill `Source`, `Purpose`, `Concrete referent`, `Role`, and `Sequence / relationship` first. Leave the final two fields empty until these five fields are complete.
4. Fill `Candidate term` only after the referent and role are fixed. Then fill `First-use definition` for a new term, or mark the term as established.
5. Submit only the table and stop for user confirmation. Do not draft the target body in the same turn.
6. After confirmation, read the approved table again and write the target body as a projection of it.
7. Keep the same mapping in prose, design elements, and code identifiers. Use separate names for separate roles.

## Referent table contract

Use this column order without reordering it:

| Source | Purpose | Concrete referent | Role | Sequence / relationship | First-use definition | Candidate term |
| --- | --- | --- | --- | --- | --- | --- |

- Use only these roles: `start condition`, `state`, `event`, `value`, `record`, `purpose`, `means`.
- Keep one role per row. Split a row when one candidate term would cover multiple roles.
- Keep a table to 1–6 rows. Split larger tables at a boundary where the meaning or reasoning stage changes.
- Preserve the source wording in `Sequence / relationship` when the user supplied an order such as test, isolate, then choose a countermeasure.
- Prefer user-provided or established terms. Define every new term as “X means ...”; if that sentence cannot be written precisely, use the concrete description instead of introducing the term.
- Confirm that hiding `Candidate term` still leaves the concrete referents and relationships understandable.

## Submission mode

- For an authorized file deliverable, save `referent-table-<slug>.md` beside the target document, report its path, and stop for confirmation.
- For a response-only task, return the standalone table and stop for confirmation without creating a file.
- Do not use a hash as evidence of creation order. The separate submission and confirmation boundary is the evidence.

## Recovery

- If body text was drafted before the table, discard only the agent-generated draft, create and submit the table, and wait again. Never delete user-authored content.
- If a referent or role is corrected, revise the row and wait for confirmation before regenerating the affected body.
- Do not repair an incorrect row by adding explanatory prose around it.

## Boundaries

### Always

- Fix referents and roles before candidate terms.
- Preserve uncertainty and reasoning order from the source.
- Wait for explicit confirmation between the table and the target body.

### Ask first

- When competing candidate terms imply materially different public contracts or domain boundaries.
- When the requested table location would require writing outside the authorized workspace.

### Never

- Use a corrected-word blacklist as the main safeguard.
- Use one term for multiple semantic roles.
- Introduce a new term without a precise first-use definition.
- Overwrite user-authored text while recovering from an ordering mistake.
