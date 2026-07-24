---
name: design-skill
description: Designs whether and how to create, merge, split, or substantially rescope an Agent Skill before implementation. Use when defining a Skill's responsibility, trigger boundary, reusable resources, and evaluation strategy; not for routine wording edits, audits of existing behavior, or implementation itself.
license: MIT
---

# Design Skill

## Objective

- Decide whether a reusable Skill is the right intervention before drafting one.
- Produce an evidence-grounded design that an implementation workflow can apply without rediscovering the responsibility, trigger, resource, or evaluation decisions.
- Keep diagnosis, design, and implementation distinct. An existing audit may supply evidence, but this Skill must remain usable without one.

## Evidence

Read `references/authoring-guide.md` completely before making design decisions.

Gather what is available:

- intended outcome, users, clients, models, and failure signals
- real task examples, corrections, traces, or outputs that expose a reusable gap
- the no-Skill or previous-version baseline
- applicable local instructions and distribution constraints
- adjacent Skills, their descriptions, and coexistence behavior

Treat applicable local instructions as authoritative within their scope. Use the bundled guide as a portable baseline where local guidance is silent. Distinguish observed evidence, inference, assumptions, and unknowns. If only textual plausibility is available, label the design as a static hypothesis rather than demonstrated improvement.

## Workflow

1. Define the intended capability and the recurring failure or knowledge gap without assuming that a new Skill is required.
2. Examine representative tasks and baseline behavior. Identify what the agent lacks, what it already handles, and which corrections are genuinely reusable.
3. Compare the relevant interventions: no durable guidance, a local instruction or tool, an update or merge of an existing Skill, a split, or a new Skill.
4. Inspect adjacent Skills and distribution surfaces. Resolve responsibility overlap, trigger competition, context cost, and coexistence risks before choosing an artifact.
5. Choose one coherent unit of responsibility. Define its target user, in-scope tasks, exclusions, inputs, outputs, and failure handling.
6. Draft a `name` and `description`. Put the complete implicit-trigger context in `description`, including a negative boundary when it prevents a likely collision.
7. Allocate only non-obvious reusable content across `SKILL.md`, `references/`, `scripts/`, `assets/`, and evaluation assets. Match instruction freedom to task fragility instead of fixing every workflow to one level of detail.
8. Define safety or permission boundaries only where the workflow needs them. Preserve required safety properties without forcing a particular heading template.
9. Design evaluation before extensive authoring: trigger, non-trigger, near-miss, baseline, isolation, coexistence, instruction-following, and output-quality cases relevant to the intended clients and models.
10. Identify only the target surfaces actually affected by the design and produce an implementation handoff. Do not edit or implement the Skill as part of this workflow.

## Decision criteria

- Prefer no Skill when the model already performs the task reliably and no reusable specialized context or procedure is missing.
- Prefer updating or merging when the trigger, output contract, and risk boundary remain coherent.
- Prefer a new or split Skill when combining responsibilities would make triggering, loading, or execution ambiguous.
- Bundle references or scripts only when they save repeated rediscovery, provide domain evidence, or make fragile operations verifiable.
- Keep the main instructions concise enough that every loaded section earns its context cost.

## Reporting contract

Use a structure suited to the decision rather than a fixed proposal template. Include:

- the recommended intervention and why it is preferable to the alternatives
- evidence, assumptions, and unresolved questions
- proposed responsibility and trigger boundary
- metadata draft when a Skill is recommended
- content and resource allocation
- safety and permission properties that must survive implementation
- evaluation and rollout strategy
- affected target surfaces and an implementation-ready handoff

Do not force a Skill proposal when the evidence supports no durable guidance or a different intervention. Do not implement files, add dependencies, or alter repository policy; leave those actions to the authorized implementation workflow.
