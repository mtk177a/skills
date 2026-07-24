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

## Separate portable and client-specific layers

Keep the standard `name`, `description`, instructions, and bundled resources as the portable layer. Add a client's metadata or configuration only when the target workflow needs that client's:

- explicit or implicit invocation control
- UI presentation
- tool or dependency declaration
- permission, sandbox, hook, or execution-context behavior

Do not add every supported extension to every Skill. Keep the portable metadata draft limited to the common contract and list target-specific additions separately in the implementation handoff. If a client's format requires an extension in the same `SKILL.md`, label the field as target-specific and verify that every other intended client tolerates it. Verify current client semantics before depending on an extension, document the supported target, and keep the core responsibility usable without unrelated client metadata.

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

## Review third-party and executable capabilities

When a design adopts or adapts third-party material, record its upstream source, pinned revision, license, complete file set, local modifications, and update path. Inspect every distributed and directly referenced file; do not infer safety from the main Markdown file alone.

When instructions can lead to scripts, tools, filesystem access, credentials, network access, or external content, trace the complete path from input through data access to side effect or outbound destination. Pay special attention to combined capabilities such as file read plus network send, untrusted documents plus privileged tools, and automatic invocation plus destructive actions.

Prefer the least authority and smallest data scope that satisfies the responsibility. Use enforceable permission, sandbox, hook, or CI controls for hard guarantees when the client provides them. Reject or leave the design unverified when provenance, executable behavior, or outbound data flow cannot be established.

## Design evaluation before extensive instructions

Evaluation should determine whether the Skill adds value, not merely whether its text looks complete. Cover the dimensions that matter:

- should-trigger, should-not-trigger, and near-miss selection
- baseline without the Skill or with the prior version
- isolation and coexistence with adjacent Skills
- instruction following and output quality on realistic tasks
- supported clients and models when behavior may differ
- scripts and critical operations with executable verification

Before adding scenarios, map each material claim or design change to a plausible failure, a scenario or check that can expose it, and a grading method. A scenario earns its place by covering a distinct responsibility, boundary, coexistence risk, or known regression. Do not add or remove scenarios to satisfy a universal count.

Keep expected conclusions and grading criteria out of executor inputs. Prefer deterministic checks for objective outcomes and a separate grader or reviewer for judgment-heavy requirements. Executor self-report is diagnostic evidence, not the sole pass/fail authority.

Use the same inputs, environment, and grading policy for baseline and candidate comparisons. Count trigger activation only from observable client evidence. Repeat runs only when variation, an unexpected result, model differences, or the consequence of failure makes another observation decision-relevant. Record skipped or unavailable observations as unexecuted or unexposed rather than passing them.

Choose evaluation depth proportionally:

- static validation for metadata, consistency, boundaries, references, and self-containment
- targeted behavioral regression for changed instructions, triggering, coexistence, safety, or output requirements
- repeated empirical prompt tuning for observed failures, high-impact or unstable behavior, or substantial redesigns

State the selected depth and the evidence that would justify escalating to the next level. Do not describe a targeted regression or a variable-output smoke test as empirical tuning unless it actually runs repeated baseline/candidate cycles to resolve observed instability or failure.

There is no universal `/eval` command. Record the exact client workflow, command, script, or manual procedure used, and introduce a wrapper only when it improves repeated execution materially.

## Produce an implementation handoff

A design is ready to implement when it states:

- the selected intervention and rejected alternatives
- the evidence and unresolved assumptions
- responsibility, trigger boundary, inputs, outputs, and exclusions
- metadata and content allocation
- portable metadata and content, separately listed client-specific additions, plus third-party provenance when applicable
- required safety, data-flow, and permission properties
- evaluation coverage, selected depth and escalation conditions, grading method, and acceptance criteria
- actual target surfaces and migration or rollout needs

The design workflow should stop at this handoff. Editing, dependency changes, policy changes, deployment, and publication follow the authorization rules of the target environment.

## Canonical sources

This guide summarizes, rather than replaces, the [Agent Skills specification](https://agentskills.io/specification), [Agent Skills authoring best practices](https://agentskills.io/skill-creation/best-practices), [OpenAI Build skills guide](https://learn.chatgpt.com/docs/build-skills), [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and [Anthropic enterprise Skill review guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise).
