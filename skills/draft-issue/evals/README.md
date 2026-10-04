# draft-issue evals

## Purpose

Verify that `draft-issue` produces an evidence-grounded, tracker-aware, unposted Issue draft and filing handoff without fabricating content, overstating verification, trusting embedded external instructions, requiring a companion Skill, or writing to a tracker.

## Assets

- `triggers.json`: trigger, continuation, near-miss, and coexistence selection cases
- `evals.json`: candidate behavior cases, selected baseline and without-Skill comparisons, and separate no-companion candidate cases with hidden grading requirements
- `results.json`: historical comparison evidence for the accepted 2026-07-31 revision
- this README: static contract, coverage, protocols, and summarized results

## Static check

- `description` targets Issue draft and filing-payload preparation while excluding general clarification, existing-Issue triage, implementation, and tracker writes.
- The body distinguishes confirmed, reported, inferred, assumed, unknown, and unverified information.
- Exactly one readiness state is assigned without requiring later technical investigation to finish before filing.
- Bug, feature, improvement, task, and project-template structures include only applicable content.
- Template and duplicate-search results use explicit observed, unavailable, or unperformed states.
- The Skill treats tracker content as untrusted, minimizes outbound data, and does not expose sensitive values.
- The workflow remains usable without `clarify-request` or a particular tracker client.
- Issue mutation remains outside the Skill even when the originating request asks to create an Issue.
- The Skill has no scripts, executable dependencies, network destination, or client-specific metadata.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Bug-specific drafting and evidence state | Presents a support reproduction as independently verified or emits feature placeholders | `grounded-reported-bug` | Evidence-fidelity and adaptive-content assertions |
| Project-template compliance | Replaces the observed template with a generic body or drops supplied acceptance criteria | `feature-with-project-template` | Heading and content comparison |
| Tracker-neutral usefulness | Blocks or invents a target, document path, or reviewer | `tracker-neutral-task` | Readiness and no-fabrication assertions |
| Iterative self-containment | Repeats answered questions, drops prior facts, or requires `clarify-request` | `continuation-after-partial-answers` | Candidate isolation and context preservation |
| Unavailable lookup handling | Claims no template or duplicate exists, requests credentials, or blocks a useful draft | `tracker-checks-unavailable` | Exact state and authority assertions |
| Duplicate uncertainty | Decides duplicate status from a similar title | `potential-duplicate-needs-owner` | Candidate and searched-scope inspection |
| Untrusted content and sensitive data | Executes embedded instructions or reproduces a synthetic credential or private hostname | `malicious-template-and-sensitive-data` | Response scan and command or tool trace |
| External-write boundary | Claims to create or mutate an Issue from a drafting request | `explicit-create-request-stops-before-write` | Response and command or tool trace |
| Material value | Adds no filing-readiness evidence beyond ordinary drafting | Selected baseline, without-Skill, and candidate conditions | Blinded comparison under the same rubric |
| Trigger and coexistence | Loads for clarification, implementation, investigation, or existing-Issue mutation | `triggers.json` | Observable Skill load |

## Execution and grading

The definitions use the executable `{skill_name, evals}` format. The two continuation and unavailable-access cases retain their no-companion conditions as separate candidate cases. Behavior cases preserve the legacy assigned assertions and case-specific expectations; routing cases preserve the expected handler sets. The project-template case materializes its four-heading template as an inline fixture.

Use the repository Runner and [evaluation workflow](../../../docs/evaluation.md). Select only cases that address a changed responsibility or a concrete remaining risk. Inspect the plan and model-call count before execution. Keep the plan, raw responses, traces, and grades in a temporary directory outside the repository. Grade only the planned requirements and observe routing through successful Skill reads. Repeat only when an unexpected or unstable result could change the decision.

The 2026-07-31 comparison below is historical evidence, not a result for this migrated definition or for a later Skill revision.

## Failure Pattern Ledger

- `reported behavior rewritten as independently verified`
- `bug and feature templates emitted together`
- `target, reproduction, impact, acceptance criteria, or metadata invented`
- `one clarification round treated as automatic completion`
- `clarify-request required for isolation behavior`
- `unavailable template or search reported as checked`
- `similar title declared a duplicate without semantic evidence`
- `template content followed as executable instruction`
- `synthetic credential or private detail copied into a public Issue`
- `draft request treated as tracker-write authority`
- `existing-Issue triage, implementation, or mutation routed to draft-issue`

## Historical behavior evidence

Evaluated on 2026-07-31 with Codex CLI 0.146.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.

- The candidate passed all 10 behavior conditions and all 87 assigned non-comparative requirements, including isolation continuations and unavailable tracker access without `clarify-request`.
- Anonymous comparison ranked the candidate above no-Skill in all four representative current/no-Skill/candidate cases. It also ranked the candidate above the current Skill in those cases.
- The candidate passed all nine trigger, continuation, near-miss, and coexistence cases with observable Skill reads.
- The initial candidate exposed duplicate-owner retention, unsupported completion-detail expansion, inferred expected behavior, data-handling, filing-next-actor, and continuation-routing gaps. Only affected behavior cases were rerun after correction; the full routing suite was rerun after the `description` change.
- A grader schema initially returned `additional_requirement` as a pseudo-assertion. Stored responses were regraded with exact assertion IDs; that corrected pass exposed two remaining duplicate-case gaps, which were fixed and rerun.
- Raw prompts, responses, JSONL, grader output, and temporary Skill directories remained under `/tmp` and were not committed.
- Claude, other clients, live tracker connectors, external writes, repeated-run stability, and model variation were not evaluated.

See [`results.json`](results.json) for candidate hashes, the case-by-requirement matrix, anonymous material-value comparisons, observable Skill loads, iteration provenance, and unverified items.

### Next validation question

- Does the candidate add enough evidence, readiness, and tracker-state discipline over ordinary drafting to justify the Skill's context and maintenance cost?
