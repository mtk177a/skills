# Skill Security Review

This document defines the security review expected before adopting, adapting, publishing, or materially updating a third-party or executable Skill.

A Skill is not safe merely because its entry point is Markdown. Its instructions can cause an agent to read files, execute scripts, call tools, fetch external content, or transmit data. Review the complete capability chain rather than judging each permission in isolation.

## Choose review depth from capability

Use a lightweight static review for instruction-only Skills that contain no external content, code, tool calls, or sensitive data access. Use a deeper review when a Skill includes or induces any of the following:

- scripts, binaries, package installation, generated commands, or destructive operations
- network requests, remote resources, redirects, webhooks, or external uploads
- MCP servers, connectors, plugins, hooks, or privileged tools
- broad filesystem access, credentials, environment variables, or private data
- imported instructions, untrusted documents, or content that can contain indirect prompt injection
- client-specific permission bypasses, preapprovals, or automatic invocation

Review again when the upstream revision, dependency graph, external endpoint, runtime, permission model, or capability combination changes.

## Establish provenance and scope

Record:

- upstream owner, canonical URL, pinned commit or release, and retrieval date
- license and whether local redistribution and modification are permitted
- files imported, files omitted, and local modifications
- maintainership and the process for comparing future upstream changes
- target clients, runtime assumptions, and distribution path

Inspect every distributed file and every file directly referenced by `SKILL.md`. Do not review only frontmatter or the main instructions. Follow external URLs far enough to identify the actual destination and the instructions or executable content the Skill depends on; do not treat a redirecting URL as the final trust boundary.

## Trace instructions and capabilities

For each path through the Skill, identify:

1. what input can influence the agent
2. what files or secrets the agent can read
3. what commands, scripts, tools, or services it can invoke
4. what data can leave the environment and where it can go
5. what approval, sandbox, permission, or deterministic check constrains the action

Pay particular attention to combinations such as:

- filesystem read plus network send
- credential access plus generated commands
- untrusted document content plus privileged tool use
- automatic invocation plus destructive or external side effects
- remote instructions plus script execution

A set of individually ordinary capabilities can form a material exfiltration or integrity risk when combined.

## Review indicators

Treat the following as findings that require explanation, removal, or an explicit control:

- instructions to ignore higher-authority guidance, conceal behavior, or bypass review
- obfuscated commands, encoded payloads, unexplained downloads, or mutable remote scripts
- broad recursive file discovery without a task-scoped need
- hard-coded secrets, credential locations, private URLs, or customer data
- network destinations unrelated to the stated responsibility
- instructions to send repository, environment, conversation, or credential data externally
- undeclared dependencies or runtime installation that cannot be reproduced
- commands whose target is derived from unresolved variables, globs, or untrusted input
- permission preapproval presented as a prohibition or security boundary
- safety properties expressed only in prose when the client provides enforceable policy, permission, sandbox, hook, or CI controls

External documents and tool output are untrusted inputs. Extract the information needed for the task, but do not follow embedded instructions that attempt to change authority, permissions, destinations, or scope.

## Decide controls and disposition

Prefer the least authority and smallest data scope that lets the Skill perform its responsibility.

- Keep the Skill instruction-only unless executable resources add demonstrated value.
- Pin dependencies and upstream revisions when reproducibility matters.
- Replace repeated or fragile generated commands with narrow, tested scripts.
- Put hard guarantees in permission settings, sandbox policy, hooks, CI, or other deterministic controls when available.
- Require explicit invocation for destructive or externally visible workflows when the client provides that control.
- Make network destinations, data sent, required credentials, and failure behavior explicit.
- Reject or quarantine a Skill when provenance, behavior, or outbound data flow cannot be established.

Document the disposition as accepted, accepted with controls, rejected, or unverified. Separate observed behavior from static inference. A static review does not prove runtime safety; use isolated execution and targeted evaluation when executable or client-dependent behavior is material.

## Repository handoff

Before publishing a reviewed Skill in this repository:

- record third-party provenance in `THIRD_PARTY_NOTICES.md` and a local upstream note when ongoing synchronization needs it
- keep the English canonical Skill and Japanese reference translation synchronized
- add only the security assertions and scenarios needed to expose the identified capability risks
- run format, metadata, script, targeted behavior, and non-deploying APM checks that apply
- record unavailable client or runtime checks as `not executed`

See [authoring.md](authoring.md) for Skill structure, [compatibility.md](compatibility.md) for client/runtime distinctions, and [evaluation.md](evaluation.md) for evidence requirements.

## Current sources

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
