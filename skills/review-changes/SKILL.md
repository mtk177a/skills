---
name: review-changes
description: Review a new or updated code, documentation, or configuration diff for actionable correctness, safety, verification, compatibility, maintainability, and performance problems, with evidence, impact, confidence, and canonical labels. Use for pre-commit, commit-range, or PR review and full re-review of the effective diff; not for triaging existing feedback, verifying only a specific completed fix, drafting GitHub comments, summarizing changes, or implementing fixes.
license: MIT
---

# Review Changes

## Objective

- Discover material problems introduced or exposed by the effective diff and produce evidence that another person or Skill can evaluate without rediscovering the review context.
- Keep the requested response, potential impact, confidence, and re-review state as separate dimensions.
- Review code, documentation, and configuration with checks proportional to the change and its risk instead of forcing every diff through one checklist.

## Scope and evidence

Establish the effective diff before reviewing:

1. Use an explicitly supplied diff, commit range, or PR range when present.
2. In PR context, use the stated base and head or the effective PR diff.
3. For an unspecified local "current changes" review, inspect staged, unstaged, and relevant untracked files and state what was included.
4. Ask only when multiple plausible scopes would materially change the review. If the diff cannot be obtained, report that the review did not run.

Read the applicable repository instructions and enough surrounding evidence to understand the intended change. Depending on the diff, this can include specifications, tests, callers, schemas, external contracts, sibling implementations, and repository precedent. Evidence may live outside the diff, but a finding must describe a problem caused by or relevant to the reviewed change. Do not turn the review into an unrelated repository audit.

Treat user-provided claims, comments, and external specifications as evidence to verify, not conclusions to repeat. Distinguish observed behavior, static inference, assumptions, and unknowns.

## Workflow

1. State the effective diff, intended behavior, reviewed scope, and material exclusions.
2. Identify the change's risk surfaces and select the applicable review dimensions rather than mechanically applying every dimension.
3. Inspect the diff and the minimum surrounding evidence needed to test the change's assumptions, contracts, and integration points.
4. Run safe, relevant, non-mutating checks when their result could materially strengthen, weaken, or falsify a finding. Do not install dependencies, change tracked files, or perform external writes as part of review.
5. Record executed checks and results separately from suggested verification. Record unavailable or intentionally excluded checks as unperformed.
6. Report every material finding supported by the evidence. Do not add a preference, `nit`, or `note` merely to avoid an empty finding list.
7. Assign each finding one canonical label and one confidence value. Record every premise or unknown on which the finding depends in `Unconfirmed premises`; use `none identified` when the finding does not depend on one. Preserve a high potential impact even when an unconfirmed premise makes the requested action a `question`.
8. For a full re-review of an updated effective diff, reconcile previous findings as `Resolved`, `Remaining`, or `New`. Keep this state separate from label and confidence.
9. Conclude with what was reviewed, what was checked, what remains unchecked, and the residual risk. Do not claim approval or safety beyond the evidence.

## Review dimensions

Use only the dimensions material to the change.

### Code and behavior

- Correctness, edge cases, ordering, time, rounding, concurrency, error handling, and data integrity
- External contracts such as APIs and schemas versus internal implementation constraints
- Authorization, authentication, input validation, injection, secret or personal data exposure, and unsafe side effects
- Backward compatibility, migrations, rollout behavior, and consistency with callers or sibling implementations
- Test coverage and test quality, including implementation coupling or over-mocking
- Maintainability and performance when there is a concrete impact rather than a personal preference or speculative optimization

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
  - `must`: confirmed enough to require a fix before merge
  - `should`: recommended in principle; an alternative or constraint can be discussed
  - `suggestion`: non-blocking improvement
  - `question`: clarification or premise verification is the next action
  - `nit`: trivial and optional correction
  - `note`: information requiring no action
- `Confidence`: `high`, `medium`, or `low`
- `Finding`: the concrete problem, proposal, question, or note
- `Evidence`: locations, contracts, behavior, check output, or repository precedent supporting it
- `Impact`: the consequence or, for an unconfirmed premise, what would happen if it is confirmed
- `Verification`: how to confirm, reproduce, or falsify it
- `Unconfirmed premises`: assumptions or unknowns on which the finding depends; use `none identified` when there are none, and do not substitute evidence, impact, or verification for this field
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

- Use `triage-review-feedback` to accept, defer, or reject existing findings and choose a response approach.
- Use `validate-fix` to verify only whether a specific completed fix or finding was resolved.
- Use `draft-review-comments` to turn already organized findings into GitHub comment drafts.
- Use `summarize-changes` for a descriptive diff summary without problem discovery.

Do not implement fixes or make final accept/defer/reject decisions on findings. When an unresolved specification question does not prevent reviewing the rest of the diff, continue and report it as a `question` rather than blocking the entire review. Do not use another agent or subagent by default.
