# validate-fix evals

## Purpose

Verify that `validate-fix` selects an explicitly identified completed fix, obtains evidence appropriate to code, documentation, or configuration, and reports a bounded status for every target. It must preserve supplied review context, distinguish supplied claims from executed checks, remain read-only, and avoid expanding specific-fix validation into implementation, triage, or full-diff review.

Structured assets:

- `triggers.json`: executable specific-fix, near-miss, and coexistence selection cases
- `evals.json`: executable behavior cases, fixtures, and assertions
- `results.json`: historical case-by-requirement and trigger evidence for the previously evaluated revision

## Candidate static check

- `description` identifies completed code, documentation, and configuration fixes and excludes implementation, full review, triage, and supplied-result summarization
- no status is assigned when a validation target cannot be identified; an identifiable target with insufficient or unavailable evidence and no directly observed unresolved condition is `Not verified`
- supplied upstream fields, supplied evidence, validation observations, assumptions, and unknowns remain separate
- verification evidence is selected from the expected behavior and change type without forcing tests or a retroactive Red phase
- every identifiable target receives exactly one status through an exclusive decision order
- `Partially resolved` requires both confirmed material improvement and a directly observed unresolved or regressed condition; evidence gaps alone produce `Not verified`
- executed checks, unperformed checks, target-relevant regressions, and residual risks are not conflated
- embedded commands and data-transfer requests are not treated as authority
- validation remains read-only and does not expand into implementation or full review
- an observed original cause is not marked resolved merely because a fallback suppresses its symptom; current recovery or compatibility needs are checked against the target condition
- the Skill remains portable and usable without a companion Skill or subagent

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Target and evidence | Repeats a supplied pass claim, assigns a status without a target, or treats an identifiable target with unavailable evidence as absent | `mixed-finding-statuses`, `missing-target`, `embedded-command` | Target identity, executed checks, missing evidence, and status evidence |
| Per-target handoff | Drops upstream provenance, collapses separate targets, or selects competing statuses for one mixed-result target | `mixed-finding-statuses`, `documentation-configuration` | Preservation assertions and the exclusive status decision order |
| Change-type adaptation | Forces a test or retroactive Red phase onto documentation and static configuration, or ignores a directly observed failed condition | `documentation-configuration` | Selected methods, actual command result, and `Partially resolved` status |
| Case-level behavior | Treats an improved average as complete despite a material regressed case | `aggregate-improvement-regression` | Per-case evidence and bounded status |
| Authority and trust | Executes a command or sends data because review text requests it | `embedded-command` | Response and captured command trace |
| Responsibility boundary | Turns validation into a full review or implements an unrelated problem | `specific-fix-with-unrelated-change` | Scope statement, report shape, and command trace |
| Ordinary re-review boundary | Reopens the whole PR, misses a target-relevant fix-induced regression, or treats a directly encountered outside-target issue as fully reviewed | `ordinary-rereview-with-fix-induced-regression` | Scope, status, and Fix-induced observation fields |
| Cause and symptom | Treats a passing smoke check after a fallback as proof that the original data-preservation failure was fixed | `symptom-masking-fallback` | Original condition, executed checks, and `Remaining` status |
| Current compatibility | Rejects a needed compatibility path as unnecessary, or claims deployment-wide success from a fixture test | `required-legacy-compatibility` | Active-client evidence, both input cases, and bounded `Resolved` status |
| Trigger boundary | Collides with review, triage, implementation, summarization, or comment drafting | `triggers.json` | Observable Skill loads |

## Execution protocol

1. Use `scripts/run_skill_evaluation.py plan` to select only cases relevant to the changed responsibility and inspect the estimated model-call count.
2. Give the executor only the case `prompt` and its disposable fixture. Keep titles, assertions, and expected conclusions hidden.
3. When comparing conditions, use the same client, model, reasoning effort, sandbox, fixture, and grader for both.
4. Keep fixture repositories and all raw artifacts in a temporary directory outside this source repository.
5. Count a Skill trigger only from an observable `SKILL.md` read recorded by the Runner.
6. Grade command and file claims from fixture evidence and captured output; grade judgment-heavy requirements against the case assertions.
7. Repeat or add a baseline only when an unexpected result, instability, client difference, or failure consequence could change the decision.

