# Skill Authoring Guide

## What makes a good Skill

A good Skill lets an agent decide when to use it without hesitation, and contains the right amount of detail — no more, no less.

Write the body in English. Use proper nouns, configuration keys, and established technical terms as-is.

Prioritize:

- A short, clear statement of what the Skill is for
- When to use it and when not to
- Readable preconditions, inputs, and expected outputs
- Minimal agent-specific language
- Clear scope for any helper scripts or reference materials

## Writing the description

The `description` is the entry point for usage decisions, not a general explanation. Include:

- What situation triggers this Skill
- What kind of work it assists with
- If it depends on a specific agent, what that dependency is
- Focus on usage context over execution mechanics
- Move internal details (roles, orchestration) to the body under `Purpose` or `When to use`

Avoid:

- Vague descriptions where the usage context is unclear
- Subjective phrases like "a useful Skill"
- Descriptions that assume Codex without stating it
- Frontmatter stuffed with internal implementation details

## Naming a Skill

Choose a name where the responsibility and usage context are clear at first glance.
This repository uses `action + object` kebab-case as the default pattern.

- Start with a short verb describing what the Skill does
- Add the object it acts on
- Prioritize names that make the usage context and responsibility boundary obvious
- When in doubt, prefer clarity over brevity

Examples:

- `scope-request`
- `design-changes`
- `implement-changes`
- `review-changes`
- `triage-review-feedback`
- `summarize-changes`

Avoid:

- Single words like `build`, `design`, `release`
- Names that read as broader than the actual scope
- Names where the responsibility boundary is hard to infer

Single words are acceptable only when the Skill's responsibility is narrow enough that the name cannot be misread.

## Shared Skills vs. agent-specific Skills

First, ask whether you can express the Skill without agent dependencies.

- Shared Skill: usable across multiple agents for the same purpose with the same steps
- Agent-specific Skill: steps, tool availability, or I/O format are tightly coupled to one agent

This repository avoids classification directories. Express differences in Skill names or `description` instead.
If agent specificity matters, include that context in the name or description.

## When to fork or copy an external Skill

External Skills are not copied into this repository as-is. External Skill installation is managed in dotfiles via `apm.yml` / `apm.lock.yaml`.

Bring a Skill into this repository only when:

- You need to continuously modify and maintain it yourself
- Redesigning it from scratch is better than using it as-is
- You want to restructure it clearly for your own workflow

Even then, review the `frontmatter` and `description` to align with this repository's conventions — do not import verbatim.

## Keeping secrets and private information out

Never include the following in Skill bodies, helper scripts, reference materials, or assets:

- API keys, tokens, passwords
- Customer names, personal information
- Internal URLs, internal procedures, non-public operational information
- References to secret files that only exist in a local environment

Write Skills assuming they may be referenced from other environments and agents.
For environment-specific information, use variable names or placeholders.

## Notes on Skills with scripts

`scripts/` directories are useful but fragile. Handle with care.

- Minimize shell, OS, and architecture dependencies
- Document any additional dependencies
- Do not depend on absolute paths outside the repository
- If the script performs destructive operations, prompt for safety confirmation in the Skill body
- Do not mix generated artifacts or caches into the repository

Avoid scripts that break compatibility with both macOS M1 and Windows WSL unless the need is explicitly justified.

## Evaluation assets

When iterating on a Skill, manage evaluation assets alongside the content.

- Skill-level scenarios and checklists go in `skills/<skill-name>/evals/`
- Multi-Skill flow evaluations go in `docs/` (see `evaluation.md`)
- Start with Iter 0: statically check that `description` and body are consistent, that output format is defined, and that the Skill is self-contained
- Formalize scenarios and requirement checklists runnable by a blank-slate subagent
- Include at least one `[critical]` item in each checklist so pass/fail is unambiguous
- Do not make another agent or subagent a default behavior in Skill bodies
- Suggest additional agents only when the user explicitly asks, or as an optional enhancement for high-risk or high-uncertainty cases

The purpose of evaluation is not the author's subjective judgment but verifying that another agent can reproduce the intended behavior without confusion.
Prioritize reusable scenarios, decision criteria, and failure patterns over informal notes.

## Making a Codex-only Skill work across agents

When adapting a Codex-specific Skill for Claude Code or GitHub Copilot, review whether Codex-specific language should stay.

Check:

- Over-reliance on specific tool names
- Whether the request format and output format make sense for other agents
- Whether steps assume Codex-specific features
- Whether agent-specific differences are adequately described in `description` or the body

Keep Codex-specific language only when that specificity is the core value of the Skill.
Otherwise, rewrite around purpose and decision criteria, making the mechanics swappable.
