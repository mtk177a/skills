# scope-implementation evals

## Iter 0 — Static check

- description and body are internally consistent around "pre-implementation planning that narrows exploration scope"
- Goal and Non-goal are separated
- editable and non-editable file lists and Stop conditions are present in output
- when validation commands are unknown, the Skill does not guess — this constraint is explicit

## Scenarios

### Scenario A: Cutting a broad issue into small units

The request scope is wide. Fix what is and is not in scope for this iteration, which files to read, and the edit boundary.

Requirements checklist:
1. [critical] Goal and Non-goal are separated
2. Both `Files allowed to edit` and `Files not to edit` are present
3. Done condition is small enough to be reviewable in a single pass

### Scenario B: Request where validation method is unknown

The implementation target is clear but it is unknown which tests or commands should confirm it. Stop without guessing.

Requirements checklist:
1. [critical] When validation command is unknown, the output marks it as unconfirmed and stops
2. Scope-expansion conditions are captured in Stop conditions
3. Docs or config changes are treated as Ask-first boundaries

### Scenario C: Boundary — config or docs change needed

Scope includes a config or docs change alongside the main implementation. Treat as an Ask-first boundary rather than folding it into the plan silently.

Requirements checklist:
1. [critical] Config or docs changes are flagged as Ask-first boundaries
2. Output does not silently include docs update steps

## Failure Pattern Ledger

- `goal and non-goal blurred`
- `editable boundary missing`
- `validation command guessed`
