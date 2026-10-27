# Compatibility and runtime requirements

A valid Agent Skills package is not enough to establish that a client can discover, invoke, or execute a Skill.\
Check the intended client's capabilities and the requirements of the task before choosing an [installation route](distribution.md#choose-an-installation-route).

## Common requirements

- The agent can read the Skill body and bundled resources; each Skill specifies which resources to read.
- Tool-dependent work has the required repository, filesystem, network, or external-service access.
- Writes, external actions, and subagent execution have the required authorization.\
  Installing a plugin does not grant it.

The public Skills currently bundle no executable scripts or additional Python dependencies.\
That does not remove a task's need for tools, permissions, or external evidence.

## Plugin runtime requirements

`mtk177a-skills` packages all public Skills without changing their instructions.\
The following requirements need particular attention when choosing an environment:

| Task or Skill | Requirement |
| --- | --- |
| `define-referents` | Read its required bundled reference before applying the Skill |
| `cognitive-rhythm-writing` | Read the adjacent `japanese-tech-writing/SKILL.md`; install the pair together |
| Writing and design Skills | Read the references selected or required by each Skill; `write-natural-japanese` requires its complete wording reference |
| Repository editing, investigation, and review | Access the actual files, differences, and evidence; executing checks requires the corresponding tools |
| `research-web-safely` | Live search/retrieval and observable source citations |
| `revise-docs-fresh-eyes` | Codex or Claude Code with an authorized independent subagent that does not inherit the authoring conversation; stop if subexecution is unavailable or prohibited |

Other workflow mentions are not automatically mandatory companion dependencies.\
Check the individual Skill for its output, missing-input handling, and stopping conditions.\
When instructions or resources change, review the affected requirements and package references together.

## Client-specific behavior

| Client or tool | What to distinguish |
| --- | --- |
| Codex | CLI/IDE explicit invocation through `/skills` or `$` and implicit selection are client behavior. Optional `agents/openai.yaml` supplies OpenAI-specific display and dependency metadata. Sandbox, approvals, rules, and tool access are separate controls |
| Claude Code | Its discovery, invocation, frontmatter, permissions, and hooks are client-specific; portable format compatibility does not establish those behaviors |
| Cursor | Use the [local plugin procedure](distribution.md#cursor), then verify discovery and explicit use in the target version |
| Other clients, including GitHub Copilot and Gemini CLI | Check current official documentation and the target version for discovery, invocation, metadata, permissions, and runtime behavior |
| APM | An installation tool for the root `skills/` catalog, not an execution client |

Add client-specific metadata only when a Skill needs the corresponding invocation control, UI, dependency declaration, or permission behavior.\
Keep `name`, `description`, instructions, and resources portable otherwise.

## Verify the required behavior

Check format, installation/discovery, invocation, client extensions, enforced permissions, and runtime access separately.

Client behavior changes independently of the package format.\
Consult current official documentation when a detail affects the task:

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Skill authoring](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [Cursor Plugins](https://cursor.com/docs/plugins)

Use [security review](security.md) when third-party material or executable capabilities are involved.
