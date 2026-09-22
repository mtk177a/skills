# Skill Evaluation

This document defines how this repository selects, runs, records, migrates, and reviews Skill evaluations.

The objective is to obtain the least evidence needed to decide whether a change is acceptable.\
Evaluation is not an automatic action after every edit, and an ordinary Skill change does not require every case, a baseline, repeated runs, or a client matrix.

## Evaluation workflow

Use these steps for a Skill change:

1. Identify the changed claim or responsibility.
2. Decide whether the Skill needs new executable evaluation definitions or has definitions that must be migrated.
3. Select the least sufficient evaluation path.
4. Select only cases that can expose the changed responsibility, a known regression, or a plausibly affected adjacent boundary.
5. Generate a plan and inspect its model-call count before execution.
6. Run the approved plan once.
7. Grade only the planned case-condition results.
8. Record the stopping reason and any unverified boundary.
9. Add evidence only when the current result is not decision-ready.

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

## Migrate existing definitions per Skill

Existing evaluation assets are not migrated repository-wide.\
During the Issue #49 audit, migrate each Skill's complete existing `evals.json` and `triggers.json` set in its Sub Issue, whether or not its instructions or runtime behavior change.\
Outside that audit, migrate a still-legacy set when a pull request first materially changes the Skill's `SKILL.md`, runtime resources, discovery behavior, responsibility, safety boundary, or evaluation definition.

Outside the audit, README changes, reference-translation synchronization, meaning-preserving documentation or metadata changes, and legacy-result-only changes do not independently trigger migration.\
If both `evals.json` and `triggers.json` exist for a Skill, migrate both in the same pull request so the Skill never has a mixed executable contract.

If only one definition file exists, migrate that file and create another only when a changed responsibility needs its evaluation path.\
When a change requires model-backed evaluation and the Skill has no executable definitions for the affected responsibility, create the needed behavior or routing definitions in the executable format before running the evaluation.\
Do not create definitions solely to perform a migration.

### Migration examples

If both definitions exist in the legacy format, migrate both in the same change.

Before migration, `evals.json` may contain:

```json
{
  "skill": "example-skill",
  "version": 1,
  "cases": [
    {
      "id": "behavior",
      "prompt": "Handle this request."
    }
  ]
}
```

Before migration, `triggers.json` may contain:

```json
{
  "skill": "example-skill",
  "version": 1,
  "cases": [
    {
      "id": "route",
      "prompt": "Handle this request.",
      "expected_handler": "example-skill"
    }
  ]
}
```

After migration, `evals.json` uses the executable behavior format:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "behavior",
      "prompt": "Handle this request.",
      "expected_output": "A bounded result."
    }
  ]
}
```

After migration, `triggers.json` uses the executable routing format:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "route",
      "prompt": "Handle this request.",
      "expected_handlers": ["example-skill"]
    }
  ]
}
```

If only a legacy `triggers.json` exists, migrate that file and do not create `evals.json`.

Before migration:

```json
{
  "skill": "example-skill",
  "version": 1,
  "cases": [
    {
      "id": "route",
      "prompt": "Handle this request.",
      "expected_handler": "example-skill"
    }
  ]
}
```

After migration:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "route",
      "prompt": "Handle this request.",
      "expected_handlers": ["example-skill"]
    }
  ]
}
```

If the Skill has no executable definitions and the change needs only static validation, leave that state unchanged.

Before migration:

```text
skills/example-skill/evals/
└── README.md
```

After migration:

```text
skills/example-skill/evals/
└── README.md
```

Migrating definitions does not mean executing every migrated case.\
If the Skill's runtime behavior and discovery are unchanged, use static validation; otherwise run only the cases required by the responsibility changed in that pull request.

Legacy `{skill, cases}` assets, `scenarios` assets, and legacy `triggers.json` remain valid repository history.\
Model-backed paths reject them before invoking Codex and explain that complete per-Skill migration is required.\
`static-only` does not read evaluation cases and remains available to an unmigrated Skill.

## Evaluation assets and schema

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

### What to record in `evals/README.md`

Use `evals/README.md` to explain the evaluation's intent, scope, method, and evidence to a human reader.\
Do not duplicate the case payloads or other machine-readable details already defined in JSON.

The README should cover the applicable information below:

1. The evaluation purpose and the Skill responsibility being examined.
2. The role of each present asset, such as `evals.json`, `triggers.json`, `report.json`, or `results.json`.
3. Static checks of the Skill instructions or bundled structure.
4. A coverage map connecting each responsibility or boundary to a plausible failure, the case or check that can expose it, and the grading method.
5. When needed, the execution and grading procedure, including isolation, comparison conditions, and repetition or stopping conditions.
6. Current evidence, including the evaluated revision, environment, selected cases, results, and anything not executed.
7. Unverified boundaries and the condition that would make further evaluation useful.

The following is a suggested structure, not a required heading template:

```markdown
# <skill-name> evals

