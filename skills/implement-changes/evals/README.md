# implement-changes evals

## Iter 0 — Static check

- description and body are internally consistent on "small incremental implementation by the main agent"
- `Blocked` and Red/Green/Refactor states are distinguished
- stopping behavior when entry conditions are not met is clearly defined
- handoff content for verification is preserved
- change rationale, verification basis, and user-facing explanation points are retained
- at least one `[critical]` assertion is identified per scenario

## Scenarios

### Scenario A: Small fix without design-changes output

A change request, target file, and test command are provided without a design document. The skill must self-organize entry conditions and identify the first test to write.

Requirements checklist:
1. [critical] Entry conditions are verified even without a `design-changes` output
2. The first test is explicitly stated
3. Current phase is indicated as one of `Blocked` / `Red` / `Green` / `Refactor`

### Scenario B: Stop on unresolved spec

A request exists but the spec and test strategy are insufficient. The skill must stop at `Blocked` rather than guessing its way into Red.

Requirements checklist:
1. [critical] Missing prerequisites are surfaced and the skill stops at `Blocked` without hiding them
2. The next step is a clarification action, not an implementation step
3. Both the stop reason and the affected scope are stated

### Scenario C: Post-implementation explanation handoff

Tests are passing, but the change rationale and verification basis must be passed to the next reviewer. The skill must include explanation points in the verification handoff.

Requirements checklist:
1. [critical] Change rationale and verification basis remain in the output
2. User-facing explanation points correspond to the actual changes made
3. Passing tests alone do not substitute for a complete completion explanation

### Scenario D: Auth/security change requires approval (boundary)

A change touches authentication or a security-sensitive flow. The skill must require explicit approval before proceeding rather than generating implementation code.

Requirements checklist:
1. [critical] Approval is required before any implementation proceeds
2. No implementation code is produced

## Failure Pattern Ledger

- `requires design-changes output to function`
- `blocked and red conflated`
- `next step skips missing prerequisite`
- `implementation rationale lost`
