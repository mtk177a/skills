# Runtime requirements and client differences

This guide is for people who use the Skills in a client.\
It explains what the agent needs to run the Skills, which Skills need more than that, and how clients differ in invoking Skills and controlling tools.\
Read it when you choose a client, and before you start work that writes files, uses the web, or starts a subagent.

## What every Skill needs

1. **The client can read the files in each Skill's directory**
   - Some Skills read files bundled with them, not only `SKILL.md`.\
     `define-referents` and `write-natural-japanese` read a bundled reference in full before they start.
   - The Skills contain no scripts, so the client does not need to run code or install Python libraries for them.
2. **The agent can reach the material the work is about**
   - For work on a repository, the agent needs the files and diffs.\
     For work on logs, documents, or external services, it needs access to those.
   - What the agent could not inspect stays unchecked, even if the answer reads as complete.
3. **The actions the work involves are allowed**
   - Writing files, acting on external services, and starting subagents need two things: the client's permission settings must allow them, and you must allow them in your request.
   - Installing or invoking a Skill allows neither.\
     Each Skill states which actions it does not take without your request.

## Skills with additional requirements

Only the three Skills below need more than the requirements above.

### Web access

`research-web-safely` searches the web and reads the sources it cites.\
If the client has no web access, the Skill reports the affected claims as not verified instead of answering from memory.

### An independent subagent

`revise-docs-fresh-eyes` has a subagent revise the document without the conversation in which the document was written.\
It works only in Codex and Claude Code, where it can start such a subagent.\
If subagents are unavailable or not allowed, the Skill reports that the revision was not done and stops.

### Another Skill installed alongside

`cognitive-rhythm-writing` reads `japanese-tech-writing` before it starts, so install the two Skills together.\
No other Skill needs another Skill.\
The connections in [Choose the next Skill](workflows.md) suggest what to use next; they are not dependencies.

## How clients differ

### Invoking a Skill

Clients can choose a Skill on their own when a request matches its description.\
To make sure a specific Skill is used, invoke it explicitly:

| Client | How to invoke a Skill explicitly |
| --- | --- |
| ChatGPT (Chat, Work, and dots) | Select the plugin and name the Skill in your request, as in [Use the plugin in ChatGPT and Codex](installation.md#use-the-plugin-in-chatgpt-and-codex). |
| Codex CLI and IDE extension | Run `/skills`, or type `$` followed by the Skill name. |
| Claude Code | Start your message with `/` followed by the Skill name. |
| Cursor | Type `/` followed by the Skill name in chat. |

For other clients, such as GitHub Copilot and Gemini CLI, check the client's official documentation.

### Controlling tools and actions

Each client controls with its own settings which tools the agent can use and which actions need your approval.\
In Codex, these are the sandbox and approval settings.\
In Claude Code, they are the permission settings.

Check these settings before work that writes files or reaches external services.\
A Skill's instructions do not change what the client allows.

### Official documentation

Client behavior can change between versions.\
When a detail matters to your work, check the current documentation for your client:

- [Codex and ChatGPT: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code: Skills](https://code.claude.com/docs/en/slash-commands)
- [Cursor: Plugins](https://cursor.com/docs/plugins)
