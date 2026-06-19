---
name: refresh-apm-lockfile
description: Use only in the mtk177a/skills repository after Skill or apm.yml changes have been committed and pushed, to refresh apm.lock.yaml from a disposable copy without deploying APM packages into the working repository.
license: MIT
---

# Refresh APM Lockfile

## Purpose

- Refresh this repository's `apm.lock.yaml` after changing public Skills or `apm.yml`.
- Keep non-dry-run APM operations out of the working repository by using a disposable copy.
- Copy only the generated `apm.lock.yaml` back, then leave the lockfile commit to the user or calling agent.

## When to use

- You are in the `mtk177a/skills` repository.
- A public Skill was added, removed, renamed, or changed in a way that requires `apm.yml` / `apm.lock.yaml` consistency.
- The Skill and manifest change has already been committed and pushed.
- The next task is refreshing `apm.lock.yaml` as a separate commit.
- The user mentions APM lockfile refresh, disposable copy, `apm update`, or this repository's self-referential APM dependency workflow.

## Preconditions

- The working tree is clean before starting.
- No tracked, staged, untracked, or ignored APM deployment artifacts are present in the working repository.
- `.agents/skills/` contains no entries except the tracked repo-local `refresh-apm-lockfile` Skill.
- `apm_modules/` does not exist.
- The current branch has an upstream.
- `HEAD` matches the upstream branch.
- `apm.yml` and `apm.lock.yaml` exist at the repository root.
- Non-dry-run `apm install` / `apm update` must not run in the working repository.

## Steps

1. Confirm the preconditions.
2. Use `scripts/refresh-apm-lockfile.sh` from the repository root.
3. If the script needs network, SSH, or credential access and sandboxing blocks it, rerun the same script with the required approval.
4. Confirm the working-repository diff is either empty or only `apm.lock.yaml`.
5. Confirm `apm install --frozen --dry-run --no-policy` and `git diff --check` passed.
6. If the lockfile was already current and no diff remains, stop without creating a commit.
7. Otherwise, commit only `apm.lock.yaml` separately, usually with `fix: refresh APM lockfile after <change>`.
8. Push the lockfile commit only after reviewing the diff.

## Script contract

Run:

```bash
bash .agents/skills/refresh-apm-lockfile/scripts/refresh-apm-lockfile.sh
```

The script:

- creates a disposable copy under `/tmp`
- tries `apm update --yes` in the disposable copy
- falls back to `apm install --update --ssh --no-policy` when the lockfile was not actually refreshed
- copies only `apm.lock.yaml` back to the working repository
- verifies the lockfile with `apm install --frozen --dry-run --no-policy`
- verifies whitespace with `git diff --check`
- exits successfully without a commit instruction when `apm.lock.yaml` was already current

The script does not:

- edit `apm.yml`
- run non-dry-run APM commands in the working repository
- copy `.agents/skills/` output back from the disposable copy
- commit or push

## Output format

- Preconditions: ...
- Disposable copy: ...
- APM command used: ...
- Resolved commit in lockfile: ...
- Working repository diff: ...
- Verification:
  - `apm install --frozen --dry-run --no-policy`: ...
  - `git diff --check`: ...
- Next action:
  - `git add apm.lock.yaml`
  - `git commit -m "fix: refresh APM lockfile after <change>"`
  - or "no commit needed" when the lockfile was already current

## Boundaries

### Always:

- Keep this Skill repository-local.
- Use a disposable copy for non-dry-run APM operations.
- Copy only `apm.lock.yaml` back into the working repository.
- Stop if the working tree is dirty before the refresh, including untracked files.
- Stop if ignored APM deployment artifacts such as `apm_modules/` or non-exception `.agents/skills/*` entries are present.
- Stop if `HEAD` is not pushed to the upstream branch.
- Leave commit and push as explicit follow-up actions.

### Ask first:

- When the lockfile refresh would require changing `apm.yml`.
- When the script would need to overwrite any file other than `apm.lock.yaml`.
- When authentication, network, or policy errors require a different APM command.

### Never:

- Do not run non-dry-run `apm install` or `apm update` in the working repository.
- Do not commit `.agents/skills/` output produced by APM integration.
- Do not commit or push automatically.
- Do not add this repo-local Skill to the public Skill catalog or `apm.yml`.
