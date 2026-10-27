# Install and update the Skills

This guide is for people who want to use the Skills in this repository.\
It explains how to choose an installation method, how to install and update the Skills with each method, and how to check that they work.

There are two installation methods: APM and the plugin ZIP.\
Both install the same Skills from this repository's `skills/` directory.

## Choose an installation method

### Clients each method supports

| Method | Clients |
| --- | --- |
| APM | Claude Code, Codex, Cursor, and the other [targets that APM supports](https://microsoft.github.io/apm/reference/targets-matrix/) |
| Plugin ZIP | ChatGPT (Chat, Work, and dots), Codex, and Cursor |

APM installs the Skills directly from this repository.\
The plugin ZIP is not published, so you need to build it yourself before installing it.

A plugin uploaded to ChatGPT is also available in Codex.\
This has been checked in Codex and dots in the Codex app, and in Chat and dots in ChatGPT in a browser.

### Choose by where you use the Skills

1. **You also use ChatGPT (Chat, Work, or dots)**
   - Use the plugin ZIP, because it is the only method that ChatGPT supports.
   - Do not also install the Skills with APM for Codex.\
     The plugin is already available in Codex.
2. **You use Codex but not ChatGPT**
   - Use APM.\
     You do not need to build the plugin ZIP.
3. **You use Claude Code**
   - Use APM.\
     This plugin has no Claude-specific manifest.
4. **You use Cursor**
   - Use APM, unless you already use the plugin ZIP for ChatGPT.
   - You can also extract the plugin ZIP into Cursor's local plugin directory.

### Do not install the same Skills twice

In each environment, install each Skill through only one method.\
Before you enable the plugin, disable or remove the same Skills installed through another plugin or through APM, including APM installations of individual Skills by path.

- APM installs Skills for Codex and Cursor into the same `.agents/skills/` directory.\
  An APM installation for Cursor therefore also makes the Skills visible to Codex in that project.
- Use the client's own controls to disable or remove duplicates.
- Do not remove unrelated Skills or credentials.
- Do not rely on undocumented precedence or namespaces to decide which duplicate the client uses.

Installing a Skill makes its instructions available to the client.\
It does not give the agent shell, repository, external-service, subagent, or write access.\
Check the [runtime requirements](compatibility.md) of the work you plan.

## Install with APM

### Choose what to install

| What to install | Command |
| --- | --- |
| All public Skills | `apm install mtk177a/skills` |
| Selected Skills | `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing` |
| One Skill by path | `apm install mtk177a/skills/skills/review-changes` |

`cognitive-rhythm-writing` reads the `japanese-tech-writing` Skill, so install the two together, as in the selected example.

To update installed Skills to the latest version, run `apm update` in the consumer repository.

### Declare the Skills as a dependency

To declare all public Skills as a dependency instead, add this repository to the `apm.yml` of your consumer repository:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

### Check the installation

After installing, check the following in the client:

1. **The Skills are where the client reads them**
   - See the [APM targets matrix](https://microsoft.github.io/apm/reference/targets-matrix/) for the directory each client uses.
2. **The client lists the Skills**
3. **You can invoke a Skill explicitly**

A successful `apm install` does not show that the client can use the Skills.

## Install from the plugin ZIP

### Build the plugin ZIP

The plugin ZIP is not published.\
Build it by following [Build the plugin ZIP](../maintainers/packaging.md).

### Use the plugin in ChatGPT and Codex

1. **Upload the plugin ZIP to ChatGPT**
   - For the first installation, upload it as a personal plugin in ChatGPT Plugins.
   - To update, first keep the previous ZIP so that you can go back to it.\
     Then select **Upload new version** from the existing plugin's menu instead of creating another plugin.
2. **Check the version and Skills**
   - Check that the plugin shows the new version and the expected Skills.
   - Then start a new conversation.
3. **Name the Skill in your request**
   - Select the plugin in the UI and name the Skill in your request.
   - For example: “Use `define-referents` from `mtk177a-skills` and read its reference before proposing names.”
4. **Check each place you use the plugin**
   - Check ChatGPT's Chat, Work, and dots, and Codex separately, because how you invoke a Skill and which capabilities are available can differ.
   - Discovery: the Skill appears in the list.
   - Loading: the client shows that it read the Skill body and references, if it can show this.
   - Output: the answer you received.\
     A plausible answer alone does not show that the Skill was loaded.

### Use the plugin in Cursor

[Cursor's documentation](https://cursor.com/docs/plugins) describes support for portable Agent Plugins and local testing under `~/.cursor/plugins/local/<plugin-name>/`.

1. **Extract the plugin ZIP**
   - Extract it so that `plugin.json` sits directly inside `~/.cursor/plugins/local/mtk177a-skills/`.
   - To update, back up the old directory if you need it, then replace the whole directory.\
     Copying new files over the old ones can leave removed Skills behind.
2. **Reload Cursor**
   - Restart Cursor, or run **Developer: Reload Window**.
3. **Check the Skills**
   - Check that Cursor lists the Skills and that you can invoke one explicitly.
   - If the Skills do not appear, check that local plugin imports are allowed.\
     Cursor discovers plugins in this directory only when they are.

This plugin contains only Skills, so it does not need `.cursor-plugin/plugin.json`.\
Submitting it to the Cursor marketplace is outside this guide.
