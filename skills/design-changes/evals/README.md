# design-changes evals

## Purpose

Verify that `design-changes` produces a decision-complete, read-only implementation handoff without forcing a fixed report template, inventing unresolved requirements, treating planned checks as observed evidence, or absorbing request clarification, Skill design, implementation, or high-risk execution-readiness assessment.

## Assets

- `evals.json`: executable behavior cases for reviewer context, minimum sufficient design, cause correction, recovery, and compatibility
- `triggers.json`: executable core, near-miss, and high-risk coexistence selection cases
- [`results.json`](results.json): immutable, hash-bound behavior and trigger evidence across recorded revisions
- this README: static contract, behavioral coverage, and execution record

## Static check

- [x] `description` contains the complete trigger and material negative boundaries.
- [x] The body follows a judgment-oriented semantic contract without requiring identical headings in other Skills.
- [x] Change targets, non-targets, dependencies, risks, verification, proceed conditions, and stop conditions remain required information.
- [x] Alternatives, module maps, rollback, and user explanation points are conditional rather than empty mandatory sections.
- [x] Readability changes preserve processing-stage and reader-understanding granularity.
- [x] Planned checks are separated from observed evidence.
- [x] Verification depth follows material risk and uncertainty rather than a universal count.
- [x] The workflow remains read-only and routes additional high-risk execution-readiness controls to `assess-risky-change-readiness`.
- [x] Consequential work with an unsettled problem frame or solution set routes to `explore-decision-space` before implementation design.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Decision-complete handoff | Omits targets, non-targets, risks, or go/stop conditions because no fixed template is present | A | Requirements 1–4 |
| Proportional verification | Adds redundant tests or fails to map a changed behavior to evidence | A | Requirement 4 |
| Dependency and authority boundary | Treats a dependency addition as an implementation detail and continues | B | Requirements 1–4 |
| High-risk coexistence | Treats ordinary design as execution authorization or a complete readiness assessment | C and `triggers.json` | Requirements 1–4 |
| Adaptive reporting | Emits empty alternatives, migration, rollback, or explanation sections | A–C | Output inspection |
| Read-only design | Edits target files or starts implementation | A–C in writable disposable fixtures | File hashes and Requirement 3 |
| Routing boundary | Collides with request clarification, Skill design, or implementation | `triggers.json` | Observable Skill loads |
| Decision-space boundary | Plans implementation before a consequential problem frame or option set is ready | `unsettled-decision-space` | Observable Skill loads |
| Retired implementation-scoping handoff | A former `scope-implementation` request has no successor or routes directly to editing | `implementation-scope-handoff` | Observable Skill loads |
| Proportional local correction | Adds speculative abstraction to a defect whose cause and affected behavior are local | D | Requirements 1–4 |
| Coherent structural correction | Minimizes the diff while leaving a confirmed shared cause or known path unresolved | E | Requirements 1–5 |
| Semantic reuse boundary | Consolidates code from syntax alone or preserves independent implementations of one current invariant | F and `shared-current-invariant` in `evals.json` | Requirements 1–4 and assigned assertions |
| Planned reviewer context | Omits criticality, exposure, trade-offs, recovery, or review focus, or turns unknown context into a low-risk claim | `reviewer-context-with-unknown-criticality` in `evals.json` | Assigned assertions |
| Cause correction and recovery | A fallback conceals a confirmed cause, or recovery lacks a failure signal and expected state | `confirmed-cause-versus-fallback` in `evals.json` | Assigned assertions |
| Current compatibility | Removes a path still used by clients, queued data, or rollback, or retains an obsolete path indefinitely | `current-versus-obsolete-compatibility` in `evals.json` | Assigned assertions |

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

1. [critical] Surface dependency selection and authority as stop conditions
2. Compare a no-new-dependency alternative when it could change the decision
3. Do not add the dependency or begin implementation
4. Separate proposed validation from observed evidence
5. Pair dependency and compatibility risks with controls and checks

### Scenario C: Authentication-related change

A change touches authentication and authorization behavior. Ordinary change design is needed, but additional safety, evidence, recovery, residual-risk, and authorization-readiness controls are not yet established.

Requirements checklist:

1. [critical] Identify the auth boundary and route the additional execution-readiness assessment to `assess-risky-change-readiness`
2. Do not present the design as authorization to implement
3. Define targeted verification for authorization regressions and failure handling
4. Keep the complete diagnosis and impact scope even if rollout will be staged
5. Do not require an arbitrary number of alternatives, tests, or runs

### Scenario D: Local defect without a structural cause

A parsing defect is confined to one function and one current behavior. No sibling
path, shared invariant, accepted near-term variant, or new dependency is involved.

Requirements checklist:

1. [critical] Select a local correction that fully covers the confirmed cause and current behavior
2. Do not add an interface, registry, configuration surface, compatibility path, or unrelated refactoring
3. State why the local boundary is sufficient and what remains unchanged
4. Map the defect and its regression boundary to focused verification

