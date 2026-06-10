---
name: plan-risky-change
description: Before a high-risk change, organize the plan, risks, and rollback to obtain approval. (destructive, migration, dependency, security)
license: Apache-2.0
---

# Plan Risky Change

## Purpose

Make planning and approval mandatory to safely proceed with dangerous or destructive changes.

## When to use (examples)

- Large-scale changes: deletions, replacements, formatting, renames, directory reorganization
- Database: migrations, data corrections, backfills
- Dependencies: adding production dependencies, build or runtime changes
- Security: changes that touch authentication, authorization, encryption, signing, or secret handling
- Operations: infrastructure / configuration / deployment procedure changes

## Steps (follow this order)

1. Summarize in one sentence what to change and why.
2. Present the plan (Steps) briefly (roughly 3–7 steps).
3. List the risks (how it can break, impact scope, symptoms on failure).
4. State the rollback explicitly (how to revert, conditions that trigger revert).
5. Present the test plan (execution commands or manual verification steps).
6. Request approval: explicitly state "Is it OK to proceed with this plan?" and wait.
7. Execute after approval. If something unexpected arises, stop, report, and confirm the approach.

## Additional safety checks

- Confirm no secrets are included (`.env` / config files / log output / test data)
- Keep dependency additions minimal; consider alternatives (standard library / existing dependencies)
- Where possible, split into incremental changes (small PRs / commits)

## Output format

- Summary: ...
- Steps:

  1) ...

- Risks:
  - ...
- Rollback:
  - ...
- Test Plan:
  - ...
- Approval: Is it OK to proceed with this plan?

## Boundaries

### Always:

- State the plan, risks, rollback, and test plan explicitly
- Obtain approval before executing

### Ask first:

- Before executing destructive changes

### Never:

- Execute without approval
