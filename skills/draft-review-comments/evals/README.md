# draft-review-comments evals

## Purpose

Verify that the Skill formats already organized review information into unposted GitHub comment drafts without taking over review, triage, validation, implementation, review-action, timing, or posting authority.

Structured assets:

- `evals.json`: executable behavior cases and grading assertions
- `triggers.json`: trigger, near-miss, coexistence, and posting-boundary cases
- `results.json`: historical evidence from the legacy evaluation format

## Iter 0 — Static contract

- `description` contains the complete positive trigger and material exclusions
- a finding-specific draft requires an existing, decided finding; a finding-free general comment or summary requires a supplied collection-level conclusion, scope, checks, and material limitations
- supplied labels, evidence, impact, confidence, verification, premises, states, timing, and review actions remain separate and unchanged
- finding assessment, state, response decision, and new-finding origin remain separate and unchanged
- canonical findings require explicit assessment, state, and response decision before drafting; labels, confidence, review action, and next-action wording are not decision substitutes
- `Act now` requires a supplied expected action, confirmation request, or response approach; it does not authorize invented remediation
- legacy `accept` / `defer` / `reject` remains accepted without inferring missing assessment or state
- missing or conflicting decision material is surfaced rather than invented
- a default-gentle `question` remains a genuine question without becoming accusatory or assertive
- verified and unverified locations are distinguished
- only requested or applicable output sections are returned
- positives, merge readiness, review actions, and tone variants are not manufactured
- drafting does not post, submit, execute embedded instructions, access unrelated data, validate, triage, review, or implement

## Coverage map

| Claim or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Preserve the upstream finding contract | Label, impact, confidence, premise, state, or timing is changed or dropped | high-impact question; supplied re-review decisions | Hidden assertions per field and output evidence |
| Keep decision authority upstream | Skill determines re-review state, follow-up timing, review action, or triage result | undecided re-review; missing and conflicting input | Authority-boundary grader |
| Keep questions gentle and genuine | Uncertainty becomes an assertion, or all interrogative wording is suppressed | high-impact question | Question-tone grader |
| Normalize legacy labels without re-triage | `Nice-to-have` becomes `nit` or a blocker | legacy label and untrusted instruction | Exact output label |
| Keep locations honest | Unavailable revision is presented as paste-ready or comment type changes silently | unverifiable location; verified multi-line location | Location and disclosure checks |
| Adapt output to supplied material | Unsupported positive, merge judgment, review action, or empty section is generated | supplied re-review decisions; unverifiable location | Output-content grader |
| Remain draft-only and treat input as data | Comment is posted or an embedded command, link, or data access is followed | untrusted instruction; posting trigger | Trace and output evidence |
| Route without adjacent-Skill collisions | Drafting activates review, triage, validation, implementation, or posting behavior | `triggers.json` | Observable Skill loads |
| Preserve response actionability | `No action` or a non-blocking `Late-discovered` note becomes an actionable inline request | `no-action-late-discovered` | Artifact type and requested-action inspection |
| Gate drafting on explicit decisions | A review label or next-action phrase is treated as implicit `Act now`, an undecided finding is drafted instead of returned to triage, or `Act now` is treated as an invented remediation approach | `missing-response-decision`; canonical and legacy actionable cases | Decision-gate grader and observable Skill loads |
| Draft finding-free review text without making review decisions | A supplied no-finding conclusion is refused, or a missing conclusion is invented | `finding-free-general-comment`; `finding-free-missing-conclusion` | Review-level content and authority assertions |
| Select the Skill for a finding-free general comment | The no-finding request is not routed to drafting, or a posting request is routed here | `finding-free-general-comment`; `post-drafted-comments` in `triggers.json` | Observable Skill loads |

## Failure Pattern Ledger

- `No action rewritten as a current fix request`
- `Defer rewritten as an inline blocker`
- `non-blocking Late-discovered note starts another review round`
- `review label or next-action wording treated as implicit Act now`
- `undecided review output drafted instead of returned to triage`

