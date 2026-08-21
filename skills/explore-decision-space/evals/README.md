# explore-decision-space evals

## Purpose

Verify that `explore-decision-space` adds value beyond both ordinary no-Skill behavior and the retired `diversify-agent-search` identity by expanding the unsettled decision layer, preserving evidence boundaries, avoiding unsupported winners, and handing adjacent work to its owning workflow.

## Iter 0 — Static check

- `description` covers proactive problem-space and solution-space convergence and excludes clarification, terminology definition, failure diagnosis, selected-approach planning, implementation, and automated optimization.
- The body distinguishes problem space, solution space, both, and no-expansion states.
- Completion does not require a fixed candidate, iteration, or agent count.
- The workflow is read-only and self-contained.
- `evals.json` keeps executor inputs separate from assertions.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grader |
| --- | --- | --- | --- |
| Problem-space expansion | Treats the first proposed fix as the problem definition | `problem-frame-fixation` | Comparative assertion grader |
| Solution-space expansion | Produces only variants of the existing mechanism | `solution-anchor-fixation` | Comparative assertion grader |
| Layer order | Expands solutions before resolving incompatible problem frames | `both-layers-unsettled` | Comparative assertion grader |
| Recovery handoff | Repeats diagnosis, invents evidence, or forces the next implementation | `diversify-handoff` | Comparative assertion grader |
| Clarification boundary | Invents scope or authority instead of handing off | `clarification-near-miss` | Comparative assertion grader and routing |
| Selected-approach boundary | Treats implementation planning as decision-space exploration | `selected-approach-near-miss`, `design-near-miss` | Comparative assertion grader and routing |
| Simple work boundary | Adds exploration ceremony to a local reversible edit | `simple-reversible-choice`, `implementation-near-miss` | Comparative assertion grader and routing |
| Terminology boundary | Reframes a referent-definition problem as option search | `terminology-near-miss` | Observable Skill load |
| Read-only authority | Edits files or runs proposed experiments | All applicable behavior cases | Command trace and fixture hash |

## Execution protocol

Behavior evaluation uses the same request, Codex model, reasoning setting, read-only sandbox, adjacent Skills, and comparative grader for three conditions:

- current: `diversify-agent-search` at commit `7317e1b7605e835a0452f9aaf7bbd0140cf6ae97`
- no-Skill: no decision-space Skill, with adjacent Skills unchanged
- candidate: the accepted `explore-decision-space`

The blank-slate executor receives only the condition's Skill content, installed adjacent Skills, and the scenario input. A separate grader receives the three responses, command traces, fixture invariants, and hidden assertions. Raw JSONL and complete responses stay in a temporary directory and are not committed.

Routing evaluation presents only names and descriptions, requires the selector to open every selected `SKILL.md`, and counts only observed file reads. `not exposed` and `not executed` do not pass.

The exact temporary drivers used for the accepted revision were:

```bash
python3 <temporary-evaluation-dir>/run-eval.py
python3 <temporary-evaluation-dir>/rerun-decisive.py
```

## Result

The three-way comparison ran on 2026-07-29 with Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.

- The candidate and no-Skill behavior both passed the proactive problem-frame, solution-anchor, and combined-layer cases.
- In the decisive exhausted-anchor handoff, the initial run graded current `fail`, no-Skill `fail`, and candidate `pass`.
- A focused rerun graded current `partial`, no-Skill `partial`, and candidate `pass`, reproducing the candidate's strict improvement.
- The candidate had no critical regression against the better baseline and no candidate routing failure.
- Candidate routing loaded `explore-decision-space` for problem-space, solution-space, and exhausted-anchor requests and selected the adjacent owner for all four near-miss cases.
- A boundary rubric that initially treated valid same-turn composition with `design-changes` as takeover was corrected. Regrading the unchanged responses produced `pass` for all three conditions.
- No behavior condition modified its fixture.

The accepted decision is to replace `diversify-agent-search` with `explore-decision-space`. See [`results.json`](results.json) for the case-by-requirement record and observable routing results.

## Evidence reuse under the cost-bounded policy

The replacement decision required relative evidence rather than an absolute
candidate pass. The predecessor and no-Skill conditions could already produce
acceptable results on several ordinary exploration cases, so adoption depended
on showing a strict candidate improvement on the exhausted-anchor handoff
without a critical regression against the better baseline. The recorded
three-way comparison and focused rerun provide that decision-relevant evidence.

The evidence is reused without another execution because the current
`SKILL.md` hash (`sha256:ff674c337a5fd6d3c11581e2077c91e4dfcafa425c4e9a6921ee7306db85a273`),
the evaluated responsibility, the decisive requirement, and the behavior
fixtures remain those recorded in `results.json`. The comparison record remains
immutable; this README addition documents the reuse decision and is not a new
behavior result. Rerunning only to conform to the newer policy would not change
acceptance.

The reuse claim is limited to the recorded Codex CLI 0.145.0,
`gpt-5.6-sol`, high reasoning, read-only sandbox, and evaluated candidate
revision. It does not verify another client, model, reasoning setting, or a
later change to the Skill body or decisive responsibility.

## Unverified

- Claude Code and other clients
- other models and reasoning settings
- implicit invocation frequency in normal long-running sessions
- automated evolutionary search, which remains outside this Skill

## Next validation question

- Does normal usage observably invoke the Skill before premature convergence often enough to justify its catalog and context cost?
