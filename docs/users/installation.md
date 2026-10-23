# Install and update the Skills

This guide is for people who want to use the Skills in this repository.\
It explains how to install and update them in each client and how to check that they work.

You can install the Skills in two ways: with APM, or from the plugin ZIP.\
Both ways install the same Skills from this repository's `skills/` directory.\
APM installs them directly from this repository.\
The plugin ZIP is not published, so you need to build it yourself by following [Build the plugin ZIP](../maintainers/packaging.md).

## Choose an installation method

Choose the method for the client you use:

| Client | Method |
| --- | --- |
| Claude Code and other clients that APM supports | [Install with APM](#install-with-apm) |
| ChatGPT and Codex | [Upload the plugin ZIP to ChatGPT](#upload-the-plugin-zip-to-chatgpt) |
| Cursor | [Extract the plugin ZIP for Cursor](#extract-the-plugin-zip-for-cursor) |

Claude Code uses APM because this plugin has no Claude-specific manifest.

Installing a Skill makes its instructions available to the client.\
It does not give the agent shell, repository, external-service, subagent, or write access.\
Before you choose a client, check the [runtime requirements](compatibility.md) of the work you plan.

## Avoid duplicate installations

In each environment, install each Skill through only one method.\
If the same Skills are already installed through another plugin, a standalone installation, or APM, disable or remove the duplicates before you enable the plugin.

- Use the client's own controls to disable or remove them.
- Do not remove unrelated Skills or credentials.
- Do not rely on undocumented precedence or namespaces to decide which duplicate the client uses.

## Install with APM

Run the command for what you want to install:

| What to install | Command |
| --- | --- |
| All public Skills | `apm install mtk177a/skills` |
| Selected Skills | `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing` |
| One Skill by path | `apm install mtk177a/skills/skills/review-changes` |

`cognitive-rhythm-writing` reads the `japanese-tech-writing` Skill, so install the two together, as in the selected example.

To declare all public Skills as a dependency instead, add this repository to the `apm.yml` of your consumer repository:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

After installing, check the following in the client:

- The Skills are in the location the client reads them from.
- The client lists the Skills.
- You can invoke a Skill explicitly.

A successful `apm install` does not show that the client can use the Skills.

## Upload the plugin ZIP to ChatGPT

Upload the plugin ZIP to ChatGPT as a personal plugin.\
Codex uses the same personal plugin, so you do not upload it separately for Codex.

1. Upload the plugin ZIP.\
   For the first installation, upload it as a personal plugin in ChatGPT Plugins.\
   To update, first keep the previous ZIP so that you can go back to it.\
   Then select **Upload new version** from the existing plugin's menu instead of creating another plugin.
2. Check that the plugin shows the new version and the expected Skills, then start a new conversation.
3. Select the plugin in the UI and name the Skill in your request.\
   For example: “Use `define-referents` from `mtk177a-skills` and read its reference before proposing names.”
4. Check the following in each place you plan to use the plugin, such as ChatGPT's Chat, Work, and dots, and Codex:
   - Discovery: the Skill appears in the list.
   - Loading: the client shows that it read the Skill body and references, if it can show this.
   - Output: the answer you received.\
     A plausible answer alone does not show that the Skill was loaded.

How you invoke a Skill and which capabilities are available can differ between ChatGPT's Chat, Work, and dots, and Codex.

## Extract the plugin ZIP for Cursor

Extract the plugin ZIP into Cursor's local plugin directory.\
[Cursor's documentation](https://cursor.com/docs/plugins) describes support for portable Agent Plugins and local testing under `~/.cursor/plugins/local/<plugin-name>/`.

1. Extract the ZIP so that `plugin.json` sits directly inside `~/.cursor/plugins/local/mtk177a-skills/`.\
   To update, back up the old directory if you need it, then replace the whole directory.\
   Copying new files over the old ones can leave removed Skills behind.
2. Restart Cursor, or run **Developer: Reload Window**.
3. Check that Cursor lists the Skills and that you can invoke one explicitly.

This plugin contains only Skills, so it does not need `.cursor-plugin/plugin.json`.\
Submitting it to the Cursor marketplace is outside this guide.
