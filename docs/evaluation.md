# Skill Evaluation

This document defines how this repository selects, runs, records, and reviews Skill evaluations.

The objective is to obtain the least evidence needed to decide whether a change is acceptable.\
Evaluation is not an automatic action after every edit, and an ordinary Skill change does not require every case, a baseline, repeated runs, or a client matrix.

## Evaluation workflow

Use these steps for a Skill change:

1. Identify the changed claim or responsibility.
2. Select the least sufficient evaluation path from the table below.
3. Select only cases that can expose the changed responsibility, a known regression, or a plausibly affected adjacent boundary.
4. Generate a plan and inspect its model-call count before execution.
5. Run the approved plan once.
6. Grade only the planned case-condition results.
7. Record the stopping reason and any unverified boundary.
8. Add evidence only when the current result is not decision-ready.

Do not connect the Runner to a file watcher, post-edit hook, or other mechanism that automatically evaluates every revision.\
The developer or reviewing agent invokes it explicitly when the selected path requires execution.

## Select an evaluation path

| Change shape | Path | Required evidence |
| --- | --- | --- |
| Documentation, formatting, meaning-preserving wording, or mechanical metadata that does not affect discovery | `static-only` | Repository checker only |
| Localized instruction, output, safety, or other runtime-responsibility change | `targeted-candidate` | The affected candidate cases, once initially |
| `name`, `description`, invocation behavior, or adjacent Skill responsibility boundary change | `targeted-routing` | Relevant trigger, non-trigger, near-miss, ambiguous, or coexistence cases |
| Known regression, major redesign, changed success contract, or ambiguous candidate-only result | `baseline-comparison` | Matched candidate plus `baseline` or `without-skill` conditions for the decision-relevant cases |
| Explicit environment-support claim or environment-specific failure | `target-environment` | Direct execution in the affected environment |

Repetition is an escalation, not a separate default path.\
Repeat only when observed instability, conflicting evidence, or a material failure consequence makes another observation decision-relevant.

Package and distribution checks remain separate from routine Skill behavior evaluation.\
Run them only when distribution behavior changes.

## Evaluation assets

Reusable assets live with the Skill:

```text
skills/<skill-name>/
└── evals/
    ├── README.md       # human-readable evaluation contract
    ├── evals.json      # optional behavior cases
    ├── triggers.json   # optional routing cases
    ├── report.json     # optional record for the latest evaluated change
    └── results.json    # optional legacy historical evidence
```

Do not add a structured asset until it makes a repeated evaluation more reproducible.\
Do not migrate existing assets merely to make their shapes uniform.

### Behavior case formats

The Runner accepts the repository's current case shape:

```json
{
  "schema_version": 1,
  "skill": "example-skill",
  "cases": [
    {
      "id": "bounded-change",
      "input": "Handle this request.",
      "assertions": ["bounded-output"]
    }
  ]
}
```

It also accepts the minimal official-style evaluation shape for `evals.json`:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Handle this request.",
      "expected_output": "A bounded result.",
      "files": []
    }
  ]
}
```

String and integer IDs are normalized to strings.\
The Runner currently consumes `prompt`, optional `expected_output`, and optional `files` from this shape.\
Keep executor input separate from assertions and expected output so the desired answer is not disclosed to the executor.

For current repository cases, the adapter also accepts `input`, `turns`, conversation context, `assertion_ids`, and inline `fixture.files`.\
It serializes multiple turns into one explicit transcript so one case-condition pair still consumes one executor call; this checks the final response with the supplied context and is not evidence for responses that would have occurred between turns.\
Repository-relative `files` are copied under `inputs/`, while inline fixture files preserve their declared paths in the disposable fixture.\
A named fixture without inline contents is rejected before execution because the Runner cannot reconstruct it safely.

Use `triggers.json` for routing cases in the repository's current `{skill, cases}` shape.\
Routing evaluation counts a Skill load only from a path or command field exposed by Codex JSONL events.\
When loading is not observable, record `not_exposed`; do not infer selection from the final response wording.

## Plan before spending tokens

Create a temporary directory and generate a plan from the repository root:

```bash
evaluation_tmp="$(mktemp -d)"

python3 scripts/run_skill_evaluation.py plan \
  --skill example-skill \
  --path targeted-candidate \
  --purpose "Check the changed output boundary." \
  --affected "output boundary" \
  --case bounded-change \
  --base-ref origin/main \
  --output "$evaluation_tmp/plan.json"
```

`plan` does not invoke a model.\
It resolves the base commit, records hashes for changed Skill files and the selected case asset, expands only explicitly selected cases and conditions, and prints the estimated model-call count.\
The temporary plan retains the selected assertion definitions, expected output, and additional grading requirements for the caller, but the executor prompt contains only the normalized case input.

Model-backed paths require at least one `--case`.\
There is no implicit all-cases option.

The default condition is `candidate`.\
`baseline-comparison` defaults to `candidate` plus `baseline` and may instead receive explicit `--condition` values, including `without-skill`.\
Other paths do not accept comparison conditions.

The default model is `gpt-5.6-sol`, the default reasoning effort is `high`, and the default sandbox is `read-only`.\
Override these inputs explicitly when the evaluation question requires another environment.

## Execute the approved plan

Run the plan with an explicit budget:

```bash
python3 scripts/run_skill_evaluation.py run \
  --plan "$evaluation_tmp/plan.json" \
  --artifacts-dir "$evaluation_tmp/artifacts" \
  --execute \
  --max-model-calls 1
