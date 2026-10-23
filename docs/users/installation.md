# Installation and updates

`mtk177a-skills` distributes the public `skills/` catalog as one portable Agent Plugin.\
Plugin and standalone/APM installations use the same sources, without separately maintained distribution copies.

- **Use Skills**: [Choose an installation route](#choose-an-installation-route) and check the [runtime requirements](compatibility.md#plugin-runtime-requirements).
- **Build the ZIP**: [Build a plugin archive](../maintainers/packaging.md).

## Choose an installation route

Choose one delivery route for overlapping Skills in each runtime:

| Target | Route |
| --- | --- |
| ChatGPT and Codex | Upload the ZIP as a personal ChatGPT plugin, then check availability in each intended surface |
| Cursor | Extract the same ZIP into Cursor's local plugin directory |
| Claude Code | Continue using the [APM installation](#install-through-apm); this package does not add a Claude-specific plugin manifest |

**Resolve overlapping installations before enabling the plugin.**

- **Target**: Identify overlapping plugin, standalone, or APM installations; disable or remove them using the client's supported controls.
- **Preserve**: Do not remove unrelated Skills or credentials, or rely on undocumented precedence or namespaces.
- **Recover and verify**: Retain the previous archive and verify the plugin in a new conversation.

Installation makes packaged instructions available; shell, repository, external-service, subagent, and write access remain separate requirements.\
An installed Skill may still lack the capabilities or permissions needed for the task.

## Install or update the plugin

### ChatGPT and Codex

The user uploads the archive manually.\
The builder does not upload files or change account settings.

1. **Upload the ZIP.**
   - First installation: use the personal plugin archive upload in ChatGPT Plugins.
   - Update: select **Upload new version** from the existing plugin's menu instead of creating another plugin.

2. **Check the version and Skill list.**\
   Then start a new conversation.

3. **Select the plugin and Skill.**\
   Use the available UI to select the plugin and name the Skill in the request.\
   For example: “Use `define-referents` from `mtk177a-skills` and read its reference before proposing names.”

4. **Verify each intended surface.**
   - Discovery: does the Skill appear in the list?
   - Loading: were the body and references read, when observable?
   - Output: what answer resulted? A plausible answer alone does not prove loading.

Chat, Work, dots, and Codex may differ in invocation syntax and runtime capabilities.

### Cursor

[Cursor's documentation](https://cursor.com/docs/plugins) describes support for portable Agent Plugins and local testing under `~/.cursor/plugins/local/<plugin-name>/`.

1. **Extract the ZIP.**\
   Place `plugin.json` directly inside `~/.cursor/plugins/local/mtk177a-skills/`.\
   When updating, preserve any needed backup and replace the old extracted directory as a whole.\
   Copying new files over old ones can leave removed Skills behind.
2. **Reload Cursor.**\
   Restart it or use **Developer: Reload Window**.
3. **Verify use.**\
   Check Skill discovery and explicit invocation.

This Skills-only package does not need `.cursor-plugin/plugin.json`.\
Marketplace submission is outside this workflow.

## Install through APM

Use APM for Claude Code or another supported APM target.

| Selection | Command |
| --- | --- |
| All Skills | `apm install mtk177a/skills` |
| Selected Skills | `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing` |
| Individual path | `apm install mtk177a/skills/skills/review-changes` |

`cognitive-rhythm-writing` reads the adjacent `japanese-tech-writing` Skill; install both using the selection above.

Alternatively, declare the bundle in the consumer's `apm.yml`:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

After installation, check the resolved location, discovery, and explicit use in the intended client.\
A successful APM install does not establish client runtime behavior.
