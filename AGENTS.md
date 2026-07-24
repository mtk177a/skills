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

When creating or editing a Skill, inspect the existing `skills/*/SKILL.md` files needed to resolve responsibility overlap and converge on a judgment. Stop when that purpose is met; do not impose an arbitrary count.

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

## Repository-local operational Skills

- Repository-local operational Skills may live under `.agents/skills/<skill-name>/` only when they are exclusively for maintaining this repository itself and should not be distributed as part of the public Skill catalog.
- These repo-local Skills are source files, not APM deployment output, when they are explicitly tracked by git.
- Do not add repo-local Skills to `README.md`, `README.ja.md`, or `apm.yml`.
- Keep repo-local Skill names kebab-case and include `SKILL.md`, `SKILL-ja.md`, and minimal supporting files only when needed.
- The current tracked repo-local Skill exception is `.agents/skills/refresh-apm-lockfile/`.

## Working rules

- Keep changes small and easy to review
- Write Skill bodies in English by default. A Skill whose core purpose is Japanese writing or editing may use a Japanese `SKILL.md` as its canonical source and omit a duplicate `SKILL-ja.md`; document the exception and provenance.
- Do not hardcode local absolute paths or environment-specific assumptions
- Prioritize clear triggers, inputs, expected outputs, and boundaries in Skill bodies
- Add concise ordered steps and verification when sequence or completeness materially affects correctness
- Keep helper scripts and reference materials to the minimum needed for the Skill to work
- Skill bodies must be readable by agents that have no prior context about this repository

## APM source and lockfile workflow

- This repository owns two APM phases: publishing canonical Skill and manifest source, then generating and verifying the repository lockfile from that pushed source. Deploying packages into consumer repositories is outside this workflow.
- Maintain `apm.yml` manually; do not regenerate it. Update its dependency list when adding, removing, or renaming a public Skill.
- Before committing a public Skill or `apm.yml` change, run the relevant Skill evaluations and the non-deploying repository check:

  ```bash
  apm install --frozen --dry-run --no-policy
  ```

- Commit and push the public Skill and manifest source before refreshing the lockfile.
- After the source commit is pushed, use `.agents/skills/refresh-apm-lockfile/` as the single entry point for lockfile generation and verification. Do not choose or substitute APM update commands manually.
- The repo-local refresh Skill runs lock generation, a full frozen install, and `apm audit --ci --no-policy` in a disposable copy outside this repository.
- Commit an updated `apm.lock.yaml` separately with a summary such as `fix: refresh APM lockfile after <change>`. If the refresh reports that no public source changed, do not create a lockfile commit.
- Do not run a non-dry-run `apm install` or `apm update` in this repository. They deploy the repository's Skills to `.agents/skills/`, causing them to appear alongside globally installed copies.
- An empty `.agents/` directory may exist because agent tools can create it.
- Do not store review notes, temporary files, or other working artifacts under `.agents/`; use a temporary directory outside this repository instead.
- If APM-deployed `.agents/skills/*` or `apm_modules/` are present, stop and report them. Remove them only after confirming they are generated artifacts and obtaining approval; preserve explicitly tracked repo-local operational Skills such as `.agents/skills/refresh-apm-lockfile/`.

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
