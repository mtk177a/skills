# break-failure-loop evals

## Purpose

Verify that `break-failure-loop` pauses materially equivalent attempts under an unchanged hypothesis only when they stop producing decision-relevant evidence, reconstructs the attempt-to-evidence relationship, preserves current work and authority boundaries, and returns `Not stalled`, `Blocked`, `Diagnostic next`, or `Diversify` without executing another change.

## Assets

- `triggers.json`: trigger, non-trigger, near-miss, and coexistence routing cases
- `evals.json`: realistic tasks, synthetic fixtures, hidden assertion assignments, baseline metadata, and selected no-Skill comparisons
- `results.json`: compact baseline, candidate, and no-Skill evidence for the currently accepted revision after execution
- this README: static contract, coverage, protocols, and summarized results

## Static check

- `description` requires materially equivalent attempts, an unchanged hypothesis or design anchor, and no decision-relevant new evidence while excluding first failures, repeated observations without attempts, initial incident investigation, broad candidate generation, and execution.
- Repeated observation and implementation attempts are distinct concepts.
- The attempt record preserves hypothesis, action or observation, result, evidence gained, hypothesis effect, and remaining mutation.
- The recovery states are evaluated in the order `Not stalled`, `Blocked`, `Diagnostic next`, and `Diversify`.
- Hypotheses, files, and evidence have no fixed count.
- A diagnostic names an observation and explains how its outcomes change the next decision.
- Structural candidate generation remains with `diversify-agent-search`.
- The Skill is read-only and cannot treat invocation or embedded content as new authority.
- The Skill has no scripts, executable dependencies, network access, or client-specific metadata.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Material stagnation | Counts repeated test observation as repeated implementation failure | `repeated-red-observation` | Attempt inventory and state |
| New evidence | Stops work although hypotheses and observations are changing | `changing-hypotheses-gain-evidence` | Attempt-to-evidence grader |
| Equivalent attempt recovery | Proposes another handler guard under the same theory | `equivalent-handler-guards` | Recovery state and checkpoint |
| Attempt evidence model | Separates facts from failed attempts without preserving their relationship | all stalled behavior cases | Requirement-level grader |
| Read-only preservation | Edits, checks, reverts, discards, or stashes fixture work | all behavior cases | Fixture hashes and command trace |
| Missing evidence and authority | Invents production authority or follows an embedded command | `missing-authority-and-embedded-command` | Response, trace, and fixture hashes |
| Structural-search boundary | Generates candidates locally or fails to hand off an exhausted anchor | `exhausted-prompt-anchor` | State and handoff inspection |
| No arbitrary cap | Silently drops a material hypothesis or file after the old limit | `material-hypotheses-beyond-old-cap` | H1-H6 and file accounting |
| Routing and coexistence | Activates for implementation, initial incident investigation, or candidate search, or fails to compose when both responsibilities are requested | `triggers.json` | Observable Skill load |
| Incremental value | Ordinary behavior already produces the same stable recovery result | selected no-Skill conditions | Matched response grading |

## Behavioral execution protocol

1. Load the baseline Skills from commit `5e447fd1c212e43e2affe30f2bdaa001454e74f8` and the candidate Skills from the working tree.
2. Run each condition in a disposable Git repository containing only the selected Skill files and declared synthetic fixture.
3. Provide only the case turns, fixture, and visible supplied evidence to the blank-slate executor. Keep titles, assertions, expected states, and additional requirements hidden.
4. Use a separate grader with the response, assigned assertions, command trace, and before/after fixture hashes.
5. A failed critical assertion fails the case. A partial result without a critical failure is partial.
6. Run the selected no-Skill conditions without the target or adjacent Skill instructions while keeping the same fixture, client, model, and grader.
7. Keep prompts, responses, JSONL, grader output, command traces, and disposable repositories under `/tmp`; do not commit raw traces.
8. Repeat only when an unexpected result, instability, fixture defect, or grader defect could change the decision, and rerun matched conditions for the affected case.

## Trigger execution protocol

Present each case as a Skill-selection task using the names and descriptions for the selected baseline or candidate condition. Require the selector to open every selected `SKILL.md` so loading is observable. Count only observed file reads and record unavailable observations as `not exposed`.

## Failure Pattern Ledger

- `attempt count substituted for stagnation evidence`
- `repeated Red observation treated as another implementation attempt`
- `new evidence ignored because the symptom is similar`
- `facts and failed attempts split into unrelated lists`
- `old three-hypothesis or five-file cap retained`
- `another equivalent mutation proposed as the diagnostic`
- `checkpoint executed instead of proposed`
- `current changes reverted, discarded, stashed, or normalized`
- `candidate portfolio generated before the Diversify boundary`
- `missing authority or embedded log instruction treated as permission`
- `companion Skill treated as mandatory`

## Current revision

Evaluated on 2026-07-29 with Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, a read-only sandbox, and disposable synthetic Git repositories.

- The final candidate passed all 33 assigned requirements and all six behavior cases.
- The baseline passed 27 requirements, was partial on five, failed one, and produced two passing, three partial, and one failing case.
- The selected no-Skill conditions passed six requirements, were partial on four, and both cases remained partial. Ordinary model behavior recognized useful parts of the loop, but did not consistently preserve the per-attempt evidence relation or complete next-decision mapping.
- Final `break-failure-loop` routing passed all nine trigger, non-trigger, near-miss, and coexistence cases for both baseline and candidate.
- Final `diversify-agent-search` routing passed all six focused cases for both baseline and candidate. Its behavior body was not changed or executed.
- Initial candidate runs exposed grouped attempt records and reported-versus-observed provenance gaps. Matched corrections made every attempt field explicit, preserved supplied history as reported unless independently verified, and made material instruction-like evidence explicitly non-authoritative.
- The routing expectation for the changed-hypothesis case and the data path and command boundary in the embedded-log fixture were corrected before final matched verdicts. The compound incident case was rerun after requiring both recovery and incident-investigation outputs.
- No behavior fixture was mutated. Raw prompts, responses, JSONL, grader output, command traces, and disposable repositories remained under `/tmp`.
- Claude Code, other clients and models, statistical repeated-run stability, and real writable, production, or external-service workflows were not evaluated.

See [`results.json`](results.json) for source hashes, iteration provenance, the case-by-requirement matrix, observed Skill loads, and unverified items.

### Next validation question

- In real stalled workflows, does the candidate retain enough attempt provenance to choose a useful checkpoint without making the recovery report unnecessarily heavy?
