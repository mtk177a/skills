# refresh-apm-lockfile evals

## Iter 0 - Static check

- description and body are internally consistent on refreshing this repository's APM lockfile from a disposable copy
- output format includes preconditions, public source delta, disposable copy, APM command used, resolved commit, verification, and next action
- the Skill is repository-local and is not added to the public Skill catalog or `apm.yml`
- at least one `[critical]` assertion is identified: never run non-dry-run APM commands in the working repository

## Scenarios

### Scenario A: Public Skill was added and pushed

A public Skill and `apm.yml` were changed, committed, and pushed. The executor must refresh only `apm.lock.yaml` from a disposable copy.

Requirements checklist:
1. [critical] Run non-dry-run APM commands only in a disposable copy
2. Copy only `apm.lock.yaml` back to the working repository
3. Generate the lockfile with `apm lock --update --no-policy`
4. Verify a frozen install and audit in the disposable copy before copying the lockfile
5. Verify `apm install --frozen --dry-run --no-policy` in the working repository
6. Leave commit and push as follow-up actions

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

### Scenario D: Generated lockfile is inconsistent

`apm lock --update --no-policy` exits successfully, but the disposable lockfile points at the wrong commit or has the wrong dependency count. The executor must stop without copying the lockfile or trying another APM command.

Requirements checklist:
1. [critical] Check dependency count and every resolved commit after lock generation
2. Preserve the disposable copy for inspection
3. Do not run an update or install fallback
4. Do not copy the inconsistent lockfile to the working repository

### Scenario E: Disposable install or audit fails

Lock generation succeeds, but the frozen install or audit fails in the disposable copy. The executor must stop before copying the lockfile.

Requirements checklist:
1. [critical] Do not copy an unverified lockfile to the working repository
2. Preserve the disposable copy and identify the failed command
3. Do not run an alternative APM command

### Scenario F: Public source has not changed

The commits after the common source commit recorded in the lockfile change only repository guidance, a repo-local Skill, unrelated documentation, or `apm.lock.yaml`. The executor must treat this as a successful no-op.

Requirements checklist:
1. [critical] Compare only `skills/` and `apm.yml` for the public source delta
2. Exit successfully without creating a disposable copy or contacting the package source
3. Report that no lockfile commit is needed

### Scenario G: Refresh produces no lockfile diff

The verified disposable refresh produces an `apm.lock.yaml` identical to the working repository's existing lockfile. The executor must treat this as a successful no-op.

Requirements checklist:
1. [critical] Exit successfully after all verification
2. Report that no working repository diff remains
3. Do not print a commit command as the next required action

## Failure Pattern Ledger

- `non-dry-run apm command run in working repo`
- `dirty working tree mixed with lockfile update`
- `untracked file ignored by precondition check`
- `ignored APM deployment artifact ignored by precondition check`
- `local unpushed commit used before GitHub can resolve it`
- `guidance-only or lock-only commit caused self-referential lockfile churn`
- `generated lockfile copied before dependency, install, and audit verification`
- `failed lock generation hidden by an update or install fallback`
- `.agents/skills output copied back from disposable copy`
- `lockfile commit and Skill commit combined`

## Iter 1 - 2026-07-24

- Static command-contract and `bash -n` checks: passed
- APM capability check for `apm lock`: passed with APM 0.26.0
- Working-repository `apm install --frozen --dry-run --no-policy`: passed for 27 dependencies without creating deployment artifacts
- Scenario B: passed; a dirty working tree stopped before disposable-copy creation
- Scenario F predicate: the current lock commit and `HEAD` have no `skills/` or `apm.yml` delta, so the expected result is a no-op
- Scenarios A, C, D, E, and G: not executed in this iteration
- Full-path execution is deferred until the next pushed public Skill or `apm.yml` change; this iteration changes only repository guidance and the repo-local Skill
