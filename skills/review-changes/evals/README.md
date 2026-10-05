# review-changes evals

## Purpose

Verify that `review-changes` selects a new or updated effective diff, inspects the surrounding evidence needed to judge it, adapts to code, documentation, and configuration changes, and reports findings with separate labels, impact, and confidence. It must distinguish executed checks from suggested verification, handle full re-review state, and report no-findings or unavailable-diff states without inventing evidence.

Structured assets:

- `triggers.json`: executable routing cases for review, near-miss, and coexistence requests
- `evals.json`: executable behavior cases, fixtures, and grading assertions
- `results.json`: historical evidence from earlier evaluation revisions

## Candidate static check

- `description` includes code, documentation, configuration, effective-diff, and full re-review triggers and excludes triage, specific-fix validation, comment drafting, summarization, and implementation
- effective diff and material exclusions are established before findings
- surrounding contracts, callers, tests, and repository precedent are read only when they can test a change assumption
- code, documentation, and configuration use applicable risk dimensions rather than one mandatory checklist
- every material finding separates canonical label, confidence, evidence, impact, verification, and an explicit `Unconfirmed premises` field
- a high-impact unconfirmed premise remains visible as a `question` and can be handed to triage without downstream inference
- executed checks, suggested verification, unchecked scope, and residual risk are not conflated
- no-findings and unavailable-diff states are distinct
- full re-review state and new-finding origin are separate from label and confidence
- reviewer context and remediation cost calibrate requested response without a numeric score
- the Skill remains read-only, portable, and usable without a companion Skill or subagent

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Effective diff | Reviews the wrong range or mixes unrelated working-tree changes | `explicit-range`, `missing-diff` | Scope statement and file evidence |
| Contextual evidence | Reviews only the changed line and misses a contract or cardinality violation | `external-contract-and-cardinality` | Assigned assertions |
| Uncertainty and handoff | Turns a potentially severe unknown into a low-value question, hides the premise in another field, or forces downstream triage to infer it | `high-impact-unconfirmed-premise` | Finding fields and handoff assertion |
| Change-type adaptation | Forces code tests onto docs/config or omits available deterministic checks | `documentation-and-configuration` | Commands and results |
| No-findings state | Invents nits or returns a bare approval | `clean-diff` | Finding count and report contract |
| Finding-free drafting handoff | Invents finding decisions or omits the review-level conclusion, scope, checks, or limitations needed for a general comment | `finding-free-draft-handoff` | Handoff fields and drafting boundary |
| Full re-review | Mixes `Resolved` / `Remaining` / `New` with label or confidence, or repeats classifications supplied by the prompt instead of deriving them from the target | `full-rereview` | Fixture-derived state reconciliation and new-finding discovery |
| Trigger boundary | Collides with triage, validation, comment drafting, summary, implementation, or guidance audit | `triggers.json` | Observable Skill loads |
| Excess complexity | Accepts speculative abstractions whose concrete maintenance cost has no current requirement or observed-risk basis | `unjustified-abstraction` | Finding evidence and assigned assertions |
| Overly narrow correction | Accepts a small patch that leaves a confirmed shared rule inconsistent across a known path | `local-patch-leaves-shared-cause` | Finding evidence and assigned assertions |
| Incidental duplication | Accepts a generic helper that couples separate contracts solely to remove similar lines | `incidental-duplication-abstraction` | Finding evidence and assigned assertions |
| Justified shared structure | Reports a preference-only finding against the existing owner of one current invariant | `justified-shared-invariant` | Finding count and assigned assertions |
| Proportionate response | A speculative low-exposure edge case becomes a blocking request despite cheap detection and recovery and high remediation cost | `low-criticality-expensive-edge-case` | Risk-context fields and requested label |
| Re-review convergence | New origins are conflated or a previously observable non-blocking nit starts another fix round | `full-rereview-origin-and-convergence` | Origin classification and actionable-output inspection |
| Confirmed cause and recovery | A catch-and-continue fallback hides a known parser failure and returns an indistinguishable empty report | `fallback-masks-confirmed-cause` | Cause, contract, detection, and recovery evidence |
| Necessary recovery | A reviewer demands removal of a tested timeout recovery path because its cause remains unknown | `verified-timeout-recovery` | Current failure condition, bounded trigger, recovered state, observable signal, tests, and finding count |
| Current compatibility | An unpublished feature is assumed to have no obligations despite persisted records and a documented rollback | `unreleased-persisted-compatibility` | Existing reader and rollback path evidence |

## Execution protocol

