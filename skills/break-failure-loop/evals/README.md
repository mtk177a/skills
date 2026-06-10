# break-failure-loop evals

## Iter 0 — Static check

- description and body are internally consistent on "stopping a failure loop"
- facts and hypotheses are separated in the output
- the limit on hypothesis count and next-step count is enforced
- at least one `[critical]` assertion is identified: recommending stop over continued iteration when appropriate

## Scenarios

### Scenario A: Same test failing more than twice

Similar fixes have been applied repeatedly without resolving the issue. The executor must organize the history and narrow the next step to exactly one.

Requirements checklist:
1. [critical] Propose exactly one next step
2. Separate confirmed successes from confirmed failures
3. Limit hypotheses to at most three

### Scenario B: Stopping is more appropriate than adding more changes

The change set has grown without progress and continuing under the same hypothesis is dangerous. The executor must return a stop recommendation.

Requirements checklist:
1. [critical] Recommend stopping rather than continuing
2. Stop reason is grounded in facts, not speculation
3. Files to read next are narrowed down

### Scenario C: First failure — not a loop

The user encountered a test failure for the first time after a change. This is not a loop. The executor must not suggest stopping or abandoning.

Requirements checklist:
1. [critical] Do not recommend stopping or abandoning on a first failure
2. Offer a hypothesis about the cause of the failure
3. Propose a diagnostic next step

## Failure Pattern Ledger

- `facts and hypotheses conflated`
- `next step not narrowed`
- `keeps editing despite repeated same-path failures`

## Iter N — not yet executed

Scenarios have not been executed. Execution results will be recorded here once run.
