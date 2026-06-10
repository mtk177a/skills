# triage-agent-usage evals

## Iter 0 — Static check

- description and body are internally consistent around "pre-task triage of tool and model selection"
- whether the task requires reading the repository is clearly distinguished
- rationale for choosing a heavier option is retained in the output
- learning-priority vs. deadline-priority, and whether the user can review the output, are evaluated
- output is sufficient to make the next delegation decision on its own
- at least one `[critical]` assertion is identified

## Scenarios

### Scenario A: Text task that does not require reading the repository

Writing or organizing text such as a design proposal or email — a coding agent is unnecessary. Recommend standard chat.

Requirements checklist:
1. [critical] A heavy coding agent is not the default recommendation for tasks that do not require reading the repository
2. The recommended tool and its rationale correspond
3. The minimum context to pass is narrowed down

### Scenario B: Multi-file change with high-risk judgment

The task involves implementation and tests, plus security or breaking-change concerns. Justify using a high-capability model explicitly.

Requirements checklist:
1. [critical] The rationale for choosing the heavier option is expressed in one line
2. High-risk elements are not forced into a lightweight option
3. The task unit does not become excessively broad
4. `Recommended tool` names a specific tool
5. `Recommended model / profile` names a specific model or profile
6. Tool selection rationale and model/profile selection rationale correspond

### Scenario C: Learning-priority implementation consultation

An unfamiliar domain implementation consultation where understanding is more important than deadline. Separate what to delegate to AI from what the user must review and decide.

Requirements checklist:
1. [critical] Learning-priority vs. deadline-priority is included as a judgment axis
2. The scope the user can review and the scope delegated to AI are clearly separated
3. Prerequisites for understanding and reviewing the output are present in the output

### Scenario D: Boundary — learning is the priority, not speed

A user explicitly says they want to understand the implementation rather than just get working code. The output must not push full delegation.

Requirements checklist:
1. [critical] Does not recommend delegating everything to AI when the user states a learning goal
2. Output includes guidance on what to understand

## Failure Pattern Ledger

- `heavy agent recommended by default`
- `model choice lacks rationale`
- `context not minimized`
- `tool or profile selection remains generic`
- `learning goal ignored`
