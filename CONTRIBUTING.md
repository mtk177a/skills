# Contributing Guide

This guide is for the maintainer of this personal repository and AI agents working on the maintainer's behalf.\
External contributions are not normally expected.\
It covers how to track, check, and submit changes, including commit messages and pull request titles.

## Make a change

### Track the work in an Issue

Track work in [GitHub Issues](https://github.com/mtk177a/skills/issues), using an existing Issue or opening one for the work.\
Only omit Issue tracking when the maintainer explicitly instructs you to do so.\
State the purpose, scope, and completion criteria, and use the applicable sections of the [Issue template](.github/ISSUE_TEMPLATE/default.md).\
Write the Issue title and `Summary` in English; write the remaining sections in Japanese by default, as specified by the template.

### Check before changing files

Read the applicable repository instructions and the files, implementation, and documentation affected by the request.\
Check the working tree so existing changes remain distinguishable from this work.\
For a Skill change, follow the structure and authoring rules in [AGENTS.md](AGENTS.md) and [the Skill authoring guide](docs/authoring.md).

### Verify the change

Choose checks that cover the changed behavior and its relevant failure conditions.\
Run the repository checker and unit tests when required by [AGENTS.md](AGENTS.md); select Skill evaluations according to [the evaluation guide](docs/evaluation.md).\
Record the checks performed, their results, and material gaps in the pull request.\
Do not present an unrun check as a passing result.

## Commit and open a pull request

Commit in units whose purpose and verification can be followed without mixing unrelated changes.\
When opening a pull request, use the [pull request template](.github/pull_request_template.md) to describe the result and verification.\
Link an Issue with `Closes #123` when the pull request completes it, or `Refs #123` when it only refers to it.\
Write the pull request `Summary` in English and the remaining sections in Japanese by default, as specified by the template.

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
| `test` | Change tests or evaluation tooling as the primary purpose without changing maintained behavior |
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
| `evaluation` | Shared Skill evaluation behavior and tooling |

#### Examples

```text
feat(evaluation): add a cost-bounded Skill evaluation runner
fix(clarify-request): align clarification boundaries
docs: explain change-aware evaluation selection
refactor: distribute Skills as a native APM bundle
```
