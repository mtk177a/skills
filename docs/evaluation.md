# Skill Evaluation

This document describes the evaluation approach used for Skills in this repository.

## Evaluation selection principle

Select the least evidence needed to decide whether a change is acceptable. Start
with deterministic repository validation. Add model-backed behavior evaluation
only when executable behavior, discovery, or a responsibility boundary changes,
and select only the cases that can expose the affected responsibility, a known
regression, or a plausibly affected adjacent boundary.

A changed `SKILL.md` file does not by itself require behavioral evaluation.
Public availability likewise does not require package-wide, model-matrix, or
client-matrix evaluation.

Use this table to select the evaluation path:

| Change shape | Selected path | Required coverage |
| --- | --- | --- |
| Documentation, formatting, meaning-preserving wording, or mechanical metadata that does not affect discovery | **Static-only** | Deterministic repository checks |
| Localized instruction, output, safety, or other runtime-responsibility change | **Targeted candidate-only** | Only candidate cases that expose the changed responsibility, a known regression, or a plausibly affected adjacent boundary; run each selected case once initially |
| `name`, `description`, invocation behavior, or adjacent Skill responsibility boundary changes | **Targeted routing or coexistence** | Only relevant should-trigger, should-not-trigger or near-miss, ambiguous, and coexistence cases |
| Known regression, major redesign, split or merge, changed subjective-quality target, changed success contract, or ambiguous candidate-only result | **Baseline comparison** | Matched baseline and candidate evidence for the decision-relevant cases |
| Observed instability, conflicting evidence, or a material failure consequence | **Repetition** | Only the additional observations needed to resolve the acceptance question |
| Explicit environment-support claim, environment-specific failure, or client-specific discovery, permission, tool, hook, or runtime change | **Model/client-specific** | Direct evaluation in the affected environment only |
| Distribution or catalog behavior changes | **Package evaluation** | The affected distribution or catalog checks, separate from routine Skill behavior evaluation |

Ordinary public Skill changes do not require a package, model, or client matrix.
Evaluation size follows the selected behavioral coverage, not a universal case
count. Official guidance sometimes uses three or 3–5 scenarios as an example or
an organizational starting point; this repository does not treat those numbers
as a universal minimum or maximum.

## Companion-Skill exceptions

Skills remain self-contained unless an approved companion relationship is
recorded in `docs/authoring.md`. An undocumented dependency fails static
validation; a documented relationship is not a general dependency mechanism.

For an approved relationship, static validation confirms that the relationship,
rationale, installation path, missing-companion behavior, provenance, and
evaluation location agree across the registry and the affected Skill assets.
When the relationship or its runtime behavior changes, targeted behavioral
evaluation may cover either or both of these distinct risks, according to what
the change affects:

- **Coexistence:** the dependent Skill reads the companion in the required
  order and preserves its applicable constraints.
- **Missing companion:** the dependent Skill follows its documented stop or
  fallback behavior and gives the supported installation path without producing
  an unauthorized partial result.

Re-run only the checks that cover the changed Skill responsibility, relationship,
installation path, or missing-companion behavior. Do not treat the exception as
proof that either Skill works independently of the documented relationship.

## Choosing evaluation depth

Apply these rules in order:

1. Identify the affected claim or responsibility and whether executable behavior
   or a discovery or responsibility boundary changes.
2. If neither changes, run deterministic repository validation and stop.
3. If runtime behavior changes, select only the affected candidate cases. Start
   with one observation for each selected case.
4. If discovery or a responsibility boundary changes, add only the relevant
   routing, near-miss, ambiguous, or coexistence cases.
5. Escalate to baseline comparison, repetition, model/client-specific evaluation,
   or package evaluation only when the corresponding condition in the table can
   change acceptance.

Do not add an unrelated core, capability, routing, or coexistence suite
automatically. A static check does not establish runtime behavior, and a targeted
regression does not establish behavior on untested clients or models. State those
limits instead of expanding the suite mechanically.

## Evaluation selection record

Record only:

- the affected claim or responsibility
- the selected path and why it is sufficient
- the selected cases or deterministic checks
- any untested boundary that limits the acceptance claim

Use the existing evaluation README or change record. Do not require a shared
metadata schema for selection records unless repeated work later demonstrates a
need for more structure.

## Evidence reuse

Treat prior evidence as a reuse candidate only when the evaluated responsibility
and the relevant content are unchanged. The execution and evidence policy
determines whether that evidence is applicable and how to represent its state.
Do not rerun unrelated evidence merely to refresh a passing appearance.

## Evaluation assets per Skill

Each Skill has an `evals/` directory. The README is required; structured assets are optional and should be added when they make repeated evaluation more reproducible.

