# Runtime requirements and client differences

This guide is for people choosing where to run the Skills.\
It lists what the agent needs in order to do the work and how clients differ in finding and running Skills.\
Check it before you choose an [installation method](installation.md#choose-an-installation-method).

A Skill that follows the Agent Skills format is not guaranteed to work in every client.\
The client must be able to find, invoke, and run the Skill, and the agent needs the tools and permissions that the work requires.

## Requirements for every Skill

- The agent can read the Skill body and the resources bundled with it.\
  Each Skill states which resources to read.
- For work that uses tools, the agent can access the required repository, files, network, or external services.
- Writing files, acting on external services, and running subagents are authorized.\
  Installing a Skill or plugin does not authorize them.

The public Skills bundle no executable scripts and require no additional Python libraries.\
The work itself may still require tools, permissions, or external evidence.

## Requirements for specific Skills

The plugin contains all public Skills with their instructions unchanged.\
Check these requirements in particular when choosing an environment.

| Skill or work | Requirement |
| --- | --- |
| `define-referents` | The agent reads its required bundled reference before applying the Skill. |
| `cognitive-rhythm-writing` | The agent reads `japanese-tech-writing/SKILL.md`, so both Skills are installed together. |
| `write-natural-japanese` | The agent reads its wording reference in full. |
| Other writing and design Skills | The agent reads the references that each Skill selects or requires. |
| Editing, investigating, or reviewing a repository | The agent can access the actual files, differences, and evidence, and the tools for any checks it runs. |
| `research-web-safely` | The agent can search and retrieve web content and cite observable sources. |
| `revise-docs-fresh-eyes` | The agent runs in Codex or Claude Code and is allowed to start an independent subagent that does not inherit the authoring conversation. |

If an independent subagent is unavailable or prohibited, `revise-docs-fresh-eyes` stops.

Apart from `cognitive-rhythm-writing`, no Skill requires another Skill.\
The connections in the [Skill workflow guide](workflows.md) are suggestions for choosing the next Skill, not dependencies.\
See each Skill for its output, its handling of missing input, and when it stops.

## Differences between clients

Clients differ in how they find, invoke, and constrain Skills:

- **Codex**:
  - Explicit invocation through `/skills` or `$` in the CLI and IDE, and implicit selection, are features of the client.
  - The optional `agents/openai.yaml` supplies OpenAI-specific display and dependency metadata.
  - Sandbox, approvals, rules, and tool access are separate controls.
- **Claude Code**: discovery, invocation, frontmatter, permissions, and hooks are specific to the client.\
  Compatibility with the portable format does not establish how they behave.
- **Cursor**: follow the [Cursor installation steps](installation.md#use-the-plugin-in-cursor), then check discovery and explicit invocation in your Cursor version.
- **Other clients, such as GitHub Copilot and Gemini CLI**: check discovery, invocation, metadata, permissions, and runtime behavior in the current official documentation and in your client version.
- **APM**: installs the `skills/` directory; it does not run Skills.

## Check that the Skills work in your client

Check each of the following separately, because passing one does not establish the others:

- The package format is valid.
- The client installs and lists the Skills.
- You can invoke a Skill.
- Client-specific extensions behave as expected.
- The client enforces the permissions you rely on.
- The agent can access what the work needs.

Client behavior changes independently of the package format.\
When a detail matters to your work, check the current official documentation:

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Skill authoring](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [Cursor Plugins](https://cursor.com/docs/plugins)
