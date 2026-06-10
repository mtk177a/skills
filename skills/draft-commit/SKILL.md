---
name: draft-commit
description: Generate commit message drafts or commit split proposals from a diff.
license: MIT
---

# Draft Commit

## Purpose

- Generate commit proposals in Conventional Commits format from a diff.

## When to use

- When you want to write a commit message
- When you want to organize how to split changes into commits
- When you want to separate changes by concern before committing

## Input

- The commit convention explicitly stated in the target repository
- The language used by the user when no repository language convention exists
- `git status -sb`
- `git diff --stat`
- `git diff -- <path>` for only the files needed
- `git diff --staged -- <path>` for only the files needed
- Contents of untracked files

## Steps

1. First confirm the commit convention explicitly stated in the target repository; if there are local rules for commit type, scope, or summary language, follow them instead.
2. Use `git status -sb` to understand the types and count of changed files.
3. Use `git diff --stat` and, if needed, `git diff --staged --stat` to understand the diff size.
4. Do not read the full diff immediately; check only the needed files with `git diff -- <path>` or `git diff --staged -- <path>`.
5. For untracked files, check only those whose content needs to be confirmed.
6. If there are multiple concerns, consider splitting commits by file or feature.
7. Narrow the primary purpose of each commit to one.
8. Draft each commit proposal in Conventional Commits format.
9. Confirm the summary is short and specific. Use the target repository's required language; otherwise use the user's language. If neither can be determined, ask before drafting.
10. Add scope only when there is an explicit convention; do not add it when the convention is unknown.
11. For diffs that include renames / moves, check the delete on the old path as well as the new path; include both old and new paths in `git add`. Do not include unrelated existing diffs.
12. For each commit proposal, provide `git add ...` and `git commit -m "..."` in a form that can be run as-is.
13. Limit proposals to at most 3.
14. For detailed type selection, refer to `references/commit-types.md`.
15. Consider using another agent only when the diff spans multiple concerns and the user requests additional confirmation.

## Output format

```text
<commit 1>
<type>(<optional-scope>): <summary>
files: <file1>, <file2>
git add <file1> <file2>
git commit -m "<type>(<optional-scope>): <summary>"

<commit 2>
<type>(<optional-scope>): <summary>
files: <file1>, <file2>
git add <file1> <file2>
git commit -m "<type>(<optional-scope>): <summary>"
```

## Type selection guide (examples)

- Check the target repository's explicit convention first; it takes precedence over this list
- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation update
- `style`: code formatting that does not affect behavior
- `refactor`: structural improvement without behavior change
- `perf`: performance improvement
- `test`: adding or modifying tests
- `build`: build or dependency changes
- `ci`: CI-related changes
- `chore`: miscellaneous or auxiliary changes

## Boundaries

### Always:

- Base proposals on the diff
- Check the target repository's explicit commit convention first
- Choose the summary language in this order: target repository convention, then the user's language
- When there are multiple concerns, propose splitting
- Start from `git status -sb` and `git diff --stat`
- Read only the needed files with individual diffs
- Limit proposals to at most 3
- For diffs with renames / moves, explicitly state the staging approach for old path / new path and unrelated existing diffs
- Attach `files:` to each commit proposal
- Attach `git add ...` and `git commit -m "..."` to each commit proposal

### Ask first:

- When the diff cannot be obtained
- When the primary purpose cannot be identified from the diff
- When neither the target repository convention nor the user's language determines the summary language
- When the diff spans multiple concerns and you want to use another agent for additional confirmation

### Never:

- Actually execute the commit
- Propose based on guesses without reading the diff