## Purpose

State the responsibility and evaluation decision this suite supports.

## Assets

Describe the role of each evaluation asset that exists.

## Static checks

List the instruction or package properties checked without model execution.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

## Execution and grading

Describe only the procedure, isolation, comparison, and stopping rules that apply.

## Current evidence

Record the revision, environment, selected cases, results, and unexecuted checks.

## Unverified boundaries

State what remains unverified and when another evaluation would be decision-relevant.
```

Use different headings when they better fit the evidence, and omit sections that do not apply.\
A failure-pattern ledger or next-validation question is optional and should appear only when it helps interpret or extend the evidence.\
The repository checker does not enforce README headings or structure.\
Existing READMEs do not require bulk migration; apply this guidance when an evaluation definition or its README is materially updated.

### Base fields and repository extensions

The executable contract adopts the fields shown in the [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills) and adds the repository-specific fields and forms listed below.\
The required, conditional, and optional labels describe this repository's executable contract rather than a universal Agent Skills JSON schema.

| Origin | Location | Field or form | Requirement in this repository | Purpose |
| --- | --- | --- | --- | --- |
| Agent Skills base | Top level | `skill_name` | Required | Identifies the Skill under evaluation. |
| Agent Skills base | Top level | `evals` | Required | Contains the evaluation cases. |
| Agent Skills base | Case | `id` | Required | Identifies the case and is normalized to a string. |
| Agent Skills base | Case | `prompt` | Conditional | Supplies the request for the single-request form and the current request in the repository-specific `conversation` form. |
| Agent Skills base | Case | `expected_output` | Optional; required for a behavior case when it has no assertions | Describes a successful result; supplies the default grading requirement only when `assertions` is empty or absent. |
| Agent Skills base | Case | `files` | Optional | Selects repository-relative input files. |
| Repository extension | Case | `baseline_files` | Optional | Commits previous text for selected inline fixture files in a disposable Git repository before writing their current versions. |
| Agent Skills base | Case | String entries in `assertions` | Optional; behavior cases require `assertions` or `expected_output` | Defines grading statements in the base string representation. |
| Repository extension | Top level | `execution.coexistence_skills` | Optional | Adds Skills that must be installed for every selected case. |
| Repository extension | Case | `title` | Optional | Preserves a human-readable case title in the normalized plan. |
| Repository extension | Case | `turns` | Conditional alternative input form | Supplies a complete conversation as the evaluation input. |
| Repository extension | Case | `authoring_turns` plus `request` | Conditional alternative input form | Separates prior artifact-authoring history from the current request. |
| Repository extension | Case | `conversation` plus `prompt` | Conditional alternative input form | Separates completed conversation context from the current request; `prompt` itself remains a base field. |
| Repository extension | Case | Object entries in `assertions` with `id`, `text`, and `critical` | Optional | Adds stable assertion identity and criticality to the base assertion field. |
| Repository extension | Case | `fixture` | Optional | Materializes inline fixture files. |
| Repository extension | Case | `coexistence_skills` | Optional | Adds Skills for one case. |
| Repository extension | Case | `conditions` | Optional | Restricts the case to selected `candidate`, `baseline`, or `without-skill` conditions. |
| Repository extension | Routing definition | `triggers.json` with case-level `expected_handlers` | `expected_handlers` is required for every routing case | Reuses the executable envelope for routing expectations, including an empty handler list. |

New executable definitions follow the [Agent Skills evaluation format](https://agentskills.io/skill-creation/evaluating-skills) with explicit repository extensions:

```json
{
  "skill_name": "example-skill",
  "execution": {
    "coexistence_skills": ["adjacent-skill"]
  },
  "evals": [
    {
      "id": 1,
      "title": "Keep the change bounded",
      "prompt": "Handle this request.",
      "expected_output": "A bounded result.",
      "files": ["tests/fixtures/input.txt"],
      "assertions": [
        "The result states the boundary.",
        {
          "id": "no-expansion",
          "text": "The result does not expand the task.",
          "critical": false
        }
      ],
      "fixture": {
        "files": {
          "notes/context.txt": "Fixture content."
        }
      },
      "coexistence_skills": [],
      "conditions": ["candidate"]
    }
  ]
}
```

The top level accepts only `skill_name`, `evals`, and the optional `execution` object.\
`execution` accepts only `coexistence_skills`.\
Every nested object is also closed: unknown fields are rejected instead of being ignored.

A case accepts only `id`, `title`, the input fields described below, `expected_output`, `files`, `assertions`, `fixture`, `coexistence_skills`, `conditions`, and `expected_handlers`.\
`id` is required, and string and integer IDs are normalized to strings.\
`title` is optional descriptive metadata, must be a non-empty string, and is preserved in the normalized plan.

## Case input forms

Every case must use exactly one of these four input forms:

| Form | Required input fields | Meaning |
| --- | --- | --- |
| Single request | `prompt` | One standalone current user request |
| Whole transcript | `turns` | The complete conversation supplied as the evaluation input |
| Authoring history and request | `authoring_turns` plus `request` | Prior artifact-authoring history kept distinct from the current request |
| Conversation and prompt | `conversation` plus `prompt` | Prior completed context kept distinct from the current request |

The following cases show the four forms without their grading fields:

```json
[
  {
    "id": "single",
    "prompt": "Handle this request."
  },
  {
    "id": "transcript",
    "turns": [
      {"role": "user", "content": "Start the task."},
      {"role": "assistant", "content": "What should I preserve?"},
      "Preserve the existing boundary."
    ]
  },
  {
    "id": "authoring",
    "authoring_turns": ["Draft the document."],
    "request": "Review it with fresh eyes."
  },
  {
    "id": "continued",
    "conversation": ["We selected option A."],
    "prompt": "Continue the implementation."
  }
]
```

`turns`, `authoring_turns`, and `conversation` must be non-empty arrays.\
Each entry is either a non-empty string, which represents a user turn, or an object containing exactly `role` and `content`.\
The only accepted roles are `user` and `assistant`.

Do not combine the forms or supply only one member of a required pair.\
For example, `prompt` plus `turns`, `request` without `authoring_turns`, and `conversation` without `prompt` are invalid.

## Case grading and execution fields

A behavior case in `evals.json` requires at least one non-empty assertion or a non-empty `expected_output`.\
When `assertions` is empty or absent, the Runner creates one critical `expected-output` requirement from `expected_output`.\
When both fields are present and `assertions` is non-empty, only `assertions` becomes grading requirements; `expected_output` remains a description of success in the definition.

An assertion is either a non-empty string or an object containing exactly a non-empty `id`, non-empty `text`, and boolean `critical`.\
A string assertion receives a stable positional ID such as `assertion-1` and is critical by default.\
Assertion IDs must be unique within the case.

A routing case in `triggers.json` requires `expected_handlers` as an array of unique Skill names and must not use it in `evals.json`.\
An empty `expected_handlers` array is valid and means that no Skill should handle the request.\
Routing cases may also contain assertions or `expected_output` for their non-routing requirements.

A minimal routing definition is:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "non-trigger",
      "prompt": "Answer an unrelated request.",
      "expected_handlers": []
    }
  ]
}
```