```text
skills/<skill-name>/
└── evals/
    ├── README.md       # purpose, procedure, result summary, and reflection
    ├── triggers.json   # optional trigger, non-trigger, and near-miss cases
    ├── evals.json      # optional realistic tasks, inputs, assertions, and baseline conditions
    └── results.json    # optional compact evidence record for the currently accepted revision
```

Do not migrate every existing Skill merely to match this structure. Other Skills may adopt structured assets when each receives its next significant revision.

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

Choose trigger cases from actual responsibility boundaries and plausible false activations. Near-miss cases are useful when an adjacent Skill or similar request could reasonably compete; unrelated negative cases are optional controls, not required coverage.

Do not use a universal repetition count or pass threshold. Repeat only after an
observed unstable result, conflicting evidence, or a material failure consequence
makes another observation decision-relevant. When a fixed run count is used as a
cost-bounded smoke test, record that rationale and do not present it as a
statistical guarantee.

Count a trigger only from evidence the client exposes. If Skill loading is not observable, record `not exposed`; do not infer a load event from output wording.

### evals/evals.json

Use this optional asset for:

- realistic tasks and their inputs
- behavioral assertions and critical requirements
- baseline conditions
- isolation and coexistence configurations

Keep scenarios rich enough to expose judgment errors without embedding the desired answer in the task.
Keep executor inputs separate from grading criteria. A scenario may include evidence that a real user would provide, but should not name the expected finding or conclusion merely to make grading easy.

### evals/results.json

Use this optional asset when aggregate counts in the README are not enough to audit an executed revision after temporary artifacts are removed. Record:

- the immutable baseline commit or content hash and candidate file hashes
- client, model, reasoning, date, normalized invocation, and verdict aggregation policy
- a compact case-by-requirement matrix with baseline and candidate verdicts and supporting evidence
- observable trigger results, deterministic fixture checks, and unverified items

Do not store raw traces, full responses, credentials, or environment-specific absolute paths in this file. Link it from the corresponding README result summary.

Treat `results.json` as the compact evidence for the currently accepted Skill revision. Update it in place rather than adding a dated file for every execution. Fold reruns and corrections for the same candidate into the same record. Git history preserves each accepted result together with the Skill source it evaluated.

In schema version 3 records, `candidate` identifies the source and evaluation-definition files currently accepted in the repository. Acceptance identifies the repository revision; it does not by itself mean that behavior or triggering was executed or passed. Record the candidate's evidence state explicitly, such as `unverified` or `targeted_only`, and list the checks that were and were not executed.

An evaluated revision is the immutable set of file hashes, baseline, environment, and execution evidence for content that was actually run. Keep a superseded full-suite result under `historical_full_evaluation`, including its original evaluated-revision hashes and pass claims. Keep later targeted evidence in separately hash-bound records. A pass applies only to its evaluated revision and to unchanged requirements whose applicability is identified explicitly; it does not establish that a different current candidate passes.

Retain a historical targeted observation that lacks required baseline, environment, or execution provenance under `historical_targeted_evidence` with `status: incomplete_provenance`. List every missing provenance field and use `claim_status: no_pass_claim`; incomplete provenance is not evaluated-revision pass evidence and cannot establish `targeted_only` for the accepted candidate. Do not infer missing metadata. When a recorded temporary candidate hash cannot be reproduced from Git, retain the hash with `snapshot_availability: not_retained` instead of claiming that the snapshot remains available.

When the accepted Skill source changes, update `results.json`, mark the affected evidence as superseded or unverified, or remove the file. Do not leave hashes or pass claims that imply the old candidate was the current source. Reuse prior evidence only when the unchanged requirement and evaluated content can be identified explicitly.

Retain a separately named historical result only when it remains necessary for a current decision and Git history is insufficient—for example, an incomparable client or evaluation method, a known regression that must remain directly reproducible, or an external audit requirement. Document its purpose and removal condition in the README. Do not retain or delete result files to satisfy a fixed count.

## Example evals/README.md structure

```markdown
# <skill-name> evals

## Iter 0 — Static check

- description and body are internally consistent
- output format is defined or clearly implied
- the Skill is self-contained or has an approved companion relationship
- material claims and fail-gating requirements are identified

## Coverage map

| Claim | Failure | Scenario | Grader |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

## Scenarios

### Scenario A: <title>

<one-sentence context>

Requirements checklist:
1. [critical] <requirement whose violation fails the scenario>
2. <other requirements>

## Failure Pattern Ledger

- `<known failure pattern>`

## Iter N — YYYY-MM-DD

### Changes

- <what changed from previous>

### Execution results

| Scenario | Result | Evidence | Weak phase |
| --- | --- | --- | --- |
| A | pass / fail / unstable | ... | — |

### Next validation question

- <question whose answer could change the decision>
```

