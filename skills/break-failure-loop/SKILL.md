---
name: break-failure-loop
description: Stop and reframe when an agent has failed twice with the same error or approach — organize hypotheses, confirmed facts, unknowns, and next branches.
license: MIT
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
- Attempts keep modifying the same design neighborhood without testing a structurally different branch

## What to do

- Organize the history of attempts in chronological order
- Separate confirmed findings from failed attempts
- Narrow current hypotheses to at most 3
- Narrow files still to read to at most 5
- Check whether the work is stuck around the same design assumption
- Propose exactly one next action
- If stuck in one design neighborhood, make the next action a structurally different branch or a search-diversification handoff
- Propose stopping if continuing implementation would be dangerous

## Steps

1. List recent attempts in chronological order.
2. For each attempt, separate: what was changed, what was checked, and what the result was.
3. Separate confirmed facts from things still based on guesses.
4. Narrow current hypotheses to at most 3; attach evidence to each hypothesis.
5. Narrow files still to read to at most 5.
6. Check whether recent attempts only changed prompt wording, regular expressions, output normalization, retries, or local patches around the same design assumption.
7. If search diversification is needed and no companion Skill is available, propose one structurally different branch directly.
8. Choose exactly one thing to check next.
9. If the only option is to continue with the same hypothesis or design anchor, propose stopping instead of continuing.

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
- Same design neighborhood?: yes/no
- Structurally different branch if needed: ...
- Next thing to check: ...
- Continue / Stop judgment: ...

## Companion skills

- `diversify-agent-search` if available for deeper candidate archive, diversity axes, and case-level evaluation planning

## Boundaries

### Always:

- Organize attempt history in chronological order
- Separate confirmed findings from failed attempts
- Narrow hypotheses to at most 3
- Check whether repeated attempts are still in the same design neighborhood
- Propose exactly one next action
- Keep the Skill useful even when no companion Skill is installed

### Ask first:

- When stopping is more appropriate than continuing implementation
- When additional changes are large and failure cost is growing further

### Never:

- Do not proceed to a third attempt of the same approach with the same hypothesis
- Do not accumulate more changes without first organizing the situation
- Do not require another Skill before giving a stop judgment or a structurally different next branch
