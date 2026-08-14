---
name: review-changes
description: Review a new code, documentation, or configuration diff, or perform an explicitly requested full re-review of the effective diff, for proportionate and actionable correctness, safety, verification, compatibility, maintainability, and performance problems. Report evidence, impact, risk context, confidence, and canonical labels. Do not use for ordinary post-fix re-review of identified findings, triaging existing feedback, drafting GitHub comments, summarizing changes, or implementing fixes.
license: MIT
---

# Review Changes

## Objective

- Discover material problems introduced or exposed by the effective diff and produce evidence that another person or Skill can evaluate without rediscovering the review context.
- Keep the requested response, potential impact, confidence, and re-review state as separate dimensions.
- Calibrate requested responses to the change purpose, affected criticality and exposure, and the cost and risk of remediation without reducing the judgment to a numeric score.
- Review code, documentation, and configuration with checks proportional to the change and its risk instead of forcing every diff through one checklist.

## Scope and evidence

Establish the effective diff before reviewing:

1. Use an explicitly supplied diff, commit range, or PR range when present.
2. In PR context, use the stated base and head or the effective PR diff.
3. For an unspecified local "current changes" review, inspect staged, unstaged, and relevant untracked files and state what was included.
4. Ask only when multiple plausible scopes would materially change the review. If the diff cannot be obtained, report that the review did not run.

Read the applicable repository instructions and enough surrounding evidence to understand the intended change. Depending on the diff, this can include specifications, tests, callers, schemas, external contracts, sibling implementations, and repository precedent. Evidence may live outside the diff, but a finding must describe a problem caused by or relevant to the reviewed change. Do not turn the review into an unrelated repository audit.

Treat user-provided claims, comments, and external specifications as evidence to verify, not conclusions to repeat. Distinguish observed behavior, static inference, assumptions, and unknowns.

Use supplied reviewer context when available: objective and expected result; product or operational context and criticality; scope and non-goals; affected users, data, contracts, and exposure; constraints and accepted trade-offs; verification and unknowns; detection and recovery controls; and requested review focus. Preserve material evidence states such as `Observed`, `Reported`, `Inferred`, `Unknown`, and `Conflicting`. Missing criticality or exposure is `Unknown`, not evidence of low risk.

## Workflow

1. State the effective diff, intended behavior, reviewer context, reviewed scope, and material exclusions. If the purpose, criticality, or exposure is material but unavailable, retain it as an unknown rather than inventing a value.
2. Review the change purpose, design, contracts, responsibility boundaries, and affected consumers before line-level details. Identify the risk surfaces and select the applicable review dimensions rather than mechanically applying every dimension.
3. Inspect the diff and the minimum surrounding evidence needed to test the change's assumptions, contracts, integration points, and claimed reviewer context.
4. Run safe, relevant, non-mutating checks when their result could materially strengthen, weaken, or falsify a finding. Do not install dependencies, change tracked files, or perform external writes as part of review.
5. Record executed checks and results separately from suggested verification. Record unavailable or intentionally excluded checks as unperformed.
6. Report every material finding supported by the evidence. Keep the stated impact to consequences supported by the supplied or inspected contracts, behavior, and paths; do not invent a plausible downstream mechanism merely to make the finding sound more severe. If a potentially material downstream consequence is useful but unverified, state it conditionally and record its dependency in `Unconfirmed premises`. Do not add a preference, `nit`, or `note` merely to avoid an empty finding list.
7. Characterize the finding's exposure and preconditions, affected criticality and blast radius, detectability and recovery, and remediation cost or trade-offs when they can change the requested response. Use ordinal, evidence-backed comparisons rather than a fabricated numeric score. Prefer the least costly response sufficient for the supported risk.
8. Assign each finding one canonical label and one confidence value. Record every premise or unknown on which the finding, its stated impact, risk context, or requested response depends in `Unconfirmed premises`; use `none identified` only when none of those claims depends on one. Preserve a high potential impact even when an unconfirmed premise makes the requested action a `question`.
9. For an explicitly requested full re-review, reconcile previous findings as `Resolved`, `Remaining`, or `New`. Classify every `New` finding as `Fix-induced`, `Newly observable`, or `Late-discovered`. Report material findings from all three origins. A previously observable `Late-discovered` item that is independently non-blocking must not start another fix round; omit it from actionable findings or, only when useful, summarize it as a non-actionable `note`.
10. Conclude with what was reviewed, what was checked, what remains unchecked, and the residual risk. If material review dimensions remain incomplete, say the review is incomplete rather than implying a completed approval or safety judgment.

## Review dimensions

Use only the dimensions material to the change.

### Code and behavior

