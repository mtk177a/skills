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

Reuse prior evidence only when the evaluated content, responsibility,
environment relevance, and requirement remain applicable. Bind new targeted
evidence to the revision that was actually evaluated. When current content
changes, identify which prior requirements remain applicable instead of treating
an earlier pass as evidence for the whole candidate.

Preserve a historical result separately only when it still informs a current
decision and Git history is insufficient. Otherwise, rely on Git history. Do not
rerun unchanged evidence merely because another part of a Skill changed or to
refresh a passing appearance.

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

- the claim or change being checked and the evaluated candidate revision
- the selection path, stopping rationale, executed checks or cases, results, and supporting evidence
- client, model, and reasoning when an LLM was executed
- the unverified scope that limits the conclusion
- baseline identity and matched conditions only when comparison was executed

Do not store raw traces, full responses, credentials, or environment-specific absolute paths in this file. Link it from the corresponding README result summary.

Treat `results.json` as the compact evidence for the currently accepted Skill revision. Update it in place rather than adding a dated file for every execution. Fold reruns and corrections for the same candidate into the same record. Git history preserves each accepted result together with the Skill source it evaluated.

Acceptance identifies the repository revision; it does not by itself mean that
behavior or triggering was executed or passed. A pass applies only to the
evaluated revision and to unchanged requirements whose continuing applicability
is explicit. When the accepted Skill source changes, update `results.json`, mark
affected evidence as `superseded` or `unverified`, or remove the file. Do not
infer missing provenance or leave hashes and pass claims that imply an old
candidate is the current source.

This repository does not require a common result schema. Preserve an existing
local schema when it remains useful, but record only fields that apply to the
selected evaluation path. Do not require baseline, comparison matrices, trigger
rates, usage metrics, or grader calls for a candidate-only result.

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

Use deterministic repository checks, fixture state, exact output fields, hashes,
traces, or another objective observation without an LLM whenever they resolve
the selected requirement.

For routine model-independent behavior that requires model execution, use Codex
with `gpt-5.6-luna` and max reasoning as the reference environment. Start with
one candidate run for each selected case. This is a low-cost reference
environment, not a support matrix or evidence for another model or client.

When the accepted claim materially depends on another model or client, execute
the selected case directly in that target environment. Examples include an
explicit support claim, an environment-specific failure, or client-specific
discovery, permissions, tools, hooks, or runtime behavior. Do not require a Luna
preflight before target-environment execution.

If a Luna run fails or is ambiguous, first determine whether it already exposes
an instruction or fixture defect. Escalate to another model only when
distinguishing Skill failure from model limitation can change acceptance. Do not
treat a Luna pass or failure as evidence for unexecuted models or clients.

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

Use the first sufficient grading method:

1. deterministic assertions for objective requirements
2. direct maintainer review against a short rubric for judgment-heavy requirements
3. a separate blank-slate LLM grader only when repeatable or independent model judgment is materially useful

An LLM grader is optional and does not need to be stronger than the executor by
default. Keep hidden answers and grading criteria out of the executor input.
Executor self-report can help diagnose confusion, but it is not sufficient as
the only evidence for an independently observable requirement.

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
commit, content hash, or retained snapshot. Use the same task inputs, fixture,
client, model, reasoning settings, sandbox, and grading policy for both sides.

Check coexistence only where adjacent surfaces could mask a gap or compete with the changed behavior. Historical benchmarks may be retained for context, but the default regression baseline is the immediately preceding behavior.

When a target model or client is unavailable, record `not executed`. A new paired baseline/candidate run on an available target may be added, but must not be merged silently with results from a different environment.

Start with one observation for each selected condition. Repeat only after an
unstable result, conflicting evidence, a defective run, or a material failure
consequence makes another observation useful for the acceptance decision.

## Stopping rule

Stop expanding or rerunning an evaluation when:

- every affected claim, changed behavior, known regression, and relevant boundary has a grading path
- each retained scenario covers a distinct risk
- observed results are stable enough for the decision being made, or remaining instability is explicitly reported
- another check or run would not change acceptance

Continue or deepen evaluation when a requirement is ungraded, results conflict, a high-impact boundary remains untested, or the next run could distinguish competing explanations.

## Result metadata and artifact handling

Record the minimal evidence needed to bound the accepted conclusion:

- the claim or change being checked
- the selection path and stopping rationale
- the checks or cases executed and their results
- client, model, and reasoning when an LLM was executed
- the unverified scope that limits the conclusion
- baseline identity and matched conditions only when comparison was executed

Record token counts, model calls, turns, tool calls, or duration only when the
client exposes them and they are used in the current cost or acceptance decision.
Do not invent unavailable data.

Use these plain evidence states where applicable without introducing a
repository-wide state machine:

- `not executed`: a check was skipped or unavailable
- `not exposed`: the client did not expose the observation
- `unverified`: the accepted claim lacks applicable evidence
- `superseded`: later content or evidence replaced the earlier claim

None of these states is a pass.

Store raw JSONL, authentication material, and full session logs only in a temporary directory outside the repository or in a retention-controlled CI artifact. Do not commit credentials, raw sessions, or unredacted traces. Keep the compact evidence for the currently accepted revision in `results.json`; use Git history to audit earlier accepted claims together with the Skill source that produced them.

## Source interpretation

- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) presents evaluation-first iteration and example scenario counts.
- [Anthropic Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise) gives an organizational 3–5 query requirement and recommends trigger, isolation, coexistence, instruction-following, output-quality, and active-model coverage.
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) recommends testing prompts against the Skill description and documents explicit and implicit Skill invocation.

This repository adopts the behavioral dimensions and evidence-first direction from those sources while choosing suite size from local responsibility and failure coverage.