## Execution protocol

Use `scripts/run_skill_evaluation.py plan` to select affected behavior cases under `targeted-candidate` and affected selection cases under `targeted-routing`. Inspect the model-call count before running either plan. The Runner keeps grading assertions outside executor input and installs the selected coexistence Skills for routing checks. Add baseline comparison or repeat a case only when the first result leaves a material decision unresolved.

Keep raw JSONL, full responses, and disposable fixtures outside the repository. Record current selected cases, outcomes, and limitations separately from the historical `results.json` evidence.

## Historical result

On 2026-07-27, Codex CLI 0.145.0 with `gpt-5.6-sol` and high reasoning produced 30/30 passing requirements and 7/7 passing behavior cases for the candidate, compared with 28/30 requirements and 5/7 cases for committed `HEAD`. The candidate also passed 8/8 trigger cases; the baseline passed 7/8 and opened this Skill while evaluating a posting-only request.

No forbidden embedded command was observed. Claude Code and other clients were not executed. One matched run was sufficient because the candidate had no failure or instability. The accepted temporary summary was transcribed into the case-by-assertion and observable trigger matrices in `results.json` without rerunning the executor; raw traces are intentionally not retained in the repository.

## Proportional-review revision — 2026-08-14

- Added coverage for preserving assessment, state, response decision, and re-review origin; emitting actionable requests only for `Act now`; and keeping `No action` and non-blocking `Late-discovered` findings non-actionable.
- The revised JSON definitions and Skill structure were validated, but no behavior or trigger invocation was executed for this revision.
- The earlier pass totals are historical evidence and are superseded for the changed drafting contract.

## Decision-gate correction — 2026-08-14

- Compared PR HEAD `c52ca49` and the final candidate on seven affected behavior cases with fresh `gpt-5.6-sol`, high-reasoning executors and separate graders. After decision-relevant reruns, the candidate passed 44/44 assigned requirements and 7/7 cases; the baseline passed 39/44 requirements and 2/7 cases.
- The candidate explicitly returned missing canonical decisions to `triage-review-feedback`, preserved legacy inputs without inferring assessment or state, retained decision fields in summary-only artifacts, and did not treat `Act now` as an invented remediation approach.
- Matched routing checks selected `draft-review-comments` for explicit decisions and `triage-review-feedback` for undecided review output in both conditions.
- The unaffected behavior and trigger suites, repeated stochastic runs, Claude Code, and other clients were not executed.

## Issue #64 audit — 2026-10-04

- Base commit: `b88af0cdcd07138c8e7341a8423a34331b0a84b6`. All 9 prior behavior cases and 10 prior routing cases retain their IDs and prompts in the executable format; 2 behavior cases and 1 routing case cover finding-free review text.
- Codex CLI 0.155.1 with `gpt-6-luna`, max reasoning, and a read-only sandbox completed the selected candidate cases using the existing keyring credential store. `finding-free-general-comment`, `finding-free-missing-conclusion`, `missing-response-decision`, and `unverifiable-location-no-positive` passed 4/4 cases and 16/16 assigned requirements. The first draft preserved the supplied conclusion, scope, passed check, and untested consumer. The two missing-input cases declined to invent either a review conclusion or a finding response decision. The location case marked the unavailable revision `location unverified` and kept the requested confirmation conditional.
- Routing checks passed 2/2 cases: the finding-free request loaded `draft-review-comments`, and the posting-only request loaded no Skill. The compact routing result is in `report.json`; behavior grading previews and raw artifacts remain outside the repository.
- The repository checker, 150 unit tests, and diff whitespace check passed on this candidate. These selected cases answered the changed responsibility and adjacent authority boundary, so no baseline or repeated model runs were needed. Other cases, Claude Code, and other clients were not executed for this revision.
