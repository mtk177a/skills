# Commit Types Reference

> **Attribution:** This file is an original summary authored for this repository.
> The message structure and type semantics are based on the [Conventional Commits specification](https://www.conventionalcommits.org) (CC BY 3.0).

Use this reference when `draft-commit` needs a non-obvious type, breaking-change marker, body, or footer decision. An explicit target-repository convention always takes precedence.

## Decision sequence

1. Identify the commit's confirmed primary intent. Do not infer intent from file extension or syntax alone.
2. Determine the user-visible or consumer-visible semantic effect.
3. Determine whether the change preserves backward compatibility.
4. Apply the target repository's type, scope, release, and language rules.
5. Select the type and decide whether the message needs a body, footer, or breaking-change marker.

If two types remain plausible because intent is missing, ask or leave the type unresolved. Do not choose whichever type appears first in this reference.

## Common types

| Type | Primary intent | Distinguishing evidence |
| --- | --- | --- |
| `feat` | Add a new capability or supported behavior | A consumer can do something newly intended |
| `fix` | Restore behavior that should already have worked | Existing expectation, contract, or documented behavior was violated |
| `refactor` | Improve internal structure without intending to change observable behavior | Public behavior and compatibility remain the same |
| `perf` | Improve performance without changing the intended result | Time, memory, throughput, or resource use is the primary change |
| `docs` | Change documentation or comments only | No product, build, test, or operational behavior changes under the repository convention |
| `test` | Add or change tests without changing production behavior | Test coverage or test infrastructure is the primary change |
| `build` | Change build system, packaging, or dependencies | Artifact construction or dependency resolution is the primary change |
| `ci` | Change continuous-integration configuration or automation | CI execution is the primary change |
| `style` | Change formatting without semantic effect | Whitespace, formatting, or equivalent presentation-only code changes |
| `chore` | Perform repository maintenance not represented by a more specific allowed type | The repository convention permits `chore` for that maintenance purpose |

Repositories may define different or additional meanings. In particular, a repository may treat a Skill, schema, configuration, or documentation file as a product surface whose behavioral change is `feat` or `fix`; do not override that rule based on the filename.

## Ambiguous cases

- A null guard is `fix` when it restores an existing expectation, `feat` when accepting the input is new supported behavior, and `refactor` only when observable behavior is intentionally unchanged.
- A dependency update is not automatically `build`; use the type that represents its primary product effect when the repository convention requires that.
- A UI appearance change is `feat` when it intentionally changes the experience, `fix` when it repairs a defect, and `style` only when it is code formatting with no visible effect.
- Moving or renaming files is `refactor` only when structure is the primary purpose and behavior remains unchanged. Otherwise use the type of the behavior delivered by the move.
- Generated files, lockfiles, and documentation can belong in the same commit as the behavior they support when they are inseparable consequences rather than independent concerns.

## Breaking changes

A breaking change alters a public API, schema, configuration contract, supported environment, data format, migration requirement, or other consumer expectation incompatibly.

Mark it with either:

```text
feat(api)!: remove the legacy endpoint
```

or:

```text
feat(api): replace the legacy endpoint

BREAKING CHANGE: clients must migrate from `/v1/legacy` to `/v2/current`.
```

The breaking marker is independent of the type. A `fix`, `refactor`, or other allowed type can still be breaking.

## Body and footers

Use a body when the subject cannot carry decision-relevant context such as why the change was needed, how two changes relate, or what migration is required. Keep the subject concise and put the additional explanation after a blank line.

Use footers for structured metadata required by the target workflow, such as:

- `BREAKING CHANGE: <description>`
- `Refs: #123`
- another trailer explicitly required by the repository

Do not invent issue references, co-author lines, release notes, or other trailers that are not supported by evidence or repository policy.
