# Portable Skill Authoring Guide

Use this reference as a cross-repository design baseline. Discover applicable local instructions instead of assuming a particular root document or directory layout. Local instructions govern their own scope; this guide fills gaps rather than overriding them.

## Start from demonstrated value

A Skill should preserve specialized knowledge, a repeatable workflow, or a fragile operation that the agent would otherwise rediscover or mishandle. Prefer evidence from:

- a completed real task and the corrections needed to make it succeed
- repeated failures, traces, outputs, review comments, or operational history
- domain artifacts such as schemas, runbooks, interfaces, and tested scripts
- baseline runs without the Skill or with the previous version

Do not infer that a requested Skill must exist. If ordinary model behavior already meets the intended outcome reliably, durable instructions may add context cost without adding capability. When behavioral evidence is unavailable, record the proposal as a hypothesis and design the evaluation needed to test it.

## Choose the intervention before the artifact

Compare the relevant options:

- no durable guidance
- a local instruction, reference, tool, or script
- update or merge an existing Skill
- split an overloaded Skill
- create a new Skill

Treat a Skill as one coherent unit of work. Too narrow a unit forces unnecessary composition and context loading; too broad a unit makes triggering and instructions ambiguous. Prefer updating or merging when the trigger, output contract, and safety boundary remain coherent. Prefer a new or split Skill when those properties differ materially.

## Design discovery metadata

The Agent Skills format requires a `SKILL.md` with `name` and `description`. Applicable local policy may require additional metadata.

- Keep `name` aligned with the directory and within the target clients' supported syntax.
- Use a specific action-and-object or otherwise unambiguous name.
- Put what the Skill does and when it should trigger in `description`.
- Front-load the key use case and trigger terms so shortening by a client does not erase them.
- Include a negative trigger boundary when it prevents a likely collision.
- Keep execution mechanics in the body unless they are themselves required trigger context.

The body cannot repair a missing implicit trigger because clients normally choose the Skill from metadata before loading the body.

## Spend context on what the agent lacks

Assume the agent already knows general software concepts. Include domain facts, non-obvious failure modes, required procedures, and validated defaults that change its behavior.

Use progressive disclosure:

- Keep core decisions and procedures in `SKILL.md`.
- Put focused, conditionally needed knowledge in `references/`.
- Put deterministic or repeatedly reconstructed operations in tested `scripts/`.
- Put distributable templates and output resources in `assets/`.
- Keep references directly discoverable from `SKILL.md`; avoid reference chains.

Do not bundle a generic guide merely because a reference directory is available. Every file should remove a demonstrated ambiguity, repeated rediscovery, or execution risk.

## Match control to fragility

Use goals, decision criteria, and examples when multiple approaches are valid. Use ordered steps, validators, or narrow scripts when sequence and consistency are safety-critical. A single Skill may mix these levels.

Prefer a clear default with an escape condition over an unranked menu. Use exact output templates only when downstream consumers require exact structure; otherwise state the required information and let the agent adapt the presentation.

## Define material boundaries

Describe inputs, outputs, exclusions, failure handling, authority, and permission boundaries when they affect correct execution.

Do not require `Always`, `Ask first`, and `Never` headings as a universal structure. Use them only when the categories clarify distinct operational behavior. Preserve safety properties across redesigns and verify replacements rather than retaining wording mechanically.

Keep portable Skills independent of unnamed external documents and companion Skills. For an intentionally project-specific Skill, make the dependency and environment explicit.

## Design evaluation before extensive instructions

Evaluation should determine whether the Skill adds value, not merely whether its text looks complete. Cover the dimensions that matter:

- should-trigger, should-not-trigger, and near-miss selection
- baseline without the Skill or with the prior version
- isolation and coexistence with adjacent Skills
- instruction following and output quality on realistic tasks
- supported clients and models when behavior may differ
- scripts and critical operations with executable verification

Use the same inputs and environment for baseline and candidate comparisons. Count trigger activation only from observable client evidence. Record skipped or unavailable observations as unexecuted or unexposed rather than passing them.

## Produce an implementation handoff

A design is ready to implement when it states:

- the selected intervention and rejected alternatives
- the evidence and unresolved assumptions
- responsibility, trigger boundary, inputs, outputs, and exclusions
- metadata and content allocation
- required safety and permission properties
- evaluation cases and acceptance criteria
- actual target surfaces and migration or rollout needs

The design workflow should stop at this handoff. Editing, dependency changes, policy changes, deployment, and publication follow the authorization rules of the target environment.

## Canonical sources

This guide summarizes, rather than replaces, the [Agent Skills specification](https://agentskills.io/specification), [Agent Skills authoring best practices](https://agentskills.io/skill-creation/best-practices), [OpenAI Build skills guide](https://learn.chatgpt.com/docs/build-skills), and [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
