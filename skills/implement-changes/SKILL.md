---
name: implement-changes
description: Implements an authorized code, documentation, or configuration change in small verified units, with test-driven development (TDD) when a test can show the expected behavior. Use when the change to make is clear and the next step is to edit files.
license: MIT
---

# Implement Changes

Make the change in small units, and verify each unit before you start the next one.

## Before you edit

1. **Write down the scope**

   Write down the expected behavior, the parts that you can change, and the parts that must stay the same.\
   Done when each item comes from the request or from an agreed plan, or the user confirmed it.\
   If a missing item can change the implementation, stop with the state `Blocked` and ask for it.

2. **For a high-risk change, confirm authorization and recovery**

   If the change deletes or migrates data, adds a dependency, or changes authentication, credentials, permissions, or cryptography, confirm two things:

   - The user authorized the action and the scope of the change.
   - A way to recover from a failure exists.

   Done when both are confirmed.\
   If one is missing, stop with the state `Blocked` before you edit, and report what is missing.

3. **Make a test list**

   Write one short line for each behavior that the change adds or changes.\
   For a change that keeps behavior, list the checks that will show the result.\
   Done when each expected behavior or result has a line.

## Do one unit at a time

Take one item from the test list, and use one of the two cycles below.

### TDD cycle

Use the TDD cycle when a fast test at a public interface can fail before the change for the expected reason.

1. **Red**

   Write one test for the item, and run it.\
   Done when the test fails, and the failure shows that the expected behavior is missing.

2. **Green**

   Make the smallest change that makes the test pass.\
   A temporary, simple implementation is acceptable.\
   Done when the new test and the other focused tests pass.

3. **Refactor**

   Improve the code and the tests that you wrote or changed in the current cycle, for example names and duplication.\
   Run the tests after each small improvement.\
   Done when the tests pass and the code of the current cycle is clear.

4. **Update the test list**

   Mark the item done, and add the new items that you found.

Write tests that:

- check behavior through a public interface, so that they pass when the internal structure changes
- get the expected value from the specification or a known example, not from the same calculation that the code uses
- replace only external dependencies, such as the network or the clock, with test doubles

When the implementation and a valid test disagree, change the implementation.\
Change a test only when the expected behavior changed.

For the TDD rhythm and common mistakes, read `references/tdd_twada.md`.

### Check cycle

Use the check cycle for documentation, metadata, generated output, and refactoring that keeps behavior.\
Use it also when a useful test needs large setup, many mocks, slow end-to-end infrastructure, or production-only state.\
A test that mostly checks mocks or the current implementation is worse than the nearest useful check.

1. **Record the current result**

   When a comparison helps, record the current result.

2. **Make the change**

   Make the change for the item.

3. **Run the check**

   Run the check that shows the result, for example one of these:

   - the existing tests, before and after the change
   - a parser or schema validation, lint, or a format check
   - a dry run, a build, or a render
   - a careful inspection, when no automated check exists

   Done when the check shows the expected result.

## When the plan stops fitting

- If the necessary change is larger than the parts that you can change, stop.\
  Report the evidence and the scope that you need.
- If a larger structural change is necessary, such as splitting a module, report it as a separate change.
- Fix the confirmed cause.\
  If you add a fallback or a mitigation, report it as a mitigation, with the condition that starts it.
- If two attempts with the same hypothesis fail and give no new evidence, stop the attempts.\
  Before the next edit, change the hypothesis or report the missing input.

## Finish

1. **Run the regression checks**

   Run the regression checks for the whole affected area.\
   Done when they pass, or when you recorded each failure.

2. **Report the result**

   Report these items:

   - the state: `Done`, `In progress`, or `Blocked`
   - the files that changed
   - for each item on the test list, the test or check, its result before the change, and its result after the change
   - the checks that you did not run, and the reason
   - the risks that remain
   - for `Blocked`, the missing input and the parts that you did not change

3. **For `Done`, add the reviewer context**

   Add the information that a reviewer needs, in the table below.\
   Include only the rows that apply.

   | Field | Content |
   | --- | --- |
   | Objective | The objective and the result |
   | Usage context | The product or operational context, and its criticality |
   | Scope | The actual scope and the exclusions |
   | Impact | The affected users, data, and contracts |
   | Decision constraints | The constraints and the accepted trade-offs |
   | Verification | The verification and the unknowns |
   | Controls | The detection and recovery controls |
   | Review | The parts that the reviewer must examine carefully |
