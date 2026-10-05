# AGENTS.md

This file is the canonical source for shared instructions for agents working in this repository.
If a deeper `AGENTS.md` exists in a subdirectory, that file takes precedence.

## Purpose

- Manage personally authored agent Skills, Skills maintained with ongoing modifications, and the two designated upstream Gist mirrors
- Keep a simple structure that multiple agents (Codex, Claude Code, GitHub Copilot, etc.) can reference easily
- Avoid OS-specific assumptions to stay compatible with both macOS M1 and Windows WSL

## Read first

- `README.md`
- `docs/authoring.md`
- `CONTRIBUTING.md` for Issue, commit, and pull request conventions

When creating or editing a Skill, inspect the existing `skills/*/SKILL.md` files needed to resolve responsibility overlap and converge on a judgment. Stop when that purpose is met; do not impose an arbitrary count.

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
- `evals/`, `references/`, `scripts/`, `assets/` are optional and added only when needed
- Do not create per-agent classification directories like `common/`, `codex/`, or `claude-code/`
- Express agent-specific differences in Skill names or `description`, not in directory structure

## Upstream Gist mirrors

- Keep `skills/japanese-tech-writing/SKILL.md` and `skills/cognitive-rhythm-writing/SKILL.md` byte-for-byte identical to the recorded upstream Gist revisions. Do not add local instructions, metadata, corrections, or translations to these files.
- Record each source URL, mirrored revision, retrieval date, file SHA-256, and license evidence in its `UPSTREAM.md`; summarize source and license in `THIRD_PARTY_NOTICES.md`. Keep repository installation guidance outside the mirrored files.
- Before updating either mirror, compare the recorded revision with the current Gist and review the complete upstream change under `docs/security.md`. If it cannot be accepted as an unmodified copy, report the difference instead of patching the Skill locally.
- These two mirrors do not require `evals/README.md`. Use model-backed evaluations only when a changed responsibility needs behavioral evidence; do not add definitions solely for a mirror update or the Issue #49 audit.

## Repository-local operational Skills

- Repository-local operational Skills may live under `.agents/skills/<skill-name>/` only when they are exclusively for maintaining this repository itself and should not be distributed as part of the public Skill catalog.
- These repo-local Skills are source files, not APM deployment output, when they are explicitly tracked by git.
- Do not add repo-local Skills to the public Skill catalog or distribution bundle.
- Keep repo-local Skill names kebab-case and include `SKILL.md`. Include `SKILL-ja.md` when that `SKILL.md` is in English; omit the duplicate for a documented Japanese writing/editing exception. Add supporting files only when needed.
- The current tracked repo-local Skill exceptions are:
  - `.agents/skills/maintain-japanese-references/`

## Working rules

- Keep changes small and easy to review
- Write authored or adapted Skill bodies in English by default. A Skill whose core purpose is Japanese writing or editing may use a Japanese `SKILL.md` as its canonical source and omit a duplicate `SKILL-ja.md`; document the exception and provenance. The upstream Gist mirrors retain their original Japanese files.
- Do not hardcode local absolute paths or environment-specific assumptions
- Prioritize clear triggers, inputs, expected outputs, and boundaries in Skill bodies
- Add concise ordered steps and verification when sequence or completeness materially affects correctness
- Keep helper scripts and reference materials to the minimum needed for the Skill to work
- Skill bodies must be readable by agents that have no prior context about this repository
- When a maintained English canonical file is added or changed, use `.agents/skills/maintain-japanese-references/` to review its Japanese counterpart and update it only when the canonical meaning changes

## APM Skill bundle workflow

- This repository publishes the root `skills/` directory as a native APM `SKILL_BUNDLE`. Do not add a root `apm.yml` or `apm.lock.yaml`; consumer repositories own their manifests and lockfiles.
- Before committing a public Skill change, run the relevant Skill evaluations, the repository checker, and the repository unit tests.
- In each Issue #49 Skill audit Sub Issue, migrate that Skill's existing `evals.json` and `triggers.json` set to the executable `{skill_name, evals}` format, even when its instructions and runtime behavior do not change.\
  Outside that audit, migrate a still-legacy set when a pull request first materially changes the Skill's instructions, runtime resources, discovery, responsibility, safety boundary, or evaluation definitions.\
  If model-backed evaluation is needed and the Skill has no executable definition for the affected responsibility, create the needed definition in that format.\
  Do not create definitions solely for migration.\
  README, reference-translation, meaning-preserving documentation or metadata, and legacy-result-only changes do not independently trigger migration outside the audit.
- Definition migration does not require executing every migrated case; run only the cases needed for the changed responsibility.
- Review evaluation sufficiency against the responsibility changed by the pull request, not against a universal case count or suite-refresh rule.
- An evaluation-insufficiency finding must identify the uncovered changed responsibility, a concrete acceptance-relevant failure, why the recorded evidence cannot expose it, and the smallest additional evaluation that would resolve it.
- Do not report an evaluation defect merely because an unselected case, unrelated suite, unchanged Skill, unmigrated repository asset, legacy `results.json`, or prior report was not refreshed.
- When distribution behavior changes, commit and push the candidate source, then verify the exact pushed commit from disposable consumer directories outside this repository.
- Verify the full bundle, any affected `--skill` selection path, and any affected individual `skills/<name>` installation path. Run consumer-side frozen install and audit checks against the generated consumer lockfile.
- Do not run a non-dry-run `apm install` or `apm update` in this repository. They create consumer manifests, lockfiles, and deployment artifacts in the source checkout.
- An empty `.agents/` directory may exist because agent tools can create it.
- Do not store review notes, temporary files, or other working artifacts under `.agents/`; use a temporary directory outside this repository instead.
- If root APM manifests, APM-deployed `.agents/skills/*`, or `apm_modules/` are present, stop and report them. Remove them only after confirming they are generated artifacts and obtaining approval; preserve the explicitly tracked repo-local operational Skill listed above.

## Commit message convention

Follow `CONTRIBUTING.md` for commit messages and pull request titles.

## Changes that require approval

- Editing `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`
- Editing `skills/*/SKILL.md`, `docs/*`, or other operational rule documents
- Importing external Skills, adding dependencies, or changing distribution sources
- Changes that alter the repository's purpose or directory structure policy

## Avoid

- Copying external distributed Skills into this repository without modification, except for the two designated upstream Gist mirrors
- Including secrets or non-public information in Skills, docs, scripts, or assets
- Introducing OS-specific or agent-specific assumptions without explicit documentation
- Proceeding with repository rule changes without approval