`conditions`, when present, must include `candidate` and may also contain `baseline` and `without-skill`, with no duplicates.\
Execution-level and case-level `coexistence_skills` contain Skill names, with no duplicates within either array.\
`fixture` contains exactly a `files` object that maps safe relative paths to string contents; named fixtures are not executable until their files are materialized inline.

Each `files` entry must be a repository-relative path using `/` separators.\
The shared contract rejects empty paths, NUL characters, absolute or Windows drive paths, backslashes, parent-directory traversal, and paths that collide after normalization.\
Inline fixture paths additionally cannot target `.agents/` or `.git/`, or use one location as both a file and a directory.\
`files` entries are materialized under `fixture/inputs/` and `fixture.files` entries under `fixture/`; combinations whose final destinations are equal or in an ancestor-descendant relationship are rejected.\
For repository-local evaluations, a `fixture.files` path is also rejected if it equals, falls inside, or is an ancestor of an installed companion's `skills/<skill-name>/` directory, whether the companion is declared for the whole definition or for one case.

Keep executor input separate from assertions and expected output so the desired answer is not disclosed to the executor.

The repository checker and Runner use this same contract.\
Both statically check that every `files` entry and every top-level or case-level `coexistence_skills` reference exists, including references in unselected cases and in a sibling executable definition loaded by the Runner.\
Referenced input files must be regular files inside the repository, and referenced Skills must have a regular `SKILL.md`; symlinked paths are rejected.\
The Runner separately checks manifests and selected execution inputs when creating and loading a plan.\
Invalid definitions fail before a model is invoked, including unknown fields, unsupported input combinations, invalid nested objects, unsafe paths, missing references, normalized ID collisions, and duplicates in set-like arrays.

