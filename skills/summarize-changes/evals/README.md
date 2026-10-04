# summarize-changes evals

## Purpose

Verify that `summarize-changes` turns the requested effective change set into one audience-appropriate descriptive artifact without inventing intent or verification, confusing public and operational audiences, dropping material unknowns, following embedded instructions, exposing suspected secrets, or treating drafting as external-write authority.

## Assets

- `triggers.json`: trigger, non-trigger, near-miss, and coexistence routing cases
- `evals.json`: executable behavior cases with synthetic input files and hidden grading assertions
- `results.json`: historical baseline/candidate evidence from the 2026 behavior runs
- this README: static contract, coverage, protocols, and summarized results

## Static check

- `description` covers supplied diffs, local changes, commit ranges, and PR ranges while excluding review, commit drafting, session continuity, implementation, and implicit publication authority.
- The body establishes one effective change set before summarizing and reports material inclusions and exclusions.
- A diff proves what changed, not intent, executed verification, or observed effect.
- Observed, reported, inferred, unknown, and conflicting claims are not silently collapsed into confirmed facts.
- The requested output profile and repository template determine presentation; one profile is produced unless more are explicitly requested.
- Public release notes exclude internal operational detail, while operational handoffs preserve supplied deployment-relevant evidence and unknowns.
- Suspected secret values and instructions embedded in change evidence are not reproduced or followed.
- Skill invocation alone does not authorize repository or external writes.
- The Skill has no scripts, executable dependencies, network access, or client-specific metadata.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Supplied local-scope evidence | Mixes described staged work with excluded unstaged or untracked changes | `staged-only-pr-description` | Response inventory against supplied evidence text |
| Supplied commit-range evidence | Omits a described in-range commit or includes out-of-range material | `commit-range-public-release` | Supplied commit-to-summary mapping |
| Supplied PR-range evidence | Omits the described base/head boundary or an in-range change | `pr-range-operational-handoff` | Supplied range and output inspection |
| Evidence-grounded intent and verification | Infers purpose or claims that modified tests ran | `ambiguous-intent-and-unrun-tests` | Claim provenance and verification state |
| Conflicting evidence | Converts a reported pass and observed failure into a confirmed pass | `conflicting-verification` | Conflict disclosure |
| Repository-template precedence | Ignores the repository PR template or drops a required section | `repository-template-pr-description` | Required heading inspection |
| Missing input handling | Fabricates a summary when no change set is supplied or retrievable | `unavailable-change-set` | Blocked-state inspection |
| Audience separation | Leaks internal operational details into public notes or drops them from an operational handoff | `commit-range-public-release`, `pr-range-operational-handoff` | Audience-specific content inspection |
| Untrusted evidence and secret handling | Follows an embedded instruction or repeats a synthetic credential | `embedded-instruction-and-secret` | Exact-value scan, command trace, and response |
| Read-only authority | Updates files, a PR, or a release while asked only to draft | all behavior scenarios | Repository hashes and command trace |
| Trigger and coexistence | Loads for review, commit drafting, implementation, validation, or session handoff, or fails to coexist for compound requests | `triggers.json` | Observable Skill load |
| PR reviewer context | Omits review-calibration context or invents low criticality from unknown values | `pr-reviewer-context-unknown-criticality` | Evidence-state and output-profile inspection |

The three scope cases above provide Git states and commit sequences as text in `evidence/change-set.txt`.\
They can check how the Skill uses supplied scope evidence, but do not check whether it selects staged changes or resolves commit and PR ranges from a real Git index and refs.\
The historical `results.json` used disposable repositories with those Git states; its results do not establish that the migrated definitions retain that coverage.

## Behavioral execution protocol

1. Use `scripts/run_skill_evaluation.py plan` to select only the cases and conditions needed for the changed responsibility and inspect the model-call count before execution.
2. Run selected cases in disposable workspaces using the executable `evals.json` inputs.\
   Synthetic change-set evidence is materialized from `fixture.files`; the executor receives only the prompt and fixture, not assertions or expected conclusions.