- Correctness, edge cases, ordering, time, rounding, concurrency, error handling, and data integrity
- External contracts such as APIs and schemas versus internal implementation constraints
- Authorization, authentication, input validation, injection, secret or personal data exposure, and unsafe side effects
- Backward compatibility, migrations, rollout behavior, and consistency with callers or sibling implementations
- Test coverage and test quality, including implementation coupling or over-mocking
- Maintainability and performance when there is a concrete impact rather than a personal preference or speculative optimization
- Unjustified abstractions, extension points, configuration surfaces, dependencies, compatibility paths, or architectural layers whose concrete maintenance or operational cost is not supported by current requirements or observed risks
- Local patches that reduce diff size while leaving a confirmed cause unresolved, duplicating a shared rule, bypassing an established responsibility boundary, creating inconsistent behavior across known paths, or requiring a known follow-up correction

Treat both excess complexity and an overly narrow correction as findings only when the evidence shows a concrete consequence such as duplicated policy, inconsistent behavior, unreachable branches, added operational burden, or a known follow-up change. Do not report either from architectural preference alone.

### Documentation

- Factual accuracy and consistency with the implementation or canonical source
- Commands, examples, links, identifiers, terminology, and reader-visible omissions
- Render, lint, or deterministic content checks when available

### Configuration

- Schema and parser validity, precedence, defaults, environment interaction, and compatibility
- Whether a static value changes observable behavior and therefore warrants a behavior check
- Rollout, recovery, secret handling, and operational consequences

## Finding contract

- `Label`
  - `must`: supported enough to require a fix before merge for a material risk when no lower-cost response sufficiently addresses it
  - `should`: recommended in principle; an alternative or constraint can be discussed
  - `suggestion`: non-blocking improvement
  - `question`: clarification or premise verification is the next action
  - `nit`: trivial and optional correction
  - `note`: information requiring no action
- `Confidence`: `high`, `medium`, or `low`
- `Finding`: the concrete problem, proposal, question, or note
- `Evidence`: locations, contracts, behavior, check output, or repository precedent supporting it
- `Impact`: the consequence supported by the available evidence or, for an explicitly recorded unconfirmed premise, what would happen if it is confirmed; do not invent an uninspected downstream mechanism
- `Exposure and preconditions`, when material to the requested response: the conditions, reachable paths, frequency, or affected population supported by evidence; use `Unknown` when it is material but unavailable
- `Criticality and blast radius`, when material to the requested response: the importance of the affected product, tool, data, contract, or operation and the supported extent of harm
- `Detectability, recovery, and workaround`, when material to the requested response: applicable detection, containment, recovery, rollback, or practical workaround evidence
- `Remediation cost and trade-offs`, when material to the requested response: material implementation, verification, complexity, regression, delay, and maintenance costs supported by current evidence
- `Verification`: how to confirm, reproduce, or falsify it
- `Unconfirmed premises`: assumptions or unknowns on which the finding, its stated impact, or the requested response depends; use `none identified` when there are none, reconcile the field with unchecked scope and residual risks, and do not substitute evidence, impact, or verification for it
- `Re-review state`: `Resolved`, `Remaining`, or `New`, only for an explicitly requested full re-review
- `New finding origin`: `Fix-induced`, `Newly observable`, or `Late-discovered`, only for a `New` finding
- `Generalizable check`: include only when it provides reusable learning beyond the current diff

Accept `Must-fix`, `Should-fix`, and `Nice-to-have` as legacy input and normalize them to `must`, `should`, and `suggestion` or `nit`. Do not use `must` or `should` for preference-only findings. A `question` can carry high potential impact; do not erase that impact merely because the premise remains unconfirmed.

## Reporting contract

Adapt the presentation to the review state and omit empty sections.

For a completed review, include:

- conclusion and effective diff
- reviewed scope and material exclusions
- findings, ordered by requested response and impact
- checks performed with commands or methods and actual results
- suggested verification, unchecked scope, and residual risks

If there are no material findings, state that explicitly and still report the reviewed scope, checks, unchecked scope, and residual risk. Do not produce a bare `LGTM` or manufacture minor comments.

If the diff cannot be obtained or its materially different interpretations cannot be resolved, state that the review did not run, identify the missing input, and do not present the result as "no issues found."

## Related workflow boundaries

- Use `triage-review-feedback` to assess existing findings and choose a response decision and approach.
- Use `validate-fix` by default for ordinary post-fix re-review of one or more identified findings.
- Use `draft-review-comments` to turn already organized findings into GitHub comment drafts.
- Use `summarize-changes` for a descriptive diff summary without problem discovery.

Do not implement fixes or make final response decisions on findings. When an unresolved specification question does not prevent reviewing the rest of the diff, continue and report it as a `question` rather than blocking the entire review. Do not use another agent or subagent by default.