```

`run` refuses to start when the plan exceeds `--max-model-calls`.\
The artifacts directory must not already exist, which prevents an earlier execution from being silently overwritten or mixed into the new result.

Every Codex invocation uses an ephemeral session, JSONL output, the planned model, reasoning effort, and sandbox, and a disposable fixture under the system temporary directory.\
The candidate condition copies the working-tree Skill, the baseline condition materializes the Skill from the resolved base commit, and the without-Skill condition omits the target Skill.\
Candidate, baseline, and companion copies exclude `evals/` so hidden assertions and expected outputs are not available to the executor.\
Only companion Skills declared by the evaluation asset are copied alongside it.

Behavior evaluation explicitly tells the executor to use the target Skill.\
Routing evaluation supplies the request without forcing Skill selection.

The Runner executes the deterministic repository checker once before model calls.\
During that check it ignores only the previous `report.json` for the Skill being evaluated, because that report is expected to become stale when the Skill changes.\
Normal repository validation does not ignore the report.

Raw JSONL, stderr, final responses, disposable fixtures, the plan, and the run record remain under the system temporary directory.\
Do not commit them.

## Grade planned results

The Runner does not use another model as an automatic grader.\
The invoking Codex session or a human grades the planned outputs against the case assertions and writes a small temporary JSON file:

```json
{
  "schema_version": 1,
  "results": [
    {
      "case_id": "bounded-change",
      "condition": "candidate",
      "status": "pass",
      "requirements": [
        {
          "id": "bounded-output",
          "status": "pass",
          "evidence": "The result states the boundary and does not expand the task."
        }
      ],
      "evidence": "All selected requirements passed."
    }
  ]
}
```

Allowed statuses are `pass`, `fail`, `inconclusive`, and `error`.\
Grades must exactly match completed case-condition pairs; missing, duplicate, and unplanned results are rejected.\
When a case assigns assertion IDs, the grade must include each assigned assertion exactly once.\
Executor failures become `error` results without requiring fabricated grading evidence.

Keep evidence concise and decision-relevant.\
Do not paste a full prompt, response, trace, stderr, JSONL event, credential, or environment-specific absolute path into grades.

## Preview and write the report

Preview the compact report before changing the repository:

```bash
python3 scripts/run_skill_evaluation.py report \
  --plan "$evaluation_tmp/plan.json" \
  --run "$evaluation_tmp/artifacts/run.json" \
  --grades "$evaluation_tmp/grades.json" \
  --stopping-reason "The selected case answered the acceptance question." \
  --unverified "Unselected responsibilities"
```

Add `--write` only after reviewing the preview.\
The command then replaces `skills/<skill-name>/evals/report.json`.

`report.json` records:

- the evaluation purpose and affected responsibilities
- the selected path, cases, and conditions
- the resolved base commit and hashes of evaluated candidate files
- the Codex client, model, reasoning effort, and sandbox
- deterministic and graded results
- the aggregate status, stopping reason, and unverified boundaries

The aggregate status uses `error`, `fail`, `inconclusive`, then `pass` precedence.\
The repository checker verifies that the summary matches the result statuses and that the evaluated file hashes remain current.

The report describes one change-scoped evaluation, not the quality of the entire Skill.\
It omits unselected cases rather than marking them stale or not executed.\
The next evaluated change replaces this file, while Git history retains earlier accepted records.

`results.json` remains valid legacy historical evidence.\
The repository checker validates its basic JSON identity but does not require its candidate hashes to match the current Skill.\
Do not refresh or migrate a legacy result merely because another part of the Skill changed.

## Stop and escalate

Stop after one observation per selected candidate case when the result answers the acceptance question, all material selected requirements are graded, and the remaining unverified scope is explicit.

Add only the evidence needed to resolve one of these conditions:

- a selected requirement is ungraded
- the case or grading rule is defective
- candidate evidence is ambiguous or conflicts with another observation
- an observed instability makes repetition decision-relevant
- acceptance depends on comparison with the prior Skill or no-Skill behavior
- a material environment-specific claim remains untested

Do not edit the Skill merely to repair a defective case or grader.\
Correct the evaluation input first.

## Review evaluation sufficiency

A reviewer decides whether the selected evidence covers the changed responsibility.\
The checker can establish record integrity, but it cannot decide semantic sufficiency.

An evaluation-insufficiency finding must identify all of the following:

- the changed responsibility that lacks coverage
- a concrete plausible failure that matters to acceptance
- why the recorded checks cannot expose that failure
- the smallest additional case, condition, or deterministic check that would resolve it

Do not report insufficiency merely because an unselected case, unrelated suite, legacy `results.json`, or prior report was not refreshed.\
Do not require a fixed case count, baseline, repetition, Skill-without condition, or model matrix without connecting it to a decision-relevant failure.

## Repository checks

Run the complete deterministic validation after writing a report or changing evaluation assets:

```bash
python3 scripts/check_repository.py
python3 -m unittest discover -s tests
```

The checker validates structure and record consistency without invoking an LLM.\
Passing static validation does not establish runtime quality, routing, or support in an untested client.
