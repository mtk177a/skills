# TDD Cycle Reference

This file is an original summary for this repository.\
It is based on Kent Beck's *Test-Driven Development: By Example* and on the workshop materials of Takuto Wada ([@t-wada](https://github.com/twada)).\
It contains no text copied from these sources.

`SKILL.md` gives the cycle: the test list, Red, Green, and Refactor.\
This file adds the rhythm of the cycle, the common mistakes, and the use of the test list.

## Rhythm

- Run each cycle in a few minutes, in small steps.
- In each cycle, run the fast tests near the target.\
  Before you finish, run the regression tests for the whole affected area.
- In Green, a fake implementation, such as a constant return value, is acceptable.\
  The next test then makes the implementation general.
- In Refactor, improve the test code as well as the implementation.\
  Rename, remove duplication, and separate concerns in small steps, and keep the tests passing after each step.
- Design each interface from the view of the code that calls it.
- Write tests that reduce the uncertainty of the developer.
- Keep most tests small and fast, and use fewer slow tests that cover the whole system.

## Common mistakes

| Mistake | Correct action |
| --- | --- |
| Several tests are written at once. | Add one test, and complete its cycle before the next test. |
| The implementation starts before a failing test. | Run the new test first, and see it fail for the expected reason. |
| An unrelated failure is created to have a Red phase. | When no meaningful failing test exists, use the check cycle in `SKILL.md`. |
| A test is deleted or commented out to make the suite pass. | Change the implementation, or change the test only when the expected behavior changed. |
| The expected value is copied from the output of the implementation. | Take the expected value from the specification or a known example. |
| Refactoring is done while a test fails. | Make the tests pass first, then refactor. |
| A large refactoring is done in one step. | Refactor in small steps, and run the tests after each step. |

## Test list

- Write each expected behavior as a short line.\
  The design of the implementation can come later.
- Add the new cases that you find during the work.
- Mark each item when its cycle is complete.
