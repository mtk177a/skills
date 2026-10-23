# Skill Authoring Guide

This is the authoring guide for Skills maintained in this repository.\
The two upstream Gist mirrors follow the separate copying rules below; the authoring rules do not change their `SKILL.md` files.\
Portable Skill design guidance that must travel with an individual Skill should live inside that Skill's own `references/` directory.

- **Create a Skill**: decide its [responsibility](#what-makes-a-good-skill), [name](#naming-a-skill), [trigger](#writing-the-description), and [body](#use-a-semantic-contract-not-a-heading-template).
- **Import external material**: check the [adoption and Gist rules](#when-to-fork-or-copy-an-external-skill).
- **Prepare a PR**: use the [new Skill checklist](#new-skill-checklist).

## What makes a good Skill

**Define one responsibility and a clear usage context.**

Follow [Localization](localization.md) for source languages and translation updates.

Prioritize these design decisions:

- High-judgment workflows designed from the intended outcome and evidence, not from a predetermined artifact
- Instruction freedom matched to task fragility and context dependence: goals and constraints when multiple approaches are valid; concise ordered steps and verification when sequence or completeness affects correctness
- Complete diagnosis kept separate from staged implementation or rollout
- Discovery and findings without arbitrary numeric limits

When comparing against existing Skills, inspect the relevant examples needed to resolve responsibility overlap and converge on a judgment.\
Stop when that purpose is met; do not impose an arbitrary count or scan the full catalog without a reason.

## Naming a Skill

Use action + object in kebab-case, such as `clarify-request` or `design-changes`, to make the responsibility and usage context clear.\
Prefer clarity over brevity and avoid names that imply broader scope.\
Use a single word such as `build` only when the responsibility is narrow enough to avoid ambiguity.

## Writing the description

The `description` is the entry point for usage decisions, not a general explanation.\
Include:

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

## Use a semantic contract, not a heading template

Skills do not need identical headings.\
They do need enough information for a blank-slate agent to select, execute, and verify the workflow without inventing missing policy.

Check for these semantic responsibilities:

- objective and one coherent responsibility
- complete trigger context and material exclusions in `description`
- evidence, inputs, or preconditions needed before acting
- workflow or decision logic
- required output information or an exact output format when a downstream consumer needs one
- authority, failure handling, and safety or permission boundaries when material
- verification of the work performed and relevant safety conditions
- bundled resources and the conditions under which they should be read or executed

Use the smallest structure that expresses those responsibilities.\
Two common archetypes are:

| Archetype | Typical semantic structure |
| --- | --- |
| Judgment-oriented | Objective, Evidence, Workflow, optional decision criteria or dimensions, Reporting contract, Boundaries |
| Operational | Objective, Inputs or Preconditions, ordered Steps, Output format, Verification, Boundaries |

These are review models, not mandatory headings.\
A Skill may mix them when contextual judgment selects an approach and a fragile operation then requires an exact sequence.

Do not add a body-level `When to use` section merely to repeat `description`.\
Keep one only when the agent needs loaded-time branching after the Skill has already been selected.\
Likewise, use exact output templates, `Always` / `Ask first` / `Never`, companion-Skill sections, and self-review checklists only when their distinctions materially change execution.

When replacing a guardrail, define how to verify equivalent or stronger protection.

## Companion Skills

Skills are self-contained by default.\
A companion relationship is a narrow, approved exception in which one Skill deliberately requires another to apply its rules correctly.\
Do not use it for convenience, related subject matter, or an arbitrary dependency graph; accidental cross-Skill coupling remains a design problem.

Do not name another public Skill in `SKILL.md` or `SKILL-ja.md`.\
Describe out-of-scope work by its type and a handoff by the input it needs.\
Record relationships between Skills only in the [Skill workflow guide](../users/workflows.md).\
`scripts/check_repository.py` enforces this rule, except for approved companion relationships and the upstream mirrors.

An approved relationship must record:

- the direction of the relationship and the participating Skills
- why the companion is required
- the supported installation path
- the behavior when the companion is unavailable, including whether work stops
- provenance and local adaptations that introduced or maintain the relationship

When either Skill, the relationship, the installation path, or its missing-companion behavior changes, review this record and verify the affected behavior.

### Approved: Japanese reference maintenance

| Required relationship | Provenance |
| --- | --- |
| `maintain-japanese-references` → `write-natural-japanese` | Original repository material. [#42](https://github.com/mtk177a/skills/pull/42) introduced the maintenance Skill; [#77](https://github.com/mtk177a/skills/issues/77) records the required relationship and Japanese-canonical exception |

- **Reason**: preserve English meaning and use context-appropriate Japanese wording.
- **Location**: both Skills are tracked in this repository.
- **Before use**: read `skills/write-natural-japanese/SKILL.md` and its required references. If a repository file is unavailable, stop and report it without substituting a personal copy.

## Shared Skills vs. agent-specific Skills

First, ask whether you can express the Skill without agent dependencies.

- Shared Skill: usable across multiple agents for the same purpose with the same steps
- Agent-specific Skill: steps, tool availability, or I/O format are tightly coupled to one agent

This repository avoids classification directories.\
Express differences in Skill names or `description` instead.\
If agent specificity matters, include that context in the name or description.

## Making a Codex-only Skill work across agents

When adapting a Codex-specific Skill for Claude Code or GitHub Copilot, review whether Codex-specific language should stay.

Do not infer instruction-file discovery, loading, precedence, or Skill invocation from format compatibility.\
When these behaviors affect a design, consult the current official documentation for each target client and verify behavior in the target version or environment where the documentation is conditional or incomplete.\
Use the result for the current decision instead of maintaining a client-behavior inventory here.

### Shared and client-specific instructions

**Keep shared repository instructions in `AGENTS.md`.**

- **Copilot bridge**: instruct Copilot to read `AGENTS.md`; if unavailable, stop without modifying files, running commands, or changing external state.
- **Surfaces without automatic loading**: repeat only the minimum safety and approval rules needed to preserve those boundaries in the bridge. This delivery fallback is not a second canonical source.
- **Updates**: check and update the fallback with any related `AGENTS.md` rule. Do not duplicate other shared rules.

### Checks when adapting for another agent

- Over-reliance on specific tool names
- Whether the request format and output format make sense for other agents
- Whether steps assume Codex-specific features
- Whether agent-specific differences are adequately described in `description` or the body
- Whether shared guidance has one canonical source and client-specific bridge files duplicate only a documented minimum safety and approval fallback
- Whether a retained safety and approval fallback remains aligned with its canonical rules
- Whether a requirement needs behavioral guidance or a client-enforced policy, permission, or hook

Keep Codex-specific language only when that specificity is the core value of the Skill.\
Otherwise, rewrite around purpose and decision criteria, making the mechanics swappable.

Current client documentation: [Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code project instructions](https://code.claude.com/docs/en/memory), [GitHub Copilot custom instructions support](https://docs.github.com/en/copilot/reference/custom-instructions-support).

## When to fork or copy an external Skill

Except for the two Gist mirrors below, external Skills are not copied into this repository as-is.\
External Skill installation is managed in dotfiles via `apm.yml` / `apm.lock.yaml`.

Bring a Skill into this repository only when:

- You need to continuously modify and maintain it yourself
- Redesigning it from scratch is better than using it as-is
- You want to restructure it clearly for your own workflow

Even then, review the `frontmatter` and `description` to align with this repository's conventions — do not import verbatim.

Before adopting or adapting a third-party Skill, review its provenance, license, complete file set, external references, scripts, tool and network use, and combined capabilities.\
Treat Markdown instructions as executable influence rather than inherently safe text.\
Follow [Security review](security.md) for the repository checklist.

### Two upstream Gist mirrors

`japanese-tech-writing` and `cognitive-rhythm-writing` are copies of k16shikano's public Gists.\
Their `SKILL.md` files match the revisions recorded in each `UPSTREAM.md` byte for byte.\
Do not add local rules, frontmatter fields, editorial corrections, or a Japanese reference translation to either file.\
The repository checker verifies each copy against the SHA-256 recorded in `UPSTREAM.md`; checking whether a newer Gist revision exists requires an explicit upstream comparison.

When updating a mirror, compare the recorded revision with the current Gist, inspect the complete change under [Security review](security.md), then copy the accepted revision without modification and update its revision, hash, and third-party notice.\
If the new upstream file cannot be accepted as-is, record the difference and do not create a local variant.

The upstream `cognitive-rhythm-writing` requires `../japanese-tech-writing/SKILL.md` before use.\
Install both through [selected installation](../users/installation.md#install-through-apm).\
Do not add a local missing-companion procedure to the upstream file.

## Keeping secrets and private information out

Never include the following in Skill bodies, helper scripts, reference materials, or assets:

- API keys, tokens, passwords
- Customer names, personal information
- Internal URLs, internal procedures, non-public operational information
- References to secret files that only exist in a local environment

Write Skills assuming they may be referenced from other environments and agents.\
For environment-specific information, use variable names or placeholders.

## Bundle only the resources needed

### Scripts

When adding `scripts/`, check runtime requirements and side effects.

- Minimize shell, OS, and architecture dependencies
- Document any additional dependencies
- Do not depend on absolute paths outside the repository
- If the script performs destructive operations, prompt for safety confirmation in the Skill body
- Do not mix generated artifacts or caches into the repository

Avoid scripts that break compatibility with both macOS M1 and Windows WSL unless the need is explicitly justified.

### References

`references/` directories hold materials the Skill needs at judgment time — formats, specs, decision criteria.

- Include only what a blank-slate agent would need to apply the Skill
- Do not copy external documents verbatim; link to the canonical source instead
- Do not store temporary notes or customer-specific information
- Check the license of any material you include; do not bundle content under incompatible licenses

### Assets

`assets/` directories hold distributable supplementary materials — images, reusable templates, or small structured data.

- Include only materials with clear provenance and compatible licensing
- Do not mix generated artifacts, caches, or temporary files into `assets/`
- Large binary files should stay out of the repository unless truly necessary

## New Skill checklist

Before opening a pull request for a new Skill:

- [ ] Directory name is kebab-case and matches the frontmatter `name`
- [ ] `SKILL.md` exists with `name`, `description`, and `license` frontmatter (the two documented Gist mirrors retain their upstream frontmatter)
- [ ] `description` makes the usage context clear without reading the body
- [ ] The body satisfies the semantic contract without copying a heading template mechanically
- [ ] Body is written in English, or a Japanese writing/editing exception is documented
- [ ] `SKILL-ja.md` Japanese reference translation exists unless `SKILL.md` is the documented Japanese canonical source
- [ ] No secrets, personal information, or internal URLs
- [ ] Third-party provenance and capability risks have been reviewed when external material is included
- [ ] `scripts/`, `references/`, `assets/` contain only what the Skill needs (empty directories removed)
- [ ] The repository checker and tests for retained code pass, and the Skill's work results and safety boundaries have been checked as appropriate
