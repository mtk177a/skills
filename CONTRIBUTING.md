# Contributing Guide

For the maintainer and AI agents working on the maintainer’s behalf.\
External contributions are not normally expected.

Follow [Issue tracking and preparation](#make-a-change) → [verification](#verify-the-change) → [commit and PR](#commit-and-open-a-pull-request).\
For message syntax, see [commit messages and PR titles](#commit-messages-and-pull-request-titles).

## Make a change

### Track the work in an Issue

Use an existing [GitHub Issue](https://github.com/mtk177a/skills/issues) or open one for the work.

- **Content**: purpose, scope, and completion criteria, using the applicable [Issue template](.github/ISSUE_TEMPLATE/default.md) sections.
- **Language**: title and `Summary` in English; other sections in Japanese by default.
- **Exception**: omit tracking only when the maintainer explicitly instructs you to do so.

### Check before changing files

Read the applicable repository instructions and the files, implementation, and documentation affected by the request.\
Check the working tree so existing changes remain distinguishable from this work.\
For a Skill change, follow the structure and authoring rules in [AGENTS.md](AGENTS.md) and [the Skill authoring guide](docs/maintainers/authoring.md).

### Verify the change

Choose checks that cover the changed behavior and its relevant failure conditions.\
Run the repository checker and tests for retained code as required by [AGENTS.md](AGENTS.md).\
Verify the results and safety boundaries of the work performed.\
Record the checks performed, their results, and material gaps in the pull request.\
Do not present an unrun check as a passing result.

Run from the repository root:

```bash
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests
git diff --check
```

The read-only checker covers structure, metadata, links, translation notices, companion relationships, and deployment artifacts.\
It exits with `0` for consistency, `1` for actionable inconsistencies, or `2` for invocation or execution failures.\
For distribution changes, also follow the [archive and APM checks](docs/maintainers/packaging.md).

## Commit and open a pull request

Commit in units whose purpose and verification can be followed without mixing unrelated changes.\
Use the [PR template](.github/pull_request_template.md) to describe the result and verification.

- **Issue link**: `Closes #123` when completed by the PR, or `Refs #123` for a reference only.
- **Language**: `Summary` in English; other sections in Japanese by default.

### Commit messages and pull request titles

Use Conventional Commits form for commit messages created or edited in this repository and for pull request titles.\
The pull request title describes its overall purpose; each commit summary describes that commit's change.

GitHub-generated merge commits and unedited Dependabot-generated titles and commit messages are exempt.\
If a generated title or message is edited, follow this convention.

#### Form

```text
<type>(<scope>): <English summary>
<type>: <English summary>
<type>(<scope>)!: <English summary>
<type>!: <English summary>
```

- Write a short, specific English summary of the result without a final period.
- Use `!` only when the change is breaking; explain the break in the commit body or pull request description as applicable.
- Choose `type` from the primary purpose and result, not the file extension or number of changed lines.\
  Include supporting tests and documentation under that purpose.
- If a summary would list independent purposes, reconsider the change unit.\
  When changes must be handled together, name the primary purpose in the title and explain the relationship in the pull request body.

#### Types

| `type` | Primary purpose |
| --- | --- |
| `feat` | Add a maintained Skill, user-facing behavior, or operational capability |
| `fix` | Correct a confirmed defect or departure from intended behavior |
| `docs` | Improve explanation, instructions, or reference material without changing the behavior of a maintained Skill |
| `chore` | Update dependencies, configuration values, or maintenance policy without adding a capability or fixing a defect |
| `refactor` | Reorganize structure without changing behavior |
| `test` | Change tests as the primary purpose without changing maintained behavior |
| `ci` | Change CI configuration or execution conditions as the primary purpose |

Skill instructions define behavior even though they are written as text.\
Use the `type` that matches the addition, correction, or restructuring of those instructions; reserve `docs` for changes whose primary purpose is explanatory.\
An intentional change to a working configuration's policy or value is not a `fix` without a confirmed defect.

#### Scopes

Use a short `scope` that identifies the main thing changed.\
Omit it when a change spans several targets with no single center.\
Choose a name for the Skill, capability, configuration, or policy rather than a file type or directory.\
Use the same `scope` for related documentation and scripts.

These are examples, not an exhaustive list.\
Reuse an existing name for the same target rather than inventing an alias.

| `scope` | Target |
| --- | --- |
| `clarify-request` | The `clarify-request` Skill and its related assets |

#### Examples

```text
fix(clarify-request): align clarification boundaries
docs: clarify repository verification steps
refactor: distribute Skills as a native APM bundle
```
