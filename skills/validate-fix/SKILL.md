---
name: validate-fix
description: Verify a fix — organize what was confirmed, what was not, and what risks remain.
license: Apache-2.0
---

# Validate Fix

## Purpose

- After a fix, separate what is confirmed from what is not, and organize residual risks.
- Organize the fix diff, tests performed, and review angles to produce decision material for whether it is safe to proceed.

## When to use

- When you want to verify after addressing review comments
- When you want to explain the post-fix state to others
- When you want to organize decision material for whether to proceed at this point

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
6. Organize remaining risks.
7. Check whether the reason for the change, verification results, and unconfirmed items can be explained.
8. Summarize the current assessment and any additional confirmations needed to proceed.
9. Only when high-risk changes or quality concerns remain, suggest using another agent / subagent.

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
- Whether it can be explained:
  - ...
- Current assessment: ...

## Companion skills

- `review-changes`
- `triage-review-feedback`

## Boundaries

### Always:

- Separate confirmed from unconfirmed
- Record test scope and unperformed scope separately
- When original comments or a response approach exist, preserve the correspondence with verification results
- Check whether the reason for the change, verification results, and unconfirmed items can be explained
- Do not use another agent / subagent by default; return verification results from this Skill alone first

### Ask first:

- When additional confirmation appears needed for a high-risk change

### Never:

- Assert safety without evidence
- Assert no issues without verification
