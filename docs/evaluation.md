# Skill Evaluation

This document describes the evaluation approach used for Skills in this repository.

## Evaluation principle

Evaluation size follows behavioral coverage, not a universal case count.

Before adding or removing scenarios, make a compact coverage map:

| Skill claim or change | Plausible failure | Scenario or check | Grading method |
| --- | --- | --- | --- |
| `<claimed behavior>` | `<observable failure>` | `<input and environment>` | `<deterministic check, rubric, or reviewer>` |

A suite is sufficient when every material responsibility, changed behavior, known regression, and relevant boundary has a way to fail visibly, and each retained scenario covers a distinct risk. Do not add scenarios to reach a target number or remove scenarios merely to stay below one.

Official guidance sometimes uses three or 3–5 scenarios as an example or an organizational starting point. This repository does not treat those numbers as a universal minimum or maximum.

## Choosing evaluation depth

Use the least expensive level that can resolve the current uncertainty:

1. **Static validation:** use for every Skill change. Check metadata, internal consistency, self-containment, references, boundaries, and output contract.
2. **Targeted behavioral regression:** use when instructions, triggering, coexistence, safety behavior, or output requirements change. Run only the scenarios that cover the affected and adjacent risks.
3. **Empirical prompt tuning:** use repeated baseline/candidate cycles when observed failures, high impact, unstable behavior, or a substantial redesign make iteration evidence worth the cost.

A static check does not establish runtime behavior. A targeted regression does not establish behavior on untested clients or models. State those limits instead of expanding the suite mechanically.

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

Do not use a universal repetition count or pass threshold. Repeat when stochastic variation, an unexpected result, model differences, or the consequence of a false activation makes another observation decision-relevant. When a fixed run count is used as a cost-bounded smoke test, record that rationale and do not present it as a statistical guarantee.

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

When the accepted Skill source changes, update `results.json`, mark the affected evidence as superseded or unverified, or remove the file. Do not leave hashes or pass claims that imply the old candidate was the current source. Reuse prior evidence only when the unchanged requirement and evaluated content can be identified explicitly.

Retain a separately named historical result only when it remains necessary for a current decision and Git history is insufficient—for example, an incomparable client or evaluation method, a known regression that must remain directly reproducible, or an external audit requirement. Document its purpose and removal condition in the README. Do not retain or delete result files to satisfy a fixed count.

## Example evals/README.md structure

```markdown
# <skill-name> evals

## Iter 0 — Static check

- description and body are internally consistent
- output format is defined or clearly implied
- the Skill is self-contained
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

Evaluate both:

- **Isolation:** the target Skill without adjacent Skills that could mask a gap
- **Coexistence:** the target Skill with adjacent Skills or instruction surfaces when a plausible trigger, authority, or workflow conflict exists

Record an unavailable observation as `not exposed` and a skipped run as `not executed`. Neither status counts as a pass.

Prefer deterministic checks for objective outcomes and a separate grader or reviewer for judgment-heavy requirements. Executor self-report can help diagnose confusion, but it is not sufficient as the only pass/fail evidence. Define how per-run and per-case verdicts aggregate before execution.

This approach is inspired by the empirical prompt-tuning methodology described in [mizchi/skills](https://github.com/mizchi/skills). See `THIRD_PARTY_NOTICES.md`.

## Iter 0 static check

Before writing scenarios, perform a static Iter 0 check:

1. `description` and body are internally consistent
2. Output format is defined or clearly implied
3. The Skill is self-contained (does not assume another Skill or agent as a dependency)
4. Critical requirements are identified only where violating them should fail the scenario
5. Material claims and changed behavior are mapped to plausible failures and grading methods

Only after Iter 0 passes should you formalize scenarios in `evals/README.md`.

## Baseline comparison

When significantly revising a Skill, compare the candidate with the previous version or with no Skill if the previous version is unavailable. Identify the baseline with a commit, content hash, or retained snapshot. Use the same task inputs, client, model, reasoning settings, environment, and grading policy for both sides.

Check coexistence only where adjacent surfaces could mask a gap or compete with the changed behavior. Historical benchmarks may be retained for context, but the default regression baseline is the immediately preceding behavior.

When a target model or client is unavailable, record `not executed`. A new paired baseline/candidate run on an available target may be added, but must not be merged silently with results from a different environment.

## Stopping rule

Stop expanding or rerunning an evaluation when:

- every material claim, changed behavior, known regression, and relevant boundary has a grading path
- each retained scenario covers a distinct risk
- observed results are stable enough for the decision being made, or remaining instability is explicitly reported
- another run would not change the current design, rollout, or confidence judgment

Continue or deepen evaluation when a requirement is ungraded, results conflict, a high-impact boundary remains untested, or the next run could distinguish competing explanations.

## Result metadata and artifact handling

Record:

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
