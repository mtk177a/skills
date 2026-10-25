# Contributing Guide

This guide is for the maintainer and the agents working for the maintainer.\
External contributions are not normally expected.

A change goes through these steps: [track it in an Issue](#track-the-work-in-an-issue), [check before changing files](#check-before-changing-files), [verify it](#verify-the-change), and [commit and open a pull request](#commit-and-open-a-pull-request).

## Track the work in an Issue

Use an existing [GitHub Issue](https://github.com/mtk177a/skills/issues) or open one for the work.

- **Content**: purpose, scope, and completion criteria, using the applicable sections of the [Issue template](.github/ISSUE_TEMPLATE/default.md).
- **Language**: the title and `Summary` in English; other sections in Japanese by default.
- **Exception**: skip the Issue only when the maintainer explicitly says to.

## Check before changing files

Read the applicable repository instructions and the files, implementation, and documentation affected by the request.\
Check the working tree so that existing changes stay distinguishable from this work.

For a Skill change, follow [AGENTS.md](AGENTS.md) and the [Skill authoring guide](docs/maintainers/authoring.md), including [Update related documents](docs/maintainers/authoring.md#update-related-documents).\
When you change an English source, update its Japanese reference translation as described in [Languages and Japanese reference translations](docs/maintainers/localization.md#update-translations-when-the-source-changes).

## Verify the change

Choose checks that cover the changed behavior and the conditions under which it could fail.\
Also verify the results of the work and its safety boundaries.\
Record the checks performed, their results, and material gaps in the pull request.\
Do not report a check you did not run as passed.

Before committing, run these from the repository root:

```bash
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests
git diff --check
```

`check_repository.py` only reads files.\
It checks Skill structure and metadata, the README catalogs, the upstream mirror hashes, links and anchors, translation notices, companion relationships, Skill name references, personal absolute paths, and files that APM deploys into this repository.\
It exits with `0` when nothing is wrong, `1` when it finds problems to fix, and `2` when it cannot run.

When you change how the Skills are installed or build a new plugin version, also follow [Build the plugin ZIP](docs/maintainers/packaging.md).

## Commit and open a pull request

Commit in units whose purpose and verification can be followed, without mixing in unrelated changes.\
Describe the result and verification in the pull request using the [PR template](.github/pull_request_template.md).

- **Issue link**: `Closes #123` when the PR completes the Issue, or `Refs #123` when it only refers to it.
- **Language**: `Summary` in English; other sections in Japanese by default.

### Commit messages and pull request titles

Use the Conventional Commits form for the commit messages you create or edit in this repository and for pull request titles.\
A pull request title describes the overall purpose of the pull request, and each commit summary describes the change in that commit.

GitHub-generated merge commits and unedited Dependabot titles and commit messages are exempt.\
If you edit a generated title or message, follow this convention.

#### Form

```text
<type>(<scope>): <English summary>
<type>: <English summary>
<type>(<scope>)!: <English summary>
<type>!: <English summary>
```

- Write a short, specific English summary of the result, without a final period.
- Use `!` only for a breaking change, and explain the break in the commit body or the pull request description.
- Choose `type` from the primary purpose and result, not from the file extension or the number of changed lines.\
  Tests and documentation that support that purpose take the same `type`.
- If a summary would have to list independent purposes, reconsider how the change is split.\
  When changes must be handled together, name the primary purpose in the title and explain how the changes relate in the pull request body.

#### Types

| `type` | Primary purpose |
| --- | --- |
| `feat` | Add a maintained Skill, behavior for people who use the Skills, or a maintenance capability |
| `fix` | Correct a confirmed defect or a departure from intended behavior |
| `docs` | Improve explanation, instructions, or reference material without changing the behavior of a maintained Skill |
| `chore` | Update dependencies, configuration values, or maintenance policy without adding a capability or fixing a defect |
| `refactor` | Reorganize structure without changing behavior |
| `test` | Change tests as the primary purpose without changing maintained behavior |
| `ci` | Change CI configuration or execution conditions as the primary purpose |

Skill instructions are text, but they define behavior.\
For a change that adds, corrects, or restructures those instructions, use the `type` that matches that change, and keep `docs` for changes whose primary purpose is explanation.\
Intentionally changing the policy or a value of a configuration that works is not a `fix` unless it corrects a confirmed defect.

#### Scopes

Use a short `scope` that names the main thing changed.\
Omit it when the change spans several targets with no single center.\
Name the Skill, capability, configuration, or policy, not a file type or directory.\
Use the same `scope` for the related documentation and scripts.

The table below gives examples, not a complete list.\
Reuse an existing name for the same target instead of inventing another.

| `scope` | Target |
| --- | --- |
| `clarify-request` | The `clarify-request` Skill and its related files |
| `readme` | `README.md` and its Japanese reference translation |

#### Examples

```text
fix(clarify-request): align clarification boundaries
docs: clarify repository verification steps
refactor: distribute Skills as a native APM bundle
```
