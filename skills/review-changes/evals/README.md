# review-changes evals

## Purpose

Verify that `review-changes` selects a new or updated effective diff, inspects the surrounding evidence needed to judge it, adapts to code, documentation, and configuration changes, and reports findings with separate labels, impact, and confidence. It must distinguish executed checks from suggested verification, handle full re-review state, and report no-findings or unavailable-diff states without inventing evidence.

Structured assets:

- `triggers.json`: review, near-miss, and coexistence selection cases
- `evals.json`: baseline, behavior, fixture, and assertion definitions
- `results.json`: compact, hash-bound evidence across recorded revisions, added after execution

## Candidate static check

- `description` includes code, documentation, configuration, effective-diff, and full re-review triggers and excludes triage, specific-fix validation, comment drafting, summarization, and implementation
- effective diff and material exclusions are established before findings
- surrounding contracts, callers, tests, and repository precedent are read only when they can test a change assumption
- code, documentation, and configuration use applicable risk dimensions rather than one mandatory checklist
- every material finding separates canonical label, confidence, evidence, impact, verification, and an explicit `Unconfirmed premises` field
- a high-impact unconfirmed premise remains visible as a `question` and can be handed to triage without downstream inference
- executed checks, suggested verification, unchecked scope, and residual risk are not conflated
- no-findings and unavailable-diff states are distinct
- full re-review state is separate from label and confidence
- the Skill remains read-only, portable, and usable without a companion Skill or subagent

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Effective diff | Reviews the wrong range or mixes unrelated working-tree changes | `explicit-range`, `missing-diff` | Scope statement and file evidence |
| Contextual evidence | Reviews only the changed line and misses a contract or cardinality violation | `external-contract-and-cardinality` | Assigned assertions |
| Uncertainty and handoff | Turns a potentially severe unknown into a low-value question, hides the premise in another field, or forces downstream triage to infer it | `high-impact-unconfirmed-premise` | Finding fields and handoff assertion |
| Change-type adaptation | Forces code tests onto docs/config or omits available deterministic checks | `documentation-and-configuration` | Commands and results |
| No-findings state | Invents nits or returns a bare approval | `clean-diff` | Finding count and report contract |
| Full re-review | Mixes `Resolved` / `Remaining` / `New` with label or confidence, or repeats classifications supplied by the prompt instead of deriving them from the target | `full-rereview` | Fixture-derived state reconciliation and new-finding discovery |
| Trigger boundary | Collides with triage, validation, comment drafting, summary, implementation, or guidance audit | `triggers.json` | Observable Skill loads |
| Excess complexity | Accepts speculative abstractions whose concrete maintenance cost has no current requirement or observed-risk basis | `unjustified-abstraction` | Finding evidence and assigned assertions |
| Overly narrow correction | Accepts a small patch that leaves a confirmed shared rule inconsistent across a known path | `local-patch-leaves-shared-cause` | Finding evidence and assigned assertions |

## Execution protocol

1. Use committed `HEAD` as the baseline and the working-tree Skill as the candidate.
2. Give the executor only the case `input` and its disposable fixture. Keep titles, assertions, and expected conclusions hidden.
3. Use the same client, model, reasoning effort, sandbox, fixture, and grader for both conditions.
4. For git fixtures, construct the declared base, candidate commit, working-tree changes, and checks in a temporary repository outside this source repository.
5. Count a Skill trigger only from an observable `SKILL.md` open.
6. Grade objective scope and command claims from the fixture and captured output; use a separate grader for judgment-heavy findings.
7. Repeat only when an unexpected result, instability, client difference, or failure consequence could change the decision.

For Codex CLI, use an ephemeral session with a pinned model and reasoning effort. Keep raw JSONL and full responses in a temporary directory.

Claude Code and other clients are outside the current execution plan and must be recorded as `not executed`.

## Failure pattern ledger

- `wrong diff or base reviewed`
- `diff-only inspection misses surrounding contract`
- `question loses high potential impact`
- `unconfirmed premise omitted or hidden in another finding field`
- `confidence collapsed into canonical label`
- `suggested check reported as executed`
- `code test forced onto static documentation or configuration`
- `clean diff padded with nits or notes`
- `unavailable diff reported as no issues`
- `re-review state mixed with label or copied from an answer-bearing prompt`
- `review workflow routed to an adjacent Skill`
- `speculative abstraction accepted without concrete cost or requirement evidence`
- `small diff accepted while a confirmed shared cause remains`

## Recorded full evaluation — 2026-07-27

On 2026-07-27, Codex CLI 0.145.0 with `gpt-5.6-sol` and high reasoning produced:

- baseline: 21/29 behavior requirements passed, 2 were partial, and 6 failed; 2/7 cases passed
- candidate: 29/29 behavior requirements and 7/7 cases passed
- trigger selection: 10/10 cases passed for both baseline and candidate

The baseline omitted the dedicated `Unconfirmed premises` field and, in two cases, other reporting details. The candidate preserved the gateway premise in that field, derived F1 as `Resolved`, F2 as `Remaining`, and the unbounded retry as `New` from the disposable repository rather than an answer-bearing prompt, and passed the retained cases. Every invocation used an isolated `HOME` so globally installed personal Skills were unavailable.

Claude Code and other clients were not executed. Detailed case-by-assertion and observable trigger evidence is in `results.json`; raw traces are intentionally not retained in the repository.

## Coherent-change revision — 2026-08-04

- Compared committed `HEAD` and the final working-tree candidate on `unjustified-abstraction` and `local-patch-leaves-shared-cause` with Codex CLI 0.146.0, `gpt-5.6-sol`, and high reasoning. Separate blind graders evaluated each matched pair.
- `unjustified-abstraction`: the final candidate passed 5/5 requirements; the baseline failed `finding-contract`. The candidate tied the concrete added concepts to maintenance and diagnostic paths, recorded unavailable fallback behavior as a premise, and did not claim unsupported runtime failure.
- `local-patch-leaves-shared-cause`: the final candidate passed 5/5 requirements; the baseline was partial on `finding-contract`. The candidate identified the known inconsistent path and shared owner while limiting Impact to the supplied specification violation and two-path inconsistency.
- Earlier candidate runs exposed two useful failures: `none identified` conflicted with an unchecked fallback, and speculative downstream account-matching effects exceeded the supplied evidence. The final candidate requires premise-consistent, evidence-bound Impact claims.
- Retained review cases and trigger routing were not rerun because their responsibilities and descriptions are unchanged.
- Next validation question: Does the same distinction hold on a real diff where callers, fallback behavior, and downstream contracts can be inspected directly?
