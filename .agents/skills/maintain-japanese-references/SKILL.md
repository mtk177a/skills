---
name: maintain-japanese-references
description: Use in the mtk177a/skills repository when an English canonical README, agent-guidance file, repository document, public Skill, or tracked repository-local Skill is added or changed and its maintained Japanese reference translation must be created, reviewed, synchronized, or explicitly left unchanged. Preserve canonical meaning and repository terminology; not for Japanese-canonical Skills, Issue or pull-request authoring, general translation, or changing the English canonical source.
license: MIT
---

# Maintain Japanese References

## Objective

- Keep maintained Japanese reference translations aligned with English canonical files when the canonical meaning changes.
- Avoid no-op translation edits when an English change does not affect Japanese meaning.
- Preserve English as the public and normative canonical source while maintaining a reusable comprehension and review aid for the primary maintainer.

## Maintained pairs

- `README.md` → `README.ja.md`
- `AGENTS.md` → `AGENTS-ja.md`
- `CLAUDE.md` → `CLAUDE-ja.md`
- `docs/<name>.md` → `docs/ja/<name>.md`
- `skills/<skill-name>/SKILL.md` → `skills/<skill-name>/SKILL-ja.md` when English is canonical
- `.agents/skills/<tracked-skill>/SKILL.md` → `.agents/skills/<tracked-skill>/SKILL-ja.md`

Do not create a translation for a documented Japanese-canonical Skill.

## Workflow

1. Inspect the request and current diff to identify added or changed English canonical files in the maintained pairs.
2. Read each changed canonical section, its surrounding context, and the current Japanese counterpart when one exists.
3. Decide whether the canonical change affects meaning that the Japanese reader needs.\
   Treat requirements, scope, exceptions, permissions, prohibitions, safety conditions, procedures, validation, links, and document structure as meaning-bearing when they affect correct use.
4. If meaning changes, create or update the corresponding Japanese reference in the same change.\
   Edit the smallest coherent sections that preserve the canonical document's relationships and intent.
5. If meaning does not change, leave the Japanese file untouched and record the reason for that decision.
6. Check the resulting pair for semantic alignment, repository terminology, translation notices, Markdown structure, and unintended changes.

Preserve normative force such as `must`, `should`, and `may`, along with exclusions, authorization boundaries, failure conditions, and uncertainty.\
Preserve frontmatter fields, headings, links, code, commands, identifiers, tables, and formatting constraints unless the canonical change requires their corresponding update.

Prefer terminology already used in the repository's Japanese references.\
Do not add explanations, policy, examples, or claims that are absent from the canonical source.\
If the canonical meaning or an established translation is materially ambiguous, report the affected pair and ambiguity instead of guessing; continue with independent pairs when possible.

## Reporting

Report:

- every maintained pair reviewed
- whether each Japanese reference was created, updated, or left unchanged
- the semantic reason for each unchanged translation
- checks performed and their results
- unresolved ambiguities or unverified pairs

## Boundaries

- Do not edit the English canonical source as part of translation maintenance.
- Do not use this Skill for Japanese-canonical Skills, Issue or pull-request authoring, or general translation outside the maintained pairs.
- Do not use an external translation service or introduce dependencies.
- Do not commit, push, post tracker content, change the selected model, or start subagents unless separately authorized.
- This Skill does not depend on `japanese-tech-writing`.\
  When both Skills are explicitly used, this Skill controls fidelity and scope, while `japanese-tech-writing` controls expression within those limits.
