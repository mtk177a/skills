# Plugin distribution

`mtk177a-skills` distributes the public `skills/` catalog as one portable Agent Plugin.\
The plugin and standalone/APM installations use the same Skill sources, so maintainers can update `skills/` without maintaining separate distribution copies.

For installation, start with [Choose an installation route](#choose-an-installation-route).\
For archive preparation, follow [Build and verify an archive](#build-and-verify-an-archive).\
The [compatibility guide](compatibility.md#plugin-runtime-requirements) describes the capabilities and inputs required by each Skill.

## Choose an installation route

Choose one delivery route for overlapping Skills in each runtime:

| Target | Route |
| --- | --- |
| ChatGPT and Codex | Upload the ZIP as a personal ChatGPT plugin, then check availability in each intended surface |
| Cursor | Extract the same ZIP into Cursor's local plugin directory |
| Claude Code | Continue using the existing [APM installation](../README.md#claude-code-apm); this package does not add a Claude-specific plugin manifest |

Before enabling the plugin, identify and disable or remove overlapping plugin, standalone, or APM installations using the client's supported controls.\
Do not remove unrelated Skills or credentials, or rely on undocumented precedence or namespaces to resolve duplicates.\
Retain the previous archive for recovery and verify the plugin in a new conversation.

Installing a plugin makes its packaged instructions available; it does not grant shell access, repository access, external connections, subagents, or write permissions.\
A Skill can therefore be installed but still lack the capabilities required for a particular task.

## Install or update the plugin

### ChatGPT and Codex

The user uploads the archive manually.\
The builder does not upload files or change account settings.

1. For the first installation, upload the ZIP through the personal plugin archive upload in ChatGPT Plugins.\
   For an update, open the existing plugin's menu and select **Upload new version** instead of creating another plugin.
2. Check the displayed version and Skill list, then start a new conversation.
3. Select the plugin with the available UI and name the intended Skill in the request.\
   For example: “Use `define-referents` from `mtk177a-skills` and read its reference before proposing names.”
4. In each intended surface, check Skill discovery, body/reference reading when observable, and the resulting output separately.

Chat, Work, dots, and Codex may differ in invocation syntax and runtime capabilities.\
A plausible answer alone does not prove that the Skill was loaded; distinguish observed loading from the resulting output.

### Cursor

[Cursor's documentation](https://cursor.com/docs/plugins) describes support for portable Agent Plugins and local testing under `~/.cursor/plugins/local/<plugin-name>/`.

1. Extract the ZIP into `~/.cursor/plugins/local/mtk177a-skills/`, with `plugin.json` directly inside that directory.\
   When updating, preserve any needed backup and replace the old extracted directory as a whole.\
   Copying new files over old ones can leave removed Skills behind.
2. Restart Cursor or use **Developer: Reload Window**.
3. Verify Skill discovery and explicit use.

This Skills-only package does not need `.cursor-plugin/plugin.json`.\
Marketplace submission is outside this workflow.

## Package contents and source files

The root `plugin.json` is the only maintained plugin manifest and declares the Agent Plugins 1.0.0 schema.\
OpenAI-specific settings, when needed, belong under `extensions["com.openai"]` in that file.\
Do not maintain a second `.codex-plugin/plugin.json`: OpenAI accepts that compatibility format, but an inline OpenAI extension replaces its settings rather than merging them.\
See [OpenAI packaging](https://developers.openai.com/plugins/build/plugins).

The builder selects files from the requested Git commit:

- Include root `plugin.json`, `LICENSE`, and `THIRD_PARTY_NOTICES.md`.
- Include tracked files under public `skills/`, including references, runtime resources, metadata, both upstream mirrors, and their `UPSTREAM.md` provenance files.\
  Exclude `evals/` directories and filenames ending in `-ja.md` or `.ja.md`.
- Exclude repository instructions, tests, documentation, and repository maintenance Skills under `.agents/`.

Included files retain their original bytes.\
New tracked files under `skills/` are distribution candidates, so review additions before committing for scripts, external references, credentials, and generated output.

There is no enclosing directory above `plugin.json` and `skills/`.\
All public Skills are packaged, but their [runtime requirements](compatibility.md#plugin-runtime-requirements) still apply.

## Build and verify an archive

Use Python 3.10 or later and Git.\
The builder uses no additional Python dependencies and performs no network requests, installation, or upload.

1. **Prepare the source commit.**\
   Keep Skill bodies and resources in `skills/`; do not maintain separate distribution copies.\
   For an update, run the checks relevant to the changed Skill responsibilities and increment the version in `plugin.json`.\
   Commit the version and source changes before building; never distribute different content under an already distributed version.

2. **Check the source and build the ZIP.**\
   Use a checkout at the same revision as the source commit to be packaged.\
   Replace `<commit>` with that commit and `<outside-repository-output-directory>` with an output directory outside the repository.

   ```bash
   python3 -B scripts/check_repository.py
   python3 -B -m unittest discover -s tests
   git diff --check
   python3 -B scripts/build_plugin.py --ref <commit> --output-dir <outside-repository-output-directory>
   ```

   The builder resolves the reference once to a commit and reads committed files only; uncommitted and untracked files are excluded.\
   Existing output files cause an error rather than being overwritten.

3. **Verify installation from the pushed commit.**\
   Push the candidate branch, then follow the [APM checks](compatibility.md#validation) against that exact commit from disposable consumer directories outside this repository.\
   Cover the full bundle, affected selections and individual paths, frozen install, and audit.\
   Do not run non-dry-run APM installation in the source checkout.

4. **Retain the artifacts and verification results.**\
   Keep the ZIP, hash, source commit, change summary, and verification results together.\
   The user can then upload the archive and check the update using the installation steps above.\
   Publishing artifacts through GitHub Releases requires separate authorization.

### Generated files

| Output | Purpose |
| --- | --- |
| `<name>-<version>.zip` | Plugin archive to install |
| `<name>-<version>.sha256` | SHA-256 hash for identifying the archive's exact contents |
| `<name>-<version>.build.json` | Source commit, archive hash, Skill list, and each packaged file's hash and mode |

Sorted entries, fixed timestamps, and uncompressed storage make repeated ZIP builds byte-identical without depending on a compression-library version.

### What the builder verifies

The builder checks:

- Supported manifest identity fields, required root files, and each Skill's `SKILL.md` entrypoint.
- Mirror hashes against the recorded provenance.
- Relative Markdown links and explicit `references/` or `../` code-span references against the selected package.
- Absence of symlinks and submodules in included paths.
- Every ZIP entry's contents and file mode against the original Git blob and mode.

These checks cover specific packaging failures; they are not complete JSON Schema validation, full Markdown parsing, or behavioral evaluation.\
When a Skill changes, separately review generic examples, plain-text references, tool availability, and conditional instructions that these checks cannot establish.

## Recover from a faulty version

Restore the needed previous source content and distribute it under a new version, using the same build, installation, and verification steps.