1. Select cases that can expose the responsibility changed by the candidate. Use `scripts/run_skill_evaluation.py plan` to inspect the model-call count before execution.
2. Give the executor only each case's `prompt` and disposable fixture. Keep titles, assertions, and expected conclusions hidden.
3. Use the planned client, model, reasoning effort, and sandbox for every selected condition. Add a baseline only when comparison can change the decision.
4. Materialize `baseline_files` and `fixture.files` in a temporary repository outside this source repository when a case needs a local diff.
5. Count a Skill trigger only from an observable `SKILL.md` read in a complete trace.
6. Grade objective scope and command claims from the fixture and captured output, then grade judgment-heavy findings by direct review. Add an independent grader only when it is decision-relevant.
7. Stop after the selected requirements answer the acceptance question. Repeat only when an unexpected result, instability, client difference, or failure consequence could change the decision.

Keep raw JSONL and full responses in a temporary directory.

Claude Code and other clients are outside the current execution plan and must be recorded as `not executed`.

## Failure pattern ledger

- `wrong diff or base reviewed`
- `diff-only inspection misses surrounding contract`
- `question loses high potential impact`
- `unconfirmed premise omitted or hidden in another finding field`
- `confidence collapsed into canonical label`
- `suggested check reported as executed`
- `code test forced onto static documentation or configuration`
- `clean diff padded with nits or notes`
- `unavailable diff reported as no issues`
- `re-review state mixed with label or copied from an answer-bearing prompt`
- `review workflow routed to an adjacent Skill`
- `speculative abstraction accepted without concrete cost or requirement evidence`
- `small diff accepted while a confirmed shared cause remains`
- `source similarity treated as sufficient abstraction evidence`
- `justified shared owner criticized because local duplication is shorter`
- `missing context treated as low risk`
- `speculative remediation cost ignored when assigning must`
- `late non-blocking issue starts another fix round`
- `verified recovery criticized solely because its root cause remains unknown`
- `finding-free review blocked on invented finding decisions`

## Recorded full evaluation — 2026-07-27

On 2026-07-27, Codex CLI 0.145.0 with `gpt-5.6-sol` and high reasoning produced:

- baseline: 21/29 behavior requirements passed, 2 were partial, and 6 failed; 2/7 cases passed
- candidate: 29/29 behavior requirements and 7/7 cases passed
- trigger selection: 10/10 cases passed for both baseline and candidate

The baseline omitted the dedicated `Unconfirmed premises` field and, in two cases, other reporting details. The candidate preserved the gateway premise in that field, derived F1 as `Resolved`, F2 as `Remaining`, and the unbounded retry as `New` from the disposable repository rather than an answer-bearing prompt, and passed the retained cases. Every invocation used an isolated `HOME` so globally installed personal Skills were unavailable.

Claude Code and other clients were not executed. Detailed case-by-assertion and observable trigger evidence is in `results.json`; raw traces are intentionally not retained in the repository.

## Coherent-change revision — 2026-08-04

- Compared committed `HEAD` and the final working-tree candidate on `unjustified-abstraction` and `local-patch-leaves-shared-cause` with Codex CLI 0.146.0, `gpt-5.6-sol`, and high reasoning. Separate blind graders evaluated each matched pair.
- `unjustified-abstraction`: the final candidate passed 5/5 requirements; the baseline failed `finding-contract`. The candidate tied the concrete added concepts to maintenance and diagnostic paths, recorded unavailable fallback behavior as a premise, and did not claim unsupported runtime failure.
- `local-patch-leaves-shared-cause`: the final candidate passed 5/5 requirements; the baseline was partial on `finding-contract`. The candidate identified the known inconsistent path and shared owner while limiting Impact to the supplied specification violation and two-path inconsistency.
- Earlier candidate runs exposed two useful failures: `none identified` conflicted with an unchecked fallback, and speculative downstream account-matching effects exceeded the supplied evidence. The final candidate requires premise-consistent, evidence-bound Impact claims.
- Retained review cases and trigger routing were not rerun because their responsibilities and descriptions are unchanged.
- Next validation question: Does the same distinction hold on a real diff where callers, fallback behavior, and downstream contracts can be inspected directly?

## Proportional-review revision — 2026-08-14

- Added coverage for proportional blocking decisions, conditional high-criticality risk, re-review origin, incomplete coverage, and routing ordinary post-fix checks to `validate-fix`.
- A matched forward test on a low-criticality, low-exposure, expensive edge case produced no material finding in either condition. The candidate additionally made the proportionality basis and cheaper verification alternative explicit.
- A matched routing test selected `validate-fix` in both conditions for an ordinary post-fix request; the candidate made the responsibility boundary explicit.
- The earlier pass totals are historical evidence and are superseded for the changed trigger and output contract. The full behavior and trigger suites were not rerun for this revision.

## Actionable-draft boundary clarification — 2026-08-14

- Clarified that review output alone does not authorize an actionable draft; assessment, state, and response decision must be supplied first, normally by `triage-review-feedback`.
- A matched routing check selected `triage-review-feedback`, not `draft-review-comments`, for review output without those decisions in both conditions.
- Review behavior cases were not rerun because finding discovery and output fields were unchanged.

