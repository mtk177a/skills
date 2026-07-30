# triage-agent-usage evals

## Purpose

Verify that `triage-agent-usage` selects the lightest adequate agent, tool, model capability, context, and work-unit structure without performing the task, inventing availability, or taking over learning calibration.

## Assets

- `triggers.json`: trigger, near-miss, and coexistence selection cases
- `evals.json`: previous-name and candidate behavior cases with hidden requirement assignments
- `results.json`: compact evidence for the accepted revision after execution
- this README: static contract, coverage, protocol, and summarized results

## Static check

- `description` covers execution-surface, capability, and operational-delegation selection and excludes learning calibration, substantive design, and task execution.
- Recommendations start from required capability and the lightest adequate available option.
- Heuristics do not form a fixed tool mapping or assume a named model or profile exists.
- Additional or parallel agents require a concrete context, specialization, verification, or latency benefit.
- Work units retain objective, constraints, authority, evidence, and verification while minimizing context.
- Learning intent produces an optional `calibrate-learning-support` handoff rather than a teaching plan inside this Skill.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Lightest adequate surface | Recommends a coding agent for a text-only task | `text-only-task` | Critical recommendation assertion |
| Capability escalation | Uses a lightweight option for consequential repository work or names an unavailable profile as fact | `high-risk-repository-change` | Capability and uncertainty grader |
| Work-unit design | Splits by arbitrary file count or produces an unreviewable broad unit | `high-risk-repository-change` | Handoff inspection |
| Additional-agent restraint | Introduces subagents without a concrete benefit | `small-established-pattern-change` | Critical restraint assertion |
| Learning boundary | Designs comprehension checkpoints instead of returning an optional handoff | `learning-goal-with-tool-selection` | Coexistence grader |
| Trigger boundary | Misses explicit tool selection or absorbs implementation and learning calibration | `triggers.json` | Observable Skill load |

## Behavioral execution protocol

1. Load the previous-name condition from baseline commit `82722ad5cfe003c164bb6b3736fae3612d4612a2` with `calibrate-ai-learning` as the adjacent learning workflow, and use the working-tree Skill with `calibrate-learning-support` for the candidate.
2. Run each condition in a disposable directory with only the target Skill and task input.
3. Keep hidden assertions and expected conclusions out of executor input.
4. Grade each condition with a separate grader using the response and assigned requirements.
5. A failed critical assertion fails the case. A partial result without a critical failure is partial.
6. Keep raw prompts, responses, JSONL, and grader output outside the repository.
7. Repeat only when variation, an unexpected result, or failure impact could change the decision.

## Trigger execution protocol

Present each case as a Skill-selection task using only installed names and descriptions. Require the selector to open every selected `SKILL.md` so loading is observable. Count only an observed target file read; record an unavailable observation as `not exposed`.

## Failure Pattern Ledger

- `heavy coding agent recommended for text-only work`
- `named model or profile availability invented`
- `task importance used as the only escalation reason`
- `parallel agents selected by default`
- `context minimized past objective or verification needs`
- `substantive task performed during triage`
- `learning calibration absorbed into tool selection`

## Current revision

Evaluated on 2026-07-30 with Codex CLI 0.146.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.

- The candidate passed all four behavior cases and all 29 assigned requirements.
- The previous-name condition passed three cases and failed the learning-goal handoff case because it returned `calibrate-ai-learning`; 28 of 29 assigned requirements passed.
- All six trigger, near-miss, and coexistence cases passed under both conditions.
- The affected behavior case was rerun under both conditions. The other three behavior grades reuse evidence from the accepted baseline revision because their instructions are unchanged.
- The candidate preserves operational tool and capability selection while handing task-specific learning support to `calibrate-learning-support`.
- Claude and other clients were not executed.

See [`results.json`](results.json) for candidate hashes, the case-by-requirement matrix, observable Skill loads, and unverified items.

### Next validation question

- In real use, are availability assumptions and the meaning of model capability stated precisely enough across clients whose tool and profile names differ?