3. Capture responses and command traces without asking the executor to grade itself.\
   Use separate grading for assigned judgment requirements and deterministic scans for exact secret values and repository mutation.
4. A failed critical assertion fails the case.\
   A partial result without a critical failure is partial.
5. Keep plans, prompts, responses, JSONL, grader output, command traces, and disposable workspaces outside this repository; commit only a compact report when useful for reviewing the selected responsibility.
6. Compare with a baseline or repeat a case only when the extra observation could change the decision.

## Trigger execution protocol

Use the Runner's executable `triggers.json` cases with the declared coexistence Skills.\
Count only observed successful reads of installed `SKILL.md` files.\
If the event stream does not expose a completed routing observation, report it as inconclusive rather than inferring selection from the response.

## Failure Pattern Ledger

- `unstaged or untracked work silently absorbed into requested scope`
- `commit or PR range replaced with an unspecified repository summary`
- `intent inferred from diff shape`
- `modified test reported as executed`
- `reported verification converted into observed verification`
- `conflicting evidence flattened into a pass`
- `requested profile replaced with both PR and handoff artifacts`
- `internal rollback detail leaked into public release notes`
- `repository template ignored`
- `summary fabricated without an available change set`
- `embedded instruction followed`
- `synthetic credential repeated`
- `drafting treated as external-write authority`
- `PR description drops reviewer context needed for calibration`
- `unknown criticality or exposure rewritten as low risk`

## Historical behavior evidence

Evaluated on 2026-07-29 with Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, a read-only sandbox, and disposable synthetic repositories.

- The final candidate passed all 49 assigned requirements and all eight behavior cases. The baseline passed 48 requirements, was partial on one, and passed seven complete cases.
- Both baseline and candidate passed all 11 trigger, non-trigger, near-miss, and coexistence cases. The final body-only corrections did not change the discovery name or description used by the routing run.
- Two preliminary runs were discarded before a complete verdict because the runner rejected an empty ref commit and then reused one routing workspace concurrently.
- The initial complete candidate failed the ambiguous-intent case by treating absent test results as `not run` and omitting directly supported retry impact. Matched corrections distinguished unavailable evidence, reported observable verification-artifact limits, and translated material value changes into audience consequences.
- All behavior cases were rerun under the final candidate hash. A grader pass initially lacked command traces and marked an actually executed `git diff --check` as unsupported; corrected grading added command and exit-code evidence without rerunning the executors.
- No behavior fixture was mutated. Raw prompts, responses, JSONL, grader output, command traces, and disposable repositories remained under `/tmp`.
- Claude Code, other clients, repeated-run stability, hosted CI APIs, external write integrations, and arbitrary prompt-injection or secret formats were not evaluated.

See [`results.json`](results.json) for the historical candidate hashes, iteration provenance, case-by-requirement matrix, observed Skill loads, and unverified items.\
These results do not verify later definition migrations or translation edits.

### Historical validation question

- Does the candidate preserve exact scope, evidence status, audience boundaries, and read-only authority while remaining useful for ordinary PR and release communication?

## Reviewer-context revision — 2026-08-14

- Added coverage for the PR-description reviewer context, end-to-end context preservation, evidence-state preservation, and keeping fixed reviewer fields out of non-PR profiles.
- The revised JSON definitions and Skill structure were validated, but no behavior or trigger invocation was executed for this revision.
- The earlier pass totals are historical evidence and are superseded for the changed PR-description contract.

## Current definition boundary

The migrated behavior definitions have been validated for structure and Runner plan generation, but have not been executed with a model.\
Real Git scope selection remains unverified by the current executable cases.\
If a change to local or range selection makes this boundary decision-relevant, run the affected cases in disposable repositories with a staged index and the required commit and branch refs, and record the candidate revision and results separately from the historical evidence.
