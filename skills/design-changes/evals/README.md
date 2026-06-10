# design-changes evals

## Iter 0 — Static check

- description and body are internally consistent on "pre-implementation design judgment"
- change targets and non-targets are separated
- risks, mitigations, and test strategy are self-contained
- implementation go-conditions and stop conditions are stated explicitly
- at least one `[critical]` assertion is identified: go/stop conditions must be separated

## Scenarios

### Scenario A: Small feature addition

A small behavioral addition to existing code. Even without a `scope-request` result, the executor must organize the change target, non-target, and test strategy.

Requirements checklist:
1. [critical] Separate the conditions for proceeding to implementation from the stop conditions
2. Separate change targets from non-targets
3. Write risks and mitigations as pairs
4. Break the change into small units

### Scenario B: Change that may require a new dependency

There is an implementation plan, but dependency addition or spec confirmation may be required. The executor must surface Ask-first conditions as stop points before proceeding.

Requirements checklist:
1. [critical] Surface Ask-first conditions as stop conditions
2. Test strategy is written as a confirmation approach, not speculation
3. The plan is reviewable as a standalone document

### Scenario C: Auth-related change with high risk

A change touches authentication or authorization logic. The executor must surface risks and not proceed to implementation.

Requirements checklist:
1. [critical] Surface risks associated with auth changes explicitly
2. Do not proceed to implementation or write code
3. State what requires approval before any work begins

## Failure Pattern Ledger

- `target and non-target blurred`
- `risk listed without mitigation`
- `design-changes only usable as implement-changes handoff`
- `tradeoff not explainable`

## Iter N — not yet executed

Scenarios have not been executed. Execution results will be recorded here once run.
