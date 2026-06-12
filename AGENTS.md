# AGENTS.md

This file provides instructions for agents working in this repository.
If a deeper `AGENTS.md` exists in a subdirectory, that file takes precedence.

## Purpose

- Manage personally authored agent Skills and Skills maintained with ongoing modifications
- Keep a simple structure that multiple agents (Codex, Claude Code, GitHub Copilot, etc.) can reference easily
- Avoid OS-specific assumptions to stay compatible with both macOS M1 and Windows WSL

## Read first

- `README.md`
- `docs/authoring.md`

When creating or editing a Skill, also review existing `skills/*/SKILL.md` files to match their style.

## What belongs in this repository

- Personally authored Skills
- External Skills that have been reviewed and adapted with ongoing maintenance
- Operational rules, authoring guidelines, and migration notes for Skills

## What does not belong in this repository

- Verbatim copies of external Skills
- Experimental, unfinished Skills that are only being tried out
- Content containing customer names, internal URLs, secrets, API keys, or personal information
- Shared team operational rules that belong in a team Skills repository

## Structure rules

- The basic unit is `skills/<skill-name>/SKILL.md`
- `<skill-name>` uses kebab-case
- `SKILL.md` frontmatter must include at minimum `name`, `description`, and `license`
- `evals/`, `references/`, `scripts/`, `assets/` are optional and added only when needed
- Do not create per-agent classification directories like `common/`, `codex/`, or `claude-code/`
- Express agent-specific differences in Skill names or `description`, not in directory structure

## Working rules

- Keep changes small and easy to review
- Write Skill bodies in English; keep proper nouns, configuration keys, and established technical terms in their original form
- Do not hardcode local absolute paths or environment-specific assumptions
- Focus Skill content on "when to use," "what to provide as input," and "what to avoid" rather than step-by-step instructions
- Keep helper scripts and reference materials to the minimum needed for the Skill to work
- Skill bodies must be readable by agents that have no prior context about this repository

## APM validation

- Do not run a non-dry-run `apm install` or `apm update` in this repository. They deploy the repository's Skills to `.agents/skills/`, causing them to appear alongside globally installed copies.
- For routine validation in this repository, use commands that do not deploy Skills:

  ```bash
  apm install --frozen --dry-run --no-policy
  apm pack --dry-run --offline
  ```

- Run a full install and `apm audit --ci --no-policy` only in a disposable copy outside this repository.
- Maintain `apm.yml` manually; do not regenerate it. Update its dependency list when adding, removing, or renaming a Skill.
- Because `apm.yml` depends on this repository's own Skills, commit and push Skill and manifest changes before updating the lockfile.
- Update the lockfile by running `apm update --yes` in a disposable copy, then copy only the resulting `apm.lock.yaml` back into this repository.
- Commit `apm.lock.yaml` updates separately with a summary such as `fix: refresh APM lockfile after <change>`.
- An empty `.agents/` directory may exist because agent tools can create it.
- Do not store review notes, temporary files, or other working artifacts under `.agents/`; use a temporary directory outside this repository instead.
- Remove APM-deployed `.agents/skills/` and `apm_modules/` when present.

## Commit message convention

- Use Conventional Commits; write the summary in English, short and specific
- One commit per logical change; do not mix unrelated changes
- `skills/*/SKILL.md` is treated as the product of this repository; do not categorize all changes as `docs`
- Adding a new Skill or new behavior to an existing Skill: use `feat`
- Fixing an inconsistency or judgment error in an existing Skill: use `fix`
- Renaming, reorganizing, or restructuring without adding behavior: use `refactor`
- Updating `README.md`, `docs/*`, or `skills/*/evals/README.md`: use `docs`
- `apm.yml` or reference updates: use the type that matches the primary purpose of the change

## Changes that require approval

- Editing `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`
- Editing `skills/*/SKILL.md`, `docs/*`, or other operational rule documents
- Importing external Skills, adding dependencies, or changing distribution sources
- Changes that alter the repository's purpose or directory structure policy

## Avoid

- Copying external distributed Skills into this repository without modification
- Including secrets or non-public information in Skills, docs, scripts, or assets
- Introducing OS-specific or agent-specific assumptions without explicit documentation
- Proceeding with repository rule changes without approval
