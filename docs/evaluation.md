# Skill Evaluation

This document describes the evaluation approach used for Skills in this repository.

## Evaluation assets per Skill

Each Skill has an `evals/` directory. The README is required; structured assets are optional and should be added when they make repeated evaluation more reproducible.

```
skills/<skill-name>/
└── evals/
    ├── README.md       # purpose, procedure, result summary, and reflection
    ├── triggers.json   # optional trigger, non-trigger, and near-miss cases
    └── evals.json      # optional realistic tasks, inputs, assertions, and baseline conditions
```

Do not migrate every existing Skill merely to match this structure. The other 26 Skills may adopt structured assets when each receives its next significant revision.

## Asset responsibilities

### evals/README.md

Keep the human-readable evaluation contract and summarized record:

- purpose and intended behavior
- execution procedure and environment
- static checks and scenario overview
- summarized results, failures, and unexecuted checks
- iteration notes and the next validation question

The exact headings may vary. Do not use the README as a substitute for raw evidence, and do not commit raw traces into it.

### evals/triggers.json

Use this optional asset for reusable:

- `should-trigger` cases
- `should-not-trigger` cases
- near-miss cases that resemble the target responsibility but belong elsewhere
- run counts, observability rules, and pass thresholds

Run trigger cases more than once. Record client, model, date, and run count because trigger behavior can vary across environments and runs.

Count a trigger only from evidence the client exposes. If Skill loading is not observable, record `not exposed`; do not infer a load event from output wording.

### evals/evals.json

Use this optional asset for:

- realistic tasks and their inputs
- behavioral assertions and critical requirements
- baseline conditions
- isolation and coexistence configurations

Keep scenarios rich enough to expose judgment errors without embedding the desired answer in the task.

## Example evals/README.md structure

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

Run evaluations with a blank-slate executor: an agent or client session that starts without repository history and receives only the inputs required by the scenario.

**Blank-slate executor protocol:**

1. Start a fresh executor with no repository context.
2. Provide the SKILL.md content and the scenario description
3. Observe whether the output satisfies each item in the requirements checklist
4. Record results honestly

Evaluate both:

- **Isolation:** the target Skill without adjacent Skills that could mask a gap
- **Coexistence:** the target Skill with adjacent Skills or instruction surfaces that are present in normal use

Record an unavailable observation as `not exposed` and a skipped run as `not executed`. Neither status counts as a pass.

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

When significantly revising a Skill, compare the candidate with the previous version or with no Skill if the previous version is unavailable. Use the same task inputs, client, model, reasoning settings, and environment for both sides. A significant revision is not complete merely because the candidate passes in isolation; compare it with the baseline and check coexistence.

## Result metadata and artifact handling

Record:

- client, model, reasoning settings, and date
- run count and trigger rate
- assertion results with supporting evidence
- isolation and coexistence configuration
- token and duration values when the client exposes them
- `not executed` and `not exposed` items

Store raw JSONL, authentication material, and full session logs only in a temporary directory outside the repository. Do not commit credentials, raw sessions, or unredacted traces.
