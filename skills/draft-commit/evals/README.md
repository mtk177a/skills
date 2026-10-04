# draft-commit evals

## Purpose

Verify that `draft-commit` produces intent-grounded, atomic commit plans without confusing staged, unstaged, untracked, or supplied-only changes; losing or absorbing unrelated work; emitting unsafe commands; omitting breaking-change semantics; exposing suspected secrets; or treating drafting as mutation authority.

## Assets

- `triggers.json`: trigger, non-trigger, continuation, near-miss, and coexistence routing cases
- `evals.json`: executable `{skill_name, evals}` behavior cases with synthetic inputs and grading requirements
- `results.json`: historical baseline/candidate evidence from the 2026-07-28 evaluation
- this README: static contract, coverage, executable-fixture limits, and historical results

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
| Effective staged scope | Includes an unstaged hunk from a partially staged file | `staged-only-partial-file` | Supplied-state plan; no live index check |
| Complete change inventory | Omits or duplicates a rename, deletion, or untracked file | `rename-delete-untracked` | Supplied-state path inventory |
| Atomic splitting without a cap | Merges or drops an independent concern after three commits | `more-than-three-concerns` | Hidden intent-to-commit mapping |
| Intent-grounded type | Infers `feat` from added syntax when the stated contract makes it a fix | `intent-determines-type` | Message type and evidence |
| Material ambiguity | Guesses a type when the supplied diff has several plausible intents | `missing-intent` | Response state and absence of unsupported type |
| Local convention precedence | Labels a product Skill change as `docs` despite a repository rule | `repository-convention-overrides-file-type` | Message type and language |
| Summary language precedence | Uses the conversation language over an explicit repository rule or ignores the user language when no rule exists | `repository-convention-overrides-file-type`, `user-language-fallback` | Message-language inspection |
| Complete Conventional Commit | Omits a required breaking marker or migration explanation | `breaking-public-contract` | Deterministic message inspection |
| Secret boundary | Repeats or normally commits a synthetic credential | `suspected-secret` | Response redaction and plan state |
| Safe file-level command | Uses an ambiguous pathspec for a whole unstaged file | `simple-safe-command` | Candidate command text; no command execution |
| Shell and path safety | Emits an executable shell string containing active metacharacters | `special-path-safety` | Candidate command text and fixture path |
| Supplied-only boundary | Claims current staging state or emits commands without a repository | `provided-diff-only` | Response and command absence |
| Authorized-workflow handoff | Treats preflight as mutation authority or blocks an already authorized caller with a new universal gate | `authorized-commit-preflight` | Authority and handoff assertions |
| Trigger and coexistence | Loads for summaries, review, or implementation, or fails to coexist with `summarize-changes` | `triggers.json` | Observable Skill load |

## Executable fixture limits

The common Runner creates actual unstaged Git changes for `more-than-three-concerns`, `suspected-secret`, `simple-safe-command`, and `special-path-safety` using `baseline_files` and `fixture.files`. The special-path case adds an unchanged marker file solely to initialize the disposable repository.

The Runner cannot construct staged changes, partially staged files, or staged renames from an evaluation definition. Six cases preserve those changes in `case-git-state.md` as a supplied synthetic snapshot. These cases can test plan reasoning from supplied state, but they cannot verify live Git-index inspection, exact staging commands, or preservation of an actual partially staged index. The earlier disposable-Git evidence for those boundaries remains historical evidence in `results.json`; it is not a result for this definition format or the current candidate.

Select and plan only cases needed for a changed responsibility. Keep Runner artifacts outside this repository. A definition migration alone calls for static validation, not a model run of every case.

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

## Historical evaluation

Evaluated on 2026-07-28 with Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, a read-only sandbox, and disposable synthetic Git repositories. These results predate the executable-definition migration and do not certify the migrated fixtures.

- The candidate passed all 64 assigned requirements and all 13 behavior cases. The baseline passed 46 requirements, was partial on 7, failed 11, and passed three complete cases.
- Both baseline and candidate passed all 10 trigger, non-trigger, continuation, near-miss, and coexistence cases. The redesign preserved existing routing while making the preflight and negative boundaries explicit.
- The initial full run was discarded because the runner stored raw logs inside each fixture repository, causing the mutation check to detect runner-owned files. After moving raw logs outside the fixtures, the corrected full run produced 11 candidate passes and one partial.
- The remaining partial applied the option-terminator requirement to a `git commit` command with no pathspec. The assertion was narrowed to commands that contain pathspecs, and a matched rerun of `staged-only-partial-file` passed.
- The empty-HEAD special-path fixture initially introduced an unrelated marker deletion. Replacing it with an empty commit and rerunning `special-path-safety` preserved the baseline partial and candidate pass verdicts.
- Static review restored the previous summary-language precedence contract. Matched runs confirmed that an explicit English repository rule overrides a Japanese request and that Japanese remains the fallback when no repository language rule exists.
- Raw prompts, responses, JSONL, grader output, command traces, and disposable repositories remained outside the source repository.
- Claude, other clients, repeated-run stability, shells other than the executor environment, and arbitrary execution of model-generated shell strings were not evaluated.

See [`results.json`](results.json) for candidate hashes, iteration provenance, the case-by-requirement matrix, observed Skill loads, and unverified items.

### Remaining validation

The migrated cases have not been run against the current Skill revision. A later change to staging or command guidance would require targeted model evaluation. Live partially staged index preservation still needs a purpose-built disposable-Git check outside the current Runner contract.
