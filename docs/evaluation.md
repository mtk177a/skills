# Skill Evaluation

This document describes the evaluation format used for Skills in this repository and how to run evaluations.

## Evaluation assets per Skill

Each Skill that has been evaluated contains an `evals/` directory:

```
skills/<skill-name>/
└── evals/
    ├── evals.json       # behavior test cases
    ├── triggers.json    # trigger detection test cases
    └── README.md        # assertions, results, open items
```

## evals.json format

Each entry in `evals.json` defines one behavior test case.

```json
[
  {
    "id": "basic-use-case",
    "description": "Representative use of the Skill",
    "input": "...",
    "assertions": [
      { "type": "contains", "value": "expected phrase" },
      { "type": "not_contains", "value": "phrase that must not appear" }
    ],
    "tags": ["representative"]
  },
  {
    "id": "boundary-case",
    "description": "Edge condition the Skill must handle correctly",
    "input": "...",
    "assertions": [...],
    "tags": ["boundary"]
  }
]
```

Minimum per Skill: 2 representative cases + 1 boundary case.

## triggers.json format

Each entry in `triggers.json` defines a trigger detection case.

```json
{
  "should_trigger": [
    { "input": "a prompt that should invoke this Skill", "reason": "why" }
  ],
  "should_not_trigger": [
    { "input": "a prompt that must not invoke this Skill", "reason": "why" }
  ]
}
```

## evals/README.md format

Record the following after each evaluation run:

```markdown
## Iter N — YYYY-MM-DD

### Assertions
- [critical] <assertion that determines pass/fail>
- <other assertions>

### Results
- Pass: <list of passing cases>
- Fail: <list of failing cases with details>

### Open items
- <anything not yet verified>
```

## Running evaluations

Use the primary evaluator with a blank-slate subagent:

```bash
# Run behavior eval for a single Skill
<evaluator command> skills/<skill-name>/evals/evals.json

# Run trigger eval
<evaluator command> --triggers skills/<skill-name>/evals/triggers.json
```

Exact commands depend on the evaluator in use. See `docs/compatibility.md` for tool references.

## Baseline comparison

When significantly revising a Skill, record the before/after result comparison in `evals/README.md` to confirm the change is an improvement and did not regress other cases.

## Iter 0 static check

Before writing runnable eval cases, perform a static Iter 0 check:

1. `description` and body are internally consistent
2. Output format is defined or clearly implied
3. The Skill is self-contained (does not assume another Skill or agent as a dependency)
4. At least one `[critical]` assertion is identified

Only after Iter 0 passes should you formalize `evals.json` and `triggers.json`.
