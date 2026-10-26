# AGENTS.md

This file is the source of truth for the shared instructions of agents in this repository.
An `AGENTS.md` in a subdirectory takes precedence in that subdirectory.

## Purpose

This repository manages these items:

- agent Skills that the owner wrote
- external Skills that the owner reviewed, adapted, and maintains
- unmodified copies of two upstream Gists: `japanese-tech-writing` and `cognitive-rhythm-writing`
- the operational rules, authoring guidelines, and migration notes for these Skills

Experimental Skills, verbatim copies of other external Skills, and rules for a team belong in other repositories.
Keep the structure simple, so that Codex, Claude Code, GitHub Copilot, and other agents can use it.
Keep the content independent of the operating system, so that it works on macOS (Apple silicon) and Windows WSL.
Keep customer names, internal URLs, secrets, API keys, and personal information out of all files.

## Read first

- [README.md](README.md)
- [CONTRIBUTING.md](CONTRIBUTING.md): Issues, verification, commit messages, and pull requests
- [docs/maintainers/authoring.md](docs/maintainers/authoring.md): when you create or edit a Skill
- [docs/maintainers/glossary.md](docs/maintainers/glossary.md): when you write about repository concepts in documents or Skill bodies

## Structure

- Put each Skill in `skills/<skill-name>/SKILL.md`, with a kebab-case name.
- Include at least `name`, `description`, and `license` in the frontmatter.
  The two upstream Gist mirrors keep their original frontmatter.
- Add `references/`, `scripts/`, and `assets/` only when the Skill needs them.
- Use one directory structure for all agents.
  Show a difference between agents in the Skill name or the `description`.

## Upstream Gist mirrors

- Keep `skills/japanese-tech-writing/SKILL.md` and `skills/cognitive-rhythm-writing/SKILL.md` byte for byte the same as the upstream revisions in their `UPSTREAM.md`.
  Put local instructions, metadata, corrections, and translations outside these files.
- Before you update a mirror, review the complete upstream change.
  If the change cannot be accepted as an unmodified copy, report the difference, and keep the current copy.
- Follow [Upstream Gist mirrors](docs/maintainers/authoring.md#upstream-gist-mirrors) for what to record and how to update a mirror.

## Repository-local operational Skills

- A Skill that only maintains this repository can be in `.agents/skills/<skill-name>/`.
  It stays out of the public Skill catalog and the plugin ZIP.
- A repository-local Skill that git tracks is a source file, not APM deployment output.
- Give a repository-local Skill a kebab-case name and a `SKILL.md`.
  Add `SKILL-ja.md` as described in [Skill files](docs/maintainers/localization.md#skill-files), and add other files only when necessary.
- The only tracked repository-local Skill is `.agents/skills/maintain-japanese-references/`.

## Working rules

- Keep each change small and easy to review.
- Write Skill bodies in English.
  For the Japanese exception, see [Skill files](docs/maintainers/localization.md#skill-files).
- Use relative paths, and state each assumption about the environment.
- Write Skill bodies as described in [Design the Skill](docs/maintainers/authoring.md#design-the-skill).
  Then agents with no context about this repository can use them.
- When you add or change an English source, review its Japanese reference translation with `.agents/skills/maintain-japanese-references/`.
  Update the translation only when the meaning of the English source changes.

## APM

- This repository publishes the `skills/` catalog through APM.
  Consumer repositories own `apm.yml` and `apm.lock.yaml`, so keep both files out of the root of this repository.
- Before you commit a change to a public Skill, run the repository checker and the unit tests.
  Verify the work and its safety boundaries as the task needs.
- When installation behavior changes or you build a new plugin version, commit and push the candidate.
  Then verify the pushed commit from disposable consumer directories outside this repository, as described in [docs/maintainers/packaging.md](docs/maintainers/packaging.md).
- In this repository, run `apm install` and `apm update` only with `--dry-run`.
  Without it, they create consumer manifests, lockfiles, and deployed files in the source checkout.
- Store review notes, temporary files, and other working files in a temporary directory outside this repository.
  Keep them out of `.agents/`.
  An empty `.agents/` directory can exist, because agent tools can create it.
- If root APM manifests, APM-deployed `.agents/skills/*`, or `apm_modules/` exist, stop and report them.
  Remove them only after you confirm that they are generated, and after you get approval.
  Keep the tracked repository-local Skills.

## Changes that need approval

Get approval before you do one of these:

- edit `AGENTS.md` or `.github/copilot-instructions.md`, or add a `CLAUDE.md`
- edit `skills/*/SKILL.md`, `docs/*`, or other documents of operational rules
- import an external Skill, add a dependency, or change where the Skills are published from
- publish the plugin ZIP, for example through GitHub Releases
- change the purpose of the repository or its policy for the directory structure
