---
name: summarize-changes
description: Summarize a diff into a PR description, release handoff, or shareable summary.
license: MIT
---

# Summarize Changes

## Purpose

- Organize a diff into a PR summary and handoff notes in a shareable form.
- State what changed, why it changed, impact scope, verification status, and remaining issues — producing material ready for review or release decisions.

## When to use

- When you want to write a PR description
- When you want to write a release description or handoff notes
- When you want to briefly share the background and impact of a diff

## Input (optional)

- `git diff`
- `git diff --staged`
- An existing diff text
- Target branch and merge destination branch
- Intended audience

## Steps

1. Confirm the target diff from `git diff`, `git diff --staged`, or an existing diff text.
2. Organize the subject of the change and the intended audience.
3. Write the PR summary.
4. Write the handoff notes.
5. Explicitly state impact, test status, verification status, unconfirmed items, and known risks.
6. If needed, adjust granularity and wording to make it shareable.

## Output format

PR template:

```markdown
# <PR title>

## Summary
- <1–3 line summary>

## Key changes
- <change 1>
- <change 2>

## Impact
- <impact on features / compatibility / operations>

## Tests
- <tests performed / reason if not performed>

## Verification
- <what was verified / reason if not verified>
```

Release Handoff template:

```markdown
# Release Handoff

## Summary
- <target branch / release unit / included changes>

## Notes
- <operational notes>

## Remaining issues
- <unfinished items / known risks / next steps; "none" if nothing>
```

## Companion skills

- `draft-commit`
- `record-session-handoff`

## Boundaries

### Always:

- Base the summary on the diff
- State impact and test status explicitly
- Write unconfirmed items as unconfirmed

### Ask first:

- When the diff cannot be obtained
- When the target branch or audience is unknown and granularity cannot be decided

### Never:

- Summarize based on guesses without reading the diff
- Include secrets in the output
- Proceed to implementation changes or design decisions

## Notes (optional)

- `draft-commit` has commit message drafting as its primary purpose; writing shareable content is not its main responsibility.
- `record-session-handoff` has session continuation notes as its primary purpose; writing PR or release descriptions is separate.
