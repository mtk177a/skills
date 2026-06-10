---
name: design-skill
description: Use when designing a new Skill, or when significantly revising an existing Skill's responsibilities and boundaries.
license: MIT
---

# Design Skill

## Purpose

- Build a new Skill proposal, taking into account existing rules and overlap checks.
- When significantly redesigning an existing Skill, organize its responsibilities, boundaries, and output contract.

## When to use

- When you want to add a new Skill
- When you want to significantly revise an existing Skill (responsibilities, boundaries, or structure change)
- When you need to decide what `name`, `description`, and boundaries to use
- When a request is still abstract and you need to fix the usage context in one sentence before drafting a Skill proposal

## Input (optional)

- Purpose, target task, intended user
- Related existing Skills, README, docs
- Source Skill or reference structure if applicable

## Steps

1. Read `docs/authoring.md` as primary sources.
2. Define purpose, scope, and target user in 1–2 lines. If the request is abstract, fix the usage context in one sentence first.
3. Check for overlap, conflicts, and merge candidates with existing Skills.
4. Decide `name` and `description`. Prioritize making the usage context readable; if the responsibility boundary is not confirmed, use a working name and get approval.
5. Define boundaries (`Always` / `Ask first` / `Never`).
6. Decide steps, output format, and whether optional directories (`evals/`, `references/`, `scripts/`, `assets/`) are needed.
7. List the impact scope (`AGENTS.md` / docs / scripts / `apm.yml`).
8. Proceed in the order: propose diff → get approval → implement.
9. If Markdown editing is involved, make a judgment call on whether to apply `format-markdown`.

## Output format (proposal)

- Summary of changes: ...
- Purpose / scope: ...
- Conflicts / overlaps: ...
- Primary sources: ...
- Metadata:
  - name: ...
  - description: ...
- Steps:
  1. ...
- Boundaries:
  - Always: ...
  - Ask first: ...
  - Never: ...
- Optional directories needed: ...
- Impact scope: ...
- Approval: Is it OK to proceed with this approach?

## Boundaries

### Always:

- State purpose, scope, and boundaries explicitly
- Treat `docs/authoring.md` as primary sources
- Check for overlap with existing Skills
- Make the usage context readable from `description`
- When input is abstract, fix the usage context first before rushing to confirm a `name`

### Ask first:

- Changes to `AGENTS.md` content
- Significant redesign of an existing Skill

### Never:

- Execute large changes without approval
- Add dependencies or reuse external code without authorization

## Notes (optional)

Principles:

- Keep changes small and reviewable
- Align with existing style
- Clear boundaries (`Always` / `Ask first` / `Never`)
- Keep `description` short; prioritize expressions that make the usage context clear
- Avoid reproducing full general guidelines; use a pointer to `docs/authoring.md` for anything that needs elaboration