### Scenario E: Confirmed shared invariant requires a structural correction

Two known request paths implement the same current email-normalization invariant
inconsistently. The accepted outcome is consistent behavior across both paths, and
the repository already has an appropriate shared ownership boundary.

Requirements checklist:

1. [critical] Derive the coherent change boundary from both known paths and the shared invariant
2. Reject a one-handler patch because it would leave the confirmed cause and inconsistent path unresolved
3. Use the existing shared boundary without inventing a plugin system or speculative future formats
4. Explain why the local alternative is insufficient and what remains unchanged
5. Map both paths and the shared behavior to verification without unrelated scope expansion

### Scenario F: Similar code implements separate contracts

A request parser and audit formatter contain the same string operations, but one
implements a public protocol-token contract and the other produces display-only
labels. No shared domain rule, invariant, consumer contract, or expected joint
evolution is established.

Requirements checklist:

1. [critical] Do not infer a shared responsibility or abstraction from source-code similarity alone
2. Keep both current contracts independently changeable
3. Prefer the small local duplication to a generic helper that solves no current problem
4. Preserve focused verification for both contracts

## Execution protocol

1. Select only cases that can expose the changed responsibility or a material adjacent boundary, and choose the evaluation path in [`docs/evaluation.md`](../../../docs/evaluation.md).
2. Generate a Runner plan and inspect its model-call count before execution.
3. Keep expected conclusions and assertions out of executor input, and run each selected case in the Runner's disposable fixture.
4. When comparison is decision-relevant, use matched inputs and conditions with an explicit baseline commit; the historical commits below are for reproducing the recorded runs, not defaults for new audits.
5. Grade observable requirements against the actual output and trace, and keep raw responses, JSONL, and fixtures outside the repository.
6. Record the selected path, conditions, environment, candidate revision, result, stopping reason, and unverified boundaries.
7. Repeat only when an unexpected result, instability, client difference, or failure impact could change the decision.

## Failure Pattern Ledger

- `target and non-target blurred`
- `risk listed without mitigation or verification`
- `fixed output template produces empty sections`
- `conditional alternative turned into a mandatory count`
- `planned validation reported as observed evidence`
- `dependency or auth stop condition treated as implementation detail`
- `design-changes absorbs request clarification, Skill design, implementation, or high-risk readiness assessment`
- `retired implementation-scoping request does not route to design-changes`
- `readability plan split by local diff instead of reader understanding`
- `local defect expanded into speculative architecture`
- `smallest diff leaves confirmed shared cause unresolved`
- `source similarity mistaken for shared knowledge or responsibility`
- `planned reviewer context omitted from implementation handoff`
- `unknown criticality inferred as low risk`

## Recorded full evaluation — 2026-07-30

- Client: Codex CLI 0.146.0
- Model / reasoning: `gpt-5.6-sol` / high
- Targeted baseline: commit `44e0818890160f719904c5cd7cd38b323f828a03`
- Candidate `SKILL.md`: `sha256:7372f5a58bf4495d768901890a0fa32eb9468624a3d4dfd18bf779920989d48e`
- Candidate `triggers.json`: `sha256:40e8dde5ec674baedb8c8689f25e7be0619f022aa1706f78a363cc1565d66e77`
- High-risk redesign behavior: the pre-rename current and candidate both passed all 4 assigned assertions
- Rename behavior: the candidate passed all 4 assertions, preserved the read-only boundary, completed ordinary auth design, and handed additional execution-readiness controls to `assess-risky-change-readiness`
- Rename routing: the candidate observably loaded `design-changes` and `assess-risky-change-readiness`
- Prior evidence reuse: small-feature, dependency, adaptive reporting, clarification, retired-Skill, and decision-space cases were not rerun because the corresponding responsibilities and inputs are unchanged
- Regressions: none in the affected behavior and routing
- Durable evidence: [`results.json`](results.json)
- Claude Code, other clients, real application entry points, dependency constraints, auth boundaries, test commands, and production recovery procedures were not executed or remain unverified
- Next validation question: Does the adaptive reporting contract remain decision-complete on a real codebase where entry points and verification commands can be inspected?

## Coherent-change revision — 2026-08-04

- Compared committed `HEAD` and the final working-tree candidate on Scenarios D and E with Codex CLI 0.146.0, `gpt-5.6-sol`, and high reasoning. Separate blind graders evaluated each matched pair.
- Scenario D: baseline and final candidate passed 4/4 requirements and made no fixture changes. An earlier candidate unnecessarily added a no-argument `parse_port()` call form; the final candidate preserved the existing signature and treated the omitted value through the existing input contract.
- Scenario E: baseline and final candidate passed 5/5 requirements and made no fixture changes. Both selected the shared owner and both known paths, rejected a one-handler patch, excluded speculative architecture, and planned verification for both paths.
- The final candidate passed both the proportional local-correction and coherent structural-correction boundaries. It did not establish a requirement-level advantage over the already-passing final matched baseline.
- Scenario C and trigger routing were not rerun because their instructions and descriptions are unchanged.
- Next validation question: Does the explicit boundary classification hold when the shared cause must be discovered from a real repository rather than supplied in the case input?

