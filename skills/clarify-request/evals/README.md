# clarify-request evals

## Iter 0 — Static check

- description and body are internally consistent on "identifying ambiguities and formulating clarifying questions"
- output is questions only — no implementation or design decisions
- multi-scope requests are flagged for splitting
- clear, well-specified requests are not over-questioned
- at least one `[critical]` assertion is identified: questions must be produced for vague requests, not implementation

## Scenarios

### Scenario A: Vague improvement request

The request is too vague to act on. The executor must produce clarifying questions rather than beginning implementation or proposing a specific solution.

Requirements checklist:
1. [critical] Produce clarifying questions — do not start implementing or optimizing
2. Questions target the ambiguity specifically (what to optimize, metric, scope)
3. At most four questions are asked

### Scenario B: Multi-scope request

A single request spans multiple unrelated changes. The executor must flag that the request should be split before proceeding.

Requirements checklist:
1. [critical] Identify that the request covers multiple separate scopes
2. Suggest splitting into separate requests
3. Do not begin any of the three tasks

### Scenario C: Well-specified request — no over-questioning

A request is specific and actionable. The executor must not block it with unnecessary clarifying questions.

Requirements checklist:
1. [critical] Do not ask for clarification when the request is already sufficiently specific
2. Do not ask what is already stated in the request

## Failure Pattern Ledger

- `questions not produced for vague requests`
- `implementation started before clarification`
- `over-questioning on clear requests`
- `multi-scope not flagged for splitting`

## Iter N — not yet executed

Scenarios have not been executed. Execution results will be recorded here once run.
