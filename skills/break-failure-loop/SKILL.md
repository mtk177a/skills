---
name: break-failure-loop
description: Stop and reframe when an agent has failed twice with the same error or approach — organize hypotheses, confirmed facts, unknowns, and next branches.
license: Apache-2.0
---

# Break Failure Loop

## Purpose

- Stop repeating the same failure and prevent a state where only the change count grows.
- Stop trial-and-error without hypothesis updates and narrow the next action to one.

## Conditions

- The same test has failed two or more times
- The same fix strategy has not resolved the issue
- The root-cause hypothesis has not been updated
- Only the number of changes is increasing

## What to do

- Organize the history of attempts in chronological order
- Separate confirmed findings from failed attempts
- Narrow current hypotheses to at most 3
- Narrow files still to read to at most 5
- Propose exactly one next action
- Propose stopping if continuing implementation would be dangerous

## Steps

1. List recent attempts in chronological order.
2. For each attempt, separate: what was changed, what was checked, and what the result was.
3. Separate confirmed facts from things still based on guesses.
4. Narrow current hypotheses to at most 3; attach evidence to each hypothesis.
5. Narrow files still to read to at most 5.
6. Choose exactly one thing to check next.
7. If the only option is to continue with the same hypothesis, propose stopping instead of continuing.

## Output format

- Current situation: ...
- What was tried:
  - ...
- What was confirmed:
  - ...
- What is still unknown:
  - ...
- Leading hypotheses:
  - ...
- Next thing to check: ...
- Continue / Stop judgment: ...

## Boundaries

### Always:

- Organize attempt history in chronological order
- Separate confirmed findings from failed attempts
- Narrow hypotheses to at most 3
- Propose exactly one next action

### Ask first:

- When stopping is more appropriate than continuing implementation
- When additional changes are large and failure cost is growing further

### Never:

- Do not proceed to a third attempt of the same approach with the same hypothesis
- Do not accumulate more changes without first organizing the situation
