---
name: review-changes
description: Review a diff for correctness, tests, safety, maintainability, and performance — organize findings with canonical labels.
license: Apache-2.0
---

# Review Changes

## Purpose

- Review a diff and organize findings across correctness, tests, safety, maintainability, and performance.
- Attach a canonical label (`must` / `should` / `suggestion` / `question` / `nit` / `note`) to each finding to connect to the next decision.
- Keep findings, evidence, and label criteria organized in a form ready to pass to `draft-review-comments`.

## When to use

- When receiving a code review request
- When you want to inspect changes before committing or opening a PR
- When you want to organize findings to hand off to the next step
- When you want a fresh review of the diff itself — not processing existing review comments

## Input (optional)

- Target diff (`git diff`, PR diff, commit diff)
- Related specifications or background
- Priority review angles

## Steps

1. Understand the change content (diff).
2. Extract problems and improvements across correctness, tests, safety, maintainability, and performance.
3. Prioritize and categorize issues that could lead to production incidents, security problems, or spec mismatches.
4. Attach evidence to each finding; add reproduction or verification angles when needed.
5. For each finding, include: evidence, why it is a problem, how to detect it, and verification angle.
6. Choose exactly one canonical label for each finding.
7. For a re-review after fixes, first organize `Resolved` / `Remaining` / `New` against the previous findings before summarizing current observations.
8. Present as a labeled finding list following the output format.
9. When `Must-fix` / `Should-fix` / `Nice-to-have` appear in input or existing notes, accept them as compatible input and map to canonical labels.
10. Only state the need for additional confirmation when high-risk changes or review quality uncertainty remain.
11. When accept/reject decisions or response approaches are needed, leave unresolved items and verification angles in a form ready to use as decision material.

## Review dimensions

### 1. Correctness

- Does it satisfy the spec? Is error and edge case handling appropriate?
- No pitfalls with null / empty / boundary values, ordering dependencies, rounding, timezones, concurrency?
- Separate external contracts (API, schema) from internal constraints; identify whether issues are contract violations or implementation choices

### 2. Tests

- Are there tests that cover the changes?
- Are tests overly coupled to implementation or fragile due to over-mocking?

### 3. Security

- No secret leakage, injection, authorization check failures, or input validation gaps?
- No PII / confidential data in logs or error messages?

### 4. Maintainability

- No issues with responsibility separation, naming, duplication, complexity, or consistency of error handling?
- No unnecessary disruption of existing design or style?
- For consistency comments, evaluate across sibling endpoints / shared wrappers / shared types in the repo and base label strength on repo precedent

### 5. Performance

- No obvious bottlenecks or wasteful processing?
- Avoid demanding excessive optimization

## Label vocabulary

- `must`: fix required before merge; do not approve if this remains
- `should`: fix recommended in principle; discussion allowed with reason
- `suggestion`: improvement proposal; better but does not block merge
- `question`: spec, intent, or assumptions are unconfirmed; should not be asserted
- `nit`: minor comment; optional by default
- `note`: reference information; no response needed
- `Must-fix` → `must`, `Should-fix` → `should`, `Nice-to-have` → `suggestion` or `nit`
- Severity and certainty are different axes; if spec or intent is unconfirmed, do not use `must` — use `question` instead
- Do not use `must` / `should` for preference-only findings

## Output format

- Summary: ...
- Findings:
  - Label: `must`
    - Finding: ...
    - Evidence: ...
    - Why it is a problem: ...
    - How to detect: ...
    - Verification angle: ...
- Test steps:
  - ...
- Additional items to check:
  - ...

## Companion skills

- `triage-review-feedback`
- `validate-fix`

## Boundaries

### Always:

- Base the review on the change content
- Attach specific evidence to each finding
- Include enough "why it is a problem" and "how to detect it" for accept/reject decisions and learning
- Attach a canonical label to each finding
- Keep labels and evidence separated so they can be passed to `draft-review-comments`
- Leave enough information that accept/reject decisions can proceed without additional context
- Do not use another agent / subagent by default; return review results from this Skill alone first

### Ask first:

- When the target change scope is unclear
- When a judgment on spec changes is required

### Never:

- Make the final accept/reject decision on findings
- Proceed to implementation fixes
- Make findings based on guesses without reading the change
- Assert an unconfirmed assumption as `must`
