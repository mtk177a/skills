# Install and update the Skills

This guide is for people who want to use the Skills in this repository.\
It explains how to install and update them in each client and how to check that they work.

You can install the Skills in two ways: with APM, or as a plugin ZIP.\
Both methods install the same Skills from this repository's `skills/` directory.\
APM installs them directly from this repository.\
The plugin ZIP is not published, so to use it you need to build it yourself by following [Build a plugin archive](../maintainers/packaging.md).

## Choose an installation method

| Client | Method |
| --- | --- |
| Claude Code and other clients that APM supports | [Install with APM](#install-with-apm) |
| ChatGPT and Codex | [Upload the plugin ZIP to ChatGPT](#upload-the-plugin-zip-to-chatgpt) |
| Cursor | [Extract the plugin ZIP for Cursor](#extract-the-plugin-zip-for-cursor) |

Claude Code uses APM because this package has no Claude-specific plugin manifest.

Installing a Skill makes its instructions available to the client.\
It does not give the agent shell, repository, external-service, subagent, or write access.\
Before you choose a client, check the [runtime requirements](compatibility.md) of the work you plan.

## Avoid duplicate installations

In each environment, install each Skill through only one method.\
If the same Skills are already installed through another plugin, a standalone installation, or APM, disable or remove the duplicates before you enable the plugin.

- Use the client's own controls to disable or remove them.
- Do not remove unrelated Skills or credentials.
- Do not rely on undocumented precedence or namespaces to choose between duplicates.

Keep the previous ZIP so that you can return to it, and check the plugin in a new conversation.

## Install with APM

Choose the command for what you want to install.

| What to install | Command |
| --- | --- |
| All Skills | `apm install mtk177a/skills` |
| Selected Skills | `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing` |
| One Skill by path | `apm install mtk177a/skills/skills/review-changes` |

`cognitive-rhythm-writing` reads the `japanese-tech-writing` Skill, so install the two together, as in the selected example.

To declare all Skills as a dependency instead, add the repository to the consumer's `apm.yml`:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

After installing, check in the client where the Skills were placed, that the client lists them, and that you can invoke one explicitly.\
A successful `apm install` does not show that the client can use the Skills.

## Upload the plugin ZIP to ChatGPT

Upload the ZIP to ChatGPT as a personal plugin, then check it in each surface you plan to use, including Codex.

1. Upload the ZIP.\
   For the first installation, use the personal plugin archive upload in ChatGPT Plugins.\
   To update, select **Upload new version** from the existing plugin's menu instead of creating another plugin.
2. Check that the plugin shows the new version and the expected Skills, then start a new conversation.
3. Select the plugin in the UI and name the Skill in your request.\
   For example: “Use `define-referents` from `mtk177a-skills` and read its reference before proposing names.”
4. In each surface you plan to use, check the following:
   - Discovery: the Skill appears in the list.
   - Loading: the client shows that the Skill body and references were read, when it can show this.
   - Output: the answer you received.\
     A plausible answer alone does not show that the Skill was loaded.

Invocation and available capabilities can differ between surfaces such as Chat, Work, dots, and Codex.

## Extract the plugin ZIP for Cursor

[Cursor's documentation](https://cursor.com/docs/plugins) describes support for portable Agent Plugins and local testing under `~/.cursor/plugins/local/<plugin-name>/`.

1. Extract the ZIP so that `plugin.json` sits directly inside `~/.cursor/plugins/local/mtk177a-skills/`.\
   To update, back up the old directory if you need it, then replace the whole directory.\
   Copying new files over the old ones can leave removed Skills behind.
2. Restart Cursor, or run **Developer: Reload Window**.
3. Check that Cursor lists the Skills and that you can invoke one explicitly.

This package contains only Skills, so it does not need `.cursor-plugin/plugin.json`.\
Submitting it to the Cursor marketplace is outside this guide.
