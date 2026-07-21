# define-referents evals

## Iter 0 — Static check

- the description triggers only when new or ambiguous terms may collapse referents or roles
- the body excludes quotations, mechanical edits, established-name reuse, boilerplate, casual conversation, and short established terminology
- the table fixes five referent fields before filling the candidate term and first-use definition
- the table and target body are separated by explicit user confirmation
- the required reference defines role criteria and validation checks without requiring the external article at runtime
- [critical] the executor must submit only the referent table and stop before drafting the target body

## Scenarios

### Scenario A: One phrase covers a threshold, condition, and event

A design draft proposes one new term for a numeric limit, the condition that compares history size with that limit, and the event that begins summarization.

Requirements checklist:
1. [critical] Put the value, start condition, and event in separate rows
2. Leave candidate terms empty until the concrete referents and roles are fixed
3. Submit only the table and wait for confirmation
4. Do not draft the design body in the same turn

### Scenario B: Preserve a cause-isolation sequence

The cause is unknown. The intended order is to run a test, retain its results, isolate the cause from those results, and choose a countermeasure only after isolation.

Requirements checklist:
1. [critical] Preserve test → record results → isolate cause → choose countermeasure
2. Distinguish records and means from the purpose of isolating the cause
3. Reject a short work label that collapses the sequence
4. Keep the cause unknown until evidence identifies it

### Scenario C: Do not trigger for a mechanical edit

The user asks to normalize Markdown list spacing while retaining all established terms and headings.

Requirements checklist:
1. [critical] Do not create a referent table
2. Do not delay the mechanical edit for terminology approval

### Scenario D: Response-only two-stage submission

The user asks for a proposed public boolean name in chat and supplies no output path.

Requirements checklist:
1. [critical] Return only a standalone referent table in the first response
2. Do not create a file
3. Wait for confirmation before proposing the final identifier or related prose

### Scenario E: Correct an approved row

After seeing the table, the user points out that one row describes an event but labels it as a state.

Requirements checklist:
1. [critical] Rewrite the row and wait for confirmation again
2. Do not preserve the incorrect row and compensate with explanatory prose
3. Do not overwrite user-authored text

## Failure Pattern Ledger

- `candidate term filled before referent and role`
- `multiple semantic roles collapsed into one row`
- `reasoning sequence compressed into a working label`
- `target body drafted before table approval`
- `incorrect row patched with explanatory prose`
- `mechanical edit triggers unnecessary referent table`

## Iter 1 — Blank-slate behavior check (2026-07-21)

### Changes

- Initial independently authored Skill based on the referents-before-labels workflow.

### Execution results

Each scenario ran in a fresh subagent context that received only the Skill path and the user-style scenario. The requirement checklist was withheld from the executor and applied afterward by the parent.

| Scenario | Result | Observation |
| --- | --- | --- |
| A | Pass | Split the numeric value, start condition, and event into three rows, then returned only the table. |
| B | Pass | Preserved test → record results → isolate cause → choose countermeasure and kept the cause unknown. |
| C | Pass | Performed only the requested Markdown spacing edit without creating a referent table. |
| D | Pass | Returned a standalone one-row table in chat without creating a file or presenting follow-on prose. |
| E | Pass | Replaced the incorrect `state` role with `event` in the row and returned only the corrected table. |

All five critical requirements passed. No target body or final identifier was generated before the confirmation boundary.

### Structured reflection

- The role split and two-stage submission contract were reproduced without exposing the checklist to executors.
- Scenario B kept records, means, and purpose distinct instead of compressing the sequence into one working label.
- Scenario C confirmed that the mechanical-edit exclusion prevents unnecessary terminology approval.
- The table output cannot reveal the executor's token-by-token field completion order; the independently understandable concrete-referent columns are the observable proxy for the referent-before-label constraint.

### Failure pattern ledger update

None of the listed failure patterns appeared in Iter 1. Keep the ledger unchanged for regression checks.

### Next fix proposal

- Make no Skill-body change from Iter 1. Re-run these scenarios after any change to the workflow, table contract, or submission boundary.
