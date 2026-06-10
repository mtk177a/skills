# clarify-request evals

Evaluates `clarify-request` in standalone operation. Checks whether it can identify ambiguities in a request and return targeted clarifying questions without beginning implementation.

## Iter 0

- `description` and body are aligned on "identifying ambiguities and formulating clarifying questions"
- Output is questions only — no implementation or design decisions
- Multi-scope requests are flagged for splitting
- Clear, well-specified requests are not over-questioned

## Open items

- Boundary between "vague enough to clarify" and "clear enough to proceed" has not been empirically tested
