# define-referents evals

## Purpose

Verify that `define-referents` makes the Grounding-then-Naming order observable, preserves uncertainty and context-specific semantic roles, and returns a naming constraint to the originating workflow without inventing missing meaning, forcing universal approval, creating unauthorized files, or taking over downstream work.

## Assets

- `triggers.json`: trigger, non-trigger, near-miss, continuation, and coexistence routing cases
- `evals.json`: realistic tasks and hidden requirement assignments
- `results.json`: compact baseline/candidate evidence for the currently accepted revision after execution
- this README: static contract, coverage, protocol, and summarized result

## Static check

- `description` targets terminology-specific ambiguity and excludes overall request clarification, downstream authoring, mechanical edits, established-name reuse, and ordinary wording.
- The Skill ends with a referent-and-naming handoff rather than writing the downstream document, report, design, or code.
- Grounding and Naming use separate observable tables, and no candidate term or first-use definition appears in Grounding.
- `Ready`, `Decision required`, and `Blocked` have distinct entry and reporting conditions.
- Confirmation is conditional on a material semantic decision rather than universal.
- A separate table file requires explicit authorization.
- Semantic roles are contextual rather than a closed taxonomy, and table splitting follows meaning rather than row count.
- The bundled reference is self-contained and the external article is provenance only.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Observable Grounding before Naming | Generates a label or definition while supposedly grounding the referent | `threshold-condition-event`, `low-impact-local-identifier` | Response-order and content inspection |
| Distinct referents and sequence | Reuses one fluent label for a threshold, condition, and event or hides an unknown cause | `threshold-condition-event`, `incident-unknown-cause` | Requirement-level grader |
| Missing input handling | Invents the meaning of an underspecified boolean to complete the table | `underspecified-public-boolean` | Critical assertion |
| Conditional decision boundary | Always waits for confirmation or silently selects a public contract | `low-impact-local-identifier`, `public-contract-alternatives` | State and question inspection |
| Context-specific roles and semantic splitting | Forces actor, component, interface, or policy into the old role list or splits at six rows | `contextual-roles-coherent-flow` | Table inspection |
| File and downstream ownership | Creates a sidecar or drafts the design/code under the semantic-preflight Skill | `design-handoff-no-sidecar`, `implementation-handoff-no-edit` | Fixture hashes and response inspection |
| Correction recovery | Retains a naming proposal whose Grounding row was corrected | `corrected-grounding-row` | Multi-turn comparison |
| Trigger boundary | Misses explicit referent work or absorbs clarification, ordinary design, implementation, investigation, and mechanical writing | `triggers.json` | Observable Skill load |
| Coexistence | Prevents or replaces the originating specialized workflow | design, incident, and implementation handoff cases | Requirement-level grader |

## Behavioral execution protocol

1. Use `define-referents` from commit `45bb765ca110bd3e0b4ab2294b7ed030a4ada55d` as the immutable baseline and the working-tree Skill as the candidate.
2. Run each condition in a disposable directory containing only the selected target Skill, its required reference, any declared adjacent Skill, and fixture files.
3. Give the executor only the visible user turns and fixture. Keep assertion statements, additional requirements, and expected conclusions hidden.
4. Use a separate Codex grader with the transcript, assigned assertions, fixture hashes, and additional requirement.
5. A failed critical assertion fails the case. A partial result without a critical failure is partial.
6. Keep prompts, responses, JSONL, grader output, and disposable fixtures under `/tmp`; do not commit raw traces.
7. Run each affected case once per condition. Repeat only when variation, an unexpected result, or failure impact could change the design decision.

## Trigger execution protocol

Present each case as a Skill-selection task with only installed names and descriptions. Require the selector to open every selected `SKILL.md` so loading is observable. Count only an observed target file read; record an unavailable observation as `not exposed`.

## Failure Pattern Ledger

- `candidate term or definition appears in Grounding`
- `distinct referents collapsed under one label`
- `missing meaning invented to finish a table`
- `low-impact naming stopped for universal confirmation`
- `material public meaning selected silently`
- `context-specific role forced into a closed taxonomy`
- `table split only because it exceeds six rows`
- `target-document authorization treated as sidecar authorization`
- `semantic preflight drafts or edits downstream content`
- `corrected grounding retains stale naming`
- `ordinary clarification, design, investigation, implementation, or mechanical writing routed to define-referents`

## Current revision

Evaluated on 2026-07-28 with Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.

- The matched baseline/candidate evidence covers nine behavior cases and 46 assigned requirements.
- The candidate passed all 46 requirements and all nine cases after correcting one grader requirement that contradicted the confirmed need for two public facts. The baseline passed no case, with 21 passed, four partial, and 21 failed requirements.
- The candidate made Grounding-then-Naming observable, distinguished conditional confirmation from low-impact completion, supported context-specific roles and semantic table splitting, preserved missing information and corrections, and left design, incident, and implementation ownership downstream.
- Nine current trigger, non-trigger, continuation, near-miss, and coexistence results remain applicable. The mechanical Markdown exclusion was changed from routing to the retired `format-markdown` Skill into an unhandled exclusion and has not been rerun.
- Claude and other clients were not executed.

See [`results.json`](results.json) for candidate hashes, the case-by-requirement matrix, observed Skill loads, grader-correction provenance, and unverified items.

### Next validation question

- Does the redesigned Skill preserve its semantic guardrail while allowing the originating workflow to continue without an unnecessary user-confirmation turn?
