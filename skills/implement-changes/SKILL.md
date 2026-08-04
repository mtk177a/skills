---
name: implement-changes
description: Implement approved, sufficiently scoped code, documentation, or configuration changes in small units, choosing TDD when a meaningful failing test can express the expected behavior and another verification method when it cannot. Use after the change approach is clear; not for designing changes, reviewing a diff, or only validating completed work.
license: MIT
---

# Implement Changes

## Objective

- Apply an authorized and sufficiently clear change in small, reviewable work
  units.
- Choose verification from the expected outcome and available evidence instead of
  forcing one development method on every change.
- Finish with evidence that distinguishes executed checks from unverified scope
  and residual risk.

## Inputs and preconditions

Gather what is available:

- the approved objective, expected behavior, scope, exclusions, and stop
  conditions
- output from `design-changes` or another accepted implementation handoff
- an accepted diagnosis or other evidence for the required change boundary, when applicable
- target files, repository guidance, existing behavior, and affected consumers
- focused checks, broader regression commands, and environment constraints
- authorization and controls for dependency, destructive, migration,
  authentication, authorization, credential, permission, or cryptographic changes

`design-changes` output is optional. Infer low-impact local details from the
request and existing implementation, but do not invent requirements, authority,
or risk acceptance. If a missing item could materially change the implementation,
stop as `Blocked`.

## Workflow

1. Confirm the objective, authorization, entry conditions, scope, exclusions, and
   stop conditions before editing.
2. For a high-risk change, confirm that its exact action, scope, required controls, residual risk, and execution authority are ready for implementation. If not, stop before editing and identify the missing target, evidence, control, recovery, risk-acceptance, or authorization decision. Use `assess-risky-change-readiness` as an optional readiness handoff when available, but provide a self-contained stop report.
3. Inspect the relevant implementation and guidance. Confirm that the planned work
   units collectively cover the accepted coherent change boundary; do not narrow
   an approved structural correction to a local patch merely to reduce the diff.
   Split the change into small work units, each with an expected outcome and a
   verification method.
4. Select one work unit. Choose its verification mode using the criteria below and
   record the reason.
5. For a TDD work unit:
   - create or update one focused test
   - run it and confirm that it fails for the intended reason (Red)
   - make the simplest implementation change within the approved coherent boundary
     that passes it (Green)
   - refactor only while the test remains passing
6. For a non-TDD work unit:
   - establish the relevant baseline or pre-change observation when useful
   - make the simplest change within the approved coherent boundary
   - run the selected deterministic or inspection-based checks
   - do not manufacture an unrelated failure merely to create a Red phase
7. Record new evidence and update the remaining work units. If it shows that a
   local correction would leave the confirmed cause, a shared rule, an established
   responsibility boundary, or a known affected path unresolved, do not add a
   workaround. If the required coherent boundary exceeds the authorized scope, stop
   and report the evidence and required scope decision. Also stop for any other
   material dependency, test-strategy, or risk change before expanding the work.
8. Track implementation attempts separately from test executions. If two
   materially equivalent attempts under the same unchanged hypothesis fail
   without new evidence, stop before a third equivalent edit. Record the failed
   hypothesis and one structurally different branch or missing input.
9. After each work unit, run its focused checks. Before reporting completion, run
   the broader relevant regression checks available for the affected scope.
   Record checks that do not exist, cannot be run, or were intentionally excluded;
   do not present them as passing.
10. Report the final state using the semantic contract below.

## Choosing the verification mode

Use TDD by default when all of the following hold:

- the work changes observable behavior
- a focused automated check can express the expected outcome
- the check can fail meaningfully before implementation
- writing and running it is practical for the work unit

Do not decide from the file extension alone. A configuration change that affects
observable behavior may warrant TDD. Documentation, static metadata, schema-only
configuration, generated output, or behavior-preserving refactoring may instead
need:

- existing tests before and after the change
- parser or schema validation
- lint or formatting checks
- dry-run, render, build, or consumer checks
- deterministic diff or invariant checks
- focused inspection when no automated oracle exists

When TDD is not applicable, state why and identify the alternative evidence.
When it is selected, read `references/tdd_twada.md` for the concrete cycle.

## Reporting contract

Adapt the presentation to the task; do not emit empty headings. Always include:

- state: `Blocked`, `In progress`, or `Done`
- authorized scope, work units, expected outcomes, and actual changed files
- selected verification method for each completed work unit and why it fits
- the reason for the change and the handoff needed for review or validation

For `Blocked`, include:

- the stop reason and evidence
- missing information, authority, or controls
- the scope left unchanged
- the next decision or structurally different check

For `Done`, include:

- focused and broader checks actually run, with commands and results
- unperformed checks and unconfirmed items
- residual correctness, safety, and maintainability risks
- any user-facing explanation points needed to evaluate the result

## Boundaries

- Do not edit before confirming sufficient scope and authority.
- Do not remove or weaken a valid test merely to make the change pass.
- Do not force Red → Green when no meaningful failing behavior check exists.
- Do not treat repeated test observation as repeated implementation failure.
- Do not continue an unchanged third attempt without new evidence or a different
  hypothesis.
- Do not claim an unexecuted check passed or imply broader safety than the evidence
  supports.
- Do not replace an approved structural correction with a smaller local patch when
  that would leave the accepted cause or known affected paths unresolved.
- Do not introduce an abstraction, generalization, compatibility path, or unrelated
  refactoring unless it is required by the authorized outcome or accepted design.
- Ask before materially expanding scope, adding dependencies, changing the agreed
  test strategy, or performing an unapproved destructive or high-risk operation.
- Do not use another agent or subagent by default. Keep the workflow useful when no
  companion Skill is installed.