Routing evaluation counts only successful read or tool events for installed Skills that Codex exposes in JSONL.\
The Runner treats the routing event stream as complete only when it contains `turn.completed`.\
A complete stream with no successful Skill read records `observed` with an empty handler array, which can pass a case whose `expected_handlers` is empty.\
Without `turn.completed`, the Runner records `not_exposed` and grades routing as `inconclusive`; it never infers a handler from the final response wording.

## Plan before spending tokens

The default `--skill-source public` reads `skills/<skill-name>/`.\
For an explicitly tracked repository-local Skill, use `--skill-source repository-local` to read `.agents/skills/<skill-name>/`; the Runner rejects untracked directories.\
Its companion Skills remain public `skills/<skill-name>/` sources and are copied both to Codex's Skill directory and to their repository paths in the disposable fixture.\
Before a repository-local model call, the Runner checks that the full candidate and installed companion descriptions are visible only at their fixture paths.\
It also rejects a personal required companion when the fixture intentionally omits it.\
The check uses the normal authentication context with per-invocation configuration that disables personal same-name Skills and plugins; it does not change personal configuration or credentials.

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
It resolves the base commit, expands only explicitly selected cases and conditions, prints the estimated model-call count, and writes schema version 3 with a digest over canonical JSON.

The plan records every regular candidate file that the executor can receive, excluding `evals/`, with its SHA-256 and normalized Git mode of `100644` or `100755`.\
Evaluation files, selected repository input files, and complete coexistence Skill manifests are recorded separately.\
Each planned execution records the union of execution-level and case-level `coexistence_skills`; the plan-level list is the union across selected executions and binds their manifests.\
Symlinks in Skill execution trees are rejected, and files outside these manifests are never copied into the fixture.

Model-backed paths require at least one `--case`; there is no implicit all-cases option.\
The default condition is `candidate`.\
`baseline-comparison` defaults to `candidate` plus `baseline` and may instead receive explicit `--condition` values, including `without-skill`.\
Other paths do not accept comparison conditions.

The default model is `gpt-5.6-luna`, the default reasoning effort is `max`, and the default sandbox is `read-only`.\
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

`run` refuses to start when the plan exceeds `--max-model-calls` or any recorded candidate, evaluation input, case input, or coexistence Skill manifest has changed, including an executable-mode change.\
These checks happen before Codex is invoked.\
The artifacts directory must not already exist.

