# refresh-apm-lockfile evals

## Iter 0 - Static check

- description and body are internally consistent on refreshing this repository's APM lockfile from a disposable copy
- output format includes preconditions, disposable copy, APM command used, resolved commit, verification, and next action
- the Skill is repository-local and is not added to the public Skill catalog or `apm.yml`
- at least one `[critical]` assertion is identified: never run non-dry-run APM commands in the working repository

## Scenarios

### Scenario A: Public Skill was added and pushed

A public Skill and `apm.yml` were changed, committed, and pushed. The executor must refresh only `apm.lock.yaml` from a disposable copy.

Requirements checklist:
1. [critical] Run non-dry-run APM commands only in a disposable copy
2. Copy only `apm.lock.yaml` back to the working repository
3. Verify `apm install --frozen --dry-run --no-policy`
4. Leave commit and push as follow-up actions

### Scenario B: Working tree is dirty

The working repository has unrelated changes before the refresh. This includes tracked changes, staged changes, untracked files, `apm_modules/`, and `.agents/skills/*` entries other than `refresh-apm-lockfile`. The executor must stop rather than mixing the lockfile update with other work or stale APM deployment artifacts.

Requirements checklist:
1. [critical] Stop before creating the disposable copy
2. Report that the working tree or APM deployment artifacts must be cleaned first
3. Do not run non-dry-run APM commands

### Scenario C: HEAD is not pushed

The local commit containing Skill or manifest changes is ahead of upstream. The executor must stop because APM resolves this repository through GitHub.

Requirements checklist:
1. [critical] Detect that `HEAD` does not match upstream
2. Tell the caller to push the Skill / manifest commit first
3. Do not update `apm.lock.yaml`

### Scenario D: `apm update --yes` does not refresh the lockfile

`apm update --yes` exits successfully but the disposable lockfile still points at the old commit or lacks a new dependency. The executor must use the fallback command in the disposable copy.

Requirements checklist:
1. [critical] Check dependency count and resolved commit after `apm update --yes`
2. Fall back to `apm install --update --ssh --no-policy`
3. Still copy back only `apm.lock.yaml`

### Scenario E: Lockfile is already current

The disposable refresh produces an `apm.lock.yaml` identical to the working repository's existing lockfile. The executor must treat this as a successful no-op.

Requirements checklist:
1. [critical] Exit successfully after verification
2. Report that no working repository diff remains
3. Do not print a commit command as the next required action

## Failure Pattern Ledger

- `non-dry-run apm command run in working repo`
- `dirty working tree mixed with lockfile update`
- `untracked file ignored by precondition check`
- `ignored APM deployment artifact ignored by precondition check`
- `local unpushed commit used before GitHub can resolve it`
- `apm update claimed success but lockfile stayed stale`
- `.agents/skills output copied back from disposable copy`
- `lockfile commit and Skill commit combined`

## Iter N - not yet executed

Scenarios have not been executed. Execution results will be recorded here once run.
