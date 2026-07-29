# diversify-agent-search evals

## Purpose

Verify that `diversify-agent-search` owns broad structural candidate search only after the current design anchor is exhausted or local distinguishing checks are insufficient, while leaving repeated-attempt reconstruction and one-check recovery to `break-failure-loop`.

## Assets

- `triggers.json`: focused trigger, near-miss, and coexistence routing cases for the revised description
- this README: existing behavior scenarios, routing protocol, and summarized result

## Static check

- `description` requires broad structural candidate search, not stagnation alone.
- A single diagnostic or missing input that can resolve a repeated-attempt loop remains outside this Skill.
- The body continues to require candidate archives, diversity axes, case-level evaluation, and protected evaluation assets.
- The Skill remains self-contained and does not require another Skill, agent, subagent, or multi-agent workflow.
- No behavior instructions, scripts, dependencies, or permissions changed in this revision.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Exhausted-anchor routing | Fails to trigger when structurally different candidates are explicitly needed | `exhausted-anchor-candidate-search` | Observable Skill load |
| Case-level candidate search | Treats an average-score comparison as local diagnosis | `case-level-candidate-search` | Observable Skill load |
| Recovery boundary | Activates when one diagnostic or missing input can resolve the loop | `reconstruct-only`, `missing-input-only` | Observable Skill load |
| Coexistence | Suppresses `break-failure-loop` or fails to join after its Diversify decision | `reframe-then-diversify` | Observable Skill loads |
| First failure | Activates before any design anchor is exhausted | `first-implementation-failure` | Observable Skill load |

## Existing behavior scenarios

The behavior body was not changed in this revision. Its prior scenarios remain unexecuted:

- prompt tuning stuck in local edits should produce structurally different candidates
- average score should not hide case-level strengths and weaknesses
- protected evaluation assets should not be relaxed to make a candidate pass
- the Skill should remain useful without companion Skills

These scenarios require a separate behavior revision or evidence need before execution. They are not counted as passing.

## Trigger execution protocol

Present each case as a Skill-selection task using the names and descriptions for the selected baseline or candidate condition. Require the selector to open every selected `SKILL.md` so loading is observable. Count only observed file reads and record unavailable observations as `not exposed`.

## Failure Pattern Ledger

- `stagnation alone treated as structural-search authority`
- `one-check recovery expanded into a candidate portfolio`
- `exhausted anchor missed despite explicit candidate-search request`
- `break-failure-loop suppressed in a compound recovery request`
- `first implementation failure treated as design-search stagnation`

## Current revision

Routing was evaluated on 2026-07-29 with Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.

- Both baseline and candidate passed all six focused trigger, near-miss, and coexistence cases.
- The candidate continued to load for exhausted-anchor and case-level candidate search.
- It did not load for one-diagnostic recovery, missing-input recovery, or a first implementation failure.
- The compound recovery request observably loaded both `break-failure-loop` and `diversify-agent-search`.
- The unchanged behavior scenarios were not executed and are not counted as passing.
- Claude Code, other clients and models, and repeated-run stability were not evaluated.

See [`results.json`](results.json) for candidate hashes, observable loads, and unverified items.

### Next validation question

- Does the narrower description preserve explicit structural-search activation while avoiding activation during diagnostic recovery?
