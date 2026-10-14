# make-it-click evaluation

The executable cases test whether the Skill produces complete, reader-facing explanations across Japanese and English, technical and everyday topics, and new writing and revision.\
They cover a missing case-specific premise, an eligibility condition, excess internal history, unsupported causation, and multiple possible contributors.\
The prompts are separate from `references/explanation-examples.md`; repeating that reference is not an acceptance criterion.

Run selected cases with the existing `scripts/run_skill_evaluation.py` Runner.\
For this new Skill, compare `candidate` with `without-skill` under the same case, model, reasoning effort, and sandbox.\
The Runner hides assertions from the executor.\
Grade each actual response against the case assertions; distinguish the observations from a manual source review.\
Keep raw artifacts under a temporary directory; [report.json](report.json) records only the selected change-scoped evidence.

## Selected coverage

| Responsibility | Acceptance-relevant failure | Selected case and grading |
| --- | --- | --- |
| Connect case-specific premises while preserving uncertainty | Reteach cache basics without explaining the regional-copy read path, or assert the unknown request destination as a proven cause | `ja-tech-premise`: grade mechanism, uncertainty, and finished-output assertions against the response |
| Revise unsupported causal certainty while preserving observations and decision status | Treat averages from different case difficulties as a proven productivity gain, or announce a pending rollout as decided | `en-revise-evidence`: grade comparison, decision, and proportion assertions against the response |

## Current result (2026-10-14)

The evaluated source is commit `88e15fb34b44a8bf4183f43d405ab70c4e49498c`; the `SKILL.md` SHA-256 is `291df87da1c9937c5db64e93407b244d92f48445143f037206762453e6a29747`.\
The environment was Codex CLI `0.162.0-alpha.17.2`, `gpt-6-luna`, `max` reasoning, and a read-only sandbox.\
Each of the two selected cases had its own matched plan with `candidate` and `without-skill`: four model calls completed, with one observation per case and condition.\
Before each call, the Runner verified the fixture Skill catalog; plugins and personal same-name Skills were disabled for that invocation.\
The initial sandboxed attempt stopped at catalog preflight without a model response; the successful executions used the authorized host execution path while retaining the executor's read-only sandbox.

| Case | Candidate | Without Skill |
| --- | --- | --- |
| `ja-tech-premise` | All 3 assertions pass | All 3 assertions pass |
| `en-revise-evidence` | All 3 assertions pass | All 3 assertions pass |

The invoking agent graded the four actual responses: all 12 assertion results passed.\
Both conditions connected the main-store update to regional copies and synchronization while retaining the unknown destination; both revisions preserved the observed averages, rejected the unsupported causal conclusion, and kept rollout pending.\
The candidate additionally made successful synchronization an explicit condition in the technical explanation, but this difference did not establish an assertion-level advantage.\
No assertion-level improvement or regression relative to no Skill was observed.\
Passing these cases confirms only the selected behavior in this environment; it does not demonstrate general effectiveness or reader comprehension.

`report.json` aggregates the two separately planned comparisons after each source run and its grades were validated through the Runner's `report` command.\
Their candidate manifests, evaluation-input hashes, base commit, environment, and static-check results matched before aggregation.\
The report contains four graded results and omits raw prompts, responses, traces, and temporary paths.\
The repository checker, 155 unit tests, and diff whitespace check passed; these deterministic checks establish record consistency, not explanation quality.

## Unverified scope and stopping condition

The `en-policy-conditions`, `ja-revise-disclosure`, and `ja-history-multiple-factors` cases were not executed.\
Disclosure boundaries, implicit routing, repeatability, reader comprehension, other models and clients, and live source verification remain unconfirmed.\
Execution stopped because the two selected review concerns were answered by completed, graded matched comparisons.\
Run further selected cases when accepting another responsibility or boundary requires evidence; repeat only when an observed ambiguity or instability makes another observation useful.\
Issue #81's broader completion criteria are not established by these two comparisons.