Every Codex invocation uses an ephemeral session, JSONL output, the planned model, reasoning effort, and sandbox, and a disposable fixture under the system temporary directory.\
The candidate condition copies the manifest-bound working-tree Skill, the baseline condition materializes regular files from the resolved base commit, and both reproduce the normalized executable mode.\
The baseline condition rejects symlinks and other unsupported Git tree entries, while the without-Skill condition omits the target Skill.\
Candidate and companion copies exclude `evals/`.\
Each execution copies only its own planned coexistence Skills; routing observations use that same installed set.

Selected case inputs are copied to `fixture/inputs/<repository-relative-path>`.\
The Runner checks the source and destination again before copying, so a case input cannot overwrite its repository source.

Behavior evaluation explicitly tells the executor to use the target Skill.\
Routing evaluation supplies the request without forcing Skill selection.

The schema version 2 `run.json` embeds the normalized plan and its digest instead of an absolute plan path.\
It also records the actual execution pairs, environment, static-check outcome, routing observations, and raw-artifact locations within the temporary artifact directory.

Raw JSONL, stderr, final responses, disposable fixtures, the plan, and the run record remain under the system temporary directory.\
Do not commit them.

## Grade planned results

The Runner does not use another model as an automatic grader.\
The invoking Codex session or a human writes schema version 2 grades for the non-routing requirements:

```json
{
  "schema_version": 2,
  "results": [
    {
      "case_id": "bounded-change",
      "condition": "candidate",
      "requirements": [
        {
          "id": "expected-output",
          "status": "pass",
          "evidence": "The result states the boundary without expanding the task."
        }
      ],
      "evidence": "The selected requirement passed."
    }
  ]
}
```

Do not provide a case-level status.\
The Runner derives it from requirement statuses and the critical flags in the bound plan:

1. An executor or requirement `error` produces `error`.
2. A critical `fail` produces `fail`.
3. A non-critical `fail` or any `inconclusive` produces `inconclusive`.
4. All requirements passing produces `pass`.

The Runner adds and grades the critical `routing-handlers` requirement from direct observations, so grades do not repeat it.\
Grades must exactly match completed case-condition pairs and non-routing requirements; missing, duplicate, and unplanned results are rejected.

Keep evidence concise and decision-relevant.\
Do not paste a full prompt, response, trace, stderr, JSONL event, credential, or environment-specific absolute path into grades.

## Preview and write the report

Preview the compact report before changing the repository:

```bash
python3 scripts/run_skill_evaluation.py report \
  --run "$evaluation_tmp/artifacts/run.json" \
  --grades "$evaluation_tmp/grades.json" \
  --stopping-reason "The selected case answered the acceptance question." \
  --unverified "Unselected responsibilities"
```

`report` accepts no separate plan.\
It uses the plan snapshot embedded in `run.json` as the only plan source and revalidates its digest, environment, execution pairs, candidate manifest, and evaluation inputs.

Add `--write` only after reviewing the preview.\
The command then replaces `skills/<skill-name>/evals/report.json` with schema version 2.

The report records the evaluation purpose, affected responsibilities, selected path and pairs, base commit, candidate manifest with hashes and modes, selected evaluation-input hashes, execution environment, derived results, stopping reason, and unverified boundaries.\
It does not include the plan snapshot, raw prompts, responses, JSONL, absolute paths, credentials, or coexistence Skill manifests.

The checker recomputes result and summary statuses and verifies that the target Skill and selected evaluation inputs remain current.\
A later unrelated change to a coexistence Skill does not make the accepted report stale.

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

Do not report insufficiency merely because an unselected case, unrelated suite, unmigrated Skill, legacy `results.json`, or prior report was not refreshed.\
Do not require a fixed case count, baseline, repetition, Skill-without condition, or model matrix without connecting it to a decision-relevant failure.

## Repository checks

Run the complete deterministic validation after writing a report or changing evaluation assets:

```bash
python3 scripts/check_repository.py
python3 -m unittest discover -s tests
```

The checker validates structure, mixed-format migration state, manifest content and executable-mode freshness, symlink absence in the candidate execution tree, and record consistency without invoking an LLM.\
Passing static validation does not establish runtime quality, routing, or support in an untested client.
