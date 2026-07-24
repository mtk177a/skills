---
name: refresh-apm-lockfile
description: Use only in the mtk177a/skills repository after public Skill or apm.yml changes have been committed and pushed, to generate and verify apm.lock.yaml in a disposable copy without deploying APM packages into the working repository.
license: MIT
---

# Refresh APM Lockfile

## Purpose

- Refresh this repository's `apm.lock.yaml` after changing public Skills or `apm.yml`.
- Keep non-dry-run APM operations out of the working repository by using a disposable copy.
- Verify the generated lockfile with a frozen install and audit before copying it back.
- Copy only the generated `apm.lock.yaml` back, then leave the lockfile commit to the user or calling agent.

## When to use

- You are in the `mtk177a/skills` repository.
- A public Skill under `skills/` or `apm.yml` was added, removed, renamed, or changed since the commit recorded in the current lockfile.
- The public source change has already been committed and pushed.
- The next task is refreshing `apm.lock.yaml` as a separate commit.
- The user mentions APM lockfile refresh, a disposable copy, or this repository's self-referential APM dependency workflow.

Do not use this Skill after changes limited to repository guidance, repo-local Skills, unrelated documentation, or `apm.lock.yaml` itself. The script detects this case and exits successfully without contacting the package source.

## Preconditions

- The working tree is clean before starting.
- No tracked, staged, untracked, or ignored APM deployment artifacts are present in the working repository.
- `.agents/skills/` contains no entries except the tracked repo-local `refresh-apm-lockfile` Skill.
- `apm_modules/` does not exist.
- The current branch has an upstream.
- `HEAD` matches the upstream branch.
- `apm.yml` and `apm.lock.yaml` exist at the repository root.
- The installed APM CLI supports `apm lock`.
- Non-dry-run `apm install` / `apm update` must not run in the working repository.

## Steps

1. Confirm the preconditions.
2. Use `scripts/refresh-apm-lockfile.sh` from the repository root.
3. If the script needs network, SSH, or credential access and sandboxing blocks it, rerun the same script with the required approval.
4. If the script reports that no public source changed, stop without creating a disposable copy or commit.
5. Otherwise, confirm the disposable lock generation, frozen install, and audit passed.
6. Confirm the working-repository diff is either empty or only `apm.lock.yaml`.
7. Confirm the working-repository frozen dry-run and `git diff --check` passed.
8. If no diff remains, stop without creating a commit.
9. Otherwise, commit only `apm.lock.yaml` separately, usually with `fix: refresh APM lockfile after <change>`.
10. Push the lockfile commit only after reviewing the diff.

## Script contract

Run:

```bash
bash .agents/skills/refresh-apm-lockfile/scripts/refresh-apm-lockfile.sh
```

The script:

- compares the public source under `skills/` and `apm.yml` with the commit recorded in the current lockfile
- exits successfully when no public source changed
- creates a disposable copy under `/tmp` when a refresh is required
- runs `apm lock --update --no-policy` in the disposable copy
- verifies dependency count and that every dependency resolves to the pushed `HEAD`
- runs `apm install --frozen --no-policy` and `apm audit --ci --no-policy` in the disposable copy
- copies only the verified `apm.lock.yaml` back to the working repository
- verifies the working repository with `apm install --frozen --dry-run --no-policy`
- verifies whitespace with `git diff --check`
- exits successfully without a commit instruction when `apm.lock.yaml` was already current

The script does not:

- edit `apm.yml`
- run non-dry-run APM commands in the working repository
- fall back to an update or install command when lock generation or verification fails
- copy `.agents/skills/` output back from the disposable copy
- commit or push

## Output format

- Preconditions: ...
- Public source delta: refresh required | no refresh required
- Disposable copy: ... | not created
- APM command used: ... | not run
- Resolved commit in lockfile: ...
- Working repository diff: ...
- Verification:
  - disposable `apm install --frozen --no-policy`: ...
  - disposable `apm audit --ci --no-policy`: ...
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
- Treat lock generation, dependency, install, audit, authentication, network, and policy errors as hard failures; preserve the disposable copy for inspection.
- Leave commit and push as explicit follow-up actions.

### Ask first:

- When the lockfile refresh would require changing `apm.yml`.
- When the script would need to overwrite any file other than `apm.lock.yaml`.
- When a failure appears to require a different APM command or distribution workflow.

### Never:

- Do not run non-dry-run `apm install` or `apm update` in the working repository.
- Do not substitute `apm update` or `apm install --update` for lock generation.
- Do not commit `.agents/skills/` output produced by APM integration.
- Do not commit or push automatically.
- Do not add this repo-local Skill to the public Skill catalog or `apm.yml`.
