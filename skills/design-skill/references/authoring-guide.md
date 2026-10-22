# Portable Skill Authoring Guide

Use this reference as a cross-repository design baseline. Discover applicable local instructions instead of assuming a particular root document or directory layout. Local instructions govern their own scope; this guide fills gaps rather than overriding them.

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

Keep portable Skills independent of unnamed external documents and companion Skills. For an intentionally project-specific Skill, make the dependency and environment explicit.

## Review third-party and executable capabilities

When a design adopts or adapts third-party material, record its upstream source, pinned revision, license, complete file set, local modifications, and update path. Inspect every distributed and directly referenced file; do not infer safety from the main Markdown file alone.

When instructions can lead to scripts, tools, filesystem access, credentials, network access, or external content, trace the complete path from input through data access to side effect or outbound destination. Pay special attention to combined capabilities such as file read plus network send, untrusted documents plus privileged tools, and automatic invocation plus destructive actions.

Prefer the least authority and smallest data scope that satisfies the responsibility. Use enforceable permission, sandbox, hook, or CI controls for hard guarantees when the client provides them. Reject or leave the design unverified when provenance, executable behavior, or outbound data flow cannot be established.

## Canonical sources

This guide summarizes, rather than replaces, the [Agent Skills specification](https://agentskills.io/specification), [Agent Skills authoring best practices](https://agentskills.io/skill-creation/best-practices), [OpenAI Build skills guide](https://learn.chatgpt.com/docs/build-skills), [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and [Anthropic enterprise Skill review guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise).
