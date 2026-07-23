# audit-agent-guidance evals

## Purpose

Verify that the Skill diagnoses guidance behavior and root causes without inheriting the current artifact layout, suppressing structural alternatives, or claiming unobserved behavior.

## Assets

- `triggers.json`: trigger and near-miss cases, run policy, and trigger pass thresholds
- `evals.json`: realistic output-quality tasks and candidate assertions
- this README: procedure, environment, and summarized results

The pre-rename Skill is the required baseline for this revision. Keep baseline copies, raw JSONL, and full session output outside the repository.

## Static check

- [x] `name`, directory, and `description` agree on durable guidance auditing.
- [x] The body defines single-Skill and cross-surface audits.
- [x] Evidence, impact, confidence, affected surfaces, and verification are required for findings.
- [x] Ordinary diff review, new guidance design, and standalone `.rules` review remain out of scope.
- [x] The reporting contract is defined without fixed headings or an arbitrary finding limit.

## Execution protocol

Use the same client, model, reasoning effort, sandbox, task input, and adjacent Skill configuration for baseline and candidate.

1. Run every trigger case three times for the previous version and candidate. Use the trigger-selection protocol in `triggers.json`: select from metadata, open each selected `SKILL.md`, report the selected names, and do not solve the underlying task.
2. Count a trigger only when the client exposes an event showing that the Skill was loaded. If Skill loading is not observable, record `not exposed`; do not infer loading from output text.
3. Run output-quality cases against the previous version and candidate from a temporary Git repository.
4. Evaluate the candidate assertions in `evals.json`, recording evidence for pass or fail.
5. Evaluate both isolation and coexistence with `design-skill`, `design-agent-instructions`, and `review-changes`.
6. Record client, model, reasoning effort, date, run count, trigger rate, assertion results, and any exposed token or duration values.

For Codex CLI, use `gpt-5.6-sol`, high reasoning, and a read-only sandbox. Invoke it with:

```bash
codex exec --ephemeral --json --ignore-user-config --ignore-rules --sandbox read-only
```

Disable an older globally installed copy of this audit Skill during candidate runs through a `skills.config` override. Do not silently substitute another model if `gpt-5.6-sol` is unavailable.

## Results summary

| Evaluation | Baseline | Candidate | Notes |
| --- | --- | --- | --- |
| Static validation | valid; 44 target Markdown issues | valid; 1 inherited translation-note issue | `quick_validate.py`, JSON parsing, and `git diff --check` passed; target lint used markdownlint-cli2 0.23.1 with MD013 disabled |
| Repository-wide Markdown baseline | not reproduced | not reproduced | The historical 182-issue baseline was not reproducible with the current tool version, whose default run reported 1,148 issues; no pass is claimed |
| `skills-ref` validation | not executed | not executed | The command was not installed, and no dependency was added |
| Trigger evaluation | 15/15 expected loads; 3/15 unexpected loads | 15/15 expected loads; 0/15 unexpected loads | Three runs per case; the previous version loaded for standalone `.rules` review |
| Output-quality evaluation | 5/9 full assertion passes | 9/9 assertion passes | Five tasks in both isolation and coexistence; all 20 runs exited successfully |
| Isolation / coexistence | Conclusions were stable, but fixed-format and minimal-change bias remained | Conclusions and assertion results were stable | No run used filesystem or network evidence outside the selected Skill files |
| Claude Code | not executed | not executed | Out of scope for this revision |

Do not treat `not executed` or `not exposed` as a pass.

## Assertion comparison

| Assertion | Baseline | Candidate | Evidence summary |
| --- | --- | --- | --- |
| Start from the intended outcome | partial | pass | The previous version led with artifact edits in the multi-surface case; the candidate defined expected behavior before diagnosis |
| Do not assume the current artifact split | fail | pass | The candidate considered keeping, removing, moving, merging, and replacing guidance |
| Do not cap material findings | fail | pass | The previous version compressed the multi-surface case into five groups; the candidate reported seven distinct findings |
| Separate evidence from inference | pass | pass | Both versions marked unknown `.rules` effects and unavailable behavior evidence as unconfirmed |
| Separate symptoms from root causes | pass | pass | Both recognized that stronger wording would not fix an unread reference; the candidate made the distinction systematic |
| Permit structural alternatives | pass | pass | Both considered consolidation or relocation; the candidate also compared no-guidance and replacement conditions |
| Keep full diagnosis separate from staged rollout | fail | pass | The previous version selected a minimal first change while suppressing findings; the candidate retained the full diagnosis and staged only rollout |
| Do not require a `Never` section universally | pass | pass | Both healthy-guidance runs recommended no change |
| Leave behavior unconfirmed without evidence | pass | pass | Both static-only runs withheld a behavioral conclusion; only the previous version still forced a reporting-format change |

## Result record

- Date: 2026-07-23
- Client: Codex CLI 0.145.0
- Model: `gpt-5.6-sol`
- Reasoning: high
- Sandbox: read-only
- Formal run count: 80 total; 60 trigger runs and 20 output-quality runs
- Baseline trigger result: 15/15 expected loads and 3/15 unexpected loads
- Candidate trigger result: 15/15 expected loads and 0/15 unexpected loads
- Assertion results: baseline 5/9 full passes; candidate 9/9 passes
- Baseline usage: 1,466,280 input, 806,400 cached input, 21,030 output, and 10,360 reasoning tokens; 651.366 cumulative seconds
- Candidate usage: 1,479,008 input, 1,002,496 cached input, 32,277 output, and 8,941 reasoning tokens; 880.412 cumulative seconds
- Unobserved or unexecuted checks: explicit Skill invocation does not always expose a dedicated load event; Claude Code and `skills-ref` were not run; the historical repository-wide 182-issue Markdown baseline was not reproducible with the current tool version
- Conclusion: the candidate preserved expected trigger recall, removed the standalone `.rules` false positive, and satisfied every output-quality assertion in isolation and coexistence

Raw JSONL, full responses, smoke runs, and the previous Skill snapshot remain in temporary directories outside the repository.
