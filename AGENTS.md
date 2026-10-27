# AGENTS.md

This file is the canonical source for shared instructions for agents working in this repository.
If a deeper `AGENTS.md` exists in a subdirectory, that file takes precedence.

## Purpose

- Manage personally authored agent Skills, Skills maintained with ongoing modifications, and the two designated upstream Gist mirrors
- Keep a simple structure that multiple agents (Codex, Claude Code, GitHub Copilot, etc.) can reference easily
- Avoid OS-specific assumptions to stay compatible with both macOS M1 and Windows WSL

## Read first

- [README.md](README.md)
- [CONTRIBUTING.md](CONTRIBUTING.md) for Issues, verification, commit messages, and pull requests
- [docs/maintainers/authoring.md](docs/maintainers/authoring.md) when creating or editing a Skill
- [docs/maintainers/glossary.md](docs/maintainers/glossary.md) when writing about repository concepts in documentation or Skill bodies

When creating or editing a Skill, inspect the existing `skills/*/SKILL.md` files needed to resolve responsibility overlap and converge on a judgment.
Stop when that purpose is met; do not impose an arbitrary count.

## What belongs in this repository

- Personally authored Skills
- External Skills that have been reviewed and adapted with ongoing maintenance
- Unmodified copies of the two designated upstream Gists: `japanese-tech-writing` and `cognitive-rhythm-writing`
- Operational rules, authoring guidelines, and migration notes for Skills

## What does not belong in this repository

- Verbatim copies of external Skills other than the two designated upstream Gist mirrors
- Experimental, unfinished Skills that are only being tried out
- Content containing customer names, internal URLs, secrets, API keys, or personal information
- Shared team operational rules that belong in a team Skills repository

## Structure rules

- The basic unit is `skills/<skill-name>/SKILL.md`
- `<skill-name>` uses kebab-case
- `SKILL.md` frontmatter must include at minimum `name`, `description`, and `license`, except that the two upstream Gist mirrors retain their original frontmatter
- `references/`, `scripts/`, `assets/` are optional and added only when needed
- Do not create per-agent classification directories like `common/`, `codex/`, or `claude-code/`
- Express agent-specific differences in Skill names or `description`, not in directory structure

## Upstream Gist mirrors

- Keep `skills/japanese-tech-writing/SKILL.md` and `skills/cognitive-rhythm-writing/SKILL.md` byte-for-byte identical to the upstream Gist revisions recorded in their `UPSTREAM.md`. Do not add local instructions, metadata, corrections, or translations to these files.
- Before updating either mirror, review the complete upstream change. If it cannot be accepted as an unmodified copy, report the difference instead of patching the Skill locally.
- Follow [Upstream Gist mirrors](docs/maintainers/authoring.md#upstream-gist-mirrors) for what to record and how to update a mirror.

## Repository-local operational Skills

- Repository-local operational Skills may live under `.agents/skills/<skill-name>/` only when they are exclusively for maintaining this repository itself and should not be published as part of the public Skill catalog.
- These repo-local Skills are source files, not APM deployment output, when they are explicitly tracked by git.
- Do not add repo-local Skills to the public Skill catalog or the plugin ZIP.
- Keep repo-local Skill names kebab-case and include `SKILL.md`. Add `SKILL-ja.md` as described in [Skill files](docs/maintainers/localization.md#skill-files). Add supporting files only when needed.
- The current tracked repo-local Skill exceptions are:
  - `.agents/skills/maintain-japanese-references/`

## Working rules

- Keep changes small and easy to review
- Write authored or adapted Skill bodies in English by default. For the Japanese exception, see [Skill files](docs/maintainers/localization.md#skill-files).
- Do not hardcode local absolute paths or environment-specific assumptions
- Write Skill bodies following [Design the Skill](docs/maintainers/authoring.md#design-the-skill), so that agents with no prior context about this repository can use them
- When an English source is added or changed, use `.agents/skills/maintain-japanese-references/` to review its Japanese reference translation and update it only when the meaning of the English source changes

## APM Skill bundle workflow

- This repository publishes the root `skills/` catalog through APM. Do not add a root `apm.yml` or `apm.lock.yaml`; consumer repositories own their manifests and lockfiles.
- Before committing a public Skill change, run the repository checker and the unit tests for retained code. Verify the changed work and its safety boundaries as appropriate to the task.
- When installation behavior changes or a new plugin version is built, commit and push the candidate source, then verify the exact pushed commit from disposable consumer directories outside this repository, as described in [docs/maintainers/packaging.md](docs/maintainers/packaging.md).
- Do not run a non-dry-run `apm install` or `apm update` in this repository. They create consumer manifests, lockfiles, and deployment artifacts in the source checkout.
- An empty `.agents/` directory may exist because agent tools can create it.
- Do not store review notes, temporary files, or other working artifacts under `.agents/`; use a temporary directory outside this repository instead.
- If root APM manifests, APM-deployed `.agents/skills/*`, or `apm_modules/` are present, stop and report them. Remove them only after confirming they are generated artifacts and obtaining approval; preserve the explicitly tracked repo-local operational Skill listed above.

## Changes that require approval

- Editing `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`
- Editing `skills/*/SKILL.md`, `docs/*`, or other operational rule documents
- Importing external Skills, adding dependencies, or changing where the Skills are published from
- Publishing the plugin ZIP, such as through GitHub Releases
- Changes that alter the repository's purpose or directory structure policy

## Avoid

- Copying external Skills into this repository without modification, except for the two designated upstream Gist mirrors
- Including secrets or non-public information in Skills, docs, scripts, or assets
- Introducing OS-specific or agent-specific assumptions without explicit documentation
- Proceeding with repository rule changes without approval