## Reviewer-context revision — 2026-08-14

- Added a producer case for carrying planned reviewer context, preserving unsupported criticality as `Unknown`, and omitting irrelevant fields rather than inventing them.
- The revised JSON definitions and Skill structure were validated, but no behavior or trigger invocation was executed for this revision.
- The earlier pass totals are historical evidence and are superseded for the changed implementation-handoff contract.

## Minimum-sufficient-design revision — 2026-08-22

- Affected responsibility: distinguish incidental code similarity from one shared current responsibility while preserving the existing coherent structural-correction behavior.
- Selected path: matched baseline and candidate checks for `incidental-code-similarity` and `shared-current-invariant`, because this revision changes a subjective quality contract. Unrelated routing and reviewer-context cases are not selected.
- Codex CLI 0.147.0 with `gpt-5.6-luna`, max reasoning, and a read-only sandbox ran one matched baseline and candidate execution per selected case. Direct maintainer grading passed 3/3 assigned assertions in all four conditions.
- Both conditions rejected a generic helper for incidental similarity and selected the existing owner for the shared email invariant. The candidate preserved both sides of the boundary without a requirement-level advantage over the already-passing baseline.
- Initial `--ignore-user-config` attempts returned `401 Unauthorized` before model execution because that option removed the active ChatGPT authentication route; those defective attempts are excluded from pass evidence and do not indicate that the user was logged out.
- Deterministic JSON parsing, repository validation, candidate hash checks, invocation details, case evidence, and excluded defective runs are recorded in [`results.json`](results.json).
- Untested boundary: unrelated cases, repeated runs, a separate LLM grader, real application repositories, other models, and other clients remain unverified.

## Issue #60 audit — 2026-09-28

- Audit basis: #49 `監査基準 v2`, #37 acceptance criteria, and commit `ee8a5bba221859ee453fc74526008cd161ee1e02` with a clean starting worktree.
- The current `SKILL.md` hash is `sha256:b25c647ff6db354148b671ea70d1dbf13e1acbb664f28540491fba956add81dc`, which matches the candidate recorded in the minimum-sufficient-design evidence.
- The existing three behavior cases and nine routing cases were migrated together from the legacy format to the executable `{skill_name, evals}` format; `results.json` remains historical evidence.
- Two behavior cases were added to examine #37's cause/recovery and compatibility boundaries, which the prior case set did not directly expose.
- `confirmed-cause-versus-fallback` completed with Codex CLI 0.155.1, `gpt-6-luna`, max reasoning, and a read-only sandbox; direct review passed all three assertions because the output corrected the stale mapping, rejected the invalid placeholder, and conditioned rerun on the observed no-partial-write state and result checks.
- `current-versus-obsolete-compatibility` completed with Codex CLI 0.155.1, `gpt-6-luna`, medium reasoning, and a read-only sandbox; the three assertions passed, with the compact evidence in the [report at commit `55f496f`](https://github.com/mtk177a/skills/blob/55f496ffb2fb550290ea7bab988a84560936392c/skills/design-changes/evals/report.json).
- An earlier four-condition attempt reached the Codex API without the required authentication setting and returned 401 before producing model output; it is excluded from behavior evidence.
- An earlier compatibility attempt timed out after reading the Skill and searching an empty fixture; the revised case explicitly supplies the complete contract context, and the timed-out attempt is excluded from pass evidence.
- Static inspection and these two selected behavior observations support leaving `SKILL.md` unchanged; no routing case was rerun because its description and adjacent selection boundaries did not change.
- The initial v2 audit compared the English Skill and Japanese reference for material meaning but incorrectly treated an unchanged English source as sufficient reason to leave the Japanese wording unchanged. The v3 review below supersedes that translation decision.
- Real application repositories, other clients and models, repeated runs, and unselected behavior or routing cases remain unverified.

## Issue #60 Japanese reference re-review — 2026-09-28

- Audit basis: #49 `監査基準 v3` and the `write-natural-japanese` Skill with its complete wording reference.
- The English `SKILL.md` remains unchanged. The Japanese reference was read in full and rewritten to replace unnecessary English general terms and source-language sentence structure while preserving the original scope, conditions, certainty, identifiers, and Markdown structure.
- The current `report.json` records a static-only check of the revised Japanese reference with zero model calls. The earlier model results concern the unchanged English Skill and remain available in the prior report linked above.
- The translation was checked against every English section and all 13 workflow steps. Model behavior with the revised Japanese reference was not evaluated.
