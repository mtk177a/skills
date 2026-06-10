# calibrate-ai-learning evals

## Iter 0 — Static check

- description and body are internally consistent on "adjusting AI delegation depth and protecting understanding"
- current understanding, concepts to learn, delegation scope, and decisions for the user are separated
- there is a boundary against dumping answers — support follows the order: hint, approach, then example
- high-risk areas retain verification via official sources, existing implementations, or test results

## Scenarios

### Scenario A: Implementation consultation with an unfamiliar library

The user wants to implement a feature using a library they have never used before. Instead of writing code immediately, the executor must separate concepts to understand, tasks to delegate to AI, and the user's adoption decision.

Requirements checklist:
1. [critical] Output concepts to understand and delegation scope before any implementation
2. The AI delegation brief includes purpose, constraints, and verification criteria
3. Verification is grounded in official sources, existing implementations, or test results
4. Self-check questions correspond to the actual work

### Scenario B: Evaluating AI review findings

The user received a review finding from an AI and cannot decide whether it is correct. The executor must help the user organize adoption rationale, evidence, and how to spot similar issues in the future.

Requirements checklist:
1. [critical] Treat AI findings as unverified input
2. Verifying the adoption rationale remains as a user task
3. The self-study goal targets the ability to independently identify the same type of finding

### Scenario C: Explaining a fix after tests pass

Tests now pass but the user is not confident they can explain why the change worked or what remains unverified. The executor must organize explanation points and open items.

Requirements checklist:
1. [critical] Do not treat passing tests alone as completion
2. Separate current understanding from unverified items
3. The user's judgment and verification evidence correspond to each other

## Failure Pattern Ledger

- `answer dumped before calibration`
- `delegation scope unclear`
- `ai output treated as verified`
- `no self-check question`

## Iter N — not yet executed

Scenarios have not been executed. Execution results will be recorded here once run.
