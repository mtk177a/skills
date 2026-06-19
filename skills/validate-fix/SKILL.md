---
name: validate-fix
description: Verify a fix — organize what was confirmed, what was not, and what risks remain.
license: MIT
---

# Validate Fix

## Purpose

- After a fix, separate what is confirmed from what is not, and organize residual risks.
- Organize the fix diff, tests performed, and review angles to produce decision material for whether it is safe to proceed.

## When to use

- When you want to verify after addressing review comments
- When you want to explain the post-fix state to others
- When you want to organize decision material for whether to proceed at this point
- When you need to detect partial improvement, case-level regression, or average-score-only success claims

## Input (optional)

- Fix diff
- Verification steps performed
- Test results
- Original review comments or response approach

## Steps

1. Organize the test scope and fix diff.
2. State the tests and verification steps performed; organize what was confirmed.
3. If original comments or a response approach exist, organize how much was resolved.
4. Separately state unperformed scope and unconfirmed items.
5. If uncertainty remains from the perspectives of correctness, safety, or maintainability, state the need for additional confirmation.
6. Check whether the fix only improved some cases while weakening others, or whether average score hides case-level behavior.
7. Organize remaining risks.
8. Check whether the reason for the change, verification results, and unconfirmed items can be explained.
9. Summarize the current assessment and any additional confirmations needed to proceed.
10. Only when high-risk changes or quality concerns remain, suggest using another agent / subagent.

## Output format

- Test scope:
  - ...
- Tests performed:
  - ...
- Confirmed resolved findings / responses:
  - ...
- What was confirmed:
  - ...
- Unperformed scope:
  - ...
- Unconfirmed items:
  - ...
- Remaining risks:
  - ...
- Case-level behavior / regressions:
  - ...
- Whether it can be explained:
  - ...
- Current assessment: ...

## Companion skills

- `review-changes`
- `triage-review-feedback`
- `diversify-agent-search` if available when partial improvement requires candidate comparison or case-level evaluation planning

## Boundaries

### Always:

- Separate confirmed from unconfirmed
- Record test scope and unperformed scope separately
- When original comments or a response approach exist, preserve the correspondence with verification results
- Treat partial improvement and case-level regressions as separate from a simple pass/fail result
- Check whether the reason for the change, verification results, and unconfirmed items can be explained
- Do not use another agent / subagent by default; return verification results from this Skill alone first
- Keep the Skill useful even when no companion Skill is installed

### Ask first:

- When additional confirmation appears needed for a high-risk change

### Never:

- Assert safety without evidence
- Assert no issues without verification
- Treat a better average result as sufficient when important case-level regressions remain unexamined
