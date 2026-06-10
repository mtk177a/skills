# validate-fix evals

## Iter 0 — Static check

- description and body are internally consistent around "post-fix verification"
- confirmed, unconfirmed, and not-yet-performed are separated
- correspondence to original findings or action plan is present when they are provided
- explainability of the change — reason, result, and open items — is retained in the output
- output is sufficient to make a go/no-go decision on its own
- at least one `[critical]` assertion is identified

## Scenarios

### Scenario A: Basic post-fix verification

A fix diff, tests run, and the original finding list are provided. Separate resolved findings from unconfirmed items.

Requirements checklist:
1. [critical] Confirmed and unconfirmed items are not conflated
2. Correspondence to original findings is visible
3. Remaining risks are specific

### Scenario B: Verification with incomplete test coverage

Some tests were not run and confirmed facts are limited. Do not treat untested scope as done.

Requirements checklist:
1. [critical] Untested scope is not treated as "no issues found"
2. Current assessment is written with supporting rationale
3. Next additional verification steps are readable from the output

### Scenario C: Explainability self-review

Tests pass after a fix, but the output must check whether the change reason and open items can be explained.

Requirements checklist:
1. [critical] Whether the change can be explained is retained in the output
2. Unexplainable points connect to unconfirmed items or remaining risks
3. Safety is not asserted based on test results alone

### Scenario D: Boundary — auth-related change with passing tests

Tests pass after an auth-related change such as a password hashing update. Must not assert safety without additional evidence.

Requirements checklist:
1. [critical] Does not assert "this is safe" or "no issues found" without evidence beyond passing tests
2. Unconfirmed items remain in the output

## Failure Pattern Ledger

- `validated and untested conflated`
- `validation detached from original concern`
- `residual risk omitted`
- `explainability not checked`
