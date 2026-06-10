# Skill Evaluation

This document describes the evaluation approach used for Skills in this repository.

## Evaluation assets per Skill

Each Skill has an `evals/` directory:

```
skills/<skill-name>/
└── evals/
    └── README.md    # Iter 0 check, scenarios, execution results, reflection
```

## evals/README.md structure

```markdown
# <skill-name> evals

## Iter 0 — Static check

- description and body are internally consistent
- output format is defined or clearly implied
- the Skill is self-contained
- at least one `[critical]` assertion is identified

## Scenarios

### Scenario A: <title>

<one-sentence context>

Requirements checklist:
1. [critical] <critical requirement>
2. <other requirements>

## Failure Pattern Ledger

- `<known failure pattern>`

## Iter N — YYYY-MM-DD

### Changes
- <what changed from previous>

### Execution results

| Scenario | Result | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|
| A | ○ | N/A | N/A | 0 | — |

### Structured reflection

- Scenario A:
  - Issue: ...
  - Cause: ...
  - General Fix Rule: ...

### Ledger updates

- Re-seen: `pattern`
- Added: `pattern`

### Next fix proposal

- <proposal>
```

## Running evaluations

Evaluations are run manually using a blank-slate subagent: an agent that starts with no context about this repository and receives only the Skill and the scenario description as input.

**Blank-slate executor protocol:**
1. Spawn a fresh subagent with no repository context
2. Provide the SKILL.md content and the scenario description
3. Observe whether the output satisfies each item in the requirements checklist
4. Record results honestly — mark as "not yet executed" if the run was not performed

The evaluator's role is to check behavior reproducibility, not to render a subjective judgment.

This approach is inspired by the empirical prompt-tuning methodology described in [mizchi/skills](https://github.com/mizchi/skills). See `THIRD_PARTY_NOTICES.md`.

## Iter 0 static check

Before writing scenarios, perform a static Iter 0 check:

1. `description` and body are internally consistent
2. Output format is defined or clearly implied
3. The Skill is self-contained (does not assume another Skill or agent as a dependency)
4. At least one `[critical]` assertion is identified

Only after Iter 0 passes should you formalize scenarios in `evals/README.md`.

## Baseline comparison

When significantly revising a Skill, record a before/after comparison in `evals/README.md` to confirm the change is an improvement and did not regress existing scenarios.
