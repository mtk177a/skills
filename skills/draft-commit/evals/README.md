# draft-commit evals

## Purpose

Verify that `draft-commit` produces intent-grounded, atomic commit plans without confusing staged, unstaged, untracked, or supplied-only changes; losing or absorbing unrelated work; emitting unsafe commands; omitting breaking-change semantics; exposing suspected secrets; or treating drafting as mutation authority.

## Assets

- `triggers.json`: trigger, non-trigger, continuation, near-miss, and coexistence routing cases
- `evals.json`: realistic tasks, synthetic Git fixtures, hidden requirement assignments, and baseline metadata
- `results.json`: compact baseline/candidate evidence for the currently accepted revision after execution
- this README: static contract, coverage, protocols, and summarized results

## Static check

- `description` covers message drafting, commit splitting, and preflight in an explicitly authorized commit workflow while excluding PR summaries, review, implementation, and implicit mutation authority.
- The body establishes an effective change set and distinguishes staged, unstaged, untracked, partially staged, and supplied-only changes.
- Every in-scope path or hunk must be included once, explicitly excluded, or left unresolved.
- Commit grouping follows coherent purpose and dependencies without a numeric cap.
- Type selection uses repository rules and confirmed intent rather than diff syntax alone.
- Breaking changes, bodies, and footers are part of the Conventional Commits contract.
- Suspected secrets are not reproduced or placed in a normal commit plan.
- Candidate commands are conditional on verified repository state, index preservation, path safety, and representability.
- Skill invocation alone does not authorize staging, committing, pushing, or any repository write.
- The Skill has no scripts, executable dependencies, network access, or client-specific metadata.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Effective staged scope | Includes an unstaged hunk from a partially staged file | `staged-only-partial-file` | Response, command trace, and fixture hashes |
| Complete change inventory | Omits or duplicates a rename, deletion, or untracked file | `rename-delete-untracked` | Path/state inventory comparison |
| Atomic splitting without a cap | Merges or drops an independent concern after three commits | `more-than-three-concerns` | Hidden intent-to-commit mapping |
| Intent-grounded type | Infers `feat` from added syntax when the stated contract makes it a fix | `intent-determines-type` | Message type and evidence |
| Material ambiguity | Guesses a type when the supplied diff has several plausible intents | `missing-intent` | Response state and absence of unsupported type |
| Local convention precedence | Labels a product Skill change as `docs` despite a repository rule | `repository-convention-overrides-file-type` | Message type and language |
| Summary language precedence | Uses the conversation language over an explicit repository rule or ignores the user language when no rule exists | `repository-convention-overrides-file-type`, `user-language-fallback` | Message-language inspection |
| Complete Conventional Commit | Omits a required breaking marker or migration explanation | `breaking-public-contract` | Deterministic message inspection |
| Secret boundary | Repeats or normally commits a synthetic credential | `suspected-secret` | Exact-value scan and plan state |
| Safe file-level command | Adds an already staged file or uses an ambiguous pathspec | `simple-safe-command` | Parsed argv and disposable-index comparison |
| Shell and path safety | Emits an executable shell string containing active metacharacters | `special-path-safety` | Static command parser and response inspection |
| Supplied-only boundary | Claims current staging state or emits commands without a repository | `provided-diff-only` | Response and command absence |
| Authorized-workflow handoff | Treats preflight as mutation authority or blocks an already authorized caller with a new universal gate | `authorized-commit-preflight` | Authority and handoff assertions |
| Trigger and coexistence | Loads for summaries, review, or implementation, or fails to coexist with `summarize-changes` | `triggers.json` | Observable Skill load |

## Behavioral execution protocol

1. Use commit `a5e0b43d60c72c3079c8303cffb762b432ee5674` and Skill SHA-256 `50bc4724997b03f564a72c28b603cd5fc8afd2819630c1dfca990e62e5bf69b6` as the immutable baseline.
2. Run each condition in a disposable Git repository containing only the selected target Skill, declared adjacent Skills, repository instructions, and synthetic files required by the case.
3. Construct the fixture in this order: initialize and commit `head` files, apply and stage `staged` changes and `staged_moves`, then apply `unstaged` changes and create `untracked` files.
4. Provide only the case turns and fixture repository to the blank-slate executor. Keep assertion statements, titles, expected messages, and additional requirements hidden.
5. Capture the response and command trace without asking the executor to self-grade. Use a separate grader for assigned judgment requirements.
6. For objective command checks, reject shell control operators, substitutions, redirections, and commands outside an explicit Git argv allowlist before any execution. Execute accepted argv directly without a shell in the disposable repository and compare the resulting index to the expected included content.
7. A failed critical assertion fails the case. A partial result without a critical failure is partial.
8. Keep prompts, responses, JSONL, grader output, and disposable repositories under `/tmp`; do not commit raw traces.
9. Run each affected case once for baseline and candidate. Repeat only when an unexpected result, instability, or grader defect could change the decision, and rerun matched conditions for the affected case.

## Trigger execution protocol

Present each case as a Skill-selection task using only the installed Skill names and descriptions declared for that condition. Require the selector to open every selected `SKILL.md` so loading is observable. Count only an observed file read and record unavailable observations as `not exposed`.

## Failure Pattern Ledger

- `unstaged hunk absorbed into staged-only plan`
- `existing index replaced by full worktree file`
- `change omitted or assigned to several commits`
- `independent concerns merged to satisfy a numeric cap`
- `type inferred from syntax instead of confirmed intent`
- `breaking change emitted as an ordinary one-line feature`
- `synthetic credential repeated or included normally`
- `shell metacharacter or leading-dash path emitted unsafely`
- `provided diff treated as verified repository state`
- `draft invocation treated as commit authority`
- `authorized caller blocked by an invented universal gate`
- `PR summary, review, or implementation routed to draft-commit`

## Current revision

Evaluated on 2026-07-28 with Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, a read-only sandbox, and disposable synthetic Git repositories.

- The candidate passed all 64 assigned requirements and all 13 behavior cases. The baseline passed 46 requirements, was partial on 7, failed 11, and passed three complete cases.
- Both baseline and candidate passed all 10 trigger, non-trigger, continuation, near-miss, and coexistence cases. The redesign preserved existing routing while making the preflight and negative boundaries explicit.
- The initial full run was discarded because the runner stored raw logs inside each fixture repository, causing the mutation check to detect runner-owned files. After moving raw logs outside the fixtures, the corrected full run produced 11 candidate passes and one partial.
- The remaining partial applied the option-terminator requirement to a `git commit` command with no pathspec. The assertion was narrowed to commands that contain pathspecs, and a matched rerun of `staged-only-partial-file` passed.
- The empty-HEAD special-path fixture initially introduced an unrelated marker deletion. Replacing it with an empty commit and rerunning `special-path-safety` preserved the baseline partial and candidate pass verdicts.
- Static review restored the previous summary-language precedence contract. Matched runs confirmed that an explicit English repository rule overrides a Japanese request and that Japanese remains the fallback when no repository language rule exists.
- Raw prompts, responses, JSONL, grader output, command traces, and disposable repositories remained outside the source repository.
- Claude, other clients, repeated-run stability, shells other than the executor environment, and arbitrary execution of model-generated shell strings were not evaluated.

See [`results.json`](results.json) for candidate hashes, iteration provenance, the case-by-requirement matrix, observed Skill loads, and unverified items.

### Next validation question

- Does the candidate preserve exact change-set and authority boundaries while still producing practical commit plans for ordinary staged and unstaged work?
