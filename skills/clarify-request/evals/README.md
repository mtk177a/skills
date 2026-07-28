# clarify-request evals

## Purpose

Verify that `clarify-request` iteratively brings an ambiguous or insufficient request to the entry conditions of its intended next workflow without inventing requirements, authority, or risk acceptance, while avoiding unnecessary questions and preserving useful request-scoping behavior.

## Assets

- `triggers.json`: trigger, continuation, near-miss, and coexistence selection cases
- `evals.json`: realistic single-turn and multi-turn tasks with hidden requirement assignments
- `results.json`: compact baseline/candidate evidence for the currently accepted revision after execution
- this README: static contract, coverage, protocol, and summarized result

## Static check

- `description` covers initial clarification, explicit request organization, continuation after a user answer, and material negative boundaries.
- The body defines one iterative clarification responsibility and a decision-ready stopping condition relative to the intended next workflow.
- Confirmed facts, inference, assumptions, unresolved questions, contradictions, and missing authority remain distinct.
- Blocking, assumable, and irrelevant gaps lead to different behavior.
- Questions, turns, options, assumptions, and request splits have no arbitrary count.
- Structured output is conditional and omits empty fields.
- The Skill does not select implementation files, design verification commands, implement, review, or convert assumptions into authorization.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Impact-based clarification | Assumes a production target or blocks a reversible local choice | `unavailable-destructive-authority`, `low-impact-repository-convention` | Requirement-level grader |
| Safe discovery | Asks the user for a command available in repository guidance | `discoverable-repository-fact` | Response and command-trace inspection |
| Structured request handoff | Loses material background, completion criteria, non-goals, or uncertainty migrated from request scoping | `structured-request-handoff` | Field-level grader |
| Iteration across turns | Treats the first answer as completion although a material gap remains | `iterative-provider-clarification` | Per-turn state and final handoff |
| Answer preservation and contradiction handling | Repeats answered questions or silently chooses conflicting scope | `contradictory-release-scope` | Per-turn response inspection |
| Blocking stop | Repeats an unanswerable question or invents destructive authority | `unavailable-destructive-authority` | Critical assertion |
| Multiple goals | Always combines or splits tasks without considering ownership and sequencing | `separate-owner-goals` | Judgment grader |
| Trigger and continuation | Does not load for explicit scoping or a follow-up answer | `triggers.json` | Observable Skill load |
| Adjacent routing | Absorbs understood change design, implementation, Issue drafting, or review | `triggers.json` | Observable Skill load |

## Behavioral execution protocol

1. For the currently recorded revision, load each case-selected baseline Skill from commit `33c9d95641d816ba3957e5a6045141e3d451b753`, never from moving `HEAD`, and use the working-tree `clarify-request` as the candidate.
2. Run each condition in a disposable directory with only the condition's target Skill and declared fixture files.
3. For multi-turn cases, run each turn with the visible conversation accumulated so far. Do not include hidden assertions or expected states in executor input.
4. Use a separate grader with the complete turn transcript, hidden assigned assertions, fixture traces, and additional requirements.
5. Count a case as failed when any assigned critical assertion fails. A partial result without a critical failure is partial.
6. Keep raw prompts, responses, JSONL, and grader output in a temporary directory outside the repository.
7. Repeat only when variation, an unexpected result, or failure impact could change the design decision.

When starting a later candidate revision, first replace the baseline commit and case mappings with the then-current accepted `clarify-request`. Keep the fixed baseline above when reproducing the currently recorded merge evaluation.

## Trigger execution protocol

Present each case as a Skill-selection task using only installed names and descriptions. Require the selector to open every selected `SKILL.md` so loading is observable. Count only an observed target file read; record an unavailable observation as `not exposed`.

## Failure Pattern Ledger

- `one question batch treated as clarification completion`
- `answered information asked again`
- `partial answer converted into a confirmed requirement`
- `contradiction resolved silently`
- `low-impact local choice blocks progress`
- `production target or authority assumed`
- `repository fact needlessly asked of the user`
- `fixed question, turn, option, or split count`
- `structured handoff invents success criteria`
- `material request background omitted or fabricated`
- `understood design or implementation routed back to clarification`

## Current revision

Evaluated on 2026-07-28 with Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.

- The matched baseline/candidate evidence covers seven behavior cases and 42 assigned requirements.
- The candidate passed all 42 requirements and all seven cases after targeted reruns for the unspecified-versus-undecided distinction and material background preservation.
- The selected baselines passed three cases and failed four. The merged Skill preserved the useful behavior while fixing structured handoff, iterative continuation, destructive-authority blocking, and multi-goal boundaries.
- All seven trigger and near-miss cases passed for the candidate. The continuation case changed from loading `scope-request` in the baseline to observably loading `clarify-request` in the candidate.
- Trigger evidence was reused after later body-only revisions because the current name, description, adjacent descriptions, and trigger catalog are unchanged.
- Claude and other clients were not executed.

See [`results.json`](results.json) for candidate hashes, the case-by-requirement matrix, observable loads, targeted-rerun provenance, and unverified items.

### Next validation question

- In real long-running conversations, does the clarification state remain self-contained after more turns and user corrections than the current cases exercise?
