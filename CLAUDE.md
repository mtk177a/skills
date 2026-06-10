# CLAUDE.md

This file provides supplementary instructions for Claude Code. `AGENTS.md` is the authoritative contract for this repository.

## Read first

- `AGENTS.md`
- `README.md`
- `docs/authoring.md`

## Expected behavior in this repository

- Treat `skills/<skill-name>/SKILL.md` as the basic unit
- Keep frontmatter `name` and `description` consistent when creating or editing a Skill
- Treat the English Skill body as canonical and maintain `SKILL-ja.md` as a Japanese reference translation
- Express agent-specific differences in Skill names or descriptions; do not add per-agent directories

## How to work

- Read existing Skills and related docs before implementing changes to avoid duplication and contradictions
- In Skill bodies, prioritize use cases, prerequisites, prohibitions, and expected output
- Do not copy external Skills directly; when considering one, identify its source and maintenance policy and discuss the approach first

## Approval boundaries

- Edit `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md` only after approval
- Edit `skills/*/SKILL.md` or `docs/*` only after approval
- Before adding dependencies or changing repository policy, explain the reason and impact

## Avoid

- Do not add secrets, personal information, or internal information
- Do not leave temporary notes or unorganized prototypes in the repository
- Do not introduce OS-specific commands or local environment assumptions without explanation
