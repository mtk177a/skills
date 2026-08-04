# design-changes evals

## Purpose

Verify that `design-changes` produces a decision-complete, read-only implementation handoff without forcing a fixed report template, inventing unresolved requirements, treating planned checks as observed evidence, or absorbing request clarification, Skill design, implementation, or high-risk execution-readiness assessment.

## Assets

- `triggers.json`: core, near-miss, and high-risk coexistence selection cases
- [`results.json`](results.json): immutable, hash-bound behavior and trigger evidence across recorded revisions
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
- `design-changes absorbs request clarification, Skill design, implementation, or high-risk readiness assessment`
- `retired implementation-scoping request does not route to design-changes`
- `readability plan split by local diff instead of reader understanding`
- `local defect expanded into speculative architecture`
- `smallest diff leaves confirmed shared cause unresolved`

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