## Running evaluations

There is no repository-wide `/eval` command or required external framework. Record the exact command, script, client workflow, or manual procedure used for each runnable suite. Add a wrapper only when it makes repeated execution materially more reproducible.

Run behavioral evaluations with a blank-slate executor: an agent or client session that starts without repository history and receives only the Skill and inputs required by the scenario.

**Blank-slate executor protocol:**

1. Start a fresh executor with no repository context.
2. Provide the `SKILL.md` content, allowed supporting files, scenario input, and required environment.
3. Keep hidden assertions, expected conclusions, and grader notes out of the executor input.
4. Capture the outcome and exposed trace without asking the executor to declare its own pass/fail result.
5. Grade each applicable requirement and record evidence for the verdict.

Select only the applicable configurations:

- **Isolation:** the target Skill without adjacent Skills that could mask a gap
- **Coexistence:** the target Skill with adjacent Skills or instruction surfaces when a plausible trigger, authority, or workflow conflict exists

Record an unavailable observation as `not exposed` and a skipped run as `not executed`. Neither status counts as a pass.

Prefer deterministic checks for objective outcomes and a separate grader or reviewer for judgment-heavy requirements. Executor self-report can help diagnose confusion, but it is not sufficient as the only pass/fail evidence. Define how per-run and per-case verdicts aggregate before execution.

This approach is inspired by the empirical prompt-tuning methodology described in [mizchi/skills](https://github.com/mizchi/skills). See `THIRD_PARTY_NOTICES.md`.

## Iter 0 static check

Before writing scenarios, perform a static Iter 0 check:

1. `description` and body are internally consistent
2. Output format is defined or clearly implied
3. The Skill is self-contained, or an approved companion relationship documents the required Skill and its missing-companion behavior
4. Critical requirements are identified only where violating them should fail the scenario
5. The affected claims and changed behavior are mapped to plausible failures and grading methods

If executable behavior and responsibility boundaries are unaffected, stop after
deterministic validation. Otherwise, only after Iter 0 passes should you
formalize the selected scenarios in `evals/README.md`.

## Baseline comparison

Run a baseline comparison only when relative evidence can change acceptance: a
known regression, a major redesign, split, or merge, a changed subjective-quality
target, a changed success contract, or an ambiguous candidate-only result. Do not
run a baseline merely because a Skill is public, its body changed, or the change
is described as significant.

When comparison is selected, use the previous version or the no-Skill condition,
whichever represents the decision being made. Identify the baseline with a
commit, content hash, or retained snapshot. Use the same task inputs, client,
model, reasoning settings, environment, and grading policy for both sides.

Check coexistence only where adjacent surfaces could mask a gap or compete with the changed behavior. Historical benchmarks may be retained for context, but the default regression baseline is the immediately preceding behavior.

When a target model or client is unavailable, record `not executed`. A new paired baseline/candidate run on an available target may be added, but must not be merged silently with results from a different environment.

## Stopping rule

Stop expanding or rerunning an evaluation when:

- every affected claim, changed behavior, known regression, and relevant boundary has a grading path
- each retained scenario covers a distinct risk
- observed results are stable enough for the decision being made, or remaining instability is explicitly reported
- another check or run would not change acceptance

Continue or deepen evaluation when a requirement is ungraded, results conflict, a high-impact boundary remains untested, or the next run could distinguish competing explanations.

## Result metadata and artifact handling

When behavioral evaluation is executed and a result record is needed, record:

- client, model, reasoning settings, and date
- run count and trigger rate
- assertion results with supporting evidence
- the coverage map and verdict aggregation rule
- isolation and coexistence configuration
- token and duration values when the client exposes them
- `not executed` and `not exposed` items

Store raw JSONL, authentication material, and full session logs only in a temporary directory outside the repository or in a retention-controlled CI artifact. Do not commit credentials, raw sessions, or unredacted traces. Keep the compact evidence for the currently accepted revision in `results.json`; use Git history to audit earlier accepted claims together with the Skill source that produced them.

## Source interpretation

- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) presents evaluation-first iteration and example scenario counts.
- [Anthropic Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise) gives an organizational 3–5 query requirement and recommends trigger, isolation, coexistence, instruction-following, output-quality, and active-model coverage.
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) recommends testing prompts against the Skill description and documents explicit and implicit Skill invocation.

This repository adopts the behavioral dimensions and evidence-first direction from those sources while choosing suite size from local responsibility and failure coverage.