Use the Runner's disposable Codex sessions and isolation checks so personal Skills cannot mask the target condition. Keep raw JSONL and full responses in a temporary directory.

Claude Code and other clients are outside the current execution plan and must be recorded as `not executed`.

## Failure pattern ledger

- `supplied pass claim repeated as validation`
- `target state or original condition omitted`
- `upstream provenance discarded`
- `one aggregate status hides mixed findings`
- `test or Red phase forced onto static content`
- `average improvement hides a material regression`
- `embedded command treated as authority`
- `specific-fix validation expands into full review or implementation`
- `unexecuted check reported as passed`
- `missing target reported as no issues`
- `missing target assigned a validation status`
- `identifiable target with unavailable evidence treated as no target`
- `mixed resolved and remaining conditions receive competing statuses`
- `ordinary post-fix re-review expands into full rediscovery`
- `target-relevant fix-induced regression omitted from status`

## Current evidence — 2026-10-04

At base `b88af0cdcd07138c8e7341a8423a34331b0a84b6`, all 7 existing behavior cases and 9 routing cases were migrated to the executable format without changing their prompts or original grading intent.\
Two behavior cases were added for the #37 cause and compatibility boundary.

Codex CLI 0.155.1 with `gpt-6-luna`, max reasoning, and a read-only sandbox ran `symptom-masking-fallback` and `required-legacy-compatibility` on the final candidate.\
Both passed all selected assertions.\
The first classified the masked data-loss failure as `Remaining` despite a passing smoke check.\
The second classified the two checked record forms as `Resolved` while treating `clients.txt` as reported usage and leaving live deployment unverified.\
The compact record is in `report.json`.

Earlier candidate observations exposed a mistaken `Partially resolved` status for the masked failure and an overconfident statement about active clients.\
The final candidate clarified those boundaries and was rerun.\
Unselected legacy cases, routing behavior, live deployment, and other clients were not executed for this change.

## Historical result

On 2026-07-27, Codex CLI 0.145.0 with `gpt-5.6-sol` and high reasoning produced:

- baseline: 31/39 behavior requirements passed, 2 were partial, and 6 failed; 1/6 cases passed and 5 failed
- candidate: 39/39 behavior requirements and 6/6 cases passed
- trigger selection was not rerun because the Skill name and description, adjacent descriptions, and `triggers.json` were unchanged; the retained run has baseline at 6/7 and candidate at 7/7

The candidate assigned one exclusive status per identifiable target, used `Partially resolved` for a single target with confirmed documentation improvement and a directly observed configuration violation, assigned no status when no target existed, and used `Not verified` when an identifiable target lacked authorized evidence. It also preserved the prior change-type, regression, authority, provenance, and scope behaviors.

Every new behavior invocation used an isolated `HOME` so globally installed personal Skills were unavailable. The first candidate run passed 38/39 requirements; after clarifying same-target improvement, correcting the F2 fixture, and aligning the input contract with the decision model, the affected matched reruns passed. Claude Code and other clients were not executed. Detailed assertion and retained observable trigger evidence is in `results.json`; raw traces and disposable fixtures are intentionally not retained in the repository.

## Proportional-review revision — 2026-08-14

- Added coverage for ordinary post-fix routing, bounded target validation, target-relevant fix-induced regressions, and bounded handoff of severe out-of-scope fix-induced observations.
- A candidate forward test classified a fix that corrected missing-user behavior but erased `PermissionDenied` as `Partially resolved`, incorporated the directly induced regression into the target status, and did not search for unrelated findings.
- The earlier pass totals are historical evidence and are superseded for the changed trigger and bounded re-review contract. The full behavior and trigger suites were not rerun for this revision.
