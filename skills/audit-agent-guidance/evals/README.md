# audit-agent-guidance evals

## Purpose

Verify that the Skill diagnoses guidance behavior and root causes without inheriting the current artifact layout, suppressing structural alternatives, claiming unobserved behavior, reducing third-party capability chains to isolated permissions, or using a fixed case count as evidence of completeness.

## Assets

- `triggers.json`: executable routing cases for triggers, near misses, and coexistence
- `evals.json`: executable behavior cases and their grading requirements
- [`results.json`](results.json): legacy historical behavior evidence for the recorded revision
- this README: coverage, selection guidance, historical evidence, and unverified boundaries

## Static check

- [x] `name`, directory, and `description` agree on existing durable guidance auditing.
- [x] The body defines single-Skill and cross-surface audits.
- [x] Findings require evidence, impact, confidence, affected surfaces, and verification or falsification.
- [x] Ordinary diff review, new guidance design, and standalone `.rules` review remain out of scope.
- [x] Evaluation depth follows material claims, changed behavior, risk, and uncertainty.
- [x] The reporting contract requires staged rollout only when a change is recommended.
- [x] Third-party and executable Skill review traces provenance, data access, outbound destinations, and enforceable controls without absorbing standalone code vulnerability review.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Outcome-first diagnosis | Accepts the requested artifact edit as the problem definition | `loading-behind-wording`, `static-only-evidence` | `outcome-first` |
| Evidence status | Claims behavior from text alone | `static-only-evidence` | `evidence-vs-inference`, `behavior-unconfirmed-without-evidence` |
| Surface discovery and client semantics | Repeats stale or unsupported loading claims | `loading-behind-wording` with supplied facts and official-source access when available | `client-semantics-evidence` |
| Finding contract | Omits impact, confidence, affected surfaces, or falsification | all material-finding cases | `finding-contract` |
| Structural alternatives | Forces a local wording patch | `loading-behind-wording`, `replace-guardrail` | counterfactual assertions |
| Guardrail replacement | Weakens safety while changing wording | `replace-guardrail` | `guardrail-safety` |
| Third-party capability chain | Reviews Markdown or individual permissions but misses file-read plus network-send risk | `third-party-skill-capability-chain` | `third-party-capability-chain` |
| Healthy guidance | Invents a change or mandatory heading | `healthy-guidance` | `never-not-universal` plus additional requirement |
| Read-only audit | Edits because the repository is writable | `read-only-in-writable-repository` | file hashes plus `read-only-audit` |
| Trigger boundary | Collides with design or ordinary review Skills | `triggers.json` near-miss and coexistence cases | observable Skill-load events |
| Proportional evaluation | Uses fixed findings, cases, or repetitions as completeness | output cases | `proportional-evaluation` |

## Execution and grading

Select the evaluation path and cases from the changed responsibility under [`docs/evaluation.md`](../../../docs/evaluation.md).\
The complete case set is a menu, not a default run list.\
A definition-only change requires a static check of schema validity and preserved case intent; it does not require a model run.

Before a model-backed run, use `scripts/run_skill_evaluation.py plan` and inspect the model-call count.\
The Runner keeps grading requirements out of executor input, observes installed Skill loads for routing cases, and uses disposable fixtures.\
For a comparison, use the immediately preceding committed Skill as the baseline and match the task input and execution environment.\
The pre-rename version is a historical benchmark only.\
Repeat a case when instability or conflicting evidence would change the decision.

Use a read-only sandbox for ordinary behavior cases.\
Run `read-only-in-writable-repository` with `--sandbox workspace-write` so the decision not to edit the supplied fixture can be observed.\
Compare the fixture guidance files before and after the run; a model's statement that it made no edits is not sufficient evidence.

Grade every planned requirement for each executed case and condition.\
Record an unexposed routing observation or an unexecuted case as unverified, not as a pass.\
Keep raw prompts, traces, and full responses outside the repository.\
Write a compact `report.json` only when a change-scoped model run contributes to the acceptance decision.

## Historical result — 2026-07-23

The pre-rename baseline was commit `73e289a016bdb26787a2329a49f27dbc7e21e8ab`; the candidate was commit `2b33ff1dabaabab04f21dc6e33c8ae782f7642be`.

- Client: Codex CLI 0.145.0
- Model: `gpt-5.6-sol`
- Reasoning: high
- Sandbox: read-only
- Formal run count: 80 total; 60 trigger runs and 20 output-quality runs
- Baseline trigger result: 15/15 expected loads and 3/15 unexpected loads
- Candidate trigger result: 15/15 expected loads and 0/15 unexpected loads
- Reported assertion result: baseline 5/9 full passes; candidate 9/9 passes
- Unexecuted checks: Claude Code and `skills-ref`

This result supports the redesign properties graded by the version-1 suite. It does not validate the current coverage map, writable-repository boundary, client-semantics lookup, or revised grading policy. Raw JSONL and full responses were temporary and are not available as durable repository evidence.

## Latest behavioral evidence — 2026-07-24

- Client: Codex CLI 0.145.0
- Model / reasoning: `gpt-5.6-sol` / high
- Baseline: commit `42ebd18cb2406d1cfcbeb34cd289fd620c8e4f9b`; candidate `SKILL.md`: `sha256:e9a13471854a6ff8f6c19215c2a10ac01bece15ddb7b86ea27d9b4eac7c499df`
- Selected behavior cases: `loading-behind-wording`, `third-party-skill-capability-chain`, and `read-only-in-writable-repository`
- Candidate grading: 14 / 14 requirements passed; baseline: 12 passed and 2 partial
- Affected trigger cases: candidate and baseline both loaded the target for the third-party trust-boundary case and did not load it for standalone script vulnerability review
- Writable fixture hashes: unchanged in baseline and candidate
- Repetition: the two initially partial candidate requirements were tightened and only the affected case was rerun; the final independent grade passed both
- Regressions: none in the selected cases
- Durable evidence: [`results.json`](results.json)
- Claude Code and other clients: not executed
- Unverified: runtime loading outside the selection protocol, approval behavior, remote destinations, network transmission, and the factual freshness of client claims in generated outputs

The current `SKILL.md` has the recorded candidate SHA-256.\
These behavior cases have not been rerun against the current Codex CLI; [`results.json`](results.json) remains historical evidence under its original grading method.

## Next validation question

Does the same finding completeness and third-party capability tracing hold on a real repository fixture with observable client loading, approval, and network behavior?