## Minimum-sufficient-review revision — 2026-08-22

- Affected responsibility: distinguish unsupported coupling from consolidation justified by one current shared responsibility, invariant, or contract.
- Selected path: matched baseline and candidate checks for `incidental-duplication-abstraction` and `justified-shared-invariant`, because this revision changes a subjective quality contract. Existing unrelated review and routing cases are not selected.
- Codex CLI 0.147.0 with `gpt-5.6-luna`, max reasoning, and a read-only sandbox ran one matched baseline and candidate execution per selected case. Direct maintainer grading passed 5/5 assertions for incidental duplication and 6/6 for justified shared structure in both conditions.
- Both conditions reported the concrete maintenance coupling introduced by a generic helper across separate contracts and reported no material finding against consolidation into the existing owner of one current invariant. The candidate preserved both sides of the boundary without a requirement-level advantage over the already-passing baseline.
- Initial authentication failures and a review batch with an incomplete inline fixture were excluded before grading. The accepted batch used complete public fixtures and separate disposable roots; no independent LLM grader or repetition was decision-relevant.
- Deterministic JSON parsing, repository validation, candidate hash checks, invocation details, case evidence, and excluded defective runs are recorded in [`results.json`](results.json).
- Untested boundary: unrelated cases, repeated runs, a separate LLM grader, real repository diffs, other models, and other clients remain unverified.

## Issue #71 audit — 2026-10-04

- Migrated all 13 existing behavior cases and all 11 routing cases to the executable format. The legacy `results.json` remains historical evidence.
- Added `fallback-masks-confirmed-cause` and `unreleased-persisted-compatibility` for the responsibilities changed under #37.\
  The candidate passed all 10 selected critical requirements across those two cases with Codex CLI 0.155.1, `gpt-6-luna`, max reasoning, and a read-only sandbox; the compact, candidate-bound record remains in Git history at `d164bc2`.
- An initial model run without a materialized diff correctly reported that review could not run. After adding the diff fixtures, a forward run exposed that one response did not keep `Unconfirmed premises` distinct; the final candidate added that reporting requirement, and both selected cases then passed. These intermediate runs are diagnostic, not accepted candidate evidence.
- The migrated `explicit-range` case now checks an explicitly scoped file diff against an unrelated untracked file. The current executable fixture contract does not construct a second committed revision, so the original `HEAD~1..HEAD` selection remains untested by this case.
- Other behavior and routing cases, real repository diffs, repeatability, other models and clients, and live production behavior were not evaluated for this revision.

## Issue #71 review feedback — 2026-10-04

- Added `verified-timeout-recovery` to check the other side of the #37 recovery boundary: a currently required, tested fallback must not be criticized solely because the timeout's root cause remains unknown.
- The new fixture defines the observed timeout, a verified snapshot no older than five minutes, the recovery signal and returned state, and visible failure when recovery is unavailable. Its three focused unit tests passed outside the model run.
- One targeted candidate execution with Codex CLI 0.155.1, `gpt-6-luna`, max reasoning, and a read-only sandbox passed all five critical requirements.\
  The response reported no material finding, read the contract and tests, and separated executed checks from unrun tests and provider integration.\
  Its compact record remains in Git history at `8069cb4`.
- The earlier two-case, ten-requirement audit result remains recorded in the Issue #71 audit above and in Git history; `report.json` records only the latest selected evaluation. `SKILL.md` and `SKILL-ja.md` did not change, so their meaning and translation alignment are unchanged.
- The first attempt stopped before model execution because the local CLI could not inspect its Skill catalog. A second reached the model endpoint without credentials and failed. Explicitly using the configured `auto` credential store produced the accepted execution. Neither failed attempt counts as behavior evidence.
- Unselected cases, real repository diffs, repeated runs, other models and clients, snapshot-provider integration, and production behavior remain unverified.

## Finding-free drafting handoff — 2026-10-05

- The retained raw response and run record for `verified-timeout-recovery` were checked against the `8069cb4` Skill file hashes and evaluation input.\
  The response did not demand removal of the verified recovery path or a speculative cause fix; it separated an executed whitespace check from tests read but not run.
- Added `finding-free-draft-handoff` to test the requested review-level handoff without inventing finding decisions or drafting or posting a comment.\
  One targeted candidate execution with Codex CLI 0.155.1, `gpt-6-luna`, max reasoning, and a read-only sandbox passed all five critical requirements.\
  The latest compact result is in [`report.json`](report.json).
- The response named `draft-review-comments`, reported no material finding, and supplied the conclusion, reviewed README scope, checks actually performed, and material limitations.\
  It did not triage, draft, post, or choose a review action.
- End-to-end drafting with the separate PR #109 candidate, actual GitHub posting, unselected cases, repeated runs, other models and clients, and production behavior remain unverified.
