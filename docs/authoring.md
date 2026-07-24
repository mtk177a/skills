# Skill Authoring Guide

This is the authoring guide for Skills maintained in this repository. Portable Skill design guidance that must travel with an individual Skill should live inside that Skill's own `references/` directory.

## What makes a good Skill

A good Skill lets an agent decide when to use it without hesitation, and contains the right amount of detail — no more, no less.

Write the body in English by default. A Skill whose core purpose is Japanese writing or editing may keep a Japanese `SKILL.md` as the canonical source instead of maintaining a duplicate Japanese translation. Document that exception and the Skill's provenance. Use proper nouns, configuration keys, and established technical terms as-is.

Prioritize:

- A short, clear statement of what the Skill is for
- When to use it and when not to
- Readable preconditions, inputs, and expected outputs
- Minimal agent-specific language
- Clear scope for any helper scripts or reference materials
- High-judgment workflows designed from the intended outcome and evidence, not from a predetermined artifact
- Instruction freedom matched to task fragility and context dependence: goals and constraints when multiple approaches are valid; concise ordered steps and verification when sequence or completeness affects correctness
- Complete diagnosis kept separate from staged implementation or rollout
- Discovery and findings without arbitrary numeric limits

When comparing against existing Skills, inspect the relevant examples needed to resolve responsibility overlap and converge on a judgment. Stop when that purpose is met; do not impose an arbitrary count or scan the full catalog without a reason.

## Use a semantic contract, not a heading template

Skills do not need identical headings. They do need enough information for a blank-slate agent to select, execute, and verify the workflow without inventing missing policy.

Check for these semantic responsibilities:

- objective and one coherent responsibility
- complete trigger context and material exclusions in `description`
- evidence, inputs, or preconditions needed before acting
- workflow or decision logic
- required output information or an exact output format when a downstream consumer needs one
- authority, failure handling, and safety or permission boundaries when material
- verification or evaluation of the behavior that can fail
- bundled resources and the conditions under which they should be read or executed

Use the smallest structure that expresses those responsibilities. Two common archetypes are:

| Archetype | Typical semantic structure |
| --- | --- |
| Judgment-oriented | Objective, Evidence, Workflow, optional decision criteria or dimensions, Reporting contract, Boundaries |
| Operational | Objective, Inputs or Preconditions, ordered Steps, Output format, Verification, Boundaries |

These are review models, not mandatory headings. A Skill may mix them when contextual judgment selects an approach and a fragile operation then requires an exact sequence.

Do not add a body-level `When to use` section merely to repeat `description`. Keep one only when the agent needs loaded-time branching after the Skill has already been selected. Likewise, use exact output templates, `Always` / `Ask first` / `Never`, companion-Skill sections, and self-review checklists only when their distinctions materially change execution.

## Writing the description

The `description` is the entry point for usage decisions, not a general explanation. Include:

- What situation triggers this Skill
- What kind of work it assists with
- If it depends on a specific agent, what that dependency is
- Focus on usage context over execution mechanics
- Put all information needed for implicit selection in `description`; move loaded-time roles, orchestration, and execution mechanics to the body

Avoid:

- Vague descriptions where the usage context is unclear
- Subjective phrases like "a useful Skill"
- Descriptions that assume Codex without stating it
- Frontmatter stuffed with internal implementation details

## Writing operational boundaries

Use `Always`, `Ask first`, and `Never` only when those categories carry meaningful distinctions for the workflow. Do not add empty sections or treat the presence of all three headings as a universal quality requirement.

Express the required behavior and safety properties rather than copying a boundary template mechanically. If an existing guardrail is replaced, define how to verify that the replacement preserves equivalent or stronger protection.

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

Before adopting or adapting a third-party Skill, review its provenance, license, complete file set, external references, scripts, tool and network use, and combined capabilities. Treat Markdown instructions as executable influence rather than inherently safe text. Follow [Security review](security.md) for the repository checklist.

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
- Before adding scenarios, map each material Skill claim or change to a plausible failure, a scenario that can expose it, and a grading method
- Add a scenario only when it covers a distinct responsibility, boundary, coexistence risk, or known regression; do not target a universal scenario count
- Formalize scenarios and requirement checklists runnable by a blank-slate executor
- Keep desired answers and grading criteria out of the executor input
- Mark requirements `[critical]` only when violating them should make the scenario fail; do not make every observation critical by default
- Do not make another agent or subagent a default behavior in Skill bodies
- Suggest additional agents only when the user explicitly asks, or as an optional enhancement for high-risk or high-uncertainty cases

The purpose of evaluation is not the author's subjective judgment but verifying that another agent can reproduce the intended behavior without confusion.
Prioritize reusable scenarios, decision criteria, and failure patterns over informal notes. Use repeated empirical prompt tuning only when observed failures, high impact, instability, or a substantial redesign justify the additional cost.

## Notes on references/

`references/` directories hold materials the Skill needs at judgment time — formats, specs, decision criteria.

- Include only what a blank-slate agent would need to apply the Skill
- Do not copy external documents verbatim; link to the canonical source instead
- Do not store temporary notes or customer-specific information
- Check the license of any material you include; do not bundle content under incompatible licenses

## Notes on assets/

`assets/` directories hold distributable supplementary materials — images, reusable templates, or small structured data.

- Include only materials with clear provenance and compatible licensing
- Do not mix generated artifacts, caches, or temporary files into `assets/`
- Large binary files should stay out of the repository unless truly necessary

## New Skill checklist

Before opening a pull request for a new Skill:

- [ ] Directory name is kebab-case and matches the frontmatter `name`
- [ ] `SKILL.md` exists with `name`, `description`, and `license` frontmatter
- [ ] `description` makes the usage context clear without reading the body
- [ ] The body satisfies the semantic contract without copying a heading template mechanically
- [ ] Body is written in English, or a Japanese writing/editing exception is documented
- [ ] `SKILL-ja.md` Japanese reference translation exists unless `SKILL.md` is the documented Japanese canonical source
- [ ] No secrets, personal information, or internal URLs
- [ ] Third-party provenance and capability risks have been reviewed when external material is included
- [ ] `scripts/`, `references/`, `assets/` contain only what the Skill needs (empty directories removed)
- [ ] `evals/README.md` Iter 0 static check is complete

## Making a Codex-only Skill work across agents

When adapting a Codex-specific Skill for Claude Code or GitHub Copilot, review whether Codex-specific language should stay.

Do not assume that compatible clients discover the same instruction filenames or apply the same precedence rules. As of the linked official documentation, Codex uses `AGENTS.md` for durable repository guidance, while Claude Code reads `CLAUDE.md` and can use an import or bridge to reuse `AGENTS.md`. Recheck current client documentation when this behavior affects a design.

Check:

- Over-reliance on specific tool names
- Whether the request format and output format make sense for other agents
- Whether steps assume Codex-specific features
- Whether agent-specific differences are adequately described in `description` or the body
- Whether shared guidance has one canonical source and client-specific bridge files avoid duplication
- Whether a requirement needs behavioral guidance or a client-enforced policy, permission, or hook

Keep Codex-specific language only when that specificity is the core value of the Skill.
Otherwise, rewrite around purpose and decision criteria, making the mechanics swappable.

Sources: [OpenAI agents guidance](https://developers.openai.com/codex/concepts/customization#agents-guidance), [Claude Code memory and CLAUDE.md](https://code.claude.com/docs/en/memory).
