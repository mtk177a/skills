---
name: implement-changes
description: Implement changes incrementally with test-driven development to progress safely.
license: MIT
---

# Implement Changes

## Purpose

- Use test-driven development as the default behavior to implement incrementally and safely.
- Drive from implementation decisions through testing to verification handoff, using this Skill alone first.

## When to use

- When you want to proceed with a new feature or fix using TDD
- When you want to implement safely in small units
- When you want to progress while organizing to a state ready to hand off to verification
- When you need to avoid continuing implementation after repeated same-hypothesis failures

## Input (optional)

- Output from `design-changes`
- Overview of the target feature
- Test execution command
- Implementation target files, constraints
- Entry conditions, scope, stop conditions

## Steps

1. Confirm the given entry conditions, scope, and stop conditions. If not stated explicitly, infer requirements from input and existing implementation; record anything missing as missing.
2. If entry conditions are not met, or a stop condition applies, do not proceed to implementation; output the reason for stopping and the next items to confirm.
3. Only when ready to proceed: break implementation tasks into small units; make the target and expected behavior explicit.
4. Create a test list.
5. Select exactly one item from the test list.
6. Translate it into a concrete test; confirm it fails (Red).
7. Write the minimal implementation to make the test pass (Green).
8. Refactor only when the test is passing.
9. Add new insights to the test list and repeat.
10. If the same test or behavior fails under the same hypothesis twice, stop implementation and record whether a structurally different branch is needed.
11. Update the test execution plan and verification handoff content.
12. Leave the reason for the change, verification basis, and explanation points for the user in the handoff.
13. Only when high-risk changes or quality uncertainty remain, explicitly state the need for additional confirmation.
14. For the concrete TDD rhythm, refer to `references/tdd_twada.md`.

## Output format

- Target: ...
- Work units: ...
- Files to change: ...
- Expected behavior: ...
- Entry condition check result: ...
- Scope: ...
- Stop conditions (Ask first): ...
- Test list:
  - ...
- Current test: ...
- Current phase: Blocked | Red | Green | Refactor | Done
- Same-hypothesis repetition check: ...
- Structurally different branch if blocked: ...
- Verification handoff: ...
- Reason for change: ...
- Verification basis: ...
- User explanation points: ...
- Next action: ...

## Boundaries

### Always:

- Follow the Red → Green → Refactor order
- Advance tests one at a time
- Stop as `Blocked` when entry conditions are not met
- State expected behavior and verification handoff explicitly
- Leave reason for change, verification basis, and explanation points
- Stop rather than keep editing when TDD iterations repeat the same hypothesis without progress
- Assess whether to proceed using only the input when `design-changes` output is not available
- Do not use another agent / subagent by default; proceed with this Skill alone first
- Keep the Skill useful even when no companion Skill is installed

### Ask first:

- When test strategy or dependencies would change significantly
- When destructive or large-scale changes are needed
- When entry conditions cannot be met and prerequisite confirmation is needed

### Never:

- Start implementation without confirming Red
- Remove tests to force a pass
- Continue local edits after repeated same-hypothesis failures without recording a different branch or stop reason
