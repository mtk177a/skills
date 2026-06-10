# scope-request evals

## Iter 0 — Static check

- description and body are internally consistent around "request decomposition"
- objective, done condition, constraints, assumptions, and open items are separated
- output is sufficient to proceed to the next decision or clarification request on its own

## Scenarios

### Scenario A: Vague improvement request

The request is short; there is background context but the done condition is ambiguous. Only request decomposition is performed — no implementation is started.

Requirements checklist:
1. [critical] Objective and done condition are written as separate items
2. Constraints and assumptions are written as separate items
3. Open items and questions to confirm are separated
4. The next step is understandable without external context

### Scenario B: Bug report with constraints

Symptoms and constraints are present but reproduction steps and scope are missing. Open items are stated explicitly; do not push toward a design solution prematurely.

Requirements checklist:
1. [critical] Missing information is retained as open items
2. Constraints are not conflated with assumptions or background
3. Questions to confirm are specific

### Scenario C: Boundary — well-specified request is not over-decomposed

A clearly scoped, single-line change should be handled directly without unnecessary breakdown into objectives and open questions.

Requirements checklist:
1. [critical] Well-specified requests are not broken down into redundant clarification steps
2. Does not ask "what is the expected behavior?" for changes that already state expected behavior

## Failure Pattern Ledger

- `goal and done conflated`
- `constraints mixed with assumptions`
- `next step only meaningful inside a flow`
