# triage-review-feedback evals

## Iter 0 — Static check

- description and body are internally consistent around "accept/defer/reject decision-making"
- accept, defer, and reject categories are clearly distinguished
- accepted items include priority and action plan
- output is sufficient to proceed to implementation start or deferral decision on its own
- at least one `[critical]` assertion is identified

## Scenarios

### Scenario A: Standard review finding triage

Two or three review findings are received. Sort into accept, defer, and reject with reasons.

Requirements checklist:
1. [critical] Each finding has an accept/defer/reject reason
2. Accepted findings have priority ordering
3. Action plan is written at an actionable level of detail

### Scenario B: Review with spec-dependent findings

Some findings require a spec decision and cannot be immediately accepted. Deferral and required follow-up are stated explicitly.

Requirements checklist:
1. [critical] Findings requiring a spec decision are not auto-accepted
2. Deferral reason and confirmation items are present
3. Output can be handed off to the next decision-maker as-is

### Scenario C: AI finding with unverified external spec claim

An AI review asserts a platform syntax error (e.g., GitHub Actions YAML) as definite, but no official source is cited in the input. Should not be auto-accepted; must route to verify or reject.

Requirements checklist:
1. [critical] Finding is not auto-accepted when no official documentation or primary source is cited
2. Accept/defer/reject decision and the required verification action are separated
3. When no evidence is available the finding is deferred; when official source confirms it is wrong the finding is rejected

## Failure Pattern Ledger

- `decision without rationale`
- `accepted item lacks actionable plan`
- `triage depends on prior flow-specific labels`
