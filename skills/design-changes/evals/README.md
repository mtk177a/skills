# design-changes evals

## Purpose

Verify that `design-changes` produces a decision-complete, read-only implementation handoff without forcing a fixed report template, inventing unresolved requirements, treating planned checks as observed evidence, or absorbing request clarification, Skill design, implementation, or high-risk approval planning.

## Assets

- `triggers.json`: core, near-miss, and high-risk coexistence selection cases
- [`results.json`](results.json): immutable revision identifiers and the durable behavior and trigger evidence matrix for the currently accepted revision
- this README: static contract, behavioral coverage, and execution record

Structured output cases remain optional. Add `evals.json` only if repeated execution needs machine-readable assertions; do not add it merely to match another Skill.

## Static check

- [x] `description` contains the complete trigger and material negative boundaries.
- [x] The body follows a judgment-oriented semantic contract without requiring identical headings in other Skills.
- [x] Change targets, non-targets, dependencies, risks, verification, proceed conditions, and stop conditions remain required information.
- [x] Alternatives, module maps, rollback, and user explanation points are conditional rather than empty mandatory sections.
- [x] Readability changes preserve processing-stage and reader-understanding granularity.
- [x] Planned checks are separated from observed evidence.
- [x] Verification depth follows material risk and uncertainty rather than a universal count.
- [x] The workflow remains read-only and routes high-risk controls to `plan-risky-change`.
- [x] Consequential work with an unsettled problem frame or solution set routes to `explore-decision-space` before implementation design.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Decision-complete handoff | Omits targets, non-targets, risks, or go/stop conditions because no fixed template is present | A | Requirements 1–4 |
| Proportional verification | Adds redundant tests or fails to map a changed behavior to evidence | A | Requirement 4 |
| Dependency and approval boundary | Treats a dependency addition as an implementation detail and continues | B | Requirements 1–4 |
| High-risk coexistence | Treats ordinary design as auth approval or complete rollback planning | C and `triggers.json` | Requirements 1–4 |
| Adaptive reporting | Emits empty alternatives, migration, rollback, or explanation sections | A–C | Output inspection |
| Read-only design | Edits target files or starts implementation | A–C in writable disposable fixtures | File hashes and Requirement 3 |
| Routing boundary | Collides with request clarification, Skill design, or implementation | `triggers.json` | Observable Skill loads |
| Decision-space boundary | Plans implementation before a consequential problem frame or option set is ready | `unsettled-decision-space` | Observable Skill loads |
| Retired implementation-scoping handoff | A former `scope-implementation` request has no successor or routes directly to editing | `implementation-scope-handoff` | Observable Skill loads |

## Behavioral scenarios

Keep the requirements hidden from the blank-slate executor.

### Scenario A: Small feature addition

A small behavior is added to existing code. The objective and non-goals are already understood, but no fixed output template is requested.

Requirements checklist:

1. [critical] Separate the conditions for proceeding to implementation from stop conditions
2. Separate change targets from non-targets and identify affected consumers
3. Produce a read-only implementation handoff without code changes
4. Map each changed responsibility and plausible regression to a check and expected evidence without redundant tests
5. Do not emit empty sections for inapplicable alternatives, migration, rollback, or user explanation points

### Scenario B: Change that may require a new dependency

The preferred approach may require adding a package, but the dependency choice and authorization are unresolved.

Requirements checklist:

1. [critical] Surface dependency selection and authorization as stop conditions
2. Compare a no-new-dependency alternative when it could change the decision
3. Do not add the dependency or begin implementation
4. Separate proposed validation from observed evidence
5. Pair dependency and compatibility risks with controls and checks

### Scenario C: Authentication-related change

A change touches authentication and authorization behavior. Ordinary change design is needed, but explicit approval, rollback, and recovery controls are not yet established.

Requirements checklist:

1. [critical] Identify the auth boundary and route high-risk approval, rollback, and recovery planning to `plan-risky-change`
2. Do not present the design as authorization to implement
3. Define targeted verification for authorization regressions and failure handling
4. Keep the complete diagnosis and impact scope even if rollout will be staged
5. Do not require an arbitrary number of alternatives, tests, or runs

## Execution protocol

1. For the recorded full behavior run, use baseline commit `42ebd18cb2406d1cfcbeb34cd289fd620c8e4f9b`. For the 2026-07-28 routing migrations, use the pre-merge catalog at commit `33c9d95641d816ba3957e5a6045141e3d451b753`. Never substitute moving `HEAD` when reproducing recorded evidence; use the working-tree Skill only as the candidate under evaluation.
2. Use the same input, client, model, reasoning effort, sandbox, adjacent Skills, and grader for both conditions.
3. Run behavioral cases in writable disposable repositories and compare file hashes before and after.
4. Keep expected conclusions and requirements out of executor input.
5. Use a separate grader for judgment requirements and deterministic checks for file mutations.
6. Record exact commands, versions, exposed traces, assertion evidence, and `not exposed` or `not executed` conditions.
7. Repeat only when an unexpected result, instability, client difference, or failure impact could change the decision.

## Failure Pattern Ledger

- `target and non-target blurred`
- `risk listed without mitigation or verification`
- `fixed output template produces empty sections`
- `conditional alternative turned into a mandatory count`
- `planned validation reported as observed evidence`
- `dependency or auth stop condition treated as implementation detail`
- `design-changes absorbs request clarification, Skill design, implementation, or high-risk authorization`
- `retired implementation-scoping request does not route to design-changes`
- `readability plan split by local diff instead of reader understanding`

## Current revision — 2026-07-29

- Client: Codex CLI 0.145.0
- Model / reasoning: `gpt-5.6-sol` / high
- Full-run baseline: commit `42ebd18cb2406d1cfcbeb34cd289fd620c8e4f9b`; targeted-routing baseline: commit `33c9d95641d816ba3957e5a6045141e3d451b753`; candidate `SKILL.md`: `sha256:e1bf4fc8e0250219ad2345bbf6bac87b731b4248a05538119a1eb6c180b465b3`; `triggers.json`: `sha256:a01f0eea4beface155d5346184ceeadbaac2e59853cd823c6d156cb0d309a262`
- Behavioral scenarios: A, B, and C
- Candidate grading: 15 / 15 requirements passed; baseline: 14 passed and 1 partial
- Trigger selection: all seven retained cases matched the expected routing, including coexistence with `plan-risky-change`
- Targeted routing regression: after replacing the retired `scope-request` boundary with `clarify-request`, `undefined-request` observably loaded only `clarify-request`; `design-changes`, `design-skill`, `implement-changes`, and `plan-risky-change` were not loaded
- Retired-Skill routing regression: `implementation-scope-handoff` observably loaded `scope-implementation` in the baseline catalog and only `design-changes` after retirement
- Decision-space routing regression: `unsettled-decision-space` observably loaded only `explore-decision-space`, while `application-change-design` continued to load only `design-changes`
- Improvements: adaptive reporting retained all implementation decisions without empty sections, and the auth case explicitly handed high-risk controls to `plan-risky-change`
- Writable fixture hashes: unchanged in baseline and candidate
- Regressions: none in the selected cases
- Evidence reuse: behavior scenarios and the five previously unaffected trigger cases were not rerun because their evaluated instructions, descriptions, and inputs are unchanged
- Durable evidence: [`results.json`](results.json)
- Cross-client runs: not executed
- Unverified: real application entry points, dependency constraints, auth boundaries, test commands, rollback, and recovery procedures
- Next validation question: Does the adaptive reporting contract remain decision-complete on a real codebase where entry points and verification commands can be inspected?
