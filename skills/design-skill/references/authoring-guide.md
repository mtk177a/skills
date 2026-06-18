# Portable Skill Authoring Guide

Use this reference when designing a Skill outside any specific repository.
Project-local files such as `AGENTS.md`, `README.md`, and `docs/authoring.md` may add constraints, but they are supplemental to this portable baseline unless the user asks to follow them.

## What makes a good Skill

A good Skill helps an agent decide when to use it without hesitation, and gives only the detail needed to perform that work.

Prioritize:

- A short statement of the Skill's purpose
- Clear "when to use" and "when not to use" guidance
- Readable preconditions, inputs, and expected outputs
- Minimal agent-specific language
- Clear scope for helper scripts, references, assets, or evals

## Description

The `description` is the main trigger for usage decisions. It should state:

- The situation that should trigger the Skill
- The kind of work it helps with
- Any required agent or tool dependency, if that dependency is part of the Skill's value

Avoid vague descriptions, subjective claims, and implementation details that belong in the body.

## Naming

Use kebab-case. Prefer names that show both the action and the object.

Good patterns:

- `scope-request`
- `design-changes`
- `implement-changes`
- `review-changes`
- `triage-review-feedback`

Avoid names that are broader than the actual responsibility. Single-word names are acceptable only when the responsibility is narrow enough that the name is not likely to be misread.

## Boundaries

Define operational boundaries explicitly:

- `Always`: behavior the agent should consistently perform
- `Ask first`: cases that require user confirmation
- `Never`: behavior that is out of scope or unsafe

When the request is abstract, fix the usage context in one sentence before choosing a final name or detailed boundary.

## Overlap Decisions

Before creating a new Skill, check existing Skills when they are available.

Prefer updating an existing Skill when the new behavior is the same workflow with clearer criteria or a small missing step.
Prefer a new Skill when the trigger, output contract, or risk boundary differs enough that combining them would make usage decisions ambiguous.

## Self-Contained References

Bundle reference material inside the Skill only when a blank-slate agent needs it at judgment time.

- Use `references/` for formats, decision criteria, and compact source material.
- Use `scripts/` only when executable support is necessary.
- Use `assets/` only for distributable supplementary materials.
- Use `evals/` for scenarios and checklists that verify the Skill's behavior.

Do not require repository-root documents unless the Skill is intentionally project-specific.

## Safety

Do not include secrets, customer names, personal information, internal URLs, API keys, tokens, or private operational details in Skill bodies, references, scripts, or assets.

When adding dependencies, using external code, making destructive changes, or changing repository policy, ask for approval first.
