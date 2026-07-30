# choose-ai-execution-setup evals

## Purpose

Verify that `choose-ai-execution-setup` produces an actionable recommendation for a concrete task from confirmed available choices while keeping access, tools, model capability, reasoning effort, context, permissions, verification, topology, and user-supplied constraints independent.

## Assets

- `triggers.json`: trigger, near-miss, and coexistence selection cases
- `evals.json`: current, no-Skill, and candidate behavior cases with hidden requirement assignments
- `results.json`: compact evidence for the accepted revision after execution
- this README: static contract, coverage, protocol, and summarized results

## Static check

- `description` targets explicit execution-setup advice and excludes task execution, implementation-unit design, client-setting changes, and learning calibration.
- Required capability and confirmed availability remain distinct.
- Model capability and reasoning effort are evaluated and reported separately.
- A completion state, gating prerequisites, decision-critical unknowns, and the next actor make the recommendation actionable.
- Topology is selected only from defined work units, and parallelism accounts for ownership, shared state, verification, parent integration, and coordination cost.
- The Skill performs no task, configuration change, permission grant, or automatic orchestration.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Confirmed setup choice | Chooses unnecessary tools or an unavailable named setup | `confirmed-text-options` | Availability and handoff assertions |
| Missing input handling | Guesses a setup without a concrete task or available choices | `missing-availability` | Completion-state and availability assertions |
| Independent dimensions | Treats stronger reasoning as a substitute for access or model capability | `routine-high-impact` | Dimension and grounding assertions |
| Bounded parallelism | Uses an integrating parent as an unconfirmed worker or ignores capacity | `parallel-independent-units` | Topology and parallel-safety assertions |
| Shared-state conflict | Parallelizes competing writes and evolving shared context | `shared-write-conflict` | Critical parallel-safety assertion |
| Task-design boundary | Invents work units before choosing topology | `undefined-work-units` | Task-design handoff assertion |
| Learning coexistence | Absorbs learning calibration or drops its explicit handoff | `learning-coexistence` | Learning-boundary assertion |
| Trigger boundary | Absorbs implementation, design, review, learning, or setting changes | `triggers.json` | Observable Skill loads |

## Behavioral execution protocol

1. Load `triage-agent-usage` from baseline commit `c464b605b1cfbb47d53fa7143aa5789d1b60387e`, the working-tree candidate, and a no-Skill condition in separate disposable directories.
2. Run candidate behavior first with Codex CLI, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.
3. Continue to the comparison only after every candidate response assigns one completion state and the candidate trigger boundary passes.
4. Keep hidden assertions and expected conclusions out of executor input.
5. Grade blinded responses with a separate executor. A failed critical assertion fails the condition; a partial result without a critical failure is partial.
6. Keep raw prompts, responses, JSONL, and grader output outside the repository.
7. Repeat only when variation, an unexpected result, or failure impact could change the decision.

## Trigger execution protocol

Present each case as a Skill-selection task with the target and adjacent Skills installed. Require the selector to open every selected `SKILL.md` so loading is observable. Count only observed target file reads; record an unavailable observation as `not exposed`.

## Failure Pattern Ledger

- `required access replaced by stronger reasoning`
- `model capability inferred from reasoning effort`
- `named setup availability invented`
- `recommendation ready despite a gating unknown`
- `implementation units invented during topology selection`
- `parallel agents selected despite shared state or write conflicts`
- `integrating parent counted as an unconfirmed worker`
- `task execution or client configuration absorbed into setup advice`
- `explicit learning goal absorbed or dropped instead of handed off`

## Current revision

Evaluated on 2026-07-30 with Codex CLI 0.146.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.

- The candidate passed all seven behavior cases and all 41 assigned assertions.
- Under the redesigned contract, the current `triage-agent-usage` baseline passed no behavior case; two were partial and five failed.
- Under the same contract, the no-Skill condition passed no behavior case.
- The candidate passed all eight trigger, near-miss, and coexistence cases. The current Skill also selected the expected owner in all eight cases.
- Without the target Skill, the predefined-topology request loaded `design-changes`; the other seven routing cases selected the expected available owner or no target.
- After the final parent-worker boundary change, `parallel-independent-units` was rerun. Other behavior evidence was reused because the added instruction applies only when an integrating parent could be counted as a worker.
- Trigger evidence was reused after body-only refinements because the `description` and adjacent Skill metadata were unchanged.
- Claude and other clients were not executed.

See [`results.json`](results.json) for candidate hashes, the case-by-requirement matrix, observable Skill loads, and unverified items.

### Next validation question

- In real use, do users provide enough information about available client surfaces and permissions for conditional recommendations to converge without unnecessary clarification?
